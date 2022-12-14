import json
from audioop import reverse
from lib2to3.pgen2.token import NOTEQUAL
import re
from django.shortcuts import render, redirect
from requests import post
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from Home.models import *
from .serlizer import *
from django.http import JsonResponse
from .utils import get_friend_request_or_false
from Home.FriendRequestStatus import FriendRequestStatus
from django.http import HttpResponse
from django.db.models import Q
from django.db.models import Count

# Create your views here.
@api_view(['GET'])
def view_users(request):
    id = request.session['user_id']
    if id != 0:
        users = Useraccount.objects.filter(id=id)

    else:
        users = Useraccount.objects.all()

    if users:
        data = userSerializer(users, many=True)
        return Response(data.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def get_all(request):
    if request.session.has_key('user_name'):
        users = Useraccount.objects.all()
        data = userSerializer(users, many=True)
        return Response(data.data)
    else:
        return redirect('/auth/login/')
        
@api_view(['GET'])
def get_Likee(request):
    users = Postlike.objects.all()
    data = LIKE(users, many=True)
    return Response(data.data)

@api_view(['GET'])
def get_Likeeuser(request,id):
    arr=[]

    result = (Postlike.objects.filter(post=id)
            .values('iconId')
            .annotate(dcount=Count('iconId'))
            .order_by()
            )

    for x in  result:
        arr.append(x)
    return JsonResponse(arr, safe=False)
    
@api_view(['GET'])
def get_likee_user_group(request, id):
    arr=[]
    result = (Postlikegroup.objects.filter(post=id)
            .values('iconId')
            .annotate(dcount=Count('iconId'))
            .order_by()
            )
    for x in  result:
        arr.append(x)
    return JsonResponse(arr, safe=False)

@api_view(['GET'])
def get_likee_user_share(request, id):
    arr=[]
    result = (PostlikeShares.objects.filter(post=id)
            .values('iconId')
            .annotate(dcount=Count('iconId'))
            .order_by()
            )
    for x in  result:
        arr.append(x)
    return JsonResponse(arr, safe=False)

#####################   Add New User   ################
@api_view(['delete'])
def delete_like(request, pk):
    trainee = Postlike.objects.get(pk=pk)
    trainee.delete()
    return Response(status=status.HTTP_202_ACCEPTED)


@api_view(['Post'])
def get_Like(request):
    user = LIKE(data=request.data)
    if user.is_valid():
        user.save()
        # return Response(user.data, status=status.HTTP_201_CREATED)
        users = Postlike.objects.all()
        data = LIKE(users, many=True)
        return Response(data.data)
    return Response(user.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['Post'])
def add_share(request):
    user = Share2(data=request.data)
    if user.is_valid():
        user.save()
        return Response(user.data, status=status.HTTP_201_CREATED)
    return Response(user.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_share(request):
    if request.session.has_key('user_name'):

        friendlist=FrienList.objects.filter(
            user=int(request.session['user_id']))
        arr = []
        if friendlist :

            friends= friendlist[0].friends.all()


            for friend in friends:
                posts = reversed(Shares.objects.filter(
                    user=friend))
                for post in posts:
                    arr2 = []
                    photos = Photos.objects.filter(post=post.post)
                    for photo in photos:
                        arr2.append( str(photo))
                    allcomments = post.post_comments_shares.all()
                    comments = []
                    for comment in allcomments:
                        print(comment)
                        comm = comment.user.first_name+" "+comment.user.last_name + \
                            "," + str(comment.user.pic.url) + \
                            "," + comment.commentcontent
                        comments.append(comm)
                    arr.append({
                        'post_id_share':post.id,
                        'post_time_share': post.sharedate,
                        'username_share':post.user.first_name+' '+post.user.last_name,
                        'user_pic_share':str(post.user.pic.url),
                        'user_id_share':post.user.id,
                        'post_username':post.post.user.first_name+' '+post.post.user.last_name,
                        'user_org_pic':str(post.post.user.pic.url),
                        'post_org_id':post.post.id,
                        'body_org':post.post.postcontent,
                        'pic':arr2,
                        'post_org_time':post.post.postdate,
                        'comments': comments,
                    })


        postss = reversed(Shares.objects.filter(
            user=int(request.session['user_id'])))
        for post in postss:
            arr2 = []
            photos = Photos.objects.filter(post=post.post)
            for photo in photos:
                arr2.append(str(photo))
            allcomments = post.post_comments_shares.all()
            comments = []
            for comment in allcomments:
                print(comment)
                comm = comment.user.first_name+" "+comment.user.last_name + \
                    "," + str(comment.user.pic.url) + \
                    "," + comment.commentcontent
                comments.append(comm)
            arr.append({
                'post_id_share': post.id,
                'post_time_share': post.sharedate,
                'username_share': post.user.first_name + ' ' + post.user.last_name,
                'user_pic_share': str(post.user.pic.url),
                'user_id_share': post.user.id,
                'post_username': post.post.user.first_name + ' ' + post.post.user.last_name,
                'user_org_pic': str(post.post.user.pic.url),
                'post_org_id': post.post.id,
                'body_org': post.post.postcontent,
                'pic': arr2,
                'post_org_time': post.post.postdate,
                'comments': comments,
            })

        return JsonResponse(arr, safe=False)

    else:
        return redirect('/auth/login/')






@api_view(['POST'])
def register_user(request):
        user = userSerializer(data=request.data)
        if user.is_valid():
            user.save()
            return Response(user.data, status=status.HTTP_201_CREATED)
        return Response(user.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login_user(request):
    if request.method == 'POST':
        loguser = Useraccount.objects.filter(
            email=request.data['email'], password=request.data['password'])
        arr=[]
        if len(loguser) > 0:
            request.session['user_name'] = loguser[0].first_name + \
                " " + loguser[0].last_name
            request.session['user_id'] = loguser[0].id
            t = Useraccount.objects.get(id=request.session['user_id'])
            t.isactive='True'
            t.save()
            return redirect('/home/Home/')
        else:
            arr.append("invalid login")
            return JsonResponse(arr,safe=False)
            # return redirect('/auth/login/')
    else:
        return render(request, 'index.html')


@api_view(['POST'])
def addpost(request):
        user = Useraccount.objects.filter(
            id=int(request.session['user_id']))[0]
        newPost = Posts.objects.create(
            user=user, postcontent=request.data['postcontent'])
        if newPost:
            try:
                friend_list = FrienList.objects.filter(user=user.id)
                friends = friend_list[0].friends.all()
                for friend in friends:
                    user_receiver = Useraccount.objects.filter(id=friend.id)[0]
                    notify = Notification.objects.create(
                        user=user , body=" Add A new post ",
                        user_receiver= user_receiver ,post=newPost,
                    )
                    notify.save()
                try :
                    if request.data['imagecontent']:
                        photo = Photos.objects.create(
                            post=newPost, imagecontent=request.data['imagecontent'])
                        photo.save()
                    return Response('successsfully')
                except:
                    return Response('successsfully')
            except :
                try :
                    if request.data['imagecontent']:
                        photo = Photos.objects.create(
                            post=newPost, imagecontent=request.data['imagecontent'])
                        photo.save()
                    return Response('successsfully')
                except:
                    return Response('successsfully')



@api_view(['POST'])
def updateprofile(request):
    user = Useraccount.objects.get(id=int(request.session['user_id']))
    try :
            if request.data['pic'] :
                user.pic = request.data['pic']
                user.save()
                newPost = Posts.objects.create(
                    user=user, postcontent="update his profile picture"
                )
                photo = Photos.objects.create(
                    post=newPost,
                    imagecontent=user.pic
                )
                photo.save()
                friend_list = FrienList.objects.filter(user=user.id)
                friends = friend_list[0].friends.all()
                for friend in friends:
                    user_receiver = Useraccount.objects.filter(id=friend.id)[0]
                    notify = Notification.objects.create(
                        user=user, body=" Update His Profile Picture ",
                        user_receiver=user_receiver ,post=newPost
                    )
                    notify.save()
            try :
                if request.data['pic_cover']:
                    user.pic_cover = request.data['pic_cover']
                    user.save()
                    newPost = Posts.objects.create(
                        user=user, postcontent="update his cover picture"
                    )
                    photo = Photos.objects.create(
                        post=newPost,
                        imagecontent=user.pic_cover
                    )
                    photo.save()
                    friend_list = FrienList.objects.filter(user=user.id)
                    friends = friend_list[0].friends.all()
                    for friend in friends:
                        user_receiver = Useraccount.objects.filter(id=friend.id)[0]
                        notify = Notification.objects.create(
                            user=user, body=" Update His Cover Picture ",
                            user_receiver=user_receiver , post = newPost
                        )
                        notify.save()
                return redirect('/home/pro/'+str(request.session['user_id']))
            except:
                return redirect('/home/pro/'+str(request.session['user_id']))
    except:
   
        if request.data['pic_cover'] :
            user.pic_cover = request.data['pic_cover']
            user.save()
            newPost = Posts.objects.create(
                user=user, postcontent="update his cover picture"
            )

            photo = Photos.objects.create(
                post=newPost,
                imagecontent=user.pic_cover
            )
            photo.save()
            friend_list = FrienList.objects.filter(user=user.id)
            friends = friend_list[0].friends.all()
            for friend in friends:
                user_receiver = Useraccount.objects.filter(id=friend.id)[0]
                notify = Notification.objects.create(
                    user=user, body=" Update His Cover Picture ",
                    user_receiver=user_receiver , post=newPost,
                )
                notify.save()
            return redirect('/home/pro/'+str(request.session['user_id']))

@api_view(['GET'])
def postNotification(request):
    
        user_receiver = Useraccount.objects.filter(
            id=int(request.session['user_id']))[0]
        notifications = reversed(Notification.objects.filter(user_receiver=user_receiver , seen=False))
        if notifications:
            data = notifySerializer(notifications, many=True)
            return Response(data.data)
        
    

@api_view(['GET'])
def requestNotification(request):
    if request.session.has_key('user_name'):
        user_receiver = Useraccount.objects.filter(
            id=int(request.session['user_id']))[0]
        NotifyRequest = reversed(NotifyRequest.objects.filter(user_receiver=user_receiver , seen=False))
        if NotifyRequest:
            data = NotifyRequestSerializer(NotifyRequest, many=True)
            return Response(data.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
    else:
        return redirect('/auth/login/')

@api_view(['GET'])
def unseenNotification(request,pk,id):
    if request.session.has_key('user_name'):
        notify = Notification.objects.get(id=pk)
        if notify:
            notify.delete()
            return redirect('/home/Post/'+id)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
    else:
        return redirect('/auth/login/')

        
@api_view(['GET'])
def get_one_post(request,id):
    if request.session.has_key('user_name'):
        post = Posts.objects.filter(id=id)
        if post:
            data = postSerializer(post , many=True)
            return Response(data.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
    else:
        return redirect('/auth/login/')

@api_view(['POST'])
def addcomment(request):
    if request.session.has_key('user_name'):
        comment = commentSerializer(data=request.data)
        if comment.is_valid():
            comment.save()
            return Response(comment.data, status=status.HTTP_201_CREATED)
        return Response(comment.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return redirect('/auth/login/')

@api_view(['PUT'])
def update_user(request, pk):
    if request.session.has_key('user_name'):
        users = Useraccount.objects.get(id=pk)
        data = userSerializer(instance=users, data=request.data)
        print(data)
        if data.is_valid():
            data.save()
            return Response(data.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
    else:
        return redirect('/auth/login/')


@api_view(['delete'])
def delete_user(request, pk):
    if request.session.has_key('user_name'):
        users = Useraccount.objects.get(id=pk)
        users.delete()
        return Response(status=status.HTTP_202_ACCEPTED)
    else:
        return redirect('/auth/login/')

@api_view(['GET'])
def getAllPosts(request):
    if request.session.has_key('user_name'):
        posts = reversed(Posts.objects.all())
        if posts:
            data = postSerializer(posts, many=True)
            return Response(data.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
    else:
        return redirect('/auth/login/')


@api_view(['GET'])
def getProfilePosts(request):
    if request.session.has_key('user_name'):
        posts = reversed(Posts.objects.filter(
            user=int(request.session['user_id'])))
        if posts:
            data = postSerializer(posts, many=True)
            return Response(data.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
    else:
        return redirect('/auth/login/')

@api_view(['GET'])
def getComments(request,pk):
    if request.session.has_key('user_name'):
        post = Posts.objects.filter(id=pk)[0]
        comments = Comments.objects.filter(post = post)


        if comments:
            data = commentSerializer(comments, many=True)
            return Response(data.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
    else:
        return redirect('/auth/login/')

@api_view(['GET'])
def get_one_user(request, id):
    if request.session.has_key('user_name'):
        context = []
        user_pk = id
        try:
            account = Useraccount.objects.get(id=user_pk)
        except:
            return HttpResponse("Something went wrong.")
        if account:
            try:
                friend_list = FrienList.objects.get(user=account)
            except FrienList.DoesNotExist:
                friend_list = FrienList(user=account)
                friend_list.save()
            friends = friend_list.friends.all()
            is_self = True
            is_friend = False
            pending_friend_request_id = ''
            request_sent = FriendRequestStatus.NO_REQUEST_SENT.value  # range: ENUM -> friend/friend_request_status.FriendRequestStatus
            friend_requests = 0
            user_id = int(request.session['user_id'])
            user = Useraccount.objects.get(id=user_id)
            if user != account:
                is_self = False
                if friends.filter(id=user.id):
                    is_friend = True
                else:
                    is_friend = False
                    if get_friend_request_or_false(sender=account, receiver=user) != False:
                        request_sent = FriendRequestStatus.THEM_SENT_TO_YOU.value
                        pending_friend_request_id = get_friend_request_or_false(
                            sender=account, receiver=user).id
                    elif get_friend_request_or_false(sender=user, receiver=account) != False:
                        request_sent = FriendRequestStatus.YOU_SENT_TO_THEM.value
                    else:
                        request_sent = FriendRequestStatus.NO_REQUEST_SENT.value
            else:
                try:
                    friend_requests = FriendRequest.objects.filter(
                        reciver=user, is_active=True).count()
                except:
                    pass
            if account.pic and account.pic_cover :
                context.append({
                    'id': account.id,
                    'friends': friends.count(),
                    'email': account.email,
                    'pic': str(account.pic.url),
                    'pic_cover': str(account.pic_cover.url),
                    'is_self': is_self,
                    'is_friend': is_friend,
                    'user_name': account.first_name+" "+account.last_name,
                    'request_sent': request_sent,
                    'friend_requests': friend_requests,
                    'pending_friend_request_id': pending_friend_request_id,
                    'Bio':account.Bio,
                })
            else:
                context.append({
                    'id': account.id,
                    'friends': friends.count(),
                    'email': account.email,
                    'pic': "",
                    'pic_cover': "",
                    'is_self': is_self,
                    'is_friend': is_friend,
                    'user_name': account.first_name + " " + account.last_name,
                    'friend_requests': friend_requests,
                    'request_sent': request_sent,
                    'pending_friend_request_id': pending_friend_request_id,
                    'Bio': account.Bio,
                })
            print(friend_requests)
            return JsonResponse(data=context, safe=False)
    else:
        return redirect('/auth/login/')


@api_view(['GET'])
def get_one_user_Posts(request, id):
    if request.session.has_key('user_name'):
        posts = reversed(Posts.objects.filter(user=int(id)))
        if posts:
            data = postSerializer(posts, many=True)
            return Response(data.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
    else:
        return redirect('/auth/login/')


@api_view(['GET'])
def friend_requests(request):
    if request.session.has_key('user_name'):
        user_id = int(request.session['user_id'])
        user = Useraccount.objects.get(id=user_id)
        friend_requests = FriendRequest.objects.filter(
            reciver=user, is_active=True)
        data = friendRequestSerializer(friend_requests, many=True)
        return Response(data.data)
    else:
        return redirect('/auth/login/')


@api_view(['GET'])
def friends_list(request, id):
    if request.session.has_key('user_name'):
        user = Useraccount.objects.get(id=id)
        friend_list = FrienList.objects.filter(user=user)
        data = postUserSerial(friend_list[0].friends.all(), many=True)
        return Response(data.data)
    else:
        return redirect('/auth/login/')

@api_view(['GET'])
def friends_list_chat(request):
            user_id = int(request.session['user_id'])
            user = Useraccount.objects.get(id=user_id)
            friend_list = FrienList.objects.filter(user=user)
            data = postUserSerial(friend_list[0].friends.all(), many=True)
            return Response(data.data)

################ chat views ##################
@api_view(['GET'])
def chatIndex(request):
    if request.session.has_key('user_name'):
        user_id = int(request.session['user_id'])
        user = Useraccount.objects.get(id=user_id)
        friend_list = FrienList.objects.filter(user=user)
        data = postUserSerial(friend_list[0].friends.all(), many=True)
        return Response(data.data)
    else:
        return redirect('/auth/login/')


@api_view(['GET'])
def chatNotification(request):
        arr = []
        try :
            user = Useraccount.objects.get(id=int(request.session['user_id']))
            friend_list = FrienList.objects.filter(user=user)
            friends = friend_list[0].friends.all()
            for friend in friends:
                chats = ChatMessage.objects.filter(msg_sender=friend, msg_receiver=user, seen=False)
                if chats.count() > 0 :
                    arr.append(chats.count())
                else : 
                    arr.append(0)
            return JsonResponse(arr, safe=False)
        except:
            return JsonResponse(arr, safe=False)
    



@api_view(['GET','POST'])
def detail(request, pk):
    if request.session.has_key('user_name'):
        user = Useraccount.objects.filter(
            id=int(request.session['user_id']))[0]
        friend_list = FrienList.objects.filter(user=user.id)
        friend = friend_list[0].friends.get(id=pk)
        chats = ChatMessage.objects.all()
        rec_chats = ChatMessage.objects.filter(
            msg_sender=friend, msg_receiver=user, seen=False)
        rec_chats.update(seen=True)
        data = ChatMessagesel(chats, many=True) 
        return Response(data.data)
    else:
        return redirect('/auth/login/')


@api_view(['GET'])
def detail_counter(request, pk):
    if request.session.has_key('user_name'):
        user = Useraccount.objects.get(
            id=int(request.session['user_id']))
        friend = Useraccount.objects.get(id=pk)
        chats = ChatMessage.objects.filter(
            msg_sender=friend, msg_receiver=user)
        return JsonResponse(chats.count(), safe=False)
    else:
        return redirect('/auth/login/')


@api_view(['POST'])
def sentMessages(request, pk):
    if request.session.has_key('user_name'):
        data = ChatMessagesel(data=request.data)
        if data.is_valid():
            data.save()
            return Response(data.data)
        return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return redirect('/auth/login/')

@api_view(['GET'])
def receivedMessages(request, pk):
    if request.session.has_key('user_name'):
        user = Useraccount.objects.filter(
            id=int(request.session['user_id']))[0]
        friend_list = FrienList.objects.filter(user=user.id)
        friend = friend_list[0].friends.get(id=pk)
        arr = []
        chats = ChatMessage.objects.filter(
            msg_sender=friend, msg_receiver=user)
        for chat in chats:
            arr.append(chat.body)
        chats.update(seen=True)
        return JsonResponse(arr, safe=False)
    else:
        return redirect('/auth/login/')


@api_view(['POST'])
def addStory(request):
    if request.session.has_key('user_name'):
        data = Storyserializer(data=request.data)
        if data.is_valid():
            data.save()
            return Response(data.data)
        return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return redirect('/auth/login/')

@api_view(['GET'])
def story(request):
    if request.session.has_key('user_name'):
        user = Useraccount.objects.get(id=int(request.session['user_id']))
        mystorys = Story.objects.filter(user=user)
        arr = []
        for st in mystorys:

            if st.pic:
                arr.append({
                    "story_id": st.id,
                    "story_pic": str(st.pic.url),
                    "story_body": st.body,
                    "user_pic": str(st.user.pic.url),
                    "user_name": st.user.first_name + " " + st.user.last_name,
                    "user_id": st.user.id,
                    "is_mine": True,
                })
            else:
                arr.append({
                    "story_id": st.id,
                    "story_body": st.body,
                    "user_pic": str(st.user.pic.url),
                    "user_name": st.user.first_name + " " + st.user.last_name,
                    "user_id": st.user.id,
                    "is_mine": True,
                })
        try:
            friend_list = FrienList.objects.filter(user=user)
        except FrienList.DoesNotExist:
            friend_list = FrienList(user=user)
            friend_list.save()
        try:
            friends = friend_list[0].friends.all()
            for friend in friends:
                storys = Story.objects.filter(user=friend)
                for story in storys:
                    if story.pic:
                        arr.append({
                            "story_id": story.id,
                            "story_pic": str(story.pic.url),
                            "story_body": story.body,
                            "user_pic": str(story.user.pic.url),
                            "user_name": story.user.first_name+" "+story.user.last_name,
                            "user_id": story.user.id,
                            "is_mine": False,
                        })
                    else:
                        arr.append({
                            "story_id": story.id,
                            "story_body": story.body,
                            "user_pic": str(story.user.pic.url),
                            "user_name": story.user.first_name+" "+story.user.last_name,
                            "user_id": story.user.id,
                            "is_mine": False,
                        })
        except:
            pass
        return JsonResponse(arr, safe=False)
    else:
        return redirect('/auth/login/')

@api_view(['DELETE'])
def deleteStory(request,pk):
    if request.session.has_key('user_name'):
        story = Story.objects.get(pk=pk)
        story.delete()
        return Response(status=status.HTTP_202_ACCEPTED)
    else:
        return redirect('/auth/login/')


@api_view(['GET'])
def get_all_users(request,name):
    if request.session.has_key('user_name'):
        context = []
        user_pk = id
        myuser = Useraccount.objects.get(id=int(request.session['user_id']))
        # users = Useraccount.objects.all()
        users = Useraccount.objects.filter(
            Q(first_name__icontains=name) | Q(last_name__icontains=name))
        if myuser:
            try:
                friend_list = FrienList.objects.get(user=myuser)
            except FrienList.DoesNotExist:
                friend_list = FrienList(user=myuser)
                friend_list.save()
        friends = friend_list.friends.all()
        for user in users:
            is_self = True
            is_friend = False
            pending_friend_request_id = ''
            request_sent = FriendRequestStatus.NO_REQUEST_SENT.value
            friend_requests = 0
            if user != myuser:
                is_self = False
                if friends.filter(id=user.id):
                    is_friend = True
                else:
                    is_friend = False
                    if get_friend_request_or_false(sender=user, receiver=myuser) != False:
                        request_sent = FriendRequestStatus.THEM_SENT_TO_YOU.value
                        pending_friend_request_id = get_friend_request_or_false(
                            sender=user, receiver=myuser).id
                    elif get_friend_request_or_false(sender=myuser, receiver=user) != False:
                        request_sent = FriendRequestStatus.YOU_SENT_TO_THEM.value
                    else:
                        request_sent = FriendRequestStatus.NO_REQUEST_SENT.value
            else:
                try:
                    friend_requests = FriendRequest.objects.filter(
                        reciver=myuser, is_active=True).count()
                except:
                    pass
            if user.pic :
                context.append({
                    'id': user.id,
                    'friends': friends.count(),
                    'email': user.email,
                    'pic': str(user.pic.url),
                    'is_self': is_self,
                    'is_friend': is_friend,
                    'user_name': user.first_name+" "+user.last_name,
                    'request_sent': request_sent,
                    'friend_requests': friend_requests,
                    'pending_friend_request_id': pending_friend_request_id,
                    'Bio': user.Bio,
                })
            else :
                context.append({
                    'id': user.id,
                    'friends': friends.count(),
                    'email': user.email,
                    'is_self': is_self,
                    'is_friend': is_friend,
                    'user_name': user.first_name+" "+user.last_name,
                    'request_sent': request_sent,
                    'friend_requests': friend_requests,
                    'pending_friend_request_id': pending_friend_request_id,
                    'Bio': user.Bio,
                })
        return JsonResponse(data=context, safe=False)
    else:
        return redirect('/auth/login/')

@api_view(['GET'])
def friends_list_contacts(request):
    if request.session.has_key('user_name'):
        user_id = int(request.session['user_id'])
        user = Useraccount.objects.get(id=user_id)
        friend_list = FrienList.objects.filter(user=user)
        data = postUserSerial(friend_list[0].friends.all(), many=True)
        return Response(data.data)
    else:
        return redirect('/auth/login/')


@api_view(['GET'])
def sugistions_list(request):
    if request.session.has_key('user_name'):
        user = Useraccount.objects.get(id=request.session['user_id'])
        arr=[]
        try:
            friend_list = FrienList.objects.get(user=user)
            print("iam heree")
            friends = friend_list.friends.all()
            users = Useraccount.objects.filter(~Q(id=user.id))
            for use in users:
                if friends.filter(id=use.id).exists():
                    pass 
                else :
                    pending_friend_request_id = ''
                    request_sent = FriendRequestStatus.NO_REQUEST_SENT.value
                    if get_friend_request_or_false(sender=use, receiver=user) != False:
                        request_sent = FriendRequestStatus.THEM_SENT_TO_YOU.value
                        pending_friend_request_id = get_friend_request_or_false(
                            sender=use, receiver=user).id
                    elif get_friend_request_or_false(sender=user, receiver=use) != False:
                        request_sent = FriendRequestStatus.YOU_SENT_TO_THEM.value
                    else:
                        request_sent = FriendRequestStatus.NO_REQUEST_SENT.value
                    arr.append(
                        {
                            'user_name': use.first_name+" "+use.last_name,
                            'user_id': use.id,
                            'user_pic': str(use.pic.url),
                            'user_email': use.email,
                            'request_sent': request_sent,
                            'pending_friend_request_id': pending_friend_request_id,
                        }
                    )
        except FrienList.DoesNotExist:
            friend_list = FrienList(user=user)
            friend_list.save()
            friends = Useraccount.objects.filter(~Q(id=user.id))
            for friend in friends:
                pending_friend_request_id = ''
                request_sent = FriendRequestStatus.NO_REQUEST_SENT.value
                if get_friend_request_or_false(sender=friend, receiver=user) != False:
                    request_sent = FriendRequestStatus.THEM_SENT_TO_YOU.value
                    pending_friend_request_id = get_friend_request_or_false(
                        sender=friend, receiver=user).id
                elif get_friend_request_or_false(sender=user, receiver=friend) != False:
                    request_sent = FriendRequestStatus.YOU_SENT_TO_THEM.value
                else:
                    request_sent = FriendRequestStatus.NO_REQUEST_SENT.value
                arr.append(
                    {
                        'user_name': friend.first_name+" "+friend.last_name,
                        'user_id': friend.id,
                        'user_pic': str(friend.pic.url),
                        'user_email': friend.email,
                        'request_sent': request_sent,
                        'pending_friend_request_id': pending_friend_request_id,
                    }
                )
        return JsonResponse(arr, safe=False)
    else:
        return redirect('/auth/login/')


################# for group #############
@api_view(['GET'])
def get_group(request,id):
    if request.session.has_key('user_name'):
        group = Groups.objects.filter(id=id)
        data = GetGroupSerializer(group, many=True)
        print(data)
        return Response(data.data)
    else:
        return redirect('/auth/login/')


@api_view(['GET'])
def get_user_for_group(request,id):
    if request.session.has_key('user_name'):
        user_id = int(request.session['user_id'])
        user = Useraccount.objects.get(id=user_id)
        group = Groups.objects.get(id=id)
        print(group.owner)
        members = group.members.all()
        arr=[]
        is_member = False
        is_owner = False
        if members.filter( id=user.id ):
            is_member = True
        else:
            is_member = False
        if user == group.owner:
            is_owner = True
        else :
            is_owner = False
        arr.append({
            "user_id":user.id,
            "user_name":user.first_name+" "+user.last_name,
            "user_pic":str(user.pic.url),
            "is_member": is_member,
            "is_owner": is_owner,
        })
        return JsonResponse(arr, safe=False)
    else:
        return redirect('/auth/login/')


@api_view(['POST'])
def addpostforgroups(request):
    if request.session.has_key('user_name'):
        user_id = int(request.session['user_id'])
        user = Useraccount.objects.get(id=user_id)
        data = PostsGroupsSerializer(data=request.data)
        if data.is_valid():
            data.save()
            return Response(data.data)
        return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return redirect('/auth/login/')


@api_view(['GET'])
def getpostforgroup(request,id):
    if request.session.has_key('user_name'):
        posts= reversed(PostsGroups.objects.filter(group=id))
        data = PostsGroupsSerializerget(posts, many=True)
        return Response(data.data)
    else:
        return redirect('/auth/login/')


@api_view(['GET'])
def get_likee_group(request):
    likes = Postlikegroup.objects.all()
    data = LIKEGroup(likes, many=True)
    return Response(data.data)

@api_view(['GET'])
def get_likee_share(request):
    likes = PostlikeShares.objects.all()
    data = LIKEshare(likes, many=True)
    return Response(data.data)

@api_view(['delete'])
def delete_like_group(request, pk):
    like = Postlikegroup.objects.get(pk=pk)
    like.delete()
    return Response(status=status.HTTP_202_ACCEPTED)

@api_view(['delete'])
def delete_like_share(request, id):
    like = PostlikeShares.objects.get(id=id)
    like.delete()
    return Response(status=status.HTTP_202_ACCEPTED)


@api_view(['Post'])
def get_like_group(request):
    like = LIKEGroup(data=request.data)
    if like.is_valid():
        like.save()
        likes = Postlikegroup.objects.all()
        data = LIKEGroup(likes, many=True)
        return Response(data.data)
    return Response(like.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['Post'])
def get_like_share(request):
    like = LIKEshare(data=request.data)
    if like.is_valid():
        like.save()
        likes = PostlikeShares.objects.all()
        data = LIKEshare(likes, many=True)
        return Response(data.data)
    return Response(like.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['Post'])
def invite(request):
    if request.session.has_key('user_name'):
        payload = []
        try:
            # Get any friend requests (active and not-active)
            invite_requests = NotificationInvite.objects.filter(
                user=request.data['user'], Invit_receiver=request.data['Invit_receiver'])
            # print(request.data.reciver,">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
            # find if any of them are active (pending)
            try:
                    for request in invite_requests:
                        if request.seen == False :
                            raise Exception(
                                "You already sent them a friend request.")
                    # If none are active create a new friend request
                    invite = NotificationInviteGroup(data=request.data)
                    if invite.is_valid():
                        invite.save()
                        return Response(invite.data, status=status.HTTP_201_CREATED)
                    
            except Exception as e:
                    payload['response'] = str(e)
        except NotificationInvite.DoesNotExist:
            invite = NotificationInviteGroup(data=request.data)
            if invite.is_valid():
                invite.save()
                return Response(invite.data, status=status.HTTP_201_CREATED)
        return Response(invite.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return redirect('/auth/login/')



@api_view(['POST'])
def addcommentGroup(request):
    if request.session.has_key('user_name'):
        comment = commentSerializergroup(data=request.data)
        if comment.is_valid():
            comment.save()
            return Response(comment.data, status=status.HTTP_201_CREATED)
        return Response(comment.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return redirect('/auth/login/')

@api_view(['POST'])
def leave_group(request):
    if request.session.has_key('user_name'):
        pk = int(request.data['group_id'])
        sender = Useraccount.objects.get(id=request.data['user_id'])
        group = Groups.objects.get(id=pk)
        members = group.remove_member(sender)
        return redirect('/home/Home/')
    else:
        return redirect('/auth/login/')


@api_view(['POST'])
def delete_request(request):
    if request.session.has_key('user_name'):
        member_request = MemberRequest.objects.get(
            id=int(request.data['request_id']))
        member_request.delete()
        return redirect('/home/group/'+str(request.data['group_id']))
    else:
        return redirect('/auth/login/')


@api_view(['POST'])
def accept_request(request):
    if request.session.has_key('user_name'):
        pk = int(request.data['group_id'])
        sender = Useraccount.objects.get(id=request.data['user_id'])
        group = Groups.objects.get(id=pk)
        members = group.add_member(sender)
        member_request = MemberRequest.objects.get(
            id=int(request.data['request_id']))
        member_request.delete()
        return redirect('/home/group/'+str(request.data['group_id']))
    else:
        return redirect('/auth/login/')

@api_view(['POST'])
def frined_request_delete_notify(request):
    if request.session.has_key('user_name'):
        friend_request = FriendRequest.objects.get(
            sender=request.data['sender_id'], reciver=request.data['user_id'])
        friend_request.delete()
        notify = NotifyRequest.objects.get(id=request.data['notify_id'])
        if notify:
            notify.delete()
        return redirect('/home/Home')
    else:
        return redirect('/auth/login/')

@api_view(['POST'])
def frined_request_accept_notify(request):
    if request.session.has_key('user_name'):
        user = Useraccount.objects.get(id=int(request.session['user_id']))
        user_friend_list = FrienList.objects.get(user=user)
        sender = Useraccount.objects.get(id=request.data['sender_id'])
        sender_friend_list = FrienList.objects.get(user=sender)
        sender_friend_list.add_friend(user)
        user_friend_list.add_friend(sender)
        friend_request = FriendRequest.objects.get(
            sender=request.data['sender_id'], reciver=request.data['user_id'])
        friend_request.delete()
        notify = NotifyRequest.objects.get(id=request.data['notify_id'])
        if notify:
            notify.delete()
        return redirect('/home/Home')
    else:
        return redirect('/auth/login/')

@api_view(['POST'])
def frined_request_delete(request):
    if request.session.has_key('user_name'):
        friend_request = FriendRequest.objects.get(
            id=int(request.data['request_id']))
        friend_request.delete()
        notify = NotifyRequest.objects.get(user=request.data['user_id'],user_receiver=int(request.data['request_id']))
        if notify:
            notify.delete()
        return redirect('/home/friendRequests')
    else:
        return redirect('/auth/login/')


@api_view(['POST'])
def send_friend_request(request):
    user = Useraccount.objects.get(id=int(request.session['user_id']))
    payload = {}
    if request.session.has_key('user_name'):
        user_id = request.data['reciver_id']
        if user_id:
            receiver = Useraccount.objects.get(pk=user_id)
            try:
                # Get any friend requests (active and not-active)
                friend_requests = FriendRequest.objects.filter(
                    sender=user, reciver=receiver)
                # find if any of them are active (pending)
                try:
                    for request in friend_requests:
                        if request.is_active:
                            raise Exception(
                                "You already sent them a friend request.")
                    # If none are active create a new friend request
                    friend_request = FriendRequest(
                        sender=user, reciver=receiver)
                    friend_request.save()
                    notify = NotifyRequest.objects.create(
                        user=user, body=" Send You Friend Request ",
                        user_receiver=receiver
                    )
                    notify.save()
                    payload['response'] = "Friend request sent."
                    return redirect('/home/pro/'+str(request.data['reciver_id']))
                except Exception as e:
                    payload['response'] = str(e)
                    return redirect('/home/pro/'+str(request.data['reciver_id']))
            except FriendRequest.DoesNotExist:
                # There are no friend requests so create one.
                friend_request = FriendRequest(
                    sender=user, reciver=receiver)
                friend_request.save()
                notify = Notification.objects.create(
                    user=user, body=" Send You Friend Request ",
                    user_receiver=receiver
                )
                notify.save()
                payload['response'] = "Friend request sent."
                return redirect('/home/pro/'+str(request.data['reciver_id']))
        else:
            # this return need to change to
            return redirect('/auth/login/')
    else:
        return redirect('/auth/login/')


@api_view(['POST'])
def cancel_friend_request(request):
    if request.session.has_key('user_name'):
        user = Useraccount.objects.get(id=int(request.session['user_id']))
        receiver = Useraccount.objects.get(id=request.data['reciver_id'])
        friend_requests = FriendRequest.objects.filter(
            sender=user,reciver=receiver, is_active=True)
        if len(friend_requests) > 1:
            for request in friend_requests:
                request.cancel()
        friend_requests.delete()
        try :
            notify = NotifyRequest.objects.get(user=user,user_receiver=receiver)
            if notify:
                notify.delete()
        except:
            pass
        return redirect('/home/pro/'+str(request.data['reciver_id']))
    else:
        return redirect('/auth/login/')

@api_view(['POST'])
def cancel_friend_request_sugestions(request):
    if request.session.has_key('user_name'):
        user = Useraccount.objects.get(id=int(request.session['user_id']))
        receiver = Useraccount.objects.get(id=request.data['reciver_id'])
        friend_requests = FriendRequest.objects.filter(
            sender=user,reciver=receiver, is_active=True)
        if len(friend_requests) > 1:
            for request in friend_requests:
                request.cancel()
        friend_requests.delete()
        try :
            notify = NotifyRequest.objects.get(user=user,user_receiver=receiver)
            if notify:
                notify.delete()
        except:
            pass
        return redirect('/home/sugistions_list/')
    else:
        return redirect('/auth/login/')


@api_view(['POST'])
def frined_request_delete_sugustions(request):
    if request.session.has_key('user_name'):
        user = Useraccount.objects.get(id=int(request.session['user_id']))
        friend_request = FriendRequest.objects.get(
            id=int(request.data['request_id']))
        friend_request.delete()
        try :
            notify = NotifyRequest.objects.get(user=request.data['sender_id'],user_receiver=user)
            if notify:
                notify.delete()
        except:
            pass
        try:
            if request.data['pro'] == 1 :
                return redirect('/home/pro/'+str(request.data['sender_id']))
        except:
            return redirect('/home/sugistions_list/')
    else:
        return redirect('/auth/login/')

        
@api_view(['POST'])
def frined_request_accept_sugustions(request):
    if request.session.has_key('user_name'):
        user = Useraccount.objects.get(id=int(request.session['user_id']))
        user_friend_list = FrienList.objects.get(user=user)
        sender = Useraccount.objects.get(id=request.data['sender_id'])
        sender_friend_list = FrienList.objects.get(user=sender)
        sender_friend_list.add_friend(user)
        user_friend_list.add_friend(sender)
        friend_request = FriendRequest.objects.get(
            id=request.data['request_id'])
        friend_request.delete()
        try :
            notify = NotifyRequest.objects.get(user=request.data['sender_id'],user_receiver=user)
            if notify:
                notify.delete()
        except:
            pass
        try:
            if request.data['pro'] == 1 :
                return redirect('/home/pro/'+str(request.data['sender_id']))
        except:
            return redirect('/home/sugistions_list/')
    else:
        return redirect('/auth/login/')


@api_view(['POST'])
def frined_request_accept(request):
    if request.session.has_key('user_name'):
        user = Useraccount.objects.get(id=int(request.session['user_id']))
        user_friend_list = FrienList.objects.get(user=user)
        sender = Useraccount.objects.get(id=request.data['sender_id'])
        sender_friend_list = FrienList.objects.get(user=sender)
        sender_friend_list.add_friend(user)
        user_friend_list.add_friend(sender)
        friend_request = FriendRequest.objects.get(
            id=request.data['request_id'])
        friend_request.delete()
        return redirect('/home/friendRequests')
    else:
        return redirect('/auth/login/')


@api_view(['POST'])
def unfriend(request):
    if request.session.has_key('user_name'):
        pk = int(request.session['user_id'])
        user = Useraccount.objects.get(id=pk)
        removee = Useraccount.objects.get(id=request.data['unfriend'])
        friend_list = FrienList.objects.get(user=user)
        friend_list.unfriend(removee)
        return redirect('/home/pro/' + str(request.data['unfriend']))
    else:
        return redirect('/auth/login/')

@api_view(['POST'])
def AddBio(request):
    if request.session.has_key('user_name'):
        user = Useraccount.objects.get(id=int(request.session['user_id']))
        user.Bio = request.data['BioInput']
        user.save()
        return redirect('/home/pro/'+str(request.session['user_id']))
    else:
        return redirect('/auth/login/')


@api_view(['POST'])
def addcommentshare(request):
    if request.session.has_key('user_name'):
        comment = commentSerializershare(data=request.data)
        if comment.is_valid():
            comment.save()
            return Response(comment.data, status=status.HTTP_201_CREATED)
        return Response(comment.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return redirect('/auth/login/')


################################# send request to join ############################3
@api_view(['POST'])
def joinGroup(request):
    if request.session.has_key('user_name'):
        payload = []
        try:
                # Get any friend requests (active and not-active)
                member_requests = MemberRequest.objects.filter(
                    sender=request.data['sender'], reciver=request.data['reciver'])
                # print(request.data.reciver,">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
                # find if any of them are active (pending)
                try:
                    for request in member_requests:
                        if request.is_active:
                            raise Exception(
                                "You already sent them a friend request.")
                    # If none are active create a new friend request
                    reques = MemberRequestSerializergroup(data=request.data)
                    if reques.is_valid():
                        reques.save()
                        return Response(reques.data, status=status.HTTP_201_CREATED)
                    payload['response'] = "Friend request sent."
                except Exception as e:
                    payload['response'] = str(e)
        except MemberRequest.DoesNotExist:
                # There are no friend requests so create one.
                reques = MemberRequestSerializergroup(data=request.data)
                if reques.is_valid():
                    reques.save()
                    return Response(reques.data, status=status.HTTP_201_CREATED)
        return Response(reques.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return redirect('/auth/login/')


########################### get requests to join ######################
@api_view(['GET'])
def joinrequests(request,pk):
    if request.session.has_key('user_name'):
        reques=MemberRequest.objects.filter(reciver=pk)
        data = getRequestSerializergroup(reques, many=True)
        return Response(data.data)
    else:
        return redirect('/auth/login/')


########################### accept requests to join ######################
@api_view(['GET'])
def friends_list_group(request, pk):
    if request.session.has_key('user_name'):
        user = Useraccount.objects.get(id=int(request.session['user_id']))
        user_id = int(request.session['user_id'])
        user = Useraccount.objects.get(id=user_id)
        friend_list = FrienList.objects.filter(user=user)
        group = Groups.objects.get(id=pk)
        friends = friend_list[0].friends.all()
        data = []
        for friend in friends:
            if group.is_mutual_member(friend) or group.owner == friend:
                print("yes")
            else :
                data.append(
                    {
                        'friend_id': friend.id,
                        'friend_name': friend.first_name+" "+friend.last_name,
                        'friend_pic': str(friend.pic.url),
                    }
                )
        return JsonResponse(data, safe=False)
    else:
        return redirect('/auth/login/')


@api_view(['GET'])
def get_all_users_group(request, pk):
    if request.session.has_key('user_name'):
        group = Groups.objects.get(id=pk)
        members=group.members.all()
        data = ShareUserSerial(members, many=True)
        return Response(data.data)
    else:
        return redirect('/auth/login/')


@api_view(['GET'])
def inviteNotification(request):
    if request.session.has_key('user_name'):
        user_receiver = Useraccount.objects.filter(
            id=int(request.session['user_id']))[0]
        notifications = reversed(NotificationInvite.objects.filter(
            Invit_receiver=user_receiver, seen=False))
        if notifications:
            data = NotificationInviteshow(notifications, many=True)
            return Response(data.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
    else:
        return redirect('/auth/login/')


@api_view(['GET'])
def unseeninviteNotification(request, pk, id):
    if request.session.has_key('user_name'):
        notify = NotificationInvite.objects.get(id=pk)
        if notify:
            notify.delete()
            return redirect('/home/group/'+id)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
    else:
        return redirect('/auth/login/')


@api_view(['POST'])
def createGroups(request):
    if request.session.has_key('user_name'):
        group = createGroup(data=request.data)
        if group.is_valid():
            group.save()
            return Response(group.data, status=status.HTTP_201_CREATED)
        return Response(group.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return redirect('/auth/login/')


@api_view(['GET'])
def checkheader(request):
    arr =[]
    try :
        ise = request.session.has_key('user_name')
        if ise:
            arr.append(True)
            return JsonResponse(arr,safe=False)
        else:
            arr.append(False)
            return JsonResponse(arr,safe=False)
    except : 
        arr.append(False)
        return JsonResponse(arr,safe=False)


@api_view(['POST'])
def removeGroup(request):
    if request.session.has_key('user_name'):
        group = Groups.objects.get(id=request.data['id'])
        if group:
            group.delete()
            return redirect('/home/Home/')
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
    else:
        return redirect('/auth/login/')


@api_view(['GET'])
def getGroups(request):
    if request.session.has_key('user_name'):
        user = Useraccount.objects.get(id=int(request.session['user_id']))
        arr=[]
        groups = Groups.objects.all()
        for group in groups:
            if group.is_mutual_member(user):
                arr.append(
                    {
                        'group_id' :group.id,
                        'group_name': group.group_name,
                        'group_pic': str(group.group_pic.url),
                    }
                )
        return JsonResponse(arr, safe=False)
    else:
        return redirect('/auth/login/')


@api_view(['GET'])
def ownGroups(request):
    if request.session.has_key('user_name'):
        user = Useraccount.objects.get(id=int(request.session['user_id']))
        arr = []
        groups = Groups.objects.all()
        for group in groups:
            if group.owner == user:
                arr.append(
                    {
                        'group_id': group.id,
                        'group_name': group.group_name,
                        'group_pic': str(group.group_pic.url),
                    }
                )
        return JsonResponse(arr, safe=False)
    else:
        return redirect('/auth/login/')


@api_view(['GET'])
def sugustionsGroups(request):
    if request.session.has_key('user_name'):
        user = Useraccount.objects.get(id=int(request.session['user_id']))
        arr = []
        groups = Groups.objects.all()
        for group in groups:
            if group.is_mutual_member(user) or group.owner == user:
                print("yes")
            else:
                arr.append(
                    {
                        'group_id': group.id,
                        'group_name': group.group_name,
                        'group_pic': str(group.group_pic.url),
                    }
                )
        return JsonResponse(arr, safe=False)
    else:
        return redirect('/auth/login/')



@api_view(['GET'])
def getGroupPost(request):
    if request.session.has_key('user_name'):
        user = Useraccount.objects.get(id=int(request.session['user_id']))
        arr = []
        groups = Groups.objects.all()
        for group in groups:
            if group.is_mutual_member(user) or group.owner == user:
                posts = group.groupPosts.all()[:2]
                for post in posts:
                    allcomments = post.post_comments_group.all()
                    print(allcomments)
                    comments = []
                    for comment in allcomments :
                        print(comment)
                        comm=comment.user.first_name+" "+comment.user.last_name+"," + str(comment.user.pic.url)+","+ comment.commentcontent
                        comments.append(comm)

                    arr.append({
                        'user_pic': str(post.user.pic.url),
                        'username': post.user.first_name + ' ' + post.user.last_name,
                        'post_id': post.id,
                        'post_timestamp': post.postdate,
                        'postcontent': post.postcontent,
                        'post_pic': str(post.images.url),
                        'group_id': group.id,
                        'user_id': post.user.id,
                        'group_pic': str(group.group_pic.url),
                        'group_name': group.group_name,
                        'comments': comments,
                    })
        return JsonResponse(arr, safe=False)
    else:
        return redirect('/auth/login/')


@api_view(['GET'])
def notifyRequest(request):
    if request.session.has_key('user_name'):
        user_receiver = Useraccount.objects.filter(
            id=int(request.session['user_id']))[0]
        notifications = reversed(NotifyRequest.objects.filter(
            user_receiver=user_receiver, seen=False))
        if notifications:
            data = NotifyRequestshow(notifications, many=True)
            return Response(data.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
    else:
        return redirect('/auth/login/')


@api_view(['GET'])
def unseennotifyRequest(request, pk, id):
    if request.session.has_key('user_name'):
        notify = NotifyRequest.objects.get(id=pk)
        if notify:
            notify.delete()
            return redirect('/home/pro/'+id)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
    else:
        return redirect('/auth/login/')
