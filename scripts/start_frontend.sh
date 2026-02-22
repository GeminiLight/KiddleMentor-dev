#!/usr/bin/env bash
set -euo pipefail

# Start the Next.js frontend in the foreground
# Usage: ./scripts/start_frontend.sh [PORT]

# Resolve repo root (one level up from this script dir)
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")"/.. && pwd)"
cd "$ROOT_DIR/apps/frontend"

PORT="${1:-${FRONTEND_PORT:-3000}}"

echo "Starting frontend (Next.js) on port ${PORT}..."
echo "Frontend will be available at: http://localhost:${PORT}"

# Clean up any stale lock files
rm -f .next/dev/lock 2>/dev/null || true

# Start Next.js dev server
exec npm run dev -- --port "${PORT}"
