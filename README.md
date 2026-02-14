# IssuePilot

> **Production-grade Jira-like Issue Tracker** with Django REST Framework + React + PostgreSQL

A comprehensive issue tracking system featuring custom workflows, real-time notifications, full-text search, Kanban boards with drag-and-drop, and enterprise-grade architecture.

![IssuePilot](https://img.shields.io/badge/Django-5.0-092E20?logo=django)
![React](https://img.shields.io/badge/React-18.2-61DAFB?logo=react)
![TypeScript](https://img.shields.io/badge/TypeScript-5.0-3178C6?logo=typescript)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791?logo=postgresql)
![License](https://img.shields.io/badge/license-MIT-green)

## 📸 Screenshots

### Projects Dashboard
Modern project management interface with gradient cards, hover animations, and real-time statistics.

### Kanban Board
Drag-and-drop issue management with visual workflow states, optimistic updates, and smooth transitions.

### Issue Detail Page
Comprehensive issue view with inline editing, comments, watchers, state transitions, and activity tracking.

### Search & Filters
Full-text search across all projects with advanced filtering by type, priority, status, and project.

### Notifications Center
Real-time notification system with unread badges, type-specific icons, and direct navigation to related issues.

### Activity Feed
Timeline of all project events with actor information, timestamps, and contextual icons.

### Dark Mode
Complete dark theme support with smooth transitions and persistent preference storage.

## ✨ Features

### Core Features
- **Multi-Project Management** - Organize work across multiple projects with team access control
- **Custom Workflows** - Define states and transitions per project with visual Kanban boards
- **Drag-and-Drop Kanban** - Intuitive issue management with real-time state transitions
- **Agile Support** - Sprints, epics, story points, and backlog management
- **Issue Types** - Tasks, bugs, stories, and epics with type-specific icons
- **Advanced Search** - Full-text search with filters for project, type, priority, and status
- **Comments & Attachments** - Rich collaboration with inline editing and file uploads
- **Watchers & Mentions** - Stay updated on relevant issues with notification system
- **Activity Feed** - Track all project and issue changes with detailed event timeline
- **Real-time Notifications** - Unread badges, type-specific icons, and mark as read functionality
- **Theme Toggle** - Light/Dark mode with smooth transitions and localStorage persistence
- **Project Settings** - Edit project details, manage members, and danger zone actions

### Technical Features
- **JWT Authentication** - Secure token-based auth with refresh tokens
- **Role-Based Access** - Project owners, admins, members, viewers with granular permissions
- **Event-Driven Notifications** - Outbox pattern for reliable delivery
- **Celery Background Jobs** - Async notification processing with beat scheduler
- **OpenAPI Documentation** - Auto-generated API docs with Swagger UI
- **Docker Support** - Full containerization for easy deployment
- **Production Ready** - Comprehensive error handling, logging, pagination, and optimistic updates
- **TypeScript Frontend** - Type-safe API client with TanStack Query for state management
- **Responsive Design** - Mobile-first design with TailwindCSS and shadcn/ui components

## 🎯 Pages & Features

### 1. **Projects Page** (`/projects`)
Your central hub for all projects with a clean, modern interface.

**Features:**
- Grid layout with gradient project cards
- Hover animations with scale effects and shadows
- Create new project dialog with name, key, icon, and description
- Project key auto-generation from name
- Member count and creation date display
- Direct navigation to project details
- Smooth transitions and lift animations

**UI Elements:**
- Gradient backgrounds (gray/blue tones)
- Icon hover scale effect (1.1x)
- Border highlights on hover
- Badge styling for project keys

### 2. **Project Detail Page** (`/projects/:id`)
Comprehensive project overview with multiple tabs.

**Features:**
- **Issues Tab**: List all project issues with create dialog
  - Border-left accent on issue cards
  - Smooth hover transitions
  - Badge-enhanced priority and type indicators
  - Click to navigate to issue details
  - Create issue with type, priority, assignee selection
  
- **Board Tab**: Quick link to Kanban board view
  
- **Activity Tab**: Timeline of recent project events
  - Event-specific icons (create, update, comment, state change)
  - Actor information with avatars
  - Relative timestamps (5m ago, 2h ago, etc.)
  - Direct links to related issues
  - Auto-refresh capability
  
- **Settings Tab**: Project management
  - Edit project name, icon, and description
  - Save changes with optimistic updates
  - Danger zone with delete confirmation
  - Prevents accidental deletions

**UI Elements:**
- Tab-based navigation
- Gradient header sections
- Hover state transitions
- Badge styling with rounded-full
- Confirmation dialogs for destructive actions

### 3. **Kanban Board** (`/projects/:id/board`)
Visual drag-and-drop issue management with workflow columns.

**Features:**
- Drag-and-drop between workflow states
- Optimistic UI updates
- Automatic state transitions via API
- Color-coded columns (TODO, In Progress, Done)
- Issue count badges per column
- Priority indicators with color-coded left borders
- Type-specific emoji icons
- Click to navigate to issue details
- Real-time issue movement
- Toast notifications on success/error

**UI Elements:**
- Gradient backgrounds on columns (category-specific)
- Backdrop blur effect on issue cards
- Lift animation on card hover
- Enhanced borders and shadows
- Icon scale animations
- Smooth drag overlay with reduced opacity

**Technical:**
- `@dnd-kit` for drag-and-drop
- Droppable zones with `useDroppable`
- Sortable items with `useSortable`
- Collision detection with `closestCorners`
- 8px activation distance to prevent accidental drags

### 4. **Issue Detail Page** (`/projects/:id/issues/:key`)
Complete issue management with inline editing and collaboration.

**Features:**
- **Header Section**:
  - Issue key, type icon, and title
  - Gradient background with primary colors
  - Breadcrumb navigation
  - Delete issue button with confirmation
  
- **Main Content**:
  - Inline description editing with Textarea
  - Save/Cancel buttons with loading states
  - Rich text support
  
- **Sidebar Cards**:
  - **Status**: Dropdown to change workflow state
    - Shows all available states
    - Triggers state transition API
    - Updates issue and invalidates queries
  - **Priority**: Dropdown to update priority
    - 5 levels: Lowest to Highest
    - Color-coded badges
  - **Assignee**: User selection dropdown
    - Shows all project members
    - Unassigned option
    - Avatar display
  - **Reporter**: Read-only user info
  - **Dates**: Created and updated timestamps
  
- **Watchers Section**:
  - Toggle watch/unwatch button
  - List of current watchers with avatars
  - Avatar rings with gradient backgrounds
  - Hover effects
  
- **Comments Section**:
  - Add new comments with Textarea
  - List all comments with author info
  - Timestamps with relative display
  - Avatar support
  - Border accent on cards
  - Empty state for no comments

**UI Elements:**
- Gradient backgrounds on header
- Colored accent borders (blue for comments)
- Avatar rings with hover effects
- Badge styling improvements
- Enhanced hover states
- Smooth transitions (200-300ms)
- Visual hierarchy with refined spacing

### 5. **Search Page** (`/search`)
Powerful full-text search across all projects with advanced filtering.

**Features:**
- **Search Bar**: Real-time text search
  - Searches title, key, and description
  - Instant results as you type
  - Search icon indicator
  
- **Filter Panel**:
  - Project dropdown (with emoji icons)
  - Type filter (Task, Bug, Story, Epic)
  - Priority filter (5 levels)
  - Status filter (TODO, In Progress, Done)
  - Clear all filters button
  
- **Results Display**:
  - Issue cards with project context
  - Type-specific emoji icons
  - Issue key in monospace font
  - Priority and status badges
  - Assignee information
  - Description preview (2 lines)
  - Click to navigate to issue
  - Result count display
  
- **Empty States**:
  - No results found message
  - Loading indicator

**UI Elements:**
- Grid layout with responsive columns
- Card hover effects with border highlights
- Badge color coding by priority
- Smooth transitions
- Icon-enhanced filters

**Technical:**
- Fetches issues from all projects
- Client-side filtering for instant results
- Preserves project context with augmented data
- Type-safe filtering logic

### 6. **Notifications Center** (`/notifications`)
Stay updated with all project activities and mentions.

**Features:**
- **Statistics Cards**:
  - Total notifications count
  - Unread count (orange badge)
  - Read count (green badge)
  - Color-coded icons with gradients
  
- **Filter Tabs**:
  - All notifications
  - Unread only (with count badge)
  
- **Notification Cards**:
  - Type-specific icons (mention, assignment, comment, state change)
  - Title and message display
  - Relative timestamps
  - "New" badge for unread
  - Issue/Project key badges
  - Click to navigate to related issue
  - Mark as read button (individual)
  - Visual distinction for unread (blue background, left border)
  
- **Actions**:
  - Mark all as read button (bulk action)
  - Mark individual notification as read
  - Auto-refresh every 30 seconds
  
- **Empty States**:
  - Different messages for All vs Unread tabs
  - Clean design with icon

**UI Elements:**
- Blue background for unread notifications
- Blue left border accent (4px)
- Type-specific colored icons
- Hover effects on cards
- Smooth transitions
- Badge styling

**Technical:**
- Real-time unread count in header (bell icon)
- Badge shows count on bell (9+ for >9)
- Auto-refresh every 30 seconds
- Optimistic updates on mark as read
- Toast notifications for actions

### 7. **Theme Toggle**
Seamless dark/light mode switching with persistence.

**Features:**
- Toggle button in header (Sun/Moon icons)
- Smooth 300ms transitions
- localStorage persistence
- Respects system preference on first load
- Full dark mode color scheme
- Applies to all components and pages

**UI Elements:**
- Icon changes based on current theme
- Scale animation on hover (1.1x)
- Smooth color transitions

**Technical:**
- ThemeProvider context with React
- CSS variables for color tokens
- Tailwind dark: variant support
- Applies .dark class to html element

### 8. **Authentication**
Secure login and registration system.

**Features:**
- Login page with email/password
- Registration with validation
- JWT token management
- Refresh token rotation
- Protected routes
- Redirect to login on auth failure
- Remember user session

**UI Elements:**
- Clean forms with validation feedback
- Loading states on submit
- Error message display

## 🎨 Design System

### Colors
- **Primary**: Blue (#3b82f6) - Actions, links, highlights
- **Success**: Green - Completed states, confirmations
- **Warning**: Orange - Priorities, unread counts
- **Danger**: Red - Delete actions, errors
- **Muted**: Gray - Secondary text, disabled states

### Animations
- **Hover Lift**: -translate-y-1 (issue cards, project cards)
- **Scale**: 1.05-1.1x (icons, buttons)
- **Duration**: 200-300ms for smoothness
- **Easing**: ease-in-out

### Typography
- **Headings**: Bold, large sizes (text-3xl for h1)
- **Body**: Regular weight, readable sizes
- **Mono**: Issue keys, code elements
- **Muted**: text-muted-foreground for secondary info

### Spacing
- **Consistent gaps**: 2, 3, 4, 6 (Tailwind scale)
- **Card padding**: p-4, p-6
- **Section spacing**: space-y-6

## 🚀 Quick Start (Docker - Recommended)

### Prerequisites
- Docker & Docker Compose
- Git

### 1. Clone and Setup

```bash
git clone <repository-url>
cd IssuePilot
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
```

### 2. Start All Services

```bash
docker compose up --build
```

This will start:
- **Backend** (Django + Gunicorn) → http://localhost:8000
- **Frontend** (React + Vite) → http://localhost:5173
- **PostgreSQL** → localhost:5432
- **Redis** → localhost:6379
- **Celery Worker** - Background task processing
- **Celery Beat** - Scheduled task execution

### 3. Initialize Database

In a new terminal:

```bash
# Run migrations
docker compose exec backend python manage.py migrate

# Create superuser
docker compose exec backend python manage.py createsuperuser

# Load demo data (optional)
docker compose exec backend python manage.py seed_data
```

### 4. Access the Application

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000/api/v1/
- **API Documentation**: http://localhost:8000/api/docs/
- **Django Admin**: http://localhost:8000/admin/

**Demo Credentials** (if you ran seed_data):
- Admin: `admin` / `admin123`
- Users: `alice` / `alice123`, `bob` / `bob123`, `charlie` / `charlie123`

## 🛠️ Local Development (Without Docker)

### Backend Setup

#### Prerequisites
- Python 3.11+
- PostgreSQL 15+
- Redis 7+

#### 1. Create Virtual Environment

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

#### 2. Install Dependencies

```bash
pip install -r requirements/dev.txt
```

#### 3. Configure Environment

```bash
cp .env.example .env
# Edit .env with your database credentials
```

#### 4. Setup Database

```bash
# Create database
createdb issuepilot

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Load demo data
python manage.py seed_data
```

#### 5. Run Backend

```bash
# Development server
python manage.py runserver

# In separate terminals:
# Celery worker
celery -A config worker -l info

# Celery beat
celery -A config beat -l info
```

### Frontend Setup

#### Prerequisites
- Node.js 20+
- npm or yarn

#### 1. Install Dependencies

```bash
cd frontend
npm install
```

#### 2. Configure Environment

```bash
cp .env.example .env
# Defaults should work for local development
```

#### 3. Run Frontend

```bash
npm run dev
```

Frontend will be available at http://localhost:5173

## 📁 Project Structure

```
IssuePilot/
├── backend/
│   ├── config/              # Django settings
│   │   ├── settings/        # Split settings (base, dev, prod, test)
│   │   ├── urls.py          # Main URL config
│   │   ├── celery.py        # Celery configuration
│   │   └── wsgi.py / asgi.py
│   ├── apps/
│   │   ├── users/           # User management
│   │   ├── projects/        # Projects, boards, workflows
│   │   ├── issues/          # Issues, comments, attachments
│   │   └── notifications/   # Notifications & outbox
│   ├── common/              # Shared utilities
│   │   ├── permissions.py   # Custom permissions
│   │   ├── pagination.py    # Custom pagination
│   │   ├── exceptions.py    # Error handling
│   │   └── middleware.py    # Request logging
│   ├── api/v1/              # API routing
│   ├── requirements/        # Python dependencies
│   └── manage.py
├── frontend/
│   ├── src/
│   │   ├── api/             # API client & types
│   │   ├── components/      # Reusable UI components
│   │   ├── pages/           # Page components
│   │   ├── store/           # Zustand state management
│   │   ├── lib/             # Utilities
│   │   └── main.tsx         # App entry point
│   ├── public/
│   └── package.json
├── Dockerfile.backend
├── Dockerfile.frontend
├── docker-compose.yml
└── README.md
```

## 🏗️ Architecture

### Backend Architecture

**Clean Architecture Pattern:**
- **Models** - Domain entities (Django ORM)
- **Services** - Business logic (write operations)
- **Selectors** - Query logic (read operations)
- **Serializers** - API serialization (DRF)
- **Views** - API endpoints (DRF views/viewsets)

**Key Design Patterns:**
- **Outbox Pattern** - Reliable event processing
- **Service Layer** - Business logic encapsulation
- **Repository Pattern** - Data access abstraction
- **Event Sourcing** - Activity tracking

### Frontend Architecture

**Feature-Based Structure:**
- **API Client** - Centralized axios instance with interceptors
- **TanStack Query** - Server state management & caching
- **Zustand** - Client state management (auth)
- **React Router** - Routing
- **shadcn/ui** - Accessible UI components

## 📊 Data Models

### Core Models

- **User** - Custom user model extending Django's AbstractUser
- **Project** - Container for issues with unique key
- **ProjectMembership** - User roles in projects
- **Board** - Kanban or Scrum board
- **Sprint** - Time-boxed iteration
- **Epic** - Large work item
- **Workflow** - State machine per project
- **WorkflowState** - States in workflow (To Do, In Progress, Done)
- **WorkflowTransition** - Allowed state transitions
- **Issue** - Core work item with auto-generated key (PROJ-123)
- **Comment** - Discussion on issues
- **Attachment** - File attachments
- **Watcher** - Issue followers
- **Event** - Activity tracking
- **OutboxMessage** - Transactional event processing
- **Notification** - User notifications

## 🔐 Security

- **JWT Authentication** with refresh tokens
- **CORS** configured for frontend origin
- **CSRF Protection** enabled
- **SQL Injection Prevention** via ORM
- **XSS Protection** via React
- **Input Validation** at serializer level
- **Permission Classes** for authorization
- **Environment Variables** for secrets

## 🧪 Testing

### Run Backend Tests

```bash
cd backend
python manage.py test
```

### Run Frontend Tests

```bash
cd frontend
npm test
```

## 📝 API Documentation

Interactive API documentation is available at:
- **Swagger UI**: http://localhost:8000/api/docs/
- **OpenAPI Schema**: http://localhost:8000/api/schema/

### Key Endpoints

#### Authentication
```
POST   /api/v1/auth/register/       # Create new user
POST   /api/v1/auth/login/          # Login and get tokens
POST   /api/v1/auth/refresh/        # Refresh access token
GET    /api/v1/auth/me/             # Get current user
```

#### Projects
```
GET    /api/v1/projects/                    # List all projects
POST   /api/v1/projects/                    # Create new project
GET    /api/v1/projects/:id/                # Get project details
PATCH  /api/v1/projects/:id/                # Update project
DELETE /api/v1/projects/:id/                # Delete project
GET    /api/v1/projects/:id/members/        # List members
POST   /api/v1/projects/:id/members/        # Add member
DELETE /api/v1/projects/:id/members/:mid/   # Remove member
GET    /api/v1/projects/:id/workflow/       # Get workflow
GET    /api/v1/projects/:id/activity/       # Get activity feed
```

#### Issues
```
GET    /api/v1/projects/:id/issues/                    # List issues
POST   /api/v1/projects/:id/issues/                    # Create issue
GET    /api/v1/projects/:id/issues/:key/               # Get issue
PATCH  /api/v1/projects/:id/issues/:key/               # Update issue
DELETE /api/v1/projects/:id/issues/:key/               # Delete issue
POST   /api/v1/projects/:id/issues/:key/transitions/   # Change state
GET    /api/v1/projects/:id/issues/:key/comments/      # List comments
POST   /api/v1/projects/:id/issues/:key/comments/      # Add comment
GET    /api/v1/projects/:id/issues/:key/watchers/      # List watchers
POST   /api/v1/projects/:id/issues/:key/watchers/      # Add watcher
DELETE /api/v1/projects/:id/issues/:key/watchers/      # Remove watcher
GET    /api/v1/projects/:id/issues/:key/activity/      # Get issue activity
```

#### Notifications
```
GET    /api/v1/notifications/              # List notifications (filter by is_read)
GET    /api/v1/notifications/unread-count/ # Get unread count
POST   /api/v1/notifications/mark-all-read/# Mark all as read
PATCH  /api/v1/notifications/:id/          # Update notification (mark as read)
```

#### Search
```
GET    /api/v1/projects/:id/issues/?search=query  # Full-text search
GET    /api/v1/projects/:id/issues/?type=bug      # Filter by type
GET    /api/v1/projects/:id/issues/?priority=high # Filter by priority
GET    /api/v1/projects/:id/issues/?state=1       # Filter by state
```

## 🚀 Deployment

### Environment Variables

#### Backend (.env)
```env
DJANGO_ENV=prod
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=your-domain.com

POSTGRES_DB=issuepilot
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your-password
POSTGRES_HOST=db
POSTGRES_PORT=5432

REDIS_URL=redis://redis:6379/0
CELERY_BROKER_URL=redis://redis:6379/1
CELERY_RESULT_BACKEND=redis://redis:6379/2

CORS_ALLOWED_ORIGINS=https://your-domain.com
```

#### Frontend (.env)
```env
VITE_API_URL=https://api.your-domain.com
```

### Production Checklist

- [ ] Set strong `SECRET_KEY`
- [ ] Set `DEBUG=False`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Set up proper database credentials
- [ ] Configure email backend (SMTP)
- [ ] Set up SSL/TLS certificates
- [ ] Configure static/media file storage (S3)
- [ ] Set up logging and monitoring
- [ ] Configure backup strategy
- [ ] Set up CI/CD pipeline

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License.

## 👥 Team

Built with ❤️ as a production-grade demonstration of modern full-stack development.

## 🙏 Acknowledgments

- Django & Django REST Framework
- React & Vite
- TailwindCSS & shadcn/ui
- PostgreSQL & Redis
- Celery
- Docker

---

**IssuePilot** - Production-grade issue tracking for modern teams.
