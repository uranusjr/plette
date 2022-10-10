from .base import DataView, DataViewMapping, DataViewSequence
from .hashes import Hash
from .packages import Package
from .scripts import Script
from .sources import Source


class PackageCollection(DataViewMapping):
    item_class = Package


class ScriptCollection(DataViewMapping):
    item_class = Script


class SourceCollection(DataViewSequence):
    item_class = Source


class Requires(DataView):
    """Representation of the `[requires]` section in a Pipfile.
    """
    __SCHEMA__ = {
        "python_version": {
            "type": "string",
            # matches 3.10 and 2.7 and 4.1
            "regex": r"[2-4]\.[0-9]{1,2}",
        },
        "python_full_version": {
            "type": "string",
            # matches 3.10.10 and 2.7.1p1 and 4.1.9 
            "regex": r"[2-4]\.[0-9]{1,2}\.[0-9p]{1,3}",
        },
    }

    @property
    def python_version(self):
        try:
            return self._data["python_version"]
        except KeyError:
            raise AttributeError("python_version")

    @property
    def python_full_version(self):
        try:
            return self._data["python_full_version"]
        except KeyError:
            raise AttributeError("python_full_version")


META_SECTIONS = {
    "hash": Hash,
    "requires": Requires,
    "sources": SourceCollection,
}


class Meta(DataView):
    """Representation of the `_meta` section in a Pipfile.lock.
    """
    __SCHEMA__ = {
        "hash": {"type": "dict", "required": True},
        "pipfile-spec": {"type": "integer", "required": True, "min": 0},
        "requires": {"type": "dict", "required": True},
        "sources": {"type": "list", "required": True},
    }

    @classmethod
    def validate(cls, data):
        super(Meta, cls).validate(data)
        for key, klass in META_SECTIONS.items():
            klass.validate(data[key])

    def __getitem__(self, key):
        value = super(Meta, self).__getitem__(key)
        try:
            return META_SECTIONS[key](value)
        except KeyError:
            return value

    def __setitem__(self, key, value):
        if isinstance(value, DataView):
            self._data[key] = value._data
        else:
            self._data[key] = value

    @property
    def hash_(self):
        return self["hash"]

    @hash_.setter
    def hash_(self, value):
        self["hash"] = value

    @property
    def hash(self):
        return self["hash"]

    @hash.setter
    def hash(self, value):
        self["hash"] = value

    @property
    def pipfile_spec(self):
        return self["pipfile-spec"]

    @pipfile_spec.setter
    def pipfile_spec(self, value):
        self["pipfile-spec"] = value

    @property
    def requires(self):
        return self["requires"]

    @requires.setter
    def requires(self, value):
        self["requires"] = value

    @property
    def sources(self):
        return self["sources"]

    @sources.setter
    def sources(self, value):
        self["sources"] = value
