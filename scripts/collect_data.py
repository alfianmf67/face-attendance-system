# scripts/collect_data.py
import streamlit as st
import cv2
import os
from datetime import datetime

# Direktori
RAW_DIR = "data/raw"
os.makedirs(RAW_DIR, exist_ok=True)

# Metadata file
CSV_PATH = os.path.join(RAW_DIR, "participants.csv")
if not os.path.exists(CSV_PATH):
    with open(CSV_PATH, "w") as f:
        f.write("id,nama,alamat,tanggal_daftar,waktu_daftar,usia,catatan\n")

st.set_page_config(page_title="Pendaftaran Peserta - Majelis Ta'lim", layout="centered")
st.title("🕌 Pendaftaran Wajah Peserta")
st.markdown("Ambil 3 foto: **Depan**, **Kiri 30 derajat**, **Kanan 30 derajat**")

# Form input
with st.form("form_peserta"):
    nama = st.text_input("Nama Lengkap", value="Ahmad Fauzi")
    alamat = st.text_input("Alamat", value="Jl. Parung Serab No. 12")
    usia = st.number_input("Usia", min_value=19, max_value=60, value=24)
    catatan = st.selectbox("Kategori", ["pra-nikah", "nikah", "pengurus"])
    submit_meta = st.form_submit_button("💾 Simpan Data & Mulai Rekam")
    st.markdown("setiap setelah ambil foto klik tombol simpan & mulai rekam")

if submit_meta:
    # Generate ID unik: ID + 3-digit (misal ID001)
    existing_ids = []
    if os.path.exists(CSV_PATH):
        with open(CSV_PATH) as f:
            lines = f.readlines()
            if len(lines) > 1:
                last_id = lines[-1].split(",")[0]
                if last_id.startswith("ID") and len(last_id) == 5:
                    num = int(last_id[2:]) + 1
                else:
                    num = 1
            else:
                num = 1
    else:
        num = 1
    peserta_id = f"ID{num:03d}"
    
    # Buat folder
    folder = os.path.join(RAW_DIR, f"{peserta_id}_{nama.replace(' ', '')}")
    os.makedirs(folder, exist_ok=True)
    
    # Simpan metadata
    now = datetime.now()
    with open(CSV_PATH, "a") as f:
        f.write(f"{peserta_id},{nama},{alamat},{now.strftime('%Y-%m-%d')},{now.strftime('%H:%M:%S')},{usia},{catatan}\n")
    
    st.session_state.peserta_id = peserta_id
    st.session_state.nama = nama
    st.session_state.folder = folder
    st.success(f"✅ Data disimpan. ID: {peserta_id}. Lanjutkan pengambilan gambar!")

# Jika metadata sudah disimpan → tampilkan kamera
if 'peserta_id' in st.session_state:
    st.subheader(f"📷 Rekam Wajah - {st.session_state.nama} ({st.session_state.peserta_id})")
    
    pose_list = ["1_front", "2_left", "3_right"]
    pose_idx = st.radio("Pilih pose", pose_list, horizontal=True)
    
    # Akses kamera
    cam = st.camera_input("Ambil foto", key=pose_idx)
    
    if cam:
        # Simpan file
        file_path = os.path.join(st.session_state.folder, f"{pose_idx}.jpg")
        with open(file_path, "wb") as f:
            f.write(cam.getbuffer())
        st.success(f"✅ {pose_idx.replace('_', ' ')} tersimpan!")
        st.image(file_path, width=300)