import xlrd


class ExcelUtil(object):

    def __init__(self, excelPath, sheetName=None):
        self.data = xlrd.open_workbook(excelPath)
        self.sheets = self.data.sheet_names()
        if sheetName:
            self.get_single(sheetName)
        else:
            self.get_all()

    # 返回所有sheet的数据，返回值类型为dict，可用sheet名字遍历取值
    def get_all(self):
        all_sheet = {}
        for sheet in self.sheets:
            all_sheet[sheet] = (self.get_single(sheet))
        return all_sheet

    # 返回指定名字sheet的数据，返回里欸写那个为list
    def get_single(self, sheet):
        table = self.data.sheet_by_name(sheet)
        rowNum = table.nrows
        colNum = table.ncols
        if rowNum < 1:
            return None
        title = table.row_values(0)
        curRowNo = 1
        sheet_data = []
        while curRowNo < rowNum:
            row_data = {}
            row = table.row_values(curRowNo)
            for x in range(colNum):
                if row[x] is not None:
                    row_data[title[x]] = row[x]
                else:
                    row_data[title[x]] = None
            sheet_data.append(row_data)
            curRowNo += 1
        return sheet_data


if __name__ == '__main__':
    print(ExcelUtil('C:/Users/Administrator/Desktop/testdata.xlsx').get_all())
