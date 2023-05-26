import os
import sys
import time
import webbrowser
from subprocess import Popen, PIPE, STDOUT


def main():
    # Getting path to python executable (full path of deployed python on Windows)
    executable = sys.executable

    path_to_main = os.path.join(os.path.dirname(__file__), "vis.py")

    # Force the opening (does not open automatically) of the browser tab before streamlit to let
    # the streamlit server start.

    webbrowser.open("http://localhost:8526")

    # Running streamlit server in a subprocess and writing to log file
    proc = Popen(
        [
            executable,
            "-m",
            "streamlit",
            "run",
            path_to_main,
            # The following option appears to be necessary to correctly start the streamlit server,
            # but it should start without it. More investigations should be carried out.
            "--server.headless=true",
            "--server.maxUploadSize=3000",
            "--global.developmentMode=false",
            "--client.showErrorDetails=false",
            "--server.port=8526",
            "--theme.base=light",
        ],
        stdin=PIPE,
        stdout=PIPE,
        stderr=STDOUT,
        text=True,
        env={'APP_PID': str(os.getpid()), **os.environ}
    )
    proc.stdin.close()

    while True:
        s = proc.stdout.read()
        if not s:
            break
        print(s, end="")

    proc.wait()


if __name__ == "__main__":
    # os.chdir(os.path.expanduser("~"))
    main()
