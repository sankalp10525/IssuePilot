"""
Project serializers.
"""
from rest_framework import serializers

from apps.projects.models import (
    Board,
    Epic,
    Project,
    ProjectMembership,
    Sprint,
    Workflow,
    WorkflowState,
    WorkflowTransition,
)
from apps.users.serializers import UserSerializer


class ProjectSerializer(serializers.ModelSerializer):
    """Project serializer."""
    owner = UserSerializer(read_only=True)
    member_count = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            "id",
            "name",
            "key",
            "description",
            "icon",
            "owner",
            "member_count",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "key", "owner", "created_at", "updated_at"]

    def get_member_count(self, obj):
        return obj.memberships.count()


class ProjectCreateSerializer(serializers.ModelSerializer):
    """Project create serializer."""
    
    class Meta:
        model = Project
        fields = ["name", "key", "description", "icon"]

    def validate_key(self, value):
        value = value.upper()
        if len(value) < 2 or len(value) > 10:
            raise serializers.ValidationError("Key must be between 2 and 10 characters.")
        if not value.isalnum():
            raise serializers.ValidationError("Key must contain only letters and numbers.")
        return value

    def create(self, validated_data):
        from apps.projects.services import project_create
        user = self.context["request"].user
        return project_create(owner=user, **validated_data)


class ProjectMembershipSerializer(serializers.ModelSerializer):
    """Project membership serializer."""
    user = UserSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = ProjectMembership
        fields = ["id", "user", "user_id", "role", "created_at"]
        read_only_fields = ["id", "created_at"]


class BoardSerializer(serializers.ModelSerializer):
    """Board serializer."""
    
    class Meta:
        model = Board
        fields = ["id", "name", "board_type", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]

    def create(self, validated_data):
        from apps.projects.services import board_create
        project = self.context["project"]
        return board_create(project=project, **validated_data)


class SprintSerializer(serializers.ModelSerializer):
    """Sprint serializer."""
    issue_count = serializers.SerializerMethodField()

    class Meta:
        model = Sprint
        fields = [
            "id",
            "name",
            "goal",
            "status",
            "start_date",
            "end_date",
            "issue_count",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def get_issue_count(self, obj):
        return obj.issues.count()

    def create(self, validated_data):
        from apps.projects.services import sprint_create
        board = self.context["board"]
        return sprint_create(board=board, **validated_data)


class EpicSerializer(serializers.ModelSerializer):
    """Epic serializer."""
    issue_count = serializers.SerializerMethodField()

    class Meta:
        model = Epic
        fields = [
            "id",
            "name",
            "description",
            "color",
            "start_date",
            "due_date",
            "issue_count",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def get_issue_count(self, obj):
        return obj.issues.count()

    def create(self, validated_data):
        from apps.projects.services import epic_create
        project = self.context["project"]
        return epic_create(project=project, **validated_data)


class WorkflowStateSerializer(serializers.ModelSerializer):
    """Workflow state serializer."""
    
    class Meta:
        model = WorkflowState
        fields = ["id", "name", "category", "order", "is_initial", "created_at"]
        read_only_fields = ["id", "created_at"]


class WorkflowTransitionSerializer(serializers.ModelSerializer):
    """Workflow transition serializer."""
    from_state = WorkflowStateSerializer(read_only=True)
    to_state = WorkflowStateSerializer(read_only=True)

    class Meta:
        model = WorkflowTransition
        fields = ["id", "from_state", "to_state", "name", "created_at"]
        read_only_fields = ["id", "created_at"]


class WorkflowSerializer(serializers.ModelSerializer):
    """Workflow serializer with states and transitions."""
    states = WorkflowStateSerializer(many=True, read_only=True)
    transitions = WorkflowTransitionSerializer(many=True, read_only=True)

    class Meta:
        model = Workflow
        fields = ["id", "name", "states", "transitions", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]


class ProjectDetailSerializer(ProjectSerializer):
    """Detailed project serializer with workflow."""
    workflow = WorkflowSerializer(read_only=True)
    boards = BoardSerializer(many=True, read_only=True)

    class Meta(ProjectSerializer.Meta):
        fields = ProjectSerializer.Meta.fields + ["workflow", "boards"]
