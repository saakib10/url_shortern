from django.urls import path

# Import the home view
from . import views

appname = "authentication"

urlpatterns = [
    # Home view
    path("sign_up/", views.sign_up_form , name="sign_up"),
    path("login/", views.log_in , name="login"),
    path('log_out/',views.log_out, name = 'logout'),
]