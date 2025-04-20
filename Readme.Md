```markdown
# 📘 Syllabyte

Syllabyte is an AI-powered study aid generator that transforms syllabus content and topics into comprehensive, interactive study materials—including notes, formulas, mind maps, and quizzes.

---

## 📑 Table of Contents

1. [Features](#features)
2. [Tech Stack](#tech-stack)
3. [Project Structure](#project-structure)
4. [Installation](#installation)
5. [Configuration](#configuration)
6. [API Documentation](#api-documentation)
7. [UI Components](#ui-components)
8. [Security Considerations](#security-considerations)
9. [Error Handling](#error-handling)
10. [Performance Optimization](#performance-optimization)
11. [Future Enhancements](#future-enhancements)

---

## ✨ Features

### 🧠 Study Material Generation
- Notes generation with markdown support
- Formula extraction and formatting
- Interactive mind maps using **GoJS**
- MCQ generation for self-assessment
- Document upload support (PDF, DOCX)

### 👤 User Management
- User registration and authentication
- Search history tracking
- Personal study material storage
- Secure password handling

### 🎨 Interactive UI
- Dark theme with neon accents
- Responsive design
- Animated backgrounds
- Interactive visualizations

---

## 🛠 Tech Stack

### 🔹 Frontend
- HTML5 / CSS3
- JavaScript
- [GoJS](https://gojs.net/) – for mind maps
- [MathJax](https://www.mathjax.org/) – for rendering math
- [Marked.js](https://marked.js.org/) – for markdown rendering

### 🔸 Backend
- Python
- Flask
- SQLAlchemy ORM
- Groq LLM API
- SQLite database


---

## ⚙️ Installation

```bash
# Clone the repository
git clone <repository-url>
cd groq_Api_

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env and add your Groq API key

# Initialize database
flask db upgrade
```

---

## 🔐 Configuration

```env
GROQ_API_KEY=gsk_your_key_here
FLASK_SECRET_KEY=secret_key
DATABASE_URL=sqlite:///history.db
```

---

## 🧬 API Documentation

### 🔐 Authentication Endpoints

- `POST /register` – Register a new user  
  **Params:** `username`, `password`

- `POST /login` – Log in a user  
  **Params:** `username`, `password`

- `GET /logout` – Log out the current user

### 📚 Study Material Endpoints

- `POST /index` – Generate study materials  
  **Params:** `topic`

- `POST /upload_document` – Upload and process a document  
  **Params:** `file` (PDF/DOCX)

- `GET /get_history_content/<history_id>` – Retrieve saved materials  
  **Params:** `history_id`

---

## 🧱 UI Components

- Interactive mind maps using **GoJS**
- Real-time math rendering via **MathJax**
- Markdown-based notes viewer with **Marked.js**
- PDF and DOCX upload interface
- Stylish neon-accented dark mode theme

---

## 🔐 Security Considerations

1. API key managed securely via environment variables  
2. Passwords hashed before storage  
3. Session-based authentication with Flask  
4. Input validation and sanitization  
5. CSRF protection via Flask-WTF

---

## ⚠️ Error Handling

- Custom error pages
- Flash messages for feedback
- File upload validation
- Clean API error responses

---

## 🚀 Performance Optimization

- Lazy-loading of heavy assets
- Caching of generated content
- Optimized database access
- Minified and compressed static files

---

## 🧭 Future Enhancements

- Support for additional file formats (e.g., PPTX, ODT)
- Real-time collaboration on study materials
- Personalization and theme customization
- Mobile application version
- API rate limiting for security and scalability

---

> Crafted with 🧠 by the Syllabyte Team – Revolutionizing the way students study with AI.
```
