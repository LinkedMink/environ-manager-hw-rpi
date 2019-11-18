from decimal import Decimal
import json

class JsonDecimalEncoder(json.JSONEncoder):
    def iterencode(self, o, _one_shot = ...):
        if isinstance(o, Decimal):
            # wanted a simple yield str(o) in the next line,
            # but that would mean a yield on the line with super(...),
            # which wouldn't work (see my comment below), so...
            return (str(o) for o in [o])
        return super(JsonDecimalEncoder, self).iterencode(o, _one_shot)