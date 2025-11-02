import json
from collections import defaultdict
from copy import deepcopy

class ProtocolQmkSettings:

    def __init__(self, settings):
        self.settings_defs = deepcopy(ProtocolQmkSettings._settings_defs)
        self.qsid_fields = deepcopy(ProtocolQmkSettings._qsid_fields)
        self.kbd_settings_set = set()
        self.qmk_settings_set = set(self.qsid_fields.keys())
        for tab in settings:
            self.settings_defs["tabs"].append(tab)
            for field in tab["fields"]:
                self.qsid_fields[field["qsid"]].append(field)
                self.kbd_settings_set.add(field["qsid"])

    @classmethod
    def initialize(cls, appctx):
        cls._qsid_fields = defaultdict(list)
        with open(appctx.get_resource("qmk_settings.json"), "r") as inf:
            cls._settings_defs = json.load(inf)
        for tab in cls._settings_defs["tabs"]:
            for field in tab["fields"]:
                cls._qsid_fields[field["qsid"]].append(field)

    def is_qsid_supported(self, qsid):
        """ Return whether this qsid is supported by the settings editor """
        return qsid in self.qsid_fields

    def qsid_serialize(self, qsid, data):
        """ Serialize from internal representation into binary that can be sent to the firmware """
        fields = self.qsid_fields[qsid]
        width = fields[0].get("width", 1)
        if fields[0]["type"] == "boolean":
            assert isinstance(data, int)
            return data.to_bytes(width, byteorder="little")
        elif fields[0]["type"] == "integer":
            assert isinstance(data, int)
            assert len(fields) == 1
            return data.to_bytes(width, byteorder="little")
        elif fields[0]["type"] == "select":
            assert isinstance(data, int)
            assert len(fields) == 1
            return data.to_bytes(width, byteorder="little")
        elif fields[0]["type"] == "string":
            assert isinstance(data, str)
            assert len(fields) == 1
            return data.strip('\x00').encode('utf-8')[:width]

    def qsid_deserialize(self, qsid, data):
        """ Deserialize from binary received from firmware into internal representation """
        fields = self.qsid_fields[qsid]
        width = fields[0].get("width", 1)

        if fields[0]["type"] == "boolean":
            return int.from_bytes(data[0:width], byteorder="little")
        elif fields[0]["type"] == "integer":
            assert len(fields) == 1
            return int.from_bytes(data[0:width], byteorder="little")
        elif fields[0]["type"] == "select":
            assert len(fields) == 1
            return int.from_bytes(data[0:width], byteorder="little")
        elif fields[0]["type"] == "string":
            assert len(fields) == 1
            return data[0:width].decode('utf-8').strip('\x00')
        else:
            raise RuntimeError("unsupported field")
