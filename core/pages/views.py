from django.http import HttpResponse
from django.shortcuts import HttpResponseRedirect, reverse, render
def index(request):
    return HttpResponseRedirect(reverse('post-list'))
def about(request):
    # return HttpResponse('About Us')
    return render(request, "pages/about.html")