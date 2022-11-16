import sqlalchemy
from sqlalchemy import func

disbursement_metadata = sqlalchemy.MetaData()    
disbursement = sqlalchemy.Table(
    "disbursement",
    disbursement_metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True),
    sqlalchemy.Column("disbursement_reference_id", sqlalchemy.String(length=250), nullable=True),
    sqlalchemy.Column("message", sqlalchemy.String(length=250), nullable=True),
    sqlalchemy.Column("status", sqlalchemy.String(length=250), nullable=True),
    sqlalchemy.Column("originatorId", sqlalchemy.String(length=250), nullable=True),
    sqlalchemy.Column("sanctionReferenceId", sqlalchemy.String(length=250), nullable=True),
    sqlalchemy.Column("customerId", sqlalchemy.String(length=250), nullable=True),
    sqlalchemy.Column("requestedAmount", sqlalchemy.String(length=250), nullable=True),
    sqlalchemy.Column("ifscCode", sqlalchemy.String(length=250), nullable=True),
    sqlalchemy.Column("branchName", sqlalchemy.String(length=250), nullable=True),
    sqlalchemy.Column("insuranceAmount", sqlalchemy.String(length=250), nullable=True),
    sqlalchemy.Column("processingFees", sqlalchemy.String(length=250), nullable=True),
    sqlalchemy.Column("disbursementDate", sqlalchemy.String(length=250), nullable=True),
)
