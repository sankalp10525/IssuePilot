# IssuePilot
Initial project setup

Jira-Like Issue Tracker (Workflow + Notifications + Search)

Problem statement

Teams need a tracker for issues, projects, sprints, and workflows—fast search, notifications, and reliable history.
Functional requirements

Projects, boards, sprints, epics, issues
Custom workflow states + transitions (per project)
Comments, attachments, watchers, mentions
Notifications (in-app + email)
Full-text search + filters + saved views
Activity feed per project/issue
Backend (Django/DRF)

Domain modeling: Issue, Sprint, Workflow, Transition, Event
Permission system: project roles + issue-level visibility
Event-driven notifications (signals/outbox pattern)
Search indexing (Postgres FTS or external search)
Async tasks: notifications, indexing, digests
Optimized list endpoints (pagination, select_related/prefetch_related)
WebSocket layer for live updates (optional)
Frontend (React)

Kanban board + drag/drop transitions
Sprint planning view
Issue detail page with comments + history
Search page with advanced filters
Notification center + activity feed
Bonus

Workflow builder UI (state machine editor)
SLA timers + escalations
Import/export (CSV / JSON)
Realtime collaboration indicators
