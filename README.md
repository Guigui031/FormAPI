# FormAPI

A clean, secure Flask API for handling contact form submissions via Gmail API.

## 🚀 Features

- **RESTful API** for contact form submissions
- **Gmail API integration** for reliable email delivery
- **Environment-based configuration** for security
- **OAuth2 authentication** flow for Gmail
- **Docker support** for easy deployment
- **Health check endpoint** for monitoring
- **CORS enabled** for frontend integration

## 📁 Project Structure

```
FormAPI/
├── src/
│   ├── app.py              # Main Flask application
│   └── setup_auth.py       # OAuth setup utility
├── tests/
│   ├── test_email.py       # Local testing script
│   └── test_production.py  # Production testing script
├── docker-compose.yml      # Docker compose configuration
├── Dockerfile             # Docker image definition
├── requirements.txt       # Python dependencies
└── README.md              # This file
```

## ⚙️ Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Gmail API Configuration
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Gmail API
4. Create credentials (OAuth 2.0 Client ID)
5. Download `credentials.json` to the project root

### 3. Environment Variables (Optional)
Create a `.env` file or set environment variables:
```bash
SECRET_KEY=your-secret-key-here
RECIPIENT_EMAIL=your-email@example.com
SENDER_EMAIL=your-gmail@gmail.com
PRODUCTION_DOMAIN=your-domain.com
```

### 4. Local Authentication Setup
```bash
python src/setup_auth.py
```

### 5. Run the Application
```bash
python src/app.py
```

## API Endpoints

### POST /api/contact
Submit a contact form that will be emailed to your configured address.

**Request Body:**
```json
{
    "name": "John Doe",
    "email": "john@example.com",
    "subject": "Contact Form Submission",
    "message": "Hello, this is a test message."
}
```

**Response:**
```json
{
    "success": true,
    "message": "Form submitted successfully",
    "message_id": "gmail-message-id"
}
```

### GET /health
Health check endpoint.

**Response:**
```json
{
    "status": "healthy"
}
```

## 🧪 Testing

### Local Testing
```bash
python tests/test_email.py
```

### Production Testing
```bash
python tests/test_production.py
```

### Manual API Testing
```bash
curl -X POST http://localhost:5000/api/contact \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "subject": "Test Subject",
    "message": "This is a test message from the form API."
  }'
```

## Deployment

### 🐳 Docker Deployment (Recommended)

1. **Using docker-compose:**
```bash
docker-compose up -d
```

2. **Manual Docker build:**
```bash
docker build -t formapi .
docker run -d -p 5000:5000 \
  -e RECIPIENT_EMAIL=your-email@example.com \
  -e SECRET_KEY=your-production-secret \
  formapi
```

### 🚀 Traditional Deployment

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Set production environment variables**

3. **Run with Gunicorn:**
```bash
gunicorn -w 4 -b 0.0.0.0:5000 src.app:app
```

4. **Configure reverse proxy (nginx/Apache)**

### Sample Nginx Configuration

```nginx
server {
    listen 443 ssl;
    server_name form.guillaume.genois.ca;

    ssl_certificate /path/to/your/cert.pem;
    ssl_certificate_key /path/to/your/private.key;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```