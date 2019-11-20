from aurora_term import terminal


def test_create_terminal():
    term = terminal.Terminal()
    assert isinstance(term, terminal.Terminal)


def test_terminal_quit_returns_true():
    term = terminal.Terminal()
    assert term.do_quit('')
