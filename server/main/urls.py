from django.urls import path
from main import views
from django.conf.urls import include


urlpatterns = [

    path('login', views.login),
    path('signup', views.signup),
    path('auth', include('rest_framework.urls', namespace='rest_framework')),

    path('category', views.categoryAPI.as_view()),
    path('category/<int:id>', views.categoryadminAPI.as_view()),
    path('post_cate_list/<int:id>', views.postcatelistAPI.as_view()),
    path("post/<int:id>", views.postAPI.as_view(), name='post'),

]
