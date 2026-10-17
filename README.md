# BCR Backend

A Django REST backend for banking customer analytics. It serves machine learning predictions and customer segmentation over a JWT-authenticated API, letting a client score individual customers for churn and credit risk and explore behavioral clusters across a large customer dataset.

## Features

- **Churn prediction** — Scores a customer's likelihood of leaving using a pre-trained XGBoost model, with feature engineering (log transforms, one-hot encoding of products and balance tiers) applied on the fly.
- **Credit risk scoring** — Classifies loan/credit risk from applicant attributes (age, job, credit amount, savings and checking tiers) via a second XGBoost model.
- **Customer segmentation** — Runs K-means clustering on user-selected features, automatically reducing dimensionality with PCA (to 90% explained variance) and picking the cluster count with the elbow method. Returns per-feature mean/median comparison charts as Base64 PNGs.
- **Customer lookup** — Fetches stored customer records by ID.
- **Authentication** — JWT-based auth (SimpleJWT) with signup and token refresh.

## How it works

The XGBoost models are loaded once into memory at app startup and reused across requests. Incoming payloads are transformed into the exact feature layout each model expects before inference. The clustering endpoint lazily loads the dataset, standardizes and PCA-reduces the chosen features, clusters them, renders comparison plots with matplotlib/seaborn, and caches the results to avoid recomputation.

## Tech stack

- **Framework:** Python, Django, Django REST Framework
- **Auth:** djangorestframework-simplejwt (JWT), PyJWT
- **ML / data:** XGBoost, scikit-learn, Yellowbrick, pandas, NumPy
- **Visualization:** matplotlib, seaborn
- **Database:** SQLite
