django-react-app/
├─ .github/
│  ├─ workflows/
│  │  ├─ ci.yml
│  │  └─ cd.yml
│  ├─ PULL_REQUEST_TEMPLATE.md
│  └─ copilot-instructions.md
│
├─ backend/
│  ├─ manage.py
│  ├─ pyproject.toml                  # poetry (recommended) OR requirements/*.txt
│  ├─ poetry.lock
│  ├─ requirements/
│  │  ├─ base.txt
│  │  ├─ dev.txt
│  │  └─ prod.txt
│  │
│  ├─ config/                         # Django "project" (settings/urls/asgi/wsgi)
│  │  ├─ __init__.py
│  │  ├─ asgi.py
│  │  ├─ wsgi.py
│  │  ├─ urls.py
│  │  └─ settings/
│  │     ├─ __init__.py
│  │     ├─ base.py
│  │     ├─ dev.py
│  │     ├─ prod.py
│  │     └─ test.py
│  │
│  ├─ apps/                           # all domain apps live here
│  │  ├─ users/
│  │  │  ├─ migrations/
│  │  │  ├─ __init__.py
│  │  │  ├─ admin.py
│  │  │  ├─ apps.py
│  │  │  ├─ models.py
│  │  │  ├─ selectors.py              # read queries (optional but clean)
│  │  │  ├─ services.py               # business logic
│  │  │  ├─ serializers.py            # DRF
│  │  │  ├─ views.py                  # DRF
│  │  │  ├─ urls.py
│  │  │  └─ tests/
│  │  └─ ... (payments, issues, etc.)
│  │
│  ├─ common/                         # shared utils
│  │  ├─ __init__.py
│  │  ├─ auth/
│  │  ├─ permissions/
│  │  ├─ pagination.py
│  │  ├─ exceptions.py
│  │  ├─ middleware.py
│  │  ├─ logging.py
│  │  └─ utils.py
│  │
│  ├─ api/                            # API router / versioning
│  │  ├─ __init__.py
│  │  ├─ urls.py                      # /api/v1/ includes apps urls
│  │  └─ v1/
│  │     ├─ __init__.py
│  │     └─ urls.py
│  │
│  ├─ static/                         # optional (mostly for admin)
│  ├─ media/                          # local dev uploads (gitignored)
│  ├─ locale/                         # i18n if needed
│  ├─ scripts/                        # dev scripts, seed data, etc.
│  └─ tests/                          # integration/e2e backend tests
│
├─ frontend/
│  ├─ package.json
│  ├─ package-lock.json / pnpm-lock.yaml / yarn.lock
│  ├─ vite.config.ts                  # or CRA/Next config
│  ├─ tsconfig.json
│  ├─ .env.example
│  ├─ public/
│  └─ src/
│     ├─ app/                         # app bootstrap
│     │  ├─ App.tsx
│     │  ├─ main.tsx
│     │  └─ routes.tsx
│     ├─ api/                         # API clients
│     │  ├─ http.ts                   # axios/fetch wrapper
│     │  ├─ endpoints.ts
│     │  └─ types.ts
│     ├─ components/                  # reusable components
│     ├─ features/                    # feature-based modules (recommended)
│     │  ├─ auth/
│     │  ├─ issues/
│     │  └─ ...
│     ├─ hooks/
│     ├─ layouts/
│     ├─ pages/                       # if not using feature routing
│     ├─ store/                       # redux/zustand
│     ├─ styles/
│     ├─ utils/
│     └─ tests/
│
├─ infra/
│  ├─ docker/
│  │  ├─ backend.Dockerfile
│  │  ├─ frontend.Dockerfile
│  │  └─ nginx.conf
│  ├─ docker-compose.yml
│  └─ k8s/                            # optional
│
├─ docs/
│  ├─ architecture.md
│  ├─ api.md
│  └─ decisions/                      # ADRs
│
├─ .env.example
├─ .gitignore
├─ Makefile                           # helpful: dev commands
└─ README.md
