You are GitHub Copilot acting as a senior full-stack engineer. Generate a complete, production-grade, Jira-like Issue Tracker with Django + DRF backend and React frontend.

The project MUST:
- Run locally using Docker (default path)
- ALSO be runnable without Docker for development
- Follow the exact repository standards defined in:
  - copilot-instructions.md
  - folderStructure.mc
Do NOT invent a different structure. If something is missing, infer minimally.

==================================================
1) TECH STACK (MANDATORY)
==================================================
Backend:
- Python 3.11
- Django 5.x
- Django REST Framework
- PostgreSQL 15+
- Redis 7+
- Celery (worker + beat)
- django-filter
- drf-spectacular (OpenAPI)
- simplejwt (JWT auth)
- django-cors-headers
- django-storages (local filesystem for dev, S3-ready interface)
- Postgres Full-Text Search (FTS)

Frontend:
- Node 20
- React 18 + Vite
- TypeScript
- React Router
- TanStack Query
- react-hook-form + zod
- @dnd-kit for Kanban drag/drop
- TailwindCSS + shadcn/ui
- Clean, subtle, enterprise UI (neutral palette, consistent spacing)

==================================================
2) DOCKER (MANDATORY – NOT OPTIONAL)
==================================================
Provide FULL Docker support.

Create:
- Dockerfile.backend
- Dockerfile.frontend
- docker-compose.yml

docker-compose MUST include:
- backend (Django + Gunicorn)
- frontend (Vite dev server)
- postgres
- redis
- celery-worker
- celery-beat

Docker rules:
- Backend uses Gunicorn inside container
- Frontend runs Vite in dev mode
- Volumes mounted for hot reload
- Healthchecks for postgres and redis
- Backend waits for DB before migrate
- One command should bring everything up:
  docker compose up --build

Also provide:
- .env.example (backend)
- .env.frontend.example
- Proper separation of env vars
- Media + static volume handling

==================================================
3) BUSINESS REQUIREMENTS
==================================================
Build a Jira-like Issue Tracker with:

Core features:
- Projects, Boards, Sprints, Epics, Issues
- Custom workflow per project (states + transitions)
- Comments, Attachments, Watchers, Mentions (@username)
- Notifications: in-app + email (console backend)
- Full-text search + filters + saved views
- Activity feed per project and per issue

Backend architecture:
- Domain models:
  Issue, Sprint, Workflow, WorkflowState, WorkflowTransition, Event
- Permission system:
  - Project roles: Owner, Admin, Member, Viewer
  - Issue visibility: project-wide or restricted
- Event-driven notifications using Outbox pattern:
  - Persist Event
  - Persist OutboxMessage
  - Celery processes outbox and creates Notifications
- Async tasks:
  - notification dispatch
  - search index updates
  - daily digest (scaffold)
- Optimized queries:
  - pagination
  - select_related / prefetch_related
  - no N+1 in serializers
- Optional WebSockets scaffold using Django Channels

==================================================
4) FRONTEND REQUIREMENTS
==================================================
Pages:
1) Auth (Login / Register)
2) Projects list + create
3) Project detail:
   - Kanban Board
   - Backlog / Sprint planning
   - Issues list
   - Activity feed
   - Settings (workflow)
4) Kanban board with drag/drop respecting transitions
5) Sprint planning view
6) Issue detail page:
   - metadata
   - comments
   - attachments
   - watchers
   - history timeline
7) Search page:
   - query
   - filters
   - saved views
8) Notification center

Frontend rules:
- Centralized API client
- TanStack Query hooks per domain
- Loading, empty, error states
- Toast notifications
- Consistent UI components
- No inline fetch calls

==================================================
5) DATA MODELS (MINIMUM REQUIRED)
==================================================
Must include:
- Project
- ProjectMembership
- Board
- Sprint
- Epic
- Workflow
- WorkflowState
- WorkflowTransition
- Issue
- Comment
- Attachment
- Watcher
- Event
- OutboxMessage
- Notification

Requirements:
- Issue key generation (PROJ-123) per project
- Transaction-safe
- Workflow transition validation enforced at API level

==================================================
6) API REQUIREMENTS
==================================================
JWT-protected DRF APIs:

Auth:
- /auth/register
- /auth/login
- /auth/me

Core:
- /projects (CRUD)
- /projects/:id/members
- /projects/:id/boards
- /sprints
- /epics
- /issues (list + filters + FTS search)
- /issues/:id
- /issues/:id/comments
- /issues/:id/attachments
- /issues/:id/watchers
- /issues/:id/transitions
- /notifications
- /activity/projects/:id
- /activity/issues/:id

Docs:
- /api/schema/
- /api/docs/

==================================================
7) DJANGO ADMIN (MANDATORY)
==================================================
Admin must be usable:
- Proper list_display, filters, search
- Inline workflow states and transitions
- Readable labels and ordering
- Autocomplete for relations
- Event + Notification visibility

==================================================
8) SEEDING, TESTS, QUALITY
==================================================
Provide:
- Migrations
- Seed command:
  - demo users
  - demo project
  - workflow with states + transitions
  - sprint + epic + issues
- Unit tests:
  - workflow transitions
  - issue key generation
  - permissions and restricted visibility

Linting:
- Backend: ruff + black (or as per copilot-instructions.md)
- Frontend: eslint + prettier

==================================================
9) README (MANDATORY)
==================================================
README must include:
- Docker-based setup (PRIMARY)
- Non-docker local setup (SECONDARY)
- Env configuration
- Running migrations
- Running Celery
- Seeding demo data
- Accessing frontend and backend

==================================================
10) OUTPUT RULES
==================================================
- Generate full file contents (no placeholders)
- Respect folderStructure.mc strictly
- Scaffold bonus features cleanly with TODOs if not fully implemented
- Ensure project runs end-to-end via Docker

This project should reflect senior-level architecture and production-grade standards.
