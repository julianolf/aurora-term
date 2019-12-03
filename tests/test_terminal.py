from io import StringIO
from unittest import mock

import pytest

from aurora_term import aurora, config, terminal


@mock.patch('aurora_term.aurora.boto3')
def test_create_terminal(m_boto3):
    term = terminal.Terminal()
    assert isinstance(term, terminal.Terminal)
    assert isinstance(term.config, config.Config)
    assert isinstance(term.aurora, aurora.Aurora)


@mock.patch('aurora_term.aurora.boto3')
def test_terminal_quit_returns_true(m_boto3):
    term = terminal.Terminal()
    assert term.do_quit('')


@mock.patch('sys.stdout', new_callable=StringIO)
@mock.patch('aurora_term.terminal.aurora')
def test_terminal_default_output(m_aurora, m_stdout):
    expected = '\nfoo: bar\n\n'
    m_aurora.Aurora.return_value.execute.return_value = [{'foo': 'bar'}]
    line = 'select * from test'
    term = terminal.Terminal()
    term.default(line)

    assert m_stdout.getvalue() == expected
    m_aurora.Aurora.return_value.execute.assert_called_once_with(line)


@mock.patch('sys.stdout', new_callable=StringIO)
@mock.patch('aurora_term.terminal.aurora')
def test_terminal_default_handles_exceptions(m_aurora, m_stdout):
    msg = 'something went wrong'
    expected = f'{msg}\n'
    m_aurora.Aurora.return_value.execute.side_effect = Exception(msg)
    line = 'select * from test'
    term = terminal.Terminal()
    term.default(line)

    assert m_stdout.getvalue() == expected
    m_aurora.Aurora.return_value.execute.assert_called_once_with(line)


@pytest.mark.parametrize(
    'data,expected', [([{'foo': 'bar'}], '\nfoo: bar\n'), ([], '')]
)
@mock.patch('aurora_term.terminal.aurora')
def test_terminal_format_default(m_aurora, data, expected):
    term = terminal.Terminal()
    got = term._format_default(data)

    assert got == expected


@pytest.mark.parametrize(
    'data,expected',
    [
        ([{'foo': 'bar', 'baz': 'bla'}], 'foo | baz\n----+----\nbar | bla'),
        ([], ''),
    ],
)
@mock.patch('aurora_term.terminal.aurora')
def test_terminal_format_table(m_aurora, data, expected):
    term = terminal.Terminal()
    got = term._format_table(data)

    assert got == expected


@pytest.mark.parametrize(
    'data,expected',
    [([{'foo': 'bar'}], '[\n  {\n    "foo": "bar"\n  }\n]'), ([], '[]')],
)
@mock.patch('aurora_term.terminal.aurora')
def test_terminal_format_json(m_aurora, data, expected):
    term = terminal.Terminal()
    got = term._format_json(data)

    assert got == expected


@pytest.mark.parametrize(
    'fmt,expected',
    [
        ('default', '\nfoo: bar\n\n'),
        ('table', 'foo\n---\nbar\n'),
        ('json', '[\n  {\n    "foo": "bar"\n  }\n]\n'),
    ],
)
@mock.patch('sys.stdout', new_callable=StringIO)
@mock.patch('aurora_term.terminal.aurora')
def test_terminal_changes_format_output(m_aurora, m_stdout, fmt, expected):
    m_aurora.Aurora.return_value.execute.return_value = [{'foo': 'bar'}]
    term = terminal.Terminal()
    term.do_format(fmt)
    term.default('select * from test')

    assert m_stdout.getvalue() == expected


@mock.patch('sys.stdout', new_callable=StringIO)
@mock.patch('aurora_term.terminal.aurora')
def test_terminal_handles_invalid_format_input(m_aurora, m_stdout):
    expected = '"cool" is not a valid format.\n'
    term = terminal.Terminal()
    term.do_format('cool')

    assert m_stdout.getvalue() == expected
