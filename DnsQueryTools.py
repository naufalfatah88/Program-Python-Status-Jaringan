import dns.resolver

# Di versi dnspython yang lama, error (exception) diimpor dari dns.resolver
# Ini adalah perubahan kunci untuk memastikan kompatibilitas.
from dns.resolver import NXDOMAIN, NoAnswer, Timeout, NoNameservers

def get_a_records(domain):
    """Fungsi untuk mencari Alamat IP (A Record)."""
    print(f"\n--- Mencari Alamat IP (A) untuk {domain} ---")
    try:
        # PENTING: Menggunakan .query() bukan .resolve() untuk kompatibilitas mundur.
        answers = dns.resolver.query(domain, 'A')
        for record in answers:
            print(f"  -> Ditemukan IP: {record.to_text()}")
            
    except NXDOMAIN:
        print(f"  [Error] Domain '{domain}' tidak ditemukan.")
    except NoAnswer:
        print(f"  [Info] Domain '{domain}' ada, tetapi tidak memiliki A record.")
    except (Timeout, NoNameservers) as e:
        print(f"  [Error] Gagal menghubungi server DNS: {e}")
    except Exception as e:
        print(f"  [Error] Terjadi kesalahan tak terduga: {e}")


def get_mx_records(domain):
    """Fungsi untuk mencari Server Email (MX Record)."""
    print(f"\n--- Mencari Server Email (MX) untuk {domain} ---")
    try:
        # PENTING: Menggunakan .query()
        answers = dns.resolver.query(domain, 'MX')
        for record in answers:
            # MX record punya format khusus: (preference, mail_server)
            print(f"  -> Prioritas: {record.preference:<5} Server: {record.exchange}")
            
    except NXDOMAIN:
        print(f"  [Error] Domain '{domain}' tidak ditemukan.")
    except NoAnswer:
        print(f"  [Info] Domain '{domain}' ada, tetapi tidak memiliki MX record.")
    except (Timeout, NoNameservers) as e:
        print(f"  [Error] Gagal menghubungi server DNS: {e}")
    except Exception as e:
        print(f"  [Error] Terjadi kesalahan tak terduga: {e}")


def get_ns_records(domain):
    """Fungsi untuk mencari Server Nama (NS Record)."""
    print(f"\n--- Mencari Server Nama (NS) untuk {domain} ---")
    try:
        # PENTING: Menggunakan .query()
        answers = dns.resolver.query(domain, 'NS')
        for record in answers:
            print(f"  -> Ditemukan Server Nama: {record.to_text()}")
            
    except NXDOMAIN:
        print(f"  [Error] Domain '{domain}' tidak ditemukan.")
    except NoAnswer:
        print(f"  [Info] Domain '{domain}' ada, tetapi tidak memiliki NS record.")
    except (Timeout, NoNameservers) as e:
        print(f"  [Error] Gagal menghubungi server DNS: {e}")
    except Exception as e:
        print(f"  [Error] Terjadi kesalahan tak terduga: {e}")


# --- Program Utama Dimulai Di Sini ---
def main_menu():
    """Menampilkan menu utama dan mengatur alur program."""
    
    while True:
        print("\n" + "="*40)
        print("    Selamat Datang di DNS Lookup Tool")
        print("="*40)
        
        domain = input("Masukkan nama domain (atau 'exit' untuk keluar): ").strip().lower()
        
        if domain == 'exit' or domain == 'q':
            break
        
        if not domain: # Jika pengguna hanya menekan Enter
            continue

        print("\nApa yang ingin Anda cari?")
        print("  1. Alamat IP (A Record)")
        print("  2. Server Email (MX Record)")
        print("  3. Server Nama (NS Record)")
        
        choice = input("Masukkan pilihan Anda (1, 2, atau 3): ").strip()
        
        if choice == '1':
            get_a_records(domain)
        elif choice == '2':
            get_mx_records(domain)
        elif choice == '3':
            get_ns_records(domain)
        else:
            print("\n[Error] Pilihan tidak valid. Harap masukkan angka 1, 2, atau 3.")

    print("\nTerima kasih! Sampai jumpa lagi.")


# Menjalankan fungsi menu utama saat script dieksekusi
if __name__ == "__main__":
    main_menu()
