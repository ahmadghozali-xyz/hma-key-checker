# HMA Key Checker

**Cek status lisensi HMA VPN dalam hitungan detik — aktif, kadaluarsa, atau tidak valid.**

Program Python sederhana untuk memeriksa banyak kunci lisensi (license key) HMA VPN sekaligus, tanpa perlu login, tanpa captcha, dan tanpa membuka aplikasi HMA VPN.

```
AKTIF     8UD6MX-2WCYYJ-5FC5PE  s/d 2027-09-02 03:08 UTC (336 hari)  | HMA Pro VPN - 1 user, 1 year  | device 7/5
EXPIRED   TRR2ZX-HMTGT2-5RLJUN  s/d 2026-09-28 14:42 UTC (-2 hari)   | HMA Pro VPN - 1 user, 1 year  | device 1/1
INVALID   66LD5V-6E7R22-5FC53N  | key tidak terdaftar
```

---

## Daftar Isi

- [Apa itu program ini?](#apa-itu-program-ini)
- [Untuk siapa README ini?](#untuk-siapa-readme-ini)
- [Persiapan (sekali saja)](#persiapan-sekali-saja)
- [Cara Pakai — Panduan Pemula](#cara-pakai--panduan-pemula)
- [Cara Pakai — Mode Lanjutan](#cara-pakai--mode-lanjutan)
- [Membuat Tabel Rapi (format_table.py)](#membuat-tabel-rapi-format_tablepy)
- [Arti Hasil Pengecekan](#arti-hasil-pengecekan)
- [Pertanyaan yang Sering Ditanyakan](#pertanyaan-yang-sering-ditanyakan)
- [Cara Kerja Program (versi teknis)](#cara-kerja-program-versi-teknis)
- [Pemecahan Masalah](#pemecahan-masalah)

---

## Apa itu program ini?

Bayangkan Anda punya tumpukan kunci lisensi HMA VPN — mungkin dari pembelian, dari catatan lama, atau dari mana saja. Satu per satu dicek lewat aplikasi HMA VPN jelas memakan waktu lama: buka aplikasi, tempel key, tunggu, catat hasilnya, ulangi.

Program ini melakukan semua itu secara otomatis:

- **Cek banyak key sekaligus** — ratusan key dalam sekali jalan
- **Beri tahu status tiap key** — masih aktif, sudah kadaluarsa, atau tidak terdaftar
- **Tampilkan tanggal kadaluarsa** dan sisa harinya
- **Tampilkan detail produk** (HMA Pro VPN 1 tahun, 3 tahun, dll.)
- **Simpan hasilnya ke file** yang bisa dibuka di Excel atau Notepad
- **Gratis dan terbuka** — kodenya bisa Anda baca sendiri, tidak ada data yang dikirim ke mana pun selain server resmi HMA/Avast

> **Catatan:** Program ini hanya **membaca status** lisensi yang sudah ada. Ia tidak membuat key baru, tidak membobol apa pun, dan tidak mengubah data lisensi. Sama seperti memasukkan key ke aplikasi HMA untuk melihat "apakah key saya masih berlaku?" — hanya saja dilakukan otomatis dan sekaligus banyak.

---

## Untuk siapa README ini?

| Anda... | Mulai dari |
|---|---|
| Baru pertama kali pakai Python atau terminal | [Cara Pakai — Panduan Pemula](#cara-pakai--panduan-pemula) |
| Sudah terbiasa dengan terminal | [Mode Lanjutan](#cara-pakai--mode-lanjutan) |
| Penasaran cara kerjanya di balik layar | [Cara Kerja Program](#cara-kerja-program-versi-teknis) |

---

## Persiapan (sekali saja)

Anda hanya butuh **Python** — sebuah program gratis yang membuat komputer bisa menjalankan skrip.

### Langkah 1 — Pasang Python (kalau belum ada)

**Windows:**

1. Buka <https://www.python.org/downloads/> lalu klik tombol besar **Download Python**
2. Jalankan file yang terunduh
3. ⚠️ **PENTING:** di layar pertama pemasangan, centang kotak **"Add Python to PATH"** di bagian bawah — ini yang paling sering terlewat
4. Klik **Install Now**, tunggu selesai

**macOS / Linux:** Python biasanya sudah terpasang. Cek dengan membuka Terminal dan mengetik `python3 --version`.

### Langkah 2 — Pastikan Python sudah terpasang

Buka **Command Prompt** (Windows: tekan `Win`, ketik `cmd`, tekan Enter) atau **Terminal** (macOS/Linux), lalu ketik:

```
python --version
```

Kalau muncul sesuatu seperti `Python 3.11.5`, berarti siap. Kalau muncul error "not recognized", lihat bagian [Pemecahan Masalah](#pemecahan-masalah).

### Langkah 3 — Unduh program ini

**Cara mudah (tanpa Git):**

1. Klik tombol hijau **Code** di halaman GitHub ini
2. Pilih **Download ZIP**
3. Ekstrak file ZIP ke folder yang mudah diingat, misalnya `C:\HMA-Checker` atau `Dokumen\HMA-Checker`

**Cara untuk yang sudah pakai Git:**

```
git clone https://github.com/ahmadghozali-xyz/hma-key-checker.git
cd hma-key-checker
```

### Langkah 4 — Masuk ke folder program

Di Command Prompt / Terminal, arahkan ke folder tempat Anda mengekstrak program:

```
cd C:\HMA-Checker
```

> **Tips:** setelah mengetik `cd ` (dengan spasi), Anda bisa *drag-and-drop* foldernya ke jendela Command Prompt — jalur foldernya akan terisi otomatis.

---

## Cara Pakai — Panduan Pemula

### Skenario 1: Cek satu atau dua key

Ketik ini di Command Prompt (ganti dengan key Anda):

```
python hma_checker.py 8UD6MX-2WCYYJ-5FC5PE
```

Hasilnya langsung muncul di layar:

```
Cek 1 key (1 request)...

AKTIF     8UD6MX-2WCYYJ-5FC5PE  s/d 2027-09-02 03:08 UTC (336 hari)  | HMA Pro VPN - 1 user, 1 year  | device 7/5

Ringkasan: 1 aktif, 0 expired, 0 invalid, 0 error
```

### Skenario 2: Cek banyak key dari sebuah file

Ini kegunaan utama program ini.

**Langkah 1** — Buat file teks biasa (pakai Notepad) bernama `keys.txt`, isi satu key per baris:

```
8UD6MX-2WCYYJ-5FC5PE
DHMMTF-QGDG8J-584F52
L55V52-8LJLPJ-5GLGJN
TRR2ZX-HMTGT2-5RLJUN
```

> Baris kosong dan baris yang diawali `#` akan diabaikan — berguna untuk memberi catatan.
>
> ```
> # Key dari pembelian Januari
> 8UD6MX-2WCYYJ-5FC5PE
> ```

**Langkah 2** — Jalankan program, sebutkan nama file input dan file hasil:

```
python hma_checker.py -f keys.txt -o hasil.csv
```

**Langkah 3** — Lihat hasilnya di layar, dan buka `hasil.csv` dengan Excel/Notepad untuk melihat seluruhnya.

### Skenario 3: Hasil dalam tabel rapi

File `hasil.csv` dari langkah di atas bentuknya masih mentah (dipisah koma) — pas untuk diolah mesin, tapi kurang enak dibaca mata. Untuk mengubahnya jadi tabel rapi:

```
python format_table.py hasil.csv hasil_rapi.txt
```

Buka `hasil_rapi.txt`, hasilnya seperti ini:

```
# 91 key: 18 AKTIF, 69 EXPIRED, 4 INVALID  |  dicek 2026-10-01
KEY                  | STATUS  | BERAKHIR             |  HARI | MODE         | PRODUK                          | DEVICE
-------------------- | ------- | -------------------- | ----- | ------------ | ------------------------------- | ------
PSBESQ-7MKMDJ-5R4JTJ | AKTIF   | 2026-10-04 23:48 UTC |     4 | TRIAL        | Ultimate Business Security      | 13/100
46VM6P-UKZHY2-5RUJZN | AKTIF   | 2026-10-09 02:54 UTC |     8 | PREAUTHTRIAL | HMA Pro VPN - 1 user, 30 days   | 5/1
...
```

Tabel ini diurutkan otomatis: key **AKTIF** di atas (yang paling cepat habis lebih dulu), lalu **EXPIRED**, terakhir **INVALID**.

---

## Cara Pakai — Mode Lanjutan

Semua opsi yang tersedia:

```
python hma_checker.py [daftar key] [-f file] [-o hasil.csv] [-d detik]
```

| Opsi | Arti | Contoh |
|---|---|---|
| `KEY1 KEY2 ...` | Cek key langsung dari perintah | `python hma_checker.py ABCD-1234-EFGH-5678` |
| `-f, --file` | Baca daftar key dari file (satu per baris) | `-f keys.txt` |
| `-o, --out` | Simpan hasil ke file CSV | `-o hasil.csv` |
| `-d, --delay` | Jeda antar pengecekan, dalam detik (default 2) | `-d 5` |
| `--selftest` | Uji program tanpa koneksi internet | `--selftest` |

**Contoh gabungan** — cek semua key, jeda 5 detik supaya tidak kena batas server, simpan hasilnya:

```
python hma_checker.py -f keys.txt -d 5 -o hasil.csv
```

### Opsi `format_table.py`

```
python format_table.py file_masukan.csv [file_keluaran.txt]
```

Tanpa argumen kedua, tabel dicetak ke layar saja. Dengan argumen kedua, disimpan ke file.

---

## Arti Hasil Pengecekan

| Status | Arti | Yang perlu dilakukan |
|---|---|---|
| **AKTIF** | Key terdaftar dan masih berlaku | Siap dipakai. Cek tanggal kadaluarsanya |
| **EXPIRED** | Key terdaftar, tapi masa berlakunya sudah habis | Tidak bisa dipakai lagi |
| **INVALID** | Key tidak dikenal oleh sistem HMA | Kemungkinan salah ketik, atau bukan key HMA |
| **ERROR** | Pengecekan gagal (biasanya kena batas server) | Tunggu sebentar, lalu cek ulang key tersebut |

**Kolom tambahan:**

| Kolom | Arti |
|---|---|
| **BERAKHIR** | Tanggal & jam key berakhir (zona waktu UTC) |
| **HARI** | Sisa hari. Angka **negatif** berarti sudah lewat sekian hari |
| **MODE** | Jenis lisensi: `PAID` (berbayar), `TRIAL` (percobaan), `PREAUTHTRIAL` |
| **PRODUK** | Nama paket dan durasinya |
| **DEVICE** | Perangkat terpakai / batas maksimum. `5/1` berarti sudah melebihi batas |

---

## Pertanyaan yang Sering Ditanyakan

**Apakah saya perlu akun HMA atau login?**
Tidak. Program ini membaca data lisensi publik dari server resmi — sama seperti saat aplikasi HMA memverifikasi key Anda.

**Apakah aman? Apakah key saya dikirim ke pihak ketiga?**
Aman. Satu-satunya koneksi yang dibuat adalah ke server resmi HMA/Avast (`my-win.avast.com`) — server yang sama yang dipakai aplikasi HMA VPN di komputer Anda. Tidak ada server perantara, tidak ada data yang dikumpulkan.

**Kenapa cuma 2 key per pengecekan?**
Bukan pilihan kami — itu batas dari servernya. Program ini otomatis mengelompokkan key menjadi pasangan-pasangan.

**Kenapa hasilnya kadang "ERROR"?**
Server HMA membatasi jumlah pengecekan per alamat IP dalam jangka waktu tertentu. Kalau kena batas, tunggu beberapa menit sampai beberapa jam, lalu jalankan ulang — program akan mengecek ulang hanya key yang belum berhasil.

**Kenapa pengecekan lambat?**
Karena ada jeda antar pengecekan (default 2 detik) supaya tidak dianggap membanjiri server. Untuk 100 key, perkirakan sekitar 2–3 menit. Jeda bisa diatur dengan `-d`.

**Apakah bisa cek ribuan key sekaligus?**
Bisa, tapi karena batas server per-IP, sebaiknya dibagi beberapa batch dengan jeda longgar. Jalankan dengan `-d 10` atau lebih untuk jumlah besar.

**Kenapa hasil menunjukkan "Avast SMB dummy product"?**
Beberapa key ternyata bukan untuk HMA VPN, melainkan produk Avast lain yang memakai sistem lisensi yang sama. Statusnya tetap valid — hanya produknya berbeda.

---

## Cara Kerja Program (versi teknis)

Bagian ini untuk yang ingin tahu isi dapur. Kalau Anda hanya ingin memakai programnya, silakan lewati.

### Alur singkat

```
keys.txt  ──>  hma_checker.py  ──>  hasil.csv  ──>  format_table.py  ──>  tabel rapi
```

### Detail teknis

Program mengirim permintaan HTTP POST ke endpoint lisensi resmi Avast:

```
POST https://my-win.avast.com/v1/query/get-exact-application-licenses
Content-Type: application/json

{"walletKeys": ["KEY-1", "KEY-2"]}
```

Endpoint ini adalah bagian dari protokol internal Avast bernama **Vaar** (dipakai aplikasi desktop Avast/HMA/AVG). Yang membuatnya bekerja adalah serangkaian header khusus yang menandai permintaan sebagai berasal dari aplikasi HMA VPN:

| Header | Nilai | Keterangan |
|---|---|---|
| `Vaar-Version` | `0` | Versi protokol |
| `Vaar-Header-App-Build-Version` | `12397` | Versi build aplikasi HMA |
| `Vaar-Header-App-Id` | `000...000` | Diisi nol (alphalib memperbolehkannya bila brand diset) |
| `Vaar-Header-App-IPM-Product` | `78` | Kode produk HMA |
| `Vaar-Header-App-Product-Brand` | `PRIVAX` | Merek (HMA = Privax) |
| `Vaar-Header-Device-Id` | 64 karakter heksadesimal | Tidak divalidasi server, boleh acak |

Verdikt ada di **header respons**, bukan di body:

| `Vaar-Status` | `Vaar-Header-Status-Debug` | Arti |
|---|---|---|
| `0` | `OK` | Key ada, body berisi JSON data lisensi |
| `2` | `NONEXISTENT_IDENTIFIER` | Key tidak terdaftar |
| `6` | `RATE_LIMIT_EXCEEDED` | Terlalu banyak permintaan |

Nilai-nilai header di atas diperoleh dengan mengekstrak langsung dari aplikasi HMA VPN resmi yang terpasang di komputer — melalui protokol debug Chromium (CDP) pada antarmuka CEF aplikasi tersebut. Nilai itu spesifik untuk perangkat/produk dan tidak bisa ditebak dari luar.

### Struktur file

```
hma-key-checker/
├── hma_checker.py     # program utama — cek key, hasilkan CSV
├── format_table.py    # ubah CSV jadi tabel rapi
├── keys.txt           # contoh daftar key
└── README.md
```

### Persyaratan teknis

- Python 3.7 atau lebih baru
- Tanpa dependensi pihak ketiga — hanya pustaka standar Python
- Koneksi internet
- Berjalan di Windows, macOS, dan Linux

---

## Pemecahan Masalah

**`python` tidak dikenali / "not recognized"**

Python belum terpasang atau belum masuk PATH. Solusi:

1. Pasang ulang Python dan pastikan centang **"Add Python to PATH"**
2. Atau coba ganti perintah `python` menjadi `python3`
3. Atau `py` (khusus Windows): `py hma_checker.py -f keys.txt`

**Semua hasilnya "ERROR"**

Kemungkinan besar sedang kena batas server (rate limit). Tunggu beberapa menit hingga beberapa jam, lalu jalankan ulang. Program menyimpan hasil ke CSV, jadi Anda bisa langsung mengulang — hanya key berstatus ERROR yang perlu dicek ulang.

**`FileNotFoundError: keys.txt`**

File key tidak ditemukan di folder aktif. Pastikan Anda sudah `cd` ke folder yang benar, atau tulis jalur lengkapnya:

```
python hma_checker.py -f "C:\Users\Nama\Documents\keys.txt" -o hasil.csv
```

**Hasil aneh / sebagian key terlihat "INVALID" padahal aslinya aktif**

Saat dua key dikirim bersamaan dan salah satunya tidak dikenal, server kadang menandai keduanya tidak valid. Jalankan ulang key tersebut satu per satu untuk memastikan.

**Ingin tahu versi Python yang terpasang**

```
python --version
```

---

## Lisensi

MIT — bebas dipakai, diubah, dan dibagikan.

## Penafian

Program ini dibuat untuk memeriksa lisensi milik sendiri. Penggunaan untuk memverifikasi key milik orang lain tanpa izin adalah tanggung jawab pengguna sepenuhnya. Penulis tidak berafiliasi dengan HMA, Privax, atau Avast.
