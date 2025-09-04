# =============================
# SECTION 1: Statistik Sederhana
# =============================
# Program ini meminta user untuk memasukkan jumlah data dan nilai-nilai data secara manual.
# Program akan menghitung rata-rata dan median dari data tersebut tanpa menggunakan fungsi .mean atau .median.
# Data diurutkan menggunakan fungsi sort() sebelum mencari median.
# Input divalidasi agar hanya menerima angka yang benar.


# data = []  # List untuk menyimpan data yang diinput user

# # Input jumlah data, harus angka > 0
# while True:
#     n_str = input("Masukkan jumlah data: ")
#     if n_str.isdigit() and int(n_str) > 0:
#         n = int(n_str)  # Konversi ke integer
#         break
#     else:
#         print("Input harus berupa angka lebih dari 0!")

# # Input nilai data satu per satu, harus angka (bisa desimal)
# for i in range(n):
#     while True:
#         val = input(f"Masukkan data ke-{i+1}: ")
#         try:
#             num = float(val)  # Konversi ke float
#             data.append(num)  # Tambahkan ke list data
#             break
#         except ValueError:
#             print("Input harus berupa angka!")

# # Hitung rata-rata secara manual
# total = sum(data)  # Jumlah seluruh data
# mean = total / n   # Rata-rata = jumlah / banyak data

# # Urutkan data sebelum cari median
# data.sort()

# # Hitung median secara manual
# if n % 2 == 1:
#     # Jika jumlah data ganjil, median adalah data tengah
#     median = data[n // 2]
# else:
#     # Jika jumlah data genap, median adalah rata-rata dua data tengah
#     median = (data[n // 2 - 1] + data[n // 2]) / 2

# # Tampilkan hasil
# print(f"Data diurutkan: {data}")
# print(f"Rata-rata: {mean}")
# print(f"Median: {median}")



# SECTION 2: Menu & Fungsi Pasar Buah
# =============================

# Data awal buah dengan list 2D (nama, stok, harga)
daftar_buah_awal = [
    ["Apel", 20, 10000],
    ["Jeruk", 15, 15000],
    ["Anggur", 25, 20000]
]
daftar_buah = [buah.copy() for buah in daftar_buah_awal]  # Copy agar bisa dikembalikan ke data awal

def tampilkan_menu(): # Definisi menampilkan menu utama
    print("\nSelamat Datang di Pasar Buah")
    print("List Menu :")
    print("1. Menampilkan Daftar Buah")
    print("2. Tambah Buah Baru")
    print("3. Edit Buah")
    print("4. Hapus Buah")
    print("5. Hapus Semua Buah")
    print("6. Restore Daftar Buah") 
    print("0. Exit Program")

#________________________________________________________________________________________________
# Definisi fungsi menghapus semua buah dengan konfirmasi
def hapus_semua_buah(): 
    print("\nHapus Semua Buah")
    if not daftar_buah:
        print("Daftar buah sudah kosong.")
        return #Jika daftar buah kosong, keluar dari fungsi
    konfirmasi = input("Yakin ingin menghapus semua buah? (y/n): ").lower()
    if konfirmasi == 'y': # Jika user konfirmasi 'y', hapus semua buah
        daftar_buah.clear()
        print("Semua buah berhasil dihapus!")
    else:
        print("Penghapusan dibatalkan.") # Jika user ketik 'n', batalkan penghapusan
#_______________________________________________________________________________________________
# Definisi fungsi untuk mengedit data buah berdasarkan index
def edit_buah(): 
    print("\nEdit Buah")
    tampilkan_daftar_buah()
    if not daftar_buah:
        print("Tidak ada buah untuk diedit.") # Jika daftar buah kosong, keluar dari fungsi
        return
    idx = input("Masukkan index buah yang ingin diedit: ")
    if not idx.isdigit() or int(idx) < 0 or int(idx) >= len(daftar_buah):
        print("Index tidak valid!")
        return
    idx = int(idx)
    nama_lama, stok_lama, harga_lama = daftar_buah[idx]
    nama = input(f"Nama buah [{nama_lama}]: ") or nama_lama
    stok = input(f"Stok buah [{stok_lama}]: ")
    harga = input(f"Harga buah [{harga_lama}]: ")
    try:
        stok = int(stok) if stok else stok_lama
        harga = int(harga) if harga else harga_lama
    except ValueError: # Jika input tidak sesuai maka ada error
        print("Stok dan harga harus berupa angka!")
        return
    daftar_buah[idx] = [nama, stok, harga]
    print(f"Buah pada index {idx} berhasil diupdate!")

#_______________________________________________________________________________________________
# Definisi fungsi untuk menghapus buah berdasarkan index
def hapus_buah(): 
    print("\nHapus Buah")
    tampilkan_daftar_buah()
    if not daftar_buah:
        print("Tidak ada buah untuk dihapus.") # Jika daftar buah kosong, keluar dari fungsi
        return
    idx = input("Masukkan index buah yang ingin dihapus: ") # Minta input index buah yang ingin dihapus
    if not idx.isdigit() or int(idx) < 0 or int(idx) >= len(daftar_buah):
        print("Index tidak valid!")
        return
    idx = int(idx)
    buah = daftar_buah.pop(idx)
    print(f"Buah '{buah[0]}' berhasil dihapus!") # Informasi buah yang dihapus

#_______________________________________________________________________________________________
# Definisi fungsi menampilkan daftar buah
def tampilkan_daftar_buah():
    print("\nDaftar Buah")
    print("=" * 43)
    if not daftar_buah:
        print("=== Daftar Buah Kosong ===")
        return
    print(f"{'Index':<5} | {'Nama':<10} | {'Stock':<5} | {'Harga':>12} |")
    print("-" * 43)
    for i, buah in enumerate(daftar_buah):
        nama = buah[0]
        stok = buah[1]
        #  Format untuk tetap sejajar
        tab = '\t' if len(nama) < 8 else ''
        # Format harga ke Rupiah dengan pemisah titik
        harga_rp = f"Rp{buah[2]:,}".replace(",", ".")
        print(f"{i:<5} | {nama:<10} | {stok:<5} | {harga_rp:>12} |")

#_______________________________________________________________________________________________
# Definisi fungsi menambahkan buah baru
def tambah_buah_baru():
    print("\nTambah Buah Baru")
    nama = input("Masukkan nama buah: ")
    while True:
        stok = input("Masukkan stok buah: ") # Input stok buah dengan divalidasi
        if stok.isdigit() and int(stok) >= 0:
            stok = int(stok)
            break
        else:
            print("Stok harus berupa angka >= 0!")
    while True:
        harga = input("Masukkan harga buah: ") # Input harga buah dengan divalidasi
        if harga.isdigit() and int(harga) >= 0:
            harga = int(harga)
            break
        else:
            print("Harga harus berupa angka >= 0!") 
    daftar_buah.append([nama, stok, harga])
    print(f"Buah '{nama}' berhasil ditambahkan!")

def restore_daftar_buah():
    global daftar_buah
    daftar_buah = [buah.copy() for buah in daftar_buah_awal]
    print("Daftar buah berhasil direstore ke data awal!")

# ==============================================================================================
while True:
    tampilkan_menu()
    pilihan = input("Masukkan angka Menu yang ingin dijalankan: ")

    if pilihan == "1":
        tampilkan_daftar_buah()
    elif pilihan == "2":
        tambah_buah_baru()
    elif pilihan == "3":
        edit_buah()
    elif pilihan == "4":
        hapus_buah()
    elif pilihan == "5":
        hapus_semua_buah()
    elif pilihan == "6":
        restore_daftar_buah()
    elif pilihan == "0":
        print("Program selesai. Terima kasih sudah berbelanja di Pasar Buah!")
        break
    else:
        print("Menu tidak valid, silakan pilih lagi.")
