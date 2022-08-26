import subprocess
from threading import Thread
from typing import Callable

from testcontainers.compose import DockerCompose
from test.utils.common_utils import get_project_root_str


def get_web_app_host():
    return "127.0.0.1"


class TodoAppDockerCompose(DockerCompose):
    def __init__(self):
        super().__init__(get_project_root_str())

    def get_web_app_port(self):
        return self.get_service_port("todo-web-app", 80)

    def follow_logs(self, new_line_callback: Callable[[str], None]):
        logs_cmd = self.docker_compose_command() + ["logs", "-f"]
        process = subprocess.Popen(
            logs_cmd,
            cwd=self.filepath,
            stdout=subprocess.PIPE,
        )

        def log_runnable(p):
            while True:
                line = p.stdout.readline()
                if line == b'' is not None:
                    break

                print_line = line.decode('utf-8').replace('\n', '')
                new_line_callback(print_line)

        log_thread = Thread(target=log_runnable, args=[process])
        log_thread.daemon = True
        log_thread.start()


