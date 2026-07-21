import paramiko
import shlex
from pathlib import Path
import posixpath
from cronboard.services.cron_logging.cron_wrapper import get_remote_home
from cronboard.config import LOG_DIR, LOG_REL_PATH
import shutil


def get_log_files(identificator: str, ssh: paramiko.SSHClient | None = None) -> dict:
    if ssh is None:
        log_dir: Path = LOG_DIR / identificator
        if not log_dir.exists():
            return {}
        return {
            p.stem: str(p)
            for p in sorted(
                log_dir.glob(f"{identificator}_*.log"), key=lambda p: p.stem
            )
        }
    else:
        home: str | None = get_remote_home(ssh)
        if not home:
            return {}
        log_dir: str = posixpath.join(home, LOG_REL_PATH, identificator)

        cmd = f"ls {log_dir} 2>/dev/null"
        _, stdout, stderr = ssh.exec_command(cmd)
        files: str = stdout.read().decode().splitlines()
        errors: str = stderr.read().decode().strip()

        if errors:
            print(f"Error: {errors}")
            return {}

        result: dict = {}
        for file in sorted(files):
            if file.startswith(f"{identificator}_") and file.endswith(".log"):
                stem: str = file[:-4]  # remove ".log"
                full_path: str = posixpath.join(log_dir, file)
                result[stem] = full_path

        return result


def read_log_file(log_path: str, ssh: paramiko.SSHClient | None = None) -> list:
    if ssh is None:
        log_file: Path = Path(log_path)
        if not log_file.exists():
            return []
        with open(log_file, "r") as f:
            return f.readlines()
    else:
        safe_path: str = shlex.quote(log_path)

        _, stdout, stderr = ssh.exec_command(f"test -f {safe_path} && cat {safe_path}")
        output: str = stdout.read().decode()
        error: str = stderr.read().decode()

        if not output or error:
            if error:
                print(f"Error: {error}")
            return []

        return output.splitlines(keepends=True)


def delete_logs_for_identificator(
    identificator: str, ssh: paramiko.SSHClient | None = None
) -> None:
    """
    Deletes all log files associated with the given identificator.
    """
    if ssh is None:
        path: Path = LOG_DIR / identificator
        shutil.rmtree(path, ignore_errors=True)
    else:
        home: str | None = get_remote_home(ssh)

        if not home:
            return

        path: str = posixpath.join(home, LOG_REL_PATH, identificator)
        ssh.exec_command(f"rm -rf -- {shlex.quote(path)}")
