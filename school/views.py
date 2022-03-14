import datetime

from django.http import HttpResponse
from django.shortcuts import render, redirect

from .pyrebase_settings import *


def index(request):
    # name = database.child('Data').child('Name').get().val()
    # stack = database.child('Data').child('Stack').get().val()
    # framework = database.child('Data').child('Framework').get().val()
    context = {
        # 'name': name,
        # 'stack': stack,
        # 'framework': framework
    }
    return render(request, 'student/index.html', context)


def index_2(request):
    return render(request, 'student/index-2.html')


def index_3(request):
    return render(request, 'student/index-3.html')


def index_4(request):
    return render(request, 'student/index-4.html')


def about(request):
    return render(request, 'student/events.html')


def events(request):
    return render(request, 'student/events.html')


def blog(request):
    global light, image, content, author, tags

    blogposts = database.child('blog').get()
    yup = database.child('blog').child('blog-1').child('tags').get()
    for i in blogposts.each():
        i.key()
        light = list(i.val().values())[4]
        image = list(i.val().values())[2]
        content = list(i.val().values())[1]
        author = list(i.val().values())[0]
    for j in yup.each():
        tags = j.val()

    context = {
        'blogpost': blogposts,
        'blogTitle': light,
        'image': image,
        'content': content,
        'author': author,
        'tags': tags,
    }
    return render(request, 'blog/blog.html', context)


def courses(request):
    return render(request, 'student/courses.html')


def contact(request):
    return render(request, 'student/contact.html')


def shop(request):
    return render(request, 'student/shop.html')


def single_shop(request):
    return render(request, 'student/shop-single.html')


def single_blog(request):
    return render(request, 'blog/blog-single.html')


def single_course(request):
    return render(request, 'student/courses-single.html')


def single_events(request):
    return render(request, 'student/events-single.html')


def dashboard(request):
    context = {}
    return render(request, 'student/studentDashboard.html', context)


def teachers(request):
    return render(request, 'student/teachers.html')


def teacher_single(request):
    return render(request, 'student/teachers-single.html')


def login(request):
    auth = firebase.auth()
    email = request.POST.get('email')
    password = request.POST.get('password')
    if request.POST:
        auth.sign_in_with_email_and_password(email, password)
        redirect('s-dashboard')
    return render(request, 'student/login.html')


def register(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    if request.POST:
        authed.create_user_with_email_and_password(email, password)
    return render(request, 'student/register.html')


def logout(request):
    return None


def blog_summit(request):
    context = {
        "apiKey": env("F_API"),
        "authDomain": env("F_AUTH_DOMAIN"),
        "databaseURL": env("F_DATABASE_URL"),
        "projectId": env("F_PROJECT_ID"),
        "storageBucket": env("F_STORAGE_BUCKET"),
        "messagingSenderId": env("F_MESSAGING_SENDER_ID"),
        "appId": env("F_APP_ID"),
        "measurementId": env("F_MEASUREMENT_ID")
    }
    if request.method == 'POST':
        file = request.POST.get('first_image')
        title = request.POST.get('blog_title')
        title_converted = str(title).lower().replace(' ', '-')
        storage.child(file).put(f'{title_converted}-{file}')
        url = storage.child(file).get_url(None)
        date = f'{datetime.datetime.now().strftime("%d")} ' \
               f'{datetime.datetime.now().strftime("%b")}' \
               f' {datetime.datetime.now().strftime("%Y")}'
        data = {
            "author": "Manka Velda",
            "content": "lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod, Lorem ipsum"
                       " dolor sit amet, consectetur adipisicing elit. Alias culpa deleniti est exercitationem"
                       " fuga laudantium libero magnam mollitia nemo nostrum, nulla odio, porro possimus quia"
                       " quisquam ratione suscipit tempora vel.",
            "first-image-path": url,
            'date': date,
            "tags": {
                "Education": "Education",
                "Technology": "Technology",
                "Business": "Business",
                "Marketing": "Marketing",
            },
            "title": title,
        }
        storage.child(file).put(title)
        database.child('blog').push(data)
        return HttpResponse('success')
    return render(request, 'blog/blog-summit.html', context)
