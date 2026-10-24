# Transactions Dashboard

Dashboard interaktif berbasis Streamlit untuk menganalisis data transaksi e-commerce: tren penjualan, metode pembayaran, efektivitas promo, dan profil pelanggan.

## Tujuan
Digunakan untuk menjawab pertanyaan berikut: 
1. Bagaimana tren penjualan dari bulan ke bulan?
2. Metode pembayaran mana yang paling besar kontribusinya, dan adakah yang sering gagal?
3. Apakah promo meningkatkan nilai pembelian?
4. Siapa pelanggan aktif dan dari mana mereka berasal?

## Data

- Sumber: `transactions.xlsx` dengan dua sheet, `transactions` dan `customer`, dihubungkan melalui `customer_id`.
- Periode: 15 Juli 2017 – 31 Juli 2022.
  
### Definisi metrik

| Metrik | Rumus |
|---|---|
| NMV | `quantity × price − promo_amount` |
| Total pembayaran | NMV + `shipment_fee` |
| Tingkat keberhasilan | Booking berstatus Success ÷ seluruh booking sesuai filter |
| Pelanggan aktif | Pelanggan unik dengan minimal satu booking Success |

Nilai uang hanya dihitung dari transaksi berstatus **Success**.

## Ringkasan Hasil

| Indikator | Nilai |
|---|---|
| Nilai penjualan (NMV) | Rp 2,61 miliar |
| Booking berhasil | 7.132 |
| Pelanggan aktif | 259 |
| Rata-rata total pembayaran per booking | Rp 374.572 |
| Tingkat keberhasilan | 95,0% (gagal 5,05%) |

## Temuan Utama

### 1. Penjualan stabil sejak pertengahan 2018

- **Fakta:** Puncak penjualan bulanan pada Maret 2019 (Rp 69,39 juta). Pada akhir 2017 hingga awal 2018 nilainya jauh lebih rendah.
- **Interpretasi (hipotesis):** Bisnis melewati fase pertumbuhan awal lalu mencapai level yang relatif stabil. Tidak terlihat tren naik yang jelas dalam beberapa tahun terakhir.

### 2. Credit Card dan Gopay menyumbang lebih dari separuh penjualan, tanpa metode yang bermasalah

- **Fakta:** Urutan NMV dari terbesar: Credit Card, Gopay, OVO, Debit Card, LinkAja. Tingkat keberhasilan semua metode hampir sama (sekitar 94–96%).
- **Interpretasi (hipotesis):** Kegagalan sekitar 5% tersebar merata, sehingga lebih mungkin disebabkan faktor umum.
- **Saran:** Jaga kestabilan Credit Card dan Gopay karena menopang lebih dari separuh penjualan. Selidiki alasan kegagalan jika datanya tersedia.

### 3. Promo dipakai hampir separuh booking, tetapi tidak menaikkan nilai pembelian

| Jenis | Booking berhasil | NMV | Total potongan | Rata-rata NMV per booking |
|---|---:|---:|---:|---:|
| Non-Promo | 4.074 | Rp 1.506.799.147 | Rp 0 | Rp 369.857 |
| Promo | 3.058 | Rp 1.099.910.234 | Rp 16.270.918 | Rp 359.683 |

- **Fakta:** 42,9% booking berhasil memakai promo. Rata-rata NMV per booking promo sekitar 2,8% lebih rendah daripada non-promo. Total potongan hanya sekitar 1,5% dari nilai kotor transaksi promo, atau sekitar Rp 5.300 per booking.
- **Interpretasi (hipotesis):** Potongan relatif kecil dan tidak mendorong pelanggan berbelanja lebih besar.

### 4. Lima kode promo mendominasi penggunaan

| Kode promo | Booking berhasil | Total potongan |
|---|---:|---:|
| AZ2022 | 802 | Rp 3.971.125 |
| BUYMORE | 611 | Rp 3.008.158 |
| WEEKENDSERU | 564 | Rp 2.794.398 |
| XX2022 | 455 | Rp 2.295.601 |
| LIBURDONG | 222 | Rp 1.150.868 |

- **Fakta:** Kelima kode ini mencakup 2.654 dari 3.058 booking promo (sekitar 87%). Potongan per penggunaan hampir sama, sekitar Rp 5.000.

### 5. Basis pelanggan kecil, berulang, dan terkonsentrasi

- **Fakta:**
  - 259 pelanggan aktif menghasilkan 7.132 booking, rata-rata sekitar 27 booking per pelanggan.
  - 10 pelanggan teratas menyumbang Rp 564,3 juta, sekitar 21% dari total pembayaran. Enam dari sepuluhnya berlokasi di luar Pulau Jawa.
  - Pelanggan aktif didominasi perempuan (71%) dan usia 15–34 tahun (lebih dari 80%).
  - Jakarta Raya adalah lokasi dengan pelanggan terbanyak, diikuti Jawa Barat dan Jawa Tengah.
- **Interpretasi (hipotesis):** Bisnis sangat bergantung pada pembeli berulang, sehingga kehilangan beberapa pelanggan teratas berdampak besar pada penjualan.
- **Saran:** Buat program retensi untuk pelanggan teratas, cek apakah mereka pembeli perorangan atau reseller, dan telaah potensi pasar di luar Jawa.

## Catatan dan Keterbatasan

- Analisis ini deskriptif. Kolom "Interpretasi" adalah hipotesis yang perlu diuji dengan data tambahan.
- Bulan pertama (Juli 2017) dan bulan terakhir (Juli 2022) perlu ditafsirkan hati-hati karena bisa jadi tidak mencakup satu bulan penuh.
- Usia pelanggan dihitung pada tanggal transaksi terakhir dalam data (31 Juli 2022).
- Profil pelanggan hanya mencakup pelanggan dengan transaksi berhasil.

## Teknologi

Python, Pandas, NumPy, Plotly, Streamlit
