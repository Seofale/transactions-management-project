from django.urls import path, include

from apps.pockets.routers import pockets_router
from apps.targets.routers import targets_router

urlpatterns = [
    path('auth/', include('apps.users.urls.auth')),
    path('users/', include('apps.users.urls.users_urls')),
    path('pockets/', include(pockets_router.urls)),
    path('targets/', include(targets_router.urls)),
    path('analytics/', include('apps.pockets.urls.analytics_by_month')),
    path('quotes/', include('apps.quotes.urls.quote')),
]
