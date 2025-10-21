import os
import platform
import subprocess
import time
import requests
import socket
import statistics
from collections import deque
from colorama import Fore, Style, init
from typing import Union # <<< PERUBAHAN 1: Tambahkan impor ini

# Inisialisasi Colorama agar warna berfungsi cross-platform
init(autoreset=True)

# --- Konfigurasi Dasbor ---
HISTORY_SIZE = 40      # Jumlah data untuk bar chart
BAR_CHART_HEIGHT = 8   # Tinggi bar chart dalam baris
CRITICAL_LATENCY = 300 # Latensi di atas ini dianggap kritis (merah)
WARNING_LATENCY = 150  # Latensi di atas ini dianggap lambat (kuning)

def clear_screen():
    """Membersihkan layar terminal."""
    os.system("cls" if platform.system() == "Windows" else "clear")

def get_local_ip_hostname():
    """Mendapatkan IP lokal dan hostname mesin."""
    try:
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        return hostname, ip_address
    except socket.gaierror:
        return "N/A", "N/A"

def get_geolocation(ip, cache):
    """Mendapatkan info geolokasi dari ip-api.com dan menyimpannya di cache."""
    if ip in cache:
        return cache[ip]
    if not ip or ip.startswith(('127.', '192.', '10.')): # Hindari lookup IP lokal
        return "Alamat Lokal"
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}?fields=country,city,org", timeout=2)
        response.raise_for_status()
        data = response.json()
        geo_info = f"{data.get('city', '')}, {data.get('country', '')} ({data.get('org', '')})"
        cache[ip] = geo_info
        return geo_info
    except requests.RequestException:
        return "Info Geo Tidak Tersedia"

# vvv PERUBAHAN 2: Ubah sintaks di baris ini vvv
def get_ping_latency(output: str) -> Union[float, None]:
    """Mengekstrak latensi dari output ping."""
    for line in output.splitlines():
        if "time=" in line.lower() and "ttl=" in line.lower():
            try:
                start = line.lower().find("time=") + 5
                end_ms = line.lower().find("ms")
                if line[start:end_ms].startswith('<'): return 0.5
                return float(line[start:end_ms])
            except (ValueError, IndexError): continue
    return None

def draw_bar_chart(history: deque, height: int):
    """Menggambar bar chart vertikal dari riwayat latensi."""
    if not history: return
    
    max_val = max(max(history), WARNING_LATENCY) # Pastikan skala tidak terlalu kecil
    
    # Membuat grid kosong
    chart = [[' ' for _ in range(len(history))] for _ in range(height)]
    
    # Mengisi grid dengan balok
    for i, val in enumerate(history):
        bar_height = int((val / max_val) * height)
        bar_height = min(bar_height, height) # Batasi tinggi
        color = Fore.GREEN if val < WARNING_LATENCY else Fore.YELLOW if val < CRITICAL_LATENCY else Fore.RED
        
        for j in range(bar_height):
            chart[height - 1 - j][i] = f"{color}█{Style.RESET_ALL}"

    # Mencetak chart baris per baris
    for row in chart:
        print("".join(row))
    
    # Axis Label
    print(f"└{'─' * (len(history) - 1)}┘ {max_val:.0f}ms")


def run_dashboard(targets: list):
    """Fungsi utama yang menjalankan dan me-render dasbor."""
    
    # State untuk setiap target
    target_states = {
        host: {
            'history': deque(maxlen=HISTORY_SIZE),
            'status': "PENDING",
            'ip': None,
            'geo': "Mencari..."
        } for host in targets
    }
    
    geo_cache = {}
    hostname, local_ip = get_local_ip_hostname()
    event_log = deque(maxlen=5)
    
    try:
        while True:
            # --- Fase Pengumpulan Data ---
            for host in targets:
                state = target_states[host]
                param = "-n 1" if platform.system().lower() == "windows" else "-c 1"
                command = f"ping {param} {host}"
                
                try:
                    output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True, timeout=3)
                    latency = get_ping_latency(output)

                    if state['ip'] is None:
                        # Dapatkan IP dari output ping (lebih andal)
                        ip_start = output.find('[') + 1
                        ip_end = output.find(']')
                        if ip_start > 0 and ip_end > ip_start:
                             state['ip'] = output[ip_start:ip_end]
                             state['geo'] = get_geolocation(state['ip'], geo_cache)

                    if latency is not None:
                        state['history'].append(latency)
                        state['status'] = f"{Fore.GREEN}ONLINE"
                    else:
                        state['history'].append(CRITICAL_LATENCY * 1.5)
                        state['status'] = f"{Fore.RED}TIMEOUT"
                        print("\a", end="") # Beep sound
                        event_log.append(f"{time.strftime('%H:%M:%S')} - {host} Request Timed Out")

                except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
                    state['history'].append(CRITICAL_LATENCY * 1.5)
                    state['status'] = f"{Fore.RED}OFFLINE"
                    print("\a", end="") # Beep sound
                    event_log.append(f"{time.strftime('%H:%M:%S')} - {host} Tidak Dapat Dijangkau")

            # --- Fase Render Dasbor ---
            clear_screen()
            print(f"{Style.BRIGHT}🚀 NetPulse Terminal Dashboard 🚀{Style.RESET_ALL}")
            print("-" * 60)
            
            # Panel 1: Info Sistem
            print(f"{Style.BRIGHT}🖥️  Sistem Anda{Style.RESET_ALL}")
            print(f"   Hostname: {Fore.CYAN}{hostname}\t{Style.RESET_ALL}IP Lokal: {Fore.CYAN}{local_ip}{Style.RESET_ALL}")
            
            # Panel 2: Ringkasan Target
            print(f"\n{Style.BRIGHT}🎯 Ringkasan Target{Style.RESET_ALL}")
            for host, state in target_states.items():
                last_ping = f"{state['history'][-1]:.1f}ms" if state['history'] and state['status'] == f"{Fore.GREEN}ONLINE" else "N/A"
                print(f"   - {host:<20} | Status: {state['status']:<18} | Latency: {last_ping}")
            
            # Panel 3: Fokus Detail (pada target pertama)
            focus_host = targets[0]
            focus_state = target_states[focus_host]
            print(f"\n{Style.BRIGHT}🔎 Fokus Detail: {focus_host} ({focus_state['ip']}){Style.RESET_ALL}")
            print(f"   Lokasi: {Fore.MAGENTA}{focus_state['geo']}{Style.RESET_ALL}")
            
            if focus_state['history']:
                avg = statistics.mean(focus_state['history'])
                jitter = statistics.stdev(focus_state['history']) if len(focus_state['history']) > 1 else 0
                print(f"   Rata²: {avg:.1f}ms | Jitter: {jitter:.1f}ms")
                draw_bar_chart(focus_state['history'], BAR_CHART_HEIGHT)
            
            # Panel 4: Log Peristiwa
            print(f"\n{Style.BRIGHT}🔔 Log Peristiwa{Style.RESET_ALL}")
            if not event_log: print("   (Tidak ada peristiwa penting)")
            for entry in event_log:
                print(f"   {Fore.YELLOW}{entry}{Style.RESET_ALL}")

            print("\n" + "-" * 60)
            print(f"Tekan {Style.BRIGHT}Ctrl+C{Style.RESET_ALL} untuk keluar.")
            
            time.sleep(1)

    except KeyboardInterrupt:
        print("\n\nDasbor dihentikan. Terima kasih telah menggunakan NetPulse!")
    except Exception as e:
        print(f"\nError Kritis: {e}")

if __name__ == "__main__":
    clear_screen()
    print("Selamat datang di NetPulse Dashboard!")
    print("Anda bisa memonitor beberapa host sekaligus.")
    target_input = input("Masukkan target (pisahkan dengan koma, misal: google.com, 8.8.8.8): ").strip()
    
    if target_input:
        target_list = [host.strip() for host in target_input.split(',')]
        run_dashboard(target_list)
    else:
        print("Error: Input target tidak boleh kosong.")
