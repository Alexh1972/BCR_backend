from django.apps import AppConfig
import pandas as pd
import pickle
import xgboost
class BcrBackConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bcr_back'

    dtree_model = None
    risk_model = None
    database = None

    def ready(self):
        if not BcrBackConfig.dtree_model:
            model_path = 'bcr_back/ml_models/churn.json'

            try:
                BcrBackConfig.dtree_model = xgboost.XGBClassifier()
                BcrBackConfig.dtree_model.load_model(model_path)

                print(f"Object successfully loaded from '{model_path}':")

            except FileNotFoundError:
                print(
                    f"Error: The model file '{model_path}' was not found. Please ensure the path and filename are correct.")
            except Exception as e:
                print(f"An error occurred during loading the model from '{model_path}': {e}")

        if not BcrBackConfig.risk_model:
            model_path = 'bcr_back/ml_models/credit_risk.json'
            try:
                BcrBackConfig.risk_model = xgboost.XGBClassifier()
                BcrBackConfig.risk_model.load_model(model_path)

                print(f"Object successfully loaded from '{model_path}':")
            except FileNotFoundError:
                print(f"Error: The file '{model_path}' was not found. Please ensure the path and filename are correct.")
            except Exception as e:
                print(f"An error occurred during loading: {e}")
        if not BcrBackConfig.database:
            df_path = 'dataset.csv'
            try:
                BcrBackConfig.database = pd.read_csv(df_path)
                print(f"Object successfully loaded from '{df_path}':")
            except FileNotFoundError:
                print(f"Error: The file '{df_path}' was not found. Please ensure the path and filename are correct.")
            except Exception as e:
                print(f"An error occurred during loading: {e}")