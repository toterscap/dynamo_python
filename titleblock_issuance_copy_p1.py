import clr
clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)

clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

clr.AddReference("RevitAPI")
import Autodesk
from Autodesk.Revit.DB import *

import System
from System.Collections.Generic import *

doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication


sheets = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Sheets).WhereElementIsNotElementType().ToElements()


for sheet in sheets:
	if sheet.LookupParameter("ISSUED FOR PERMIT").AsString() != None:
		issue_parameter = sheet.LookupParameter("ISSUED FOR QC")
	
		TransactionManager.Instance.EnsureInTransaction(doc)
		
		issue_parameter.Set("●")

		TransactionManager.Instance.TransactionTaskDone()

OUT = 
