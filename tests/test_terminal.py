from aurora_term import aurora, config, terminal


def test_create_terminal():
    term = terminal.Terminal()
    assert isinstance(term, terminal.Terminal)
    assert isinstance(term.config, config.Config)
    assert isinstance(term.aurora, aurora.Aurora)


def test_terminal_quit_returns_true():
    term = terminal.Terminal()
    assert term.do_quit('')
