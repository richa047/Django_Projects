from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm
from django.core.mail import send_mail


def post_list(request):
    object_list = Post.published.all()
    paginator = Paginator(object_list, 3) #3 posts in each page
    page = request.GET.get('page')
    try:
        posts= paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        #If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request,
                  'blog/post/list.html',
                  {'page':page,
                   'posts': posts})

'''def post_list(request):
    posts = Post.published.all()
    return render(request, 'blog/post/list.html',{'posts':posts})'''

# Create your views here.
def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                                   status='published',
                                   publish_year=year,
                                   publish_month=month,
                                   publish_day= day)
    return render(request,'blog/post/detail.html',{'posts':posts})

#class based view
class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'

def post_share(request, post_id):
    #Retrive post by Id
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False

    if request.method == 'POST':
       # Form was submitted
       form = EmailPostForm(request.POST)
       if form.is_valid():
           # Form fields passed validation
           cd = form.cleaned_data
           post_url = request.build_absolute_uri(post.get_absolute_url())
           subject = '{} ({}) recommends you reading "{}"'.format(cd['name'], cd['email'], post.title)
           message = 'Read "{}" at {}\n\n{}\'s comments:{}'.format(post.title, post_url, cd['name'], cd['comments']) 
           send_mail(subject, message, 'rpricha4@gmail.com', [cd['to']])
           sent = True
          

           #post_url = request.
           #...send email
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post':post, 'form':form, 'sent':sent })