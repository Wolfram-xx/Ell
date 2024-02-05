import easygui
import pandas as excel
import OpenExFile

def SaveDataForOlimp(str1, str2):
    nameexcel = "Excel.xlsx"
    path = easygui.filesavebox("Таблица Excel", "Сохранить как", nameexcel, filetypes=["*.xlsx"])
    if (path != None):
        Data1 = excel.DataFrame(str1)
        Data2 = excel.DataFrame(str2)
        Data1.to_excel(path)
        excel.set_option('display.max_colwidth', 500)
        # excel.set_option('display.width', 500)
        with excel.ExcelWriter(path) as writer:
            Data1.to_excel(writer, sheet_name='Расчет первичных затрат', index=False)
            Data2.to_excel(writer, sheet_name='Расчет первичных затрат', index=False, startrow=2)
    """path = "C:\\Users\\lizag\\PycharmProjects\\pythonProject1\\asd.xlsx"
    path = OpenExFile.OpenFileEXL()"""
