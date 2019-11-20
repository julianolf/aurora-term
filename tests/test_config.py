from dataclasses import asdict, is_dataclass

from aurora_term import config


def test_config():
    expected = {
        'profile': 'default',
        'cluster_arn': 'foo',
        'secret_arn': 'bar',
        'database': 'baz',
    }
    conf = config.Config(
        profile='default', cluster_arn='foo', secret_arn='bar', database='baz'
    )

    assert is_dataclass(conf)
    assert asdict(conf) == expected
