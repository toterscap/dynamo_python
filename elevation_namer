#reference - http://thebuildingcoder.typepad.com/blog/2013/03/rename-view-by-matching-elevation-tag-with-room.html
 
import math
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
 
def angles_yo(view_section):
    elevX = view_section.ViewDirection.X
    elevY = view_section.ViewDirection.Y
 
    radian_angle = math.atan2(elevX-0,elevY-0)
    degrees_angle = math.degrees(radian_angle)
    return degrees_angle
   
def direction_yo(angle):
    if angle <= -45 and angle >=-135:
        return "EAST"
    if angle <= -135 and angle >= -180 or angle >= 135 and angle <= 180:
        return "NORTH"
    if angle >= 45 and angle <= 135:
        return "WEST"
    if angle >= -45 and angle <=45:
        return "SOUTH"
 
def getRoomAtPoint(view_section):
    xmax = (UnwrapElement(view_section).CropBox.Max.X)
    xmin = (UnwrapElement(view_section).CropBox.Min.X)
    ymax = (UnwrapElement(view_section).CropBox.Max.Y)
    ymin = (UnwrapElement(view_section).CropBox.Min.Y)
    zmax = (UnwrapElement(view_section).CropBox.Max.Z)     
    zmin = (UnwrapElement(view_section).CropBox.Min.Z)
 
    location_point = Autodesk.Revit.DB.XYZ(xmax-0.5*(xmax-xmin),ymax-0.5*(ymax-ymin),0)
    location_point_transform = view_section.CropBox.Transform.OfPoint(location_point)
 
    room_at_point = doc.GetRoomAtPoint(location_point_transform)
    # TransactionManager.Instance.EnsureInTransaction(doc)
    return room_at_point
 
def getBaseName(view_section):
    room_at_point = getRoomAtPoint(view_section)
 
    room_name = room_at_point.LookupParameter("Name").AsString()
    room_number = room_at_point.Number.ToString()
       
    view_angle = angles_yo(view_section)
    direction = direction_yo(view_angle)
 
    return (room_number + " " + room_name + " - " + direction)
 
 
view_sections = FilteredElementCollector(doc).OfClass(ViewSection).WhereElementIsNotElementType().ToElements()
 
unique_names = []
dones = [] 
 
TransactionManager.Instance.EnsureInTransaction(doc)

for view_section in view_sections:
    if view_section.LookupParameter("Type").AsValueString() == "Interior Elevation":
        base_name = getBaseName(view_section)
        new_name = base_name
       	counter = 1
        while new_name in unique_names:
            counter += 1
            new_name = base_name + " " + str(counter)
        unique_names.append(new_name)
       
		
		
        view_name_param = view_section.get_Parameter(BuiltInParameter.VIEW_NAME)
        done = view_name_param.Set(new_name)       
        dones.append(done) 
       
TransactionManager.Instance.TransactionTaskDone()  
 
 
OUT = dones, unique_names
