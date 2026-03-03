#!/usr/bin/env bash
set -euo pipefail

# Start both backend (FastAPI) and frontend (Next.js) in the background
# Creates pids/ and logs/ directories and writes PID files for later termination
# Usage: ./scripts/start_service.sh

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")"/.. && pwd)"
LOG_DIR="$ROOT_DIR/logs"
PID_DIR="$LOG_DIR/pids"
mkdir -p "$LOG_DIR" "$PID_DIR"

echo "============================================================"
echo "  Starting GenMentor - Full Stack"
echo "============================================================"
echo ""

# --- Backend (FastAPI) ---
echo "[1/2] Starting backend (FastAPI)..."
(
  cd "$ROOT_DIR/apps/backend"
  if [[ -f .env ]]; then
    set -a
    # shellcheck disable=SC1091
    source .env
    set +a
  fi
  BACKEND_PORT="${BACKEND_PORT:-5000}"

  # Kill any existing process on the backend port
  lsof -ti:${BACKEND_PORT} | xargs kill -9 2>/dev/null || true

  echo "  -> Backend starting on port ${BACKEND_PORT}..."
  nohup python main.py \
    >"$LOG_DIR/backend.log" 2>&1 &
  echo $! >"$PID_DIR/backend.pid"
  echo "  Backend PID: $(cat "$PID_DIR/backend.pid")"
  echo "  Backend URL: http://127.0.0.1:${BACKEND_PORT}"
  echo "  API Docs: http://127.0.0.1:${BACKEND_PORT}/docs"
)

# Wait a bit for backend to start
sleep 2

# --- Frontend (Next.js) ---
echo ""
echo "[2/2] Starting frontend (Next.js)..."
(
  cd "$ROOT_DIR/apps/frontend"
  FRONTEND_PORT="${FRONTEND_PORT:-3000}"

  # Kill any existing process on the frontend port
  lsof -ti:${FRONTEND_PORT} | xargs kill -9 2>/dev/null || true

  # Clean up any stale lock files
  rm -f .next/dev/lock 2>/dev/null || true

  echo "  -> Frontend starting on port ${FRONTEND_PORT}..."
  nohup npm run dev -- --port "${FRONTEND_PORT}" \
    >"$LOG_DIR/frontend.log" 2>&1 &
  echo $! >"$PID_DIR/frontend.pid"
  echo "  Frontend PID: $(cat "$PID_DIR/frontend.pid")"
  echo "  Frontend URL: http://localhost:${FRONTEND_PORT}"
)

# Wait for frontend to start
sleep 3

echo ""
echo "============================================================"
echo "  GenMentor Started Successfully!"
echo "============================================================"
echo ""
echo "  Frontend:  http://localhost:${FRONTEND_PORT:-3000}"
echo "  Backend:   http://127.0.0.1:${BACKEND_PORT:-5000}"
echo "  API Docs:  http://127.0.0.1:${BACKEND_PORT:-5000}/docs"
echo ""
echo "  Logs:      $LOG_DIR/"
echo "  PIDs:      $PID_DIR/"
echo ""
echo "  To stop: ./scripts/stop_service.sh"
echo "  To view logs: tail -f $LOG_DIR/backend.log"
echo "               tail -f $LOG_DIR/frontend.log"
echo "============================================================"
echo ""
