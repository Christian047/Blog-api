from django.urls import path
from .views import *

urlpatterns = [
    path('blog/', BlogView.as_view()),
    path('publicblog/', PublicblogView.as_view()),
]
