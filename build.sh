#!/bin/bash

set -o errexit

pip install -r requirements.txt

echo "💡 Collecting static files..."
python manage.py collectstatic --no-input

echo "🔄 Applying migrations..."
python manage.py migrate

echo "✅ Build complete!"