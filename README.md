# Retail Dashboard

Dashboard interaktif berbasis Streamlit untuk menganalisis kinerja penjualan retail berdasarkan tren penjualan bulanan, performa produk, kontribusi negara dan kanal pemasaran, serta karakteristik pelanggan. Dashboard ini dirancang untuk membantu pengguna memahami pola penjualan dan mengevaluasi kinerja bisnis berdasarkan data transaksi.

## Tujuan

Dashboard ini digunakan untuk menjawab pertanyaan berikut:

1. Bagaimana tren penjualan dari bulan ke bulan, dan kapan penjualan mencapai nilai tertinggi?
2. Produk apa yang memberikan kontribusi terbesar terhadap pendapatan dan jumlah unit terjual?
3. Kanal pemasaran mana yang menghasilkan pendapatan terbesar?
4. Negara mana yang memberikan kontribusi terbesar terhadap penjualan?
5. Bagaimana karakteristik pelanggan aktif dan tingkat konsentrasi penjualan pada pelanggan tertentu?
6. Bagaimana data pembatalan transaksi memengaruhi evaluasi kinerja penjualan?

## Data

- **Sumber:** Dataset retail yang telah dibersihkan dan diproses, yaitu `cleaned_retail_with_flags.csv` dan `cleaned_retail_active.csv`.
- **Jumlah data awal:** 198 baris transaksi, termasuk catatan pembatalan dan biaya pengiriman.
- **Data aktif:** 193 baris setelah catatan pembatalan dikeluarkan.
- **Periode:** 2 Januari 2011 – 10 Desember 2011.
- **Mata uang:** Dataset menggunakan nilai asli dalam Pound Sterling (GBP). Untuk penyajian dalam Rupiah, digunakan asumsi konversi £1 = Rp22.000 sesuai konfigurasi yang menjadi acuan dashboard.
- **Variabel utama:** Nomor transaksi, kode dan nama produk, kuantitas, tanggal transaksi, harga satuan, ID pelanggan, negara, kanal pemasaran, serta penanda pembatalan dan biaya pengiriman.

### Definisi metrik

| Metrik | Rumus atau definisi |
|---|---|
| Gross Revenue | Kuantitas × harga satuan sebelum penyesuaian pembatalan. |
| Active Revenue | Pendapatan transaksi aktif setelah penyesuaian pembatalan. |
| Total Orders | Jumlah nomor transaksi unik sesuai kriteria perhitungan. |
| Active Customers | Jumlah pelanggan unik yang memiliki transaksi aktif. |
| Average Order Value (AOV) | Total pendapatan produk aktif ÷ jumlah transaksi produk aktif yang unik. |
| Product Performance | Kontribusi produk berdasarkan pendapatan dan jumlah unit terjual. |
| Channel Performance | Pendapatan yang tercatat pada setiap kanal pemasaran. |
| Country Performance | Pendapatan yang tercatat pada setiap negara. |
| Cancellation Records | Jumlah baris transaksi yang ditandai sebagai pembatalan. |

Nilai penjualan untuk analisis produk dihitung dari transaksi aktif berjenis `Product Sale`. Biaya pengiriman dipisahkan dari pendapatan penjualan produk. Pembatalan dikeluarkan dari perhitungan pendapatan aktif.

## Ringkasan Hasil

| Indikator | Hasil |
|---|---:|
| Pendapatan produk aktif | Rp75.497.620 |
| Transaksi produk aktif | 186 |
| Pelanggan aktif | 163 |
| Rata-rata nilai transaksi (AOV) | Rp405.901 |
| Produk unik terjual | 170 |
| Total unit produk terjual | 2.043 |
| Negara dengan penjualan terbesar | United Kingdom |
| Kanal dengan pendapatan terbesar | Instagram Ads |
| Bulan dengan pendapatan tertinggi | Mei 2011 |
| Pendapatan tertinggi bulanan | Rp12.432. - |

*Catatan: Pendapatan produk aktif sebesar £3.431,71 dikonversi menggunakan asumsi kurs Rp22.000 per £1. Nilai pendapatan bulanan tertinggi pada Mei 2011 adalah £565,09 atau Rp12.432. - jika dibulatkan ke ribuan rupiah terdekat.*

## Temuan Utama

### 1. Tren penjualan dari bulan ke bulan

- **Fakta:** Penjualan produk aktif mencapai nilai tertinggi pada Mei 2011 sebesar £565,09 atau sekitar Rp12,43 juta. Juni 2011 menyusul dengan £559,45 atau sekitar Rp12,31 juta. Nilai penjualan terendah tercatat pada Februari 2011, yaitu £147,10 atau sekitar Rp3,24 juta.
- **Analisis:** Penjualan meningkat dari Februari hingga mencapai puncak pada Mei dan Juni. Setelah Juni, penjualan berfluktuasi dan tidak mempertahankan nilai puncaknya. Pola ini menunjukkan bahwa kontribusi penjualan tidak merata sepanjang tahun pengamatan.
- **Kesimpulan:** Mei 2011 merupakan bulan dengan pendapatan produk aktif tertinggi, sedangkan Februari 2011 menjadi bulan dengan pendapatan terendah. Perencanaan penjualan perlu mempertimbangkan perubahan kinerja antarbulan.
- **Saran:** Evaluasi produk, kanal pemasaran, dan aktivitas promosi yang berkontribusi terhadap penjualan pada Mei dan Juni sebagai bahan perencanaan periode berikutnya.

### 2. Performa produk

- **Fakta:** Produk *JUMBO BAG RED RETROSPOT* memiliki kontribusi pendapatan terbesar, yaitu £330,00 atau sekitar Rp7,26 juta, dengan total 200 unit terjual. Produk ini berada di posisi teratas berdasarkan pendapatan produk aktif.
- **Analisis:** Kontribusi pendapatan produk menunjukkan bahwa sebagian produk memiliki nilai penjualan lebih besar dibandingkan produk lainnya. Jumlah unit terjual juga memberikan informasi tambahan untuk membedakan produk dengan volume penjualan tinggi dari produk yang memiliki nilai pendapatan tinggi.
- **Kesimpulan:** *JUMBO BAG RED RETROSPOT* menjadi produk unggulan berdasarkan pendapatan pada dataset yang dianalisis. Informasi ini dapat digunakan sebagai dasar evaluasi prioritas persediaan dan strategi pemasaran produk.
- **Saran:** Pantau ketersediaan produk unggulan dan evaluasi konsistensi permintaannya sebelum menetapkan prioritas stok atau promosi.

### 3. Kontribusi kanal pemasaran

- **Fakta:** Instagram Ads mencatat pendapatan produk aktif terbesar, yaitu £744,36 atau sekitar Rp16,38 juta. Kanal berikutnya adalah Retargeting sebesar £520,34, Paid Ads sebesar £493,38, dan Criteo sebesar £484,13.
- **Analisis:** Instagram Ads memberikan kontribusi pendapatan terbesar di antara tujuh kanal yang tercatat. Namun, pendapatan saja belum cukup untuk menyimpulkan bahwa kanal tersebut paling efisien karena data biaya iklan, jumlah klik, konversi, dan laba per kanal tidak tersedia dalam perhitungan ini.
- **Kesimpulan:** Instagram Ads merupakan kanal dengan pendapatan tertinggi berdasarkan data yang dianalisis. Efektivitas biaya pemasaran masing-masing kanal masih perlu dievaluasi menggunakan data biaya dan konversi.
- **Saran:** Lakukan evaluasi lanjutan terhadap biaya iklan, tingkat konversi, dan laba per kanal sebelum memutuskan penambahan anggaran pemasaran.

### 4. Persebaran penjualan berdasarkan negara

- **Fakta:** United Kingdom menghasilkan pendapatan produk aktif sebesar £2.825,45 atau sekitar Rp62,16 juta, setara dengan sekitar 82,3% dari total pendapatan produk aktif. Jerman berada di posisi berikutnya dengan £179,38, diikuti Finlandia dengan £141,63.
- **Analisis:** Pendapatan sangat terkonsentrasi di United Kingdom. Kontribusi negara lain relatif lebih kecil sehingga kinerja penjualan dalam dataset ini sangat bergantung pada pasar utama tersebut.
- **Kesimpulan:** United Kingdom merupakan pasar terbesar berdasarkan pendapatan produk aktif. Negara tersebut menjadi pasar utama yang perlu dipertahankan, sementara pasar lainnya dapat dievaluasi sebagai peluang pengembangan.
- **Saran:** Pertahankan strategi penjualan di United Kingdom dan kaji potensi pertumbuhan di negara lain berdasarkan permintaan, biaya distribusi, dan profitabilitas.

### 5. Karakteristik dan konsentrasi pelanggan

- **Fakta:** Terdapat 163 pelanggan unik pada transaksi produk aktif. Sepuluh pelanggan dengan pendapatan tertinggi menyumbang sekitar 36,9% dari total pendapatan produk aktif.
- **Analisis:** Kontribusi sepuluh pelanggan teratas menunjukkan adanya konsentrasi pendapatan pada kelompok pelanggan tertentu. Kondisi ini dapat menjadi peluang untuk mempertahankan pelanggan bernilai tinggi, tetapi juga perlu diperhatikan karena perubahan aktivitas pembelian kelompok tersebut berpotensi memengaruhi pendapatan.
- **Kesimpulan:** Pelanggan dengan kontribusi pendapatan tinggi merupakan kelompok penting dalam evaluasi kinerja retail. Data yang tersedia belum cukup untuk menyimpulkan karakteristik demografis pelanggan karena informasi yang dianalisis terutama mencakup ID pelanggan dan transaksi.
- **Saran:** Evaluasi frekuensi pembelian, nilai transaksi, dan pembelian berulang untuk menyusun strategi retensi pelanggan berdasarkan perilaku transaksi aktual.

### 6. Pembatalan transaksi dan kualitas data

- **Fakta:** Dataset awal berisi 198 baris, termasuk lima baris yang ditandai sebagai pembatalan dengan nilai bruto £164,06. Setelah pembatalan dikeluarkan, tersisa 193 baris aktif. Dataset juga memuat dua baris biaya pengiriman.
- **Analisis:** Pemisahan transaksi aktif, pembatalan, dan biaya pengiriman membantu menjaga konsistensi perhitungan pendapatan produk. Pembatalan tidak seharusnya dihitung sebagai pendapatan penjualan aktif. Jumlah baris pembatalan juga tidak sama dengan jumlah transaksi unik yang dibatalkan.
- **Kesimpulan:** Penanganan status transaksi merupakan bagian penting dalam menghasilkan ringkasan penjualan yang akurat. Tingkat pembatalan sebaiknya dihitung berdasarkan definisi transaksi unik yang konsisten, bukan hanya jumlah baris.
- **Saran:** Pertahankan penanda pembatalan dan biaya pengiriman dalam proses pengolahan data. Validasi kembali nomor transaksi unik, status transaksi, dan definisi pendapatan sebelum menggunakan dashboard sebagai dasar keputusan bisnis.

## Teknologi

Python, Pandas, NumPy, Plotly, Streamlit.

## Dashboard

**Link Dashboard:** https://dashboard-retail-8rbmvmfhceqrqjpe3jqb5a.streamlit.app/
