# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

FormAPI is a Flask-based contact form API that accepts form submissions and forwards them via Gmail API. The application is designed for deployment as a containerized service behind a reverse proxy (nginx).

## Development Commands

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Set up Gmail API authentication (run once)
python setup_auth.py

# Run development server
python app.py

# Test the API locally
python test_email.py
```

### Docker Development
```bash
# Build and run with Docker Compose
docker-compose up -d

# Or build and run manually
docker build -t formapi .
docker run -d -p 5000:5000 formapi

# Test production deployment
python test_production.py
```

## Architecture

### Core Components

- **app.py**: Main Flask application with two endpoints:
  - `POST /api/contact`: Accepts form submissions and sends emails
  - `GET /health`: Health check endpoint

- **Gmail API Integration**: Uses Google OAuth2 for authentication with two modes:
  - Local development: Uses `token.json` file created by `setup_auth.py`
  - Production: Uses default credentials from Google Cloud environment

### Authentication Flow

The application handles Gmail API credentials through `get_gmail_credentials()` in app.py:63:
1. Attempts to load local `token.json` for development
2. Falls back to `google.auth.default()` for production deployment
3. Automatically refreshes expired tokens when possible

### Email Processing

Form submissions are processed in `send_form_email()` in app.py:39:
- Creates formatted email with sender info and form data
- Sets Reply-To header to form submitter's email
- Sends to hardcoded recipient: `guillaumegenois031@gmail.com`

### Container Configuration

- Uses Python 3.11-slim base image
- Runs as non-root user for security
- Uses Gunicorn with 4 workers in production
- Health check endpoint configured for container orchestration

## File Structure

- `app.py`: Main application logic
- `setup_auth.py`: OAuth2 setup for local development
- `test_email.py`: Local API testing script
- `test_production.py`: Production deployment testing
- `sendMessage.py` / `createMessage.py`: Gmail API examples (not used by main app)
- `credentials.json`: OAuth2 client credentials (not committed)
- `token.json`: Generated user credentials (not committed)

## Testing

The project includes test scripts for both environments:
- Local testing: `python test_email.py` (tests localhost:5000)
- Production testing: `python test_production.py` (tests production URL)

Both scripts test the contact form endpoint with sample data and verify responses.