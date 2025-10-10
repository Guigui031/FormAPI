#!/bin/bash
# Manual Docker run for troubleshooting

# Stop any existing container
sudo docker stop formapi 2>/dev/null || true
sudo docker rm formapi 2>/dev/null || true

# Build the image
sudo docker build -t formapi .

# Run the container
sudo docker run -d \
  --name formapi \
  -p 5000:5000 \
  --restart unless-stopped \
  -v $(pwd)/token.json:/app/token.json:ro \
  formapi

# Check if it's running
sudo docker ps | grep formapi
sudo docker logs formapi

echo "Test with: curl http://localhost:5000/health"