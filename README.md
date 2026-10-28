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

### 1. Tren penjualan dari bulan ke bulan

- **Fakta:** Penjualan bulanan mencapai nilai tertinggi pada Maret 2019, dengan NMV sebesar **Rp 69,39 juta**. Pada akhir 2017 hingga awal 2018, nilai penjualan tercatat jauh lebih rendah dibandingkan periode puncaknya.
- **Analisis:** Data menunjukkan bahwa penjualan mengalami peningkatan dari periode awal hingga mencapai puncak pada Maret 2019. Namun, untuk memastikan apakah penjualan selanjutnya stabil atau mengalami penurunan, diperlukan perbandingan nilai penjualan pada bulan-bulan setelah periode tersebut.
- **Kesimpulan:** Maret 2019 merupakan bulan dengan NMV tertinggi dalam periode pengamatan berdasarkan hasil analisis yang tersedia.

### 2. Kontribusi dan tingkat keberhasilan metode pembayaran

- **Fakta:** Credit Card memberikan kontribusi NMV terbesar, diikuti oleh Gopay, OVO, Debit Card, dan LinkAja. Tingkat keberhasilan transaksi pada seluruh metode pembayaran relatif serupa, yaitu sekitar **94–96%**.
- **Analisis:** Credit Card dan Gopay merupakan dua metode pembayaran dengan kontribusi penjualan terbesar. Sementara itu, perbedaan tingkat keberhasilan antarmetode pembayaran relatif kecil sehingga belum menunjukkan adanya satu metode yang memiliki tingkat kegagalan jauh lebih tinggi dibandingkan metode lainnya.
- **Kesimpulan:** Credit Card menjadi metode pembayaran dengan kontribusi penjualan terbesar, sedangkan tingkat keberhasilan seluruh metode pembayaran relatif sebanding. Pemeriksaan lebih lanjut terhadap penyebab kegagalan diperlukan untuk mengetahui faktor yang memengaruhinya.

### 3. Hubungan penggunaan promo dengan nilai pembelian

- **Fakta:** Sebanyak **3.058 booking berhasil** menggunakan promo, sedangkan **4.074 booking berhasil** tidak menggunakan promo. Rata-rata NMV per booking pada transaksi promo sebesar **Rp 359.683**, lebih rendah dibandingkan transaksi non-promo sebesar **Rp 369.857**. Selisihnya sekitar **2,8%**.
- **Analisis:** Berdasarkan data tersebut, transaksi yang menggunakan promo memiliki rata-rata NMV per booking lebih rendah daripada transaksi tanpa promo. Dengan demikian, data yang tersedia belum menunjukkan bahwa penggunaan promo berkaitan dengan nilai pembelian rata-rata yang lebih tinggi. Namun, perbandingan ini belum membuktikan bahwa promo menyebabkan penurunan nilai pembelian karena karakteristik pelanggan dan jenis transaksi dapat berbeda.
- **Fakta tambahan:** Lima kode promo yang paling banyak digunakan adalah AZ2022, BUYMORE, WEEKENDSERU, XX2022, dan LIBURDONG. Kelimanya mencakup **2.654 dari 3.058 booking promo**, atau sekitar **87%**.
- **Kesimpulan:** Penggunaan promo cukup besar, tetapi rata-rata NMV per booking promo lebih rendah dibandingkan transaksi non-promo. Penggunaan kode promo juga terkonsentrasi pada lima kode utama.

### 4. Karakteristik, pola pembelian, dan persebaran pelanggan aktif

- **Fakta:** Sebanyak **259 pelanggan aktif** menghasilkan **7.132 booking berhasil**, atau rata-rata sekitar **27,5 booking per pelanggan**. Sepuluh pelanggan dengan kontribusi tertinggi menyumbang sekitar **21% dari total pembayaran**. Pelanggan aktif didominasi perempuan sebesar **71%** dan kelompok usia 15–34 tahun sebesar lebih dari **80%**. Jakarta Raya menjadi lokasi dengan jumlah pelanggan terbanyak, diikuti Jawa Barat dan Jawa Tengah.
- **Analisis:** Rata-rata booking per pelanggan menunjukkan bahwa transaksi berulang berperan penting dalam aktivitas penjualan. Selain itu, kontribusi sepuluh pelanggan teratas yang mencapai sekitar 21% menunjukkan adanya konsentrasi pembayaran pada kelompok pelanggan tertentu. Profil demografis dan persebaran lokasi juga memberikan gambaran mengenai karakteristik pelanggan aktif yang tercatat dalam data.
- **Kesimpulan:** Aktivitas transaksi didukung oleh pelanggan yang melakukan pembelian berulang. Pelanggan aktif didominasi perempuan dan kelompok usia 15–34 tahun, sedangkan Jakarta Raya menjadi lokasi dengan jumlah pelanggan terbanyak.
- **Saran:** Pertimbangkan program retensi untuk pelanggan dengan frekuensi atau kontribusi pembelian tinggi. Profil usia, jenis kelamin, dan lokasi pelanggan juga dapat digunakan sebagai bahan evaluasi strategi pemasaran, dengan tetap mempertimbangkan keterbatasan data.

## Teknologi
Python, Pandas, NumPy, Plotly, Streamlit

## Dashboard
**Link Dashboard:https://dashboard-transaction-vdtfpjd8fhyf7gvjzswwn2.streamlit.app/**
