import cv2
import numpy as np
import face_recognition
from sklearn.svm import OneClassSVM
import pickle
import os

MODEL_FILE = "user_model.pkl"
FRAME_RESIZE = 0.25  # Perkecil frame agar proses cepat (0.25 = 1/4 ukuran asli)
SAMPLE_SIZE = 50     # Jumlah foto wajah yang diambil saat registrasi
NU_PARAM = 0.01      # Sensitivitas Anomali (0.01 - 0.1). Semakin kecil semakin ketat
GAMMA_PARAM = 0.001  

def save_model(clf, frame_embeddings):
    """Menyimpan model SVM dan data referensi ke file"""
    with open(MODEL_FILE, 'wb') as f:
        pickle.dump({'model': clf, 'ref_data': frame_embeddings}, f)
    print(f"[INFO] Model berhasil disimpan ke {MODEL_FILE}")
def load_model():
    """Memuat model jika ada"""
    if not os.path.exists(MODEL_FILE):
        return None
    with open(MODEL_FILE, 'rb') as f:
        data = pickle.load(f)
    return data

def main():
    cap = cv2.VideoCapture(0) # 0 untuk webcam default
    
    # Cek model user sudah ada atau blm, jika sudah ada dan ingin muka lain, hapus model yg sudah ada 
    model_data = load_model()
    if model_data:
        clf = model_data['model']
        print("[INFO] Model User ditemukan. Masuk ke Mode DETEKSI.")
        mode = "DETECT"
    else:
        print("[INFO] Model tidak ditemukan. Masuk ke Mode REGISTRASI.")
        print("[INFO] Tekan 'r' untuk mulai merekam wajah asli.")
        mode = "IDLE"

    collected_embeddings = []

    while True:
        ret, frame = cap.read()
        if not ret: break

        # Resize frame untuk mempercepat pemrosesan face_recognition
        small_frame = cv2.resize(frame, (0, 0), fx=FRAME_RESIZE, fy=FRAME_RESIZE)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        # Deteksi wajah & Encode (Ekstrak Fitur 128-dimensi)
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        # --- LOGIKA REGISTRASI ---
        if mode == "REGISTER":
            cv2.putText(frame, f"Mengambil Sampel: {len(collected_embeddings)}/{SAMPLE_SIZE}", (10, 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
            
            if len(face_encodings) > 0:
                # Ambil encoding wajah pertama yang terdeteksi
                collected_embeddings.append(face_encodings[0])
            
            if len(collected_embeddings) >= SAMPLE_SIZE:
                print("[INFO] Sampel cukup. Melatih model One-Class SVM...")
                
                # TRAIN ONE-CLASS SVM (Implementasi Paper 3)
                # kernel='rbf' memetakan data ke dimensi tinggi untuk mencari boundary non-linear
                clf = OneClassSVM(kernel='rbf', gamma=GAMMA_PARAM, nu=NU_PARAM)
                X = np.array(collected_embeddings)
                clf.fit(X)
                
                save_model(clf, collected_embeddings)
                mode = "DETECT"
                print("[INFO] Training selesai. Beralih ke Mode DETEKSI.")

        # --- LOGIKA DETEKSI (ANTI-SPOOFING) ---
        elif mode == "DETECT":
            if len(face_encodings) > 0:
                # Prediksi menggunakan SVM
                # Output 1 = Asli (Inliers), Output -1 = Palsu/Anomali (Outliers)
                prediction = clf.predict([face_encodings[0]])
                score = clf.decision_function([face_encodings[0]]) # Jarak ke boundary

                # Ambil koordinat wajah untuk visualisasi
                top, right, bottom, left = face_locations[0]
                # Scale balik ke ukuran asli
                top *= 4; right *= 4; bottom *= 4; left *= 4

                if prediction[0] == 1:
                    label = "REAL USER (ACCESS GRANTED)"
                    color = (0, 255, 0) # Hijau
                else:
                    label = f"SPOOF / UNKNOWN (BLOCKED)"
                    color = (0, 0, 255) # Merah
                
                # Tampilkan kotak dan label nya
                cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
                cv2.putText(frame, label, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
                cv2.putText(frame, f"Score: {score[0]:.2f}", (left, bottom + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1)

        #buat UI display perintah 
        elif mode == "IDLE":
             cv2.putText(frame, "Tekan 'r' untuk Registrasi Wajah Asli", (10, 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

        cv2.imshow('Anti-Spoofing Demo (One-Class SVM)', frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('r') and mode == "IDLE":
            mode = "REGISTER"
        elif key == ord('c'): # Clear model untuk demo ulang
            if os.path.exists(MODEL_FILE):
                os.remove(MODEL_FILE)
                print("[INFO] Model dihapus. Restart program untuk registrasi ulang.")
                break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
