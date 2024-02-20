from django.urls import path
from core import views

urlpatterns = [
    #Hello
    path('', views.HelloView.as_view(), name='hello'),
    #Register
    path('signup/',views.signup,name='signup'),
    #Login
    path('login/',views.signin,name='signin'),
    #Logout
    path('signout/',views.signout,name='signout'),

    #notes
    path('notes/create/',views.NotesView.as_view(),name='notescreate'),
    path('notes/<int:nid>/',views.NotesView.as_view(),name='notesrud'),
    path('notes/version-history/<int:nid>/',views.NotesVHView.as_view(),name='notesvh'),
    path('notes/share/',views.NotesShareView.as_view(),name='noteshare')
]
