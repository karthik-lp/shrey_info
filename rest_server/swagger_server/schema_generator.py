from swagger_server.schemas.family import Family
import yaml
from pydantic import schema


def get_schemas(schema_list=None):

    if schema_list is None:
        schema_list = [
            Family
        ]

    s = schema.schema(
        schema_list,
        ref_prefix="#/components/schemas/",
    )
    return s["definitions"]


if __name__ == "__main__":
    print(yaml.dump(get_schemas))
