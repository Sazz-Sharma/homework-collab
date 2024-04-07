from django.urls import path
from . import views

urlpatterns = [
    # Add your URL patterns here
    path('create_space/', views.create_space),
    path('add_member/<uuid:spaceId>/<str:member_name>/', views.add_member),
    path('change_to_teacher/<uuid:spaceId>/<str:member_name>/', views.add_member),
    path('all_spaces/', views.spaces),
    path('<uuid:spaceId>/notice/', views.notice_manager),
    path('<uuid:spaceId>/members/', views.member_of_space),
    path('', views.my_spaces),
    path('<spaceId>/send_request/', views.send_join_request),
    path('<spaceId>/request_manager/', views.join_request_manager),
    path('<spaceId>/iamteacher/',views.hi)
]



