from django.urls import path

from users.views import SinginView, LogoutView

app_name = 'users'
urlpatterns = [
    path('signin/', SinginView.as_view(), name='signin'),
    path('logout/', LogoutView.as_view(), name='logout')
]
