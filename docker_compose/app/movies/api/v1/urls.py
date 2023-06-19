from django.urls import path, include

from movies.api.v1 import views

urlpatterns = [
    path('v1/', include('movies.api.urls')),
    path('movies/<uuid:pk>', views.MovieDetailApi.as_view()),
    path('movies/', views.MoviesListApi.as_view())
]
