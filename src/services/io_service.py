"""Low level IO operations involving (de)serialisation and file read/write"""
import json
from lib.core import (
    DataFormat,
    SerialiserInterface,
    DeserialiserInterface)


# Serialiser
class Serialiser():
    """Factory for format appropriate serialiser objects"""
    def __init__(self, data_format: DataFormat) -> None:
        self._serialiser = self._get_serialiser(data_format)

    def _get_serialiser(self, data_format: DataFormat):
        serialisers = {'json': JSONSerialiser}
        return serialisers[data_format.value]

    def serialise(self, object_to_serialise: object):
        """Returns serialised strings in specified formats using factory created serialiser"""
        return self._serialiser.serialise(object_to_serialise)


# Deserialiser
class Deserialiser():
    """Factory for format appropriate deserialiser objects"""
    def __init__(self, data_format: DataFormat) -> None:
        self._deserialser = self._get_deserialiser(data_format)

    def _get_deserialiser(self, data_format: DataFormat):
        deserialisers = {'json': JSONDeserialiser}
        return deserialisers[data_format.value]

    def deserialise(self, string_to_deserialise: str):
        """Returns deserialised from formatted strings using factory created serialiser"""
        return self._deserialser.deserialise(string_to_deserialise)


# DataFormat and the Serialiser/Deserialiser pairings should be in the same file.
# JSON Serializer
class JSONSerialiser(SerialiserInterface):
    """Serialiser for objects in JSON format"""
    @staticmethod
    def serialise(object_to_serialise):
        """Returns a JSON serialised string representing an input object"""
        return json.dumps(object_to_serialise)


# JSON Deserializer
# NEEDS A TEST
class JSONDeserialiser(DeserialiserInterface):
    """Deserialiser for objects in JSON format"""
    @staticmethod
    def deserialise(string_to_deserialise):
        """Returns a JSON deserialised object from an input string, or an empty dictionary"""
        if string_to_deserialise:
            return json.loads(string_to_deserialise)
        return {}


class IOService:
    """Carries out low level data IO operations"""
    def __init__(
            self,
            data_format: DataFormat = None,
            serialiser: SerialiserInterface = None,
            deserialiser: DeserialiserInterface = None) -> None:
        self._data_format = None
        self._serialiser = None
        self._deserialiser = None
        if data_format is not None:
            self._data_format = data_format
        if serialiser is not None:
            self._serialiser = serialiser
        if deserialiser is not None:
            self._deserialiser = deserialiser

    @property
    def data_format(self):
        """Property containing a registered DataFormat value"""
        return self._data_format

    def read(self, filename):
        """Returns data from the specified UTF-8 file."""
        try:
            with open(filename, "r", encoding='UTF-8') as file_ref:
                data = file_ref.read()
            return data
        except FileNotFoundError:
            with open(filename, "w", encoding='UTF-8') as file_ref:
                file_ref.write("")
            return None

    def store(self, filename, data):
        """Stores input data in a specified UTF-8 file."""
        with open(filename, "w", encoding='UTF-8') as file_ref:
            file_ref.write(data)

    def serialise_obj_to_string(self, obj: object):
        """Converts an input object into a serialised string in the specified data_format"""
        if self._serialiser:
            return self._serialiser.serialise(obj)
        return Serialiser(self._data_format).serialise(obj)

    def deserialise_string_to_obj(self, string: str):
        """Converts an input string in the specified data_format into a deserialised object"""
        if self._deserialiser:
            return self._deserialiser.deserialise(string)
        return Deserialiser(self._data_format).deserialise(string)

    def serialise_and_store(self, obj: object, filename: str):
        """Serialise an input object and then store it in a file."""
        serialised_string = self.serialise_obj_to_string(obj)
        self.store(filename + ".data", serialised_string)

    def deserialise_stored(self, filename: str):
        """Read from a specified file and return the deserialised contents."""
        serialised_string = self.read(filename + ".data")
        return self.deserialise_string_to_obj(serialised_string)
