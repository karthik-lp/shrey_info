import argparse
import logging
import os


class BackendConfig(object):
    default_path = os.path.join(
        os.environ.get("XDG_CONFIG_HOME", os.path.join(os.environ["HOME"], ".config/personal_project", )),
        "data_base",
    )

    parser = argparse.ArgumentParser(description="Configure Backend settings")

    parser.add_argument(
        "-f",
        "--data_folder",
        dest="base_data_base_path",
        help="Open specified data_base base path",
        default=default_path,
    )
    parser.add_argument(
        "-l",
        "--log",
        dest="log_level",
        help="Set log level",
        type=str,
        choices=["critical", "error", "warn", "info", "debug"],
        default="warn",
    )
    parser.add_argument(
        "-d",
        "--debug_mode_on",
        dest="debug_mode_on",
        help="Activate the debug mode if set on True",
        default=False,
    )
    parser.add_argument(
        "-p",
        "--port",
        dest="port",
        help="Set the rest_server port",
        default=8080,
    )
    parser.add_argument(
        "-s",
        "--server_name",
        dest="server_name",
        help="Set the server name",
        default="/v1",
    )

    args = parser.parse_args()
    base_data_base_path = args.base_data_base_path
    debug_mode_on = args.debug_mode_on
    port = args.port
    server_name = args.server_name
    if args.log_level == "critical":
        log_level = logging.CRITICAL
    elif args.log_level == "error":
        log_level = logging.ERROR
    elif args.log_level == "info":
        log_level = logging.INFO
    elif args.log_level == "debug":
        log_level = logging.DEBUG
    else:
        log_level = logging.WARN
