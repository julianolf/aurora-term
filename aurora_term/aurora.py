import boto3


class Aurora:
    def __init__(
        self, profile='default', cluster_arn='', secret_arn='', database=''
    ):
        self.cli = boto3.Session(profile_name=profile).client('rds-data')
        self.cluster_arn = cluster_arn
        self.secret_arn = secret_arn
        self.database = database

    def _fetch_value(self, obj):
        key, value = next(iter(obj.items()))

        if key == 'arrayValue':
            return self._fetch_value(value)

        if key == 'arrayValues':
            return [self._fetch_value(v) for v in value]

        return value

    def _format_response(self, response):
        output = []
        labels = tuple(m['label'] for m in response['columnMetadata'])

        for row in response['records']:
            item = {labels[i]: self._fetch_value(v) for i, v in enumerate(row)}
            output.append(item)

        return output

    def execute(self, stmt):
        response = self.cli.execute_statement(
            includeResultMetadata=True,
            resourceArn=self.cluster_arn,
            secretArn=self.secret_arn,
            database=self.database,
            sql=stmt,
        )
        return self._format_response(response)
