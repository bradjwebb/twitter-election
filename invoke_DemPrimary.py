"""check and start child process"""
import subprocess
import datetime
import time


def invoke(command, script):  # command ex: 'python', script ex: 'test.py'
    invoke = subprocess.Popen([command, script])
    text = invoke.communicate()[0]
    run_check = invoke.returncode
    if run_check == 1:
        status = True
    else:
        status = False
    return status

today = str(datetime.datetime.now())
end = '2016-03-02'  # day after super tuesday primaries

while today < end:
    try:
        invoke('python', 'streaming.py')
    except Exception:
        pass
    finally:
        time.sleep(5)
