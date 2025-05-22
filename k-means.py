from sklearn.decomposition import PCA
from io import BytesIO
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from yellowbrick.cluster import KElbowVisualizer
from sklearn.cluster import KMeans

chosen_column_names = [3, 5, 9, 10, 11, 12]
clusters_name = "Clusters"

columns = [
    "ID",
    "POSTING_DATE",
    "GPI_AGE",
    "GPI_CLS_CODE_PT_OCCUP",
    "GPI_CLS_PT_EDU_DESC",
    "GPI_COUNTY_NAME",
    "GPI_DOMICILE_TYPE",
    "GPI_GENDER_CODE",
    "GPI_MARITAL_SATUS_CODE",
    "GPI_REGION_NAME",
    "CLIENT_TENURE",
    "CLIENT_TENURE_ACTIVE_ACC",
    "PTS_CIC_OPENED_ND",
    "PTS_CLIENT_STATUS_ND",
    "CEC_ALL_ACTIVE_CNT",
    "CEC_ALL_PROD_CNT",
    "CLO_ALL_ACTIVE_CNT",
    "CLO_ALL_PROD_CNT",
    "CRT_ALL_ACTIVE_CNT",
    "DEP_ALL_ACTIVE_CNT",
    "DEP_ALL_PROD_CNT",
    "ICC_ALL_ACTIVE_CNT",
    "ICC_ALL_PROD_CNT",
    "INS_VIG_ALL_ACTIVE_CNT",
    "INV_ALL_ACTIVE_CNT",
    "PPI_ALL_ACTIVE_CNT",
    "REFIN_ALL_ACTIVE_CNT",
    "REFIN_ALL_PROD_CNT",
    "TER_ALL_ACTIVE_CNT",
    "TER_ALL_PROD_CNT",
    "OT_COLT_ALL_PROD_CNT",
    "OT_COLT_ALL_ACTIVE_CNT",
    "LOA_ALL_PROD_CNT",
    "LOA_ALL_ACTIVE_CNT",
    "CRT_ALL_PROD_CNT",
    "CEC_AVG_BALANCE_AMT",
    "CEC_TOTAL_BALANCE_AMT",
    "CLO_AVG_BALANCE_AMT",
    "CLO_MAX_BALANCE_AMT",
    "CLO_MIN_BALANCE_AMT",
    "CLO_TOTAL_BALANCE_AMT",
    "CRT_AVG_BALANCE_AMT",
    "CRT_MAX_BALANCE_AMT",
    "CRT_MIN_BALANCE_AMT",
    "CRT_TOTAL_BALANCE_AMT",
    "DEP_AVG_BALANCE_AMT",
    "DEP_MAX_BALANCE_AMT",
    "DEP_MIN_BALANCE_AMT",
    "DEP_TOTAL_BALANCE_AMT",
    "DTER_AVG_BALANCE_AMT",
    "DTER_TOTAL_BALANCE_AMT",
    "ICC_MAX_BALANCE_AMT",
    "ICC_MIN_BALANCE_AMT",
    "ICC_TOTAL_BALANCE_AMT",
    "OVD_AVG_BALANCE_AMT",
    "OVD_MAX_BALANCE_AMT",
    "OVD_MIN_BALANCE_AMT",
    "OVD_TOTAL_BALANCE_AMT",
    "SAV_AVG_BALANCE_AMT",
    "SAV_TOTAL_BALANCE_AMT",
    "OT_COLT_TOTAL_BALANCE_AMT",
    "OT_COLT_MIN_BALANCE_AMT",
    "OT_COLT_MAX_BALANCE_AMT",
    "OT_COLT_AVG_BALANCE_AMT",
    "LOA_TOTAL_BALANCE_AMT",
    "LOA_MIN_BALANCE_AMT",
    "LOA_MAX_BALANCE_AMT",
    "LOA_AVG_BALANCE_AMT",
    "ICC_AVG_BALANCE_AMT",
    "GPI_CUSTOMER_TYPE_DESC",
    "CRT_GEORGE_FLAG",
    "CRT_LST_ACC_CLOSE_ND",
    "CRT_FST_ACC_ACTIVE_OPEN_ND",
    "PTS_IB_FLAG",
    "APPLE_PAY_FLAG",
    "GEORGE_PAY_FLAG",
    "GOOGLE_PAY_FLAG",
    "WALLET_FLAG",
    "GPI_LST_SALARY_ND",
    "PBS_FLAG",
    "OVD_APPROVED_LIMIT_AMT",
    "OVD_REMAINING_LIMIT_AMT",
    "OVD_REMAINING_LIMIT_AMT_AVG",
    "OVD_REMAINING_LIMIT_AMT_MIN",
    "TRX_IN_ALL_CNT",
    "TRX_IN_ATM_CNT",
    "TRX_IN_OTH_BNK_CNT",
    "TRX_IN_OTH_COUNTRY_CNT",
    "TRX_IN_ALL_AMT",
    "TRX_IN_ATM_AMT",
    "TRX_IN_CRT_AMT",
    "TRX_IN_OTH_BNK_AMT",
    "TRX_IN_OTH_COUNTRY_AMT",
    "TRX_OUT_ALL_CNT",
    "TRX_OUT_ATM_CNT",
    "TRX_OUT_CASH_CNT",
    "TRX_OUT_EC_CNT",
    "TRX_OUT_IB_CNT",
    "TRX_OUT_INTER_TRANSFERS_CNT",
    "TRX_OUT_OFF_DESK_CNT",
    "TRX_OUT_OTH_COUNTRY_CNT",
    "TRX_OUT_POS_CNT",
    "TRX_OUT_ALL_AMT",
    "TRX_OUT_ATM_AMT",
    "TRX_OUT_CASH_AMT",
    "TRX_OUT_EC_AMT",
    "TRX_OUT_IB_AMT",
    "TRX_OUT_INTER_TRANSFERS_AMT",
    "TRX_OUT_OFF_DESK_AMT",
    "TRX_OUT_OTH_COUNTRY_AMT",
    "TRX_OUT_POS_AMT",
    "MCC_UTILITY_SERV_CNT",
    "MCC_UTILITY_SERV_AMT",
    "MCC_TRAVEL_CNT",
    "MCC_TRAVEL_AMT",
    "MCC_TRANSPORTATION_CNT",
    "MCC_TRANSPORTATION_AMT",
    "MCC_RETAIL_OUTLET_SERV_CNT",
    "MCC_RETAIL_OUTLET_SERV_AMT",
    "MCC_PROFESSIONAL_SERV_CNT",
    "MCC_PROFESSIONAL_SERV_AMT",
    "MCC_MONEY_TRANSFER_CNT",
    "MCC_MONEY_TRANSFER_AMT",
    "MCC_MISCELLANEOUS_STORES_CNT",
    "MCC_MISCELLANEOUS_STORES_AMT",
    "MCC_LEISURE_CNT",
    "MCC_LEISURE_AMT",
    "MCC_HOME_AND_CONSTR_CNT",
    "MCC_HOME_AND_CONSTR_AMT",
    "MCC_GOVERNMENT_SERV_CNT",
    "MCC_GOVERNMENT_SERV_AMT",
    "MCC_FOOD_CNT",
    "MCC_FOOD_AMT",
    "MCC_FINANCIAL_INST_CNT",
    "MCC_FINANCIAL_INST_AMT",
    "MCC_ELECT_AND_DIG_GOODS_CNT",
    "MCC_ELECT_AND_DIG_GOODS_AMT",
    "MCC_CONTRACTED_SERV_CNT",
    "MCC_CONTRACTED_SERV_AMT",
    "MCC_CLOTHING_STORES_CNT",
    "MCC_CLOTHING_STORES_AMT",
    "MCC_CAR_RENTAL_CNT",
    "MCC_CAR_RENTAL_AMT",
    "MCC_BUSINESS_SERV_CNT",
    "MCC_BUSINESS_SERV_AMT",
    "MCC_BANKING_ALTER_CNT",
    "MCC_BANKING_ALTER_AMT",
    "MCC_AGRICULTURAL_CNT",
    "MCC_AGRICULTURAL_AMT",
    "ICC_APPROVED_LIMIT",
    "ICC_REMAINING_LIMIT_AMT",
    "CHNL_BRANCH_SCANS_CNT",
    "CHNL_BRANCH_SCANS_DAYS_CNT",
    "CHNL_IB_LOGINS_CNT",
    "CHNL_INBOUND_CALLS_CNT",
    "CHNL_INBOUND_CALLS_DAYS_CNT",
    "CLO_APPROVED_LIMIT",
    "CRT_ACTIVE_FC_CNT",
    "CRT_ACTIVE_FX_CNT",
    "DIRECT_DEBIT_FLAG",
    "GEORGE_INFO_FLAG",
    "ICC_LST_USE_ND",
    "ICC_TRX_ATM_AMT",
    "ICC_TRX_ATM_CNT",
    "LOA_REFUND_FLAG",
    "LOA_TOTAL_REFUND_FLAG",
    "MONEYBACK_FLAG",
    "CLO_LST_ACC_CLOSE_ND",
    "CLO_MAX_MAT_LEFT_ACT_ND",
    "DEP_MAX_MAT_LEFT_ACT_ND",
    "ICC_UTILIZATION_GRADE",
    "OVD_UTILIZATION_GRADE",
    "PTS_CODEBTOR_STATUS_FLAG",
    "PTS_REJECTED_LOANS_REQ_CNT",
    "PTS_TOTAL_LOANS_REQ_CNT"
]

chosen_features = [columns[i] for i in chosen_column_names if i < len(columns) and i != 0]


df = pd.read_csv("../Hackathon_2025_Dataset.csv")
df = df.replace('XNA', np.nan)
df = df.dropna(subset=chosen_features + ["ID"])
df_id = df["ID"].reset_index(drop=True)
df = df[chosen_features]

for col in df.columns:
    if not pd.api.types.is_numeric_dtype(df[col]):
        unique_vals = df[col].dropna().unique()

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
all_colors = ["#682F2F", "#9E726F", "#D6B2B1", "#B9C0C9", "#F3AB60",
              "#4C5B5C", "#88A2AA", "#FFE156", "#6A0572", "#AB83A1"]
colors = []
if nclusters <= 10:
    colors = all_colors[:nclusters]
else:
    extra_colors = sns.color_palette("husl", nclusters - 10).as_hex()
    colors = nclusters + extra_colors

def is_not_binary(series):
    unique_vals = series.dropna().unique()
    return len(unique_vals) != 2

numeric_cols = [col for col in df.columns if is_not_binary(df[col]) and col != 'Clusters']
n_cols = len(numeric_cols)

cluster_stats = df.groupby('Clusters')[numeric_cols].agg(['mean', 'median'])

image_list = []

for i, col in enumerate(numeric_cols):
    fig, axes = plt.subplots(1, 2, figsize=(14, 4))
    fig.suptitle(f'{col} - Cluster Comparison', fontsize=14)

    axes[0].bar(range(nclusters), cluster_stats[col]['mean'], color=colors)
    axes[0].set_title(f'{col} - Mean Comparison')
    axes[0].set_xticks(range(nclusters))
    axes[0].set_xticklabels([f'Cluster {j}' for j in range(nclusters)])

    axes[1].bar(range(nclusters), cluster_stats[col]['median'], color=colors)
    axes[1].set_title(f'{col} - Median Comparison')
    axes[1].set_xticks(range(nclusters))
    axes[1].set_xticklabels([f'Cluster {j}' for j in range(nclusters)])

    buf = BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format='png')
    buf.seek(0)
    image_list.append(buf)
    plt.show(fig)


for ci in range(nclusters):
    cluster = df[df['Clusters'] == ci]
    print(f"Cluster {ci}: {len(cluster)} samples")

df_clusters_unique = df_clusters.drop_duplicates(subset="ID", keep="first")
df_clusters_unique.to_csv(f"{clusters_name}.csv", index=False)
