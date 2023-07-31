from django.urls import path

from . import views

app_name = "materials"
urlpatterns = [
    path("", views.MaterialListView.as_view(), name="index"),
	path("<int:pk>/", views.MaterialDetailView.as_view(), name="material_detail"),
    path("tags/", views.TagListView.as_view(), name="tag_list"),
	path("tags/<int:pk>/", views.TagDetailView.as_view(), name="tag_detail"),
	path("explore/", views.explore, name="explore"),
]