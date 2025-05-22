from django.urls import path
from .views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('api/getUsers/', get_users, name='get_users'),
    path('api/churnPrediction/', get_churn_prediction, name='get_churn_prediction'),
    path('api/riskPrediction/', get_risk_prediction, name='get_risk_prediction'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/signup/', signup, name='signup'),
    path('api/clusters/', clusters, name='clusters'),
]