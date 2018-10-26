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

dataEnteringNode = IN

#===================================================================

def feet_to_decimal(figure):
  feet = figure.split('\'')[0]
  inches = figure.split('-')[1][:-1]
  product = float(feet) + float(inches)/12
  return product


def point_to_XYZ(point):
  split = str(point).split(',')
  x = float(split[0].split('=')[1])
  y = float(split[1].split('=')[1])
  z = float(split[2].split('=')[1][:-1])
  return XYZ(x,y,z)

def make_room_plan(rm):
	rm_level = rm.GetParameterValueByName("Level")
	for level in levels:
		if rm_level == level.Name:
			level = level.Id
			
			TransactionManager.Instance.EnsureInTransaction(doc)
			
			new_plan = ViewPlan.Create(doc, floor_plan, level)
			
			TransactionManager.Instance.TransactionTaskDone()
			
			old_name = new_plan.LookupParameter("Name")
		
			return new_plan

#==================================================================

#get levels in project
levels = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Levels).WhereElementIsNotElementType().ToElements()


#type of plan created
view_type = FilteredElementCollector(doc).OfClass(ViewFamilyType).ToElements()

#type of floor plan created
for view in view_type:
	if UnwrapElement(view.FamilyName.ToString()) == "Floor Plan":
		floor_plan = view.Id


#list of rooms to have plans made
room = IN[0]
room_unwrap = UnwrapElement(room)
room_level = room_unwrap.get_Parameter(BuiltInParameter.ROOM_LEVEL_ID).AsValueString()
room_location = point_to_XYZ(room.Location)


level_set = 0
for level in levels:
	if room_level == level.Name:
		elevation = level.get_Parameter(BuiltInParameter.LEVEL_ELEV).AsValueString()
		level_set = feet_to_decimal(elevation)

#new view
new_plan = make_room_plan(room)
#crops on and open to be non-orthagonal and so it can be set further down
new_plan.CropBoxVisible = True
new_plan.CropBoxActive = True

expandVal = 2

bounds = room_unwrap.get_BoundingBox(None)
minPt = XYZ(bounds.Min.X-expandVal,bounds.Min.Y-expandVal,0)
maxPt = XYZ(bounds.Max.X+expandVal,bounds.Max.Y+expandVal,0)

bounds.Min = minPt
bounds.Max = maxPt

#bounds_poly = bounds.ToPolySurface()

segment_list = room_unwrap.GetBoundarySegments(SpatialElementBoundaryOptions())
segment_list = [y for x in segment_list for y in x]

segments_for_bounds = []


loop = CurveLoop.Create(segments_for_bounds)


crop = new_plan.GetCropRegionShapeManager()
#crop.SetCropShape(loop)

new_plan.CropBox = bounds
new_plan.CropBoxVisible = False

OUT = new_plan
