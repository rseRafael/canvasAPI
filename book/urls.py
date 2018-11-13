from django.urls import path
from . import views


getters = [
    path("getbooks/", views.getBooks), #retrieves a json with all books informations
    path("getmarkups/<int:bookId>/<int:page>/", views.getMarkups),
    path("getpage/<int:bookId>/<int:pageNumber>/", views.getPage),
]

setters = [
    path("setmarkups/", views.setMarkups),
]
urlpatterns = getters + setters