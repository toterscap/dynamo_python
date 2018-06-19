import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

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

from System.IO import *

doc = DocumentManager.Instance.CurrentDBDocument


path = r"W:\66370\Record-Set\_Existing\1968 Mass Archives Dwg Scans\Small PDF"

files = Directory.GetFiles(path)

full_name = []
sheet_number = []
sheet_name = []


for file in files:
	split_1 = file.split("Small PDF\\")[1]
	full = split_1[:-4]
	full_name.append(full)
	sheet_number.append(full.split(" ",1)[0])
	sheet_name.append(full.split(" ",1)[1])
	
##########################################################################


outs = []

TransactionManager.Instance.EnsureInTransaction(doc)

for index, value in enumerate(sheet_number):
	newsheet = ViewSheet.CreatePlaceholder(doc)
	newsheet.SheetNumber = sheet_number[index]
	newsheet.Name = sheet_name[index]
	outs.append(newsheet)
	p = newsheet.LookupParameter("Discipline")
	
	if newsheet.SheetNumber[0] == "E":
		p.Set("04 - ELECTRICAL")
	elif newsheet.SheetNumber[0] == "P":
		p.Set("02 - PLUMBLING")
	elif newsheet.SheetNumber[0] == "H":
		p.Set("03 - MECHANICAL")
	elif newsheet.SheetNumber[0] == "A":
		p.Set("01 - ARCHITECTURE")
		

	date = newsheet.get_Parameter(BuiltInParameter.SHEET_ISSUE_DATE)
	date.Set("1968")


TransactionManager.Instance.TransactionTaskDone()

OUT = sheet_name,sheet_number
