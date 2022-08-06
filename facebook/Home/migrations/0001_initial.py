# Generated by Django 4.0.6 on 2022-08-06 03:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Groups',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group_name', models.TextField()),
                ('group_pic', models.ImageField(blank=True, null=True, upload_to='img')),
                ('About_group', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pagename', models.CharField(max_length=20)),
                ('pagecontent', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Posts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('postdate', models.DateTimeField(auto_now_add=True)),
                ('postcontent', models.TextField()),
                ('islike', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Useraccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=50, unique=True)),
                ('password', models.CharField(max_length=255)),
                ('phone_number', models.CharField(blank=True, max_length=11)),
                ('birthdate', models.DateField()),
                ('gender', models.CharField(choices=[('m', 'Male'), ('f', 'Female')], max_length=20)),
                ('pic', models.ImageField(blank=True, default='img/defaultpic.png', null=True, upload_to='img')),
                ('pic_cover', models.ImageField(blank=True, default='img/defaultpic.png', null=True, upload_to='img')),
                ('address', models.CharField(max_length=100, null=True)),
                ('location', models.CharField(max_length=100, null=True)),
                ('Bio', models.CharField(max_length=300, null=True)),
                ('isactive', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Story',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pic', models.ImageField(blank=True, null=True, upload_to='img')),
                ('body', models.TextField(blank=True, null=True)),
                ('timesstamp', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Home.useraccount')),
            ],
        ),
        migrations.CreateModel(
            name='Shares',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sharedate', models.DateTimeField(auto_now_add=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Home.posts')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Home.useraccount')),
            ],
        ),
        migrations.CreateModel(
            name='PostsGroups',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('postdate', models.DateTimeField(auto_now_add=True)),
                ('postcontent', models.TextField(blank=True, null=True)),
                ('images', models.ImageField(blank=True, null=True, upload_to='img')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='groupPosts', to='Home.groups')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Home.useraccount')),
            ],
        ),
        migrations.AddField(
            model_name='posts',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Home.useraccount'),
        ),
        migrations.CreateModel(
            name='PostlikeShares',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('iconId', models.IntegerField()),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Home.shares')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Home.useraccount')),
            ],
        ),
        migrations.CreateModel(
            name='Postlikegroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('iconId', models.IntegerField()),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Home.postsgroups')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Home.useraccount')),
            ],
        ),
        migrations.CreateModel(
            name='Postlike',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('iconId', models.IntegerField()),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Home.posts')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Home.useraccount')),
            ],
        ),
        migrations.CreateModel(
            name='Photos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagecontent', models.ImageField(blank=True, null=True, upload_to='img')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_photos', to='Home.posts')),
            ],
        ),
        migrations.CreateModel(
            name='Pageslike',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Home.page')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Home.useraccount')),
            ],
        ),
        migrations.CreateModel(
            name='NotifyRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField(blank=True, null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('seen', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_sender_NotifyRequest', to='Home.useraccount')),
                ('user_receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_receiver_NotifyRequest', to='Home.useraccount')),
            ],
        ),
        migrations.CreateModel(
            name='NotificationInvite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField(blank=True, null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('seen', models.BooleanField(default=False)),
                ('Invit_receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Invit_reciver', to='Home.useraccount')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Home.groups')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Invit_user', to='Home.useraccount')),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField(blank=True, null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('seen', models.BooleanField(default=False)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_notifications', to='Home.posts')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_sender', to='Home.useraccount')),
                ('user_receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_receiver', to='Home.useraccount')),
            ],
        ),
        migrations.CreateModel(
            name='MemberRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timesstamp', models.DateTimeField(auto_now_add=True)),
                ('reciver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='group_sender_req', to='Home.groups')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='group_sender_req', to='Home.useraccount')),
            ],
        ),
        migrations.AddField(
            model_name='groups',
            name='members',
            field=models.ManyToManyField(blank=True, related_name='members', to='Home.useraccount'),
        ),
        migrations.AddField(
            model_name='groups',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Home.useraccount'),
        ),
        migrations.CreateModel(
            name='FrienList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('friends', models.ManyToManyField(blank=True, related_name='friends', to='Home.useraccount')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user', to='Home.useraccount')),
            ],
        ),
        migrations.CreateModel(
            name='FriendRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(blank=True, default=True)),
                ('timesstamp', models.DateTimeField(auto_now_add=True)),
                ('reciver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reciver', to='Home.useraccount')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sender', to='Home.useraccount')),
            ],
        ),
        migrations.CreateModel(
            name='CommentsShares',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('commentdate', models.DateTimeField(auto_now_add=True)),
                ('commentcontent', models.TextField()),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_comments_shares', to='Home.shares')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Home.useraccount')),
            ],
        ),
        migrations.CreateModel(
            name='Commentsgroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('commentdate', models.DateTimeField(auto_now_add=True)),
                ('commentcontent', models.TextField()),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_comments_group', to='Home.postsgroups')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Home.useraccount')),
            ],
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('commentdate', models.DateTimeField(auto_now_add=True)),
                ('commentcontent', models.TextField()),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_comments', to='Home.posts')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Home.useraccount')),
            ],
        ),
        migrations.CreateModel(
            name='Commentlikes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Home.comments')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Home.useraccount')),
            ],
        ),
        migrations.CreateModel(
            name='ChatMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField()),
                ('seen', models.BooleanField(default=False)),
                ('msg_receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='msg_receiver', to='Home.useraccount')),
                ('msg_sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='msg_sender', to='Home.useraccount')),
            ],
        ),
    ]
