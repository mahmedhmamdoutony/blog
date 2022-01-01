from django.urls import path
from . import views
from .views import NewPost,UpdatePost,DeletePost

app_name='blog'

urlpatterns = [
    path('',views.blog_home,name='blog_home'),
    path('blog_details/<int:blog_id>/',views.blog_details,name='blog_details'),
    path('new_post/',NewPost.as_view(),name='new_post'),
    path('comment_details/<int:comment_id>/',
         views.comment_detail, name='comment_details'),
    path('comment_all/<int:com_id>/', views.comment_all, name='comment_all'),
    path('new_post/<str:pk>/update/', UpdatePost.as_view(), name='update_post'),
    path('delete_post/<str:pk>/delete/',
         DeletePost.as_view(), name='delete_post'),

         
         
   
]
