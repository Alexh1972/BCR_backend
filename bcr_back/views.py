from .models import CustomerData
from django.shortcuts import HttpResponse
import json
from bcr_back.apps import BcrBackConfig
from .serializers import CustomerDataSerializer
import numpy as np
import pandas as pd
from django.contrib.auth.models import User

from .token_decoder import JWTTokenDecoder


def get_users(request):
    jwt_token_decoder = JWTTokenDecoder(request)
    user = jwt_token_decoder.getUserFromToken()

    if user is None:
        return HttpResponse(status=401)

    body = request.body
    customer_ids = json.loads(body).get("IDS")

    if not customer_ids or not isinstance(customer_ids, list):
        return HttpResponse(status=400, content=json.dumps({'error': "Field 'IDS' not found!"}))

    customers = CustomerData.objects.filter(customer_id__in=customer_ids)

    serializer = CustomerDataSerializer(customers, many=True)

    return HttpResponse(json.dumps({'no_customers': customers.count(), 'customers': serializer.data}))


def get_churn_prediction(request):
    jwt_token_decoder = JWTTokenDecoder(request)
    user = jwt_token_decoder.getUserFromToken()

    if user is None:
        return HttpResponse(status=401)

    body = request.body
    body = json.loads(body)

    required_fields = ["credit_score", "age", "tenure", "credit_card", "is_active", "salary", "male", "products",
                       "balance"]
    for field in required_fields:
        if field not in body:
            return HttpResponse(status=401, content=json.dumps({'error': f"Field '{field}' not found!"}))

    credit_score = body["credit_score"]
    age = body["age"]
    tenure = body["tenure"]
    credit_card = body["credit_card"]
    is_active = body["is_active"]
    salary = body["salary"]
    male = body["male"]
    products = body["products"]
    balance = body["balance"]

    d_tree = BcrBackConfig.dtree_model

    cols = ['CreditScore',
            'Age',
            'Tenure',
            'HasCrCard',
            'IsActiveMember',
            'EstimatedSalary',
            'Gender_Female',
            'Gender_Male',
            'Total_Products_More Than 2 Products',
            'Total_Products_One product',
            'Total_Products_Two Products',
            'Account_Balance_More Than zero Balance',
            'Account_Balance_Zero Balance']

    row = {'CreditScore': credit_score,
           'Age': np.log(age),
           'Tenure': tenure / 365.0,
           'HasCrCard': (credit_card == 1),
           'IsActiveMember': (is_active == 1),
           'EstimatedSalary': salary / 5.0,
           'Gender_Female': (male == 0),
           'Gender_Male': (male == 1),
           'Total_Products_More Than 2 Products': (products >= 1) & (products < 5),
           'Total_Products_One product': products > 20,
           'Total_Products_Two Products': (products >= 5) & (products < 20),
           'Account_Balance_More Than zero Balance': (balance != 0),
           'Account_Balance_Zero Balance': (balance == 0)}
    df = pd.DataFrame([row], columns=cols)

    pred = d_tree.predict(df.values)

    return HttpResponse(json.dumps({'churned': int(pred[0])}))


def get_risk_prediction(request):
    jwt_token_decoder = JWTTokenDecoder(request)
    user = jwt_token_decoder.getUserFromToken()

    if user is None:
        return HttpResponse(status=401)

    body = request.body
    body = json.loads(body)

    required_fields = ["age", "job", "credit_amount", "male", "savings", "check"]
    for field in required_fields:
        if field not in body:
            return HttpResponse(status=401, content=json.dumps({'error': f"Field '{field}' not found!"}))

    age = body["age"]
    job = body["job"]
    credit_amount = body["credit_amount"]
    male = body["male"]
    savings = body["savings"]
    balance = body["check"]

    cols = ['Age',
            'Job',
            'Credit amount',
            'Sex_male',
            'Savings_moderate',
            'Savings_no_inf',
            'Savings_quite rich',
            'Savings_rich',
            'Check_moderate',
            'Check_no_inf',
            'Check_rich',
            'Age_cat_Young',
            'Age_cat_Adult',
            'Age_cat_Senior']

    row_l = {'Age': age,
             'Job': job,
             'Credit amount': np.log(credit_amount * 0.38),
             'Sex_male': male == 1,
             'Savings_moderate': (savings >= 5000) & (savings < 15000),
             'Savings_no_inf': (savings < 5000),
             'Savings_quite rich': (savings >= 15000) & (savings < 40000),
             'Savings_rich': (savings >= 40000),
             'Check_moderate': (balance >= 2000) & (balance < 7000),
             'Check_no_inf': (balance < 2000),
             'Check_rich': (balance >= 7000),
             'Age_cat_Young': age < 25,
             'Age_cat_Adult': (age >= 25) & (age < 60),
             'Age_cat_Senior': age >= 60}

    df = pd.DataFrame([row_l], columns=cols)

    pred = BcrBackConfig.risk_model.predict(df.values)

    return HttpResponse(json.dumps({'credit_risk': int(pred[0])}))

def signup(request):
    username = request.POST.get('username')
    password = request.POST.get('password')

    if User.objects.get(username=username):
        return HttpResponse(json.dumps({'error': 'Username already taken!'}))

    User.objects.create_user(username=username, password=password)
    return HttpResponse(json.dumps({'success': 'User created'}))
