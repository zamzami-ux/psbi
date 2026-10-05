# Projek-PSBI

Proyek Django sederhana untuk LMS (Learning Management System).

## Ringkasan
Aplikasi ini adalah proyek Django (lihat `manage.py` dan `lms_project/`). Database default: SQLite (`db.sqlite3`).

## Persiapan dan menjalankan lokal

1. Buat virtual environment dan aktifkan:

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate
```

2. Pasang dependensi:

```bash
pip install -r requirements.txt
```

3. Migrasi database dan jalankan server:

```bash
python manage.py migrate
python manage.py runserver
```

4. Jalankan test:

```bash
pytest
```

## Catatan deploy
- Aplikasi ini dibuat sebagai aplikasi Django. Untuk deploy rekomendasi: Render, Heroku, atau VPS (Gunicorn + nginx).
- Jika tujuan Anda adalah menjadikan antarmuka sebagai aplikasi Streamlit, aplikasi perlu ditulis ulang ke `streamlit_app.py`. Beritahu saya jika Anda ingin saya buatkan versi Streamlit.

## Deploy Django (Heroku / Render)

Contoh langkah cepat untuk deploy ke Heroku / Render menggunakan Gunicorn:

1. Pastikan `requirements.txt`, `Procfile`, dan `runtime.txt` ada di root (sudah ditambahkan).

2. Set config vars (di Heroku/Render) untuk produksi:

- `DJANGO_SECRET_KEY` — secret key produksi
- `DJANGO_DEBUG` — `False` untuk produksi
- `DATABASE_URL` — (opsional) PostgreSQL URL, Heroku menyediakan ini otomatis

3. Jalankan deploy (Heroku contoh):

```bash
heroku create your-app-name
git push heroku main
heroku run python manage.py migrate
heroku run python manage.py collectstatic --noinput
heroku open
```

4. Jika menggunakan Render: atur build command `pip install -r requirements.txt` dan start command `gunicorn lms_project.wsgi`.

Catatan: Static files akan dilayani oleh WhiteNoise jika `DJANGO_DEBUG` diset `False`.

## Deploy with Docker (recommended for many hosts)

Quick steps to run the project in Docker locally or on any container host:

1. Copy `.env.example` to `.env` and edit values (especially `DJANGO_SECRET_KEY`).

2. Build and run with Docker Compose:

```bash
docker compose build
docker compose up -d
```

3. The app will be available at `http://localhost:8000`.

Notes:
- The `docker-compose.yml` creates a `db` Postgres service and the `web` service runs Gunicorn.
- The container `entrypoint.sh` runs migrations and `collectstatic` on start.
- For production hosting, push your Docker image to your container registry and run on your provider (Render, Railway, Fly, or any Kubernetes/VPS).


## Streamlit app
Saya menambahkan `app.py` sebagai entrypoint Streamlit yang merender template HTML sehingga dapat langsung dijalankan di Streamlit Cloud atau host Streamlit lain.

Jalankan lokal:

```bash
pip install -r requirements.txt
streamlit run app.py
```

Catatan: `app.py` merender HTML template statis (Django template tags tidak diproses). Jika Anda ingin integrasi dinamis antara Streamlit dan Django, kita perlu menambahkan API endpoints di Django dan panggil dari Streamlit.

### Deploying to Streamlit Cloud

**IMPORTANT:** The full `requirements.txt` contains server-side packages that fail on Streamlit Cloud. Use `requirements-streamlit.txt` instead.

#### Step-by-step setup:

1. **Push repository to GitHub:**
   ```bash
   git add .
   git commit -m "Add Streamlit app and deployment configs"
   git push origin main
   ```

2. **Connect to Streamlit Cloud:**
   - Go to https://streamlit.io/cloud
   - Click "New app" → select your GitHub repo → select branch `main` → set main file path to **`app.py`**
   - Click "Deploy"

3. **Fix requirements error:**
   - If you get an error like "Error installing requirements", go to your app's **Manage App** (top-right menu)
   - Go to **Settings** → **Advanced** → **Requirements file**
   - Change from `requirements.txt` to `requirements-streamlit.txt`
   - Click "Save" → Streamlit will redeploy automatically

4. **(Optional) Add backend URL to Streamlit Secrets:**
   - In **Manage App** → **Secrets**, paste:
   ```toml
   backend_url = "https://your-deployed-django-backend.render.com"
   ```
   - Replace with your actual Django backend URL (Render/Heroku/Docker)
   - The Streamlit app will use this URL for the Interactive mode

5. **Configure Django backend separately:**
   - Deploy Django on Render/Heroku/Docker (see "Deploy with Docker" section above)
   - Ensure Django is accessible from the Streamlit app (allow CORS if needed)
   - Test by using Streamlit's "Interactive" mode with the backend URL

#### Files involved:
- `app.py` — Streamlit app entrypoint
- `requirements-streamlit.txt` — minimal dependencies (use this for Streamlit Cloud!)
- `.streamlit/config.toml` — Streamlit configuration
- `.streamlit/secrets.example.toml` — template for backend URL (copy to Secrets in Streamlit Cloud)

## File penting
- `manage.py` — entrypoint Django.
- `lms_project/` — konfigurasi project.
- `dashboard/` — aplikasi utama dengan templates dan static files.
- `DEPLOYMENT.md` — detailed deployment guide untuk Streamlit Cloud, Render, Docker, etc.

## Lisensi
Lisensi MIT (file `LICENSE`).
