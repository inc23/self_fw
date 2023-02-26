from fw.urls import Urls
from view import HomePage, Hello

urlpatterns = [
    Urls('^$', HomePage),
    Urls('^/hello$', Hello)
]