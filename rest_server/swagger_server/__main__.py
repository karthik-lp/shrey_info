#!/usr/bin/env python3

import connexion
import yaml
import os
import logging


from flask_cors import CORS

from typing import Any, Dict
from pathlib import Path

from swagger_server.schema_generator import get_schemas
from swagger_server.schema_generator import Family

from connexion.resolver import RestyResolver
from connexion.apis import flask_utils

from swagger_server.src.config import BackendConfig
from swagger_server import encoder
from swagger_server.validator import Validator
from swagger_server.src.tools.converters import (
    NumberConverter,
    IntegerConverter,
)
from swagger_server.src.tools.logging import (
    get_file_handler,
    get_stream_handler,
)

schema_list = [Family]


def access_recursive(dictionary, keys):
    """
    the two things are/should be equivalent:
    dictionary["k1"]["k2"]["k3"] == access_recursive(dictionary, "k1/k2/k3")

    special cases:
    - access_recursive(dictionary, []) returns dictionary
    - access_recursive(dictionary, "////k1") returns dictionary["k1"]
    """
    if keys == []:
        return dictionary
    keys = keys[0].split("/")
    data = dictionary
    for key in keys:
        if key == "":
            continue
        data = data[key]
    return data


def get_bundled_specs(main_file: Path) -> Dict[str, Any]:
    spec = {}
    with open(main_file) as f:
        spec = yaml.load(f, Loader=yaml.SafeLoader)
    if spec["components"]["schemas"] is not None:
        raise AssertionError(
            "components/schemas of swagger.yaml should be empty and dynamically created. It will be overwritten."
        )
    spec["components"]["schemas"] = get_schemas(schema_list)
    for endpoint, specification in spec["paths"].items():
        if len(specification) != 1 or "$ref" not in specification:
            # as soon as we have more than one child key we skip that endpoint
            # if "$ref" is not that one child we don't need to resolve anything
            continue
        if not specification["$ref"].startswith("./"):
            # the reference does not point to a file in the directory or its subfolders
            continue
        split = specification["$ref"].split("#")
        if len(split) > 2:
            raise RuntimeError(
                f"Cannot resolve \"{specification['$ref']}\", since it contains more than one \"#\""
            )
        ref_path = main_file.parent / split[0]

        with open(ref_path) as f:
            spec["paths"][endpoint] = access_recursive(
                yaml.load(f, Loader=yaml.SafeLoader), split[1:]
            )

    return spec


def main():

    # Setup Connexion App
    flask_utils.PATH_PARAMETER_CONVERTERS["integer"] = "integer"
    flask_utils.PATH_PARAMETER_CONVERTERS["number"] = "number"

    spec_dir = "./swagger/"
    specfile_name = "swagger.yaml"
    options = {
        "swagger_ui_config": {
            "tagsSorter": "alpha",
            "operationsSorter": "alpha",
            "displayRequestDuration": True,
            "swagger_ui": True,
        },
        "swagger_url": "/",
    }
    app = connexion.FlaskApp(
        "swagger_server", specification_dir=spec_dir, options=options
    )
    app.app.url_map.converters["number"] = NumberConverter
    app.app.url_map.converters["integer"] = IntegerConverter
    CORS(app.app)
    app.app.json_encoder = encoder.JSONEncoder

    api_spec = get_bundled_specs(
        Path(os.path.join(app.get_root_path(), spec_dir, specfile_name))
    )
    app.app.config["validator"] = Validator(api_spec)
    app.add_api(
        api_spec,
        resolver=RestyResolver("end_points"),
        pythonic_params=True,
        base_path=BackendConfig.server_name,
    )

    # Setup logging
    fileHandler = get_file_handler(log_level=logging.INFO)
    streamHandler = get_stream_handler(log_level=BackendConfig.log_level)
    app.app.logger.addHandler(streamHandler)
    app.app.logger.addHandler(fileHandler)
    logging.getLogger("werkzeug").addHandler(
        get_stream_handler(log_level=logging.INFO, format=None)
    )

    app.run(port=BackendConfig.port, debug=BackendConfig.debug_mode_on)


if __name__ == "__main__":
    main()
