import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --- Konfigurasi Halaman Streamlit ---
st.set_page_config(page_title="Dashboard Kualitas Udara Beijing",
                   page_icon="🌬️",
                   layout="wide")

# --- Fungsi untuk Memuat Data (dengan caching agar cepat) ---
@st.cache_data
def load_data(path):
    data = pd.read_csv(path)
    # Pastikan kolom waktu diparsing dengan benar jika diperlukan
    # Dalam kasus ini, kita akan membuat kolom Date untuk visualisasi
    data['YearMonth'] = pd.to_datetime(data['year'].astype(str) + '-' + data['month'].astype(str))
    data['Date'] = pd.to_datetime(data[['year', 'month', 'day']])
    return data

# Load the data
df_main = load_data('main_data.csv')

# --- Header Dashboard ---
st.title("Dashboard Analisis Kualitas Udara Beijing 🌬️")
st.markdown("Selamat datang di dashboard interaktif untuk menganalisis data kualitas udara di tiga stasiun di Beijing (Dingling, Dongsi, Gucheng) dari 2013 hingga 2017.")
st.divider()

# --- Gambaran Umum Data ---
st.header("1. Gambaran Umum Data")
st.write("Berikut adalah 5 baris pertama dari data yang telah dibersihkan:")
st.dataframe(df_main.head())

st.write("Statistik deskriptif untuk kolom numerik kunci:")
st.dataframe(df_main[['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3', 'TEMP', 'PRES', 'DEWP', 'RAIN', 'WSPM']].describe())

st.write("Jumlah entri per stasiun:")
st.dataframe(df_main['station'].value_counts().reset_index())
st.divider()

# --- Pertanyaan Bisnis 1: Tren Konsentrasi PM2.5 Bulanan per Stasiun ---
st.header("2. Tren Konsentrasi PM2.5 Bulanan per Stasiun")
st.subheader("Bagaimana tren rata-rata konsentrasi PM2.5 bulanan per stasiun berubah dari tahun 2013 hingga 2017, dan apakah ada pola musiman yang konsisten?")

pm25_monthly_avg = df_main.groupby(['YearMonth', 'station'])['PM2.5'].mean().reset_index()

fig1, ax1 = plt.subplots(figsize=(12, 6))
sns.lineplot(data=pm25_monthly_avg, x='YearMonth', y='PM2.5', hue='station', marker='o', ax=ax1, errorbar=None)
ax1.set_title('Tren Rata-rata Konsentrasi PM2.5 Bulanan per Stasiun (2013-2017)')
ax1.set_xlabel('Tahun-Bulan')
ax1.set_ylabel('Rata-rata Konsentrasi PM2.5')
ax1.tick_params(axis='x', rotation=45)
ax1.grid(True, linestyle='--', alpha=0.7)
ax1.legend(title='Stasiun')
st.pyplot(fig1)

st.markdown("""
**Insight:**
*   Terdapat pola musiman yang konsisten di ketiga stasiun, dengan konsentrasi PM2.5 cenderung meningkat signifikan pada musim dingin (Oktober-Maret) dan menurun pada musim panas (Mei-September).
*   Stasiun Dongsi dan Gucheng sering menunjukkan tingkat PM2.5 yang lebih tinggi dibandingkan Dingling.
""")
st.divider()

# --- Pertanyaan Bisnis 2: Pengaruh Kecepatan Angin Terhadap PM10 di Stasiun Dongsi Berdasarkan Musim ---
st.header("3. Pengaruh Kecepatan Angin Terhadap PM10 di Stasiun Dongsi Berdasarkan Musim")
st.subheader("Di stasiun Dongsi, bagaimana pengaruh kecepatan angin (WSPM) terhadap PM10 secara harian, dan apakah ada perbedaan signifikan antara musim kemarau dan hujan?")

# Menyiapkan data untuk Pertanyaan Bisnis 2
df_qa2 = df_main[df_main['station'] == 'Dongsi'].copy()

def get_season(month):
    if 5 <= month <= 9:
        return 'Musim Kemarau' # Dry Season
    else:
        return 'Musim Hujan' # Wet Season

df_qa2['Season'] = df_qa2['month'].apply(get_season)
daily_avg_dongsi = df_qa2.groupby(['Date', 'Season'])[['PM10', 'WSPM']].mean().reset_index()

fig2, (ax2a, ax2b) = plt.subplots(1, 2, figsize=(18, 6))

# Musim Kemarau
sns.scatterplot(data=daily_avg_dongsi[daily_avg_dongsi['Season'] == 'Musim Kemarau'],
                x='WSPM', y='PM10', alpha=0.6, color='orange', ax=ax2a)
sns.regplot(data=daily_avg_dongsi[daily_avg_dongsi['Season'] == 'Musim Kemarau'],
            x='WSPM', y='PM10', scatter=False, color='red', line_kws={'linestyle': '--'}, ax=ax2a)
ax2a.set_title('WSPM vs PM10 di Dongsi (Musim Kemarau)')
ax2a.set_xlabel('Kecepatan Angin (WSPM)')
ax2a.set_ylabel('Konsentrasi PM10')
ax2a.grid(True, linestyle='--', alpha=0.7)

# Musim Hujan
sns.scatterplot(data=daily_avg_dongsi[daily_avg_dongsi['Season'] == 'Musim Hujan'],
                x='WSPM', y='PM10', alpha=0.6, color='blue', ax=ax2b)
sns.regplot(data=daily_avg_dongsi[daily_avg_dongsi['Season'] == 'Musim Hujan'],
            x='WSPM', y='PM10', scatter=False, color='darkblue', line_kws={'linestyle': '--'}, ax=ax2b)
ax2b.set_title('WSPM vs PM10 di Dongsi (Musim Hujan)')
ax2b.set_xlabel('Kecepatan Angin (WSPM)')
ax2b.set_ylabel('Konsentrasi PM10')
ax2b.grid(True, linestyle='--', alpha=0.7)

st.pyplot(fig2)

corr_kemarau = daily_avg_dongsi[daily_avg_dongsi['Season'] == 'Musim Kemarau'][['PM10', 'WSPM']].corr().iloc[0, 1]
corr_hujan = daily_avg_dongsi[daily_avg_dongsi['Season'] == 'Musim Hujan'][['PM10', 'WSPM']].corr().iloc[0, 1]

st.write(f"Koefisien Korelasi (WSPM vs PM10) Musim Kemarau: `{corr_kemarau:.2f}`")
st.write(f"Koefisien Korelasi (WSPM vs PM10) Musim Hujan: `{corr_hujan:.2f}`")

st.markdown("""
**Insight:**
*   **Musim Kemarau:** Korelasi antara kecepatan angin dan PM10 sangat lemah (mendekati nol). Kecepatan angin tidak memiliki pengaruh signifikan terhadap tingkat polusi PM10.
*   **Musim Hujan:** Terdapat korelasi negatif moderat (-0.43), yang berarti peningkatan kecepatan angin cenderung berkorelasi dengan penurunan konsentrasi PM10. Angin lebih efektif membersihkan polutan di musim hujan.
""")
st.divider()

# --- Analisis Lanjutan: Pola Harian Konsentrasi Polutan ---
st.header("4. Pola Harian Konsentrasi Polutan (PM2.5 & PM10)")
st.subheader("Bagaimana rata-rata konsentrasi polutan berubah sepanjang jam dalam sehari?")

hourly_avg_pollutants = df_main.groupby('hour')[['PM2.5', 'PM10']].mean().reset_index()

fig3, (ax3a, ax3b) = plt.subplots(1, 2, figsize=(18, 6))

sns.lineplot(data=hourly_avg_pollutants, x='hour', y='PM2.5', marker='o', color='red', ax=ax3a)
ax3a.set_title('Rata-rata Konsentrasi PM2.5 per Jam dalam Sehari')
ax3a.set_xlabel('Jam dalam Sehari (0-23)')
ax3a.set_ylabel('Rata-rata Konsentrasi PM2.5')
ax3a.set_xticks(range(0, 24))
ax3a.grid(True, linestyle='--', alpha=0.7)

sns.lineplot(data=hourly_avg_pollutants, x='hour', y='PM10', marker='o', color='blue', ax=ax3b)
ax3b.set_title('Rata-rata Konsentrasi PM10 per Jam dalam Sehari')
ax3b.set_xlabel('Jam dalam Sehari (0-23)')
ax3b.set_ylabel('Rata-rata Konsentrasi PM10')
ax3b.set_xticks(range(0, 24))
ax3b.grid(True, linestyle='--', alpha=0.7)

st.pyplot(fig3)

st.markdown("""
**Insight:**
*   Konsentrasi PM2.5 dan PM10 cenderung mencapai puncaknya pada dini hari (sekitar 00:00-05:00) dan malam hari (sekitar 19:00-23:00).
*   Terjadi penurunan konsentrasi di pagi hari, kemungkinan karena aktivitas angin yang meningkat atau dispersi atmosfer.
""")
st.divider()

# --- Penutup ---
st.markdown("""
---  
_Dashboard ini dibuat untuk Proyek Analisis Data_  
_Sumber Data: PRSA Air Quality Data, Beijing (2013-2017)_  
""")
