import logging
import os
import sys
from flask import has_request_context, request
from swagger_server.src.config import BackendConfig


class RequestFormatter(logging.Formatter):
    def format(self, record):
        if has_request_context():
            record.url = request.url
            record.method = request.method
        else:
            record.url = None
            record.method = None
        return super().format(record)


log_format = (
    "[%(asctime)s] - %(name)s - %(levelname)s Requested %(url)s %(method)s\n"
    + " Msg: %(message)s"
)


def get_file_handler(
    filename="rest_api.log", log_level=logging.WARN, format=log_format
):
    handler = logging.FileHandler(os.path.join(BackendConfig.base_data_base_path, filename))
    handler.setLevel(log_level)
    if format is None:
        pass
    else:
        handler.setFormatter(RequestFormatter(log_format))
    return handler


def get_stream_handler(ostream=sys.stderr, log_level=logging.WARN, format=log_format):
    handler = logging.StreamHandler(ostream)
    handler.setLevel(log_level)
    if format is None:
        pass
    else:
        handler.setFormatter(RequestFormatter(log_format))
    return handler
