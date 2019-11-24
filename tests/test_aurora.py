from unittest import mock

from pytest import fixture, mark

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
    expected = [{'id': 1, 'msg': 'hello'}]
    response = {
        'columnMetadata': [{'label': 'id'}, {'label': 'msg'}],
        'records': [[{'longValue': 1}, {'stringValue': 'hello'}]],
    }
    m_cli = m_boto3.Session.return_value.client.return_value
    m_cli.execute_statement.return_value = response
    aur = aurora.Aurora(database='test_db', **credentials)
    sql = 'select * from information_schema.tables'
    res = aur.execute(sql)

    assert res == expected
    m_cli.execute_statement.assert_called_once_with(
        includeResultMetadata=True,
        resourceArn=credentials['cluster_arn'],
        secretArn=credentials['secret_arn'],
        database='test_db',
        sql=sql,
    )


@mark.parametrize(
    'param,expected',
    [
        ({'stringValue': 'test'}, 'test'),
        ({'arrayValue': {'longValues': [1, 2, 3]}}, [1, 2, 3]),
        (
            {
                'arrayValue': {
                    'arrayValues': [
                        {'stringValue': 'foo'},
                        {'stringValue': 'bar'},
                    ]
                }
            },
            ['foo', 'bar'],
        ),
    ],
)
@mock.patch('aurora_term.aurora.boto3')
def test_fetch_value(m_boto3, param, expected, credentials):
    aur = aurora.Aurora(database='test_db', **credentials)
    value = aur._fetch_value(param)

    assert value == expected
