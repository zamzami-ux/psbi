from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('kursus/', views.kursus, name='kursus'),
    path('komunitas/', views.komunitas, name='komunitas'),
    path('misi/', views.misi, name='misi'),
    path('misi/<int:mission_id>/materi/', views.materi_view, name='misi_materi'),
    path('misi/<int:mission_id>/kuis/', views.kuis_view, name='misi_kuis'),
    path('misi/<int:mission_id>/evaluasi/', views.evaluasi_view, name='misi_evaluasi'),
    path('misi/<int:mission_id>/selesai/', views.selesai_view, name='misi_selesai'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('pengaturan/', views.pengaturan, name='pengaturan'),

    # Admin Panel URLs
    path('panel/', views.admin_dashboard, name='admin_dashboard'),
    path('panel/users/', views.admin_users, name='admin_users'),
    path('panel/users/<int:user_id>/edit/', views.admin_user_edit, name='admin_user_edit'),
    path('panel/users/<int:user_id>/delete/', views.admin_user_delete, name='admin_user_delete'),
    path('panel/missions/', views.admin_missions, name='admin_missions'),
    path('panel/missions/create/', views.admin_mission_create, name='admin_mission_create'),
    path('panel/missions/<int:mission_id>/edit/', views.admin_mission_edit, name='admin_mission_edit'),
    path('panel/missions/<int:mission_id>/delete/', views.admin_mission_delete, name='admin_mission_delete'),
    path('panel/missions/<int:mission_id>/questions/', views.admin_questions, name='admin_questions'),
    path('panel/missions/<int:mission_id>/questions/create/', views.admin_question_create, name='admin_question_create'),
    path('panel/missions/<int:mission_id>/questions/<int:question_id>/delete/', views.admin_question_delete, name='admin_question_delete'),
]
