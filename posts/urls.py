from django.urls import path
from .views import PostListAPIView, PostRetrieveAPIView


urlpatterns = [
    path('', PostListAPIView.as_view(), name='post-list'),
    path('<int:pk>', PostRetrieveAPIView.as_view(), name='post-detail')
]