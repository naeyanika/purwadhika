# # harga buah
# HARGA = {
#     "apel": 10000,
#     "jeruk": 15000,
#     "anggur": 20000,
# }

# def rupiah(n: int) -> str:

#     return f"{n:,}".replace(",", ".")
#     #Fungsi untuk memformat angka ke format rupiah sederhana.
#     #Contoh: 160000 -> '160.000'

# def input_bilangan_bulat(prompt: str) -> int:
#     #Fungsi untuk meminta input bilangan bulat >= 0 dari user.
#     #Akan terus meminta input sampai user memasukkan angka yang valid.
#     while True:
#         s = input(prompt).strip()
#         try:
#             val = int(s)
#             if val < 0:
#                 print("Masukan harus >= 0, coba lagi ya.")
#                 continue
#             return val
#         except ValueError:
#             print("Masukan harus angka bulat, coba lagi ya.")

# def input_uang(prompt: str) -> int:
#     #Fungsi untuk meminta input uang (bilangan bulat >= 0) dari user.
#     #Akan terus meminta input sampai user memasukkan angka yang valid.
#     while True:
#         s = input(prompt).strip()
#         try:
#             val = int(s)
#             if val < 0:
#                 print("Uang tidak boleh negatif, coba lagi ya.")
#                 continue
#             return val
#         except ValueError:
#             print("Masukan harus angka bulat, coba lagi ya.")

# # --------------------- Form Input --------------------- #
# while True:
#     # --- Input jumlah buah ---
#     jml_apel   = input_bilangan_bulat("Masukkan Jumlah Apel  : ")
#     jml_jeruk  = input_bilangan_bulat("Masukkan Jumlah Jeruk : ")
#     jml_anggur = input_bilangan_bulat("Masukkan Jumlah Anggur: ")

#     # --- Hitung detail ---
#     # hitung subtotal untuk setiap buah dan total keseluruhan belanjaan
#     sub_apel   = jml_apel   * HARGA["apel"]
#     sub_jeruk  = jml_jeruk  * HARGA["jeruk"]
#     sub_anggur = jml_anggur * HARGA["anggur"]
#     total      = sub_apel + sub_jeruk + sub_anggur

#     # --- Cetak ringkasan belanja ---
#     # menapilkan detail belanja (jumlah, harga, satuan dan subtotal) dan total belanja
#     print("\nDetail Belanja")
#     print(f"Apel  : {jml_apel} x {rupiah(HARGA['apel'])}  = {rupiah(sub_apel)}")
#     print(f"Jeruk : {jml_jeruk} x {rupiah(HARGA['jeruk'])} = {rupiah(sub_jeruk)}")
#     print(f"Anggur: {jml_anggur} x {rupiah(HARGA['anggur'])}= {rupiah(sub_anggur)}")
#     print(f"\nTotal : {rupiah(total)}")

#     total_bayar = total

#     # --- Input uang dan tentukan kondisi ---
#     # Masukan pembayaran dari user
#     uang = input_uang(f"\nMasukkan jumlah uang (Total bayar: {rupiah(total_bayar)}): ")

#     if uang < total_bayar:
#         # Jika uang pertama kurang dari total bayar:
#         kekurangan = total_bayar - uang
#         print(f"Uang anda kurang sebesar {rupiah(kekurangan)}.")
#         # minta user memasukkan kekurangan (boleh lebih dari kekurangan)
#         tambahan = input_uang(f"Masukkan kekurangan sebesar {rupiah(kekurangan)} (boleh lebih): ")
#         total_uang = uang + tambahan
#         if total_uang < total_bayar:
#             # Transaksi batal jika masih kurang
#             kekurangan2 = total_bayar - total_uang
#             print(f"Maaf, uang anda masih kurang {rupiah(kekurangan2)}. Transaksi dibatalkan.")
#         elif total_uang == total_bayar:
#             # Transaksi berhasil jika penambahan pas atau lebih
#             print("Terima kasih, pembayaran pas.")
#         else:
#             # Hitung kembalian jika ada kelebihan
#             kembalian = total_uang - total_bayar
#             print("Terima kasih")
#             print(f"Uang kembali anda : {rupiah(kembalian)}")
#     elif uang == total_bayar:
#         # Transaksi berhasil jika uang pas
#         print("Terima kasih")
#     else:
#         # Hitung kembalian jika lebih bayar
#         kembalian = uang - total_bayar
#         print("Terima kasih")
#         print(f"Uang kembali anda : {rupiah(kembalian)}")

#     # Setelah transaksi selesai atau dibatalkan:
#     ulang = input("\nApakah ingin melakukan transaksi lagi? (y/n): ").strip().lower()
#     if ulang != "y":
#         print("Terima kasih telah berbelanja!")
#         break


# Input kalimat
kalimat = input("Masukan Sebuah Kata/Kalimat : ")

# Variabel penghitung
jumlah_huruf = 0
jumlah_angka = 0
jumlah_lain = 0

# Loop setiap karakter dalam kalimat
for char in kalimat:
    if char.isalpha():       # untuk cek apakah huruf
        jumlah_huruf += 1
    elif char.isdigit():     # untuk cek apakah angka
        jumlah_angka += 1
    else:
        jumlah_lain += 1

# Output hasil
print("Jumlah Huruf Pada Karakter Sebanyak", jumlah_huruf)
print("Jumlah Angka Pada Kalimat Sebanyak", jumlah_angka)
print("Jumlah Karakter Lain Pada Kalimat Sebanyak", jumlah_lain)
