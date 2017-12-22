import os
import textwrap

import pytest

import frontdoor


def test_from_root(monkeypatch):
    monkeypatch.setattr(frontdoor, 'ROOT', '~root~')
    monkeypatch.setattr(os, 'name', 'nt')
    assert ('~root~\\a\\b\\c' == frontdoor.from_root('a/b/c')
            or '~root~/a\\b\\c' == frontdoor.from_root('a/b/c'))
    monkeypatch.setattr(os, 'name', 'linux')
    assert '~root~/a/b/c' == frontdoor.from_root('a/b/c')


def assert_silence(capsys):
    out, err = capsys.readouterr()
    assert out == ''
    assert err == ''


class TestCommandRegistry(object):

    @pytest.fixture(autouse=True)
    def setup(self):
        self.registry = frontdoor.CommandRegistry('my-tool')
        cmd = self.registry.decorate

        self._remembered_args = None

        @cmd('arg-to-number', desc='Converts arg 1 to exit code.')
        def arg_to_number(args):
            return int(args[0])

        @cmd(['r', 'remember_args'],
             help='Extra long-winded, helpful info can go here.')
        def remember_args(args):
            self._remembered_args = args

    EXPECTED_HELP = textwrap.dedent("""\
            {}
                arg-to-number   Converts arg 1 to exit code.
                help
                r,remember_args
            """)

    @pytest.fixture
    def fake_help(self):
        state = {}

        def fake_help(args):
            print("HELP-GOES-HERE")
            state['called'] = True
            assert [] == args

        self.registry.help = fake_help
        yield
        assert 'called' in state

    @pytest.mark.parametrize(
        'registry_name,args,expected_prefix,expected_result',
        [
            ('my-tool', [], 'Available options for my-tool:', 0),
            (None, [], 'Available options:', 0),
            ('my-tool', ['blah'], 'Unknown command "blah".\n'
                                  'Available options for my-tool:', 1),
        ]
    )
    def test_show_help(self, capsys, registry_name, args,
                       expected_prefix, expected_result):
        expected_text = self.EXPECTED_HELP.format(expected_prefix)

        self.registry.name = registry_name
        exit_code = self.registry.dispatch(['help'] + args)
        assert expected_result == exit_code
        out, err = capsys.readouterr()
        assert expected_text == out
        assert '' == err

    @pytest.mark.parametrize(
        'arg,expected_output',
        [
            ('arg-to-number',
                'arg-to-number\n'
                '\tConverts arg 1 to exit code.\n\n'),
            ('remember_args',
                'remember_args\n'
                '\n'
                'Extra long-winded, helpful info can go here.\n\n'),
        ]
    )
    def test_show_help_for_option(self, capsys, arg, expected_output):
        exit_code = self.registry.dispatch(['help', arg])
        assert 0 == exit_code
        out, err = capsys.readouterr()
        assert expected_output == out
        assert '' == err

    @pytest.mark.parametrize('registry_name', [
        ('my-tool'),
        (None),
    ])
    def test_no_args(self, capsys, fake_help, registry_name):
        self.registry.name = registry_name
        expected_output = 'Expected argument.\nHELP-GOES-HERE\n'

        exit_code = self.registry.dispatch([])
        assert 1 == exit_code
        out, err = capsys.readouterr()
        assert out == expected_output
        assert err == ''

    @pytest.mark.parametrize('registry_name,expected_output', [
        ('my-tool',
            'my-tool knows not of command "cow".\n\nHELP-GOES-HERE\n'),
        (None,
            'I know not of this command "cow".\n\nHELP-GOES-HERE\n'),
    ])
    def test_unknown_command(self, capsys, fake_help, registry_name,
                             expected_output):
        self.registry.name = registry_name
        exit_code = self.registry.dispatch(['cow'])
        assert 1 == exit_code
        out, err = capsys.readouterr()
        assert expected_output == out
        assert '' == err

    def test_passing_args(self, capsys):
        exit_code = self.registry.dispatch(['arg-to-number', '42'])
        assert 42 == exit_code
        assert_silence(capsys)

    @pytest.mark.parametrize('option', ['r', 'remember_args'])
    def test_using_aliases(self, capsys, option):
        exit_code = self.registry.dispatch([option, 'a', 'b', 'c'])
        assert ['a', 'b', 'c'] == self._remembered_args
        assert 0 == exit_code
        assert_silence(capsys)
