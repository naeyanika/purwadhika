# Buat definisi luas segitiga beserta rumus
def hitung_luas_segitiga():
    alas = float(input("Masukan Alas Segitiga : "))
    tinggi = float(input("Masukan Tinggi Segitiga : "))
    luas = 0.5 * alas * tinggi
    print(f"Luas Segitiga Tersebut Adalah {luas}\n")

# Buat definisi luas persegi beserta rumus
def hitung_luas_persegi():
    sisi = float(input("Masukan Sisi Dari Persegi : "))
    luas = sisi * sisi
    print(f"Luas Persegi Tersebut Adalah {luas}\n")

# Program Menu
print("MENU MENGHITUNG RUMUS LUAS SEGITIGA DAN PERSEGI")
print("Masukan Angka 1 Untuk Menghitung Luas Segitiga")
print("Masukan Angka 2 Untuk Menghitung Luas Persegi")

pilihan = input("Pilihan Menu Yang Diinginkan : ")

if pilihan == "1":
    hitung_luas_segitiga()
elif pilihan == "2":
    hitung_luas_persegi()
else:
    print("Masukan Inputan Yang Benar")
