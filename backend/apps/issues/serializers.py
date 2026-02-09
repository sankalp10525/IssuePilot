"""
Issue serializers.
"""
from rest_framework import serializers

from apps.issues.models import Attachment, Comment, Event, Issue, Watcher
from apps.projects.serializers import WorkflowStateSerializer
from apps.users.serializers import UserSerializer


class IssueListSerializer(serializers.ModelSerializer):
    """Lightweight issue serializer for lists."""
    reporter = UserSerializer(read_only=True)
    assignee = UserSerializer(read_only=True)
    state = WorkflowStateSerializer(read_only=True)

    class Meta:
        model = Issue
        fields = [
            "id",
            "key",
            "title",
            "issue_type",
            "priority",
            "state",
            "reporter",
            "assignee",
            "sprint",
            "epic",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "key", "created_at", "updated_at"]


class IssueDetailSerializer(serializers.ModelSerializer):
    """Detailed issue serializer."""
    reporter = UserSerializer(read_only=True)
    assignee = UserSerializer(read_only=True)
    state = WorkflowStateSerializer(read_only=True)
    watchers = serializers.SerializerMethodField()
    is_watching = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()
    attachment_count = serializers.SerializerMethodField()

    class Meta:
        model = Issue
        fields = [
            "id",
            "key",
            "sequence",
            "title",
            "description",
            "issue_type",
            "priority",
            "state",
            "reporter",
            "assignee",
            "sprint",
            "epic",
            "parent",
            "story_points",
            "time_estimate",
            "time_spent",
            "due_date",
            "resolved_at",
            "watchers",
            "is_watching",
            "comment_count",
            "attachment_count",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "key", "sequence", "created_at", "updated_at", "resolved_at"]

    def get_watchers(self, obj):
        return UserSerializer(
            [w.user for w in obj.watchers.all()],
            many=True
        ).data

    def get_is_watching(self, obj):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return obj.watchers.filter(user=request.user).exists()
        return False

    def get_comment_count(self, obj):
        return obj.comments.count()

    def get_attachment_count(self, obj):
        return obj.attachments.count()


class IssueCreateSerializer(serializers.ModelSerializer):
    """Issue create serializer."""
    assignee_id = serializers.IntegerField(required=False, allow_null=True)

    class Meta:
        model = Issue
        fields = [
            "title",
            "description",
            "issue_type",
            "priority",
            "assignee_id",
            "sprint",
            "epic",
            "parent",
            "story_points",
            "time_estimate",
            "due_date",
        ]

    def create(self, validated_data):
        from apps.issues.services import issue_create
        from django.contrib.auth import get_user_model
        
        User = get_user_model()
        project = self.context["project"]
        reporter = self.context["request"].user
        
        assignee_id = validated_data.pop("assignee_id", None)
        assignee = User.objects.get(id=assignee_id) if assignee_id else None
        
        return issue_create(
            project=project,
            reporter=reporter,
            assignee=assignee,
            **validated_data
        )


class IssueUpdateSerializer(serializers.ModelSerializer):
    """Issue update serializer."""
    assignee_id = serializers.IntegerField(required=False, allow_null=True)
    state_id = serializers.IntegerField(required=False)

    class Meta:
        model = Issue
        fields = [
            "title",
            "description",
            "issue_type",
            "priority",
            "assignee_id",
            "state_id",
            "sprint",
            "epic",
            "story_points",
            "time_estimate",
            "time_spent",
            "due_date",
        ]

    def update(self, instance, validated_data):
        from apps.issues.services import issue_update
        from apps.projects.models import WorkflowState
        from django.contrib.auth import get_user_model
        
        User = get_user_model()
        actor = self.context["request"].user
        
        # Handle assignee
        if "assignee_id" in validated_data:
            assignee_id = validated_data.pop("assignee_id")
            validated_data["assignee"] = User.objects.get(id=assignee_id) if assignee_id else None
        
        # Handle state
        if "state_id" in validated_data:
            state_id = validated_data.pop("state_id")
            validated_data["state"] = WorkflowState.objects.get(id=state_id)
        
        return issue_update(issue=instance, actor=actor, **validated_data)


class CommentSerializer(serializers.ModelSerializer):
    """Comment serializer."""
    author = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "content", "author", "created_at", "updated_at"]
        read_only_fields = ["id", "author", "created_at", "updated_at"]

    def create(self, validated_data):
        from apps.issues.services import comment_create
        issue = self.context["issue"]
        author = self.context["request"].user
        return comment_create(issue=issue, author=author, **validated_data)

    def update(self, instance, validated_data):
        from apps.issues.services import comment_update
        return comment_update(comment=instance, **validated_data)


class AttachmentSerializer(serializers.ModelSerializer):
    """Attachment serializer."""
    uploaded_by = UserSerializer(read_only=True)
    url = serializers.SerializerMethodField()

    class Meta:
        model = Attachment
        fields = [
            "id",
            "filename",
            "file_size",
            "content_type",
            "url",
            "uploaded_by",
            "created_at",
        ]
        read_only_fields = ["id", "uploaded_by", "created_at"]

    def get_url(self, obj):
        request = self.context.get("request")
        if obj.file and request:
            return request.build_absolute_uri(obj.file.url)
        return None

    def create(self, validated_data):
        from apps.issues.services import attachment_create
        issue = self.context["issue"]
        uploaded_by = self.context["request"].user
        file = self.context["request"].FILES.get("file")
        
        return attachment_create(
            issue=issue,
            uploaded_by=uploaded_by,
            file=file,
            filename=file.name,
            file_size=file.size,
            content_type=file.content_type,
        )


class WatcherSerializer(serializers.ModelSerializer):
    """Watcher serializer."""
    user = UserSerializer(read_only=True)

    class Meta:
        model = Watcher
        fields = ["id", "user", "created_at"]
        read_only_fields = ["id", "created_at"]


class EventSerializer(serializers.ModelSerializer):
    """Event serializer for activity feed."""
    actor = UserSerializer(read_only=True)
    issue_key = serializers.CharField(source="issue.key", read_only=True, allow_null=True)

    class Meta:
        model = Event
        fields = ["id", "event_type", "actor", "issue_key", "data", "created_at"]
        read_only_fields = ["id", "created_at"]


class IssueTransitionSerializer(serializers.Serializer):
    """Serializer for issue state transitions."""
    to_state_id = serializers.IntegerField()

    def validate_to_state_id(self, value):
        from apps.projects.models import WorkflowState
        from apps.projects.selectors import workflow_can_transition
        
        try:
            to_state = WorkflowState.objects.get(id=value)
        except WorkflowState.DoesNotExist:
            raise serializers.ValidationError("Invalid state ID.")
        
        issue = self.context["issue"]
        if not workflow_can_transition(from_state=issue.state, to_state=to_state):
            raise serializers.ValidationError(
                f"Cannot transition from {issue.state.name} to {to_state.name}."
            )
        
        return value
