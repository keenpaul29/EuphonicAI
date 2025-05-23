#!/bin/bash

# Deployment script for Moodify

# Navigate to project directory
cd /path/to/moodify

# Pull latest changes
git pull origin main

# Backend setup
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate  # If using Django or similar
deactivate

# Frontend setup
cd ../frontend
npm install
npm run build

# Restart services
sudo systemctl restart moodify-backend
sudo systemctl restart moodify-frontend

# Optional: Cleanup
npm prune --production

echo "Deployment completed successfully!"
