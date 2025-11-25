from . import views
from django.urls import path


urlpatterns = [
    path('', views.PrincipalView.as_view(), name='home'),
    path('login/', views.LoginView.as_view(), name='login'),
    
    path('logout/', views.LogoutView.as_view(), name='logout'),
    ]
