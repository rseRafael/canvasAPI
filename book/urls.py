from django.urls import path
from . import views

getters = [
    path("getbooks/", views.getBooks),  # retrieves a json with all books informations
    path("getmarkups/<int:bookId>/<int:pageNumber>/", views.getMarkups),
    path("getpage/<int:bookId>/<int:pageNumber>/", views.getPage),
    # path("getmarkups2/<int:bookId>/<int:pageNumber>/", views.getMarkups2),
]
setters = [
    path("setmarkups/", views.setMarkups),
]
urlpatterns = getters + setters
