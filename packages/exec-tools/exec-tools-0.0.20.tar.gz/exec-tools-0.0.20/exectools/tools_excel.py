from os.path import exists, expanduser
import pandas as pd
import time


class ExecExcel:
    """
    read xlsx and csv
    """
    def __init__(self, file_path):
        self.file_path = expanduser(file_path)

    def read(self, sheet='Sheet1', axis=0, index_col=None, **kwargs):
        df = pd.ExcelFile(self.file_path)
        sheets = [sheet] if sheet else df.sheet_names
        df_parse = df.parse(sheets, index_col=index_col, **kwargs)
        frame_data = pd.concat(df_parse, axis=axis)
        return ExcelResponse(frame_data, self.file_path)

    def read_csv(self, **kwargs):
        frame_data = pd.read_csv(self.file_path, **kwargs)
        return ExcelResponse(frame_data, self.file_path)

    def data_format(self, data: list, axis=0):
        """
        Write data to excel.
        :param axis:
        :param data: dict in list
        """
        fd = [pd.DataFrame(item, index=[0]) for item in data]
        frame_data = pd.concat(fd, axis=axis)
        return ExcelResponse(frame_data, self.file_path)

    def append_row(self, data: list, sheet='Sheet1', axis=0, index_col=None, **kwargs):
        if exists(self.file_path):
            df = pd.ExcelFile(self.file_path)
            sheets = [sheet] if sheet else df.sheet_names
            df_parse = df.parse(sheets, index_col=index_col, **kwargs)
            frame_data = pd.concat(df_parse, axis=axis)
        else:
            frame_data = pd.DataFrame()
        new_data = pd.concat([pd.DataFrame(item, index=[0]) for item in data], axis=axis)
        frame_data = pd.concat([frame_data, new_data], axis=axis)
        return ExcelResponse(frame_data, self.file_path)


class ExcelResponse:
    def __init__(self, frame_data, file_path: str):
        self.frame_data = frame_data
        self.file_path = file_path

    def to_data(self, orient='records', empty=False, nana=None):
        """
        :param empty: if True show empty value
        :param orient:
        {
        orient=’records’: [{column -> value}, … , {column -> value}],
        orient=’index’  : {index -> {column -> value}},
        orient=’dict’   : {column -> {index -> value}},
        orient=’list’   : {column -> [values]} ,
        orient=’series’ : {column -> Series(values)},
        orient=’split’  : {index -> [index], columns -> [columns], data -> [values]},
        }
        :param nana: null display NaNa/None/''
        :return: dict : generator object
        """
        frame_data = self.frame_data.where(self.frame_data.notnull(), nana)
        data_load = frame_data.to_dict(orient=orient)
        if orient == 'records':
            for index, value in enumerate(data_load):
                yield {k: v for k, v in value.items()} if empty else {k: v for k, v in value.items() if v}
        else:
            for index, value in data_load.items():
                if value is dict:
                    yield index, {k: v for k, v in value.items()} if empty else {k: v for k, v in value.items() if v}
                else:
                    yield {index: value}

    def to_excel(self, sheet="Sheet1", file_path=None, index=False, **kwargs):
        """
        Write data to excel.
        :param index:
        :param file_path: save excel file name
        :param sheet: excel sheet name
        """
        file_path = file_path or self.file_path.rsplit('.')[0] + f'_{int(time.time())}.xlsx'
        self.frame_data.to_excel(file_path, index=index, sheet_name=sheet, **kwargs)
