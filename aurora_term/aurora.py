import boto3


class Aurora:
    def __init__(
        self, profile='default', cluster_arn='', secret_arn='', database=''
    ):
        self.cli = boto3.Session(profile_name=profile).client('rds-data')
        self.cluster_arn = cluster_arn
        self.secret_arn = secret_arn
        self.database = database

    def execute(self, stmt):
        return self.cli.execute_statement(
            resourceArn=self.cluster_arn,
            secretArn=self.secret_arn,
            database=self.database,
            sql=stmt,
        )
