from django.urls import path

from .views import (
    AdList,
    AdDetail,
    AdCreate,
    AdEdit,
    AdDelete,
    ReplyDetail,
    ReplyCreate,
    ReplyEdit,
    ReplyDelete,
    ReplyAcceptDecline,
)

urlpatterns = [
    path('', AdList.as_view(), {'personal': False}, name='ad_list'),
    path('<int:pk>', AdDetail.as_view(), name='ad_details'),
    path('create/', AdCreate.as_view(), name='ad_create'),
    path('<int:pk>/edit', AdEdit.as_view(), name='ad_edit'),
    path('<int:pk>/delete', AdDelete.as_view(), name='ad_delete'),
    path('personal/', AdList.as_view(), {'personal': True}, name='ad_list_personal'),
    path('<int:ad_pk>/reply/create', ReplyCreate.as_view(), name='reply_create'),
    path('reply/<int:pk>', ReplyDetail.as_view(), name='reply_details'),
    path('reply/<int:pk>/edit', ReplyEdit.as_view(), name='reply_edit'),
    path('reply/<int:pk>/delete', ReplyDelete.as_view(), name='reply_delete'),
    path('reply/<int:pk>/accept', ReplyAcceptDecline.as_view(), name='reply_accept'),
    path('reply/<int:pk>/decline', ReplyAcceptDecline.as_view(), name='reply_decline'),
]
