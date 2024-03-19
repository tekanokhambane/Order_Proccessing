#!/bin/bash

# Move to the client-side directory
cd frontend

# Install dependencies
#npm install

# Build the React app
echo "building..."
npm run build 


echo "copying..."
rm -r ../products/static/products/

mkdir ../products/static/products/

cp -r dist/static/products/* ../products/static/products/

cd ..

# cd editor
# npm run build

# rm -r ../admin/static/editor
# mkdir ../admin/static/editor/
# cp -r dist/static/* ../admin/static/editor/

# cd ..

echo "collecting..."

export $(grep -v '^#' .env | xargs)
python3 manage.py collectstatic --noinput

# Apply database migrations
echo "migrating..."
python3 manage.py migrate

# Run collectstatic

echo "done..."


# Start the Gunicorn server
# exec gunicorn --bind 0.0.0.0:$PORT --workers 1 --threads 8 --timeout 0 flexibuilder.wsgi:application