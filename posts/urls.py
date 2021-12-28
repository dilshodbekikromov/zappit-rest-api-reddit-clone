from django.conf.urls import include
from django.urls import path
from posts import views
urlpatterns = [
    path('api/post' , views.PostList.as_view() , name="Just a little change ") , 
    path('api/post/<int:pk>/' , views.RetrieveDestroyAPIView.as_view() , name="Just a little change ") , 
    path('api/post/<int:pk>/vote' , views.VoteCreate.as_view() , name="Just a little change ") , 
    #path('api-auth/' , include('rest-framework.urls')) , 
]
