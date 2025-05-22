import base64
from .models import CustomerData
from django.shortcuts import HttpResponse
import json
from bcr_back.apps import BcrBackConfig
from .serializers import CustomerDataSerializer
import numpy as np
import pandas as pd
from django.contrib.auth.models import User
from .token_decoder import JWTTokenDecoder
from sklearn.decomposition import PCA
from io import BytesIO
import seaborn as sns
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from yellowbrick.cluster import KElbowVisualizer
from sklearn.cluster import KMeans
from django.core.cache import cache


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

    if User.objects.filter(username=username).exists():
        return HttpResponse(json.dumps({'error': 'Username already taken!'}))

    User.objects.create_user(username=username, password=password)
    return HttpResponse(json.dumps({'success': 'User created'}))

def clusters(request):
    jwt_token_decoder = JWTTokenDecoder(request)
    user = jwt_token_decoder.getUserFromToken()

    if user is None:
        return HttpResponse(status=401)

    body = request.body
    body = json.loads(body)

    required_fields = ["name", "columns"]
    for field in required_fields:
        if field not in body:
            return HttpResponse(status=401, content=json.dumps({'error': f"Field '{field}' not found!"}))

    cache_key = f"cluster_{body['name']}"
    cached_result = cache.get(cache_key)
    if cached_result is not None:
        return HttpResponse(json.dumps({'images': cached_result, 'cached': True}))

    if BcrBackConfig.db_loaded == False:
        BcrBackConfig.db_loaded = True
        df_path = "dataset.csv"
        try:
            BcrBackConfig.database = pd.read_csv(df_path, nrows=50000)
            print(f"Object successfully loaded from '{df_path}':")
        except FileNotFoundError:
            print(f"Error: The file '{df_path}' was not found. Please ensure the path and filename are correct.")
        except Exception as e:
            print(f"An error occurred during loading: {e}")

    clusters_name = body["name"]
    columns = body["columns"]
    df = BcrBackConfig.database
    chosen_features = columns
    df = df.replace('XNA', np.nan)
    df = df.dropna(subset=chosen_features + ["ID"])
    df_id = df["ID"].reset_index(drop=True)
    df = df[chosen_features]

    for col in df.columns:
        if not pd.api.types.is_numeric_dtype(df[col]):
            unique_vals = df.groupby(col).size().reset_index(name='counts')[col].dropna().unique()

            if len(unique_vals) == 2:
                mapping = {val: i for i, val in enumerate(unique_vals)}
                df[col] = df[col].map(mapping)
            elif len(unique_vals) > 2:
                dummies = pd.get_dummies(df[col], prefix='is')
                df = pd.concat([df.drop(columns=[col]), dummies], axis=1)

    PCA_DIMENSION = 1
    X = StandardScaler().fit_transform(df.values)
    pca = PCA(n_components=PCA_DIMENSION)
    pca_x = pca.fit_transform(X)
    PCA_DIMENSION += 1
    if np.sum(pca.explained_variance_ratio_) < 0.9:
        while True:
            pca_cand = PCA(n_components=PCA_DIMENSION)
            pca_x_cand = pca_cand.fit_transform(X)
            if np.sum(pca_cand.explained_variance_ratio_) >= 0.9:
                pca_x = pca_x_cand
                del pca_cand
                break
            PCA_DIMENSION += 1
            del pca_x_cand

    del pca
    PCA_ds = pd.DataFrame(pca_x)
    Elbow_M = KElbowVisualizer(KMeans(), k=10)
    Elbow_M.fit(PCA_ds)

    nclusters = Elbow_M.elbow_value_ if Elbow_M.elbow_value_ is not None else 4

    kmeans = KMeans(n_clusters=nclusters, 
                init='k-means++', 
                n_init=10,
                random_state=42)

    yhat_kmeans = kmeans.fit_predict(df)

    df["Clusters"] = yhat_kmeans
    df_clusters = pd.DataFrame({
        "ID": df_id.values,
        "Clusters": yhat_kmeans
    })

    del PCA_ds


    plt.style.use('ggplot')
    plt.rcParams['figure.facecolor'] = '#FFF9ED'
    plt.rcParams['axes.facecolor'] = '#FFF9ED'
    
    # Color setup
    all_colors = ["#682F2F", "#9E726F", "#D6B2B1", "#B9C0C9", "#F3AB60",
                 "#4C5B5C", "#88A2AA", "#FFE156", "#6A0572", "#AB83A1"]
    
    if nclusters <= 10:
        colors = all_colors[:nclusters]
    else:
        extra_colors = sns.color_palette("husl", nclusters - 10).as_hex()
        colors = all_colors + extra_colors

    # Filter numeric columns (excluding binary and cluster columns)
    def is_not_binary(series):
        unique_vals = series.dropna().unique()
        return len(unique_vals) != 2

    numeric_cols = [col for col in df.columns 
                   if is_not_binary(df[col]) and col != 'Clusters']
    
    # Calculate cluster statistics
    cluster_stats = df.groupby('Clusters')[numeric_cols].agg(['mean', 'median'])
    image_list = []

    # Generate visualizations for each numeric column
    for col in numeric_cols:
        fig, axes = plt.subplots(1, 2, figsize=(14, 4))
        fig.suptitle(f'{col} - Cluster Comparison', fontsize=14)

        # Mean comparison plot
        axes[0].bar(range(nclusters), cluster_stats[col]['mean'], color=colors)
        axes[0].set_title(f'{col} - Mean Comparison')
        axes[0].set_xticks(range(nclusters))
        axes[0].set_xticklabels([f'Cluster {j}' for j in range(nclusters)])

        # Median comparison plot
        axes[1].bar(range(nclusters), cluster_stats[col]['median'], color=colors)
        axes[1].set_title(f'{col} - Median Comparison')
        axes[1].set_xticks(range(nclusters))
        axes[1].set_xticklabels([f'Cluster {j}' for j in range(nclusters)])

        # Save to buffer
        buf = BytesIO()
        plt.tight_layout()
        plt.savefig(buf, format='png', bbox_inches='tight', dpi=100)
        buf.seek(0)
        img_base64 = base64.b64encode(buf.read()).decode('utf-8')
        image_list.append(img_base64)
        
        # Clean up
        plt.close(fig)
        buf.close()
    
    cache.set(cache_key, image_list, timeout=60*24)

    return HttpResponse(json.dumps({'images': image_list}))
