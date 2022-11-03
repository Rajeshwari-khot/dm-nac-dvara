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
    sqlalchemy.Column("dedupe_results", sqlalchemy.String(length=2000), nullable=True),
    sqlalchemy.Column("created_date", sqlalchemy.DateTime(), server_default=func.now())
    

    
)