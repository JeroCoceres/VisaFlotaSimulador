from django.urls import path
from django.contrib.auth.views import LogoutView
from users.views import login_view, register, logout_view
from users.views import admin_edit_users,admin_bulk_add_users,admin_complete_user_details, delete_user

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/',admin_bulk_add_users, name='register'),

    path("admin/users/edit/", admin_edit_users, name="admin_edit_users"),
    path("register/details/",admin_complete_user_details, name=''),
    path('admin/users/delete/<int:user_id>/', delete_user, name='delete_user'),



]