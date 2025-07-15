# Anton LAN Storage

Anton LAN Storage is a minimal, self-hosted file manager for your local network.

Upload, download, and organize files and folders from any device on the same LAN — all through a simple web UI.

![Screenshot](https://your-screenshot-url-if-any)

---

## Features

- 📁 Upload / download / delete files
- 🗂️ Create folders
- 🎨 Clean, mobile-friendly Tailwind UI
- 🔐 Login auth (via `.env`)
- 📦 Easy setup with Python or Docker

---

## Requirements

- Python 3.8+ **or** Docker

---

## Option 1: Run with Python

```bash
git clone https://github.com/Swanand01/anton-LAN-storage.git

cp .env.example .env  # Optional: configure credentials
python run.py
```

## Option 2: Run with Docker Compose

```bash
docker-compose up
```

App runs at: http://localhost:8000

## Default Login

By default, login is required.

Set your credentials in .env:

```env
AUTH_USERNAME=admin
AUTH_PASSWORD=secret
SECRET_KEY=randomsecretkey
```

For security, the app will not start without `AUTH_USERNAME` and `AUTH_PASSWORD`.

## Tech Stack

- Flask
- Tailwind CSS
- Docker (optional)

[!NOTE] This app is designed for LAN use — **not hardened for internet-facing production**.