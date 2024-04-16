from django.urls import path

from . import views

app_name = 'user'

urlpatterns = [
    path(
        'profile', views.profile, name='profile'
    ),
    path(
        'orders', views.orders, name='orders'
    ),
    path(
        'cart', views.cart, name='cart'
    ),
    path(
        'favorite', views.favorite, name='favorite'
    ),
]

"""Авторизация"""
urlpatterns += [
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    # path(
    #     'logout/',
    #     LogoutView.as_view(template_name='users/logged_out.html'),
    #     name='logout'
    # ),
    # path(
    #     'password_change/',
    #     PasswordChangeView.as_view(
    #         template_name='users/password_change_form.html',
    #         success_url=reverse_lazy('users:password_change_done')
    #     ),
    #     name='password_change_form'
    # ),
    # path(
    #     'password_change/done/',
    #     PasswordChangeDoneView.as_view(
    #         template_name='users/password_change_done.html'
    #     ),
    #     name='password_change_done'
    # ),
    # path(
    #     'password_reset/',
    #     PasswordResetView.as_view(
    #         template_name='users/password_reset_form.html',
    #         success_url=reverse_lazy('users:password_reset_done')
    #     ),
    #     name='password_reset_form'
    # ),
    # path(
    #     'password_reset/done/',
    #     PasswordResetDoneView.as_view(
    #         template_name='users/password_reset_done.html'
    #     ),
    #     name='password_reset_done'
    # ),
    # path(
    #     'reset/<str:uidb64>/<str:token>/',
    #     PasswordResetConfirmView.as_view(
    #         template_name='users/password_reset_confirm.html'
    #     ),
    #     name='password_reset_confirm'
    # ),
    # path(
    #     'reset/done/',
    #     PasswordResetCompleteView.as_view(
    #         template_name='users/password_reset_complete.html'
    #     ),
    #     name='password_reset_complete'
    # ),
]
