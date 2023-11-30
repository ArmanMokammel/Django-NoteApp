from django.urls import path
from UserData import views

app_name = 'UserData'

urlpatterns = [
    path('', views.landingPage, name='landing_page'),
    path('login/', views.login, name="login"),
    path('signup/', views.signup, name="signup"),
    path('logout/', views.logout, name="logout"),
    path('notes_home/<str:username>', views.notes_home, name="notes_home"),
    path('create_note/<str:username>', views.add_note, name="add_note"),
    path('note_description/<str:username>/<str:id>', views.note_description, name="note_description"),
    path('note_description/<str:username>/<str:id>/update', views.update_note, name='update_note'),
    path('note_description/<str:username>/<str:id>/delete', views.delete_note, name='delete_note')
]