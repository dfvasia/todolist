from django.urls import path, include

from goals.views.boards import (BoardCreateView,
                                BoardView,
                                BoardListView,
                                )
from goals.views.category import (GoalCategoryCreateView,
                                  GoalCategoryListView,
                                  GoalCategoryView,
                                  )
from goals.views.comment import (CommentCreateView,
                                 CommentListView,
                                 CommentView,
                                 )
from goals.views.goals import (GoalCreateView,
                               GoalListView,
                               GoalView,
                               )

urlpatterns = [


    path('goal_category/', include((
        [
            path('create', GoalCategoryCreateView.as_view(), name='create'),
            path('list', GoalCategoryListView.as_view(), name='list'),
            path('<pk>', GoalCategoryView.as_view(), name='main'),
        ], 'goal_category'), namespace='goal_category')),

    path('goal/', include((
        [
            path('create', GoalCreateView.as_view(), name='create'),
            path('list', GoalListView.as_view(), name='list'),
            path('<pk>', GoalView.as_view(), name='main'),
        ], 'goal'), namespace='goal')),

    path('goal_comment/', include((
        [    
            path('create', CommentCreateView.as_view(), name='create'),
            path('list', CommentListView.as_view(), name='list'),
            path('<pk>', CommentView.as_view(), name='main'),
        ], 'goal_comment'), namespace='goal_comment')),

    path('board/', include((
        [
            path('create', BoardCreateView.as_view(), name='create'),
            path('list', BoardListView.as_view(), name='list'),
            path('<pk>', BoardView.as_view(), name='main'),
        ], 'board'), namespace='board')),
    ]
