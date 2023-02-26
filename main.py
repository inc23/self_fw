import os
from fw.main import FrameWork
from urls import urlpatterns
from fw.middleware import middleware

settings = {
    'BASE_DIR': os.path.dirname(os.path.abspath(__file__)),
    'TEMPLATE_DIR_NAME': 'templates'
}

app = FrameWork(urls=urlpatterns, settings=settings, middleware=middleware)