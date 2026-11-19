> **STATUS: TUGAS KULIAH / PRACTICE.** Ini deteksi wajah palsu memakai One-Class SVM, bukan deteksi phishing URL. Sengaja tidak dimasukkan ke rangkuman [`phishing-detection`](https://github.com/hayyanjpg/phishing-detection).

# Face Anti-Spoofing Demo (Client-Specific Anomaly Detection)
Disusun Oleh: Kelompok 8

Project ini adalah implementasi sistem keamanan biometrik wajah untuk mendeteksi serangan spoofing (pemalsuan wajah). Sistem ini dikembangkan sebagai Tugas Besar, mengacu pada pendekatan "Client-Specific Anomaly Detection" (berdasarkan studi literatur Paper 3).

Sistem bekerja dengan metode One-Class Learning, di mana model hanya mempelajari wajah asli pengguna. Segala input yang tidak sesuai dengan karakteristik wajah asli (seperti foto cetak, video replay, atau wajah orang lain) akan dianggap sebagai anomali dan akses akan ditolak.

FITUR UTAMA:
1. Registrasi Wajah Real-time: Mengambil sampel wajah pengguna secara langsung melalui webcam.
2. One-Class SVM Learning: Model dilatih hanya menggunakan data wajah asli, tanpa memerlukan dataset serangan (spoof).
3. Anomaly Detection: Otomatis memblokir akses jika fitur wajah terdeteksi menyimpang dari data registrasi.

------------------------------------------------------
PERSYARATAN SISTEM (PREREQUISITES)
-------------------------------------------------------
Pastikan Python sudah terinstall di komputer Anda. Project ini membutuhkan library berikut:
- opencv-python
- numpy
- face_recognition
- scikit-learn

Catatan Instalasi: Library 'face_recognition' memerlukan CMake dan C++ Compiler. Jika menggunakan Windows, pastikan 'Desktop development with C++' sudah terinstall via Visual Studio Installer.

-------------------------------------------------------
CARA INSTALASI
-------------------------------------------------------
1. Clone repository ini ke komputer Anda:
   git clone https://github.com/hayyanjpg/anti_spoofing.git

2. Masuk ke folder project:
   cd anti_spoofing

3. Install library yang dibutuhkan:
   pip install opencv-python numpy face_recognition scikit-learn

-------------------------------------------------------
PANDUAN MENJALANKAN DEMO
-------------------------------------------------------
Untuk memulai program, jalankan perintah berikut di terminal:
python main.py

Sistem memiliki 3 status operasional: IDLE, REGISTER, dan DETECT.

TAHAP 1: REGISTRASI WAJAH (IDLE -> REGISTER)
1. Pastikan wajah pengguna terlihat jelas di kamera.
2. Tekan tombol 'r' pada keyboard untuk memulai pengambilan sampel.
3. PENTING: Saat proses pengambilan sampel (sekitar 50 foto), gerakkan kepala sedikit (oleh ke kiri/kanan, ubah ekspresi senyum/datar, majukan/mundurkan kepala sedikit). Hal ini agar model mengenali variasi wajah Anda dan tidak kaku (overfitting).
4. Tunggu hingga proses training selesai dan sistem masuk ke mode DETECT.

TAHAP 2: PENGUJIAN (DETECT)
Setelah training selesai, sistem akan mendeteksi wajah secara real-time.

- Skenario A (Wajah Asli):
  Arahkan wajah asli ke kamera. Sistem seharusnya menampilkan kotak HIJAU dengan status "REAL USER".

- Skenario B (Serangan Spoofing):
  Gunakan HP Anda, cari foto wajah Anda, lalu arahkan layar HP ke depan kamera laptop. Sistem seharusnya menampilkan kotak MERAH dengan status "SPOOF / BLOCKED" karena mendeteksi anomali pada tekstur/depth.

TAHAP 3: RESET (GANTI PENGGUNA)
Jika ingin mendemokan dengan orang yang berbeda:
1. Tekan tombol 'c' pada keyboard.
2. Program akan menghapus model pengguna sebelumnya dan menutup aplikasi.
3. Jalankan ulang program untuk mendaftarkan pengguna baru.

-------------------------------------------------------
PENGATURAN SENSITIVITAS (TUNING)
-------------------------------------------------------
Jika hasil deteksi kurang akurat, Anda dapat mengubah parameter di bagian atas file 'main.py':

- SAMPLE_SIZE = 50
  Jumlah foto yang diambil saat registrasi. Semakin banyak semakin akurat, namun proses registrasi lebih lama.

- NU_PARAM = 0.01
  Tingkat toleransi error.
  * Ubah ke 0.05 jika foto spoof (HP) sering lolos (sistem kurang ketat).
  * Ubah ke 0.01 atau lebih kecil jika wajah asli sering terblokir (sistem terlalu ketat).

-------------------------------------------------------
REFERENSI JURNAL
-------------------------------------------------------
Program ini dibangun berdasarkan analisis dari jurnal:
1. A hierarchical multi-modal cross-attention model for face anti-spoofing
2. Antispoofing in face biometrics: a comprehensive study
3. Client-Specific Anomaly Detection for Face Presentation Attack Detection
