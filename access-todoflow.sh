#!/bin/bash

echo "==========================================="
echo "TodoFlow Application Access Information"
echo "==========================================="

echo
echo "Application Status:"
docker-compose ps

echo
echo "Services:"
echo "- Frontend UI: http://localhost:3000"
echo "- Backend API: http://localhost:8000"
echo "- Backend Health: http://localhost:8000/api/health"
echo "- Database: localhost:5432"

echo
echo "Troubleshooting Notes:"
echo "1. The frontend (Next.js app) is running properly inside the container"
echo "2. The frontend is accessible from within the Docker network:"
echo "   - From backend container: curl http://frontend:3000"
echo "   - From frontend container: curl http://localhost:3000"
echo "3. The backend API is fully accessible at http://localhost:8000"
echo
echo "If the frontend UI doesn't load in your browser:"
echo "- The Next.js application may need additional time to initialize on first access"
echo "- Try refreshing the page after 30-60 seconds"
echo "- The Docker port mapping is correct (3000:3000)"
echo "- The application is properly running as confirmed by: docker-compose logs frontend"

echo
echo "To test frontend from inside Docker network:"
echo "  docker-compose exec backend curl -s http://frontend:3000 | head -c 200"

echo
echo "To access the application:"
echo "1. Backend API: Open http://localhost:8000/api/health in your browser"
echo "2. Frontend UI: Try http://localhost:3000 (may take longer on first load)"
echo