import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np # Ditambahkan untuk perhitungan regresi linear

# Set Streamlit page configuration
st.set_page_config(layout="wide", page_title="Air Quality Dashboard")

st.title("Dashboard Analisis Kualitas Udara")
st.write("Dashboard ini menampilkan hasil analisis kualitas udara dari tiga stasiun di Beijing: Dingling, Dongsi, dan Gucheng.")

# Fungsi untuk memuat data dengan cache
@st.cache_data
def load_data():
    # Memuat data dari 'main_data.csv' seperti yang diminta pengguna
    try:
        df = pd.read_csv('main_data.csv') # Pastikan file ini ada di direktori yang sama saat deployment
        # Pastikan kolom-kolom terkait waktu bertipe integer jika diperlukan untuk pd.to_datetime
        df['year'] = df['year'].astype(int)
        df['month'] = df['month'].astype(int)
        df['day'] = df['day'].astype(int)
        df['hour'] = df['hour'].astype(int)
    except FileNotFoundError:
        st.error("Error: File 'main_data.csv' tidak ditemukan. Pastikan file CSV ada di direktori yang sama.")
        st.stop()
    return df

df = load_data()

# --- Bagian 1: Tren Rata-rata Konsentrasi PM2.5 Bulanan per Stasiun ---
st.header("1. Tren Rata-rata Konsentrasi PM2.5 Bulanan per Stasiun")
st.write("Grafik ini menunjukkan bagaimana rata-rata konsentrasi PM2.5 berubah dari bulan ke bulan, serta pola musiman yang terjadi di setiap stasiun (2013-2017).")

# Persiapan data untuk BQ1
df_qa1 = df.copy()
df_qa1['YearMonth'] = pd.to_datetime(df_qa1['year'].astype(str) + '-' + df_qa1['month'].astype(str))
pm25_monthly_avg = df_qa1.groupby(['YearMonth', 'station'])['PM2.5'].mean().reset_index()
pm25_monthly_avg = pm25_monthly_avg.sort_values(by=['YearMonth', 'station'])

fig1, ax1 = plt.subplots(figsize=(12, 6))

# Menggunakan matplotlib.pyplot.plot secara manual untuk setiap stasiun
for station in pm25_monthly_avg['station'].unique():
    station_data = pm25_monthly_avg[pm25_monthly_avg['station'] == station]
    ax1.plot(station_data['YearMonth'], station_data['PM2.5'], marker='o', label=station)

ax1.set_title('Tren Rata-rata Konsentrasi PM2.5 Bulanan per Stasiun')
ax1.set_xlabel('Tahun-Bulan')
ax1.set_ylabel('Rata-rata Konsentrasi PM2.5')
ax1.tick_params(axis='x', rotation=45)
ax1.grid(True, linestyle='--', alpha=0.7)
ax1.legend(title='Stasiun')
plt.tight_layout()
st.pyplot(fig1)

st.subheader("Insight Utama BQ1:")
st.markdown("""
-   **Pola Musiman yang Konsisten:** Ketiga stasiun menunjukkan pola musiman yang sangat konsisten. Konsentrasi PM2.5 cenderung **meningkat secara signifikan pada bulan-bulan musim dingin (sekitar Oktober hingga Maret)** dan **menurun pada bulan-bulan musim panas (sekitar Mei hingga September)**.
-   **Variasi Antar Stasiun:** Stasiun `Dongsi` dan `Gucheng` seringkali menunjukkan tingkat PM2.5 yang lebih tinggi dibandingkan `Dingling`, terutama selama periode polusi tinggi.
""")

# --- Bagian 2: Pengaruh Kecepatan Angin Terhadap PM10 di Stasiun Dongsi Berdasarkan Musim ---
st.header("2. Pengaruh Kecepatan Angin Terhadap PM10 di Stasiun Dongsi Berdasarkan Musim")
st.write("Analisis ini menunjukkan bagaimana kecepatan angin (WSPM) memengaruhi konsentrasi PM10 di stasiun Dongsi, dengan membedakan antara Musim Kemarau dan Musim Hujan (2013-2017).")

# Persiapan data untuk BQ2
df_qa2 = df[df['station'] == 'Dongsi'].copy()
df_qa2['Date'] = pd.to_datetime(df_qa2[['year', 'month', 'day']])

def get_season(month):
    if 5 <= month <= 9:
        return 'Musim Kemarau'
    else:
        return 'Musim Hujan'

df_qa2['Season'] = df_qa2['month'].apply(get_season)
daily_avg_dongsi = df_qa2.groupby(['Date', 'Season'])[['PM10', 'WSPM']].mean().reset_index()

fig2, (ax2a, ax2b) = plt.subplots(1, 2, figsize=(16, 6))

# Scatter plot untuk Musim Kemarau
kemarau_data = daily_avg_dongsi[daily_avg_dongsi['Season'] == 'Musim Kemarau']
ax2a.scatter(kemarau_data['WSPM'], kemarau_data['PM10'], alpha=0.6, color='orange')
# Hitung dan gambar garis regresi secara manual
m_kemarau, b_kemarau = np.polyfit(kemarau_data['WSPM'], kemarau_data['PM10'], 1)
ax2a.plot(kemarau_data['WSPM'], m_kemarau * kemarau_data['WSPM'] + b_kemarau, color='red', linestyle='--', label='Regresi Linear')
ax2a.set_title('WSPM vs PM10 di Dongsi (Musim Kemarau)')
ax2a.set_xlabel('Kecepatan Angin (WSPM)')
ax2a.set_ylabel('Konsentrasi PM10')
ax2a.grid(True, linestyle='--', alpha=0.7)

# Scatter plot untuk Musim Hujan
hujan_data = daily_avg_dongsi[daily_avg_dongsi['Season'] == 'Musim Hujan']
ax2b.scatter(hujan_data['WSPM'], hujan_data['PM10'], alpha=0.6, color='blue')
# Hitung dan gambar garis regresi secara manual
m_hujan, b_hujan = np.polyfit(hujan_data['WSPM'], hujan_data['PM10'], 1)
ax2b.plot(hujan_data['WSPM'], m_hujan * hujan_data['WSPM'] + b_hujan, color='darkblue', linestyle='--', label='Regresi Linear')
ax2b.set_title('WSPM vs PM10 di Dongsi (Musim Hujan)')
ax2b.set_xlabel('Kecepatan Angin (WSPM)')
ax2b.set_ylabel('Konsentrasi PM10')
ax2b.grid(True, linestyle='--', alpha=0.7)

plt.tight_layout()
st.pyplot(fig2)

corr_kemarau = daily_avg_dongsi[daily_avg_dongsi['Season'] == 'Musim Kemarau'][['PM10', 'WSPM']].corr().iloc[0, 1]
corr_hujan = daily_avg_dongsi[daily_avg_dongsi['Season'] == 'Musim Hujan'][['PM10', 'WSPM']].corr().iloc[0, 1]

st.subheader("Insight Utama BQ2:")
st.markdown(f"""
-   **Musim Kemarau (Mei-September):** Koefisien Korelasi: `{corr_kemarau:.2f}` (sangat lemah). Kecepatan angin memiliki pengaruh yang sangat lemah atau hampir tidak ada terhadap PM10.
-   **Musim Hujan (Oktober-April):** Koefisien Korelasi: `{corr_hujan:.2f}` (moderasi negatif). Peningkatan kecepatan angin cenderung berkorelasi dengan penurunan konsentrasi PM10 yang signifikan.
-   **Kesimpulan:** Musim memoderasi hubungan antara kecepatan angin dan tingkat polusi PM10, dengan angin lebih efektif membersihkan polusi di Musim Hujan.
""")

# --- Bagian 3: Pola Harian Konsentrasi Polutan (PM2.5 & PM10) ---
st.header("3. Pola Harian Konsentrasi Polutan (PM2.5 & PM10)")
st.write("Grafik ini menunjukkan rata-rata konsentrasi PM2.5 dan PM10 setiap jam dalam sehari, mengungkap siklus harian polusi (2013-2017).")

# Persiapan data untuk pola harian
hourly_avg_pollutants = df.groupby('hour')[['PM2.5', 'PM10']].mean().reset_index()

fig3, ax3 = plt.subplots(figsize=(12, 6))
ax3.plot(hourly_avg_pollutants['hour'], hourly_avg_pollutants['PM2.5'], marker='o', color='red', label='PM2.5')
ax3.plot(hourly_avg_pollutants['hour'], hourly_avg_pollutants['PM10'], marker='o', color='blue', label='PM10')
ax3.set_title('Rata-rata Konsentrasi PM2.5 dan PM10 per Jam dalam Sehari')
ax3.set_xlabel('Jam dalam Sehari (0-23)')
ax3.set_ylabel('Rata-rata Konsentrasi Polutan')
ax3.set_xticks(range(0, 24))
ax3.grid(True, linestyle='--', alpha=0.7)
ax3.legend()
plt.tight_layout()
st.pyplot(fig3)

st.subheader("Insight Pola Harian:")
st.markdown("""
-   **Puncak Polusi Dini Hari dan Malam Hari:** Konsentrasi PM2.5 dan PM10 cenderung mencapai puncaknya pada dini hari (sekitar jam 00:00 - 05:00) dan malam hari (sekitar jam 19:00 - 23:00).
-   **Penurunan di Pagi Hari:** Terjadi penurunan konsentrasi yang signifikan di pagi hari, kemungkinan karena peningkatan aktivitas angin atau dispersi atmosfer yang lebih baik.
-   **Fluktuasi Siang Hari:** Selama siang hari, konsentrasi polutan cenderung stabil atau sedikit meningkat kembali sebelum mencapai puncak malam hari.
""")

st.sidebar.header("Tentang Aplikasi")
st.sidebar.info(
    "Dashboard ini dibuat untuk memvisualisasikan analisis kualitas udara di tiga stasiun di Beijing. "
    "Data telah dibersihkan dan dianalisis untuk menjawab pertanyaan bisnis terkait tren dan faktor meteorologi."
)
