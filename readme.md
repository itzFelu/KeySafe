# 🔐 KeySafe – Access Your Data Anytime, Anywhere

## 📌 Overview
**KeySafe** is a secure web-based note management system that allows users to store, access, and manage personal notes from anywhere. The application focuses on **multi-layer authentication**, **data security**, and a **clean user experience**.

---

## 🚀 Tech Stack
- **Backend:** Python, Django  
- **Database:** SQLite *(can be upgraded to PostgreSQL)*  
- **Frontend:** Django Templates, Bootstrap  
- **Authentication:** Django Auth + Custom Security Question Layer  

---

## ✨ Features

### 🔑 1. User Authentication System

#### 📝 Sign Up
Users must register with:
- Name  
- Date of Birth  
- Email ID *(unique)*  
- Password & Confirm Password  
- Security Question *(select one)*:
  - School Name  
  - Favorite Player  
  - Nickname  
- Security Answer  

**Validation Rules:**
- Unique email required  
- Password confirmation must match  
- Only one security question allowed  

---

#### 🔓 Sign In (Multi-Step Authentication)
1. Enter Email + Password  
2. If valid → Prompt Security Question  
3. Correct Answer → Login Successful  
4. Incorrect Answer → Authentication Failed  

---

#### 🔁 Forgot Password
- Enter registered Email ID  
- Receive password reset link  
- Reset password via email link  

---

## 🏠 2. Dashboard

### Header
- Left: Branding + About  
- Right:
  - Profile Icon  
  - Dropdown:
    - Name & Email  
    - Profile  
    - Logout  

### Body
- Center: **Add Note Button**  
- Below: List of Notes  

Each note includes:
- Clickable title → Open note  
- Three-dot menu (⋮):
  - Edit  
  - Delete  

---

## 🗒️ 3. Notes Management

### ➕ Add Note
- Fields:
  - Title  
  - Content  

- Actions:
  - Save  
  - Discard  

**Behavior:**
- Discard triggers confirmation if fields are not empty  
- On save → Redirect to dashboard with success message  

---

### 👁️ View Note (Read Mode)
- Title (top-left)  
- Content (read-only)  
- Three-dot menu:
  - Edit  
  - Delete  

---

### ✏️ Edit Note
- Editable mode  
- Save / Cancel options  

---

### 🗑️ Delete Note (Soft Delete)
- Confirmation modal before deletion  
- Uses soft delete:
  - `is_deleted = True`  

**Future Scope:**
- Trash & Restore functionality  

---

## 👤 4. Profile Management

### Profile Page
- Displays:
  - Name  
  - Email  

---

### 🔐 Update Password
- Shows confirmation modal  
- Sends password reset link to registered email  

---

### ❓ Update Security Question
- Requires current password  
- User selects new question + answer  

---

## 🔄 Data Flow

### 🔐 Authentication Flow
```
Sign Up → Store User + Security Q/A  
Sign In → Validate Password → Validate Security Answer → Login  
Forgot Password → Email → Reset Link → Update Password  
```

---

### 🗒️ Notes Flow
```
Dashboard → Add Note → Save → Display in List  
Click Note → View Mode  
Edit → Update → Save  
Delete → Soft Delete → Hidden from List  
```

---

### 👤 Profile Flow
```
Profile Page →
   → Update Password (via email link)  
   → Update Security Question (requires password)  
```

---

## 🗄️ Database Design (High-Level)

### User (Extended Django User)
- id  
- name  
- dob  
- email  
- password  
- security_question  
- security_answer  

---

### Note
- id  
- user_id (FK)  
- title  
- content  
- created_at  
- updated_at  
- is_deleted *(Boolean, default=False)*  

---

## ⚙️ Key Design Considerations

### 🔒 Security
- Password hashing (Django default)  
- Security question as second layer  
- Email-based password reset  

### 📈 Scalability
- SQLite → Upgradeable to PostgreSQL  
- Modular Django architecture  

### 🎨 User Experience
- Clean Bootstrap UI  
- Modal confirmations  
- Clear success/error messages  

---

## 🔮 Future Enhancements
- Trash & Restore Notes  
- Search functionality *(ElasticSearch / Django ORM)*  
- Rich text editor  
- Tags / Categories  
- Note sharing  
- Two-Factor Authentication (OTP)  
- REST API (Django REST Framework)  

---

## 🛠️ Setup Instructions (Optional Section)

```bash
# Clone the repository
git clone https://github.com/itzfelu/keysafe.git

# Navigate into project
cd keysafe

# Create virtual environment
python -m venv venv

# Activate environment
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start server
python manage.py runserver

```
---

## 📌 Authors

- **Sukanta Roy**  
- **Ramit Kumar Mandal**
