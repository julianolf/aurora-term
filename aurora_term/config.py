import os
from dataclasses import dataclass


@dataclass
class Config:
    profile: str = os.getenv('AWS_PROFILE', 'default')
    cluster_arn: str = os.getenv('RDS_CLUSTER_ARN', '')
    secret_arn: str = os.getenv('RDS_SECRET_ARN', '')
    database: str = os.getenv('RDS_DB_NAME', '')