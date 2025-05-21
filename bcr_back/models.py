from django.db import models

class CustomerData(models.Model):
    """
    A Django model representing customer data from the Hackathon 2025 dataset.
    Each field corresponds to a column in the provided CSV description.
    """

    # Choices for categorical fields
    OCCUPATION_CHOICES = [
        ('BIOLOG', 'Biolog/ Zoolog'),
        ('ORG_EVENIM', 'Organizator de conferinte si evenimente'),
        ('CONTROLORI', 'Controlori/operatori pentru trafic naval si aerian'),
        ('COND_VEHIC', 'Conducatori de vehicule, soferi'),
        ('LEGISLATOR', 'Legislatori, membri ai executivului'),
        ('TRADUCAT', 'Traducator/ Interpret'),
        ('JURIST', 'Specialisti in domeniul juridic si asimilati'),
        ('ANALIST_IT', 'Analist/ Programator IT'),
        ('AG_VANZARI', 'Lucratori in domeniul vanzarilor'),
        ('AUTOR', 'Autor/Jurnalist'),
        ('INSP_VAMAL', 'Inspectori de vama si frontiera'),
        ('JURNALIST', 'Jurnalist'),
        ('PAZA_PROT', 'Lucratori in paza si protectie'),
        ('FOTOGRAF', 'Fotograf'),
        ('ANALIST', 'Analist financiar'),
        ('FIZIOTERAP', 'Fizioterapeut'),
        ('SPORTIV', 'Atleti si sportivi'),
        ('MAT_STAT', 'Matematician/Statistician'),
        ('AG_ASIG', 'Agent de asigurari'),
        ('TEHNICIENI', 'Tehnicieni in domeniul medical'),
        ('FIZ_CHIM', 'Fizician/ Chimist'),
        ('PREOT', 'Preot'),
        ('INSP_FISC', 'Inspector fiscal'),
        ('SPEC_HR', 'Specialist Resurse umane'),
        ('BUCATAR', 'Personal hoteluri/restaurante/baruri'),
        ('ARTIST', 'Artist'),
        ('AG_IMOB', 'Agenti si administratori imobiliari'),
        ('PSIHOLOG', 'Sociolog/ Psiholog'),
        ('PERS_INGR', 'Personal de ingrijire'),
        ('ANTRENOR', 'Antrenori, instructori'),
        ('CONSULT', 'Consultant financiar'),
        ('DESIGNER', 'Designer grafica'),
        ('ASIST_SOC', 'Specialisti in asistenta sociala'),
        ('INVATATOR', 'Cadru didactic'),
        ('MED_REZID', 'Medic rezident'),
        ('INGINER', 'Inginer'),
        ('VETERINAR', 'Veterinar'),
        ('ALTII', 'Altii'),
        ('MEDIC', 'Medic'),
        ('AUDITOR', 'Auditor/Contabil'),
        ('ASIST_VET', 'Asistenti veterinari'),
        ('ASIST_MED', 'Asistenti in domeniul medical'),
        ('NOTAR', 'Notar'),
        ('FUNCTIONAR', 'Functionari de birou'),
        ('PENS', 'Pensionari'),
        ('ANG_POL', 'Angajati in politie si jandarmerie'),
        ('COPII', 'Copii/Adolescenti'),
        ('STUD', 'Studenti'),
        ('ARHITECT', 'Arhitect'),
        ('NECALIF', 'Muncitori necalificati'),
        ('MAGISTRAT', 'Magistrat (judecatori, procurori)'),
        ('PENS_MIRA', 'Pensionari MIRA/MAPN'),
        ('ANG_ARMAT', 'Angajati in cadrul fortelor armate'),
        ('FARMA', 'Farmacist'),
        ('ECONOM', 'Economist'),
        ('STOM', 'Stomatolog'),
        ('INTREP', 'Liber Intreprinzatori'),
        ('ANG_PUB', 'Angajati in serviciul public'),
        ('PROFESOR', 'Profesori in inv superior, secundar si asimilati'),
        ('PERS_NEANG', 'Persoane neangajate'),
        ('CALIF', 'Meseriasi si muncitori calificati'),
        ('DIRECTOR', 'Directori generali, directori si asimilati'),
        ('COND_FUNC', 'Conducatori si functionari superiori in adm publ'),
        ('AVOCAT', 'Avocat'),
        ('EVAL', 'Evaluator'),
        ('PASTOR', 'Pastor'),
    ]

    MARITAL_STATUS_CHOICES = [
        ('D', 'Divortat'),
        ('C', 'Casatorit'),
        ('X', 'Unknown'),
        ('V', 'Vaduv'),
        ('N', 'Necasatorit'),
    ]

    CUSTOMER_TYPE_CHOICES = [
        ('STAND', 'Mass Market'),
        ('INDIV', 'Mass Affluent'),
    ]

    DOMICILE_CHOICES = [
        ('Urban', 'Urban'),
        ('Rural', 'Rural'),
    ]

    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('U', 'Unknown'),
    ]

    customer_id = models.CharField(max_length=255, help_text="Customer ID")
    POSTING_DATE = models.DateField(help_text="Reporting month (EOM)")
    GPI_AGE = models.IntegerField(null=True, blank=True, help_text="Client age in the current month")
    GPI_CLS_CODE_PT_OCCUP = models.CharField(
        max_length=255,
        choices=OCCUPATION_CHOICES,
        null=True,
        blank=True,
        help_text="Party classification for occupation code"
    )
    GPI_CLS_PT_EDU_DESC = models.CharField(max_length=255, null=True, blank=True, help_text="Party classification for education")
    GPI_COUNTY_NAME = models.CharField(max_length=255, null=True, blank=True, help_text="Client county domicile")
    GPI_DOMICILE_TYPE = models.CharField(
        max_length=50,
        choices=DOMICILE_CHOICES,
        null=True,
        blank=True,
        help_text="Client domicile type (Urban/Rural)"
    )
    GPI_GENDER_CODE = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
        null=True,
        blank=True,
        help_text="Party gender"
    )
    GPI_MARITAL_SATUS_CODE = models.CharField(
        max_length=10,
        choices=MARITAL_STATUS_CHOICES,
        null=True,
        blank=True,
        help_text="Party marital status"
    )
    GPI_REGION_NAME = models.CharField(max_length=255, null=True, blank=True, help_text="Client region domicile")
    GPI_CUSTOMER_TYPE_DESC = models.CharField(
        max_length=255,
        choices=CUSTOMER_TYPE_CHOICES,
        null=True,
        blank=True,
        help_text="Party type (mass market, mass affluent)"
    )

    # Tenure and Status
    CLIENT_TENURE = models.IntegerField(null=True, blank=True, help_text="Client tenure - calculated as difference between posting date and the first account opening date")
    CLIENT_TENURE_ACTIVE_ACC = models.IntegerField(null=True, blank=True, help_text="Number of days since the first active account opened")
    PTS_CIC_OPENED_ND = models.IntegerField(null=True, blank=True, help_text="Number of days since the CIC opening")
    PTS_CLIENT_STATUS_ND = models.IntegerField(null=True, blank=True, help_text="Number of days since the last 'Client' status from Sibcor")
    PTS_LST_SALARY_ND = models.IntegerField(null=True, blank=True, help_text="Number of days since the last salary received in the last month")
    ICC_LST_USE_ND = models.IntegerField(null=True, blank=True, help_text="Number of days since the last credit card transaction for credit cards")
    CLO_LST_ACC_CLOSE_ND = models.IntegerField(null=True, blank=True, help_text="Number of days from closing the last product for unsecured loans")
    CLO_MAX_MAT_LEFT_ACT_ND = models.IntegerField(null=True, blank=True, help_text="Maximum number of days to maturity for active products for unsecured loans")
    DEP_MAX_MAT_LEFT_ACT_ND = models.IntegerField(null=True, blank=True, help_text="Maximum number of days to maturity for active products for deposits")
    CRT_LST_ACC_CLOSE_ND = models.IntegerField(null=True, blank=True, help_text="Number of days from closing the last product for current accounts")
    CRT_FST_ACC_ACTIVE_OPEN_ND = models.IntegerField(null=True, blank=True, help_text="Number of days from opening the first active product for current accounts")


    # Product Counts (Active and Total)
    CEC_ALL_ACTIVE_CNT = models.IntegerField(null=True, blank=True, help_text="Number of all active economies")
    CEC_ALL_PROD_CNT = models.IntegerField(null=True, blank=True, help_text="Number of all economies account (active or not)")
    CLO_ALL_ACTIVE_CNT = models.IntegerField(null=True, blank=True, help_text="Number of active products for unsecured loans")
    CLO_ALL_PROD_CNT = models.IntegerField(null=True, blank=True, help_text="Number of all products until posting date for unsecured loans")
    CRT_ALL_ACTIVE_CNT = models.IntegerField(null=True, blank=True, help_text="Number of active products for current accounts")
    DEP_ALL_ACTIVE_CNT = models.IntegerField(null=True, blank=True, help_text="Number of active products for deposits")
    DEP_ALL_PROD_CNT = models.IntegerField(null=True, blank=True, help_text="Number of all products until posting date for deposits")
    ICC_ALL_ACTIVE_CNT = models.IntegerField(null=True, blank=True, help_text="Number of active products for credit cards")
    ICC_ALL_PROD_CNT = models.IntegerField(null=True, blank=True, help_text="Number of all products until posting date for credit cards")
    INS_VIG_ALL_ACTIVE_CNT = models.IntegerField(null=True, blank=True, help_text="Number of VIG insurance policies")
    INV_ALL_ACTIVE_CNT = models.IntegerField(null=True, blank=True, help_text="Number of active investments products in month")
    PPI_ALL_ACTIVE_CNT = models.IntegerField(null=True, blank=True, help_text="Number of payment protection insurances")
    REFIN_ALL_ACTIVE_CNT = models.IntegerField(null=True, blank=True, help_text="Number of active refinancings at the end of the posting month")
    REFIN_ALL_PROD_CNT = models.IntegerField(null=True, blank=True, help_text="Number of all refinancings until the end of the posting month")
    TER_ALL_ACTIVE_CNT = models.IntegerField(null=True, blank=True, help_text="Number of all active term deposits")
    TER_ALL_PROD_CNT = models.IntegerField(null=True, blank=True, help_text="Number of all term deposits (active or not)")
    OT_COLT_ALL_PROD_CNT = models.IntegerField(null=True, blank=True, help_text="Number of all products until posting date for collateral deposits")
    OT_COLT_ALL_ACTIVE_CNT = models.IntegerField(null=True, blank=True, help_text="Number of active products for collateral deposits")
    LOA_ALL_PROD_CNT = models.IntegerField(null=True, blank=True, help_text="Number of all products until posting date for loans")
    LOA_ALL_ACTIVE_CNT = models.IntegerField(null=True, blank=True, help_text="Number of active products for loans")
    CRT_ALL_PROD_CNT = models.IntegerField(null=True, blank=True, help_text="Number of all products until posting date for current accounts")
    CRT_ACTIVE_FC_CNT = models.IntegerField(null=True, blank=True, help_text="Number of active products in home currency for current accounts")
    CRT_ACTIVE_FX_CNT = models.IntegerField(null=True, blank=True, help_text="Number of active products in foreign currency for current accounts")


    # Balance Amounts
    CEC_AVG_BALANCE_AMT = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, help_text="Average balance amount for saving accounts")
    CEC_TOTAL_BALANCE_AMT = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, help_text="Total balance amount for savings accounts at the end of the month")
    CLO_AVG_BALANCE_AMT = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, help_text="Average balance amount for unsecured loans")
    CLO_MAX_BALANCE_AMT = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, help_text="Maximum balance amount for unsecured loans")
    CLO_MIN_BALANCE_AMT = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, help_text="Minimum balance amount for unsecured loans")
    CLO_TOTAL_BALANCE_AMT = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, help_text="Total balance amount at the end of the month for unsecured loans")
    CRT_AVG_BALANCE_AMT = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, help_text="Average balance amount for current accounts")
    CRT_MAX_BALANCE_AMT = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, help_text="Maximum balance amount for current accounts")
    CRT_MIN_BALANCE_AMT = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, help_text="Minimum balance amount for current accounts")
    CRT_TOTAL_BALANCE_AMT = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, help_text="Total balance amount at the end of the month for current accounts")
    DEP_AVG_BALANCE_AMT = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, help_text="Average balance amount for deposits")
    DEP_MAX_BALANCE_AMT = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, help_text="Maximum balance amount for deposits")
    DEP_MIN_BALANCE_AMT = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, help_text="Minimum balance amount for deposits")
    DEP_TOTAL_BALANCE_AMT = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, help_text="Total balance amount at the end of the month for deposits")
    DTER_AVG_BALANCE_AMT = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, help_text="Average balance amount for term deposits")
    DTER_TOTAL_BALANCE_AMT = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, help_text="Total balance amount for term deposits at the end of the month")
    ICC_MAX_BALANCE_AMT = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, help_text="Maximum balance amount for credit cards")
    ICC_MIN_BALANCE_AMT = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, help_text="Minimum balance amount for credit cards")
    ICC_TOTAL_BALANCE_AMT = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, help_text="Total balance amount at the end of the month for credit cards")
    OVD_AVG_BALANCE_AMT = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, help_text="Average balance amount for overdraft")
    OVD_MAX_BALANCE_AMT = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, help_text="Maximum balance amount for overdraft")
    OVD_MIN_BALANCE_AMT = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, help_text="Minimum balance amount for overdraft")
    OVD_TOTAL_BALANCE_AMT = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, help_text="Total balance amount at the end of the month for overdraft")
    SAV_AVG_BALANCE_AMT = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, help_text="Average balance amount for saving plans")
    SAV_TOTAL_BALANCE_AMT = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, help_text="Total balance for saving plans at the end of the month")
    OT_COLT_TOTAL_BALANCE_AMT = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, help_text="Total balance amount at the end of the month for collateral deposits")
    OT_COLT_MIN_BALANCE_AMT = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, help_text="Minimum balance amount for collateral deposits")
    OT_COLT_MAX_BALANCE_AMT = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, help_text="Maximum balance amount for collateral deposits")
    OT_COLT_AVG_BALANCE_AMT = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, help_text="Average balance amount for collateral deposits")
    LOA_TOTAL_BALANCE_AMT = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, help_text="Total balance amount at the end of the month for loans")
    LOA_MIN_BALANCE_AMT = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, help_text="Minimum balance amount for loans")
    LOA_MAX_BALANCE_AMT = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, help_text="Maximum balance amount for loans")
    LOA_AVG_BALANCE_AMT = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, help_text="Average balance amount for loans")
    ICC_AVG_BALANCE_AMT = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, help_text="Average balance amount for credit cards")


    # Flags (Boolean fields)
    CRT_GEORGE_FLAG = models.BooleanField(null=True, blank=True, help_text="Flag 1/0 if the client has an active George CA as of end of the month")
    PTS_IB_FLAG = models.BooleanField(null=True, blank=True, help_text="Internet banking flag (George)")
    APPLE_PAY_FLAG = models.BooleanField(null=True, blank=True, help_text="Flag 1/0 if the client has Apple Pay as of end of the posting month")
    GEORGE_PAY_FLAG = models.BooleanField(null=True, blank=True, help_text="Flag 1/0 if the client has George Pay as of end of the posting month")
    GOOGLE_PAY_FLAG = models.BooleanField(null=True, blank=True, help_text="Flag 1/0 if the client has Google Pay as of end of the posting month")
    WALLET_FLAG = models.BooleanField(null=True, blank=True, help_text="Flag 1/0 if the client has at least one card enrolled in wallet as of end of the posting month")
    PBS_FLAG = models.BooleanField(null=True, blank=True, help_text="PBS flag based on party benefit packages")
    DIRECT_DEBIT_FLAG = models.BooleanField(null=True, blank=True, help_text="Flag 1/0 if the client has Direct Debit as of end of the posting month")
    GEORGE_INFO_FLAG = models.BooleanField(null=True, blank=True, help_text="Flag 1/0 if the client has George Info as of end of the posting month (push notification)")
    LOA_REFUND_FLAG = models.BooleanField(null=True, blank=True, help_text="Flag 1/0 if the client has a loan refund in month")
    LOA_TOTAL_REFUND_FLAG = models.BooleanField(null=True, blank=True, help_text="Flag 1/0 if the client has a total loan refund in month")
    MONEYBACK_FLAG = models.BooleanField(null=True, blank=True, help_text="Flag 1/0 if the client has Money Back (cash-back service) as of end of the posting month")
    PTS_CODEBTOR_STATUS_FLAG = models.BooleanField(null=True, blank=True, help_text="Flag 1/0 if party is codebtor for other party loans")


    # Overdraft and Limits
    OVD_APPROVED_LIMIT_AMT = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, help_text="Overdraft approved limit")
    OVD_REMAINING_LIMIT_AMT = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, help_text="Overdraft remaining limit at the end of the posting month")
    OVD_REMAINING_LIMIT_AMT_AVG = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, help_text="Average overdraft remaining limit in the posting month")
    OVD_REMAINING_LIMIT_AMT_MIN = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, help_text="Minimum overdraft remaining limit in the posting month")
    ICC_APPROVED_LIMIT = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, help_text="Approved limit for credit cards")
    ICC_REMAINING_LIMIT_AMT = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, help_text="Overdraft remaining limit at the end of the posting month (Note: description says overdraft but field name is ICC)")
    CLO_APPROVED_LIMIT = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, help_text="Approved limit for unsecured loans")


    # Transaction Counts
    TRX_IN_ALL_CNT = models.IntegerField(null=True, blank=True, help_text="Number of incoming payments")
    TRX_IN_ATM_CNT = models.IntegerField(null=True, blank=True, help_text="Total number of ATM/APT/MFM/NCR inflows in the posting month")
    TRX_IN_OTH_BNK_CNT = models.IntegerField(null=True, blank=True, help_text="Number of other banks receipts in the current month")
    TRX_IN_OTH_COUNTRY_CNT = models.IntegerField(null=True, blank=True, help_text="Number of other country receipts in the current month")
    TRX_OUT_ALL_CNT = models.IntegerField(null=True, blank=True, help_text="Number of outgoing payments")
    TRX_OUT_ATM_CNT = models.IntegerField(null=True, blank=True, help_text="Total number of ATM/APT/MFM/NCR outflows in the posting month")
    TRX_OUT_CASH_CNT = models.IntegerField(null=True, blank=True, help_text="Number of outgoing transactions in the current month")
    TRX_OUT_EC_CNT = models.IntegerField(null=True, blank=True, help_text="Number of e-commerce transactions in the current month")
    TRX_OUT_IB_CNT = models.IntegerField(null=True, blank=True, help_text="Number of internet banking transactions in the current month")
    TRX_OUT_INTER_TRANSFERS_CNT = models.IntegerField(null=True, blank=True, help_text="Number of interbanking transfers in the posting month")
    TRX_OUT_OFF_DESK_CNT = models.IntegerField(null=True, blank=True, help_text="Number of office desk transactions in the current month")
    TRX_OUT_OTH_COUNTRY_CNT = models.IntegerField(null=True, blank=True, help_text="Number of other country transactions in the current month")
    TRX_OUT_POS_CNT = models.IntegerField(null=True, blank=True, help_text="POS number of transactions in the current month")
    ICC_TRX_ATM_CNT = models.IntegerField(null=True, blank=True, help_text="Number of ATM withdrawals with credit card for credit cards")
    PTS_REJECTED_LOANS_REQ_CNT = models.IntegerField(null=True, blank=True, help_text="Total number of rejected loan requests")
    PTS_TOTAL_LOANS_REQ_CNT = models.IntegerField(null=True, blank=True, help_text="Total number of loan requests")


    # Transaction Amounts
    TRX_IN_ALL_AMT = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, help_text="Total amount of incoming payments")
    TRX_IN_ATM_AMT = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, help_text="Total amount of ATM/APT/MFM/NCR inflows in the posting month")
    TRX_IN_CRT_AMT = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, help_text="Total amount of current account inflows in the posting month")
    TRX_IN_OTH_BNK_AMT = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, help_text="Other banks receipts amount in the current month")
    TRX_IN_OTH_COUNTRY_AMT = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, help_text="Other country receipts amount in the current month")
    TRX_OUT_ALL_AMT = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, help_text="Total amount of outgoing payments")
    TRX_OUT_ATM_AMT = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, help_text="Total amount of ATM/APT/MFM/NCR outflows in the posting month")
    TRX_OUT_CASH_AMT = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, help_text="Outgoing cash transactions in the current month")
    TRX_OUT_EC_AMT = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, help_text="E-commerce transactions amount in the current month")
    TRX_OUT_IB_AMT = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, help_text="Internet banking transactions amount in the current month")
    TRX_OUT_INTER_TRANSFERS_AMT = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, help_text="Total amount of interbanking transfers in the posting month")
    TRX_OUT_OFF_DESK_AMT = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, help_text="Office desk transactions amount in the current month")
    TRX_OUT_OTH_COUNTRY_AMT = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, help_text="Other country transactions amount in the current month")
    TRX_OUT_POS_AMT = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, help_text="POS transactions amount in the current month")
    ICC_TRX_ATM_AMT = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, help_text="Total ATM amount withdrawals with credit card for credit cards")


    # MCC (Merchant Category Code) Transactions
    MCC_UTILITY_SERV_CNT = models.IntegerField(null=True, blank=True, help_text="Number of utility services MCC transactions")
    MCC_UTILITY_SERV_AMT = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, help_text="Amount of utility services MCC transactions")
    MCC_TRAVEL_CNT = models.IntegerField(null=True, blank=True, help_text="Number of travel MCC transactions")
    MCC_TRAVEL_AMT = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, help_text="Amount of travel MCC transactions")
    MCC_TRANSPORTATION_CNT = models.IntegerField(null=True, blank=True, help_text="Number of transportation MCC transactions")
    MCC_TRANSPORTATION_AMT = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, help_text="Amount of transportation MCC transactions")
    MCC_RETAIL_OUTLET_SERV_CNT = models.IntegerField(null=True, blank=True, help_text="Number of retail outlet services MCC transactions")
    MCC_RETAIL_OUTLET_SERV_AMT = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, help_text="Amount of retail outlet services MCC transactions")
    MCC_PROFESSIONAL_SERV_CNT = models.IntegerField(null=True, blank=True, help_text="Number of professional services and membership organizations MCC transactions")
    MCC_PROFESSIONAL_SERV_AMT = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, help_text="Amount of professional services and membership organizations MCC transactions")
    MCC_MONEY_TRANSFER_CNT = models.IntegerField(null=True, blank=True, help_text="Number of money transfer MCC transactions")
    MCC_MONEY_TRANSFER_AMT = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, help_text="Amount of money transfer MCC transactions")
    MCC_MISCELLANEOUS_STORES_CNT = models.IntegerField(null=True, blank=True, help_text="Number of miscellaneous stores MCC transactions")
    MCC_MISCELLANEOUS_STORES_AMT = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, help_text="Amount of miscellaneous stores MCC transactions")
    MCC_LEISURE_CNT = models.IntegerField(null=True, blank=True, help_text="Number of leisure MCC transactions")
    MCC_LEISURE_AMT = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, help_text="Amount of leisure MCC transactions")
    MCC_HOME_AND_CONSTR_CNT = models.IntegerField(null=True, blank=True, help_text="Number of home and construction MCC transactions")
    MCC_HOME_AND_CONSTR_AMT = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, help_text="Amount of home and construction MCC transactions")
    MCC_GOVERNMENT_SERV_CNT = models.IntegerField(null=True, blank=True, help_text="Number of government services MCC transactions")
    MCC_GOVERNMENT_SERV_AMT = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, help_text="Amount of government services MCC transactions")
    MCC_FOOD_CNT = models.IntegerField(null=True, blank=True, help_text="Number of food MCC transactions")
    MCC_FOOD_AMT = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, help_text="Amount of food MCC transactions")
    MCC_FINANCIAL_INST_CNT = models.IntegerField(null=True, blank=True, help_text="Number of financial institutions MCC transactions")
    MCC_FINANCIAL_INST_AMT = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, help_text="Amount of financial institutions MCC transactions")
    MCC_ELECT_AND_DIG_GOODS_CNT = models.IntegerField(null=True, blank=True, help_text="Number of electronic and digital goods MCC transactions")
    MCC_ELECT_AND_DIG_GOODS_AMT = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, help_text="Amount of electronic and digital goods MCC transactions")
    MCC_CONTRACTED_SERV_CNT = models.IntegerField(null=True, blank=True, help_text="Number of contracted services MCC transactions")
    MCC_CONTRACTED_SERV_AMT = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, help_text="Amount of contracted services MCC transactions")
    MCC_CLOTHING_STORES_CNT = models.IntegerField(null=True, blank=True, help_text="Number of clothing stores MCC transactions")
    MCC_CLOTHING_STORES_AMT = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, help_text="Amount of clothing stores MCC transactions")
    MCC_CAR_RENTAL_CNT = models.IntegerField(null=True, blank=True, help_text="Number of car rental MCC transactions")
    MCC_CAR_RENTAL_AMT = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, help_text="Amount of car rental MCC transactions")
    MCC_BUSINESS_SERV_CNT = models.IntegerField(null=True, blank=True, help_text="Number of business services MCC transactions")
    MCC_BUSINESS_SERV_AMT = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, help_text="Amount of business services MCC transactions")
    MCC_BANKING_ALTER_CNT = models.IntegerField(null=True, blank=True, help_text="Number of banking alternative MCC transactions")
    MCC_BANKING_ALTER_AMT = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, help_text="Amount of banking alternative MCC transactions")
    MCC_AGRICULTURAL_CNT = models.IntegerField(null=True, blank=True, help_text="Number of agricultural MCC transactions")
    MCC_AGRICULTURAL_AMT = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, help_text="Amount of agricultural MCC transactions")


    # Channel Interactions
    CHNL_BRANCH_SCANS_CNT = models.IntegerField(null=True, blank=True, help_text="Number of branch ID scans in the posting month")
    CHNL_BRANCH_SCANS_DAYS_CNT = models.IntegerField(null=True, blank=True, help_text="Number of days with branch ID scans in the posting month")
    CHNL_IB_LOGINS_CNT = models.IntegerField(null=True, blank=True, help_text="Number of Internet Banking logins")
    CHNL_INBOUND_CALLS_CNT = models.IntegerField(null=True, blank=True, help_text="Number of inbound call center calls")
    CHNL_INBOUND_CALLS_DAYS_CNT = models.IntegerField(null=True, blank=True, help_text="Number of days with Contact Center inbound calls in the posting month")

    # Utilization Grades
    ICC_UTILIZATION_GRADE = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="Maximum utilization grade per day in month for credit cards")
    OVD_UTILIZATION_GRADE = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="Maximum utilization grade per day in month for overdraft")


    class Meta:
        verbose_name = "Customer Data Entry"
        verbose_name_plural = "Customer Data Entries"

    def __str__(self):
        return f"Customer ID: {self.customer_id} - Date: {self.POSTING_DATE}"

