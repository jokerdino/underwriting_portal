from django.urls import path
from .views import (
    ProposalListView,
    ProposalCreateView,
    ProposalUpdateView,
    ProposalDetailView,
    load_segments,
)

urlpatterns = [
    path("", ProposalListView.as_view(), name="proposal_list"),
    path(
        "status/<str:status>/",
        ProposalListView.as_view(),
        name="proposal_list_by_status",
    ),
    path("create/", ProposalCreateView.as_view(), name="proposal_create"),
    path("<int:pk>/", ProposalDetailView.as_view(), name="proposal_detail"),
    path("<int:pk>/edit/", ProposalUpdateView.as_view(), name="proposal_update"),
    path("ajax/load-segments/", load_segments, name="ajax_load_segments"),
]
