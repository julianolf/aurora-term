from unittest import mock

from pytest import fixture

from aurora_term import aurora


@fixture
def credentials():
    return {
        'cluster_arn': 'arn:aws:rds:us-east-1:123:cluster:foo',
        'secret_arn': 'arn:aws:secretsmanager:us-east-1:123:secret:bar',
    }


@mock.patch('aurora_term.aurora.boto3')
def test_create_aurora(m_boto3, credentials):
    aur = aurora.Aurora(database='test_db', **credentials)

    assert isinstance(aur, aurora.Aurora)
    assert aur.cluster_arn == credentials['cluster_arn']
    assert aur.secret_arn == credentials['secret_arn']
    assert aur.database == 'test_db'
    m_boto3.Session.assert_called_once_with(profile_name='default')
    m_boto3.Session.return_value.client.assert_called_once_with('rds-data')


@mock.patch('aurora_term.aurora.boto3')
def test_aurora_execute_statement(m_boto3, credentials):
    aur = aurora.Aurora(database='test_db', **credentials)
    sql = 'select * from information_schema.tables'
    aur.execute(sql)

    m_cli = m_boto3.Session.return_value.client.return_value
    m_cli.execute_statement.assert_called_once_with(
        resourceArn=credentials['cluster_arn'],
        secretArn=credentials['secret_arn'],
        database='test_db',
        sql=sql,
    )
