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


path = r"P:\2019\19049\BIM\a\lib\spec test"

files = Directory.GetFiles(path)

imageOptions = Autodesk.Revit.DB.ImageImportOptions()

dims = []
boundbox = []
vertex = []
images= []

for file in files:
	TransactionManager.Instance.EnsureInTransaction(doc)

	outs = doc.Import(file,imageOptions,doc.ActiveView)

	TransactionManager.Instance.TransactionTaskDone()
	
	images.append(outs[1])
	
	dims.append([outs[1].LookupParameter("Width").AsValueString(),outs[1].LookupParameter("Height").AsValueString()])
	
	vertex.append(outs[1].LookupParameter("Height"))
	


OUT = images
