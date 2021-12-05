import jsonschema


class Validator(object):
    def __init__(self, openapi_spec):
        self.spec = openapi_spec

    def __call__(self, instance, schema):
        return self.validate(instance, schema)

    def validate(self, instance, schema):
        return jsonschema.validate(instance, self.spec["components"]["schemas"][schema])
