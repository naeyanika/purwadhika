# # inisialisasi variabel
# x = 4
# y = 3
# z = 2

# w = ((float(x) + float(y) * float(z)) / (float(x) * float(x) * float(y))) ** float(z)
# print("hasil w=", w)

# # y * z berarti 3 * 2 = 6 (perkalian)
# # x + (hasil sebelumnya) berarti 4 + 6 = 10 (penjumlahan)
# # x * x * y berarti 4 * 4 * 3 = 48 (perkalian)
# # (hasil penjumlahan) / (hasil perkalian) berarti 10 / 48 = 0.2083... (pembagian)
# # (hasil pembagian) ** z berarti 0.2083... pangkat 2 = 0.0434... (pangkat)

# angka = int(input("Silakan masukkan angka berapapun : "))
# hasil_kuadrat = angka ** 2
# print(f"Kuadrat dari {angka} = {hasil_kuadrat}")

# member_nct_dream = 7
# teman_per_member = int(input("Setiap member NCT Dream membawa berapa teman? "))
# total_orang = member_nct_dream + (member_nct_dream * teman_per_member)
# print(f"Total orang yang hadir: {total_orang} (7 member + {member_nct_dream * teman_per_member} teman)")

#____________________________________________________________________________________________________________________________
#List harga buah (menyimpan harga buah)
harga_apel = 10000
harga_jeruk = 15000
harga_anggur = 20000

#Input jumlah buah (input field untuk buah)
jumlah_apel = int(input("Masukkan jumlah apel: "))
jumlah_jeruk = int(input("Masukkan jumlah jeruk: "))
jumlah_anggur = int(input("Masukkan jumlah anggur: "))

# hitung total harga per buah ( mengalikan jumlah buah dengan harga satuan untuk mendapatkan total harga masing2 buah)
total_apel = jumlah_apel * harga_apel
total_jeruk = jumlah_jeruk * harga_jeruk
total_anggur = jumlah_anggur * harga_anggur

# hitung total keseluruhan (menjumlahkan total harga dari semua buah)
total = total_apel + total_jeruk + total_anggur

print("\nDetail Belanja") # menampilkan detail
print(f"Apel: {jumlah_apel} x {harga_apel} = {total_apel}")
print(f"Jeruk: {jumlah_jeruk} x {harga_jeruk} = {total_jeruk}")
print(f"Anggur: {jumlah_anggur} x {harga_anggur} = {total_anggur}")
print(f"Total: {total}")

#______________________________________________________________________________________________
# Buat form input untuk menghitung total hari
total_hari = int(input("Masukkan total hari: "))

#sumber : https://en.m.wikipedia.org/wiki/360-day_calendar
'''The 360-day calendar is a method of measuring durations used in financial markets, in computer models, in ancient literature, and in prophetic literary genres.

It is based on merging the three major calendar systems into one complex clock[citation needed], with the 360-day year derived from the average year of the lunar and the solar: (365.2425 (solar) + 354.3829 (lunar))/2 = 719.6254/2 = 359.8127 days, rounding to 360.

A 360-day year consists of 12 months of 30 days each, so to derive such a calendar from the standard Gregorian calendar, certain days are skipped.

For example, the 27th of June (Gregorian calendar) would be the 4th of July in the USA.'''

#Floor division '//' mengambil bagian bulat, berapa kali bisa dibagi dan modulus '%' untuk mengambil sisanya

#hitung tahun
tahun = total_hari // 360 # membagi total hari dengan 360 untuk menandapatkan jumlah tahun, ini dengan asumsi per bulan di ambil 30 hari, jadi saya ambil satu tahun itu 360 hari
sisa_hari = total_hari % 360 # ambil sisa hari setelah dihitung tahun, agar sisa ini bisa dihitung ke bulan

#hitung bulan
bulan = sisa_hari // 30 #sama seperti di atas, ini mengambil 30 karena saya mengambil asusmsi satu tahun 360 hari, disini saya mengambil jumlah bulan ( 1 bulan = 30 hari)
sisa_hari = sisa_hari % 30 #ambil sisa hari setelah dihitung bulan, agar sisa ini bisa dihitung ke minggu

#hitung minggu
minggu = sisa_hari // 7 #membagi sisa hari dengan 7 untuk mendapatkan jumlah minggu
sisa_hari = sisa_hari % 7 #ambil sisa hari setelah dihitung minggu, agar sisa ini bisa dihitung ke hari

#hitung hari
hari = sisa_hari #jumlah hari yang tersisa

#output
print(f"{total_hari} hari adalah {tahun} tahun, {bulan} bulan, {minggu} minggu, dan {hari} hari.")