import gzip

from timebox.pipe import run_piped_commands


def test_piped_commands_rev(tmp_path):
    target_file = tmp_path / "output"
    commands = [["echo", "-n", "hello world"], ["rev"]]
    res = run_piped_commands(commands, {}, target_file)
    assert set(res) == {0}
    with open(target_file) as f:
        content = f.read()
    assert content == "hello world"[::-1]


def test_piped_commands_gzip(tmp_path):
    target_file = tmp_path / "output2"
    commands = [["echo", "-n", "hello world"], ["rev"], ["gzip"]]
    res = run_piped_commands(commands, {}, target_file)
    assert set(res) == {0}
    with gzip.open(target_file) as f:
        content = f.read()
    assert content == b"hello world"[::-1]
