from apps.accounts.api.v1.views import RegisterView
from django.urls import path, include

urlpatterns = [
    path('accounts/', include('apps.accounts.api.v1.urls')),
]
