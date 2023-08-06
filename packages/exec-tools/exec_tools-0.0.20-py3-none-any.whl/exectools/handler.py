from exectools.tools_excel import ExecExcel
from exectools.tools_basic import Tools
from json import load, dump


class ExecImport:
    def __init__(self, path):
        self.path = Tools.extend_path(path)

    def from_json(self):
        with open(self.path, 'r') as f:
            return load(f)

    def from_excel(self, sheet='Sheet1', axis=0, index_col=None,
                   orient='records', empty=False, nana=None, **kwargs) -> iter:
        return ExecExcel(self.path).read(sheet, axis, index_col, **kwargs).to_data(orient, empty, nana)


class ExecExport:
    def __init__(self, path):
        self.path = Tools.extend_path(path)

    def to_json(self, data):
        with open(self.path, 'w') as f:
            dump(data, f)

    def to_excel(self, data: list, sheet='Sheet1', file_path=None, index=False, axis=0, index_col=None, **kwargs):
        ExecExcel(self.path).append_row(data, sheet, axis, index_col).to_excel(sheet, file_path, index, **kwargs)
