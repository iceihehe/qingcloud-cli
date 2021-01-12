import json
import unittest

from click.testing import CliRunner
from unittest.mock import MagicMock, patch

from command import cli
from sdk import QingCloudApi
from util import load_config, _CONFIG_FILE, _AUTH_KEY, _AUTH_SECRET


class TestCommand(unittest.TestCase):

    def setUp(self):
        self.runner = CliRunner()

    def tearDown(self):
        pass

    def test_config(self):
        runner = self.runner
        with runner.isolated_filesystem():
            runner.invoke(cli, ["config", "a", "b"])
            with open(_CONFIG_FILE, "r") as f:
                config = load_config()
                assert _AUTH_KEY in config
                assert config[_AUTH_KEY] == "a"
                assert _AUTH_SECRET in config
                assert config[_AUTH_SECRET] == "b"

    def test_describe_instances_mock(self):
        runner = self.runner
        with patch.object(QingCloudApi, "describe_instances", MagicMock(return_value="success")):
            result = runner.invoke(cli, ["describe-instances", "pek3b"])
            assert result.output.split()[-1] == "success"
            result = runner.invoke(cli, ["describe-instances"])
            assert result.exception

    def test_describe_instances(self):
        runner = self.runner
        result = runner.invoke(cli, ["describe-instances", "pek3b"])
        result_json = json.loads(result.output.strip())
        assert result_json["ret_code"] == 0

    def test_run_instances_mock(self):
        runner = self.runner
        with patch.object(QingCloudApi, "run_instances", MagicMock(return_value="success")):
            result = runner.invoke(cli, ["run-instances", "imageid", "passwd", "pek3b", "--login-passwd=123456",
                                         "--instance-type=c1m1"])
            assert result.output.split()[-1] == "success"
            result = runner.invoke(cli, ["run-instances", "imageid", "passwd", "pek3b", "--login-passwd=123456"])
            assert result.output.split()[-1] == "缺少必要CPU内存参数"
            result = runner.invoke(cli, ["run-instances", "imageid", "passwd", "pek3b"])
            assert result.output.strip() == "缺失login-passwd"
            result = runner.invoke(cli, ["run-instances", "imageid", "keypair", "pek3b"])
            assert result.output.strip() == "缺失login-keypair"

    def test_run_instances(self):
        runner = self.runner
        result = runner.invoke(cli, ["run-instances", "debian106x64", "passwd", "pek3b", "--login-passwd=yERxtw49",
                                     "--instance-type=c1m1"])
        result_json = json.loads(result.output.strip())
        assert result_json["ret_code"] == 0

    def test_terminate_instances_mock(self):
        runner = self.runner
        with patch.object(QingCloudApi, "terminate_instances", MagicMock(return_value="success")):
            result = runner.invoke(cli, ["terminate-instances", "pek3b", "--instance-id=instanceid"])
            assert result.output.split()[-1] == "success"
            result = runner.invoke(cli, ["terminate-instances", "pek3b"])
            assert result.exception

    def test_terminate_instances(self):
        runner = self.runner
        result = runner.invoke(cli, ["terminate-instances", "pek3b", "--instance-id=fakeid"])
        result_json = json.loads(result.output.strip())
        assert result_json["ret_code"] == 2100


if __name__ == '__main__':
    unittest.main()
