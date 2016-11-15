from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from urllib.parse import quote

from .models import Post
from .forms import PostForm, ContactForm

# Create your views here.


@login_required()
def post_create(request):
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, 'Dodano nowy wpis')
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        'form': form,
        'title': 'Nowy post'
    }
    return render(request, 'post_form.html', context)


def post_list(request):
    if request.user.is_authenticated:
        photos_list = Post.objects.all()    # display all photos to authenticated user
    else:
        photos_list = Post.objects.filter(private=False)  # display only non private photos

    paginator = Paginator(photos_list, 6)  # Show 6 contacts per page

    page = request.GET.get('page')
    try:
        photos_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        photos_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        photos_list = paginator.page(paginator.num_pages)

    context = {
        'photos_list': photos_list,
        'title': 'Galeria'
    }
    return render(request, 'post_list.html', context)


def post_detail(request, slug):
    instance = get_object_or_404(Post, slug=slug)
    share_title = quote(instance.title)
    share_text = quote(instance.text)

    context = {
        'photo': instance,
        'title': instance.title,
        'share_title': share_title,
        'share_text': share_text,
    }
    return render(request, 'post_detail.html', context)


@login_required()
def post_update(request, slug):
    instance = get_object_or_404(Post, slug=slug)
    form = PostForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, 'Wpis został zaktualizowany')
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        'photo': instance,
        'title': "Edycja " + instance.title,
        'form': form
    }
    return render(request, 'post_form.html', context)


@login_required()
def post_delete(request, slug):
    instance = get_object_or_404(Post, slug=slug)
    instance.delete()
    messages.success(request, 'Wpis został usunięty')
    return redirect("posts:list")


def contact(request):
    form = ContactForm(request.POST or None)
    if form.is_valid():
        form_email = form.cleaned_data.get("email")
        form_message = form.cleaned_data.get("message")
        form_full_name = form.cleaned_data.get("full_name")
        subject = 'Site contact from %s' % form_full_name
        message = '%s, \n\n %s \n %s' % (form_message, form_full_name, form_email)
        from_email = settings.EMAIL_HOST_USER
        to_email = ['abialczak@interia.pl']
        send_mail(subject, message, from_email, to_email, fail_silently=True)
        messages.success(request, 'Wiadomość wysłana')
        return redirect("posts:list")

    context = {
        'form': form,
    }
    return render(request, 'contact.html', context)


def about(request):
    return render(request, 'about.html', {})


@login_required()
def logout_view(request):
    logout(request)
    return redirect("posts:list")