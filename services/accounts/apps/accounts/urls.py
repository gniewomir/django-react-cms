from django.urls import path

from .views import UserView

urlpatterns = [
    path('user/', UserView.as_view({'post': 'create'}), name='users'),
    path('user/<uuid:pk>/', UserView.as_view({'get': 'retrieve', 'patch': 'update', 'delete': 'destroy'}), name='user-single'),
]
