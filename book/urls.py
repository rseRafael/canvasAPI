from django.urls import path
from . import views
urlpatterns = [
    path("get/", views.getbooks ),
    path("setstack/", views.setStack),
    path("getstack/<int:book_id>/<str:page>/", views.getStack),
]