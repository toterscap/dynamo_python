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
 
from System.IO import *
 
doc = DocumentManager.Instance.CurrentDBDocument 
uiapp = DocumentManager.Instance.CurrentUIApplication 

images = UnwrapElement(IN[0])


def boundingBoxMove(box, row, column):
	
	boxMax = box.Max
	boxMin = box.Min

	boxMaxX = boxMax.X
	boxMinX = boxMin.X

	boxMaxY = boxMax.Y
	boxMinY = boxMin.Y
	
	Xvector = XYZ(boxMaxX-boxMinX,0,0)
	Yvector = XYZ(0,boxMinY-boxMaxY,0)

	Xvector = Xvector*column 
	Yvector = Yvector*row
	
	vector = Xvector + Yvector
	
	return vector
	



column = 0
row = 0

for image in images:
	

	image = doc.GetElement(image.Id)

	box = image.get_BoundingBox(doc.ActiveView)
	
	vector = boundingBoxMove(box, row, column)

	location = image.Location

	TransactionManager.Instance.EnsureInTransaction(doc)

	location.Move(vector)


	TransactionManager.Instance.TransactionTaskDone()
	
	#image location in grid
	if row == 2:
		column += 1
		row = 0
	else:
		row += 1
	

OUT = vector
