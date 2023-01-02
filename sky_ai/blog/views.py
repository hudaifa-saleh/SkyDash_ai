from django.shortcuts import render



def blog_topic(request):
     context = {}
     
     return render(request, 'blog/blog_topic.html', context)