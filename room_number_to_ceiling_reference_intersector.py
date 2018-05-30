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

ray_direction = XYZ(0,0,1)

ref_intersector = ReferenceIntersector(doc.ActiveView)

number_outs = []
outs = []
origin_outs = []
ref_context_outs = []
element_outs = []

for room in roomz:
	number = room.Number
	number_outs.append(number)
	origin = room.Location.Point
	origin_outs.append(origin)
	ref_context = ref_intersector.Find(origin,ray_direction)
	ref_context_outs.append(ref_context)
	for index,context in enumerate(ref_context):
		if index == 0:
			id = context.GetReference().ElementId
			element = doc.GetElement(id)
			outs.append(element)
			
			TransactionManager.Instance.EnsureInTransaction(doc)
			element_param = element.LookupParameter("Ceiling Room Number").Set(number)
			TransactionManager.Instance.TransactionTaskDone()
			
			element_outs.append(element_param)
	
#Assign your output to the OUT variable.
OUT = element_outs
