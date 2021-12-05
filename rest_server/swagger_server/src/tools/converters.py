from werkzeug.routing import BaseConverter


class NumberConverter(BaseConverter):
    """Flask converter for OpenAPI number type"""

    regex = r"[+-]?[0-9]+.*(\.[0-9]*)?"

    def to_python(self, value):
        return float(value)


class IntegerConverter(BaseConverter):
    """Flask converter for OpenAPI integer type"""

    regex = r"[+-]?[0-9]+"

    def to_python(self, value):
        return int(value)
