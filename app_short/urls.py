from django.urls import path

# Import the home view
from .views import home_view, redirect_url_view,ApiForUrlList,render_api_data

appname = "app_short"

urlpatterns = [
    # Home view
    path("", home_view, name="home"),
    path('<str:shortened_part>', redirect_url_view, name='redirect'),
    # path("url_list/", load_url_list, name="url_list"),
     path('url_api/', ApiForUrlList.as_view()),
     path("url_list/", render_api_data, name="url_list"),
     
]