import psutil

def tampilkan_status_jaringan():
    """
    Fungsi ini akan menampilkan semua network interface yang ada
    di komputer beserta alamat dan statusnya (aktif/tidak).
    """
    try:
        # Mengambil statistik dari semua network interface
        stats = psutil.net_if_stats()
        # Mengambil alamat dari semua network interface
        addrs = psutil.net_if_addrs()

        print("=============================================")
        print("    STATUS KONEKSI JARINGAN DI KOMPUTER ANDA   ")
        print("=============================================")

        # Looping melalui setiap interface yang terdeteksi
        for interface, info in stats.items():
            print(f"\nNama Interface: {interface}")
            
            # Cek status interface (up/down)
            status = "Aktif (Up)" if info.isup else "Tidak Aktif (Down)"
            print(f"  -> Status      : {status}")

            # Cek alamat IP jika ada
            if interface in addrs:
                for addr in addrs[interface]:
                    # Menampilkan alamat IPv4
                    if addr.family == psutil.AF_LINK:
                        print(f"  -> MAC Address : {addr.address}")
                    elif addr.family == 2: # AF_INET (IPv4)
                        print(f"  -> IPv4 Address: {addr.address}")

        print("\n=============================================")
        print("Gunakan informasi di atas untuk menonaktifkan")
        print("koneksi yang tidak perlu melalui Control Panel.")

    except Exception as e:
        print(f"Terjadi kesalahan saat mengambil data jaringan: {e}")

if __name__ == "__main__":
    tampilkan_status_jaringan()
