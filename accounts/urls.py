from django.urls import path
from .views import (
    CustomLoginView,
    CustomLogoutView,
    UserCreateView,
    UserListView,
    UserDetailView,
    UserUpdateView,
    UploadExcelView,
    ForcePasswordResetView,
)

urlpatterns = [
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path("create/", UserCreateView.as_view(), name="user_create"),
    path("", UserListView.as_view(), name="user_list"),
    path("<int:pk>/", UserDetailView.as_view(), name="user_detail"),
    path("<int:pk>/edit/", UserUpdateView.as_view(), name="user_update"),
    path(
        "password_reset/",
        ForcePasswordResetView.as_view(),
        name="password_reset",
    ),
    path("bulk_upload/", UploadExcelView.as_view(), name="bulk_upload"),
]
