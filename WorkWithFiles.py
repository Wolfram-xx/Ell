import shutil
import easygui
from zipfile import ZipFile

def save_inzip(files):
    exportPath = easygui.filesavebox(title="Сохранить в", default= "./name.zip", filetypes=["*zip"])
    with ZipFile(exportPath, "w") as myzip:
        for i in range(len(files)):
            myzip.write(files[i])
    pass
def copyfile(src, dest = 'img'):
    shutil.copy2(src, dest)

def open_and_copypath(typefile):
    return easygui.fileopenbox(typefile, "Открыть")
    pass
