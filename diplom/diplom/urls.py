"""diplom URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from myapp.views import test_view, players_view, matches_view, predictions_view, logout_view, login_view, login_operation_view, register_view, register_operation_view, subscriptions_view, confirm_sub_view, prediction_confirm_view, prediction_confirm_operation_view, analysis_view, matches_by_player_view, subscription_download_view, analysis_operation_view





app_name='myapp'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', test_view, name='base'),
    path('players', players_view, name='players'),
    path('matches', matches_view, name='matches'),
    path('predictions', predictions_view, name='predictions'),
    path('logout', logout_view, name='logout'),
    path('login', login_view, name='login'),
    path('login_operation', login_operation_view, name='login_operation'),
    path('register', register_view, name='register'),
    path('register_operation', register_operation_view, name='register_operation'),
    path('subscriptions/<int:id>/', subscriptions_view, name='subscriptions'),
    path('confirm_operation/<int:id>/', confirm_sub_view, name='confirm_operation'),
    path('prediction_confirm/<path:name>/', prediction_confirm_view, name='prediction_confirm'),
    path('prediction_confirm_operation/<path:name>/', prediction_confirm_operation_view, name='prediction_confirm_operation'),
    path('analysis', analysis_view, name='analysis'),
    path('players/<int:id>/', matches_by_player_view, name='players_by_id'),
    path('subscription_pdf', subscription_download_view, name='subscription_pdf'),
    path('analysis_operation', analysis_operation_view, name='analysis_operation'),
]
