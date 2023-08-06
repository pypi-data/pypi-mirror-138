from exectools.handler import *


class TestExecExcel:
    __excel_path = '~/Desktop/test_exec_tools.xlsx'
    __csv_path = '~/Desktop/test_exec_tools.csv'
    __excel_data = ExecExcel(__excel_path)
    __csv_data = ExecExcel(__csv_path)

    @classmethod
    def test_read(cls, sheet='Sheet1'):
        for i in cls.__excel_data.read(sheet=sheet).to_data():
            print(i)

    @classmethod
    def test_read_csv(cls):
        for i in cls.__csv_data.read_csv().to_data():
            print(i)

    @classmethod
    def test_read_to_excel(cls, sheet='Sheet1'):
        cls.__excel_data.read(sheet=sheet).to_excel()

    @classmethod
    def test_read_csv_to_excel(cls):
        cls.__csv_data.read_csv().to_excel()

    @classmethod
    def test_data_format(cls, data):
        for i in cls.__excel_data.data_format(data=data).to_data():
            print(i)

    @classmethod
    def test_append_row(cls, data):
        for i in cls.__excel_data.append_row(data=data).to_data():
            print(i)

    @classmethod
    def test_append_row_to_excel(cls, data):
        cls.__excel_data.append_row(data=data).to_excel()


if __name__ == '__main__':
    # TestExecExcel.test_append_row([dict(No=111, display_name="123")])
    TestExecExcel.test_append_row_to_excel([dict(No=111, display_name="123")])
    # TestExecExcel.test_read_to_excel(sheet="")
