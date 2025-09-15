# Service Account Setup for Production

## Create Service Account in Google Cloud Console:

1. Go to Google Cloud Console → "IAM & Admin" → "Service Accounts"
2. Click "Create Service Account"
3. Name: "formapi-service"
4. Click "Create and Continue"
5. Skip roles → Click "Done"

## Enable Domain-wide Delegation (if sending from different email):

1. Click on the service account
2. Go to "Details" tab
3. Check "Enable Google Workspace Domain-wide Delegation"
4. Save

## Download Service Account Key:

1. Go to "Keys" tab
2. Click "Add Key" → "Create New Key"
3. Choose "JSON"
4. Download the file as `service-account.json`

## Upload to Server:

```bash
scp service-account.json your-username@your-server:/var/www/FormAPI/
```

## Update docker-compose.yml for Service Account:

```yaml
services:
  formapi:
    build: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
      - GOOGLE_APPLICATION_CREDENTIALS=/app/service-account.json
    volumes:
      - ./service-account.json:/app/service-account.json:ro
    restart: unless-stopped
```