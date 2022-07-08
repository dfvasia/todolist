from django.contrib import admin
from django.db.models import Count

from goals.models import GoalCategory, Goal, GoalComment, Board, BoardParticipant


class BoardParticipantInline(admin.TabularInline):
    model = BoardParticipant
    extra = 0

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if not self.has_view_or_change_permission(request):
            queryset = queryset.none()
        queryset = queryset.exclude(role=BoardParticipant.Role.owner)
        return queryset


class GoalCommentInline(admin.TabularInline):
    model = GoalComment
    extra = 0
    show_change_link = True

    def _get_form_for_get_fields(self, request, obj=None):
        return self.get_formset(request, obj, fields=('user', 'text', 'goal')).form

    def has_change_permission(self, request, obj=None):
        return False


class GoalInline(admin.TabularInline):
    model = Goal
    extra = 0
    show_change_link = True

    def _get_form_for_get_fields(self, request, obj=None):
        return self.get_formset(request, obj, fields=('title', 'status', 'priority', 'due_date')).form

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(GoalCategory)
class GoalCategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'goals_count', 'created', 'updated')
    search_fields = ('title', 'user')
    readonly_fields = ('created', 'updated')
    list_filter = ('is_deleted',)
    inlines = (GoalInline,)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(_goals_count=Count('goals', distinct=True))
        return queryset

    def goals_count(self, obj):
        return obj._goals_count

    goals_count.short_description = 'Количество целей'


@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'status', 'description', 'due_date', 'category', 'comments_count')
    search_fields = ('title', 'description')
    readonly_fields = ('created', 'updated')
    inlines = (GoalCommentInline,)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(_comments_count=Count('goal_comments', distinct=True))
        return queryset

    def comments_count(self, obj):
        return obj._comments_count

    comments_count.short_description = 'Количество комментов'


@admin.register(GoalComment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('goal_id', 'text')
    list_display_links = ('text',)
    search_fields = ('text',)
    readonly_fields = ('created', 'updated')


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'participants_count', 'created', 'updated')
    search_fields = ('title',)
    list_filter = ('is_deleted',)
    readonly_fields = ('created', 'updated')
    inlines = (BoardParticipantInline,)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.prefetch_related('participants')
        return queryset

    def owner(self, obj):
        return obj.participants.filter(role=BoardParticipant.Role.owner).get().user

    def participants_count(self, obj):
        count = obj.participants.count()-1
        return count if count >= 0 else 0

    owner.short_description = 'Владелец'
    participants_count.short_description = 'количество участников'
