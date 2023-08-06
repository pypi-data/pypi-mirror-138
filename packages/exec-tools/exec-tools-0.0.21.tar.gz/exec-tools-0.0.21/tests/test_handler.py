from exectools import *


if __name__ == '__main__':
    # ExecExport("~/Desktop/test_exec_tools_empty.xlsx").to_excel([dict(No=111, display_name="123")])
    for i in ExecImport("~/Desktop/test_exec_tools.xlsx").from_excel():
        print(i)
