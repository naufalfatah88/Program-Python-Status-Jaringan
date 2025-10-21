# Program-Python-Status-Jaringan 🚀

Selamat datang di repositori Program Python Status Jaringan! Repositori ini berisi kumpulan alat jaringan berbasis Python yang dirancang untuk memberikan wawasan mendalam tentang konektivitas dan status jaringan Anda, langsung dari terminal.

Setiap alat dibuat untuk menjadi alternatif yang lebih visual, cepat, dan informatif dibandingkan utilitas baris perintah standar.

## ✨ Fitur Utama

*   **Dasbor Jaringan Live:** Pantau konektivitas ke beberapa target secara bersamaan dengan dasbor TUI yang terus diperbarui.
*   **Visualisasi Data:** Manfaatkan output berwarna, tabel yang rapi, dan grafik bar ASCII untuk memahami data jaringan secara sekilas.
*   **Informasi Geolokasi (GeoIP):** Lacak lokasi fisik alamat IP untuk melihat perjalanan data Anda di seluruh dunia.
*   **Kinerja Tinggi:** Dapatkan hasil lebih cepat dengan teknik seperti *probing* paralel dan *lookup* asinkron.
*   **Alat DNS Interaktif:** Lakukan berbagai jenis kueri DNS dengan mudah melalui menu yang ramah pengguna.

---

## 🛠️ Proyek yang Termasuk

Berikut adalah penjelasan untuk setiap alat di dalam repositori ini:

### 1. NetPulse.py

Sebuah dasbor pemantau jaringan canggih yang mampu melacak beberapa target secara bersamaan. NetPulse mengubah data `ping` menjadi dasbor visual yang menampilkan status, latensi, statistik, grafik bar, dan informasi geolokasi secara *real-time*.

*   **Fitur:** Multi-target, grafik bar latensi, info GeoIP, statistik (Jitter, Loss), notifikasi suara.

### 2. TracePulse.py

Alat `traceroute` yang dioptimalkan untuk kecepatan dan visualisasi. Ia memetakan rute paket Anda melintasi internet, menampilkan setiap hop secara *real-time* lengkap dengan informasi geolokasi untuk setiap alamat IP.

*   **Fitur:** Penemuan hop paralel, *timeout* agresif, *lookup* GeoIP di latar belakang, dasbor yang diperbarui secara live.
*   **Catatan:** Membutuhkan hak akses `sudo` di Linux/macOS untuk kinerja optimal.

### 3. DnsQueryTools.py

Sebuah alat `nslookup` sederhana dengan menu interaktif. Program ini memandu pengguna untuk memasukkan domain dan memilih jenis *record* (Alamat IP, Server Email, atau Server Nama) yang ingin dicari. Dibuat khusus untuk kompatibilitas maksimum dengan versi library yang lebih lama.

*   **Fitur:** Menu interaktif, fokus pada tiga *record* utama (A, MX, NS), sangat mudah digunakan.

### 4. Netcheck.py

Sebuah monitor ping *live* yang sederhana untuk satu target. Alat ini terus-menerus mengirim ping ke host yang ditentukan dan menampilkan status setiap balasan dengan kode warna untuk menunjukkan koneksi yang stabil (hijau), lambat (kuning), atau gagal (merah).

*   **Fitur:** Pemantauan berkelanjutan, visualisasi status berwarna, statistik real-time, ringkasan akhir.

---

## 🚀 Memulai

### Prasyarat

*   **Python 3.6+**
*   **pip** (Package installer for Python)

### Instalasi Dependensi

Semua proyek ini memerlukan beberapa library eksternal. Anda dapat menginstal semuanya dengan satu perintah. Buka terminal Anda dan jalankan:

```bash
pip3 install requests colorama dnspython
```

### Cara Menjalankan

Setiap alat dijalankan dari terminal. Pastikan Anda berada di direktori proyek.

1.  **NetPulse.py**
    ```bash
    # Program akan meminta Anda memasukkan target
    # Anda bisa memasukkan satu atau lebih target, dipisahkan koma
    python3 NetPulse.py
    ```

2.  **TracePulse.py**
    > **Penting:** Di Linux dan macOS, gunakan `sudo` untuk hasil terbaik.
    ```bash
    # Program akan meminta Anda memasukkan target
    sudo python3 TracePulse.py
    ```

3.  **DnsQueryTools.py**
    ```bash
    # Cukup jalankan file-nya dan ikuti menu interaktif yang muncul
    python3 DnsQueryTools.py
    ```

4.  **Netcheck.py**
    ```bash
    # Program akan meminta Anda memasukkan target yang ingin dipantau
    python3 Netcheck.py
    ```

---

## 🤝 Kontribusi

Merasa ada yang bisa ditingkatkan? Silakan buat *Fork* repositori ini, lakukan perubahan Anda, dan kirimkan *Pull Request*. Kontribusi dalam bentuk apa pun sangat dihargai!
