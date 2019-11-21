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
