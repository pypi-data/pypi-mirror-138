from io import StringIO
from typing import Union
from os import PathLike
import unittest
from genevieve import generate_pwsh, generate_sh, parse_yaml, main
from pathlib import Path


class TestGenevieve(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.yaml_path = Path(__file__).parent / "test.yaml"
        cls.parsed_yaml = parse_yaml(cls.yaml_path)
        cls.expected_bash = Path(__file__).parent / "xout_bash.txt"
        cls.expected_pwsh = Path(__file__).parent / "xout_pwsh.txt"
        cls.stream = StringIO()

    def read_expected(self, expected_path: Union[str, PathLike]) -> str:
        with open(expected_path, "r") as f:
            expected = f.read()
        return expected

    def write_to_stream(self, string: str):
        self.stream.write(string)

    def test_bash_output(self):
        out = generate_sh(self.parsed_yaml, "variables")
        expected = self.read_expected(self.expected_bash)
        self.assertEqual(out, expected)

    def test_powershell_output(self):
        out = generate_pwsh(self.parsed_yaml, "variables")
        expected = self.read_expected(self.expected_pwsh)
        self.assertEqual(out, expected)

    def test_main_interface(self):
        import sys
        sys.argv = sys.argv[1:]
        sys.argv += ["-f", str(self.yaml_path), "--debug"]
        expected = \
            self.read_expected(self.expected_bash) + \
            self.read_expected(self.expected_pwsh)
        try:
            main(self.write_to_stream)()
        except SystemExit as e:
            self.assertIn(0, e.args)
        stdout_capture = self.stream.getvalue()
        self.assertEqual(stdout_capture, expected)


if __name__ == "__main__":
    unittest.main()
