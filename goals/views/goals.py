from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
)
from django_filters.rest_framework import DjangoFilterBackend

from goals.filters import GoalDateFilter
from goals.models import Goal
from goals.permissions import GoalPermissions
from goals.serializers import (
    GoalCreateSerializer,
    GoalSerializer,
)


class GoalCreateView(CreateAPIView):
    model = Goal
    serializer_class = GoalCreateSerializer
    permission_classes = [GoalPermissions]


class GoalView(RetrieveUpdateDestroyAPIView):
    model = Goal
    serializer_class = GoalSerializer
    permission_classes = [GoalPermissions]

    def get_queryset(self):
        return Goal.objects.filter(category__board__participants__user=self.request.user)

    def perform_destroy(self, instance):
        instance.status = Goal.Status.archived
        instance.save()
        return instance


class GoalListView(ListAPIView):
    model = Goal
    permission_classes = [GoalPermissions]
    serializer_class = GoalSerializer
    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]
    filterset_class = GoalDateFilter
    search_fields = ['title', 'description']
    ordering_fields = ['due_date', 'priority']
    ordering = ['priority', 'due_date']

    def get_queryset(self):
        return Goal.objects.filter(category__board__participants__user=self.request.user)
