from django.urls import path
from django.contrib.auth.views import LoginView
from django.contrib.auth import views as auth_view
from django.views.generic.base import TemplateView


from . import views

app_name = 'user'
urlpatterns = [
    path('sign_up/', views.sign_up, name='sign_up'),
    path('login/', LoginView.as_view(template_name='user/login.html'), name='sign_in'),
    path('logout/', views.log_out, name='log_out'),
    path('active/<uidb64>/<token>/', views.active, name='active'),
    path('profile/<int:user_id>/', views.profile, name='profile'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('all_post_user/<int:post_id>/',
         views.all_post_user, name='all_post_user'),
    path('show_post_foruser/<int:post_id>/',
         views.show_post_foruser, name='show_post_foruser'),

    # reset password here
    path('password_reset/', auth_view.PasswordResetView.as_view(
         template_name='user/registrations/password_reset_form.html',
          email_template_name='user/registrations/password_reset_email.html',
          success_url='password_reset_email_confirm'), name='password_reset'),
         path('password_reset/password_reset_email_confirm/',TemplateView.as_view(
         template_name='user/registrations/password_reset_done.html'),
         name='password_reset_done'),     
    path('password_reset_confirm/<uidb64>/<token>/',
         auth_view.PasswordResetConfirmView.as_view(
              template_name='user/registrations/password_reset_confirm.html',
          success_url='/user/password_reset_complete'), name='password_reset_confirm'),

    path('password_reset_complete/', auth_view.PasswordResetCompleteView.as_view(
         template_name='user/registrations/password_reset_complete.html'
          ), name='password_reset_complete')

]
