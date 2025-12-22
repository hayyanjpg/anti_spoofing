# Face Anti-Spoofing Demo (Client-Specific Anomaly Detection)

Project ini adalah implementasi sistem deteksi *Face Spoofing* (anti-pemalsuan wajah) untuk Tugas Besar Mata Kuliah [Nama Matkul]. 

Sistem ini menggunakan pendekatan **Client-Specific Anomaly Detection** (mengacu pada Paper 3 review jurnal), di mana model hanya dilatih menggunakan wajah asli pengguna (*One-Class SVM*). Wajah yang tidak sesuai dengan pola data asli (seperti foto cetak, video replay, atau wajah orang lain) akan dianggap sebagai anomali dan diblokir.

## 📋 Fitur Utama
- **Registrasi Wajah Real-time:** Mengambil sampel wajah pengguna secara langsung.
- **One-Class Learning:** Tidak membutuhkan data serangan (*spoof*) saat training, hanya data asli.
- **Liveness/Anomaly Check:** Memblokir akses jika fitur wajah terdeteksi sebagai anomali (jarak fitur terlalu jauh dari data asli).

## 🛠️ Persiapan (Installation)

Pastikan Python sudah terinstall di laptop.

1. **Clone Repository ini**
   ```bash
   git clone [https://github.com/hayyanjpg/anti_spoofing.git](https://github.com/hayyanjpg/anti_spoofing.git)
   cd anti_spoofing
Install Library yang Dibutuhkan Project ini membutuhkan opencv, face_recognition, dan scikit-learn.

(Catatan: Library face_recognition membutuhkan CMake. Jika gagal install di Windows, pastikan "C++ development with Visual Studio" sudah terinstall).

Jalankan perintah ini di terminal:

Bash

pip install opencv-python numpy face_recognition scikit-learn
🚀 Cara Menjalankan Demo
Jalankan script utama (pastikan nama file python-nya sesuai, misal main.py):

Bash

python main.py
Langkah-Langkah Demo (Skenario Presentasi)
Sistem memiliki 3 Mode: IDLE, REGISTER, dan DETECT.

1. Tahap Registrasi (Mode IDLE -> REGISTER)
Saat program pertama kali jalan (atau setelah reset), statusnya adalah IDLE.

Pastikan wajah user (Dosen/Teman) terlihat di kamera.

Tekan tombol r pada keyboard untuk mulai merekam wajah asli.

PENTING: Saat proses pengambilan 50 sampel, gerak-gerakkan kepala sedikit (kiri, kanan, senyum, ubah ekspresi, maju-mundur sedikit) agar model mengenali variasi wajahmu.

Tunggu hingga proses Training One-Class SVM selesai (muncul pesan di terminal).

2. Tahap Pengujian (Mode DETECT)
Setelah training selesai, sistem otomatis masuk mode deteksi.

Skenario A: Akses Diterima (Wajah Asli)

Arahkan wajah asli ke kamera.

Hasil: Kotak Hijau bertuliskan "REAL USER".

Skenario B: Serangan Spoofing (Foto HP)

Ambil HP, cari foto wajahmu, lalu arahkan layar HP ke kamera laptop.

Hasil: Kotak Merah bertuliskan "SPOOF / BLOCKED".

Penjelasan: Model SVM mendeteksi bahwa tekstur/fitur dari layar HP berbeda (anomali) dibandingkan sampel wajah asli.

3. Reset Model (Ganti Orang)
Jika ingin mencoba dengan orang lain:

Tekan tombol c (Clear).

Program akan menghapus model lama dan keluar.

Jalankan ulang program untuk registrasi orang baru.

⚙️ Konfigurasi (Tuning)
Jika hasil deteksi terlalu sensitif (wajah asli sering diblokir) atau terlalu longgar (foto spoof tembus), ubah parameter di bagian atas file python:

Python

SAMPLE_SIZE = 50   # Jumlah foto saat registrasi (Makin banyak makin akurat)
NU_PARAM = 0.01    # Sensitivitas Anomali. 
                   # Naikkan (0.05) jika spoof sering tembus. 
                   # Turunkan (0.01) jika wajah asli sering keblokir.
GAMMA_PARAM = 'scale' # Biarkan 'scale' agar adaptif.
📚 Referensi
Code ini dibuat berdasarkan review jurnal:

A hierarchical multi-modal cross-attention model for face anti-spoofing

Antispoofing in face biometrics: a comprehensive study

Client-Specific Anomaly Detection for Face Presentation Attack Detection
