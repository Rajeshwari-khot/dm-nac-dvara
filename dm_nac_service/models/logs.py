import sqlalchemy
from sqlalchemy import func

logs_metadata = sqlalchemy.MetaData()


api_logs = sqlalchemy.Table(
    "api_logs",
    logs_metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True),
    sqlalchemy.Column("channel", sqlalchemy.String(length=255), nullable=True),
    sqlalchemy.Column("request_url", sqlalchemy.String(length=2000), nullable=True),
    sqlalchemy.Column("request_method", sqlalchemy.String(length=255), nullable=True),
    sqlalchemy.Column("params", sqlalchemy.String(length=255), nullable=True),
    sqlalchemy.Column("request_body", sqlalchemy.String(length=5000), nullable=True),
    sqlalchemy.Column("response_body", sqlalchemy.String(length=5000), nullable=True),
    sqlalchemy.Column("status_code", sqlalchemy.String(length=255), nullable=True),
    sqlalchemy.Column("api_call_duration", sqlalchemy.String(length=255), nullable=True),
    sqlalchemy.Column("request_time", sqlalchemy.String(length=255), nullable=True),
    sqlalchemy.Column("created_date", sqlalchemy.DateTime(), server_default=func.now()),
    sqlalchemy.Column("updated_date", sqlalchemy.DateTime(), server_default=func.now())
)