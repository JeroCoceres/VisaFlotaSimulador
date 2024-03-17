from django.urls import path

from django_base.views import index
from costcenter.views import create_transaction,test 

urlpatterns = [
    path("new_transaction/", create_transaction, name="create_transaction"),
    path("test/",test)
]

