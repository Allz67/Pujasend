import pandas as pd
import csv
import time
import qrcode

def baca_menu_dari_csv():
    try:
        menu_df = pd.read_csv("stand.csv")
        return menu_df
    except FileNotFoundError:
        print("File 'stand.csv' tidak ditemukan.")
        return pd.DataFrame(columns=["Stand", "Nama Menu", "Harga"])

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

def tampilkan_stand(stand_df):
    print("\n=== Daftar Stand ===")
    stands = stand_df["Stand"].unique()  
    for i, stand in enumerate(stands, start=1):
        print(f"{i}. {stand}")
    return stands

def pilih_stand(stand_df):
    stands = tampilkan_stand(stand_df)
    while True:
        try:
            pilihan = int(input("\nPilih nomor stand: "))
            if 1 <= pilihan <= len(stands):
                return stands[pilihan - 1]
            else:
                print("Pilihan tidak valid. Coba lagi.")
        except ValueError:
            print("Input harus berupa angka. Coba lagi.")

def animasi_proses():
    print("\nPesanan sedang diproses...", end="", flush=True)
    time.sleep(1)
    print(".", end="", flush=True)
    time.sleep(1)
    print(".", flush=True)
    time.sleep(1)
    print("\nPesanan sedang dibuat dan akan dikirimkan ke alamatmu jika sudah siap!")

def pilih_kecamatan():
    tarif = {
        "kaliwates": {"cepat": 15000, "standar": 13000, "hemat": 11000},
        "sumbersari": {"cepat": 10000, "standar": 8000, "hemat": 6000},
        "patrang": {"cepat": 12000, "standar": 10000, "hemat": 8000},
    }
    while True:
        lokasi = input("Masukkan kecamatan (Kaliwates/Sumbersari/Patrang): ").lower()
        if lokasi in tarif:
            while True:
                print("\nOpsi pengiriman:")
                print("1. Cepat (lebih mahal, lebih cepat)")
                print("2. Standar (seimbang)")
                print("3. Hemat (lebih murah, lebih lama)")
                try:
                    metode = int(input("Pilih metode pengiriman (1/2/3): "))
                    if metode == 1:
                        return lokasi, tarif[lokasi]["cepat"]
                    elif metode == 2:
                        return lokasi, tarif[lokasi]["standar"]
                    elif metode == 3:
                        return lokasi, tarif[lokasi]["hemat"]
                    else:
                        print("Pilihan tidak valid. Coba lagi.")
                except ValueError:
                    print("Input harus berupa angka. Coba lagi.")
        else:
            print("Kecamatan tidak tersedia. Silakan pilih antara Kaliwates, Sumbersari, atau Patrang.")

def hitung_total(keranjang, ongkir, voucher_df, kode_voucher=None):
    subtotal = sum(data["total_harga"] for data in keranjang.values()) 
    diskon = 0
    if kode_voucher:
        if kode_voucher.upper() in voucher_df["Kode Voucher"].values:
            diskon_persen = voucher_df.loc[voucher_df["Kode Voucher"] == kode_voucher.upper(), "Diskon"].values[0]
            diskon = subtotal * (int(diskon_persen) / 100)
            print(f"Voucher {kode_voucher.upper()} diterapkan! Anda mendapatkan diskon {diskon_persen}%.")
        else:
            print("Voucher tidak valid atau tidak berlaku.")
    total = subtotal - diskon + ongkir
    return subtotal, diskon, total
        
def tampilkan_menu(menu_df, stand):
    print(f"\n=== Menu di Stand {stand.capitalize()} ===")
    stand_menu = menu_df[menu_df["Stand"].str.lower() == stand.lower()]
    if not stand_menu.empty:
        for idx, (index, row) in enumerate(stand_menu.iterrows(), start=1):
            print(f"{idx}. {row['Nama Menu']} - Rp{row['Harga']}")
    else:
        print("Menu kosong. Tidak ada data untuk ditampilkan.")

def buat_pesanan(menu_df):
    keranjang = {}
    voucher_df = baca_voucher_dari_csv()

    while True:
        stand = pilih_stand(menu_df)
        tampilkan_menu(menu_df, stand)
        while True:
            try:
                pilihan_menu = int(input("\nMasukkan nomor menu (atau ketik 'selesai' untuk checkout): "))
                stand_menu = menu_df[menu_df["Stand"].str.lower() == stand.lower()]
                if 1 <= pilihan_menu <= len(stand_menu):
                    nama_menu = stand_menu.iloc[pilihan_menu - 1]["Nama Menu"]
                    harga = stand_menu.iloc[pilihan_menu - 1]["Harga"]
                    jumlah = int(input(f"Masukkan jumlah {nama_menu}: "))

                    if nama_menu in keranjang:
                        keranjang[nama_menu]["jumlah"] += jumlah
                        keranjang[nama_menu]["total_harga"] += harga * jumlah
                    else:
                        keranjang[nama_menu] = {"jumlah": jumlah, "harga_satuan": harga, "total_harga": harga * jumlah}

                    print(f"{jumlah} {nama_menu} ditambahkan ke keranjang.")
                else:
                    print("Menu tidak ditemukan. Coba lagi.")
            except ValueError:
                if input("\n Apakah anda sudah yakin?(y/t) ").lower() == "y":
                    break
                else:
                    print("Pilihan tidak valid. Coba lagi.")

        if input("Pilih stand lain? (y/n): ").lower() != "y":
            break

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
        print(f"Ongkir: Rp{ongkir}")
        print(f"Total yang harus dibayar: Rp{total}")

        simpan = input("\nKonfirmasi pesanan? (y/n): ").lower()
        if simpan == "y":
            for nama_menu, data in keranjang.items():
                simpan_orderan_ke_csv([nama_menu, data["jumlah"], data["total_harga"]])
            bayar = input('Silahkan pilih metode pembayaran (QRIS/cash): ').lower()
            if bayar == 'cash':
                print(f'Silahkan siapkan uang tunai sebesar {total} ya! ^^')
            elif bayar == 'qris':
                data = "bayar woi"
                qr = qrcode.QRCode(version=1, box_size=1, border=1)  
                qr.add_data(data)
                qr.make(fit=True)
                qr_matrix = qr.get_matrix()
                ascii_qr = "\n".join(
                   "".join("██" if cell else "  " for cell in row) for row in qr_matrix
                )
                print(f'Silahkan scan qrcode berikut dengan total {total}')
                print(ascii_qr)
                while True:
                    validasi_bayar = input("Tekan 'enter' jika telah selesai melakukan pembayaran: ")
                    if validasi_bayar == "":
                        break
                    else:
                        print("Input tidak valid. Harap tekan 'enter' setelah selesai melakukan pembayaran.")
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
    buat_pesanan(menu_df)

if __name__ == "__main__":
    main()
