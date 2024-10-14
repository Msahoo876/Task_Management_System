from django.urls import path
from . import views

urlpatterns = [
    path('',views.Home,name="Home"),
    path('sign',views.sign,name="sign"),
    path('crud', views.crud, name='crud'),
    path('create',views.create, name='create'),
    path('update',views.update, name='update'),
    path('delete',views.delete, name='delete'),
    path('view_t',views.view_t,name='view_t'),
    path('assign',views.assign,name='assign'),
    path('profile/',views.profile,name='profile'),
    path('create-task/', views.create_task, name='create_task'),
    path('get_tasks/', views.get_tasks, name='get_tasks'),
    path('update_task/', views.update_task, name='update_task'),
    path('get_tasks1/', views.get_tasks1, name='get_tasks1'),
    path('delete_task/', views.delete_task, name='delete_task'),
    path('get_tasks2/', views.get_tasks2, name='get_tasks2'),
    path('search_task/', views.search_task, name='search_task'),
    path('get_tasks3/', views.get_tasks3, name='get_tasks3'),

    path('signup_task/', views.signup_task, name='signup_task'),
    path('login_task/', views.login_task, name='login_task'),
    path('assign_task/',views.assign_task,name='assign_task'),
    path('profile_task/',views.profile_task,name='profile_task'),
    path('feedback/',views.feedback,name='feedback'),
    path('logout/', views.logout_view, name='logout'),
    path('back/', views.back, name='back'),
    
]
