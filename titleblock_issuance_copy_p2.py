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
	if sheet.LookupParameter("ISSUED FOR QC").AsString() != None:
		elems_on_sheet = FilteredElementCollector(doc,sheet.Id).ToElements()

		for elem in elems_on_sheet:
			if "FamilyInstance" in elem.ToString():
				outtie.append(elem)
				
				tbk_qc_issue_param = elem.LookupParameter("ISSUE - QC")
				
				if tbk_qc_issue_param != None:
					
					TransactionManager.Instance.EnsureInTransaction(doc)
		
					tbk_qc_issue_param.Set(True)
		
					TransactionManager.Instance.EnsureInTransaction(doc)				



OUT = 
