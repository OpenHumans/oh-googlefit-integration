from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('setup/', views.setup, name='setup'),
    path('logout/', views.logout_user, name='logout'),
    path('complete/', views.complete_googlefit, name='complete_googlefit'),
    path('authorize/', views.authorize_googlefit, name='authorize_googlefit'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('update_data/', views.update_data, name='update_data'),
    path('remove_googlefit/', views.remove_googlefit, name='remove_googlefit')
]
