from django.contrib import admin
from django.urls import path, include

from movies.api.v1 import views
from .settings import DEBUG

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/movies/', views.MoviesListApi.as_view()),
    path('api/v1/movies/<uuid:pk>', views.MovieDetailApi.as_view()),
]

if DEBUG:
    urlpatterns += [
        path('__debug__/', include('debug_toolbar.urls')),
    ]
