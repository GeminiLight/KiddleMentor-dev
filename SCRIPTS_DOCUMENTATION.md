# Scripts Documentation

This document describes all the startup and shutdown scripts for the GenMentor project.

## Overview

The GenMentor project consists of two main services:
- **Backend**: FastAPI application running on port 5000 (default)
- **Frontend**: Next.js application running on port 3000 (default)

## Available Scripts

### 1. `scripts/start_all.sh`

Starts both backend and frontend services in the background with proper process management.

**Usage:**
```bash
./scripts/start_all.sh
```

**Features:**
- Creates `logs/` and `pids/` directories for process management
- Kills any existing processes on the target ports
- Starts backend (FastAPI) on port 5000 (configurable via `BACKEND_PORT`)
- Starts frontend (Next.js) on port 3000 (configurable via `FRONTEND_PORT`)
- Writes PID files to `pids/` for later termination
- Writes logs to `logs/backend.log` and `logs/frontend.log`
- Cleans up stale Next.js lock files

**Environment Variables:**
- `BACKEND_PORT`: Backend server port (default: 5000)
- `FRONTEND_PORT`: Frontend server port (default: 3000)

**Output:**
```
============================================================
  Starting GenMentor - Full Stack
============================================================

[1/2] Starting backend (FastAPI)...
  → Backend starting on port 5000...
  ✓ Backend PID: 12345
  ✓ Backend URL: http://127.0.0.1:5000
  ✓ API Docs: http://127.0.0.1:5000/docs

[2/2] Starting frontend (Next.js)...
  → Frontend starting on port 3000...
  ✓ Frontend PID: 12346
  ✓ Frontend URL: http://localhost:3000

============================================================
  GenMentor Started Successfully!
============================================================

  🚀 Frontend:  http://localhost:3000
  🔧 Backend:   http://127.0.0.1:5000
  📚 API Docs:  http://127.0.0.1:5000/docs

  📁 Logs:      /path/to/gen-mentor/logs/
  📝 PIDs:      /path/to/gen-mentor/pids/

  To stop: ./scripts/stop_all.sh
  To view logs: tail -f logs/backend.log
               tail -f logs/frontend.log
============================================================
```

### 2. `scripts/stop_all.sh`

Stops all running GenMentor services by reading PID files.

**Usage:**
```bash
./scripts/stop_all.sh
```

**Features:**
- Reads PID files from `pids/` directory
- Attempts graceful shutdown with SIGTERM
- Waits up to 10 seconds for each process to exit
- Falls back to SIGKILL if graceful shutdown fails
- Removes PID files after stopping processes
- Handles missing or stale PID files gracefully

**Output:**
```
Stopping backend (pid 12345)...
backend stopped.
Stopping frontend (pid 12346)...
frontend stopped.
All services stopped.
```

### 3. `scripts/start_backend.sh`

Starts only the backend service in the foreground (useful for development).

**Usage:**
```bash
./scripts/start_backend.sh [PORT]
```

**Parameters:**
- `PORT` (optional): Port number to use (default: 5000 or `$BACKEND_PORT`)

**Features:**
- Loads environment variables from `apps/backend/.env` if present
- Starts FastAPI with uvicorn in reload mode (auto-restart on code changes)
- Runs in foreground (logs to stdout)

**Example:**
```bash
# Start with default port (5000)
./scripts/start_backend.sh

# Start on custom port
./scripts/start_backend.sh 8000
```

### 4. `scripts/start_frontend.sh`

Starts only the frontend service in the foreground (useful for development).

**Usage:**
```bash
./scripts/start_frontend.sh [PORT]
```

**Parameters:**
- `PORT` (optional): Port number to use (default: 3000 or `$FRONTEND_PORT`)

**Features:**
- Cleans up stale Next.js lock files
- Starts Next.js dev server with Turbopack
- Runs in foreground (logs to stdout)

**Example:**
```bash
# Start with default port (3000)
./scripts/start_frontend.sh

# Start on custom port
./scripts/start_frontend.sh 3001
```

## Common Workflows

### Development Workflow (Foreground)

When developing, you typically want to run services in separate terminals to see logs in real-time:

**Terminal 1 - Backend:**
```bash
./scripts/start_backend.sh
```

**Terminal 2 - Frontend:**
```bash
./scripts/start_frontend.sh
```

Press `Ctrl+C` in each terminal to stop the services.

### Production-like Workflow (Background)

For testing the full stack or running in the background:

**Start all services:**
```bash
./scripts/start_all.sh
```

**View logs:**
```bash
# Backend logs
tail -f logs/backend.log

# Frontend logs
tail -f logs/frontend.log

# Both logs simultaneously
tail -f logs/*.log
```

**Stop all services:**
```bash
./scripts/stop_all.sh
```

## Port Conflicts

If you see errors about ports being in use:

**Backend port conflict (5000):**
```bash
# Find and kill process using port 5000
lsof -ti:5000 | xargs kill -9
```

**Frontend port conflict (3000):**
```bash
# Find and kill process using port 3000
lsof -ti:3000 | xargs kill -9
```

The `start_all.sh` script automatically handles port conflicts by killing existing processes on the target ports.

## Next.js Lock File Issues

If you see this error:
```
⨯ Unable to acquire lock at .next/dev/lock, is another instance of next dev running?
```

**Solution:**
```bash
rm -f apps/frontend/.next/dev/lock
```

The `start_all.sh` and `start_frontend.sh` scripts automatically clean up stale lock files.

## Environment Variables

### Backend (.env in apps/backend/)

Create a `.env` file in `apps/backend/` for backend configuration:

```env
BACKEND_PORT=5000
DEBUG=True
ENVIRONMENT=dev
STORAGE_MODE=local
WORKSPACE_BASE=~/.gen-mentor/workspace

# LLM Configuration
DEFAULT_LLM_PROVIDER=deepseek
DEFAULT_LLM_MODEL=deepseek-chat
DEEPSEEK_API_KEY=your_api_key_here
```

### Frontend (.env.local in apps/frontend/)

Create a `.env.local` file in `apps/frontend/` for frontend configuration:

```env
NEXT_PUBLIC_API_URL=http://localhost:5000/api/v1
FRONTEND_PORT=3000
```

## Troubleshooting

### Backend won't start

1. Check if Python dependencies are installed:
   ```bash
   cd apps/backend
   pip install -r requirements.txt
   ```

2. Check if port 5000 is available:
   ```bash
   lsof -i:5000
   ```

3. Check backend logs:
   ```bash
   tail -f logs/backend.log
   ```

### Frontend won't start

1. Check if Node.js dependencies are installed:
   ```bash
   cd apps/frontend
   npm install
   ```

2. Check if port 3000 is available:
   ```bash
   lsof -i:3000
   ```

3. Check frontend logs:
   ```bash
   tail -f logs/frontend.log
   ```

4. Clear Next.js cache:
   ```bash
   cd apps/frontend
   rm -rf .next
   ```

### Services won't stop

If `stop_all.sh` doesn't work:

```bash
# Force kill all processes
lsof -ti:5000 | xargs kill -9  # Backend
lsof -ti:3000 | xargs kill -9  # Frontend

# Remove PID files
rm -f pids/*.pid
```

## Health Checks

### Backend Health Check

```bash
curl http://127.0.0.1:5000/api/v1/health
```

Expected response:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2026-02-22T18:08:33.417958"
}
```

### Frontend Health Check

```bash
curl -I http://localhost:3000
```

Expected response:
```
HTTP/1.1 200 OK
```

## API Documentation

Once the backend is running, you can access the interactive API documentation at:

- **Swagger UI**: http://127.0.0.1:5000/docs
- **ReDoc**: http://127.0.0.1:5000/redoc

## Next Steps

After starting the services:

1. **Access the frontend**: http://localhost:3000
2. **Click "Start Learning Locally"**: Initializes a new learner session
3. **Complete onboarding**: Set learning goal, provide background info
4. **View dashboard**: See personalized learning path and resources

## Script Maintenance

All scripts are located in the `scripts/` directory and follow these conventions:

- Use `#!/usr/bin/env bash` shebang
- Set `set -euo pipefail` for safety
- Resolve repository root dynamically
- Handle errors gracefully
- Provide clear output messages
- Are executable (`chmod +x`)

### Making scripts executable

If you need to make scripts executable:

```bash
chmod +x scripts/*.sh
```

## Related Documentation

- [Frontend Integration](./FRONTEND_INTEGRATION_COMPLETE.md)
- [Backend API](./apps/backend/README.md)
- [Workspace Memory](./WORKSPACE_MEMORY.md)
- [Configuration](./apps/backend/config/README.md)
