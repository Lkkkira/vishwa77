# Free Render deployment

Deploy the React/Vite frontend and FastAPI/SQLite backend together as one Docker Web Service. The root Streamlit `app.py` and `vercel.json` are alternative entry points and are not used by this deployment.

## Settings

| Setting | Value |
| --- | --- |
| Runtime | Docker |
| Instance type | Free |
| Root directory | Repository root (leave blank) |
| Dockerfile | `./Dockerfile` |
| Docker context | `.` |
| Build | Dockerfile builds React with `npm ci` and `npm run build`, then installs `backend/requirements.txt` |
| Start | Keep Dockerfile default: `python -m uvicorn backend.app.main:app --host 0.0.0.0 --port ${PORT:-8000}` |
| Health check | `/api/health` |
| `PORT` | `8000` |
| `FILEPILOT_DB_PATH` | `/app/workspace/filepilot.db` |
| `FILEPILOT_WORKSPACE` | `/app/workspace` |
| `PYTHONUNBUFFERED` | `1` |

No API keys, external database, frontend API URL, paid disk, or custom domain are required. The frontend calls `/api` on the same service. `render.yaml` captures these settings for a Blueprint deployment.

## Free-plan behavior

Render Free services sleep after 15 minutes without traffic and take time to wake up. SQLite data and uploaded/generated files are ephemeral: they are lost on spin-down, restart, or redeploy. Download organized results before leaving. This configuration is appropriate for a temporary demo, not durable storage.

The application currently has one shared workspace and no user authentication. Everyone with the live URL can access jobs and files; use non-sensitive test archives.

Keep the service on Free and do not add paid resources. Accounts with payment methods can incur usage overages; review workspace billing and spending controls to preserve a zero-cost setup. See [Render Free service limits](https://render.com/docs/free).

## Validation

Run `npm ci` and `npm run build` in `frontend`, then install `backend/requirements.txt` and run `python -m pytest backend/tests -q` from the repository root. Building first enables the deployment regression tests for the homepage, built JavaScript, frontend route fallback, API routing, and static-file boundary.
