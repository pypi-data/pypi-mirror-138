import logging
import subprocess
import traceback

from subprocess import CalledProcessError


LOG = logging.getLogger(__name__)


def run_command(cmd: list[str]) -> str:
    """
    Returns the output from a command executed in the shell
    """
    curated_command = " ".join(cmd)
    LOG.info("Running command: %s", curated_command)
    try:
        output = subprocess.check_output(cmd, shell=False)
    except CalledProcessError as err:
        LOG.error("Error - {} ".format(traceback.format_exc()))
        raise err
    return output.decode("utf-8")
