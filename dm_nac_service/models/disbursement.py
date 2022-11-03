import sqlalchemy
from sqlalchemy import func

disbursement_metadata = sqlalchemy.MetaData()
disbursement = sqlalchemy.Table(
    "disbursement",
    disbursement_metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True),
    sqlalchemy.Column("disbursement_reference_id", sqlalchemy.String(length=250), nullable=True),
    sqlalchemy.Column("disbursement_status", sqlalchemy.String(length=250), nullable=True),
    sqlalchemy.Column("stage", sqlalchemy.String(length=250), nullable=True),
    sqlalchemy.Column("utr", sqlalchemy.String(length=250), nullable=True),
    sqlalchemy.Column("message", sqlalchemy.String(length=250), nullable=True),
    sqlalchemy.Column("status", sqlalchemy.String(length=250), nullable=True),
    sqlalchemy.Column("originator_id", sqlalchemy.String(length=250), nullable=True),
    sqlalchemy.Column("sanction_reference_id", sqlalchemy.String(length=250), nullable=True),
    sqlalchemy.Column("customer_id", sqlalchemy.String(length=250), nullable=True),
    sqlalchemy.Column("requested_amount", sqlalchemy.String(length=250), nullable=True),
    sqlalchemy.Column("ifsc_code", sqlalchemy.String(length=250), nullable=True),
    sqlalchemy.Column("branch_name", sqlalchemy.String(length=250), nullable=True),
    sqlalchemy.Column("processing_fees", sqlalchemy.String(length=250), nullable=True),
    sqlalchemy.Column("insurance_amount", sqlalchemy.String(length=250), nullable=True),
    sqlalchemy.Column("disbursement_date", sqlalchemy.String(length=250), nullable=True),
    sqlalchemy.Column("created_date", sqlalchemy.DateTime(), server_default=func.now()),
    sqlalchemy.Column("updated_date", sqlalchemy.DateTime(), server_default=func.now())
)