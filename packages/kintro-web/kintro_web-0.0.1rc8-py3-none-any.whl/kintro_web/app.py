import json
from logging.config import dictConfig
import os
import subprocess
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Dict,
    List,
    Optional,
    Tuple,
    Union,
)

from flask import Flask
from kintro import kintro


if TYPE_CHECKING:
    BytesProcess = subprocess.Popen[bytes]
else:
    BytesProcess = subprocess.Popen

dictConfig(
    {
        "version": 1,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
            }
        },
        "handlers": {"wsgi": {"class": "logging.StreamHandler", "formatter": "default"}},
        "root": {"level": "DEBUG", "handlers": ["wsgi"]},
    }
)


def get_env_or_abort(env: str):
    val = os.getenv(env, None)
    if val is None:
        raise ValueError(f"{env} must be set")
    return val


def stream_stdout_to_log(
    cmd: Union[str, List[str]], log_fn: Callable[[str], None], process_kwargs: Optional[Dict[str, Any]] = None
) -> Tuple[BytesProcess, List[str]]:
    all_output = []
    process_kwargs = {} if process_kwargs is None else process_kwargs

    with subprocess.Popen(cmd, **process_kwargs, stdout=subprocess.PIPE) as process:
        assert process.stdout is not None
        for line in iter(process.stdout.readline, b""):
            decoded_line = line.decode("utf-8")
            log_fn(decoded_line)
            all_output.append(decoded_line)

    return process, all_output


def create_app(cfg=None):
    plex_server_url = get_env_or_abort("KINTRO_PLEX_URL")
    plex_server_token = get_env_or_abort("KINTRO_PLEX_TOKEN")
    kintro_log_level = get_env_or_abort("KINTRO_LOG_LEVEL")
    tv_path = get_env_or_abort("KINTRO_TV_PATH")
    replace_path = get_env_or_abort("KINTRO_REPLACE_PATH")

    application = Flask(__name__)

    @application.route("/episode/<series>/<int:season>/<int:episode>", methods=["POST"])
    def episode(series: str, season: int, episode: int):
        kintro_cmd = [
            "kintro",
            "--log-level",
            kintro_log_level,
            "server",
            "--url",
            plex_server_url,
            "--token",
            plex_server_token,
            "sync",
            "--find-path",
            tv_path,
            "--replace-path",
            replace_path,
            "--libtype",
            "episode",
            "--filter-json",
            json.dumps(
                {
                    "and": [
                        {
                            "show.title==": series,
                        },
                        {
                            "season.index=": season,
                        },
                        {
                            "episode.index=": episode,
                        },
                    ],
                },
            ),
            "--max-workers",
            "1",
            "--worker-batch-size",
            "1",
            "--analyze-if-intro-missing",
        ]

        kintro_process, all_output = stream_stdout_to_log(kintro_cmd, application.logger.info)

        return {
            "exit_code": kintro_process.returncode,
            "output": all_output,
        }

    return application
