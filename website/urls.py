from django.urls import path
from . import views

urlpatterns = [ # type: ignore
    path('', views.home, name='home'),# type: ignore
    path('login/', views.login_user, name = 'login'),# type: ignore
    path('logout/', views.logout_user, name='logout'),# type: ignore
    path('register/', views.register_user, name='register'),# type: ignore
    path('record/<int:pk>',views.customer_record, name='record'),# esta es la funcion definida de la vista
    path('delete_record/<int:pk>/', views.delete_record, name='delete_record'),
    path('add_record/', views.add_record, name='add_record'),
    path('update_record/<int:pk>/', views.update_record, name='update_record'),
    path('profile/', views.profile, name='profile'),
    path('manage_users/', views.manage_users, name='manage_users'),
    path('admin_ranking/', views.admin_ranking, name='admin_ranking'),
    path('admin_games/', views.admin_games, name='admin_games'),
]