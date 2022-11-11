import sqlalchemy
from sqlalchemy import func

dedupe_metadata = sqlalchemy.MetaData()    
dedupe = sqlalchemy.Table(
    "dedupe",
    dedupe_metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True),
    sqlalchemy.Column("dedupe_reference_id", sqlalchemy.String(length=250), nullable=True),
    sqlalchemy.Column("account_number", sqlalchemy.String(length=250), nullable=True),
    sqlalchemy.Column("contact_number", sqlalchemy.String(length=250), nullable=True),
    sqlalchemy.Column("customer_name", sqlalchemy.String(length=250), nullable=True),
    sqlalchemy.Column("dob", sqlalchemy.String(length=250), nullable=True),
    sqlalchemy.Column("id_type1", sqlalchemy.String(length=250), nullable=True),
    sqlalchemy.Column("id_value1", sqlalchemy.String(length=250), nullable=True),
    sqlalchemy.Column("id_type2", sqlalchemy.String(length=250), nullable=True),
    sqlalchemy.Column("id_value2", sqlalchemy.String(length=250), nullable=True),
    sqlalchemy.Column("loan_id", sqlalchemy.String(length=250), nullable=True),
    sqlalchemy.Column("pincode", sqlalchemy.String(length=250), nullable=True),
    sqlalchemy.Column("dedupe_present", sqlalchemy.String(length=250), nullable=True),
    sqlalchemy.Column("response_type", sqlalchemy.String(length=250), nullable=True),
    sqlalchemy.Column("result_attribute", sqlalchemy.String(length=250), nullable=True),
    sqlalchemy.Column("result_value", sqlalchemy.String(length=250), nullable=True),
    sqlalchemy.Column("result_rule_name", sqlalchemy.String(length=250), nullable=True),
    sqlalchemy.Column("result_ref_loan_id", sqlalchemy.String(length=250), nullable=True),
    sqlalchemy.Column("result_is_eligible", sqlalchemy.String(length=250), nullable=True),
    sqlalchemy.Column("result_message", sqlalchemy.String(length=250), nullable=True),
    sqlalchemy.Column("ref_originator_id", sqlalchemy.String(length=250), nullable=True),
    sqlalchemy.Column("ref_sector_id", sqlalchemy.String(length=250), nullable=True),
    sqlalchemy.Column("ref_max_dpd", sqlalchemy.String(length=250), nullable=True),
    sqlalchemy.Column("ref_first_name", sqlalchemy.String(length=250), nullable=True),
    sqlalchemy.Column("ref_date_of_birth", sqlalchemy.String(length=250), nullable=True),
    sqlalchemy.Column("ref_mobile_phone", sqlalchemy.String(length=250), nullable=True),
    sqlalchemy.Column("ref_account_number_loan_ref", sqlalchemy.String(length=250), nullable=True),
    sqlalchemy.Column("created_date", sqlalchemy.DateTime(), server_default=func.now()),
    sqlalchemy.Column("updated_date", sqlalchemy.DateTime(), server_default=func.now())   
)