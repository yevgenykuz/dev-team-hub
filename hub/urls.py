from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('search', views.search, name='search'),
    path('signup', views.signup, name='signup'),
    path('login', auth_views.LoginView.as_view(template_name='hub/accounts/login.html'), name='login'),
    path('logout', auth_views.LogoutView.as_view(), name='logout'),

    path('account', views.UserUpdateView.as_view(), name='account'),
    path('account/change-password', auth_views.PasswordChangeView.as_view(template_name='hub/accounts/pw_change.html'),
         name='password_change'),
    path('account/change-password/done',
         auth_views.PasswordChangeDoneView.as_view(template_name='hub/accounts/pw_change_complete.html'),
         name='password_change_done'),

    path('reset-password',
         auth_views.PasswordResetView.as_view(template_name='hub/accounts/pw_reset.html',
                                              email_template_name='hub/accounts/pw_reset_email.html',
                                              subject_template_name='hub/accounts/pw_reset_email_title.txt'),
         name='password_reset'),
    path('reset-password/email-sent',
         auth_views.PasswordResetDoneView.as_view(template_name='hub/accounts/pw_reset_email_sent.html'),
         name='password_reset_done'),
    path('reset-password/confirm/<uidb64>/<token>',
         auth_views.PasswordResetConfirmView.as_view(template_name='hub/accounts/pw_reset_confirm.html'),
         name='password_reset_confirm'),
    path('reset-password/complete',
         auth_views.PasswordResetCompleteView.as_view(template_name='hub/accounts/pw_reset_complete.html'),
         name='password_reset_complete'),
]
