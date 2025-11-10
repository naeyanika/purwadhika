# PT. DanaPintar Indonesia — Penjelasan Per Section Notebook

Dokumen ini menjelaskan setiap section kode pada notebook `DanaPintar.ipynb` secara ringkas, terstruktur, dan berbahasa Indonesia. Gunakan ini sebagai panduan saat mereview atau mempresentasikan proyek.

---

## 1) Import Library

- Mengimpor pustaka untuk manipulasi data (pandas, numpy), visualisasi (matplotlib, seaborn), serta machine learning (scikit-learn: model, preprocessing, evaluasi, dan hyperparameter tuning).
- `warnings.filterwarnings('ignore')` untuk menyembunyikan peringatan yang tidak krusial sehingga output lebih bersih.

Kenapa penting: Menyiapkan semua alat yang dibutuhkan sejak awal agar setiap section berikutnya fokus ke logika analisis.

---

## 2) Load Data & Initial Exploration

- `pd.read_csv('data_pinjaman_train.csv')` memuat data historis peminjam.
- Menampilkan ukuran data (shape) dan sampel 10 baris pertama sebagai sanity check.

Kenapa penting: Memastikan file terbaca dengan benar serta memahami bentuk awal data.

---

## 3) Info Dataset

- `df_train.info()` untuk melihat tipe data per kolom dan jumlah non-null.
- Cek missing values per kolom dengan `df_train.isnull().sum()`.
- Cek distribusi target `Status_Pinjaman` (jumlah dan persentase kelas Lancar vs Macet).

Insight utama:

- Mengidentifikasi kebutuhan cleaning (jika ada missing/anomali) dan memonitor imbalance pada target (berpengaruh ke evaluasi model).

---

## 4) Statistik Deskriptif (Fitur Numerik)

- `df_train.describe()` merangkum metrik seperti min, max, mean, std, dan kuartil untuk fitur numerik.

Apa yang dicari:

- Range nilai, outlier potensial, serta indikasi distribusi (skew/normal) yang memandu preprocessing dan pilihan model.

---

## 5) Exploratory Data Analysis (EDA)

### 5.1 Distribusi Target

- Visualisasi Pie dan Bar untuk kelas `Status_Pinjaman`.
- Menilai apakah data imbalanced (umum pada kasus risiko kredit).

Dampak: Jika imbalanced, perhatikan metrik evaluasi (precision/recall/F1) dan gunakan `stratify` saat split.

### 5.2 Distribusi Fitur Numerik

- Histogram untuk 9 fitur numerik: Usia, Pendapatan_Bulanan, Lama_Bekerja_Tahun, Jumlah_Tanggungan, Skor_Kredit_Internal, Jumlah_Pinjaman_Diminta, Rasio_Utang_Pendapatan, Jml_Keterlambatan_Bayar_12bln, Durasi_Pinjaman_Bulan.

Tujuan: Memahami pola (normal, skewed, multimodal) dan potensi outlier.

### 5.3 Distribusi Fitur Kategorik

- Bar chart untuk 5 fitur kategorik: Tujuan_Pinjaman, Status_Kepemilikan_Rumah, Jenis_Pekerjaan, Pendidikan_Terakhir, Status_Pernikahan.

Tujuan: Menemukan kategori dominan/rare yang dapat mempengaruhi encoding dan stabilitas model.

### 5.4 Korelasi Fitur Numerik vs Target

- Menghitung korelasi tiap fitur numerik terhadap target yang diencode (Macet=1, Lancar=0).
- Visualisasi bar horizontal (merah = korelasi positif dengan Macet, hijau = negatif).

Interpretasi umum:

- `Jml_Keterlambatan_Bayar_12bln` cenderung berkorelasi positif dengan macet.
- `Skor_Kredit_Internal` cenderung berkorelasi negatif (semakin tinggi skor, risiko lebih rendah).

### 5.5 Heatmap Korelasi Antar Fitur Numerik

- Heatmap matriks korelasi untuk mendeteksi multicollinearity (fitur yang saling berkorelasi tinggi).

Dampak: Fitur sangat berkorelasi dapat menyebabkan redundansi; pertimbangkan reduksi fitur jika diperlukan.

---

## 6) Data Preprocessing

### 6.1 Feature Encoding

- Target `Status_Pinjaman`: Lancar→0, Macet→1 (label encoding manual).
- Fitur kategorik: one-hot encoding dengan `pd.get_dummies(..., drop_first=True)` untuk menghindari dummy trap.

Hasil: Semua fitur menjadi numerik dan siap untuk algoritma ML.

### 6.2 Train-Test Split

- Memisahkan data menjadi training (80%) dan testing (20%).
- Menggunakan `stratify=y` untuk menjaga proporsi kelas target pada train dan test.

Alasan: Evaluasi objektif pada data yang tidak terlihat saat training serta menjaga distribusi kelas konsisten.

### 6.3 Feature Scaling

- `StandardScaler` diterapkan pada X_train/X_test untuk model yang sensitif skala (KNN, SVM, Logistic Regression, Naive Bayes).
- Decision Tree tidak membutuhkan scaling (menggunakan X asli saat baseline dan tuning).

Manfaat: Menyamakan skala fitur agar perhitungan jarak/optimasi bekerja optimal.

---

## 7) Pembuatan Model (Baseline)

Melatih dan mengevaluasi 5 model dasar:

- Logistic Regression (scaled)
- K-Nearest Neighbors (scaled)
- Support Vector Machine (scaled)
- Decision Tree (tanpa scaling)
- Gaussian Naive Bayes (scaled)

Metrik yang dilaporkan: Accuracy, Precision, Recall, F1-Score. Hasil dirangkum dalam tabel perbandingan baseline.

Tujuan: Menjadi acuan awal sebelum optimasi hyperparameter.

---

## 8) Hyperparameter Tuning (GridSearchCV)

Mengoptimalkan 4 model (kecuali GNB) menggunakan cross-validation (cv=5) dan skor F1 (lebih relevan untuk data yang mungkin imbalanced).

- Logistic Regression: `solver`, `C`, `max_iter`.
- KNN: `n_neighbors`, `weights`, `metric`.
- SVM: `kernel`, `C`, `gamma`.
- Decision Tree: `criterion`, `max_depth`, `min_samples_split`, `min_samples_leaf`.

Output: Estimator terbaik (`best_estimator_`), parameter terbaik, dan metrik pada set test.

---

## 9) Evaluasi Model (Setelah Tuning)

- Tabel perbandingan untuk semua model teroptimasi berdasarkan Accuracy, Precision, Recall, F1-Score.
- Visualisasi barh per metrik untuk memudahkan pembacaan.
- Menentukan “Model Terbaik” berdasarkan F1-Score tertinggi.

Kenapa F1-Score: Menyeimbangkan precision dan recall, cocok untuk kasus risiko kredit dengan biaya error yang berbeda (false negative vs false positive).

---

## 10) Confusion Matrix & Classification Report

- Membuat confusion matrix untuk model terbaik guna memahami kesalahan prediksi (TN, FP, FN, TP).
- Menampilkan classification report (precision, recall, f1 per kelas) untuk interpretasi menyeluruh.

Fokus bisnis:

- False Negative (prediksi Lancar tapi aktual Macet) biasanya paling berbiaya tinggi dan perlu diminimalkan.

---

## 11) Feature Importance (Decision Tree)

- Jika model terbaik adalah Decision Tree, tampilkan 10 fitur paling penting beserta grafik bar.
- Memberi insight fitur mana yang paling berpengaruh terhadap keputusan model.

Catatan: Model lain seperti SVM/LogReg (tanpa regularisasi khusus) tidak langsung menyediakan “feature importance” seperti DT/RF.

---

## 12) Prediksi Final ke Data Baru

### 12.1 Load Data Predict

- Memuat `data_pinjaman_predict.csv` (tanpa kolom target) sebagai kandidat peminjam baru.

### 12.2 Preprocessing Konsisten

- One-hot encoding kolom kategorik pada data predict.
- Menyamakan kolom dengan training (menambah kolom yang hilang → 0, menghapus kolom ekstra) dan mengurutkan sesuai fitur training.

### 12.3 Train Ulang Model Terbaik

- Melatih ulang model terbaik menggunakan seluruh data training (bukan hanya X_train) untuk memaksimalkan informasi sebelum prediksi.
- Terapkan scaling kembali bila modelnya membutuhkan (LogReg/KNN/SVM/GNB).

### 12.4 Prediksi & Ekspor

- Menghasilkan label `Prediksi_Status_Pinjaman` (Lancar/Macet) untuk setiap baris data baru.
- Menyimpan hasil ke `hasil_prediksi_danapintar.csv`.

---

## 13) Kesimpulan & Rekomendasi Bisnis

- Menegaskan alasan pemilihan model terbaik (F1-Score tertinggi dan konteks risiko kredit).
- Merangkum 3 temuan EDA terpenting (contoh: Skor Kredit, DTI Ratio, Keterlambatan Bayar) sebagai faktor risiko utama.
- Rekomendasi dapat ditindaklanjuti: implementasi scoring otomatis, kebijakan DTI, early warning system, risk-adjusted pricing, dan data enrichment.

Nilai tambah: Mengaitkan hasil teknis ke keputusan operasional untuk menurunkan NPL.

---

## 14) Summary Akhir

- Ringkasan jumlah data, jumlah fitur, nama model terbaik, performa metrik kunci pada test set, serta ringkasan agregat hasil prediksi (proporsi Lancar vs Macet) dan lokasi file output.

Tujuan: Memberi gambaran singkat proyek dari ujung ke ujung.

---

## Catatan Teknis Tambahan

- Scaling hanya dipakai pada model distance/gradient-based; tree-based tidak membutuhkan.
- Stratified split menjaga proporsi kelas sehingga evaluasi lebih representatif.
- Gunakan F1-Score sebagai metrik utama saat kelas tidak seimbang atau ketika biaya FN/FP penting.
- Pastikan preprocessing data predict identik dengan training (kolom, urutan, dan scaling bila perlu).

---

## Appendix: Alasan Desain, Alternatif, dan Trade-off (Siap Dipresentasikan ke Dosen)

Bagian ini merangkum “kenapa ini, kenapa itu” untuk setiap keputusan penting, lengkap dengan alternatif dan trade-off-nya.

### A. Encoding Fitur Kategorik: Kenapa One-Hot Encoding (OHE)?

- Alasan: Sebagian besar model (LogReg, SVM, KNN, Naive Bayes) memerlukan input numerik dan mengasumsikan hubungan linear/berbasis jarak; label encoding bisa memberi urutan semu pada kategori. OHE menghindari ordinal palsu.
- Implementasi: `pd.get_dummies(..., drop_first=True)` untuk menghindari dummy trap (multikolinearitas sempurna).
- Alternatif: `OneHotEncoder` dari scikit-learn di dalam `Pipeline` lebih “production-ready” (fit hanya di train, transform konsisten di test/predict). Di notebook ini, kami kompensasikan dengan menyamakan kolom train vs predict secara manual (menambah kolom hilang = 0, hapus kolom ekstra, urutkan kolom).
- Trade-off: OHE bisa meledak jumlah fitur bila kategori tinggi. Solusi lanjut: target encoding, hashing trick, atau penggabungan kategori rare.

### B. Kenapa StandardScaler (bukan MinMaxScaler)?

- Alasan: StandardScaler menghasilkan distribusi fitur dengan mean≈0 dan std≈1, cocok untuk LogReg/SVM (optimisasi gradient) dan KNN (jarak Euclidean). Umumnya lebih stabil terhadap outlier moderat dibanding MinMax yang memetakan ke [0,1].
- Alternatif: MinMaxScaler bagus untuk metode berbasis jarak ketika semua fitur berada pada range terbatas dan ingin menjaga bentuk distribusi asli; RobustScaler jika banyak outlier.
- Trade-off: Pilihan scaler memengaruhi performa KNN/SVM; bisa dieksperimenkan sebagai hyperparameter di masa depan.

### C. Kenapa Model-Model Ini?

- Logistic Regression: baseline yang kuat, interpretabel (koefisien), cepat, dan sering kompetitif pada masalah linier/nyaris-linier.
- KNN: non-parametrik, sederhana, menangkap pola lokal; sensitif skala dan nilai k.
- SVM: kuat pada ruang berdimensi tinggi, kernel RBF untuk pola non-linear.
- Decision Tree: interpretabel, menangani non-linearitas dan interaksi fitur, tidak butuh scaling.
- Gaussian Naive Bayes: asumsi independensi fitur dan Gaussian pada fitur kontinu; cepat sebagai baseline probabilistik.
- Trade-off umum: model yang sangat akurat kadang kurang interpretabel (SVM), sementara model interpretabel (DT) bisa overfit tanpa regularisasi (depth/leaf).

### D. Kenapa Stratified Split?

- Alasan: Menjaga proporsi kelas target yang mungkin imbalanced di train dan test. Tanpa stratifikasi, metrik bisa bias akibat sampling acak yang tidak representatif.

### E. Kenapa F1-Score Sebagai Metrik Utama?

- Alasan: Pada kredit macet, biaya FN (prediksi Lancar padahal Macet) tinggi. F1 menyeimbangkan precision dan recall sehingga penalti untuk salah satu tidak terlalu besar. Accuracy bisa menipu jika kelas tidak seimbang.
- Alternatif: PR AUC (lebih informatif saat imbalance), Recall kelas “Macet” sebagai KPI risiko, atau F2 untuk menekankan recall.
- Trade-off: Fokus ke F1 mungkin mengorbankan interpretasi bisnis tertentu; jelaskan biaya kesalahan untuk menjustifikasi metrik.

### F. Kenapa GridSearchCV cv=5?

- Alasan: Cross-validation mengurangi variance penilaian dan mencegah overfitting pada validation tunggal. cv=5 adalah kompromi umum antara stabilitas dan waktu komputasi.
- Alternatif: RandomizedSearchCV (lebih cepat pada grid besar), Bayesian optimization (lebih sample-efficient), atau cv=10 (lebih stabil, lebih lambat).

### G. Kenapa Parameter Grid Tersebut?

- Logistic Regression: `C` mengatur kekuatan regularisasi (kecil=lebih kuat). `solver` dipilih yang kompatibel untuk konvergensi stabil.
- KNN: `n_neighbors` menyeimbangkan bias-variance; `weights` uniform vs distance; `metric` (euclidean/manhattan) berefek pada bentuk tetangga.
- SVM: `C` (margin vs error), `gamma` (jangkauan pengaruh), `kernel` (linear vs RBF) untuk fleksibilitas non-linear.
- Decision Tree: `max_depth`, `min_samples_split/leaf` untuk regularisasi pohon agar tidak overfit; `criterion` (gini/entropy) perbedaan minor performa.

### H. Pencegahan Data Leakage

- Scaling dilakukan setelah split dan fit hanya di train, lalu transform test/predict. Ini mencegah kebocoran statistik (mean/std) dari test ke train.
- Encoding kategori: “fit” OHE seharusnya di train saja; di sini diatasi dengan penyelarasan kolom train vs predict sebelum inferensi (menambah kolom hilang=0, drop ekstra, urutkan). Praktik produksi: pakai `ColumnTransformer`+`Pipeline`.

### I. Mengatasi Imbalance: class_weight vs SMOTE

- class_weight='balanced' (LogReg/SVM/DT) memberi penalti lebih besar pada kelas minoritas.
- SMOTE menambah sampel sintetis untuk kelas minoritas. Kelebihan: memperkaya sinyal; Kekurangan: risiko overfit jika tidak hati-hati.
- Pilih sesuai konteks: jika data terbatas dan pola minoritas jelas, SMOTE bisa membantu. Jika ingin sederhana dan aman, mulai dari class_weight.

### J. Threshold Tuning & Kalibrasi Probabilitas

- Setelah memilih model terbaik, tuning ambang (threshold) dapat menyeimbangkan precision vs recall sesuai biaya bisnis (misal target recall Macet ≥ 0.8).
- Kalibrasi probabilitas (Platt scaling/Isotonic) meningkatkan kualitas probabilitas untuk pengambilan keputusan berbasis skor (cutoff dinamis).

### K. Evaluasi Tambahan yang Relevan

- PR Curve (Precision-Recall) lebih informatif daripada ROC saat imbalance.
- Cost-sensitive analysis: tetapkan matrix biaya bisnis (FP vs FN) untuk memilih threshold optimal.

### L. Reproducibility & Robustness

- Set `random_state` pada split/model agar eksperimen replikasi.
- Tangani kategori langka (rare) dengan penggabungan “Other” bila perlu.
- Tangani missing values (jika ada) dengan imputer yang di-fit di train.

### M. Potensi Pertanyaan Dosen & Jawaban Singkat

1. Kenapa pilih F1, bukan accuracy? → Karena data cenderung tidak seimbang dan biaya FN tinggi; F1 menyeimbangkan precision-recall.
2. Kenapa perlu scaling? → Model berbasis jarak/gradien sensitif skala fitur; tanpa scaling, fitur besar mendominasi.
3. Kenapa OHE, bukan label encoding? → Hindari ordinal palsu antar kategori yang menyesatkan model linier/jarak.
4. Bagaimana cegah leakage? → Fit scaler/encoder hanya di train; untuk predict, samakan kolom dengan train dan gunakan transform yang sama.
5. Kenapa cv=5? → Kompromi stabilitas vs waktu; mengurangi variance estimasi performa.
6. Bagaimana jika data makin imbalanced? → Pertimbangkan class_weight, SMOTE, PR AUC, dan threshold tuning berbasis biaya bisnis.
7. Bagaimana interpretasi model? → Gunakan DT feature importance; untuk LogReg lihat koefisien; untuk SVM gunakan SHAP/LIME.

### N. Next Steps (Pekerjaan Lanjutan yang Direkomendasikan)

- Bungkus preprocessing+model dalam `Pipeline`/`ColumnTransformer` agar anti-leak dan mudah deploy.
- Tambahkan evaluasi PR AUC dan threshold tuning berbasis biaya.
- Coba class_weight/SMOTE dan bandingkan terhadap baseline F1/Recall kelas Macet.
- Uji stabilitas dengan k-fold lebih besar atau repeated CV.
- Pertimbangkan model ensemble (Random Forest, XGBoost/LightGBM) untuk kinerja lebih tinggi dan feature importance yang lebih robust.
