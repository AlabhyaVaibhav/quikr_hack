from django.urls import path
from .views import (
    FirebaseListApiView, FirebaseCreateNodeApiView, FirebaseCreateNodeV2, FirebaseCreateNodeV3
)


urlpatterns = [
    path('', FirebaseListApiView.as_view()),
    path('v1/node', FirebaseCreateNodeApiView.as_view()),
    path('v2/node', FirebaseCreateNodeV2.as_view()), # increased prices
    path('v3/node', FirebaseCreateNodeV3.as_view()), # decreased prices
]
