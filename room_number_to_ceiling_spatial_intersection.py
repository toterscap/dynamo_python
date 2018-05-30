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

doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication

roomz = FilteredElementCollector(doc).OfClass(SpatialElement).ToElements()

roomz_out = []

calculator = SpatialElementGeometryCalculator(doc)

results_out = []
ceilings_out = []
element_outs = []

for room in roomz:
	number = room.Number
	try:
		results = calculator.CalculateSpatialElementGeometry(room)
		results_out.append(results)
	except:
		pass
	room_solid = results.GetGeometry()
	ceilings = FilteredElementCollector(doc).OfClass(Ceiling)
	ceilings_intersect = ceilings.WherePasses(ElementIntersectsSolidFilter(room_solid))
	ceilings_out.append(ceilings_intersect)
	for ceiling in ceilings_intersect:
		try:
			TransactionManager.Instance.EnsureInTransaction(doc)
			element_param = ceiling.LookupParameter("Ceiling Room Number").Set(number)
			TransactionManager.Instance.TransactionTaskDone()
			element_outs.append(element_param)
		except:
			pass			
				
#Assign your output to the OUT variable.
OUT = element_outs
