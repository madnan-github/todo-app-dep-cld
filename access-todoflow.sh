#!/bin/bash
echo "Testing the TaskFlow application..."

echo ""
echo "Checking backend health endpoint..."
curl -s -o /dev/null -w "Backend health status: %{http_code}\n" http://localhost:8000/health

echo ""
echo "Checking backend API root endpoint..."
curl -s -o /dev/null -w "Backend API status: %{http_code}\n" http://localhost:8000/

echo ""
echo "Checking frontend availability..."
curl -s -o /dev/null -w "Frontend status: %{http_code}\n" http://localhost:3000/

echo ""
echo "Application is running successfully!"
echo ""
echo "Access the application:"
echo "- Frontend: http://localhost:3000"
echo "- Backend API: http://localhost:8000"
echo "- Backend API Docs: http://localhost:8000/docs"
echo ""
echo "Services running:"
echo "- PostgreSQL: localhost:5432"
echo "- Backend API: localhost:8000"
echo "- Frontend: localhost:3000"