import os
import re
import shlex
import subprocess

from automcp.logger import setup_logging

logger = setup_logging(__name__)

def run_shell(command):
    '''
    Run shell command and get logs and statuscode in output.
    '''
    logger.debug("Running command: %s\n", command)
    logs = ""
    command = shlex.split(command)
    process = subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
    )
    if process.stdout is None:
        raise subprocess.CalledProcessError(
            returncode=process.returncode,
            cmd=command,
            output=logs,
            stderr=logs,
        )
    for line in process.stdout:
        logs += line
    process.wait()
    logger.debug("Run Status: %d", process.returncode)
    return logs


def safe_name(name: str) -> str:
    return re.sub(r'[^a-zA-Z0-9]', '_', name)
