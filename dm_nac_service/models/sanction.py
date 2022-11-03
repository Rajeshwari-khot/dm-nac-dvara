
from typing import Optional
from enum import Enum

import sqlalchemy
from pydantic import BaseModel
from sqlalchemy import func






sanction_metadata = sqlalchemy.MetaData()


sanction = sqlalchemy.Table(
    'sanction',
    sanction_metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True),
    sqlalchemy.Column('message', sqlalchemy.String(length=250), nullable=True),
    sqlalchemy.Column('sanction_status', sqlalchemy.String(length=250), nullable=True),
    sqlalchemy.Column('customer_id', sqlalchemy.String(length=500), nullable=True),
    sqlalchemy.Column('client_id', sqlalchemy.String(length=250), nullable=True),
    sqlalchemy.Column('status', sqlalchemy.String(length=250), nullable=True),
    sqlalchemy.Column('value_status', sqlalchemy.String(length=2000), nullable=True),
    sqlalchemy.Column('stage', sqlalchemy.String(length=2000), nullable=True),
    
    sqlalchemy.Column('sanction_reference_id', sqlalchemy.String(length=250), nullable=True),
    sqlalchemy.Column('bureau_fetch_status', sqlalchemy.String(length=250), nullable=True),
    sqlalchemy.Column('reject_reason', sqlalchemy.String(length=250), nullable=True),
    # sqlalchemy.Column('first_name', sqlalchemy.String(length=250), nullable=True),
    # sqlalchemy.Column('last_name', sqlalchemy.String(length=250), nullable=True),
    # sqlalchemy.Column('father_name', sqlalchemy.String(length=250), nullable=True),
    # sqlalchemy.Column('gender', sqlalchemy.String(length=250), nullable=True),
    # sqlalchemy.Column('id_proof_type_from_partner', sqlalchemy.String(length=250), nullable=True),
    # sqlalchemy.Column('id_proof_number_from_partner', sqlalchemy.String(length=250), nullable=True),
    # sqlalchemy.Column('address_proof_type_from_partner', sqlalchemy.String(length=250), nullable=True),
    # sqlalchemy.Column('address_proof_number_from_partner', sqlalchemy.String(length=250), nullable=True),
    # sqlalchemy.Column('dob', sqlalchemy.String(length=250), nullable=True),
    # sqlalchemy.Column('owned_vehicle', sqlalchemy.String(length=250), nullable=True),
    # sqlalchemy.Column('curr_door_and_building', sqlalchemy.String(length=250), nullable=True),
    # sqlalchemy.Column('curr_street_and_locality', sqlalchemy.String(length=250), nullable=True),
    # sqlalchemy.Column('curr_landmark', sqlalchemy.String(length=250), nullable=True),
    # sqlalchemy.Column('curr_city', sqlalchemy.String(length=250), nullable=True),
    # sqlalchemy.Column('curr_district', sqlalchemy.String(length=250), nullable=True),
    # sqlalchemy.Column('curr_state', sqlalchemy.String(length=250), nullable=True),
    # sqlalchemy.Column('curr_pincode', sqlalchemy.String(length=250), nullable=True),
    # sqlalchemy.Column('perm_door_and_building', sqlalchemy.String(length=250), nullable=True),
    # sqlalchemy.Column('perm_landmark', sqlalchemy.String(length=250), nullable=True),
    # sqlalchemy.Column('perm_city', sqlalchemy.String(length=250), nullable=True),
    # sqlalchemy.Column('perm_district', sqlalchemy.String(length=250), nullable=True),
    # sqlalchemy.Column('perm_state', sqlalchemy.String(length=250), nullable=True),
    # sqlalchemy.Column('perm_pincode', sqlalchemy.String(length=250), nullable=True),
    # sqlalchemy.Column('occupation', sqlalchemy.String(length=250), nullable=True),
    # sqlalchemy.Column('company_name', sqlalchemy.String(length=250), nullable=True),
    # sqlalchemy.Column('gross_monthly_income', sqlalchemy.Integer, nullable=True),
    # sqlalchemy.Column('net_monthly_income', sqlalchemy.Integer, nullable=True),
    # sqlalchemy.Column('income_validation_status', sqlalchemy.String(length=250), nullable=True),
    # sqlalchemy.Column('pan', sqlalchemy.String(length=250), nullable=True),
    # sqlalchemy.Column('purpose_of_loan', sqlalchemy.String(length=250), nullable=True),
    # sqlalchemy.Column('loan_amount', sqlalchemy.Integer, nullable=True),
    # sqlalchemy.Column('interest_rate', sqlalchemy.Integer, nullable=True),
    # sqlalchemy.Column('schedule_start_date', sqlalchemy.String(length=250), nullable=True),
    # sqlalchemy.Column('first_installment_date', sqlalchemy.String(length=250), nullable=True),
    # sqlalchemy.Column('total_processing_fees', sqlalchemy.Integer, nullable=True),
    # sqlalchemy.Column('gst', sqlalchemy.Integer, nullable=True),
    # sqlalchemy.Column('pre_emi_amount', sqlalchemy.Integer, nullable=True),
    # sqlalchemy.Column('emi', sqlalchemy.Integer, nullable=True),
    # sqlalchemy.Column('emi_date', sqlalchemy.String(length=250), nullable=True),
    # sqlalchemy.Column('emi_week', sqlalchemy.Integer, nullable=True),
    # sqlalchemy.Column('repayment_frequency', sqlalchemy.String(length=250), nullable=True),
    # sqlalchemy.Column('repayment_mode', sqlalchemy.String(length=250), nullable=True),
    # sqlalchemy.Column('tenure_value', sqlalchemy.Integer, nullable=True),
    # sqlalchemy.Column('tenure_units', sqlalchemy.String(length=250), nullable=True),
    # sqlalchemy.Column('product_name', sqlalchemy.String(length=250), nullable=True),
    # sqlalchemy.Column('primary_bank_account', sqlalchemy.String(length=250), nullable=True),
    # sqlalchemy.Column('bank_name', sqlalchemy.String(length=250), nullable=True),
    # sqlalchemy.Column('mode_of_salary', sqlalchemy.String(length=250), nullable=True),
    # sqlalchemy.Column('client_id', sqlalchemy.String(length=250), nullable=True),
    sqlalchemy.Column('dedupe_reference_id', sqlalchemy.String(length=250), nullable=True),
    # sqlalchemy.Column('email', sqlalchemy.String(length=250), nullable=True),
    # sqlalchemy.Column('middle_name', sqlalchemy.String(length=250), nullable=True),
    # sqlalchemy.Column('marital_status', sqlalchemy.String(length=250), nullable=True),
    sqlalchemy.Column('loan_id', sqlalchemy.String(length=250), nullable=True),
    sqlalchemy.Column("created_date", sqlalchemy.DateTime(), server_default=func.now()),
    sqlalchemy.Column("updated_date", sqlalchemy.DateTime(), server_default=func.now())
)

sanction_fileupload = sqlalchemy.Table(
    'sanction_fileupload',
    sanction_metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True),
    sqlalchemy.Column('message', sqlalchemy.String(length=2000), nullable=True),
    sqlalchemy.Column('status', sqlalchemy.String(length=250), nullable=True),
    sqlalchemy.Column("created_date", sqlalchemy.DateTime(), server_default=func.now()),
    sqlalchemy.Column("updated_date", sqlalchemy.DateTime(), server_default=func.now())
)

sanction_status =sqlalchemy.Table(
    'sanction_status',
    sanction_metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True),
    
    sqlalchemy.Column('status', sqlalchemy.String(length=250), nullable=True),
    sqlalchemy.Column('value_status', sqlalchemy.String(length=2000), nullable=True),
    sqlalchemy.Column('stage', sqlalchemy.String(length=2000), nullable=True),
    sqlalchemy.Column('bureau_fetch_status', sqlalchemy.String(length=2000), nullable=True),
    sqlalchemy.Column("created_date", sqlalchemy.DateTime(), server_default=func.now()),
    sqlalchemy.Column("updated_date", sqlalchemy.DateTime(), server_default=func.now())

)