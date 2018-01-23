from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.signup, name='signup'),
    path('login', auth_views.LoginView.as_view(template_name='hub/accounts/login.html'), name='login'),
    path('logout', auth_views.LogoutView.as_view(), name='logout'),

    path('account', views.UserUpdateView.as_view(), name='account'),
    path('account/change-password', auth_views.PasswordChangeView.as_view(template_name='hub/accounts/pw_change.html'),
         name='pw_change'),
    path('account/change-password/complete',
         auth_views.PasswordChangeDoneView.as_view(template_name='hub/accounts/pw_change_complete.html'),
         name='pw_change_complete'),

    path('reset', auth_views.PasswordResetView.as_view(template_name='hub/accounts/pw_reset.html',
                                                       email_template_name='hub/accounts/pw_reset_email.html',
                                                       subject_template_name='hub/accounts/pw_reset_email_title.txt'),
         name='pw_reset'),
    path('reset/email-sent',
         auth_views.PasswordResetDoneView.as_view(template_name='hub/accounts/pw_reset_email_sent.html'),
         name='pw_reset_email_sent'),
    path(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
         auth_views.PasswordResetConfirmView.as_view(template_name='hub/accounts/pw_reset_from_emailed_link.html'),
         name='pw_reset_from_emailed_link'),
    path('reset/complete',
         auth_views.PasswordResetCompleteView.as_view(template_name='hub/accounts/pw_reset_complete.html'),
         name='pw_reset_complete'),
]
