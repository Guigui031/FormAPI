# FormAPI

A clean, secure Flask API for handling contact form submissions via Gmail API.

## 🚀 Features

- **RESTful API** for contact form submissions
- **Gmail API integration** for reliable email delivery
- **Environment-based configuration** for security
- **OAuth2 authentication** with dual-mode support (local & production)
- **Docker support** for easy deployment
- **Health check endpoint** for monitoring
- **CORS enabled** for frontend integration
- **Automatic credential management** with fallback logic

## 📁 Project Structure

```
FormAPI/
├── src/
│   ├── app.py              # Main Flask application
│   └── setup_auth.py       # OAuth setup utility
├── archives/               # Old test files (not actively used)
├── docker-compose.yml      # Docker compose configuration
├── Dockerfile              # Docker image definition
├── nginx-config.conf       # Sample nginx reverse proxy config
├── requirements.txt        # Python dependencies
├── setup_service_account.md # Service account setup guide
├── CLAUDE.md               # AI assistant guidance document
└── README.md               # This file
```

## ⚙️ Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Gmail API Configuration

#### Option A: OAuth2 (Local Development)
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Gmail API
4. Create credentials (OAuth 2.0 Client ID)
   - Application type: Desktop app
   - Download `credentials.json` to the project root

#### Option B: Service Account (Production)
See `setup_service_account.md` for detailed instructions.

### 3. Environment Variables

Create a `.env` file or set environment variables:

```bash
# Required
RECIPIENT_EMAIL=your-email@example.com
SENDER_EMAIL=your-gmail@gmail.com

# Optional (with defaults)
SECRET_KEY=your-secret-key-here  # Default: development key
PRODUCTION_DOMAIN=your-domain.com  # Default: form.guillaume.genois.ca

# For service account authentication (production)
GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json
```

### 4. Local Authentication Setup

Run the OAuth setup utility to authenticate with Gmail:

```bash
python src/setup_auth.py
```

This will:
- Open a browser window for Google authentication
- Generate `token.json` with your credentials
- Allow the app to send emails from your Gmail account

### 5. Run the Application

**Development mode:**
```bash
python src/app.py
```

**Production mode (with Gunicorn):**
```bash
gunicorn --bind 0.0.0.0:5000 --workers 4 src.app:app
```

The API will be available at `http://localhost:5000`

## 📡 API Endpoints

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

**Response (Success):**
```json
{
    "success": true,
    "message": "Form submitted successfully",
    "message_id": "18f1234567890abcd"
}
```

**Response (Error):**
```json
{
    "success": false,
    "error": "Missing required field: email"
}
```

**Validation:**
- All fields (`name`, `email`, `subject`, `message`) are required
- Email must contain `@` and `.`
- Empty/whitespace-only values are rejected

### GET /health
Health check endpoint for monitoring.

**Response:**
```json
{
    "status": "healthy"
}
```

### GET /auth
Initiates OAuth2 authentication flow (for initial setup).

### GET /auth/callback
OAuth2 callback handler (automatically called by Google).

### GET /debug-redirect
Debug endpoint showing OAuth redirect URI configuration.

## 🧪 Testing

### Manual API Testing

**Health check:**
```bash
curl http://localhost:5000/health
```

**Submit a contact form:**
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

**Test with invalid data:**
```bash
curl -X POST http://localhost:5000/api/contact \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "invalid-email",
    "subject": "Test",
    "message": "Test"
  }'
```

## 🐳 Docker Deployment (Recommended)

### Quick Start with Docker Compose

```bash
docker-compose up -d
```

This will:
- Build the Docker image
- Run the container on port 5000
- Mount your credentials for Gmail API access
- Enable automatic restart

### Manual Docker Build

```bash
# Build the image
docker build -t formapi .

# Run with environment variables
docker run -d -p 5000:5000 \
  -e RECIPIENT_EMAIL=your-email@example.com \
  -e SENDER_EMAIL=your-gmail@gmail.com \
  -e SECRET_KEY=your-production-secret \
  -v ~/.config/gcloud:/home/app/.config/gcloud:ro \
  --name formapi \
  formapi
```

### Docker with Service Account

For production deployments using a service account:

```bash
docker run -d -p 5000:5000 \
  -e RECIPIENT_EMAIL=your-email@example.com \
  -e SENDER_EMAIL=your-gmail@gmail.com \
  -e SECRET_KEY=your-production-secret \
  -e GOOGLE_APPLICATION_CREDENTIALS=/app/service-account.json \
  -v /path/to/service-account.json:/app/service-account.json:ro \
  --name formapi \
  formapi
```

## 🚀 Traditional Deployment

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Production Environment Variables

```bash
export RECIPIENT_EMAIL=your-email@example.com
export SENDER_EMAIL=your-gmail@gmail.com
export SECRET_KEY=your-production-secret
export PRODUCTION_DOMAIN=your-domain.com
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json
```

### 3. Run with Gunicorn

```bash
gunicorn --bind 0.0.0.0:5000 --workers 4 src.app:app
```

For production, use a process manager like systemd:

```ini
# /etc/systemd/system/formapi.service
[Unit]
Description=FormAPI Service
After=network.target

[Service]
User=www-data
WorkingDirectory=/var/www/FormAPI
Environment="RECIPIENT_EMAIL=your-email@example.com"
Environment="SENDER_EMAIL=your-gmail@gmail.com"
Environment="SECRET_KEY=your-production-secret"
Environment="PRODUCTION_DOMAIN=your-domain.com"
Environment="GOOGLE_APPLICATION_CREDENTIALS=/var/www/FormAPI/service-account.json"
ExecStart=/usr/local/bin/gunicorn --bind 0.0.0.0:5000 --workers 4 src.app:app

[Install]
WantedBy=multi-user.target
```

### 4. Configure Reverse Proxy

**Sample Nginx Configuration:**

```nginx
server {
    listen 443 ssl http2;
    server_name form.your-domain.com;

    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;

    # Security headers
    add_header X-Content-Type-Options nosniff;
    add_header X-Frame-Options DENY;
    add_header X-XSS-Protection "1; mode=block";

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # CORS headers (if needed)
        add_header Access-Control-Allow-Origin *;
        add_header Access-Control-Allow-Methods "POST, GET, OPTIONS";
        add_header Access-Control-Allow-Headers "Content-Type";
    }

    # Health check endpoint
    location /health {
        proxy_pass http://localhost:5000/health;
        access_log off;
    }
}

# HTTP to HTTPS redirect
server {
    listen 80;
    server_name form.your-domain.com;
    return 301 https://$server_name$request_uri;
}
```

## 🔐 Authentication Modes

The application automatically handles authentication in two modes:

### Local Development
- Uses `token.json` generated by `src/setup_auth.py`
- Requires interactive OAuth2 flow once
- Credentials stored locally and auto-refreshed

### Production
- Uses Google Application Default Credentials
- Supports service account authentication
- Set `GOOGLE_APPLICATION_CREDENTIALS` environment variable

The app intelligently falls back between these methods for maximum flexibility.

## 📝 Environment Variables Reference

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `RECIPIENT_EMAIL` | Yes | `guillaumegenois031@gmail.com` | Email address to receive form submissions |
| `SENDER_EMAIL` | Yes | `guillaumegenois031@gmail.com` | Gmail account used to send emails |
| `SECRET_KEY` | No | `your-secret-key-change-this-in-production` | Flask session secret key |
| `PRODUCTION_DOMAIN` | No | `form.guillaume.genois.ca` | Production domain for OAuth redirects |
| `GOOGLE_APPLICATION_CREDENTIALS` | No | - | Path to service account JSON file |
| `FLASK_ENV` | No | - | Set to `production` for production mode |

## 🛠️ Development

### Project Dependencies
- Flask 2.3.3 - Web framework
- Flask-CORS 4.0.0 - CORS support
- google-auth 2.23.3 - Google authentication
- google-api-python-client 2.104.0 - Gmail API client
- gunicorn 21.2.0 - WSGI HTTP server

### Key Implementation Details

**Gmail API Scope:**
- Uses `gmail.send` scope only
- To add email reading functionality, update `SCOPES` in `src/app.py`

**OAuth Redirect URI:**
- Production: Forces HTTPS with `PRODUCTION_DOMAIN`
- Development: Uses `request.url_root`

**Email Format:**
- Plain text email with structured form data
- Reply-To header set to form submitter's email
- Automatic "Form Submission:" prefix on subject

## 📚 Additional Resources

- [Gmail API Documentation](https://developers.google.com/gmail/api)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Docker Documentation](https://docs.docker.com/)
- [Gunicorn Documentation](https://docs.gunicorn.org/)

## 🤝 Contributing

When working on this project:
1. Review `CLAUDE.md` for architectural guidelines
2. Test locally before deploying
3. Update documentation for any API changes
4. Follow existing code structure and patterns

## 📄 License

This project is provided as-is for personal and educational use.
