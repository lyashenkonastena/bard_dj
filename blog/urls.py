from django.urls import path

from .views import (
    BlogList,
    PostDetail,
)

urlpatterns = [
    path('', BlogList.as_view(), name='blog_list'),
    path('<int:pk>', PostDetail.as_view(), name='post_details'),
]
