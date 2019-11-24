from io import StringIO
from unittest import mock

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
    expected = '[{\'foo\': \'bar\'}]\n'
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
