from django.urls import path
from . import views

app_name = 'research'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('session/<uuid:session_id>/', views.SessionView.as_view(), name='session'),
    path('api/sessions/', views.SessionListView.as_view(), name='api_sessions'),
    path('api/sessions/create/', views.CreateSessionView.as_view(), name='api_create_session'),
    path('api/query/', views.QueryView.as_view(), name='api_query'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
]