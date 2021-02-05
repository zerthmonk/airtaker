from django.urls import path
from core.views import profile, healthcheck

urlpatterns = [
    path('profiles/', profile),
    path('healthcheck/', healthcheck)
]
