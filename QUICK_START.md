# GenMentor Quick Start Guide

## Start the Application

```bash
# Start both backend and frontend
./scripts/start_all.sh

# Or start individually in separate terminals
./scripts/start_backend.sh   # Terminal 1
./scripts/start_frontend.sh  # Terminal 2
```

## Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://127.0.0.1:5000
- **API Docs**: http://127.0.0.1:5000/docs

## Stop the Application

```bash
./scripts/stop_all.sh
```

## View Logs

```bash
# Backend logs
tail -f logs/backend.log

# Frontend logs
tail -f logs/frontend.log

# Both logs
tail -f logs/*.log
```

## Check Health

```bash
# Backend
curl http://127.0.0.1:5000/api/v1/health

# Frontend
curl -I http://localhost:3000
```

## Common Issues

### Port already in use
```bash
# Kill process on port 5000 (backend)
lsof -ti:5000 | xargs kill -9

# Kill process on port 3000 (frontend)
lsof -ti:3000 | xargs kill -9
```

### Next.js lock file error
```bash
rm -f apps/frontend/.next/dev/lock
```

### Clear caches
```bash
# Frontend
cd apps/frontend && rm -rf .next && npm install

# Backend
cd apps/backend && rm -rf __pycache__ && pip install -r requirements.txt
```

## Development Workflow

1. Start services: `./scripts/start_all.sh`
2. Open browser: http://localhost:3000
3. Make code changes (auto-reload enabled)
4. View logs: `tail -f logs/*.log`
5. Stop services: `./scripts/stop_all.sh`

## Environment Setup

### Backend (.env)
```bash
cd apps/backend
cp .env.example .env
# Edit .env with your API keys
```

### Frontend (.env.local)
```bash
cd apps/frontend
echo "NEXT_PUBLIC_API_URL=http://localhost:5000/api/v1" > .env.local
```

## Full Documentation

- [Scripts Documentation](./SCRIPTS_DOCUMENTATION.md)
- [Frontend Integration](./FRONTEND_INTEGRATION_COMPLETE.md)
- [Workspace Memory](./WORKSPACE_MEMORY.md)
- [API Documentation](http://127.0.0.1:5000/docs) (requires backend running)
