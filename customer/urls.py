from django.urls import path
from .views import RegisterView, LoginView, CustomerView, LogoutView, CourseView, HomeWorkView,ApproveView,CustomerListView,CustomerById

urlpatterns = [
    path('register', RegisterView.as_view()),
    path('login', LoginView.as_view()),
    path('user', CustomerView.as_view()),
    path('logout', LogoutView.as_view()),
    path('course', CourseView.as_view()),
    path('course/<str:pk>', CourseView.as_view()),
    path('work', HomeWorkView.as_view()),
    path('work/<str:pk>', HomeWorkView.as_view()),
    path('status', ApproveView.as_view()),
    path('customerList', CustomerListView.as_view()),
    path('customerById/<str:pk>', CustomerById.as_view()),
]
