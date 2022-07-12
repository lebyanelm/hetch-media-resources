# dependencies
import nanoid
import json
import os

from hetch_utilities.models.time_created import TimeCreatedModel

class DataModel:
    def __init__(self):
        self.key = nanoid.generate()
        self.time_created = TimeCreatedModel().__dict__
        self.last_modified = TimeCreatedModel().__dict__
        self._selected_database_ = "live" if os.environ.get("ENVIRONMENT") == "production" else "testing"

    def to_json(self) -> str:            
        return json.dumps(obj=self.__dict__)

    def to_dict(self) -> dict:
        if type(self) != dict:
            new_self_dict = {**self.__dict__}
        else:
            new_self_dict = {**self}

        if new_self_dict.get("_id"):
            new_self_dict["_id"] = str(new_self_dict["_id"])
        
        for parameter in new_self_dict:
            if type(new_self_dict[parameter]) == list:
                for index, item in enumerate(new_self_dict[parameter]):
                    new_self_dict[parameter][index] = str(item)

        return new_self_dict

    def get_schema():
        return { }

    @classmethod
    def verify_schema(cls, d: dict) -> list:
        schema = cls.get_schema()
        schema_keys = schema.keys()
        errors = []
        for schema_key in schema_keys:
            if d.get(schema_key):
                if type(d.get(schema_key)) != schema[schema_key]:
                    errors.append({ "error": f'Invalid data type "{type(d.get(schema_key)).__name__}" used in {schema_key}. "{schema[schema_key].__name__}" required instead.', "error_type": "invalid"})
            else:
                errors.append({ "error": f"Attribute {schema_key} of {schema[schema_key].__name__} required in request body.", "error_type": "undefined" })
        return errors