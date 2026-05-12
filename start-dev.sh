#!/bin/bash

# SyncType Development Startup Script
# This script starts both backend and frontend in separate terminal tabs/windows

echo "🚀 Starting SyncType Development Environment..."
echo ""

# Color codes
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if we're in the right directory
if [ ! -d "backend" ] || [ ! -d "frontend" ]; then
    echo "❌ Error: Please run this script from the synctype-integrated directory"
    exit 1
fi

echo "${BLUE}📦 Starting Backend (FastAPI)...${NC}"
echo "Backend will run on http://localhost:8000"
echo ""

# Start backend in background
cd backend
if [ ! -d ".venv" ]; then
    echo "${YELLOW}⚠️  Virtual environment not found. Creating one...${NC}"
    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
else
    source .venv/bin/activate
fi

# Start backend server in background
uvicorn main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!
cd ..

echo "${GREEN}✓ Backend started (PID: $BACKEND_PID)${NC}"
echo ""

# Wait a bit for backend to start
sleep 2

echo "${BLUE}🎨 Starting Frontend (Vite + React)...${NC}"
echo "Frontend will run on http://localhost:5173"
echo ""

# Start frontend
cd frontend
if [ ! -d "node_modules" ]; then
    echo "${YELLOW}⚠️  Node modules not found. Installing...${NC}"
    npm install
fi

npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "${GREEN}✓ Frontend started (PID: $FRONTEND_PID)${NC}"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "${GREEN}✨ SyncType is running!${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "🔗 Backend API: ${BLUE}http://localhost:8000${NC}"
echo "🔗 Frontend UI: ${BLUE}http://localhost:5173${NC}"
echo "📚 API Docs:    ${BLUE}http://localhost:8000/docs${NC}"
echo ""
echo "Press ${YELLOW}Ctrl+C${NC} to stop both servers"
echo ""

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "${YELLOW}🛑 Stopping servers...${NC}"
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    echo "${GREEN}✓ Servers stopped${NC}"
    exit 0
}

# Trap Ctrl+C and call cleanup
trap cleanup INT TERM

# Wait for both processes
wait $BACKEND_PID $FRONTEND_PID
