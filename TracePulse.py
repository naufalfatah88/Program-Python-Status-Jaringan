import os
import platform
import subprocess
import re
import requests
import socket
from colorama import Fore, Style, init
from typing import Union, Dict, Any

# Inisialisasi Colorama
init(autoreset=True)

def clear_screen():
    """Membersihkan layar terminal."""
    os.system("cls" if platform.system() == "Windows" else "clear")

def get_geolocation(ip: str, cache: Dict[str, str]) -> str:
    """Mendapatkan info geolokasi dari ip-api.com dan menggunakan cache."""
    if ip in cache:
        return cache[ip]
    if ip.startswith(('192.168.', '10.', '172.')) or ip == "127.0.0.1":
        return "Jaringan Lokal (Private)"
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}?fields=status,city,country,org", timeout=3)
        response.raise_for_status()
        data = response.json()
        if data.get('status') == 'success':
            geo_info = f"{data.get('city', '')}, {data.get('country', '')} - {data.get('org', '')}"
            cache[ip] = geo_info
            return geo_info
        else:
            return "Informasi Lokasi Tidak Ditemukan"
    except requests.RequestException:
        return "Gagal Menghubungi API GeoIP"

def parse_traceroute_line(line: str) -> Union[Dict[str, Any], None]:
    """
    Mem-parsing satu baris output dari traceroute/tracert dengan regex yang lebih baik.
    """
    # Regex yang lebih spesifik untuk mencari alamat IP (X.X.X.X)
    ip_pattern = r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
    
    # Mencari hop dan IP terlebih dahulu
    hop_ip_match = re.search(r'^\s*(\d+)\s+.*?(' + ip_pattern + r')', line)
    if hop_ip_match:
        hop = hop_ip_match.group(1)
        ip = hop_ip_match.group(2)
        
        # Mencari latensi secara terpisah
        latency_match = re.search(r'(\d+\.\d+)\s+ms', line)
        latency = float(latency_match.group(1)) if latency_match else None
        
        return {"hop": hop, "ip": ip, "latency": latency}

    # Regex untuk timeout (jika tidak ada IP yang ditemukan)
    timeout_match = re.search(r'^\s*(\d+)\s+([*]\s+)+', line)
    if timeout_match:
        return {"hop": timeout_match.group(1), "ip": None, "latency": None}
        
    return None

def run_visual_traceroute(target: str):
    """Fungsi utama untuk menjalankan traceroute dan menampilkan hasilnya secara visual."""
    
    system = platform.system().lower()
    command = ["tracert", "-d", target] if system == "windows" else ["traceroute", target]
    
    clear_screen()
    print(f"{Style.BRIGHT}🚀 TracePulse - Visual Traceroute 🚀{Style.RESET_ALL}")
    try:
        target_ip = socket.gethostbyname(target)
        print(f"Melacak rute ke {Fore.CYAN}{target}{Style.RESET_ALL} [{Fore.CYAN}{target_ip}{Style.RESET_ALL}]\n")
    except socket.gaierror:
        print(f"{Fore.RED}Error: Tidak dapat menemukan host {target}.")
        return

    print(f"{'Hop':<5} {'Alamat IP':<18} {'Latensi':<10} {'Lokasi & Organisasi'}")
    print("─" * 80)

    geo_cache = {}
    
    try:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)

        for line in iter(process.stdout.readline, ''):
            parsed_data = parse_traceroute_line(line.strip())
            
            if parsed_data:
                hop = parsed_data['hop']
                ip = parsed_data['ip']
                latency = parsed_data['latency']

                if ip:
                    latency_str = f"{latency:.1f} ms" if latency else "N/A"
                    geo_info = get_geolocation(ip, geo_cache)
                    print(f"{hop:<5} {Fore.CYAN}{ip:<18}{Style.RESET_ALL} {Fore.GREEN}{latency_str:<10}{Style.RESET_ALL} {Fore.MAGENTA}{geo_info}{Style.RESET_ALL}")
                else:
                    print(f"{hop:<5} {Fore.YELLOW}{'* * *':<18}{Style.RESET_ALL} {'Request timed out.':<10}")

        process.stdout.close()
        process.wait()

    except FileNotFoundError:
        print(f"\n{Fore.RED}Error: Perintah '{command[0]}' tidak ditemukan di sistem Anda.")
    except Exception as e:
        print(f"\n{Fore.RED}Terjadi kesalahan: {e}")

    print("\n" + "─" * 80)
    print(f"{Style.BRIGHT}Pelacakan selesai.{Style.RESET_ALL}")

if __name__ == "__main__":
    import socket
    clear_screen()
    target_host = input("Masukkan domain atau Alamat IP untuk dilacak (misal: google.com atau 8.8.8.8): ").strip()
    
    if target_host:
        run_visual_traceroute(target_host)
    else:
        print("Error: Input tidak boleh kosong.")
