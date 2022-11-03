from typing import Optional

import sqlalchemy
from pydantic import BaseModel
from sqlalchemy import func


collect_metadata = sqlalchemy.MetaData()


collect = sqlalchemy.Table(
    "collect",
    collect_metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True),
    sqlalchemy.Column("demand_amount", sqlalchemy.Integer, nullable=True),
    sqlalchemy.Column("demand_date", sqlalchemy.String(length=250), nullable=True),
    sqlalchemy.Column("instrument_type", sqlalchemy.String(length=250), nullable=True),
    sqlalchemy.Column("partner_loan_id", sqlalchemy.String(length=250), nullable=True),
    sqlalchemy.Column("reference", sqlalchemy.String(length=250), nullable=True),
    sqlalchemy.Column("repayment_amount", sqlalchemy.Integer, nullable=True),
    sqlalchemy.Column("repayment_date", sqlalchemy.String(length=250), nullable=True),
    sqlalchemy.Column("settlement_date", sqlalchemy.String(length=250), nullable=True),
    sqlalchemy.Column("tds_amount", sqlalchemy.Integer, nullable=True),
    sqlalchemy.Column("outstanding_amount", sqlalchemy.Integer, nullable=True),
    sqlalchemy.Column("transaction_name", sqlalchemy.String(length=250), nullable=True),
    sqlalchemy.Column("created_date", sqlalchemy.DateTime(), server_default=func.now()),
    sqlalchemy.Column("updated_date", sqlalchemy.DateTime(), server_default=func.now())
)