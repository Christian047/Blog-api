from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from rest_framework import status


class RegisterView(APIView):
    def post(self, request):
        try:
            data = request.data
            serializer = RegisterSerializer(data=data)

            if not serializer.is_valid():
                return Response({'data': serializer.errors, 'message': 'Validation failed'}, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()

            return Response({'data': {}, 'message': 'Your account has been created'}, status=status.HTTP_201_CREATED)

        except Exception as e:
            # Log the exception for debugging purposes
            print(f"An error occurred: {e}")
            return Response({'data': {}, 'message': 'An error occurred while processing your request'}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        try:
            
            data = request.data
            serializer = LoginSerializer(data=data)

            if not serializer.is_valid():
                # Correcting the response structure for validation errors
                return Response({
                    'data': serializer.errors, 
                    'message': 'Validation failed'},
                                status=status.HTTP_400_BAD_REQUEST)

            response = serializer.get_jwt_token(serializer.data)

            return Response(response, status=status.HTTP_200_OK)

        except Exception as e:
            # Log the exception for debugging purposes
            print(f"An error occurred: {e}")
            return Response({'data': {}, 'message': 'An error occurred while processing your request'}, status=status.HTTP_400_BAD_REQUEST)
