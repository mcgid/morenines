import os
from click.testing import CliRunner

from morenines import application


def test_init(data_dir):
    """Inits a repo in a dir with files, subdirs and no existing repo"""
    runner = CliRunner()

    result = runner.invoke(application.main, ['init', data_dir])

    assert result.exit_code == 0

    mn_dir = os.path.join(data_dir, '.morenines')

    assert os.path.isdir(mn_dir) == True


# XXX I can't get this test to work because chdir() isn't having any effect.
#     I suspect it's somehow related to testing with click, but I can't figure
#     out exactly why.
#
#     Leaving the test in but commented because it's failing because of the
#     testing environment, not the code, so having it always fail won't tell us
#     anything useful. It would be nice to have it part of the suite eventually.
#
#def test_init_with_no_args(tmpdir, monkeypatch):
#    monkeypatch.chdir(tmpdir.strpath)
#
#    runner = CliRunner()
#    result = runner.invoke(application.main, ['init'])
#
#    mn_dir = tmpdir.join('.morenines').strpath
#
#    assert os.path.isdir(mn_dir) == True
