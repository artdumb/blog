from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_200_OK
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import User, Category, Post, Review
from .serializers import UserSerializer, CategorySerializer, PostSerializer, ReviewSerializer
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework import viewsets
from rest_framework.views import APIView
from django.shortcuts import render, get_object_or_404, redirect, get_list_or_404
import json

# ====================User=======================


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        usernamee = data['username']
        passwordd = data['password']
        if usernamee is None or passwordd is None:
            return JsonResponse(status=400)

        user = authenticate(username=usernamee, password=passwordd)
        if not user:
            return Response({'error': 'Invalid credentials'}, status=HTTP_404_NOT_FOUND)
        else:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    data = JSONParser().parse(request)
    usernamee = data['username']
    emaill = data['email']
    nick = data['nickname']
    password1 = data['password1']
    password2 = data['password2']
    if request.method == 'POST':
        if password1 == password2:
            User.objects.create_user(
                username=usernamee,
                password=password1,
                email=emaill,
                nickname=nick,)
            return HttpResponse(status=200)
        return Response({'error': "비밀번호가 다릅니다"}, status=HTTP_404_NOT_FOUND)
# ====================Category=======================


class categoryAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        obj = Category.objects.all()
        serializers = CategorySerializer(obj, many=True)
        return Response(serializers.data)

    def post(self, request):
        data = json.loads(request.body)
        title = data.get('category_title', None)
        if not (title):
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)
        Category.objects.create(
            category_title=title,
        )
        return JsonResponse({'message': 'SUCCESS'}, status=200)


class categoryadminAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    def put(self, request, id):
        data = json.loads(request.body)
        titlee = data.get('category_title', None)
        obj = get_object_or_404(Category, pk=id)
        if not (titlee):
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)
        obj.category_title = titlee
        obj.save()
        return HttpResponse(status=200)

    def delete(self, request, id):
        request = json.loads(request.body)
        obj = get_object_or_404(Category, pk=id)
        obj.delete()
        return HttpResponse(status=200)


# ==================Post============================
class postcatelistAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        obj = get_list_or_404(Post, category_id=id)
        serializers = PostSerializer(obj, many=True)
        return Response(serializers.data)


class postAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        obj = get_object_or_404(Post, pk=id)
        serializers = PostSerializer(obj)
        return Response(serializers.data)

    #

    def post(self, request):
        data = json.loads(request.body)
        contentt = data.get('content', None)
        titlee = data.get('title', None)
        cate_id = data.get('category_id', None)
        # KEY_ERROR check
        if not (contentt):
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)
        Post.objects.create(
            content=contentt,
            title=titlee,
            category_id=cate_id,
            # 작성자 추가
            user=request.user
        )
        return JsonResponse({'message': 'SUCCESS'}, status=200)

    def put(self, request, id):
        data = json.loads(request.body)
        contentt = data.get('content', None)
        titlee = data.get('title', None)
        cate_id = data.get('category_id', None)
        obj = get_object_or_404(Post, pk=id)
        if request.user != obj.user:
            return JsonResponse({'message': 'user is different'}, status=400)
        if not (contentt):
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)
        obj.category_id = cate_id
        obj.content = contentt
        obj.title = titlee
        obj.save()
        return HttpResponse(status=200)

    def delete(self, request, id):
        request = json.loads(request.body)
        obj = get_object_or_404(Post, pk=id)
        if request.user != obj.user:
            return JsonResponse({'message': 'user is different'}, status=400)
        obj.delete()
        return HttpResponse(status=200)
