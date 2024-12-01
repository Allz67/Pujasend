import pandas as pd
import csv
import os

username = "aliakanina"
#================================================================================

def baca_menu_dari_csv(): 
    try:
        with open("DaftarMenu.csv", mode="r") as file:
            reader = csv.DictReader(file)
            menu={}
            for row in reader:
                if row['username_penjual'] == username:
                    nama_menu = row['nama_menu']
                    harga_menu = int(row['harga_menu'])
                    menu[nama_menu] = harga_menu
            return menu
    except FileNotFoundError:
        return {}
    
menu = baca_menu_dari_csv()

def simpan_menu_ke_csv():
    with open("DaftarMenu.csv", "w", newline="") as file:
        writer = csv.writer(file)
        menu = baca_menu_dari_csv()
        for nama_menu, harga_menu in menu.items():
            writer.writerow([nama_menu, harga_menu])

def baca_orderan_dari_csv():
    try:
        with open("orderan.csv", "r") as file:
            reader = csv.reader(file)
            return [baris for baris in reader]
    except FileNotFoundError:
        return []  # Jika file belum ada, kembalikan list kosong

def simpan_orderan_ke_csv():
    with open("orderan.csv", "w", newline="") as file:
        writer = csv.writer(file)
        for orderan in daftar_orderan:
            writer.writerow(orderan)

def baca_orderan_selesai_dari_csv():
    try:
        with open("orderan_selesai.csv", "r") as file:
            reader = csv.reader(file)
            return [baris for baris in reader]
    except FileNotFoundError:
        return []  # Jika file belum ada, kembalikan list kosong

def simpan_orderan_selesai_ke_csv():
    with open("orderan_selesai.csv", "w", newline="") as file:
        writer = csv.writer(file)
        for orderan_selesai in daftar_orderan_selesai:
            writer.writerow(orderan_selesai)

# kelola menu
def kelola_menu():
    while True:
        header("Penjual > Kelola Menu")
        print("[1] Lihat Menu\n[2] Tambah Menu\n[3] Ubah Menu\n[4] Hapus Menu\n[5] Kembali ke Menu Utama")
        pilihan = input("Pilih opsi: ")

        if pilihan == "1":
            header('Penjual > Kelola Menu > Lihat Menu')
            print("\nDaftar Menu:")
            angka =1
            if menu:
                for nama_menu,harga_menu in menu.items():
                    print(f"{angka}. {nama_menu}\t Rp{harga_menu}")
                    angka +=1
            else:
                print("Menu masih kosong.")
            x = input("\nEnter untuk kembali.")
            if x == '':
                continue

        elif pilihan == "2":
            header('Penjual > Kelola Menu > Tambah Menu')
            nama_menu = input("Masukkan nama menu: ")
            if nama_menu in menu:
                print(f"{nama_menu} sudah ada di menu.")
            else:
                try:
                    harga_menu = int(input("Masukkan harga menu: "))
                    menu[nama_menu] = harga_menu
                    simpan_menu_ke_csv()
                    print(f"{nama_menu} berhasil ditambahkan!")
                except ValueError:
                    print("Harga harus berupa angka.")

        elif pilihan == "3":
            if menu:
                for nama_menu,harga_menu in menu.items():
                    print(f"{angka}. {nama_menu}\t Rp{harga_menu}")
                    angka +=1
            else:
                print("Menu masih kosong.")
            nama_menu = input("Masukkan nama menu yang ingin diubah: ")
            if nama_menu in menu:
                print(f"{nama_menu} sudah ada di menu.")
                ubah = input("Apakah Anda ingin mengubah nama atau harga menu? (y untuk ya, b untuk batal): ").lower()
        
                if ubah == 'y':
                    nama_baru = input("Masukkan nama baru untuk menu: ")
                    try:
                        harga_baru = int(input("Masukkan harga baru untuk menu: "))
                        menu[nama_baru] = harga_baru  # Mengubah nama dan harga menu 
                        del menu[nama_menu]  # Menghapus menu lama
                        simpan_menu_ke_csv()  
                        print(f"Menu {nama_menu} berhasil diubah menjadi {nama_baru} dengan harga Rp{harga_baru}.")
                    except ValueError:
                        print("Harga harus berupa angka.")
                
                elif ubah == 'b':
                    print("Perubahan dibatalkan.")
                else:
                    print("Pilihan tidak valid.")
            else:
                print(f"{nama_menu} tidak ditemukan di menu.")

        elif pilihan == "4":
            nama_menu = input("Masukkan nama menu yang ingin dihapus: ")
            if nama_menu in menu:
                del menu[nama_menu]
                simpan_menu_ke_csv()
                print(f"{nama_menu} berhasil dihapus!")
            else:
                print("Menu tidak ditemukan.")
        elif pilihan == "5":
            break
        else:
            print("Pilihan tidak valid. Coba lagi.")

def kelola_orderan():
    while True:
        print("\n=== Kelola Orderan ===")
        print("1. Lihat Orderan Masuk")
        print("2. Lihat Orderan yang Sedang Diproses")
        print("3. Kembali ke Menu Utama")
        pilihan = input("Pilih opsi: ")

        if pilihan == "1":
            print("\nOrderan Masuk:")
            if daftar_orderan:
                for indeks, orderan in enumerate(daftar_orderan):
                    print(f"{indeks + 1}. Pesanan: {orderan[0]}, Status: {orderan[1]}")
                    keputusan = input("Terima (TE) atau Tolak (TO)? (TE untuk Terima, TO untuk Tolak): ").lower()
                    if keputusan == 'te':
                        # Jika diterima, pindahkan ke daftar orderan sedang diproses
                        orderan[1] = "Diproses"
                        daftar_orderan_diproses.append(orderan)
                        daftar_orderan.remove(orderan)
                        simpan_orderan_ke_csv()
                        print(f"Orderan {orderan[0]} diterima dan sedang diproses.")
                    elif keputusan == 'to':
                        daftar_orderan.remove(orderan)
                        simpan_orderan_ke_csv()
                        print(f"Orderan {orderan[0]} ditolak.")
                    else:
                        print("Pilihan tidak valid. Kembali ke menu.")
            else:
                print("Tidak ada orderan masuk.")
        elif pilihan == "2":
            print("\nOrderan yang Sedang Diproses:")
            if daftar_orderan_diproses:
                for orderan in daftar_orderan_diproses:
                    print(f"Pesanan: {orderan[0]}, Status: {orderan[1]}")
                    keputusan = input("Selesai diproses (S) atau belum (B)? (S untuk Selesai, B untuk Belum): ").lower()
                    if keputusan == 's':
                        orderan[1] = "Selesai"
                        daftar_orderan_selesai.append(orderan)
                        daftar_orderan_diproses.remove(orderan)
                        simpan_orderan_selesai_ke_csv()
                        simpan_orderan_ke_csv()
                        print(f"Orderan {orderan[0]} selesai dan dipindahkan ke laporan penjualan.")
                    elif keputusan == 'b':
                        print(f"Orderan {orderan[0]} belum selesai diproses.")
                    else:
                        print("Pilihan tidak valid. Kembali ke menu.")
            else:
                print("Tidak ada orderan yang sedang diproses.")
        elif pilihan == "3":
            break
        else:
            print("Pilihan tidak valid. Coba lagi.")

def lihat_laporan_penjualan():
    print("\n=== Laporan Penjualan ===")
    if daftar_orderan_selesai:
        for orderan_selesai in daftar_orderan_selesai:
            print(f"Pesanan: {orderan_selesai[0]}, Status: {orderan_selesai[1]}")
    else:
        print("Tidak ada penjualan yang tercatat.")

daftar_orderan = baca_orderan_dari_csv()
daftar_orderan_diproses = []
daftar_orderan_selesai = baca_orderan_selesai_dari_csv()

def penjual():
    while True:
        header("Penjual")
        print("[1] Kelola Menu\n[2] Kelola Orderan\n[3] Lihat Laporan Penjualan\n[4] Keluar")   
        pilihan = input("Masukkan opsi: ")
        if pilihan == "1":
            kelola_menu()
        elif pilihan == "2":
            kelola_orderan()
        elif pilihan == "3":
            lihat_laporan_penjualan()
        elif pilihan == "4":
            logout()
            break
        else:
            print("Pilihan tidak valid. Coba lagi.")
#=========================================================================

def header(isi='', homepage=0):
    os.system('cls')
    with open('Header.txt', 'r', encoding='utf-8') as file:
        filetxt = file.read()
    print(filetxt)
    width = (67-len(isi))//2
    print(" "*width+isi+" "*width)
    print('='*67)
    if homepage == 1:
        kalimat = "Selamat Datang di aplikasi kami! ^-^"
        width = (67-len(kalimat))//2
        print(" "*width+kalimat+" "*width)
        kalimat = "Untuk masuk silahkan pilih opsi dibawah ini"
        width = (67-len(kalimat))//2
        print(" "*width+kalimat+" "*width)
        print("[1] Log in\n[2] Sign in\n[0] Keluar")
        while (True):
            pilihan = input("")
            match pilihan:
                case '1':
                    login()
                    break
                case '2':
                    registrasi()
                    break
                case '0':
                    logout()
                    break
                case _ :
                    print('Maaf, silahkan masukkan pilihan yang tersedia.')

def login():
    global username
    header('LOGIN')
    df = pd.read_csv('DaftarPengguna.csv')
    daftar_pengguna = df.set_index("username")
    masukkan_password = True
    while(True):
        print("\nMasukkan username anda : ")
        username = input("")
        if username in daftar_pengguna.index:
            while(masukkan_password):
                print("\nMasukkan Password : ")
                password = input("")
                if password == daftar_pengguna.loc[username, 'password']:
                    print(f'Anda masuk sebagai {username}')
                    print(daftar_pengguna.loc[username, 'role'])
                    if daftar_pengguna.loc[username, 'role'] == "Penjual":
                        penjual()
                    masukkan_password = False
                else :
                    print('\n|  Password yang anda masukkan salah!\n| Silahkan coba kembali...')
        else :
            print('\n|  Maaf, username tidak dikenali\n|    Silahkan coba kembali...')
        if masukkan_password == False:
            break

def registrasi():
    header('SIGN IN')
    df = pd.read_csv('DaftarPengguna.csv')
    daftar_pengguna = df.set_index("username")

    while(True):
        username = input("\nMasukkan username : ")
        if username in daftar_pengguna.index:
            print('Maaf, username sudah ada!!!\nSilahkan masukkan username lain')
        else:
            password = input("\nMasukkan Password : ")
            print("Anda bisa memilih peran yang akan dijalankan\n[1]Pembeli\n[2]Penjual")
            while(True):
                role = input("Masukkan peran : ")
                if role == '1' :
                    role = 'Pembeli'
                    break
                elif role == '2' :
                    role = 'Penjual'
                    break
                else :
                    print('Tolong masukkan 1 atau 2')
            data_baru = {'username' : username, 'password' : password, 'role' : role}
            data_baru = pd.DataFrame([data_baru])  # Ubah data baru menjadi DataFrame
            daftar_pengguna = pd.concat([daftar_pengguna.reset_index(), data_baru], ignore_index=True)
            daftar_pengguna.to_csv('DaftarPengguna.csv', index=False)
            print(f'Anda masuk sebagai {username}')
            break

def logout():
    header('LOG OUT')
    kalimat = "Terimakasih sudah menggunakan layanan kami!"
    width = (67-len(kalimat))//2
    print('\n'+" "*width+kalimat+" "*width+'\n\n'+'='*67)
header('',1)


