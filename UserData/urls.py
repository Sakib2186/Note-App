from django.urls import path
from UserData import views
app_name='UserData'

urlpatterns = [
    path('',views.landingPage,name='landing_page'),
    path('login/',views.login,name='login'),
    path('signup/',views.signup,name='signup'),
    path('logout/',views.logout,name='logout'),
    path('notes/<str:username>',views.notes_home,name='notes_home'),
    path('create_note/<str:username>',views.add_note,name='add_note'),
    path('details/<int:pk>', views.note_description, name='note_description'),
    path('edit/<int:pk>',views.notes_edit,name="notes_edit")
]
