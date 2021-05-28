from django.shortcuts import render, redirect, HttpResponse
from .models import *
from django.contrib import messages


def index(request):
    return render(request, 'index.html')


def register(request):
    errors = User.objects.validate(request.POST)
    if len(errors) > 0:
        for k, v in errors.items():
            messages.error(request, v)
        return redirect('/')
    newUser = User.objects.create(
        firstName=request.POST['firstName'], lastName=request.POST['lastName'], email=request.POST['email'], password=request.POST['password'])
    request.session['user'] = newUser.firstName
    request.session['id'] = newUser.id
    request.session['email'] = newUser.email
    return redirect('/success')


def login(request):
    user = User.objects.filter(email=request.POST['email'])
    # if not User.objects.validate(request.POST['email'], request.POST['password']):
    #     messages.error(request, 'Invalid email and/or password')
    #     return redirect('/')
    if len(user) > 0:
        user = user[0]
        if user.password == request.POST['password']:
            request.session['user'] = user.firstName.capitalize()
            request.session['id'] = user.id
            request.session['email'] = user.email
            return redirect('/success')
    return redirect('/')


def logout(request):
    request.session.flush()
    return redirect('/')


def success(request):
    if 'user' not in request.session:
        return redirect('/')
    context = {
        'users': User.objects.all(),
        'messages': Message.objects.all()
    }
    return render(request, 'success.html', context)


def postMessage(request):
    Message.objects.create(user=User.objects.get(
        id=request.session['id']), message=request.POST['message'])
    return redirect('/success')


def addComment(request, id):
    user = User.objects.get(id=request.session['id'])
    message = Message.objects.get(id=id)
    Comment.objects.create(
        message=message, user=user, comment=request.POST['comment'])
    return redirect('/success')


def deleteComment(request, id):
    comment = Comment.objects.get(id=id)
    comment.delete()
    return redirect('/success')
