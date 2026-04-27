# Proyek Analisis Data: Air Quality Data Analysis
# Link Dashboard : https://cdc30implementing-air-quality-dataset-j7ftnvwftl657fkb5uddiq.streamlit.app/
## Deskripsi Proyek
Proyek ini melakukan analisis data kualitas udara (`Air Quality Data Analysis`) untuk memahami tren polusi dan faktor-faktor yang mempengaruhinya di beberapa stasiun pengamatan di Beijing, Tiongkok, selama periode 2013-2017. Analisis ini fokus pada konsentrasi PM2.5, PM10, dan pengaruh kondisi meteorologi seperti kecepatan angin (WSPM).

**Tujuan Utama:**

1.  Menganalisis tren rata-rata konsentrasi PM2.5 bulanan per stasiun (`Dingling`, `Dongsi`, `Gucheng`) dari tahun 2013 hingga 2017, serta mengidentifikasi pola musiman yang konsisten.
2.  Mengevaluasi pengaruh kecepatan angin (WSPM) terhadap tingkat polusi PM10 secara harian di stasiun `Dongsi`, membandingkan perbedaan hubungan ini antara musim kemarau (Mei-September) dan musim hujan (Oktober-April).
## Sumber Data

Data yang digunakan dalam analisis ini berasal dari dataset PRSA (Beijing PM2.5 Data) yang mencakup data kualitas udara dan meteorologi dari beberapa stasiun di Beijing. Dataset ini diperoleh dari repositori GitHub:

*   **Dingling:** `https://raw.githubusercontent.com/Marsello-or/CDC_30_Implementing-Air-Quality-Dataset/refs/heads/main/PRSA_Data_20130301-20170228/PRSA_Data_Dingling_20130301-20170228.csv`
*   **Dongsi:** `https://raw.githubusercontent.com/Marsello-or/CDC_30_Implementing-Air-Quality-Dataset/refs/heads/main/PRSA_Data_20130301-20170228/PRSA_Data_Dongsi_20130301-20170228.csv`
*   **Gucheng:** `https://raw.githubusercontent.com/Marsello-or/CDC_30_Implementing-Air-Quality-Dataset/refs/heads/main/PRSA_Data_20130301-20170228/PRSA_Data_Gucheng_20130301-20170228.csv`

## Library yang Digunakan

Proyek ini menggunakan beberapa library Python populer untuk analisis dan visualisasi data:

*   **`pandas`**: Untuk manipulasi dan analisis data.
*   **`matplotlib`**: Untuk membuat visualisasi statis, interaktif, dan animasi di Python.
*   **`seaborn`**: Berbasis `matplotlib`, menyediakan antarmuka tingkat tinggi untuk menggambar grafik statistik yang menarik dan informatif.
*   **`warnings`**: Untuk mengelola pesan peringatan (digunakan untuk menjaga kerapian output notebook).


## Tahapan Analisis

1.  **Data Gathering**: Mengumpulkan data dari tiga stasiun (`Dingling`, `Dongsi`, `Gucheng`).
2.  **Data Assessing**: Melakukan pengecekan struktur data, tipe data, missing values, dan ringkasan statistik.
3.  **Data Cleaning**: Menangani *missing values* menggunakan interpolasi (`ffill().bfill()`) untuk kolom numerik dan modus untuk kolom kategorikal (`wd`), serta memastikan tidak ada anomali nilai negatif.
4.  **Exploratory Data Analysis (EDA)**: Mengeksplorasi distribusi polutan, faktor meteorologi, dan korelasi antar variabel.
5.  **Visualization & Explanatory Analysis**: Menjawab pertanyaan bisnis menggunakan visualisasi dan analisis mendalam.
6.  **Analisis Lanjutan (Opsional)**: Mengeksplorasi pola harian konsentrasi polutan.

   
## Hasil dan Insight Kunci

### Pertanyaan Bisnis 1: Tren Konsentrasi PM2.5 Bulanan per Stasiun (2013-2017)

*   **Pola Musiman yang Konsisten:** Semua stasiun menunjukkan peningkatan signifikan PM2.5 pada bulan-bulan musim dingin (Oktober-Maret) dan penurunan pada musim panas (Mei-September), dengan puncak polusi di Januari-Februari.
*   **Variasi Antar Stasiun:** `Dongsi` dan `Gucheng` sering memiliki tingkat PM2.5 lebih tinggi dibandingkan `Dingling`.
*   **Tren Jangka Panjang:** Tidak ada tren drastis jangka panjang, melainkan fluktuasi yang didominasi musim.

### Pertanyaan Bisnis 2: Pengaruh Kecepatan Angin Terhadap PM10 di Stasiun Dongsi Berdasarkan Musim (2013-2017)

*   **Musim Kemarau (Mei-September):** Kecepatan angin memiliki pengaruh yang sangat lemah atau hampir tidak ada terhadap PM10 (korelasi: -0.04).
*   **Musim Hujan (Oktober-April):** Terdapat korelasi negatif moderat (korelasi: -0.43), menunjukkan peningkatan kecepatan angin berkorelasi dengan penurunan PM10.
*   **Kesimpulan Perbandingan Musim:** Musim secara signifikan memoderasi hubungan ini, dengan angin lebih efektif dalam mengurangi polusi PM10 di Musim Hujan.

### Analisis Lanjutan: Pola Harian Konsentrasi Polutan (PM2.5 & PM10)

*   **Puncak Polusi:** Konsentrasi PM2.5 dan PM10 cenderung mencapai puncaknya pada dini hari (00:00-05:00) dan malam hari (19:00-23:00).
*   **Penurunan Pagi Hari:** Terjadi penurunan signifikan di pagi hari, kemungkinan karena aktivitas angin atau dispersi atmosfer yang lebih baik.
*   **Implikasi:** Pola harian ini menunjukkan pengaruh gabungan aktivitas manusia dan kondisi meteorologi harian, penting untuk strategi mitigasi polusi.
