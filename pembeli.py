import pandas as pd
import csv
import time

def baca_menu_dari_csv():
    try:
        menu_df = pd.read_csv("DaftarMenu.csv", header=None, names=["Nama Menu", "Harga"])
        return menu_df
    except FileNotFoundError:
        print("Menu tidak ditemukan. Pastikan file 'DaftarMenu.csv' tersedia.")
        return pd.DataFrame(columns=["Nama Menu", "Harga"])

def baca_voucher_dari_csv():
    try:
        voucher_df = pd.read_csv("voucher.csv", header=None, names=["Kode Voucher", "Diskon"])
        return voucher_df
    except FileNotFoundError:
        print("Voucher tidak ditemukan. Pastikan file 'voucher.csv' tersedia.")
        return pd.DataFrame(columns=["Kode Voucher", "Diskon"])

def simpan_orderan_ke_csv(orderan):
    with open("orderan.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(orderan)

def tampilkan_menu(menu_df):
    print("\n=== Daftar Menu ===")
    if not menu_df.empty:
        print(menu_df.to_string(index=False))  
    else:
        print("Menu kosong. Tidak ada data untuk ditampilkan.")

def animasi_proses():
    print("\nPesanan sedang diproses...", end="", flush=True)
    time.sleep(1)
    print(".", end="", flush=True)
    time.sleep(1)
    print(".", flush=True)
    time.sleep(1)
    print("\nPesanan sedang dibuat dan akan dikirimkan ke alamatmu jika sudah siap!")

def pilih_kecamatan():
    kecamatan = {
        "kaliwates": 15000,
        "sumbersari": 12000,
        "patrang": 15000
    }
    while True:
        lokasi = input("Masukkan kecamatan (Kaliwates/Sumbersari/Patrang): ").lower()
        if lokasi in kecamatan:
            return lokasi, kecamatan[lokasi]
        else:
            print("Kecamatan tidak tersedia. Silakan pilih antara Kaliwates, Sumbersari, atau Patrang.")

def hitung_total(keranjang, ongkir, voucher_df, kode_voucher=None):
    subtotal = sum(data["total_harga"] for data in keranjang.values()) 
    diskon = 0
    if kode_voucher and kode_voucher.upper() in voucher_df["Kode Voucher"].values:
        diskon_persen = voucher_df.loc[voucher_df["Kode Voucher"] == kode_voucher.upper(), "Diskon"].values[0]
        diskon = subtotal * (diskon_persen / 100)
        print(f"Voucher {kode_voucher.upper()} diterapkan! Anda mendapatkan diskon {diskon_persen}%.")
    total = subtotal - diskon + ongkir
    return subtotal, diskon, total

def buat_pesanan(menu_df):
    keranjang = {}
    voucher_df = baca_voucher_dari_csv()

    while True:
        nama_menu = input("\nMasukkan nama menu (atau ketik 'selesai' untuk checkout): ").lower()
        if nama_menu == "selesai":
            break
        elif nama_menu in menu_df["Nama Menu"].str.lower().values:
            try:
                jumlah = int(input(f"Masukkan jumlah {nama_menu}: "))
                harga = menu_df.loc[menu_df["Nama Menu"].str.lower() == nama_menu, "Harga"].values[0]
                
                if nama_menu in keranjang:
                    keranjang[nama_menu]["jumlah"] += jumlah
                    keranjang[nama_menu]["total_harga"] += harga * jumlah
                else:
                    keranjang[nama_menu] = {"jumlah": jumlah, "harga_satuan": harga, "total_harga": harga * jumlah}
                
                print(f"{jumlah} {nama_menu} ditambahkan ke keranjang.")
            except ValueError:
                print("Jumlah harus berupa angka.")
        else:
            print("Menu tidak ditemukan. Coba lagi.")

    if keranjang:
        print("\n=== Ringkasan Pesanan ===")
        ringkasan = []
        for nama_menu, data in keranjang.items():
            ringkasan.append([nama_menu, data["jumlah"], data["total_harga"]])
        
        ringkasan_df = pd.DataFrame(ringkasan, columns=["Nama Menu", "Jumlah", "Total Harga"])
        print(ringkasan_df.to_string(index=False))
        
        kecamatan, ongkir = pilih_kecamatan()
        print(f"Ongkir ke kecamatan {kecamatan.capitalize()}: Rp{ongkir}")

        kode_voucher = input("Masukkan kode voucher (jika ada) atau tekan Enter: ").upper()

        subtotal, diskon, total = hitung_total(keranjang, ongkir, voucher_df, kode_voucher)

        print(f"\nSubtotal: Rp{subtotal}")
        if diskon > 0:
            print(f"Diskon: Rp{int(diskon)}")
        print(f"Total yang harus dibayar: Rp{total}")

        simpan = input("\nKonfirmasi pesanan? (y/n): ").lower()
        if simpan == "y":
            for nama_menu, data in keranjang.items():
                simpan_orderan_ke_csv([nama_menu, data["jumlah"], data["total_harga"]])
            animasi_proses()
            print("\nPesanan berhasil disimpan. Terima kasih!")
        else:
            print("Pesanan dibatalkan.")
    else:
        print("Tidak ada item yang dipesan.")

def main():
    menu_df = baca_menu_dari_csv()
    if menu_df.empty:
        return
    tampilkan_menu(menu_df)
    buat_pesanan(menu_df)

if __name__ == "__main__":
    main()
