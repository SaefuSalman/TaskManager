# Task Manager — Django

Final project bootcamp: aplikasi web manajemen tugas (to-do list) dengan
autentikasi user, dibangun pakai Django. Setiap user hanya bisa melihat
dan mengelola tugasnya sendiri.

## Fitur

- Registrasi & login user (pakai sistem auth bawaan Django)
- CRUD tugas: buat, lihat, edit, hapus
- Setiap tugas punya status (To Do / In Progress / Done) dan prioritas
  (Low / Medium / High)
- Filter daftar tugas berdasarkan status
- Data terisolasi per user — user A tidak bisa lihat/akses tugas user B
- Halaman admin Django siap pakai untuk mengelola data langsung

## Struktur Proyek

```
task-manager-django/
├── manage.py
├── requirements.txt
├── .gitignore
├── taskmanager/          # konfigurasi project (settings, urls utama)
│   ├── settings.py
│   ├── urls.py
│   └── ...
├── tasks/                 # app utama
│   ├── models.py          # model Task
│   ├── forms.py           # form create/edit Task
│   ├── views.py           # logic CRUD + registrasi
│   ├── urls.py            # routing app tasks
│   ├── admin.py           # konfigurasi Django admin
│   └── tests.py           # unit test (6 test, semua lulus)
└── templates/              # semua template HTML (Bootstrap 5 via CDN)
    ├── base.html
    ├── registration/
    │   ├── login.html
    │   └── register.html
    └── tasks/
        ├── task_list.html
        ├── task_detail.html
        ├── task_form.html
        └── task_confirm_delete.html
```

## Cara Menjalankan

### 1. Setup environment

```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Migrasi database

```bash
python manage.py migrate
```

### 3. (Opsional) Buat superuser untuk akses `/admin/`

```bash
python manage.py createsuperuser
```

### 4. Jalankan server

```bash
python manage.py runserver
```

Buka `http://127.0.0.1:8000/` di browser. Kamu akan diarahkan ke halaman
login — klik "Daftar di sini" untuk membuat akun baru, lalu langsung bisa
mulai menambah tugas.

### 5. Jalankan test

```bash
python manage.py test tasks
```

## Konsep Django yang Dipakai (untuk bahan presentasi)

| Konsep | Di mana dipakai |
|---|---|
| Model & ORM | `tasks/models.py` — `Task` dengan `ForeignKey` ke `User` |
| Class-based views | `TaskListView`, `TaskDetailView` (generic `ListView`/`DetailView`) |
| Function-based views | `task_create`, `task_update`, `task_delete` |
| Forms | `TaskForm` (ModelForm) untuk validasi input |
| Auth bawaan Django | Login, logout, `UserCreationForm` untuk registrasi |
| Middleware `LoginRequiredMixin` / `@login_required` | Proteksi halaman yang butuh login |
| Template inheritance | `base.html` di-*extend* semua halaman |
| Django Admin | Terdaftar di `tasks/admin.py`, siap dipakai di `/admin/` |
| Testing | `tasks/tests.py` — test model, akses data antar user, CRUD |

## Catatan Keamanan untuk Production

Kalau mau di-deploy (bukan cuma untuk demo/latihan), sebelum production:

- [ ] Pindahkan `SECRET_KEY` di `settings.py` ke environment variable
- [ ] Set `DEBUG = False`
- [ ] Isi `ALLOWED_HOSTS` sesuai domain
- [ ] Ganti database dari SQLite ke PostgreSQL
- [ ] Kumpulkan static files dengan `python manage.py collectstatic`

## Rencana Pengembangan Selanjutnya

- [ ] Tambah REST API dengan Django REST Framework
- [ ] Reminder due date lewat email (Django `send_mail` + Celery)
- [ ] Fitur kolaborasi: assign tugas ke user lain
- [ ] Deploy ke Railway/Render dengan PostgreSQL

## Author

Dibuat sebagai final project bootcamp Python (jalur Backend) — Nusacodes.
