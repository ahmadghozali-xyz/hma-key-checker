#!/usr/bin/env python3
"""Cek status key HMA VPN (aktif/expired/invalid) via backend resmi Avast my-win.

Pakai:
  python hma_checker.py KEY1 KEY2 ...
  python hma_checker.py -f keys.txt            # satu key per baris
  python hma_checker.py -f keys.txt -o hasil.csv
  python hma_checker.py -f keys.txt -d 5       # jeda 5 detik antar request
  python hma_checker.py --selftest

Rate limit: server membatasi request per IP (Vaar-Status 6, RATE_LIMIT_EXCEEDED,
HTTP tetap 200). Kirim maksimal 2 key per request (batas server) dan beri jeda.
Kalau kena limit: berhenti dulu, jangan polling cepat — polling terus-menerus
memperpanjang window. Bucket IPv4 dan IPv6 terpisah.
"""
import argparse
import csv
import json
import secrets
import socket
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone

EP = "https://my-win.avast.com/v1/query/get-exact-application-licenses"
BATCH = 2          # server limit: walletKeys size 0..2
DELAY = 2.0        # jeda antar request (detik)
RETRY_WAIT = 3.0

DEVICE_ID = secrets.token_hex(32)  # device id tidak divalidasi server, random cukup

HEADERS = {
    "Content-Type": "application/json",
    "Vaar-Version": "0",
    "Vaar-Header-App-Build-Version": "12397",
    "Vaar-Header-App-Id": "00000000-0000-0000-0000-000000000000",
    "Vaar-Header-App-IPM-Product": "78",
    "Vaar-Header-App-Product-Brand": "PRIVAX",
    "Vaar-Header-App-Product-Edition": "HMA_VPN_CONSUMER",
    "Vaar-Header-App-Product-Mode": "PAID",
    "Vaar-Header-Device-Id": DEVICE_ID,
    "Vaar-Header-Device-Platform": "WIN",
}


def check_batch(keys, family=None):
    """Return (vaar_status, licenses, error). vaar_status: 0=ok 2=tidak ada 6=rate limit.

    family: 4 = paksa IPv4, 6 = paksa IPv6, None = default sistem.
    """
    body = json.dumps({"walletKeys": list(keys)}).encode()
    req = urllib.request.Request(EP, data=body, headers=HEADERS, method="POST")
    orig_gai = socket.getaddrinfo
    if family in (4, 6):
        want = socket.AF_INET if family == 4 else socket.AF_INET6
        socket.getaddrinfo = lambda h, p, f=0, t=0, pr=0, fl=0: orig_gai(h, p, want, t, pr, fl)
    try:
        for attempt in range(2):
            try:
                with urllib.request.urlopen(req, timeout=20) as r:
                    raw = r.read()
                    status = int(r.headers.get("Vaar-Status", "-1"))
                    debug = r.headers.get("Vaar-Header-Status-Debug", "")
                return status, (json.loads(raw) if raw else []), debug
            except urllib.error.HTTPError as e:
                msg = e.read().decode("utf-8", "replace")[:200]
                if e.code in (429, 500, 502, 503) and attempt == 0:
                    time.sleep(RETRY_WAIT)
                    continue
                return -1, [], "HTTP %s: %s" % (e.code, msg)
            except Exception as e:
                if attempt == 0:
                    time.sleep(RETRY_WAIT)
                    continue
                return -1, [], str(e)
        return -1, [], "gagal"
    finally:
        socket.getaddrinfo = orig_gai


def classify_from(key, st, lics, debug):
    """Hasil untuk satu key dari respons batch: dict(status, expires, days, mode, product, note)."""
    out = {"key": key, "status": "ERROR", "expires": "", "days": "", "mode": "", "product": "", "note": debug}
    if st == 2:
        out["status"] = "INVALID"
        out["note"] = "key tidak terdaftar"
        return out
    if st == 6:
        out["note"] = "rate limit server"
        return out
    if st != 0 or not lics:
        return out
    lic = next((l for l in lics if key in l.get("walletKeys", [])), None)
    if lic is None:
        out["status"] = "INVALID"
        out["note"] = "tidak ada di respons"
        return out
    exp_ms = lic.get("expires", 0)
    out["expires"] = datetime.fromtimestamp(exp_ms / 1000, tz=timezone.utc).strftime("%Y-%m-%d %H:%M UTC") if exp_ms else ""
    out["days"] = int((exp_ms / 1000 - time.time()) // 86400) if exp_ms else ""
    out["mode"] = lic.get("mode", "")
    out["product"] = lic.get("product", {}).get("name", "")
    usage = lic.get("licenseUsage", {})
    out["note"] = "device %s/%s" % (usage.get("current", "?"), usage.get("maximum", "?"))
    out["status"] = "ACTIVE" if (exp_ms and exp_ms / 1000 > time.time()) else "EXPIRED"
    return out


def classify(key, family=None):
    """Hasil untuk satu key: dict(status, expires, days, mode, product, note)."""
    st, lics, debug = check_batch([key], family=family)
    return classify_from(key, st, lics, debug)


def print_result(res):
    icon = {"ACTIVE": "AKTIF", "EXPIRED": "EXPIRED", "INVALID": "INVALID", "ERROR": "ERROR"}[res["status"]]
    line = "%-9s %s" % (icon, res["key"])
    if res["expires"]:
        line += "  s/d %s (%s hari)" % (res["expires"], res["days"])
    if res["product"]:
        line += "  | %s" % res["product"]
    if res["note"]:
        line += "  | %s" % res["note"]
    print(line, flush=True)


def run(keys, delay, family=None):
    results = []
    batches = [keys[i:i + BATCH] for i in range(0, len(keys), BATCH)]
    for bi, batch in enumerate(batches, 1):
        st, lics, dbg = check_batch(batch, family=family)
        for k in batch:
            res = classify_from(k, st, lics, dbg)
            results.append(res)
            print_result(res)
        if bi < len(batches):
            time.sleep(delay)
    return results


def selftest():
    assert classify.__doc__
    fake_lic = {"walletKeys": ["X"], "expires": (time.time() + 86400) * 1000,
                "mode": "PAID", "product": {"name": "HMA Pro VPN"}, "licenseUsage": {}}
    global check_batch
    real = check_batch
    try:
        check_batch = lambda keys, family=None: (0, [fake_lic], "OK")
        assert classify("X")["status"] == "ACTIVE"
        check_batch = lambda keys, family=None: (2, [], "NONEXISTENT_IDENTIFIER")
        assert classify("X")["status"] == "INVALID"
        check_batch = lambda keys, family=None: (-1, [], "HTTP 500")
        assert classify("X")["status"] == "ERROR"
        check_batch = lambda keys, family=None: (6, [], "RATE_LIMIT_EXCEEDED")
        assert classify("X")["status"] == "ERROR"
        # batch campuran: satu key ada di respons, satu tidak
        check_batch = lambda keys, family=None: (0, [fake_lic], "OK")
        r = classify_from("Y", 0, [fake_lic], "OK")
        assert r["status"] == "INVALID"
    finally:
        check_batch = real
    print("selftest OK")


def main():
    ap = argparse.ArgumentParser(description="Cek key HMA VPN aktif/expired/invalid")
    ap.add_argument("keys", nargs="*", help="key HMA (format XXXX-XXXX-XXXX-XXXX)")
    ap.add_argument("-f", "--file", help="file berisi key, satu per baris")
    ap.add_argument("-o", "--out", help="simpan hasil ke CSV")
    ap.add_argument("-d", "--delay", type=float, default=DELAY, help="jeda antar request dalam detik (default 2)")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()

    if a.selftest:
        selftest()
        return

    keys = list(a.keys)
    if a.file:
        with open(a.file) as f:
            keys += [ln.strip() for ln in f if ln.strip() and not ln.startswith("#")]
    keys = [k.strip().upper() for k in keys]
    keys = list(dict.fromkeys(keys))  # dedupe, jaga urutan
    if not keys:
        ap.error("tidak ada key. Beri key sebagai argumen atau pakai -f keys.txt")

    print("Cek %d key (%d request)...\n" % (len(keys), (len(keys) + BATCH - 1) // BATCH))
    results = run(keys, a.delay)

    if a.out:
        with open(a.out, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=["key", "status", "expires", "days", "mode", "product", "note"])
            w.writeheader()
            w.writerows(results)
        print("\nHasil disimpan: %s" % a.out)

    n = {s: sum(1 for r in results if r["status"] == s) for s in ("ACTIVE", "EXPIRED", "INVALID", "ERROR")}
    print("\nRingkasan: %d aktif, %d expired, %d invalid, %d error" % (n["ACTIVE"], n["EXPIRED"], n["INVALID"], n["ERROR"]))


if __name__ == "__main__":
    main()
