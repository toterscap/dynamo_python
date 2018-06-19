import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

clr.AddReference('Microsoft.Office.Interop.Excel, Version=11.0.0.0, Culture=neutral, PublicKeyToken=71e9bce111e9429c')
from Microsoft.Office.Interop import Excel
from System.Runtime.InteropServices import Marshal

clr.AddReference("RevitAPI")
import Autodesk
from Autodesk.Revit.DB import *

clr.AddReference("RevitServices")
import RevitServices 
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)
clr.ImportExtensions(Revit.GeometryConversion)

doc = DocumentManager.Instance.CurrentDBDocument


path = r"W:\66370\Record-Set\_Existing\1998 BAA Most Current Dwgs\SHEET LIST.xlsx"

#instantiate excel
ex = Excel.ApplicationClass()
ex.Visible = False
ex.DisplayAlerts = False

workbook = ex.Workbooks.Open(path)

ws = workbook.Worksheets[1]

x1range = ws.Range["A1","A88"]
x2range = ws.Range["B1","B88"]

r1 = [str(item) for item in x1range.Value2]
r2 = [str(item) for item in x2range.Value2]



##########################################################################


outs = []

TransactionManager.Instance.EnsureInTransaction(doc)

for index, value in enumerate(r1):
	newsheet = ViewSheet.CreatePlaceholder(doc)
	newsheet.SheetNumber = r1[index]
	newsheet.Name = r2[index]
	outs.append(newsheet)
	p = newsheet.LookupParameter("Discipline")
	
	if newsheet.SheetNumber[0] == "E":
		p.Set("06 - ELECTRICAL")
	elif newsheet.SheetNumber[0] == "P" or newsheet.SheetNumber[0] == "F":
		p.Set("04 - PLUMBLING AND FIRE PROTECTION")
	elif newsheet.SheetNumber[0] == "D":
		p.Set("01 - DEMOLITION")
	elif newsheet.SheetNumber[0] == "M":
		p.Set("05 - MECHANICAL")
	elif newsheet.SheetNumber[0] == "S":
		p.Set("03 - STRUCTURAL")
	elif newsheet.SheetNumber[0] == "A":
		p.Set("02 - ARCHITECTURE")
		
	p.Set(index)
	date = newsheet.get_Parameter(BuiltInParameter.SHEET_ISSUE_DATE)
	date.Set("1998")


TransactionManager.Instance.TransactionTaskDone()

OUT = r1


ex.ActiveWorkbook.Close(False)
Marshal.ReleaseComObject(ws)
Marshal.ReleaseComObject(workbook)
Marshal.ReleaseComObject(ex)
