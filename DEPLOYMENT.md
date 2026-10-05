# Deployment Guide

This guide covers the three recommended ways to deploy **Projek-PSBI**.

## 1. Streamlit App (Frontend only) → Streamlit Cloud

### Use case:
You want a lightweight frontend deployed on Streamlit Cloud.

### Steps:

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Ready for Streamlit Cloud"
   git push origin main
   ```

2. **Go to Streamlit Cloud** (https://streamlit.io/cloud)
   - Click "New app"
   - Select your repo, branch `main`, main file `app.py`
   - Click "Deploy"

3. **Fix requirements error** (if it occurs):
   - Manage App → Settings → Advanced → Requirements file
   - Change to `requirements-streamlit.txt`
   - Save (auto-redeploy)

4. **(Optional) Add backend URL to Secrets**
   - Manage App → Secrets
   - Paste:
   ```toml
   backend_url = "https://your-django-backend.render.com"
   ```
   - The Streamlit app's "Interactive" mode will use this URL

---

## 2. Django Backend + Streamlit Frontend (Separate deployments)

### Use case:
You want both the Django API and Streamlit frontend running online.

### Step A: Deploy Django on Render or Heroku

#### Render example:
1. Go to https://render.com
2. Click "New +" → "Web Service"
3. Connect your GitHub repo
4. Settings:
   - **Build Command:** `pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput`
   - **Start Command:** `gunicorn lms_project.wsgi:application --bind 0.0.0.0:$PORT`
   - **Environment Variables:**
     ```
     DJANGO_SECRET_KEY=<generate-a-secure-random-key>
     DJANGO_DEBUG=False
     DATABASE_URL=<Render provides this if you add PostgreSQL>
     ```
5. Click "Deploy"
6. After deployment, copy your app's URL (e.g., `https://your-app.render.com`)

### Step B: Deploy Streamlit on Streamlit Cloud

1. Follow steps 1-3 from section 1 above
2. In Streamlit Secrets, add:
   ```toml
   backend_url = "https://your-app.render.com"
   ```
3. The Streamlit "Interactive" mode will talk to your Render Django app

---

## 3. Docker Deployment (All-in-one)

### Use case:
You want everything containerized and deployable anywhere.

### Local testing:
```bash
cp .env.example .env
# Edit .env and set DJANGO_SECRET_KEY to something secure

docker compose build
docker compose up -d
# Visit http://localhost:8000
```

### Deploy to production:
- **Render:** Push Dockerfile to Render (Auto-detects Docker)
- **Fly.io:** Use `flyctl deploy`
- **AWS/GCP/Azure:** Push image to ECR/GCR/ACR, then deploy
- **Your own VPS:** Push image to registry, pull on VPS, run with docker-compose

#### Example: Deploy to Render with Docker
1. Go to https://render.com
2. Click "New +" → "Web Service"
3. Connect repo
4. Runtime: Select "Docker"
5. Settings:
   - **Build Command:** `docker build -t myapp .`
   - **Start Command:** `docker run -p $PORT:8000 myapp`
   - **Environment Variables:**
     ```
     DJANGO_SECRET_KEY=<secure-key>
     DJANGO_DEBUG=False
     DATABASE_URL=<PostgreSQL connection string>
     ```
6. Deploy

---

## Comparison

| Method | Cost | Ease | Best For |
|--------|------|------|----------|
| Streamlit Cloud only | Free tier available | Very easy | Quick demo, frontend-only |
| Render (Django) + Streamlit Cloud | $7-12/mo (Render) | Easy | Production with separate frontend/backend |
| Docker on Render/Fly | $5-20/mo | Medium | Full control, scalable |

---

## Environment Variables Reference

### Django (`.env` or platform settings)
- `DJANGO_SECRET_KEY` — Django secret key (generate one!)
- `DJANGO_DEBUG` — `False` for production
- `DATABASE_URL` — PostgreSQL URL (optional; defaults to SQLite)
- `ALLOWED_HOSTS` — Comma-separated list of allowed domains

### Streamlit (`.streamlit/secrets.toml` or platform Secrets)
- `backend_url` — URL to your Django API (e.g., `https://your-app.render.com`)

---

## Troubleshooting

### Streamlit Cloud: "Error installing requirements"
- **Solution:** Set Requirements file to `requirements-streamlit.txt` in App Settings

### Streamlit can't reach Django API
- Check `backend_url` in Streamlit Secrets
- Ensure Django allows requests from Streamlit's domain (CORS settings if needed)
- Django should have CORS middleware if Streamlit is on different domain

### Django collectstatic fails
- Ensure `STATIC_ROOT` is set in `settings.py` (it is by default)
- Try: `python manage.py collectstatic --noinput`

---

## Need help?
- Django: https://docs.djangoproject.com/
- Streamlit: https://docs.streamlit.io/
- Render: https://render.com/docs
- Docker: https://docs.docker.com/
