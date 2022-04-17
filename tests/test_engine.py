import tarfile
from pathlib import Path

from timebox.config import Backup, Config, PostOp
from timebox.engine import Engine
from timebox.input_providers import FolderInputProvider
from timebox.output_providers import FolderOutputProvider
from timebox.rotation_providers.simple_rotation import SimpleRotation


def test_engine_with_post_op(tmp_path):
    input = FolderInputProvider(
        type="folder",
        path=Path("tests/data"),
        compression=None,
    )  # type: ignore
    output = FolderOutputProvider(type="folder", path=tmp_path)
    rotation = SimpleRotation(type="simple", days=2)
    backup = Backup(
        name="test_post_op",
        input=input,
        outputs=[output],
        rotation=rotation,
        post_ops=["compress"],
    )
    config = Config(post_ops={"compress": PostOp(command=["xz"], extension="xz")})  # type: ignore
    engine = Engine(backups=[backup], config=config)
    engine.perform_backups()
    items = output.ls("test_post_op")
    assert items[0].extensions == ["tar", "xz"]

    tar = tarfile.open(tmp_path / items[0].filename, "r|xz")
    assert len(tar.getmembers()) > 0
