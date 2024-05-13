from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from .models import Post, Category, Comments, Contact, Tag


def home_view(request):
    categories = Category.objects.all()
    tags = Tag.objects.all()
    posts = Post.objects.filter(is_published=True)
    more_posts = posts.order_by('-views')[:4]
    banner_posts = posts.order_by('-views')[:3]
    latest_posts = posts.order_by('-created_at')[:3]
    data = request.GET
    page = data.get('page', 1)
    page_obj = Paginator(posts, 2)

    context = {
        'tags': tags,
        'more_posts': more_posts,
        'latest_posts': latest_posts,
        'banner_posts': banner_posts,
        'posts': page_obj.get_page(page),
        'categories': categories,
        'home': 'active'
    }

    return render(request, 'index.html', context=context)


def blog_view(request):
    categories = Category.objects.all()
    d = {
        'categories': categories
    }
    return render(request, 'blog.html', context=d)


def about_view(request):
    posts = Post.objects.filter(is_published=True)
    categories = Category.objects.all()
    category = Category.objects.filter().first()
    latest_posts = posts.order_by('-created_at')[:3]
    d = {
        'latest_posts': latest_posts,
        'about': 'active',
        'category': category,
        'categories': categories
    }
    return render(request, 'about.html', context=d)


def category_view(request):
    posts = Post.objects.filter(is_published=True)
    latest_posts = posts.order_by('-created_at')[:3]
    tags = Tag.objects.all()
    categories = Category.objects.all()
    data = request.GET
    cat = data.get('cat', None)
    page = data.get('page', 1)

    if cat:
        cat_name = categories.filter(id=cat).first()
        posts = Post.objects.filter(is_published=True, category_id=cat)
        d = {
            'tags': tags,
            'latest_posts': latest_posts,
            'categories': categories,
            'posts': posts,
            'cat_name': cat_name,
            'category': 'active'
        }
        return render(request, 'category.html', context=d)
    else:
        posts = Post.objects.filter(is_published=True)

    page_obj = Paginator(posts, 2)

    d = {
        'category': 'active',
        'blog': 'active',
        'posts': page_obj.get_page(page),
        'categories': categories
    }
    return render(request, 'category.html', context=d)


def contact_view(request):
    posts = Post.objects.filter(is_published=True)
    latest_posts = posts.order_by('-created_at')[:3]
    categories = Category.objects.all()
    if request.method == 'POST':
        data = request.POST
        obj = Contact.objects.create(name=data['name'],
                                     email=data['email'],
                                     phone=data['phone'],
                                     message=data['message'])
        obj.save()
        return redirect('/contact')
    d = {
        'latest_posts': latest_posts,
        'categories': categories,
        'contact': 'active'
    }
    return render(request, 'contact.html', context=d)


def blog_detail_view(request, pk):
    posts = Post.objects.filter(is_published=True)
    latest_posts = posts.order_by('-created_at')[:3]
    categories = Category.objects.all()
    tags = Tag.objects.filter(id=pk)
    if request.method == 'POST':
        data = request.POST
        comment = Comments.objects.create(post_id=pk, name=data['name'], email=data['email'], message=data['message'])
        comment.save()
        return redirect(f'/blog/{pk}')
    post = Post.objects.filter(id=pk).first()
    post.views += 1
    post.save(update_fields=['views'])
    comments = Comments.objects.filter(post_id=pk)
    context = {
        'latest_posts': latest_posts,
        'tags': tags,
        'post': post,
        'comments': comments,
        'categories': categories,
        'category': 'active'
    }
    return render(request, 'blog-single.html', context=context)


def search_view(request):
    if request.method == 'POST':
        data = request.POST
        query = data['query']
        return redirect(f'/search?q={query}')
    query = request.GET.get('q')
    if query is not None and len(query) >= 1:
        posts = Post.objects.filter(is_published=True, title__icontains=query)
    else:
        posts = Post.objects.filter(is_published=True)
    d = {
        'posts': posts
    }

    return render(request, 'category.html', context=d)

def tag_view(request, pk):
    post = Post.objects.filter(is_published=True)
    more_posts = post.order_by('-views')[:4]
    tags = Tag.objects.all()
    tag = Tag.objects.get(id=pk)
    tag_post = Post.objects.filter(tag=tag)
    d = {
        'more_posts': more_posts,
        'tags': tags,
        'posts': tag_post,
        'tag': tag
    }

    return render(request, 'index.html', context=d)
# def tag_posts_view(request, pk):
#     tag = Tag.objects.all()
#     latest_posts = Post.objects.filter(is_published=True).order_by('-created_at')[:3]
#     categories = Category.objects.all()
#     tag = Tag.objects.get(pk=pk)
#     newest_posts = Post.objects.filter(is_published=True).order_by('-created_at')[:6]
#
#     tag_posts = Post.objects.filter(tags=tag)
#     return render(request, 'index.html', {'tag': tag, 'posts': tag_posts, 'categories': categories, 'tag': tag,
#                                           'latest_posts': latest_posts, 'newest_posts': newest_posts})