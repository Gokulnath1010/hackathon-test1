from django.urls import path

from . import views

urlpatterns = [
	path('login/', views.login, name='login'),
	path('exams/', views.exam_list, name='exam_list'),
	path('logout/', views.logout, name='logout'),
	path('test/', views.mock_test, name='mock_test'),
	path('test/<slug:exam_slug>/', views.mock_test, name='exam_mock_test'),
]
