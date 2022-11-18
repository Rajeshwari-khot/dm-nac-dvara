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
    sqlalchemy.Column("value_status", sqlalchemy.String(length=250), nullable=True),
    sqlalchemy.Column("utr", sqlalchemy.String(length=250), nullable=True),
    sqlalchemy.Column("stage", sqlalchemy.String(length=250), nullable=True),
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


disbursement_status =sqlalchemy.Table(
    'disbursement_status',
    disbursement_metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True),   
    sqlalchemy.Column('status', sqlalchemy.String(length=250), nullable=True),
    sqlalchemy.Column('value_status', sqlalchemy.String(length=2000), nullable=True),
    sqlalchemy.Column('utr', sqlalchemy.String(length=2000), nullable=True),
    sqlalchemy.Column('stage', sqlalchemy.String(length=2000), nullable=True),
    sqlalchemy.Column("created_date", sqlalchemy.DateTime(), server_default=func.now()),
    sqlalchemy.Column("updated_date", sqlalchemy.DateTime(), server_default=func.now())
)
