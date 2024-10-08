### TikTokPy Downloader

**TikTokPy Downloader** adalah aplikasi web yang memungkinkan pengguna untuk dengan mudah mengunduh video dan audio dari TikTok. Aplikasi ini menggunakan Flask sebagai backend dan mengintegrasikan dengan API eksternal untuk mengambil detail video.

## Fitur

- Masukkan URL TikTok untuk mendapatkan video dan audio.
- Menampilkan thumbnail, judul video, dan opsi untuk mengunduh video dan audio.
- Antarmuka pengguna yang responsif dan modern menggunakan Tailwind CSS.

## Teknologi yang Digunakan

- **Flask**: Kerangka kerja web untuk Python.
- **HTML, CSS, JavaScript**: Untuk tampilan depan.
- **jQuery**: Untuk interaksi AJAX dan DOM.
- **SweetAlert2**: Untuk menampilkan notifikasi dan modal.

## Instalasi

1. Kloning repositori ini:

   ```bash
   git clone https://github.com/BOTCAHX/TikTokPy.git
   cd TikTokPy
   ```

2. Buat dan aktifkan virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # di Linux/Mac
   .\venv\Scripts\activate   # di Windows
   ```

3. Instal dependensi:

   ```bash
   pip install -r requirements.txt
   ```

4. Jalankan aplikasi:

   ```bash
   python3 app.py
   ```

5. Buka browser Anda dan akses `http://127.0.0.1:5000`.
   
## Membangun Gambar Docker
```
docker build -t flask-app .
```
## Menjalankan Kontainer Docker
```
docker run -p 5000:5000 flask-app
```
## Cara Menggunakan

1. Masukkan URL video TikTok di kolom yang disediakan.
2. Klik tombol "Download".
3. Tunggu hingga data diambil, dan Anda akan melihat thumbnail serta opsi untuk mengunduh video dan audio.

## Kontribusi

Silakan fork repositori ini dan kirim pull request jika Anda memiliki saran atau perbaikan.

## Lisensi

MIT
