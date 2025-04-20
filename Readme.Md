# Syllabyte

![Syllabyte Logo](https://github.com/avi-dev-machine/Syllabyte/blob/main/Screenshot%202025-04-20%20081617.png)

> AI-powered study aid generator that transforms syllabus content into comprehensive, interactive study materials

## Overview

Syllabyte is an advanced educational tool designed to revolutionize how students study. By leveraging AI technology, it converts syllabus content and academic topics into a variety of engaging study formats including detailed notes, formula compilations, interactive mind maps, and self-assessment quizzes.

## Features

### 🧠 Study Material Generation
- **Intelligent Notes**: Automatically generated study notes with full markdown support
- **Formula Extraction**: Smart identification and formatting of mathematical formulas
- **Interactive Mind Maps**: Visual concept mapping powered by GoJS
- **Self-Assessment**: Auto-generated MCQs with detailed explanations
- **Document Support**: Upload and process syllabi in PDF and DOCX formats

### 👤 User Management
- Secure account registration and authentication
- Personal study material library
- Search history tracking and management
- Comprehensive user profiles

### 🎨 User Interface
- Professional dark theme with neon accents
- Fully responsive design for all devices
- Animated transitions and backgrounds
- Interactive data visualizations

## Getting Started

### Prerequisites
- Python 3.8+
- pip
- Virtual environment tool (recommended)

### Installation

1. Clone the repository
```bash
git clone https://github.com/yourusername/syllabyte.git
cd syllabyte
```

2. Set up a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Configure environment variables
```bash
cp .env.example .env
# Edit .env file and add your Groq API key
```

5. Initialize the database
```bash
flask db upgrade
```

6. Run the application
```bash
flask run
```

## Configuration

Essential configuration options in the `.env` file:

```
GROQ_API_KEY=gsk_your_key_here
FLASK_SECRET_KEY=your_secret_key
DATABASE_URL=sqlite:///history.db
```

## Tech Stack

### Frontend
- HTML5 / CSS3
- JavaScript
- GoJS (mind mapping)
- MathJax (math rendering)
- Marked.js (markdown parsing)

### Backend
- Python
- Flask web framework
- SQLAlchemy ORM
- Groq LLM API
- SQLite database

## API Documentation

### Authentication Endpoints
- `POST /register` - Create new user account
- `POST /login` - Authenticate existing user
- `GET /logout` - End current user session

### Study Material Endpoints
- `POST /index` - Generate study materials from a topic
- `POST /upload_document` - Process uploaded syllabus documents
- `GET /get_history_content/<history_id>` - Retrieve saved study materials

## Security

Syllabyte implements several security measures:
- Secure API key management via environment variables
- Password hashing before storage
- Session-based authentication
- Input validation and sanitization
- Cross-Site Request Forgery (CSRF) protection

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- The Groq team for their powerful LLM API
- GoJS for mind mapping capabilities
- MathJax for beautiful math rendering

---

Crafted with 🧠 by the Syllabyte Team – Revolutionizing the way students study with AI.
