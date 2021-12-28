from django.core.exceptions import ValidationError
from django.shortcuts import render
from rest_framework import generics , permissions , mixins , status 
from .serializers import PostSerializers , VoteSerializers 
from posts.models import Post , Vote
from rest_framework.response import Response
# Create your views here.

class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializers
    permissions_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(poster=self.request.user)
class RetrieveDestroyAPIView(generics.RetrieveDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializers
    permissions_classes = [permissions.IsAuthenticated]
    def delete(self , request , *args , **kwargs ):
        post = Post.objects.filter(pk=kwargs['pk'] , poster=self.request.user)
        if post.exists():
            return self.destroy(request , *args , **kwargs )
        else:
            raise ValidationError('This is not your post to delete bro ')


class VoteCreate(generics.CreateAPIView  , mixins.DestroyModelMixin):
    queryset = Post.objects.all()
    serializer_class = VoteSerializers
    permissions_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        user = self.request.user
        post = Post.objects.get(pk=self.kwargs['pk'])
        return Vote.objects.filter(voter=user , post=post)
    def perform_create(self, serializer):
        if self.get_queryset().exists():
            raise ValidationError('You have already voted :)')
        serializer.save(voter=self.request.user ,post = Post.objects.get(pk=self.kwargs['pk']))
    def delete(self , request , *args , **kwargs ):
        if self.get_queryset().exists():
            self.queryset().delete()
            return Response(status.HTTP_204_NO_CONTENT)
        else:
            raise ValidationError('You have already voted :)')











