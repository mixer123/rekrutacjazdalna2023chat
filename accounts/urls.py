from django.urls import path, include
#
from . import views
from .views import SignUpView, success


urlpatterns = [
    path('registration/', SignUpView.as_view(), name='signup'),
    path('success/', views.success, name="success"),
    # path('', include('accounts.urls')),
    # path("", include("django.contrib.auth.urls"))
    # path('accounts/password_reset/', name='password_reset'),
    # path('accounts/password_reset/done/', name='password_reset_done'),
]