from django.shortcuts import render
from .models import Post, Signup, Author

def index(request):
    featured = Post.objects.filter(featured=True)
    latest = Post.objects.order_by('-timestamp')[0:3]

    # basic new letter user save
    if request.method == "POST":
        email = request.POST["email"]
        new_signup = Signup()
        new_signup.email = email
        new_signup.save()
    
    context = {
        'object_list': featured,
        'latest':latest
    }
    return render(request,'myBlog/index.html', context)