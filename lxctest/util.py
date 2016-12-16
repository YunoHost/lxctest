import subprocess


def run(command, shell = False):
    """
    Wrapper around subprocess to execute commands.
    """
    try:
        if (not shell):
            child = subprocess.Popen(command,
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE)
        else :
            child = subprocess.Popen(command,
                                     shell=True,
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE)

        (stdout, stderr) = child.communicate()
        return_code = child.returncode
    except OSError as e:
        return ('', 'Error: Command failed', e.errno)

    return stdout.decode('utf-8'), stderr.decode('utf-8'), return_code
