# FormAPI

A simple Flask API for handling contact form submissions via Gmail API.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up Gmail API credentials:
   - Follow the Gmail API quickstart guide to enable the API and get credentials
   - Save your credentials file as needed for google.auth.default()

3. Run the server:
```bash
python app.py
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

## Example Usage

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

### Option 1: Docker Deployment (Recommended)

1. **Build and run with docker-compose:**
```bash
docker-compose up -d
```

2. **Or build and run manually:**
```bash
docker build -t formapi .
docker run -d -p 5000:5000 \
  -v ~/.config/gcloud:/home/app/.config/gcloud:ro \
  formapi
```

3. **For your subdomain (form.guillaume.genois.ca):**
   - Configure nginx/Apache to proxy to the Docker container
   - Set up SSL certificates for HTTPS
   - Use a reverse proxy configuration

### Option 2: Traditional Deployment

1. Configure your web server (nginx/Apache) to proxy requests to the Flask app
2. Use a WSGI server like Gunicorn: `gunicorn -w 4 -b 0.0.0.0:5000 app:app`
3. Set up SSL certificates for HTTPS
4. Configure environment variables for production Gmail API credentials

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