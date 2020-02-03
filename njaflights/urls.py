from django.urls import path


from . import views

urlpatterns = [
   path("", views.index, name="index"),
   path("<int:njaflight_id>", views.njaflight, name="njaflight"),
   path("<int:njaflight_id>/book", views.book, name="book"),
]
