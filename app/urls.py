from django.urls import path
from .apps import AppConfig
from .views import IndexView, ContactView, BlogDetailsView, BlogsView

app_name = AppConfig.name

urlpatterns = [
    path(route="", view=IndexView.as_view(), name=IndexView.get_url_name()),
    path(route="index/", view=IndexView.as_view(), name=IndexView.get_url_name()),
    path(route="contact/", view=ContactView.as_view(), name=ContactView.get_url_name()),
    path(route=f"{BlogDetailsView.get_url_name()}/<int:{BlogDetailsView.blogIdKey}>/", view=BlogDetailsView.as_view(), name=BlogDetailsView.get_url_name()),
    path(route="blogs/", view=BlogsView.as_view(), name=BlogsView.get_url_name()),
    path(route="blogs/<int:page>/", view=BlogsView.as_view(), name=BlogsView.get_url_name()),
]
