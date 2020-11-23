import os
import sys

import pytest

ROOT = os.path.dirname(os.path.realpath(__file__))


if sys.version_info[0] >= 3:

    def from_root(path):
        # type: (str) -> str
        """Returns a path relative to the root directory."""
        if os.name == 'nt':
            path = path.replace('/', '\\')
        return os.path.join(ROOT, path)

    def get_code_text_from_in_readme_md(ext):
        result = []
        record = False
        with open(from_root('../README.md'), 'r') as f:
            for line in f.readlines():
                if '```' in line:
                    if '```{}'.format(ext) in line:
                        record = True
                    else:
                        record = False
                elif record:
                    result.append(line.strip())

        return '\n'.join(result)

    def get_ci_py_code_in_readme_md():
        return get_code_text_from_in_readme_md('py3')

    def read_ci_py():
        with open(from_root('../ci.py'), 'r') as file:
            return '\n'.join(line.strip() for line in file.readlines())

    def test_readme_python_snippet_is_correct():
        """
        The stand alone ci.py is run through pep8 and mypy, so it's best to
        make sure README.md matches it.
        """
        expected = read_ci_py()
        actual = get_ci_py_code_in_readme_md()
        assert expected == actual

    def get_ci_py_no_arg_output_in_readme_md():
        return get_code_text_from_in_readme_md('bash')

    def get_actual_ci_py_no_arg_output(monkeypatch, capsys):
        import ci
        monkeypatch.setattr(sys, 'argv', ['ci.py'])
        with pytest.raises(SystemExit):
            ci.main()
        out, err = capsys.readouterr()

        return '\n'.join(
            ['$ python ci.py'] + [line.strip() for line in out.split('\n')]
        )

    def test_readme_example_output_is_correct(monkeypatch, capsys):
        """
        This runs the actual ci.py script with no args to make sure the output
        matches what's shown in README.md.
        """
        expected = get_ci_py_no_arg_output_in_readme_md()
        actual = get_actual_ci_py_no_arg_output(monkeypatch, capsys)
        assert expected == actual
