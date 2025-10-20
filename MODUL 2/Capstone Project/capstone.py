# # Latar Belakang
# New York City Taxi & Limousine Commission (TLC) merilis catatan perjalanan taksi (Trip Records) yang berisi informasi transaksi per perjalanan (waktu, lokasi, jarak, tarif, metode pembayaran, dsb).
# 
# Notebook ini menganalisis data Green Taxi (LPEP) untuk:
# - memahami pola permintaan (kapan/di jam apa dan hari apa volume tinggi),
# - memetakan pendorong pendapatan (fare, tip, tol),
# - mengevaluasi indikator operasional (durasi, kecepatan, penumpang),
# - serta menurunkan rekomendasi bisnis yang dapat dieksekusi.


# ## Pernyataan Masalah
# Sebagai data analyst, kita ingin menjawab:
# 
# 1) Bagaimana pola permintaan perjalanan berdasarkan jam dan tipe hari (weekday vs weekend)?
# 2) Bagaimana struktur pendapatan (kontribusi fare, tip, tol) dan lokasi pickup ber-revenue tertinggi?
# 3) Seberapa efisien operasi dilihat dari durasi, kecepatan rata-rata, dan jumlah penumpang?
# 4) Bagaimana perilaku pembayaran mempengaruhi tip dan nilai transaksi?
# 5) Apa perbedaan karakteristik perjalanan bandara vs non-bandara (RateCode JFK/Newark)?
# 
# Hasilnya diharapkan menjadi dasar rekomendasi penempatan armada, strategi harga, dan inisiatif peningkatan pendapatan.


# ## Data
# - Sumber: NYC TLC Green Taxi (LPEP) Trip Records.
# - Unit analisis: per perjalanan (row = satu trip).
# - Fitur inti: waktu pickup/dropoff, jarak, jumlah penumpang, komponen tarif (fare, mta_tax, improvement_surcharge, tolls, tip), total_amount, lokasi pickup/dropoff (Taxi Zone), rate code, payment type.
# 
# Data pada notebook ini diambil dari file CSV yang telah diunggah ke Google Drive dan diunduh via gdown. Setelah pemuatan, nama kolom dinormalisasi ke snake_case agar konsisten lintas skema TLC.
# 
# ## Metodologi Singkat
# 1) Normalisasi skema: deteksi nama kolom lintas variasi TLC (lpep/tpep) secara dinamis.  
# 2) Casting & fitur turunan: konversi tipe datetime/numerik; hitung durasi dan kecepatan rata-rata.  
# 3) Imputasi data hilang: pemilihan mean vs median berbasis uji normalitas (D'Agostino–Pearson) per kolom.  
# 4) Pembersihan anomali: aturan bisnis untuk durasi tidak logis, jarak/kecepatan mustahil, dan nilai biaya negatif.  
# 5) Validasi tarif: flag inkonsistensi penjumlahan komponen terhadap total_amount (tidak di-drop).  
# 6) Feature engineering: ekstraksi jam/hari, label rate code dan payment type.  
# 7) Analisis deskriptif: Demand, Revenue, Operations, Payment Behavior, dan Rate/Airport dengan visualisasi.


!pip install gdown

import gdown
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from scipy.stats import normaltest, ttest_ind, mannwhitneyu, pearsonr
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Set style untuk visualisasi
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

# Load dataset dari Google Drive
file_id = "1NYZJYi8n6Vc2Hso2_g_9Fut9M1QrkGjP"
url = f"https://drive.google.com/uc?id={file_id}"
output = "data.csv"
gdown.download(url, output, quiet=False)

df = pd.read_csv(output)

def normalize_columns(cols):
    return [c.strip().lower().replace(" ", "_") for c in cols]

df.columns = normalize_columns(df.columns.tolist())
df.head()

# # Data Understanding & Cleaning


# ## Deteksi nama kolom (tahan variasi skema TLC)


def find_col(df, candidates):
    for c in candidates:
        if c in df.columns:
            return c
    return None

col_pickup  = find_col(df, ["lpep_pickup_datetime","tpep_pickup_datetime","pickup_datetime"])
col_dropoff = find_col(df, ["lpep_dropoff_datetime","tpep_dropoff_datetime","dropoff_datetime"])
col_dist    = find_col(df, ["trip_distance","distance"])
col_pass    = find_col(df, ["passenger_count","passenger_cnt"])
col_fare    = find_col(df, ["fare_amount","fare"])
col_mta     = find_col(df, ["mta_tax","mta"])
col_impr    = find_col(df, ["improvement_surcharge","improvement_surch"])
col_tolls   = find_col(df, ["tolls_amount","tolls"])
col_tip     = find_col(df, ["tip_amount","tip"])
col_total   = find_col(df, ["total_amount","total"])

# ## Casting tipe data & fitur turunan dasar


# Datetime
for c in [col_pickup, col_dropoff]:
    if c is not None:
        df[c] = pd.to_datetime(df[c], errors="coerce")

# Numerik
for c in [col_dist, col_pass, col_fare, col_mta, col_impr, col_tolls, col_tip, col_total]:
    if c is not None and c in df.columns:
        df[c] = pd.to_numeric(df[c], errors="coerce")

# Fitur durasi & kecepatan rata-rata
if (col_pickup is not None) and (col_dropoff is not None):
    df["trip_duration_minutes"] = (df[col_dropoff] - df[col_pickup]).dt.total_seconds()/60.0
    df["trip_duration_hours"]   = df["trip_duration_minutes"]/60.0
else:
    df["trip_duration_minutes"] = np.nan
    df["trip_duration_hours"]   = np.nan

if col_dist is not None:
    df["avg_speed_mph"] = np.where(df["trip_duration_hours"]>0,
                                   df[col_dist]/df["trip_duration_hours"], np.nan)
else:
    df["avg_speed_mph"] = np.nan


# ## Uji normalitas → pilih MEAN atau MEDIAN (p-value dari normaltest)


def choose_imputer(series, alpha=0.05, sample_cap=100_000):
    """Return dict: {'method': 'mean'/'median', 'p_value': float, 'stat': float}"""
    x = series.dropna().values
    if x.size == 0:
        return {"method":"median", "p_value": np.nan, "stat": np.nan}  # default aman
    # sampling bila terlalu besar
    if x.size > sample_cap:
        rng = np.random.default_rng(42)
        x = rng.choice(x, size=sample_cap, replace=False)
    # kalau data terlalu kecil/variasi nol → median
    if len(x) < 8 or np.nanstd(x) == 0:
        return {"method":"median", "p_value": np.nan, "stat": np.nan}
    stat, p = stats.normaltest(x)  # D’Agostino–Pearson
    return {"method": ("mean" if p >= alpha else "median"), "p_value": float(p), "stat": float(stat)}


# ## Daftar kolom yang akan diimputasi + aturan nilai 0 by domain


# Kolom yang wajar diisi 0 jika NaN (berdasarkan proses)
always_zero_if_nan = [col_tolls, col_tip]  # tip tunai tak tercatat; NaN → 0 aman

# Kolom yang ditentukan via normaltest
impute_targets = [
    col_pass, col_dist, col_fare, col_mta, col_impr, col_total,
    "trip_duration_minutes", "avg_speed_mph"
]
impute_targets = [c for c in impute_targets if (c is not None and c in df.columns)]
impute_targets


# ## Terapkan imputasi (logika mean/median berdasarkan p-value)


# Set 0 untuk kolom yang domain-nya wajar nol
for c in always_zero_if_nan:
    if c is not None and c in df.columns:
        df[c] = df[c].fillna(0.0)

# Imputasi statistik
impute_report = {}
for c in impute_targets:
    info = choose_imputer(df[c], alpha=0.05)
    impute_report[c] = info
    fill_value = df[c].mean() if info["method"] == "mean" else df[c].median()
    df[c] = df[c].fillna(fill_value)

# Tampilkan ringkas keputusan imputasi (kolom : metode, p-value)
pd.DataFrame.from_dict(impute_report, orient="index")

# ## Drop baris anomali (cleaning inti – aturan dasar)
# 


rows_before = len(df)

# Waktu/durasi tidak logis
time_bad = pd.Series(False, index=df.index)
if (col_pickup is not None) and (col_dropoff is not None):
    time_bad = df[col_pickup].isna() | df[col_dropoff].isna() \
               | (df["trip_duration_minutes"] <= 0) \
               | (df["trip_duration_minutes"] > 8*60)  # >8 jam: out-of-scope intra-kota

# Jarak tidak valid
dist_bad = pd.Series(False, index=df.index)
if col_dist is not None:
    dist_bad = (df[col_dist] <= 0) | (df[col_dist] > 1000)

# Kecepatan mustahil
speed_bad = pd.Series(False, index=df.index)
if "avg_speed_mph" in df.columns:
    speed_bad = df["avg_speed_mph"] > 120

# Komponen biaya negatif / total negatif
neg_bad = pd.Series(False, index=df.index)
for c in [col_fare, col_mta, col_impr, col_tolls, col_tip, col_total]:
    if c is not None and c in df.columns:
        neg_bad = neg_bad | (df[c] < 0)

drop_mask = time_bad | dist_bad | speed_bad | neg_bad
df_clean = df.loc[~drop_mask].copy()
rows_after = len(df_clean)

print({"rows_in": rows_before, "rows_out": rows_after, "dropped": rows_before-rows_after})


# ## Cek konsistensi tarif sebagai flag saja


if all(c is not None for c in [col_fare, col_mta, col_impr, col_tolls, col_tip, col_total]):
    df_clean["fare_components_sum"]  = df_clean[[col_fare,col_mta,col_impr,col_tolls,col_tip]].sum(axis=1, skipna=True)
    df_clean["total_components_diff"] = df_clean["fare_components_sum"] - df_clean[col_total]
    df_clean["fare_mismatch_flag"]    = df_clean["total_components_diff"].abs() > 0.75  # tidak drop, hanya flag

df_clean

# # Analisis Data


# ## Preprocessing untuk analisis


if col_pickup is not None:
    df_clean['pickup_hour'] = df_clean[col_pickup].dt.hour
    df_clean['pickup_date'] = df_clean[col_pickup].dt.date
    df_clean['pickup_day_of_week'] = df_clean[col_pickup].dt.dayofweek  # 0=Monday, 6=Sunday
    df_clean['is_weekend'] = df_clean['pickup_day_of_week'].isin([5, 6])  # Saturday, Sunday

# Payment type labels
payment_labels = {1: 'Credit Card', 2: 'Cash', 3: 'No Charge', 4: 'Dispute', 5: 'Unknown', 6: 'Voided'}
if 'payment_type' in df_clean.columns:
    df_clean['payment_type_label'] = df_clean['payment_type'].map(payment_labels)

# Rate code labels  
rate_labels = {1: 'Standard', 2: 'JFK', 3: 'Newark', 4: 'Nassau/Westchester', 5: 'Negotiated', 6: 'Group'}
if 'ratecodeid' in df_clean.columns:
    df_clean['rate_code_label'] = df_clean['ratecodeid'].map(rate_labels)

df_clean

# ### Penjelasan:
# - Ekstraksi fitur waktu
# - Labeling metode pembayaran
# - Labeling kode tarif


# ## Demand
# hitung trip per jam/hari, weekday vs weekend.


demand_hourly = df_clean.groupby(['pickup_hour', 'is_weekend']).size().reset_index(name='trip_count')
demand_pivot = demand_hourly.pivot(index='pickup_hour', columns='is_weekend', values='trip_count').fillna(0)
demand_pivot.columns = ['Weekday', 'Weekend']
demand_pivot['Total'] = demand_pivot['Weekday'] + demand_pivot['Weekend']
demand_pivot['Weekend_Ratio'] = (demand_pivot['Weekend'] / demand_pivot['Total'] * 100).round(2)

print("\n📊 TABEL: Trip Count per Hour (Weekday vs Weekend)")
print(demand_pivot.head(10))

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

# Hourly demand
demand_pivot[['Weekday', 'Weekend']].plot(kind='bar', ax=ax1, color=['#3498db', '#e74c3c'])
ax1.set_title('Trip Demand by Hour: Weekday vs Weekend', fontsize=14, fontweight='bold')
ax1.set_xlabel('Hour of Day')
ax1.set_ylabel('Number of Trips')
ax1.legend()
ax1.tick_params(axis='x', rotation=45)

# Daily demand
daily_demand = df_clean.groupby(['pickup_date', 'is_weekend']).size().reset_index(name='daily_trips')
daily_summary = daily_demand.groupby('is_weekend')['daily_trips'].agg(['mean', 'std']).round(0)
daily_summary.index = ['Weekday', 'Weekend']

daily_summary['mean'].plot(kind='bar', ax=ax2, color=['#3498db', '#e74c3c'])
ax2.set_title('Average Daily Trip Volume', fontsize=14, fontweight='bold')
ax2.set_xlabel('Day Type')
ax2.set_ylabel('Average Trips per Day')
ax2.tick_params(axis='x', rotation=0)

# Tambahkan teks aktual rata-rata perjalanan
for i, v in enumerate(daily_summary['mean']):
    ax2.text(i, v + 5, str(int(v)), color='black', ha='center', fontweight='bold')

plt.tight_layout()
plt.show()

# ### Kesimpulan Temuan
# 1. Permintaan jauh lebih tinggi di hari kerja (Weekday)
# - Bar chart kanan menunjukkan Average Daily Trip Volume: ±2.020 trip/hari di weekday vs ±1.765 trip/hari di weekend.
# - Artinya, weekday ≈ 14–15% lebih tinggi dari weekend (selisih ~255 trip/hari).
# 
# 2. Pola per jam (Demand by Hour) sangat berbeda antar hari
# - Weekday: kurva naik stabil mulai pukul 06:00–07:00, puncak kuat di sore–petang (±16:00–19:00) mendekati ~3.800–4.000 trip/jam, lalu turun malam. Ini khas arus komuter pulang kerja.
# - Weekend: lebih “flat” dan lebih rendah keseluruhan; puncak ada di siang–sore (±12:00–18:00) ~1.000–1.400 trip/jam, tak setinggi weekday.
# 
# 3. Rasio Weekend (Weekend_Ratio) tinggi di rentang malam–dini hari
# - Dari tabel, contoh pukul 00:00–03:00: proporsi weekend terhadap total bisa ~49–62%, artinya weekend mendekati (bahkan melampaui) volume weekday pada jam-jam larut malam/awal pagi.
# - Setelah pagi menjelang siang (08:00–12:00) rasio weekend anjlok jadi ~9–15%—dominasi weekday sangat kuat pada jam komuter/aktivitas rutin.


# ## Revenue
# Rata-rata total_amount per pulocationid/dolocationid, lihat kontribusi tolls_amount & tip_amount (tip tunai tak tercatat).


# Tabel: Revenue by Location
if col_total is not None:
    revenue_by_pickup = df_clean.groupby('pulocationid').agg({
        col_total: ['mean', 'sum', 'count'],
        col_tolls: 'mean',
        col_tip: 'mean'
    }).round(2)
    
    revenue_by_pickup.columns = ['Avg_Total', 'Sum_Total', 'Trip_Count', 'Avg_Tolls', 'Avg_Tip']
    revenue_by_pickup = revenue_by_pickup.sort_values('Sum_Total', ascending=False).head(10)
    
    print("\n💰 TABEL: Top 10 Pickup Locations by Total Revenue")
    print(revenue_by_pickup)

# Chart 1: Revenue distribution
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

# Revenue components
revenue_components = df_clean[[col_fare, col_tolls, col_tip]].mean()
revenue_components.plot(kind='pie', ax=ax1, autopct='%1.1f%%', startangle=90)
ax1.set_title('Revenue Components Breakdown', fontsize=14, fontweight='bold')
ax1.set_ylabel('')

# Total amount distribution
df_clean[col_total].hist(bins=50, ax=ax2, alpha=0.7, color='green')
ax2.axvline(df_clean[col_total].mean(), color='red', linestyle='--', label=f'Mean: ${df_clean[col_total].mean():.2f}')
ax2.axvline(df_clean[col_total].median(), color='orange', linestyle='--', label=f'Median: ${df_clean[col_total].median():.2f}')
ax2.set_title('Total Amount Distribution', fontsize=14, fontweight='bold')
ax2.set_xlabel('Total Amount ($)')
ax2.set_ylabel('Frequency')
ax2.legend()

plt.tight_layout()
plt.show()

# ### Kesimpulan Temuan
# 1. Zona pickup penyumbang revenue terbesar
# - PULocationID 74 dan 75 memimpin total pendapatan (Sum_Total tertinggi) sekaligus volume perjalanan (Trip_Count besar).
# - Rata-rata tagihan per trip (Avg_Total) di 10 zona teratas berkisar ~$18–$31; zona 244 tampak paling tinggi (±$31.33).
# 
# 2. Tip & tol per zona relatif kecil terhadap total
# - Avg_Tip rata-rata per zona berada sekitar $1.4–$3.5.
# - Avg_Tolls umumnya < $0.4 (bahkan ada yang ~$0.01), artinya sebagian besar trip tidak melewati tol atau kontribusi tol sangat minor.
# 
# 3. Struktur pendapatan (pie chart)
# - Fare_amount ~87.5% → komponen utama pendapatan.
# - Tip_amount ~11.7% → kontribusi kedua yang signifikan, terutama untuk pembayaran kartu.
# - Tolls_amount ~0.8% → dampak kecil secara agregat.
# 
# 4. Distribusi Total Amount (histogram)
# - Distribusi skewed ke kanan: Mean ≈ $21.75 lebih besar dari Median ≈ $17.90 → ada ekor panjang trip mahal (mis. bandara/long-trip), tapi mayoritas trip berkumpul di $10–$30.
# 
# 5. Implikasi cepat (tanpa keputusan final dulu)
# - Fokus alokasi armada di zona ber-Trip_Count dan Sum_Total tinggi (mis. 74, 75) untuk menjaga utilisasi.
# - Program peningkatan tip (UX pembayaran non-tunai, saran tipping) punya potensi karena tip menyumbang ~12% dari revenue.
# - Tol bukan pengungkit utama; pricing/strategi lebih efektif di tarif dasar & volume.


# ## Operations
# Sebaran trip_duration_minutes, avg_speed_mph, passenger_count (spot outlier).


# Tabel: Operations metrics
operations_metrics = pd.DataFrame({
    'Metric': ['Trip Duration (min)', 'Average Speed (mph)', 'Passenger Count'],
    'Mean': [df_clean['trip_duration_minutes'].mean(), 
             df_clean['avg_speed_mph'].mean(), 
             df_clean[col_pass].mean()],
    'Median': [df_clean['trip_duration_minutes'].median(),
               df_clean['avg_speed_mph'].median(),
               df_clean[col_pass].median()],
    'Std': [df_clean['trip_duration_minutes'].std(),
            df_clean['avg_speed_mph'].std(),
            df_clean[col_pass].std()],
    'Q25': [df_clean['trip_duration_minutes'].quantile(0.25),
            df_clean['avg_speed_mph'].quantile(0.25),
            df_clean[col_pass].quantile(0.25)],
    'Q75': [df_clean['trip_duration_minutes'].quantile(0.75),
            df_clean['avg_speed_mph'].quantile(0.75),
            df_clean[col_pass].quantile(0.75)]
}).round(2)

print("\n⚙️ TABEL: Operations Metrics Summary")
print(operations_metrics)

# Chart 1: Trip duration and speed distribution
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))

# Trip duration
df_clean['trip_duration_minutes'].hist(bins=50, ax=ax1, alpha=0.7, color='blue')
ax1.set_title('Trip Duration Distribution', fontsize=12, fontweight='bold')
ax1.set_xlabel('Duration (minutes)')
ax1.set_ylabel('Frequency')
ax1.axvline(df_clean['trip_duration_minutes'].mean(), color='red', linestyle='--', alpha=0.8)

# Speed distribution
df_clean['avg_speed_mph'].hist(bins=50, ax=ax2, alpha=0.7, color='orange')
ax2.set_title('Average Speed Distribution', fontsize=12, fontweight='bold')
ax2.set_xlabel('Speed (mph)')
ax2.set_ylabel('Frequency')
ax2.axvline(df_clean['avg_speed_mph'].mean(), color='red', linestyle='--', alpha=0.8)

# Passenger count
passenger_counts = df_clean[col_pass].value_counts().sort_index()
passenger_counts.plot(kind='bar', ax=ax3, color='green')
ax3.set_title('Passenger Count Distribution', fontsize=12, fontweight='bold')
ax3.set_xlabel('Number of Passengers')
ax3.set_ylabel('Trip Count')
ax3.tick_params(axis='x', rotation=0)

# Speed vs Duration scatter
sample_data = df_clean.sample(n=min(5000, len(df_clean)), random_state=42)
ax4.scatter(sample_data['trip_duration_minutes'], sample_data['avg_speed_mph'], alpha=0.5, s=1)
ax4.set_title('Speed vs Duration Relationship', fontsize=12, fontweight='bold')
ax4.set_xlabel('Trip Duration (minutes)')
ax4.set_ylabel('Average Speed (mph)')

plt.tight_layout()
plt.show()

# ### Kesimpulan Temuan
# 1. Durasi perjalanan pendek dengan ekor panjang
# - Rata-rata 13.9 menit, median 11.4 menit (Q25 7.4, Q75 17.3) → distribusi right-skewed: mayoritas trip singkat, sebagian kecil trip lama menarik mean ke atas.
# 
# 2. Kecepatan rata-rata rendah khas kota padat
# - Rata-rata ~12 mph, median ~10.6 mph (Q25 8.6, Q75 13.7) → sebagian besar perjalanan bergerak di 8–14 mph. Ada ekor kecil ke >20 mph, tapi jarang.
# 
# 3. Passenger count didominasi single rider
# - Median = 1 dan modus jelas di 1 penumpang. Ada sebagian kecil 2–6 penumpang; kemungkinan trip bersama/keluarga. Jika ada 0 penumpang, itu outlier input (layak diflag).
# 
# 4. Hubungan speed vs duration: cenderung menurun/lemah
# - Scatter mengelompok di durasi <30 menit dan speed <25 mph.
# - Semakin lama durasi, kecenderungan speed lebih rendah (kemacetan/stop-and-go), namun korelasinya tidak kuat—durasi panjang juga bisa karena jarak lebih jauh.
# 
# 5. Implikasi cepat
# - Benchmark SLA operasional wajar: 10–17 menit per trip; kecepatan 8–14 mph.
# - Fokus optimasi di short trips volume tinggi (dominant segment).
# - Cek & bersihkan passenger_count=0 serta very-long-duration outliers (mis. >60–90 menit) untuk akurasi metrik.


# ## Payment behavior
# proporsi payment type + rata-rata tip per payment (kartu cenderung ada tip; cash biasanya 0 di data).


# Tabel: Payment behavior
if 'payment_type_label' in df_clean.columns:
    payment_analysis = df_clean.groupby('payment_type_label').agg({
        col_tip: ['mean', 'median', 'std'],
        col_total: 'mean',
        'vendorid': 'count'
    }).round(2)
    
    payment_analysis.columns = ['Avg_Tip', 'Median_Tip', 'Std_Tip', 'Avg_Total', 'Trip_Count']
    payment_analysis['Tip_Rate_%'] = ((payment_analysis['Avg_Tip'] / payment_analysis['Avg_Total']) * 100).round(2)
    payment_analysis = payment_analysis.sort_values('Trip_Count', ascending=False)
    
    print("\n💳 TABEL: Payment Behavior Analysis")
    display(payment_analysis)

# Chart 1: Payment type distribution and tip analysis
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

# Payment type proportion
payment_props = df_clean['payment_type_label'].value_counts()
payment_props.plot(kind='pie', ax=ax1, autopct='%1.1f%%', startangle=90)
ax1.set_title('Payment Type Distribution', fontsize=14, fontweight='bold')
ax1.set_ylabel('')

# Average tip by payment type
payment_analysis['Avg_Tip'].plot(kind='bar', ax=ax2, color=['#3498db', '#e74c3c', '#2ecc71', '#f39c12'])
ax2.set_title('Average Tip Amount by Payment Type', fontsize=14, fontweight='bold')
ax2.set_xlabel('Payment Type')
ax2.set_ylabel('Average Tip ($)')
ax2.tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.show()

# ### Kesimpulan Temuan
# 1. Pangsa pembayaran: ~63.5% Credit Card, 36.1% Cash, sisanya “No Charge/Dispute” sangat kecil.
# 2. Tip hanya muncul pada Credit Card:
# - Avg_Tip ≈ $3.32, Median_Tip ≈ $2.86, Std_Tip ≈ $3.12 → variasi tip cukup lebar.
# - Tip_Rate ≈ 14.6% (proporsi trip kartu yang memberi tip).
# - Cash/No Charge/Dispute = $0 tip (sesuai karakter data: tip tunai tidak terekam).
# 3. Nilai tagihan rata-rata per metode:
# - Credit Card ≈ $22.78 > Cash ≈ $18.41 > No Charge ≈ $11.17 ≈ Dispute ≈ $10.96.
# - Indikasi: trip kartu cenderung sedikit lebih mahal dan menyumbang seluruh pendapatan tip yang tercatat.


# ## Rate & Airport
# proporsi rate_code_label (JFK/Newark) sebagai indikasi rute bandara.


# Tabel: Rate code analysis
if 'rate_code_label' in df_clean.columns:
    rate_analysis = df_clean.groupby('rate_code_label').agg({
        'vendorid': 'count',
        col_total: 'mean',
        'trip_duration_minutes': 'mean',
        col_dist: 'mean'
    }).round(2)
    
    rate_analysis.columns = ['Trip_Count', 'Avg_Total', 'Avg_Duration_min', 'Avg_Distance_mi']
    rate_analysis['Proportion_%'] = ((rate_analysis['Trip_Count'] / rate_analysis['Trip_Count'].sum()) * 100).round(2)
    rate_analysis = rate_analysis.sort_values('Trip_Count', ascending=False)
    
    print("\n✈️ TABEL: Rate Code Analysis (Airport Routes)")
    display(rate_analysis)

# Chart 1: Rate code distribution and airport analysis
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

# Rate code proportion
rate_props = df_clean['rate_code_label'].value_counts()
rate_props.plot(kind='bar', ax=ax1, color='skyblue')
ax1.set_title('Rate Code Distribution', fontsize=14, fontweight='bold')
ax1.set_xlabel('Rate Code Type')
ax1.set_ylabel('Trip Count')
ax1.tick_params(axis='x', rotation=45)

# Airport vs non-airport comparison
airport_codes = ['JFK', 'Newark']
df_clean['is_airport'] = df_clean['rate_code_label'].isin(airport_codes)
airport_comparison = df_clean.groupby('is_airport').agg({
    col_total: 'mean',
    'trip_duration_minutes': 'mean',
    col_dist: 'mean'
}).round(2)

airport_comparison.index = ['Non-Airport', 'Airport']
airport_comparison.plot(kind='bar', ax=ax2)
ax2.set_title('Airport vs Non-Airport Trips Comparison', fontsize=14, fontweight='bold')
ax2.set_xlabel('Trip Type')
ax2.set_ylabel('Average Values')
ax2.legend(['Total Amount ($)', 'Duration (min)', 'Distance (mi)'])
ax2.tick_params(axis='x', rotation=0)

plt.tight_layout()
plt.show()

# ### Kesimpulan Temuan
# 1. Standard mendominasi volume
# - ~98.2% trip = Standard rate (≈59k trip). Ini core bisnis harian jarak pendek–menengah di dalam kota.
# 
# 2. Airport = volume kecil, nilai tinggi
# - JFK/Newark hanya ~0.25% total trip, tapi ticket size jauh lebih besar:
#     - JFK: Avg_Total ~$87, durasi ~36–37 min, jarak ~15 mi.
#     - Newark: Avg_Total ~$112, durasi ~33 min, jarak ~18 mi.
# - Negotiated (±1.5%): Avg_Total ~$33.7, lebih lama & jauh dari Standard (durasi ~16.7 min, jarak ~4.4 mi).
# 
# 3. Perbandingan Airport vs Non-Airport (chart kanan)
# - Airport trips punya Total Amount, Duration, Distance yang jauh di atas Non-Airport—low volume, high value.
# 
# 4. Implikasi operasional cepat
# - Strategi “low-volume high-value” untuk bandara:
#     - Penempatan armada di koridor bandara (jam keberangkatan/kedatangan padat).
#     - Insentif/priority dispatch agar acceptance rate rute bandara tinggi.
#     - Pantau tolls & waktu tunggu; potensi add-on cost dan SLA lebih ketat.
# - Bisnis utama tetap Standard → optimasi utilisasi dan rotasi armada di zona demand tinggi (downtown, hub transit).
# 
# 5. Catatan analitis
# - Flag otomatis airport_trip via rate_code_label ∈ {JFK, Newark} untuk pelacakan KPI.
# - Bandingkan net revenue per hour airport vs non-airport (durasi panjang bisa menurunkan turn-over meski ticket size besar).
# - Audit konsistensi rate code dan komponen tarif (tol, surcharge) pada rute bandara.


# ## Ruang Lingkup & Asumsi
# - Tip tunai tidak tercatat; tip terutama muncul pada pembayaran kartu.
# - Ambang pembersihan (mis. durasi > 8 jam, kecepatan > 120 mph) digunakan sebagai aturan praktis intra-kota.
# - Perbedaan kecil antara penjumlahan komponen dan total_amount ditoleransi dan hanya diberi flag.
# - Analisis bersifat deskriptif pada periode data yang tersedia; faktor eksternal (cuaca, event) tidak dimodelkan.


# ## Tujuan
# - Menyediakan ringkasan metrik kunci yang dapat ditindaklanjuti untuk tim operasi, pricing, dan growth.
# - Menghasilkan rekomendasi taktis (penempatan armada, promosi akhir pekan, optimasi tip) dan arah strategis.


# # Kesimpulan & Rekomendasi


# ## 📊 **KESIMPULAN UTAMA**
# 
# ### **Kualitas Data & Pembersihan**
# 1. **Dataset awal**: Berhasil membersihkan dataset dengan menghapus anomali berdasarkan aturan bisnis yang ketat
# 2. **Imputasi cerdas**: Menggunakan uji normalitas untuk menentukan metode imputasi (rata-rata vs median) secara statistik
# 3. **Konsistensi tarif**: Implementasi penanda untuk memantau inkonsistensi komponen tarif tanpa menghapus data
# 
# ### **Temuan Bisnis Utama**
# 
# #### **1. Pola Permintaan**
# - **Dominasi hari kerja**: 14-15% lebih tinggi dari akhir pekan (~2.020 vs 1.765 perjalanan/hari)
# - **Efek jam sibuk**: Puncak permintaan jam 16:00-19:00 (3.800-4.000 perjalanan/jam) di hari kerja
# - **Pola akhir pekan**: Lebih datar, puncak di siang-sore (1.000-1.400 perjalanan/jam)
# 
# #### **2. Struktur Pendapatan**
# - **Dominasi tarif**: 87,5% dari total pendapatan berasal dari tarif dasar
# - **Kontribusi tip**: 11,7% dari pendapatan (hanya dari pembayaran kartu)
# - **Tol minimal**: Hanya 0,8% kontribusi pendapatan
# - **Konsentrasi pendapatan**: Zona 74 & 75 menjadi generator pendapatan teratas
# 
# #### **3. Efisiensi Operasional**
# - **Durasi perjalanan**: Median 11,4 menit, mayoritas perjalanan singkat (<30 menit)
# - **Kecepatan rata-rata**: ~12 mph (khas kota padat dengan lalu lintas macet)
# - **Penumpang tunggal**: Dominasi 1 penumpang per perjalanan
# - **Premium bandara**: JFK/Newark hanya 0,25% volume tapi nilai tiket 4-5x lipat
# 
# #### **4. Perilaku Pembayaran**
# - **Kartu kredit**: 63,5% transaksi dengan tingkat tip 14,6%
# - **Tunai**: 36,1% transaksi tanpa tip tercatat
# - **Perbedaan nilai**: Perjalanan kartu kredit rata-rata $4-5 lebih mahal


# ## 🎯 **REKOMENDASI STRATEGIS**
# 
# ### **A. PENINGKATAN PERMINTAAN**
# 
# #### **📅 Jangka Pendek (1-3 bulan)**
# 
# **1. Optimalisasi Jam Sibuk**
# ```
# • Penetapan harga dinamis di jam 16:00-19:00 hari kerja untuk maksimalkan pendapatan
# • Insentif pengemudi untuk jam sepi akhir pekan (pagi-siang)
# • Penempatan armada waktu nyata ke zona 74, 75, dan lokasi pendapatan tinggi
# ```
# 
# **2. Strategi Akhir Pekan**
# ```
# • Promosi akhir pekan: "Jelajah Akhir Pekan" dengan diskon 10-15%
# • Kemitraan dengan tempat acara untuk perjalanan malam hari
# • Target pasar: kehidupan malam, pusat perbelanjaan, aktivitas rekreasi
# ```
# 
# **3. Peningkatan Pembayaran**
# ```
# • Kampanye "Tanpa Tunai = Lebih Banyak Reward" untuk tingkatkan adopsi kartu
# • Saran tip dalam aplikasi untuk tingkatkan tingkat tip dari 14,6%
# • Pemrosesan pembayaran instan untuk pengalaman pelanggan
# ```
# 
# #### **⏳ Jangka Menengah (3-12 bulan)**
# 
# **1. Ekspansi Geografis**
# ```
# • Analisis zona dengan pasokan rendah-permintaan tinggi untuk ekspansi
# • Integrasi mikro-mobilitas (sepeda/skuter) untuk perjalanan pertama-terakhir
# • Kemitraan strategis dengan mal, hotel, dan hub transit
# ```
# 
# **2. Diversifikasi Layanan**
# ```
# • Layanan premium untuk rute bandara (armada khusus)
# • Program berbagi perjalanan untuk segmen sadar biaya
# • Model berlangganan untuk komuter yang sering bepergian
# ```
# 
# **3. Integrasi Teknologi**
# ```
# • Peramalan permintaan berbasis AI untuk posisi armada proaktif
# • Model penetapan harga dinamis berdasarkan permintaan waktu nyata
# • Pembelajaran preferensi pelanggan untuk layanan personal
# ```
# 
# #### **🚀 Jangka Panjang (1-3 tahun)**
# 
# **1. Kepemimpinan Pasar**
# ```
# • Transisi kendaraan listrik untuk branding berkelanjutan
# • Program percontohan kendaraan otonom di zona terpilih
# • Platform mobilitas terintegrasi (taksi + transportasi umum + mikro-mobilitas)
# ```
# 
# **2. Monetisasi Data**
# ```
# • Wawasan pola lalu lintas anonim untuk perencanaan kota
# • Layanan intelijen lokasi untuk bisnis ritel
# • Analitik prediktif untuk pariwisata dan manajemen acara
# ```
# 
# **3. Pengembangan Ekosistem**
# ```
# • Pengembangan super-app (perjalanan + makanan + pengiriman + pembayaran)
# • Solusi korporat B2B untuk transportasi karyawan
# • Kemitraan kota pintar untuk optimalisasi lalu lintas
# ```


# ### **B. AUDIT & TATA KELOLA**
# 
# #### **🔍 Audit Kualitas Data**
# 
# **1. Pemantauan Waktu Nyata**
# ```
# Implementasi dasbor pemantauan untuk:
# • Konsistensi komponen tarif (target: <5% ketidakcocokan)
# • Anomali durasi perjalanan (target: <2% outlier)
# • Validasi kecepatan (peringatan jika >80 mph)
# • Validasi jumlah penumpang (tandai jika = 0)
# ```
# 
# **2. Jaminan Pendapatan**
# ```
# • Rekonsiliasi mingguan komponen tarif vs jumlah total
# • Audit bulanan persentase tip berdasarkan jenis pembayaran
# • Tinjauan triwulanan efektivitas model penetapan harga
# • Benchmarking tahunan vs standar industri
# ```
# 
# #### **📋 Audit Operasional**
# 
# **1. KPI Kinerja**
# ```
# • Waktu respons rata-rata per zona (target: <5 menit)
# • Tingkat utilisasi pengemudi (target: >70%)
# • Skor kepuasan pelanggan (target: >4,2/5,0)
# • Pendapatan per perjalanan per zona (lacak tren bulanan)
# ```
# 
# **2. Pemantauan Kepatuhan**
# ```
# • Akurasi kode tarif untuk perjalanan bandara
# • Kepatuhan pemrosesan pembayaran
# • Status lisensi pengemudi dan inspeksi kendaraan
# • Verifikasi cakupan asuransi
# ```
# 
# #### **💰 Audit Keuangan**
# 
# **1. Optimalisasi Pendapatan**
# ```
# • Analisis P&L bulanan per zona dan segmen waktu
# • Pelacakan biaya akuisisi vs nilai seumur hidup
# • Analisis elastisitas harga untuk tingkat surge optimal
# • Tinjauan efektivitas struktur komisi
# ```
# 
# **2. Manajemen Risiko**
# ```
# • Deteksi penipuan untuk pola perjalanan mencurigakan
# • Penilaian risiko kredit untuk akun korporat
# • Dampak nilai tukar untuk pembayaran internasional
# • Pelacakan biaya kepatuhan regulasi
# ```


# ## 📈 **HASIL YANG DIHARAPKAN**
# 
# ### **Dampak Pendapatan**
# - **Jangka pendek**: Peningkatan pendapatan 8-12% melalui penetapan harga surge dan optimalisasi tip
# - **Jangka menengah**: Pertumbuhan pangsa pasar 15-25% melalui diversifikasi layanan
# - **Jangka panjang**: Ekspansi pendapatan 30-50% melalui pengembangan ekosistem
# 
# ### **Keunggulan Operasional**
# - **Efisiensi**: Peningkatan 20% dalam utilisasi armada
# - **Kualitas**: Tingkat penyelesaian perjalanan 95% dengan <2% anomali
# - **Pelanggan**: Skor rating 4,5+ dengan tingkat retensi 90%
# 
# ### **Posisi Pasar**
# - **Kepemimpinan**: Posisi 2 teratas pasar dalam 18 bulan
# - **Inovasi**: Keunggulan first-mover dalam kendaraan otonom/listrik
# - **Keberlanjutan**: 50% armada listrik dalam 3 tahun
# 
# ## ⚠️ **PRIORITAS IMPLEMENTASI**
# 
# 1. **🚨 Segera (Minggu 1-4)**
#    - Implementasi penetapan harga surge untuk jam sibuk
#    - Peluncuran kampanye promosi tanpa tunai
#    - Penyebaran dasbor pemantauan waktu nyata
# 
# 2. **📊 Prioritas Tinggi (Bulan 1-3)**
#    - Program stimulasi permintaan akhir pekan
#    - Peluncuran layanan premium bandara
#    - Infrastruktur analitik lanjutan
# 
# 3. **🔧 Prioritas Menengah (Bulan 3-6)**
#    - Peluncuran diversifikasi layanan
#    - Inisiatif integrasi teknologi
#    - Perencanaan ekspansi pasar
# 
# 4. **🌟 Strategis (Bulan 6+)**
#    - Program transformasi jangka panjang
#    - Pengembangan ekosistem
#    - Inisiatif keberlanjutan
# 
# ---
# 
# **💡 Faktor Kunci Kesuksesan:**
# - Pengambilan keputusan berbasis data dengan pemantauan waktu nyata
# - Pendekatan berpusat pada pelanggan dalam semua inisiatif
# - Implementasi gesit dengan perbaikan berkelanjutan
# - Ekosistem kemitraan yang kuat untuk pertumbuhan berkelanjutan