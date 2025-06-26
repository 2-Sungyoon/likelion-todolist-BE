"""
URL configuration for todolistProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

urlpatterns = [
    path('<int:user_id>/', views.Todos.as_view()),
    path('<int:user_id>/<int:todo_id>/', views.TodoDetail.as_view()),
    path('<int:user_id>/<int:todo_id>/check/', views.TodoCheck.as_view()),
    path('<int:user_id>/<int:todo_id>/reviews/', views.TodoReview.as_view()),
    #? 뒤에 qeurt string 부분은 url에 표시 x
]


