from django.urls import path
from . import views

urlpatterns = [
    path("get/", views.getbooks),
    path("getpage/<int:bookId>/<int:pageNumber>/", views.sendpage),
    path("setstack/", views.setStack),
    path("getstack/<int:book_id>/<str:page>/", views.getStack),
    path("setmarkups/", views.receiveMarkups),
    path("getbook/<int:bookId>/", views.getwholebook),
    path("getloadedbooks/", views.getloadedbooks),
    # path("getpage/<int:bookId>/<int:pageNumber>/", views.getPages),
]
