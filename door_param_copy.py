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
uidoc = DocumentManager.Instance.CurrentUIDocument
#========================================================================


doors = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Doors).WhereElementIsNotElementType().ToElements()


outs = []

#old param
for door in doors:
	old_params = door.LookupParameter("Hardware Set")
	outs.append(old_params.AsString())
	
	if old_params.AsString() is not None:
		TransactionManager.Instance.EnsureInTransaction(doc)
		
		new_params = door.LookupParameter("DOOR HARDWARE").Set(old_params.AsString())
		
		TransactionManager.Instance.TransactionTaskDone()



# Place your code below this line

# Assign your output to the OUT variable.
OUT = outs, new_params
