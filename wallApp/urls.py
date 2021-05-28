from django.urls import path
from . import views
urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('success', views.success),
    path('postMessage', views.postMessage),
    path('login', views.login),
    path('logout', views.logout),
    path('addComment/<int:id>', views.addComment),
    path('deleteComment/<int:id>', views.deleteComment)
]
