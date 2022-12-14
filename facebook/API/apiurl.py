"""DjangoD4 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.Home, name='Home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='Home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .views import *
from rest_framework.response import Response
from rest_framework import status
from .serlizer import *

urlpatterns = [
    path('get/', view_users),
    path('register_user/', register_user),
    path('update_user/<pk>', update_user),
    path('delete_user/<pk>', delete_user),
    path('getAllPosts/', getAllPosts),
    path('getProfilePosts/', getProfilePosts),
    path('getComments/<pk>', getComments),
    path('friend_requests/', friend_requests),
    path('friends_list_chat/', friends_list_chat, name='friends_list_chat'),
    path('friends_list/<id>',friends_list,name='friends_list'),
    path('get_one_user/<id>', get_one_user, name='get_one_user'),
    path('get_one_user_Posts/<id>', get_one_user_Posts, name='get_one_user_Posts'),
    path('get_all/', get_all, name='get_all'),
    path('detail/<pk>', detail, name='detail'),
    path('detail_counter/<pk>', detail_counter, name='detail_counter'),
    path('chatIndex/', chatIndex, name="chatIndex"),
    path('chatNotification/', chatNotification, name="chatNotification"),
    path('sent_msg/<str:pk>', sentMessages, name="sent_msg"),
    path('rec_msg/<str:pk>', receivedMessages, name="rec_msg"),
    path('story/', story, name="story"),
    path('get_all_users/<name>', get_all_users, name="get_all_users"),
    path('addStory/', addStory, name="addStory"),
    path('get_like/', get_Like, name='get_like'),
    path('get_likee/', get_Likee, name='get_like'),
    path('get_likee_user/<id>/', get_Likeeuser, name='get_like'),
    path('delete_like/<pk>', delete_like, name='del_like'),
    path('addpost/', addpost, name='addpost'),
    path('addcomment/', addcomment, name='addcomment'),
    path('friends_list_contacts/', friends_list_contacts, name='friends_list_contacts'),
    path('addshare/',add_share,name='shares'),
    path('getshare/', get_share, name='sharess'),
    path('updateprofile/', updateprofile, name='updateprofile'),
    path('deleteStory/<pk>', deleteStory, name='deleteStory'),
    path('sugistions_list/', sugistions_list, name='sugistions_list'),
    path('postNotification/',postNotification , name='postNotification'),
    path('unseenNotification/<pk>/<id>/', unseenNotification, name='unseenNotification'),
    path('get_one_post/<id>', get_one_post, name='get_one_post'),
    path('get_group/<id>', get_group, name='get_group'),
    path('get_user_for_group/<id>', get_user_for_group, name='get_user_for_group'),
    path('addpostforgroups/', addpostforgroups, name='addpostforgroups'),
    path('getpostforgroup/<id>', getpostforgroup, name='getpostforgroup'),
    path('get_like_group/', get_like_group, name='get_like_group'),
    path('get_likee_group/', get_likee_group, name='get_likee_group'),
    path('requestNotification/', requestNotification, name='requestNotification'),
    path('delete_like_group/<pk>', delete_like_group, name='delete_like_group'),
    path('addcommentGroup/', addcommentGroup, name='addcommentGroup'),
    path('joinGroup/', joinGroup, name='joinGroup'),
    path('joinrequests/<pk>', joinrequests, name='joinrequests'),
    path('friends_list_group/<pk>', friends_list_group, name='friends_list_group'),
    path('invite/', invite, name='invite'),
    path('get_all_users_group/<pk>',get_all_users_group, name='get_all_users_group'),
    path('inviteNotification/', inviteNotification, name='inviteNotification'),
    path('unseeninviteNotification/<pk>/<id>/',unseeninviteNotification, name='unseeninviteNotification'),
    path('removeGroup/', removeGroup, name='removeGroup'),
    path('getGroups/', getGroups, name='getGroups'),
    path('ownGroups/', ownGroups, name='ownGroups'),
    path('createGroup/', createGroups, name='createGroup'),
    path('sugustionsGroups/', sugustionsGroups, name='sugustionsGroups'),
    path('getGroupPost/', getGroupPost, name='getGroupPost'),
    path('get_likee_user_group/<id>/',get_likee_user_group, name='get_likee_user_group'),
    path('addcommentshare/', addcommentshare, name='addcommentshare'),
    path('delete_like_share/<id>/', delete_like_share, name='delete_like_share'),
    path('get_likee_user_share/<id>/',get_likee_user_share, name='get_likee_user_share'),
    path('get_likee_share/', get_likee_share, name='get_likee_share'),
    path('get_like_share/', get_like_share, name='get_like_share'),
    path('notifyRequest/', notifyRequest, name='notifyRequest'),
    path('unseennotifyRequest/<pk>/<id>/',unseennotifyRequest, name='unseennotifyRequest'),
    path('login_user/',login_user, name='login_user'),
    path('leave_group/',leave_group, name='leave_group'),
    path('delete_request/',delete_request, name='delete_request'),
    path('accept_request/',accept_request, name='accept_request'),
    path('frined_request_delete_notify/',frined_request_delete_notify, name='frined_request_delete_notify'),
    path('frined_request_accept_notify/',frined_request_accept_notify, name='frined_request_accept_notify'),
    path('frined_request_delete/',frined_request_delete, name='frined_request_delete'),
    path('frined_request_accept/',frined_request_accept, name='frined_request_accept'),
    path('send_friend_request/',send_friend_request, name='send_friend_request'),
    path('cancel_friend_request/',cancel_friend_request, name='cancel_friend_request'),
    path('frined_request_delete_sugustions/',frined_request_delete_sugustions, name='frined_request_delete_sugustions'),
    path('frined_request_accept_sugustions/',frined_request_accept_sugustions, name='frined_request_accept_sugustions'),
    path('cancel_friend_request_sugestions/',cancel_friend_request_sugestions, name='cancel_friend_request_sugestions'),
    path('unfriend/',unfriend, name='unfriend'),
    path('AddBio/',AddBio, name='AddBio'),
    path('checkheader/',checkheader, name='checkheader'),
]

