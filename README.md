# 📚 BookStore Management System
### Django + PyMongo + MongoDB Atlas  (works with Python 3.14)

---

## 📁 Project Structure

```
django-bookstore/
├── bookstore_project/
│   ├── settings.py      ← PUT YOUR ATLAS URI HERE
│   ├── urls.py
│   └── wsgi.py
├── books/
│   ├── templates/books/
│   │   └── index.html   ← Frontend
│   ├── mongo.py         ← MongoDB connection
│   ├── views.py         ← All CRUD operations
│   └── urls.py
├── manage.py
└── requirements.txt
```

---

## ✅ Step 1 — Add your Atlas URI

Open `bookstore_project/settings.py`

Find this line:
```python
MONGO_URI = 'mongodb+srv://<username>:<password>@cluster0.dlchkoo.mongodb.net/...'
```

Replace with YOUR connection string:
```python
MONGO_URI = 'mongodb+srv://admin:Bookstore123@cluster0.dlchkoo.mongodb.net/BookStoreDB?retryWrites=true&w=majority'
```

---

## 🚀 Step 2 — Install & Run

Open PowerShell inside the project folder:

```bash
cd D:\zaid\django-bookstore

pip install -r requirements.txt

python manage.py migrate

python manage.py runserver
```

Open browser: **http://127.0.0.1:8000**

---

## ✅ Why this works with Python 3.14

- ❌ Old version used **djongo** — broken on Python 3.14
- ✅ This version uses **pymongo directly** — works on all Python versions
- Django handles routing and templates
- PyMongo talks to MongoDB Atlas

---

## ❗ Common Errors

| Error | Fix |
|-------|-----|
| `Authentication failed` | Wrong password in MONGO_URI |
| `ServerSelectionTimeoutError` | IP not whitelisted in Atlas / use hotspot |
| `ModuleNotFoundError: pymongo` | Run `pip install -r requirements.txt` |
