"""
Seed demo data command.
"""
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction

from apps.issues.services import comment_create, issue_create
from apps.projects.services import epic_create, project_create, sprint_create

User = get_user_model()


class Command(BaseCommand):
    help = "Seed database with demo data"

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write("Seeding demo data...")

        # Create demo users
        self.stdout.write("Creating users...")
        admin, _ = User.objects.get_or_create(
            username="admin",
            defaults={
                "email": "admin@issuepilot.dev",
                "first_name": "Admin",
                "last_name": "User",
                "is_staff": True,
                "is_superuser": True,
            }
        )
        admin.set_password("admin123")
        admin.save()

        alice, _ = User.objects.get_or_create(
            username="alice",
            defaults={
                "email": "alice@issuepilot.dev",
                "first_name": "Alice",
                "last_name": "Johnson",
            }
        )
        alice.set_password("alice123")
        alice.save()

        bob, _ = User.objects.get_or_create(
            username="bob",
            defaults={
                "email": "bob@issuepilot.dev",
                "first_name": "Bob",
                "last_name": "Smith",
            }
        )
        bob.set_password("bob123")
        bob.save()

        charlie, _ = User.objects.get_or_create(
            username="charlie",
            defaults={
                "email": "charlie@issuepilot.dev",
                "first_name": "Charlie",
                "last_name": "Brown",
            }
        )
        charlie.set_password("charlie123")
        charlie.save()

        # Create demo project
        self.stdout.write("Creating project...")
        try:
            project = project_create(
                name="Demo Project",
                key="DEMO",
                description="A demo project for IssuePilot showcasing all features",
                owner=admin,
            )
        except Exception:
            # Project already exists
            from apps.projects.models import Project
            project = Project.objects.get(key="DEMO")

        # Add team members
        self.stdout.write("Adding team members...")
        from apps.projects.services import project_add_member
        from apps.projects.models import ProjectMembership
        
        project_add_member(project=project, user=alice, role=ProjectMembership.Role.ADMIN)
        project_add_member(project=project, user=bob, role=ProjectMembership.Role.MEMBER)
        project_add_member(project=project, user=charlie, role=ProjectMembership.Role.MEMBER)

        # Create sprint
        self.stdout.write("Creating sprint...")
        from apps.projects.models import Board
        from apps.projects.services import sprint_create, sprint_start
        board = project.boards.first()
        
        sprint = sprint_create(
            board=board,
            name="Sprint 1",
            goal="Complete initial features",
        )
        sprint_start(sprint=sprint)

        # Create epics
        self.stdout.write("Creating epics...")
        epic_auth = epic_create(
            project=project,
            name="Authentication & Authorization",
            description="User authentication and role-based access control",
            color="#3B82F6",
        )

        epic_issues = epic_create(
            project=project,
            name="Issue Management",
            description="Core issue tracking functionality",
            color="#10B981",
        )

        epic_ui = epic_create(
            project=project,
            name="User Interface",
            description="Frontend components and pages",
            color="#F59E0B",
        )

        # Create issues
        self.stdout.write("Creating issues...")
        from apps.issues.models import Issue
        
        issue1 = issue_create(
            project=project,
            title="Implement user registration and login",
            description="Create JWT-based authentication system with registration and login endpoints",
            issue_type=Issue.Type.STORY,
            priority=Issue.Priority.HIGH,
            reporter=admin,
            assignee=alice,
            epic=epic_auth,
            sprint=sprint,
            story_points=5,
        )

        issue2 = issue_create(
            project=project,
            title="Design Kanban board component",
            description="Create a drag-and-drop Kanban board using @dnd-kit with smooth animations",
            issue_type=Issue.Type.TASK,
            priority=Issue.Priority.MEDIUM,
            reporter=alice,
            assignee=bob,
            epic=epic_ui,
            sprint=sprint,
            story_points=8,
        )

        issue3 = issue_create(
            project=project,
            title="Implement issue search with full-text",
            description="Add PostgreSQL full-text search for issues with filters and saved views",
            issue_type=Issue.Type.STORY,
            priority=Issue.Priority.MEDIUM,
            reporter=admin,
            assignee=alice,
            epic=epic_issues,
            story_points=5,
        )

        issue4 = issue_create(
            project=project,
            title="Fix issue key generation bug",
            description="Issue keys are not incrementing correctly when multiple issues are created simultaneously",
            issue_type=Issue.Type.BUG,
            priority=Issue.Priority.HIGHEST,
            reporter=bob,
            assignee=charlie,
            epic=epic_issues,
            sprint=sprint,
            story_points=3,
        )

        issue5 = issue_create(
            project=project,
            title="Add email notifications for issue updates",
            description="Send email notifications when issues are assigned, commented on, or state changes",
            issue_type=Issue.Type.TASK,
            priority=Issue.Priority.LOW,
            reporter=alice,
            epic=epic_issues,
            story_points=5,
        )

        # Add comments
        self.stdout.write("Creating comments...")
        comment_create(
            issue=issue1,
            author=alice,
            content="I'll start working on this today. Will use Django REST Framework SimpleJWT.",
        )

        comment_create(
            issue=issue1,
            author=admin,
            content="Great! Make sure to include refresh token rotation and proper error handling.",
        )

        comment_create(
            issue=issue2,
            author=bob,
            content="Should we follow the design in Figma or create our own variant?",
        )

        comment_create(
            issue=issue4,
            author=charlie,
            content="Found the issue - it's a race condition in the save() method. Working on a fix using select_for_update().",
        )

        self.stdout.write(self.style.SUCCESS("Successfully seeded demo data!"))
        self.stdout.write(f"Project: {project.key}")
        self.stdout.write(f"Users: admin/admin123, alice/alice123, bob/bob123, charlie/charlie123")
        self.stdout.write(f"Created {project.issues.count()} issues")
