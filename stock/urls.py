from django.contrib import admin
from django.urls import path
from order.views import view_stocks

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', view_stocks, name="view_stocks"),
]
