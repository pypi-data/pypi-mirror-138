import pandas as pd


f_path = '~/Desktop/test_exec_tools.xlsx'

data1 = pd.ExcelFile(f_path).sheet_names
# data2 = pd.read_excel(f_path)
# all_data = [data1, data2]

# data3 = pd.concat(all_data)
print(data1)
