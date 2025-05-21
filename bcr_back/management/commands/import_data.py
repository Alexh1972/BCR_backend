import csv
import os
import django
from datetime import datetime
from decimal import Decimal, InvalidOperation

from django.core.management import CommandError, BaseCommand

# --- Configuration ---
# IMPORTANT: Replace 'your_project_name' with the actual name of your Django project.
# This is the name of the directory that contains your settings.py file.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bcr")
django.setup()

# IMPORTANT: Replace 'your_app_name' with the actual name of your Django app
# where your CustomerData model is located (e.g., 'customers').
from ...models import CustomerData

# Define the full path to your CSV file.
# Make sure the path is correct for your system.
CSV_FILE_PATH = r'C:\Alex\bcr\Hackathon_2025_Dataset.csv'

# --- Helper Functions for Data Cleaning ---

def safe_int(value):
    """
    Safely converts a string value to an integer.
    Returns None if the value is empty, cannot be converted, or is not provided.
    """
    if value is None or value == '':
        return None
    try:
        return int(value)
    except (ValueError, TypeError):
        # print(f"Warning: Could not convert '{value}' to integer.")
        return None

def safe_decimal(value):
    """
    Safely converts a string value to a Decimal.
    Returns None if the value is empty, cannot be converted, or is not provided.
    """
    if value is None or value == '':
        return None
    try:
        return Decimal(value)
    except (InvalidOperation, TypeError):
        # print(f"Warning: Could not convert '{value}' to decimal.")
        return None

def safe_boolean(value):
    """
    Safely converts a string value ('1' or '0') to a boolean (True or False).
    Returns None if the value is not '1' or '0', or is not provided.
    """
    if value == '1':
        return True
    elif value == '0':
        return False
    # print(f"Warning: Could not convert '{value}' to boolean (expected '1' or '0').")
    return None

# --- Main Import Function (now part of a Django management command) ---

class Command(BaseCommand):
    help = 'Imports customer data from a CSV file into the CustomerData model.'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, nargs='?',
                            help='The path to the CSV file to import. Defaults to CSV_FILE_PATH in the script.')

    def handle(self, *args, **options):
        file_path = options['csv_file'] if options['csv_file'] else CSV_FILE_PATH

        if not os.path.exists(file_path):
            raise CommandError(f"Error: The file '{file_path}' was not found. Please check the path.")

        self.stdout.write(self.style.SUCCESS(f"Starting data import from '{file_path}'..."))
        imported_count = 0
        skipped_count = 0

        try:
            with open(file_path, mode='r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                # Get a list of all valid field names from the CustomerData model
                model_field_names = {f.name for f in CustomerData._meta.get_fields()}

                for row_num, row in enumerate(reader, 2):  # Start row_num from 2 for header + first data row
                    customer_data_to_create = {}
                    try:
                        # --- Core Customer Information ---
                        customer_data_to_create['customer_id'] = row.get('ID')
                        if not customer_data_to_create['customer_id']:
                            self.stdout.write(self.style.WARNING(f"Skipping row {row_num}: 'ID' is missing or empty. Row data: {row}"))
                            skipped_count += 1
                            continue

                        # Date field conversion
                        posting_date_str = row.get('POSTING_DATE')
                        if posting_date_str:
                            try:
                                customer_data_to_create['POSTING_DATE'] = datetime.strptime(posting_date_str, '%Y-%m-%d').date()
                            except ValueError:
                                self.stdout.write(self.style.WARNING(f"Warning: Invalid date format for POSTING_DATE '{posting_date_str}' in row {row_num}. Setting to None."))
                                customer_data_to_create['POSTING_DATE'] = None
                        else:
                            customer_data_to_create['POSTING_DATE'] = None

                        # Ensure POSTING_DATE is not None if it's part of the unique lookup
                        if customer_data_to_create['POSTING_DATE'] is None:
                            self.stdout.write(self.style.WARNING(f"Skipping row {row_num}: 'POSTING_DATE' is missing or invalid. Row data: {row}"))
                            skipped_count += 1
                            continue


                        customer_data_to_create['GPI_AGE'] = safe_int(row.get('GPI_AGE'))
                        customer_data_to_create['GPI_CLS_CODE_PT_OCCUP'] = row.get('GPI_CLS_CODE_PT_OCCUP')
                        customer_data_to_create['GPI_CLS_PT_EDU_DESC'] = row.get('GPI_CLS_PT_EDU_DESC')
                        customer_data_to_create['GPI_COUNTY_NAME'] = row.get('GPI_COUNTY_NAME')
                        customer_data_to_create['GPI_DOMICILE_TYPE'] = row.get('GPI_DOMICILE_TYPE')
                        customer_data_to_create['GPI_GENDER_CODE'] = row.get('GPI_GENDER_CODE')
                        customer_data_to_create['GPI_MARITAL_SATUS_CODE'] = row.get('GPI_MARITAL_SATUS_CODE')
                        customer_data_to_create['GPI_REGION_NAME'] = row.get('GPI_REGION_NAME')
                        customer_data_to_create['GPI_CUSTOMER_TYPE_DESC'] = row.get('GPI_CUSTOMER_TYPE_DESC')

                        # --- Tenure and Status ---
                        customer_data_to_create['CLIENT_TENURE'] = safe_int(row.get('CLIENT_TENURE'))
                        customer_data_to_create['CLIENT_TENURE_ACTIVE_ACC'] = safe_int(row.get('CLIENT_TENURE_ACTIVE_ACC'))
                        customer_data_to_create['PTS_CIC_OPENED_ND'] = safe_int(row.get('PTS_CIC_OPENED_ND'))
                        customer_data_to_create['PTS_CLIENT_STATUS_ND'] = safe_int(row.get('PTS_CLIENT_STATUS_ND'))
                        customer_data_to_create['PTS_LST_SALARY_ND'] = safe_int(row.get('PTS_LST_SALARY_ND'))
                        customer_data_to_create['ICC_LST_USE_ND'] = safe_int(row.get('ICC_LST_USE_ND'))
                        customer_data_to_create['CLO_LST_ACC_CLOSE_ND'] = safe_int(row.get('CLO_LST_ACC_CLOSE_ND'))
                        customer_data_to_create['CLO_MAX_MAT_LEFT_ACT_ND'] = safe_int(row.get('CLO_MAX_MAT_LEFT_ACT_ND'))
                        customer_data_to_create['DEP_MAX_MAT_LEFT_ACT_ND'] = safe_int(row.get('DEP_MAX_MAT_LEFT_ACT_ND'))
                        customer_data_to_create['CRT_LST_ACC_CLOSE_ND'] = safe_int(row.get('CRT_LST_ACC_CLOSE_ND'))
                        customer_data_to_create['CRT_FST_ACC_ACTIVE_OPEN_ND'] = safe_int(row.get('CRT_FST_ACC_ACTIVE_OPEN_ND'))

                        # --- Product Counts (Active and Total) ---
                        customer_data_to_create['CEC_ALL_ACTIVE_CNT'] = safe_int(row.get('CEC_ALL_ACTIVE_CNT'))
                        customer_data_to_create['CEC_ALL_PROD_CNT'] = safe_int(row.get('CEC_ALL_PROD_CNT'))
                        customer_data_to_create['CLO_ALL_ACTIVE_CNT'] = safe_int(row.get('CLO_ALL_ACTIVE_CNT'))
                        customer_data_to_create['CLO_ALL_PROD_CNT'] = safe_int(row.get('CLO_ALL_PROD_CNT'))
                        customer_data_to_create['CRT_ALL_ACTIVE_CNT'] = safe_int(row.get('CRT_ALL_ACTIVE_CNT'))
                        customer_data_to_create['DEP_ALL_ACTIVE_CNT'] = safe_int(row.get('DEP_ALL_ACTIVE_CNT'))
                        customer_data_to_create['DEP_ALL_PROD_CNT'] = safe_int(row.get('DEP_ALL_PROD_CNT'))
                        customer_data_to_create['ICC_ALL_ACTIVE_CNT'] = safe_int(row.get('ICC_ALL_ACTIVE_CNT'))
                        customer_data_to_create['ICC_ALL_PROD_CNT'] = safe_int(row.get('ICC_ALL_PROD_CNT'))
                        customer_data_to_create['INS_VIG_ALL_ACTIVE_CNT'] = safe_int(row.get('INS_VIG_ALL_ACTIVE_CNT'))
                        customer_data_to_create['INV_ALL_ACTIVE_CNT'] = safe_int(row.get('INV_ALL_ACTIVE_CNT'))
                        customer_data_to_create['PPI_ALL_ACTIVE_CNT'] = safe_int(row.get('PPI_ALL_ACTIVE_CNT'))
                        customer_data_to_create['REFIN_ALL_ACTIVE_CNT'] = safe_int(row.get('REFIN_ALL_ACTIVE_CNT'))
                        customer_data_to_create['REFIN_ALL_PROD_CNT'] = safe_int(row.get('REFIN_ALL_PROD_CNT'))
                        customer_data_to_create['TER_ALL_ACTIVE_CNT'] = safe_int(row.get('TER_ALL_ACTIVE_CNT'))
                        customer_data_to_create['TER_ALL_PROD_CNT'] = safe_int(row.get('TER_ALL_PROD_CNT'))
                        customer_data_to_create['OT_COLT_ALL_PROD_CNT'] = safe_int(row.get('OT_COLT_ALL_PROD_CNT'))
                        customer_data_to_create['OT_COLT_ALL_ACTIVE_CNT'] = safe_int(row.get('OT_COLT_ALL_ACTIVE_CNT'))
                        customer_data_to_create['LOA_ALL_PROD_CNT'] = safe_int(row.get('LOA_ALL_PROD_CNT'))
                        customer_data_to_create['LOA_ALL_ACTIVE_CNT'] = safe_int(row.get('LOA_ALL_ACTIVE_CNT'))
                        customer_data_to_create['CRT_ALL_PROD_CNT'] = safe_int(row.get('CRT_ALL_PROD_CNT'))
                        customer_data_to_create['CRT_ACTIVE_FC_CNT'] = safe_int(row.get('CRT_ACTIVE_FC_CNT'))
                        customer_data_to_create['CRT_ACTIVE_FX_CNT'] = safe_int(row.get('CRT_ACTIVE_FX_CNT'))

                        # --- Balance Amounts ---
                        customer_data_to_create['CEC_AVG_BALANCE_AMT'] = safe_decimal(row.get('CEC_AVG_BALANCE_AMT'))
                        customer_data_to_create['CEC_TOTAL_BALANCE_AMT'] = safe_decimal(row.get('CEC_TOTAL_BALANCE_AMT'))
                        customer_data_to_create['CLO_AVG_BALANCE_AMT'] = safe_decimal(row.get('CLO_AVG_BALANCE_AMT'))
                        customer_data_to_create['CLO_MAX_BALANCE_AMT'] = safe_decimal(row.get('CLO_MAX_BALANCE_AMT'))
                        customer_data_to_create['CLO_MIN_BALANCE_AMT'] = safe_decimal(row.get('CLO_MIN_BALANCE_AMT'))
                        customer_data_to_create['CLO_TOTAL_BALANCE_AMT'] = safe_decimal(row.get('CLO_TOTAL_BALANCE_AMT'))
                        customer_data_to_create['CRT_AVG_BALANCE_AMT'] = safe_decimal(row.get('CRT_AVG_BALANCE_AMT'))
                        customer_data_to_create['CRT_MAX_BALANCE_AMT'] = safe_decimal(row.get('CRT_MAX_BALANCE_AMT'))
                        customer_data_to_create['CRT_MIN_BALANCE_AMT'] = safe_decimal(row.get('CRT_MIN_BALANCE_AMT'))
                        customer_data_to_create['CRT_TOTAL_BALANCE_AMT'] = safe_decimal(row.get('CRT_TOTAL_BALANCE_AMT'))
                        customer_data_to_create['DEP_AVG_BALANCE_AMT'] = safe_decimal(row.get('DEP_AVG_BALANCE_AMT'))
                        customer_data_to_create['DEP_MAX_BALANCE_AMT'] = safe_decimal(row.get('DEP_MAX_BALANCE_AMT'))
                        customer_data_to_create['DEP_MIN_BALANCE_AMT'] = safe_decimal(row.get('DEP_MIN_BALANCE_AMT'))
                        customer_data_to_create['DEP_TOTAL_BALANCE_AMT'] = safe_decimal(row.get('DEP_TOTAL_BALANCE_AMT'))
                        customer_data_to_create['DTER_AVG_BALANCE_AMT'] = safe_decimal(row.get('DTER_AVG_BALANCE_AMT'))
                        customer_data_to_create['DTER_TOTAL_BALANCE_AMT'] = safe_decimal(row.get('DTER_TOTAL_BALANCE_AMT'))
                        customer_data_to_create['ICC_MAX_BALANCE_AMT'] = safe_decimal(row.get('ICC_MAX_BALANCE_AMT'))
                        customer_data_to_create['ICC_MIN_BALANCE_AMT'] = safe_decimal(row.get('ICC_MIN_BALANCE_AMT'))
                        customer_data_to_create['ICC_TOTAL_BALANCE_AMT'] = safe_decimal(row.get('ICC_TOTAL_BALANCE_AMT'))
                        customer_data_to_create['OVD_AVG_BALANCE_AMT'] = safe_decimal(row.get('OVD_AVG_BALANCE_AMT'))
                        customer_data_to_create['OVD_MAX_BALANCE_AMT'] = safe_decimal(row.get('OVD_MAX_BALANCE_AMT'))
                        customer_data_to_create['OVD_MIN_BALANCE_AMT'] = safe_decimal(row.get('OVD_MIN_BALANCE_AMT'))
                        customer_data_to_create['OVD_TOTAL_BALANCE_AMT'] = safe_decimal(row.get('OVD_TOTAL_BALANCE_AMT'))
                        customer_data_to_create['SAV_AVG_BALANCE_AMT'] = safe_decimal(row.get('SAV_AVG_BALANCE_AMT'))
                        customer_data_to_create['SAV_TOTAL_BALANCE_AMT'] = safe_decimal(row.get('SAV_TOTAL_BALANCE_AMT'))
                        customer_data_to_create['OT_COLT_TOTAL_BALANCE_AMT'] = safe_decimal(row.get('OT_COLT_TOTAL_BALANCE_AMT'))
                        customer_data_to_create['OT_COLT_MIN_BALANCE_AMT'] = safe_decimal(row.get('OT_COLT_MIN_BALANCE_AMT'))
                        customer_data_to_create['OT_COLT_MAX_BALANCE_AMT'] = safe_decimal(row.get('OT_COLT_MAX_BALANCE_AMT'))
                        customer_data_to_create['OT_COLT_AVG_BALANCE_AMT'] = safe_decimal(row.get('OT_COLT_AVG_BALANCE_AMT'))
                        customer_data_to_create['LOA_TOTAL_BALANCE_AMT'] = safe_decimal(row.get('LOA_TOTAL_BALANCE_AMT'))
                        customer_data_to_create['LOA_MIN_BALANCE_AMT'] = safe_decimal(row.get('LOA_MIN_BALANCE_AMT'))
                        customer_data_to_create['LOA_MAX_BALANCE_AMT'] = safe_decimal(row.get('LOA_MAX_BALANCE_AMT'))
                        customer_data_to_create['LOA_AVG_BALANCE_AMT'] = safe_decimal(row.get('LOA_AVG_BALANCE_AMT'))
                        customer_data_to_create['ICC_AVG_BALANCE_AMT'] = safe_decimal(row.get('ICC_AVG_BALANCE_AMT'))

                        # --- Flags (Boolean fields) ---
                        customer_data_to_create['CRT_GEORGE_FLAG'] = safe_boolean(row.get('CRT_GEORGE_FLAG'))
                        customer_data_to_create['PTS_IB_FLAG'] = safe_boolean(row.get('PTS_IB_FLAG'))
                        customer_data_to_create['APPLE_PAY_FLAG'] = safe_boolean(row.get('APPLE_PAY_FLAG'))
                        customer_data_to_create['GEORGE_PAY_FLAG'] = safe_boolean(row.get('GEORGE_PAY_FLAG'))
                        customer_data_to_create['GOOGLE_PAY_FLAG'] = safe_boolean(row.get('GOOGLE_PAY_FLAG'))
                        customer_data_to_create['WALLET_FLAG'] = safe_boolean(row.get('WALLET_FLAG'))
                        customer_data_to_create['PBS_FLAG'] = safe_boolean(row.get('PBS_FLAG'))
                        customer_data_to_create['DIRECT_DEBIT_FLAG'] = safe_boolean(row.get('DIRECT_DEBIT_FLAG'))
                        customer_data_to_create['GEORGE_INFO_FLAG'] = safe_boolean(row.get('GEORGE_INFO_FLAG'))
                        customer_data_to_create['LOA_REFUND_FLAG'] = safe_boolean(row.get('LOA_REFUND_FLAG'))
                        customer_data_to_create['LOA_TOTAL_REFUND_FLAG'] = safe_boolean(row.get('LOA_TOTAL_REFUND_FLAG'))
                        customer_data_to_create['MONEYBACK_FLAG'] = safe_boolean(row.get('MONEYBACK_FLAG'))
                        customer_data_to_create['PTS_CODEBTOR_STATUS_FLAG'] = safe_boolean(row.get('PTS_CODEBTOR_STATUS_FLAG'))

                        # --- Overdraft and Limits ---
                        customer_data_to_create['OVD_APPROVED_LIMIT_AMT'] = safe_decimal(row.get('OVD_APPROVED_LIMIT_AMT'))
                        customer_data_to_create['OVD_REMAINING_LIMIT_AMT'] = safe_decimal(row.get('OVD_REMAINING_LIMIT_AMT'))
                        customer_data_to_create['OVD_REMAINING_LIMIT_AMT_AVG'] = safe_decimal(row.get('OVD_REMAINING_LIMIT_AMT_AVG'))
                        customer_data_to_create['OVD_REMAINING_LIMIT_AMT_MIN'] = safe_decimal(row.get('OVD_REMAINING_LIMIT_AMT_MIN'))
                        customer_data_to_create['ICC_APPROVED_LIMIT'] = safe_decimal(row.get('ICC_APPROVED_LIMIT'))
                        customer_data_to_create['ICC_REMAINING_LIMIT_AMT'] = safe_decimal(row.get('ICC_REMAINING_LIMIT_AMT'))
                        customer_data_to_create['CLO_APPROVED_LIMIT'] = safe_decimal(row.get('CLO_APPROVED_LIMIT'))

                        # --- Transaction Counts ---
                        customer_data_to_create['TRX_IN_ALL_CNT'] = safe_int(row.get('TRX_IN_ALL_CNT'))
                        customer_data_to_create['TRX_IN_ATM_CNT'] = safe_int(row.get('TRX_IN_ATM_CNT'))
                        customer_data_to_create['TRX_IN_OTH_BNK_CNT'] = safe_int(row.get('TRX_IN_OTH_BNK_CNT'))
                        customer_data_to_create['TRX_IN_OTH_COUNTRY_CNT'] = safe_int(row.get('TRX_IN_OTH_COUNTRY_CNT'))
                        customer_data_to_create['TRX_OUT_ALL_CNT'] = safe_int(row.get('TRX_OUT_ALL_CNT'))
                        customer_data_to_create['TRX_OUT_ATM_CNT'] = safe_int(row.get('TRX_OUT_ATM_CNT'))
                        customer_data_to_create['TRX_OUT_CASH_CNT'] = safe_int(row.get('TRX_OUT_CASH_CNT'))
                        customer_data_to_create['TRX_OUT_EC_CNT'] = safe_int(row.get('TRX_OUT_EC_CNT'))
                        customer_data_to_create['TRX_OUT_IB_CNT'] = safe_int(row.get('TRX_OUT_IB_CNT'))
                        customer_data_to_create['TRX_OUT_INTER_TRANSFERS_CNT'] = safe_int(row.get('TRX_OUT_INTER_TRANSFERS_CNT'))
                        customer_data_to_create['TRX_OUT_OFF_DESK_CNT'] = safe_int(row.get('TRX_OUT_OFF_DESK_CNT'))
                        customer_data_to_create['TRX_OUT_OTH_COUNTRY_CNT'] = safe_int(row.get('TRX_OUT_OTH_COUNTRY_CNT'))
                        customer_data_to_create['TRX_OUT_POS_CNT'] = safe_int(row.get('TRX_OUT_POS_CNT'))
                        customer_data_to_create['ICC_TRX_ATM_CNT'] = safe_int(row.get('ICC_TRX_ATM_CNT'))
                        customer_data_to_create['PTS_REJECTED_LOANS_REQ_CNT'] = safe_int(row.get('PTS_REJECTED_LOANS_REQ_CNT'))
                        customer_data_to_create['PTS_TOTAL_LOANS_REQ_CNT'] = safe_int(row.get('PTS_TOTAL_LOANS_REQ_CNT'))

                        # --- Transaction Amounts ---
                        customer_data_to_create['TRX_IN_ALL_AMT'] = safe_decimal(row.get('TRX_IN_ALL_AMT'))
                        customer_data_to_create['TRX_IN_ATM_AMT'] = safe_decimal(row.get('TRX_IN_ATM_AMT'))
                        customer_data_to_create['TRX_IN_CRT_AMT'] = safe_decimal(row.get('TRX_IN_CRT_AMT'))
                        customer_data_to_create['TRX_IN_OTH_BNK_AMT'] = safe_decimal(row.get('TRX_IN_OTH_BNK_AMT'))
                        customer_data_to_create['TRX_IN_OTH_COUNTRY_AMT'] = safe_decimal(row.get('TRX_IN_OTH_COUNTRY_AMT'))
                        customer_data_to_create['TRX_OUT_ALL_AMT'] = safe_decimal(row.get('TRX_OUT_ALL_AMT'))
                        customer_data_to_create['TRX_OUT_ATM_AMT'] = safe_decimal(row.get('TRX_OUT_ATM_AMT'))
                        customer_data_to_create['TRX_OUT_CASH_AMT'] = safe_decimal(row.get('TRX_OUT_CASH_AMT'))
                        customer_data_to_create['TRX_OUT_EC_AMT'] = safe_decimal(row.get('TRX_OUT_EC_AMT'))
                        customer_data_to_create['TRX_OUT_IB_AMT'] = safe_decimal(row.get('TRX_OUT_IB_AMT'))
                        customer_data_to_create['TRX_OUT_INTER_TRANSFERS_AMT'] = safe_decimal(row.get('TRX_OUT_INTER_TRANSFERS_AMT'))
                        customer_data_to_create['TRX_OUT_OFF_DESK_AMT'] = safe_decimal(row.get('TRX_OUT_OFF_DESK_AMT'))
                        customer_data_to_create['TRX_OUT_OTH_COUNTRY_AMT'] = safe_decimal(row.get('TRX_OUT_OTH_COUNTRY_AMT'))
                        customer_data_to_create['TRX_OUT_POS_AMT'] = safe_decimal(row.get('TRX_OUT_POS_AMT'))
                        customer_data_to_create['ICC_TRX_ATM_AMT'] = safe_decimal(row.get('ICC_TRX_ATM_AMT'))

                        # --- MCC (Merchant Category Code) Transactions ---
                        customer_data_to_create['MCC_UTILITY_SERV_CNT'] = safe_int(row.get('MCC_UTILITY_SERV_CNT'))
                        customer_data_to_create['MCC_UTILITY_SERV_AMT'] = safe_decimal(row.get('MCC_UTILITY_SERV_AMT'))
                        customer_data_to_create['MCC_TRAVEL_CNT'] = safe_int(row.get('MCC_TRAVEL_CNT'))
                        customer_data_to_create['MCC_TRAVEL_AMT'] = safe_decimal(row.get('MCC_TRAVEL_AMT'))
                        customer_data_to_create['MCC_TRANSPORTATION_CNT'] = safe_int(row.get('MCC_TRANSPORTATION_CNT'))
                        customer_data_to_create['MCC_TRANSPORTATION_AMT'] = safe_decimal(row.get('MCC_TRANSPORTATION_AMT'))
                        customer_data_to_create['MCC_RETAIL_OUTLET_SERV_CNT'] = safe_int(row.get('MCC_RETAIL_OUTLET_SERV_CNT'))
                        customer_data_to_create['MCC_RETAIL_OUTLET_SERV_AMT'] = safe_decimal(row.get('MCC_RETAIL_OUTLET_SERV_AMT'))
                        customer_data_to_create['MCC_PROFESSIONAL_SERV_CNT'] = safe_int(row.get('MCC_PROFESSIONAL_SERV_CNT'))
                        customer_data_to_create['MCC_PROFESSIONAL_SERV_AMT'] = safe_decimal(row.get('MCC_PROFESSIONAL_SERV_AMT'))
                        customer_data_to_create['MCC_MONEY_TRANSFER_CNT'] = safe_int(row.get('MCC_MONEY_TRANSFER_CNT'))
                        customer_data_to_create['MCC_MONEY_TRANSFER_AMT'] = safe_decimal(row.get('MCC_MONEY_TRANSFER_AMT'))
                        customer_data_to_create['MCC_MISCELLANEOUS_STORES_CNT'] = safe_int(row.get('MCC_MISCELLANEOUS_STORES_CNT'))
                        customer_data_to_create['MCC_MISCELLANEOUS_STORES_AMT'] = safe_decimal(row.get('MCC_MISCELLANEOUS_STORES_AMT'))
                        customer_data_to_create['MCC_LEISURE_CNT'] = safe_int(row.get('MCC_LEISURE_CNT'))
                        customer_data_to_create['MCC_LEISURE_AMT'] = safe_decimal(row.get('MCC_LEISURE_AMT'))
                        customer_data_to_create['MCC_HOME_AND_CONSTR_CNT'] = safe_int(row.get('MCC_HOME_AND_CONSTR_CNT'))
                        customer_data_to_create['MCC_HOME_AND_CONSTR_AMT'] = safe_decimal(row.get('MCC_HOME_AND_CONSTR_AMT'))
                        customer_data_to_create['MCC_GOVERNMENT_SERV_CNT'] = safe_int(row.get('MCC_GOVERNMENT_SERV_CNT'))
                        customer_data_to_create['MCC_GOVERNMENT_SERV_AMT'] = safe_decimal(row.get('MCC_GOVERNMENT_SERV_AMT'))
                        customer_data_to_create['MCC_FOOD_CNT'] = safe_int(row.get('MCC_FOOD_CNT'))
                        customer_data_to_create['MCC_FOOD_AMT'] = safe_decimal(row.get('MCC_FOOD_AMT'))
                        customer_data_to_create['MCC_FINANCIAL_INST_CNT'] = safe_int(row.get('MCC_FINANCIAL_INST_CNT'))
                        customer_data_to_create['MCC_FINANCIAL_INST_AMT'] = safe_decimal(row.get('MCC_FINANCIAL_INST_AMT'))
                        customer_data_to_create['MCC_ELECT_AND_DIG_GOODS_CNT'] = safe_int(row.get('MCC_ELECT_AND_DIG_GOODS_CNT'))
                        customer_data_to_create['MCC_ELECT_AND_DIG_GOODS_AMT'] = safe_decimal(row.get('MCC_ELECT_AND_DIG_GOODS_AMT'))
                        customer_data_to_create['MCC_CONTRACTED_SERV_CNT'] = safe_int(row.get('MCC_CONTRACTED_SERV_CNT'))
                        customer_data_to_create['MCC_CONTRACTED_SERV_AMT'] = safe_decimal(row.get('MCC_CONTRACTED_SERV_AMT'))
                        customer_data_to_create['MCC_CLOTHING_STORES_CNT'] = safe_int(row.get('MCC_CLOTHING_STORES_CNT'))
                        customer_data_to_create['MCC_CLOTHING_STORES_AMT'] = safe_decimal(row.get('MCC_CLOTHING_STORES_AMT'))
                        customer_data_to_create['MCC_CAR_RENTAL_CNT'] = safe_int(row.get('MCC_CAR_RENTAL_CNT'))
                        customer_data_to_create['MCC_CAR_RENTAL_AMT'] = safe_decimal(row.get('MCC_CAR_RENTAL_AMT'))
                        customer_data_to_create['MCC_BUSINESS_SERV_CNT'] = safe_int(row.get('MCC_BUSINESS_SERV_CNT'))
                        customer_data_to_create['MCC_BUSINESS_SERV_AMT'] = safe_decimal(row.get('MCC_BUSINESS_SERV_AMT'))
                        customer_data_to_create['MCC_BANKING_ALTER_CNT'] = safe_int(row.get('MCC_BANKING_ALTER_CNT'))
                        customer_data_to_create['MCC_BANKING_ALTER_AMT'] = safe_decimal(row.get('MCC_BANKING_ALTER_AMT'))
                        customer_data_to_create['MCC_AGRICULTURAL_CNT'] = safe_int(row.get('MCC_AGRICULTURAL_CNT'))
                        customer_data_to_create['MCC_AGRICULTURAL_AMT'] = safe_decimal(row.get('MCC_AGRICULTURAL_AMT'))

                        # --- Channel Interactions ---
                        customer_data_to_create['CHNL_BRANCH_SCANS_CNT'] = safe_int(row.get('CHNL_BRANCH_SCANS_CNT'))
                        customer_data_to_create['CHNL_BRANCH_SCANS_DAYS_CNT'] = safe_int(row.get('CHNL_BRANCH_SCANS_DAYS_CNT'))
                        customer_data_to_create['CHNL_IB_LOGINS_CNT'] = safe_int(row.get('CHNL_IB_LOGINS_CNT'))
                        customer_data_to_create['CHNL_INBOUND_CALLS_CNT'] = safe_int(row.get('CHNL_INBOUND_CALLS_CNT'))
                        customer_data_to_create['CHNL_INBOUND_CALLS_DAYS_CNT'] = safe_int(row.get('CHNL_INBOUND_CALLS_DAYS_CNT'))

                        # --- Utilization Grades ---
                        customer_data_to_create['ICC_UTILIZATION_GRADE'] = safe_decimal(row.get('ICC_UTILIZATION_GRADE'))
                        customer_data_to_create['OVD_UTILIZATION_GRADE'] = safe_decimal(row.get('OVD_UTILIZATION_GRADE'))

                        # Filter out any keys from the CSV row that are not actual model fields
                        filtered_data = {
                            key: value for key, value in customer_data_to_create.items()
                            if key in model_field_names
                        }

                        # Use .create() to always create a new record.
                        # Note: This will create duplicate records if the script is run multiple times
                        # with the same CSV data, as 'ID' is no longer unique.
                        obj = CustomerData.objects.create(**filtered_data)
                        imported_count += 1

                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f"Error processing row {row_num} (ID: {row.get('ID', 'N/A')}, POSTING_DATE: {row.get('POSTING_DATE', 'N/A')}): {e}"))
                        skipped_count += 1

        except FileNotFoundError:
            raise CommandError(f"Error: The file '{file_path}' was not found. Please check the path.")
        except Exception as e:
            raise CommandError(f"An unexpected error occurred while reading the CSV file: {e}")

        self.stdout.write(self.style.SUCCESS(f"\n--- Data Import Summary ---"))
        self.stdout.write(self.style.SUCCESS(f"Successfully imported: {imported_count} records."))
        self.stdout.write(self.style.WARNING(f"Skipped due to errors: {skipped_count} records."))