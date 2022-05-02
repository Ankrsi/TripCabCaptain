from django.contrib import admin
from django.urls import path
from server import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('list/',views.list),
    path('car_lat_long/',views.updateLatLong),
    path('user_lat_long/<str:latlong>',views.nearestcab),
]
