from django.urls import path
from . import views
urlpatterns = [
    path("get/", views.getbooks ),
    path("getpage/<int:bookId>/<int:pageNumber>/", views.getPages2 ),
    path("setstack/", views.setStack),
    path("getstack/<int:book_id>/<str:page>/", views.getStack),
    path("setmarkups/", views.receiveMarkups),
    path("getpage/<int:book_id>/<int:page>"),
    #path("getpage/<int:bookId>/<int:pageNumber>/", views.getPages),
]