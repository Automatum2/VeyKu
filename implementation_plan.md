# 🧭 Rencana Implementasi — VEYKU (Pemilihan Jurusan Kuliah)

## Konsep: Tes Minat Bakat Jurusan Kuliah
Proyek ini telah beralih dari "Kerja vs Kuliah" menjadi **VEYKU**: sebuah platform tes minat dan bakat untuk membantu calon mahasiswa yang bimbang memilih rumpun jurusan kuliah yang tepat.

---

## 1. Konsep Utama & Kategori Jurusan

Sistem akan menanyakan serangkaian pertanyaan berbasis psikologi/minat bakat (mirip dengan tes RIASEC) yang akan memetakan user ke dalam 5 rumpun utama jurusan kuliah:

1. **💻 Teknik & IT** (Ilmu Komputer, Teknik Sipil, Sistem Informasi, dll)
2. **🩺 Sains & Medis** (Kedokteran, Farmasi, Biologi, Kimia, dll)
3. **📈 Bisnis & Manajemen** (Akuntansi, Manajemen, Bisnis Digital, dll)
4. **🎨 Seni & Desain** (DKV, Arsitektur, Seni Rupa, Desain Interior, dll)
5. **🗣️ Sosial & Humaniora** (Psikologi, Ilmu Komunikasi, Hukum, Hubungan Internasional)

> [!IMPORTANT]
> **User Review Required**: Apakah 5 kategori rumpun jurusan ini sudah cukup mewakili, atau Anda ingin menambahkan kategori spesifik lain (misal: Pendidikan/Keguruan, Pertanian)?

---

## 2. Alur Pengguna (User Flow)

1. **🏠 Landing Page (Sesuai Gambar VEYKU)**
   - Header: Survey | Tentang | Contact
   - Headline: "Pilih Jurusan Gak Pake Pusing cek di VEYKU aJa"
   - Tombol CTA utama menuju halaman pendaftaran.
2. **📝 Register / Data Diri**
   - Nama Lengkap, Asal Sekolah, Email, Nomor WA.
3. **❓ Survei Minat Bakat (10 Pertanyaan)**
   - Menampilkan satu per satu pertanyaan (SPA-like).
4. **📊 Halaman Hasil Rekomendasi**
   - Menampilkan persentase kecocokan dengan rumpun jurusan.
   - Rekomendasi 3 jurusan spesifik teratas dari rumpun yang menang.
5. **👨‍💻 Admin Dashboard**
   - Melihat statistik jurusan apa yang paling banyak diminati oleh pendaftar.

---

## 3. Desain UI (Berdasarkan Referensi Gambar VEYKU)

- **Warna Utama**: Biru Veyku (`#3B38F6` atau sesuai logo), Hitam, Putih.
- **Tipografi**: Bersih, modern, font sans-serif untuk body dan font dekoratif (seperti tulisan *Jurusan* dan *Pusing*) pada headline.
- **Style**: Minimalis, clean, dengan lengkungan (border-radius) yang halus di bagian footer/header.

---

## 4. Draf Pertanyaan Survei (Contoh)

Setiap opsi jawaban akan menyumbang +1 poin ke salah satu dari 5 rumpun jurusan.

| # | Pertanyaan |
|---|------------|
| 1 | **Apa aktivitas yang paling kamu nikmati di waktu luang?**<br>A. Mengotak-atik gadget/komputer (Teknik/IT)<br>B. Membaca artikel sains/eksperimen (Medis/Sains)<br>C. Berjualan atau mengatur keuangan (Bisnis)<br>D. Menggambar, memotret, atau bermusik (Seni)<br>E. Mengobrol dan mendengarkan curhat teman (Soshum) |
| 2 | **Pelajaran apa yang paling tidak membosankan buatmu?**<br>A. Matematika / TIK<br>B. Biologi / Kimia<br>C. Ekonomi / Akuntansi<br>D. Seni Budaya / Prakarya<br>E. Sosiologi / Sejarah / Bahasa |
| 3 | **Jika ada masalah di sekolah, peran apa yang kamu ambil?**<br>A. Mencari solusi teknis/sistemnya<br>B. Menganalisis penyebabnya secara logis/faktual<br>C. Mengatur strategi dan pembagian tugas teman<br>D. Membuat poster/media untuk kampanye penyelesaian<br>E. Menjadi penengah (mediator) bagi pihak yang berkonflik |
| *(dst hingga 10 pertanyaan, akan kita lengkapi nanti)* |

> [!NOTE]
> Pertanyaan akan dirancang agar tidak terlalu kaku dan terkesan seperti *personality quiz* yang menyenangkan.

---

## 5. Perubahan Database Schema (Proposed Changes)

Karena proyek berubah, tabel database perlu disesuaikan.

### [MODIFY] `models/respondent.py`
Ubah atribut `nisn`, `jurusan`, `kelas` menjadi `asal_sekolah`, `email`, dan `no_wa`.

### [MODIFY] `models/survey_response.py`
Ubah perhitungan skor yang awalnya `kerja` vs `kuliah` menjadi 5 skor: `skor_teknik`, `skor_medis`, `skor_bisnis`, `skor_seni`, `skor_soshum`. Kolom `hasil` akan berisi nama rumpun jurusan pemenang.

### [DELETE] `models/work_preference.py` & `models/study_preference.py`
Tabel ini tidak lagi relevan dan akan dihapus.

---

## 6. Tahapan Pengerjaan Baru

1. **Pembersihan (Cleanup)**: Menyesuaikan model database Python dengan konsep baru.
2. **Re-init Database**: Menghapus database lama dan membuat ulang tabel baru.
3. **Frontend VEYKU**: Membuat HTML/CSS yang persis meniru desain Landing Page VEYKU dari screenshot Anda.
4. **Logic Backend**: Memasukkan 10+ pertanyaan minat bakat dan algoritma perhitungan persentase jurusan.
5. **Dashboard Admin**: Menampilkan statistik jurusan yang paling cocok dengan pengguna.

---

## Verification Plan
1. Jalankan `python app.py` dan periksa UI Landing Page agar sama persis dengan gambar referensi.
2. Isi survei dan pastikan perhitungan 5 rumpun jurusan berjalan dengan benar.
