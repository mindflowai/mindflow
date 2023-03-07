from click.testing import CliRunner

import mindflow
from mindflow.cli.new_click_cli.cli_main import mindflow_cli


def test_version():
    runner = CliRunner()
    result = runner.invoke(mindflow_cli, ["version"])
    assert result.exit_code == 0
    assert result.output == f"{mindflow.__version__}\n"
