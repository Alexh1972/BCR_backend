from django.urls import path
from .views import *
urlpatterns = [
    path('api/getUsers/', get_users, name='get_users'),
    path('api/churnPrediction/', get_churn_prediction, name='get_churn_prediction'),
    path('api/riskPrediction/', get_risk_prediction, name='get_risk_prediction')
]