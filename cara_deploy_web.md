Workflow Update: Lokal → GitHub → PythonAnywhere
1️⃣ Di Lokal (VS Code) — Edit seperti biasa
Modifikasi file apa saja yang kamu mau, tambah fitur, perbaiki bug, dll.

2️⃣ Push ke GitHub
Buka terminal di VS Code, jalankan:

bash
git add .
git commit -m "Deskripsi perubahan kamu"
git push origin main
3️⃣ Di PythonAnywhere — Pull & Reload
Buka Bash console di PythonAnywhere, jalankan:

bash
git pull origin main

4️⃣ Restart WSGI server
Dari Web tab di PythonAnywhere, klik "Reload" di bagian WSGI configuration.
Selesai! Perubahan kamu akan langsung live.

Cuma itu saja! Kalau ada perubahan yang menambahkan package baru di requirements.txt, tambahkan langkah install sebelum reload:

bash
cd ~/VeyKu
source .venv/bin/activate
pip install --no-cache-dir nama_package_baru