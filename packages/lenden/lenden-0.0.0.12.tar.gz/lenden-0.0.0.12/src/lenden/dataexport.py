from enum import Enum
import json


def compare(s, t):
    """Compare two list without check the index

    Args:
        s (list): List A
        t (list): List B

    Returns:
        [boolean]: True if the two list have the same values.
    """
    t = list(t)   # make a mutable copy
    try:
        for elem in s:
            t.remove(elem)
    except ValueError:
        return False
    return not t


class DisplayType(str, Enum):
    """Display Enum Type
    """
    grid = "grid"
    """Display Type grid.
    """
    row = "row"
    """Display Type row.
    """

class ResultType(str, Enum):
    """Result Enum Type
    """
    str = "str"
    """Result Type string.
    """
    int = "int"
    """Result Type integer.
    """
    float = "float"
    """Result Type float.
    """
    percent = "percent"
    """Result Type percent without the % simbol.
    """
    image = "image"
    """Result Type image.
    """
    images = "images"
    """Result Type array of images.
    """
    numberarray = "numberarray"
    """Result Type array number.
    """

class ResultSizeType(str, Enum):
    """Result Size Type.
    """
    normal = "normal"
    """Result Type normal.
    """
    wide = "wide"
    """Result Type wide.
    """
    big = "big"
    """Result Type big.
    """


class ComplexEncoder(json.JSONEncoder):
    """Complex Encoder Json

    Args:
        json ([type]): Object to  convert to JSON
    """
    def default(self, obj):
        if hasattr(obj, '__toJSON'):
            return obj.__toJSON()
        else:
            return json.JSONEncoder.default(self, obj)


class DataResults(object):
    def __init__(self, Description, Help, Type, Path, Size, Format):
        self.Description = Description
        self.Help = Help
        self.Type = Type
        self.Path = Path
        self.Size = Size
        self.Format = Format

    def __eq__(self, obj):
        return self.Description == obj.Description and self.Help == obj.Help \
            and self.Type == obj.Type and self.Path == obj.Path \
            and self.Size == obj.Size and self.Format == obj.Format

    def __toJSON(obj):
        return dict(Description=obj.Description, Help=obj.Help, Type=obj.Type, Path=obj.Path, Size=obj.Size, Format=obj.Format)

    def getJSON(self):
        return json.dumps(DataResults.__toJSON(self), cls=ComplexEncoder)

    def __fromJSON(dct):
        return DataResults(dct["Description"], dct["Help"], dct["Type"], dct["Path"], dct["Size"], dct["Format"])

    def fromJSON(strjson):
        return json.loads(strjson, object_hook=DataResults.__fromJSON)


class DataLog(object):
    def __init__(self, Description, Path):
        self.Description = Description
        self.Path = Path

    def __eq__(self, obj):
        r_local = self.Path
        r_obj = obj.Path
        return self.Description == obj.Description and compare(r_local, r_obj)

    def __toJSON(obj):
        return dict(Description=obj.Description, Path=obj.Path)

    def getJSON(self):
        return json.dumps(DataLog.__toJSON(self), cls=ComplexEncoder)

    def __fromJSON(dct):
        return DataLog(dct["Description"], dct["Path"])

    def fromJSON(strjson):
        return json.loads(strjson, object_hook=DataLog.__fromJSON)


class DataExport(object):
    def __init__(self, Version, HasError, DisplayType, Results, Logs=DataLog("", [])):
        """DataExport

        Args:
            Version ([float]): Number Version of the Model.
            HasError ([number]): 0  for Error and 1 for Not error
            DisplayType ([DisplayType]): Display Type
            Results ([list of DataResults]): List of DataResults
        """
        self.Version = Version
        self.HasError = HasError
        self.DisplayType = DisplayType
        if Results is None:
            Results = []
        self.Results = Results
        if Logs is None:
            Logs = DataLog("", [])
        if Logs.Path is None:
            Logs.Path = []
        self.Logs = Logs

    def __eq__(self, obj):
        r_local = self.Results
        r_obj = obj.Results
        return self.Version == obj.Version and self.HasError == obj.HasError \
            and self.DisplayType == obj.DisplayType and compare(r_local, r_obj) and self.Logs == obj.Logs

    def __toJSON(obj):
        resultsorig = obj.Results
        results_json = list(map(lambda x: x.getJSON(), resultsorig))
        if obj.Logs is None:
            log = DataLog("", [])
            log_json = log.getJSON()
        else:
            log_json = obj.Logs.getJSON()
        return dict(Version=obj.Version, HasError=obj.HasError, DisplayType=obj.DisplayType, Results=results_json, Logs=log_json)

    def getJSON(self):
        return json.dumps(DataExport.__toJSON(self))

    def __fromJSON(dct):
        strarray = dct["Results"]
        results_json = list(map(lambda x: DataResults.fromJSON(x), strarray))
        if dct["Logs"] is None:
            logs = DataLog("", [])
        else:
            logs = DataLog.fromJSON(dct["Logs"])
        return DataExport(dct["Version"], dct["HasError"], dct["DisplayType"], results_json, logs)

    def fromJSON(strjson):
        return json.loads(strjson, object_hook=DataExport.__fromJSON)
