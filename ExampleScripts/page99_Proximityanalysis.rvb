Option Explicit
'Script written by David Rutten
'Script copyrighted by Robert McNeel & Associates
'Script version 15 July 2007 18:56:57

Call ProximityAnalysis()
Sub ProximityAnalysis()
	Dim idMesh, idBRep
	
	idMesh = Rhino.GetObject("Mesh for proximity analysis", 32, True, True)
	If IsNull(idMesh) Then Exit Sub
	
	idBRep = Rhino.GetObject("Surface for proximity test", 8+16, False, True)
	If IsNull(idBRep) Then Exit Sub
	
	Dim arrV, arrF, arrD
	arrV = Rhino.MeshVertices(idMesh)
	arrF = Rhino.MeshFaceVertices(idMesh) 
	arrD = VertexValueArray(arrV, idBRep)
	
	Dim minD : minD = Rhino.Min(arrD)
	Dim maxD : maxD = Rhino.Max(arrD)
	Dim proxFactor, i
	Dim arrC() : ReDim arrC(UBound(arrV))
	
	For i = 0 To UBound(arrV)
		proxFactor = (arrD(i) - minD) / (maxD - minD)

		arrC(i) = RGB(255, 255*proxFactor, 255*proxFactor)
	Next
	
	Call Rhino.AddMesh(arrV, arrF, ,, arrC)
	Call Rhino.DeleteObject(idMesh)
End Sub

Function VertexValueArray(ByVal pts, ByVal id)
	Dim i, arrD() : ReDim arrD(UBound(pts))
		
	For i = 0 To UBound(pts)
		arrD(i) = DistanceTo(pts(i), id)
	Next
	VertexDistanceArray = arrD
End Function

Function DistanceTo(ByVal pt, ByVal id)
	DistanceTo = Null
	Dim ptCP : ptCP = Rhino.BrepClosestPoint(id, pt)
	
	If IsNull(ptCP) Then Exit Function
	Dim D : D = Rhino.Distance(pt, ptCP(0))
	D = Log(D + 1.0)
	
	DistanceTo = D
End Function