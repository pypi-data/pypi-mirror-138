import unittest
from unittest.mock import patch
from src.lenden.dataexport import *
import json


class TestDataExports(unittest.TestCase):

    def get_DataResults1(self):
        desc = "Irure aute ex irure fugiat."
        help = "Ex consequat nostrud enim nulla dolore incididunt officia ullamco ut consequat mollit nulla."
        type = ResultType.image
        path = "/path/to/image"
        size = ResultSizeType.normal
        format = "f2%"
        dataR1 = DataResults(Description=desc, Help=help,
                             Type=type, Path=path, Size=size, Format=format)
        return dataR1

    def get_DataResults2(self):
        desc = "Dolore culpa duis duis nulla duis eiusmod ullamco adipisicing aliqua."
        help = "Dolore mollit nulla.Nulla amet quis ad deserunt sit laboris irure incididunt est ea occaecat sunt."
        type = ResultType.numberarray
        path = "/path/to/numbersfile"
        size = ResultSizeType.big
        format = "%f12%"
        data1 = DataResults(Description=desc, Help=help,
                            Type=type, Path=path, Size=size, Format=format)
        return data1

    def test_DataExport_Not_Equals(self):
        data1 = self.get_DataResults1()
        data2 = self.get_DataResults2()

        data = DataExport(Version=0.1, HasError=False,
                          DisplayType=DisplayType.grid, Results=[data1, data2], Logs=None)

        dem0 = data.getJSON()
        data2 = DataExport.fromJSON(dem0)

        self.assertEqual(data, data2)
