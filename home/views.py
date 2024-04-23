from email.policy import HTTP
from functools import partial
from django.shortcuts import render
from .serializers import *
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from django.db.models import Q

# models
from .models import Blog

# Authentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

# Paginator
from django.core.paginator import Paginator


class PublicblogView(APIView):
    def get(self,request):
        try:

            # filter all blogs and get the users blog posts
            blog = Blog.objects.all()

            # search
            if request.GET.get('search'):
                search = request.GET.get('search')
                blogs = blogs.filter(Q(title__icontains=search) | Q(blog_text__icontains=search))

            # serializer = BlogSerializer(blog, many=True)
            
            # pagination
            page_number= request.GET.get('page',1)
            paginator = Paginator(blogs,1)
            
            serializer= BlogSerializer(paginator.page(page_number), many=True)
            

            return Response({'data': serializer.data,
                            'message': "blog fetched successfully"}, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            print(f"An error occurred: {e}")
            return Response({'data': {}, 'message': 'Could not get blogs'}, status=status.HTTP_400_BAD_REQUEST)

        
        
        
        
    def post(self, request):
        try:
            data = request.data
            data['user'] = request.user.id
            serializer = BlogSerializer(data=data)

            if not serializer.is_valid():
                return Response({
                    'data': serializer.errors,
                    'message': 'something went wrong'},
                    status=status.HTTP_400_BAD_REQUEST)

            serializer.save()
            return Response({'data': serializer.data, 'message': 'Your Blog has been created'}, status=status.HTTP_201_CREATED)

        except Exception as e:
            print(e)
            print(f"An error occurred: {e}")
            return Response({'data': {}, 'message': 'Problem creating blog'}, status=status.HTTP_400_BAD_REQUEST)

        
        
        
        
        






class BlogView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        try:

            # filter all blogs and get the users blog posts
            blogs = Blog.objects.filter(user=request.user)

            # search
            if request.GET.get('search'):
                search = request.GET.get('search')
                blogs = blogs.filter(Q(title__icontains=search) | Q(blog_text__icontains=search))


                        # pagination
            page_number= request.GET.get('page',1)
            paginator = Paginator(blogs,2)
            
            serializer= BlogSerializer(paginator.page(page_number), many=True)
            

            # serializer = BlogSerializer(blog, many=True)

            return Response({'data': serializer.data,
                            'message': "blog fetched successfully"}, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            print(f"An error occurred: {e}")
            return Response({'data': {}, 'message': 'Could not get blogs or invalid page number'}, status=status.HTTP_400_BAD_REQUEST)





    def post(self, request):
        try:
            data = request.data
            data['user'] = request.user.id
            serializer = BlogSerializer(data=data)

            if not serializer.is_valid():
                return Response({
                    'data': serializer.errors,
                    'message': 'something went wrong'},
                    status=status.HTTP_400_BAD_REQUEST)

            serializer.save()
            return Response({'data': serializer.data, 'message': 'Your Blog has been created'}, status=status.HTTP_201_CREATED)

        except Exception as e:
            print(e)
            print(f"An error occurred: {e}")
            return Response({'data': {}, 'message': 'Problem creating blog'}, status=status.HTTP_400_BAD_REQUEST)

        # def get(self,request):


    def patch(self,request):
        try:
            data = request.data
            blog = Blog.objects.filter(uuid=data.get('uuid'))
            
            if not blog.exists():
                 return Response({'data': {}, 'message': 'blog doesnt exist'}, status=status.HTTP_400_BAD_REQUEST)
        
            if request.user != blog[0].user:
              return Response({'data': {}, 'message': 'Not authorized'}, status=status.HTTP_400_BAD_REQUEST)
        
            serializer= BlogSerializer(blog[0],data=data, partial= True)
            
            if not serializer.is_valid():
                return Response({
                'data': serializer.errors,
                'message': 'something went wrong'},
                status=status.HTTP_400_BAD_REQUEST)

            serializer.save()
            return Response({'data': serializer.data, 'message': 'Your Blog has been updated'}, status=status.HTTP_201_CREATED)
                    
                    
        
        except Exception as e:
            print(e)
            print(f"An error occurred: {e}")
            return Response({'data': {}, 'message': 'Problem creating blog'}, status=status.HTTP_400_BAD_REQUEST)
      
      
      
        
        

    def delete(self, request):
        try:
            # Extracting data from request
            data = request.data
            
            # Fetching the blog object based on uuid
            blog = Blog.objects.filter(uuid=data.get('uuid'))
            
            # Check if the blog exists
            if not blog.exists():
                return Response({'data': {}, 'message': 'Blog does not exist'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Check if the user is authorized to delete the blog
            if request.user != blog[0].user:
                return Response({'data': {}, 'message': 'Not authorized'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Deleting the blog
            blog[0].delete()
            
            # Returning success response
            return Response({'message': 'Your Blog has been deleted'}, status=status.HTTP_200_OK)
            
        except Exception as e:
            # Handling exceptions
            print(e)
            print(f"An error occurred: {e}")
            return Response({'data': {}, 'message': 'Problem deleting blog'}, status=status.HTTP_400_BAD_REQUEST)