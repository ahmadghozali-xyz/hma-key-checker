#!/usr/bin/env python3
"""Ubah CSV hasil hma_checker.py jadi tabel rapi, pemisah " | ".

Pakai:
  python format_table.py hasil_raw.csv              # cetak ke layar
  python format_table.py hasil_raw.csv hasil.csv    # simpan ke file

Urutan baris: AKTIF (paling cepat berakhir di atas), lalu EXPIRED (paling
baru dulu), terakhir INVALID. Kolom HARI: positif = sisa hari,
negatif = sudah lewat sekian hari.
"""
import csv
import sys
from datetime import datetime

HEADERS = ["KEY", "STATUS", "BERAKHIR", "HARI", "MODE", "PRODUK", "DEVICE"]
RIGHT_ALIGN = {"HARI"}
STATUS_LABEL = {"ACTIVE": "AKTIF"}


def load(path):
    with open(path, encoding="utf-8-sig", errors="replace") as f:
        return list(csv.DictReader(f))


def values(row):
    note = row["note"] or ""
    device = note[7:] if note.startswith("device ") else "-"
    return [
        row["key"],
        STATUS_LABEL.get(row["status"], row["status"]),
        row["expires"] or "-",
        row["days"] or "-",
        row["mode"] or "-",
        row["product"] or "-",
        device,
    ]


def sort_key(row):
    days = int(row["days"]) if row["days"] else 0
    if row["status"] == "ACTIVE":
        return (0, days, row["key"])      # sisa hari paling sedikit dulu
    if row["status"] == "EXPIRED":
        return (1, -days, row["key"])     # paling baru expired dulu
    return (2, 0, row["key"])             # INVALID di bawah


def build(rows):
    rows = sorted(rows, key=sort_key)
    table = [values(r) for r in rows]
    widths = [max([len(HEADERS[i])] + [len(v[i]) for v in table])
              for i in range(len(HEADERS))]

    def fmt(vals):
        cells = []
        for i, v in enumerate(vals):
            v = str(v)
            cells.append(v.rjust(widths[i]) if HEADERS[i] in RIGHT_ALIGN else v.ljust(widths[i]))
        return " | ".join(cells).rstrip()

    counts = {s: sum(1 for r in rows if r["status"] == s) for s in ("ACTIVE", "EXPIRED", "INVALID")}
    lines = [
        "# %d key: %d AKTIF, %d EXPIRED, %d INVALID  |  dicek %s"
        % (len(rows), counts["ACTIVE"], counts["EXPIRED"], counts["INVALID"],
           datetime.now().strftime("%Y-%m-%d")),
        fmt(HEADERS),
        " | ".join("-" * w for w in widths),
    ]
    lines += [fmt(v) for v in table]
    return "\n".join(lines) + "\n"


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return
    text = build(load(sys.argv[1]))
    if len(sys.argv) > 2:
        with open(sys.argv[2], "w", encoding="utf-8") as f:
            f.write(text)
        print("ditulis: %s" % sys.argv[2])
    else:
        sys.stdout.write(text)


if __name__ == "__main__":
    main()
