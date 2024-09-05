Here’s the full **README.md** code with modern tags and formatting based on the content you provided:

```md
# StoryKeeper 📝

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Django](https://img.shields.io/badge/Django-4.x-green)
![MySQL](https://img.shields.io/badge/Database-MySQL-blue)
![Google OAuth](https://img.shields.io/badge/Auth-Google%20OAuth2-orange)
![License](https://img.shields.io/github/license/<your-username>/StoryKeeper)

---

## 🚀 **Getting Started**

### **1. Create a Virtual Environment**
```bash
python -m venv env
source env/bin/activate  # For Linux/macOS
# or
env\Scripts\activate  # For Windows
```

### **2. Install Dependencies**
```bash
pip install -r requirements.txt
```

---

## 🛠️ **Database Configuration**

### **MySQL Setup**

#### **Step 1: Update Settings**
- In `settings.py`, uncomment the MySQL database settings and comment out the SQLite configuration.

#### **Step 2: Create `my.cnf` File**
- Add a `my.cnf` file with the following format:

```ini
[client]
database = DB_NAME
host = localhost
user = DB_USER
password = DB_PASSWORD
default-character-set = utf8
```

#### **Step 3: Link MySQL Config**
- Add the path to your `my.cnf` file in `settings.py`:

```python
'read_default_file': '/path/to/my.cnf'
```

#### **Step 4: Migrate the Database**
```bash
python manage.py makemigrations
python manage.py migrate
```

#### **Step 5: Create a Superuser**
```bash
python manage.py createsuperuser
```

#### **Step 6: Import CSV Data**
- Use the provided CSV file in the `src` folder:

```bash
python manage.py import_csv_data /path/to/csv
```

---

## 🔐 **Google Authentication**

### **Step 1: Create a Google Project**
- Visit the [Google OAuth2 Console](https://developers.google.com/identity/protocols/oauth2) and create a project.

### **Step 2: Update `settings.py`**
- Add your `client_id` and `client_secret` in the `SOCIALACCOUNT_PROVIDERS` section.

---

## ⚙️ **Additional Customizations**

- You can adjust **session duration** in the `member.forms` file to suit your requirements.
- Contributions are welcome! Feel free to fork and open a pull request.

---

## 📸 **Project Screenshots**

![Screenshot 1](./path/to/images/1.png)
![Screenshot 2](./path/to/images/2.png)
![Screenshot 3](./path/to/images/3.png)
![Screenshot 4](./path/to/images/4.png)
![Screenshot 5](./path/to/images/5.png)
![Screenshot 6](./path/to/images/6.png)
![Screenshot 7](./path/to/images/7.png)
![Screenshot 8](./path/to/images/8.png)
![Screenshot 9](./path/to/images/9.png)

---

## 🤝 **Contributing**

- Fork this repository
- Create a branch: `git checkout -b <branch_name>`
- Make your changes and commit them: `git commit -m '<commit_message>'`
- Push to the branch: `git push origin <branch_name>`
- Open a pull request

---
