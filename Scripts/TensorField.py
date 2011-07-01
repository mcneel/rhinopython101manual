import rhinoscriptsyntax as rs


def SurfaceTensorField():
    #Prompt the user for all required data
    srf_id = rs.GetObject("Surface for tensor curvature field", 8, True, True)
    if not srf_id: return

    u = 100
    v = 100
    s = 10

    pListBoxResult = rs.PropertyListBox( ("U-samples", "V-samples", "Smoothing iterations"), \
        (u, v, S), "Algorithm settings", "Tensor field")
    if not pListBoxResult: return

    #Convert all strings in the PopertyListBox result into numbers again
    u = int(pListBoxResult[0])
    v = int(pListBoxResult[1])
    s = int(pListBoxResult[2])
    #Make sure the values are within logical limits
    if u<1 or v<1 or s<0: return

    #At this point we have all input data collected.
    #We also know all values are correct

    #Initiate the Tensor Space
    T, K = SurfaceTensorField(srf_id, u, v)
    if not T or not K:
        print "Unable to construct basis Tensor field"
        return

    #Smooth the Tensor Space s times
    for i in range(s):
        rs.Prompt("Smoothing tensor field. Iteration: %d" % i)
        T, K = SmoothTensorField(T, K)


    #Add all Tensors as line segments
	Call Rhino.EnableRedraw(False)
	Dim A, B
	For i = 0 To u
		For j = 0 To v
			A = T(i,j)(0)
			B = Rhino.PointAdd(A, K(i,j))

			Call Rhino.AddLine(A, B)
		Next
	Next
	Call Rhino.EnableRedraw(True)
End Sub

def SurfaceTensorField(srf_id, Nu, Nv):
    uDomain = rs.SurfaceDomain(srf_id, 0)
    vDomain = rs.SurfaceDomain(srf_id, 1)

    t = []
    k = []
    for i in range(Nu):
        u = uDomain[0] + (i/Nu)*(uDomain[1]-uDomain[0])
        for j in range(Nv):
            v = vDomain[0]+(j/Nv)*(vDomain[1]-vDomain[0])
            t.append( rs.SurfaceFrame(srf_id, (u,v)) )
            k.append( rs.SurfaceCurvature(srf_id, (u,v))[5] )
    return t,k


def SmoothTensorField(t,k):
    
	SmoothTensorField = False
	Dim K_copy : K_copy = K
	
	Dim Ub1 : Ub1 = UBound(T, 1)
	Dim Ub2 : Ub2 = UBound(T, 2)
	
	Dim i, j, x, y, xm, ym
	Dim k_tot, k_dir
	
	For i = 0 To Ub1
		For j = 0 To Ub2
			k_tot = Array(0,0,0)
			
			For x = i-1 To i+1
				xm = (x+Ub1) Mod Ub1
				For y = j-1 To j+1
					ym = (y+Ub2) Mod Ub2
					
					'If (x >= 0) And (y >= 0) And (x <= Ub1) And (y <= Ub2) Then
					k_tot = Rhino.VectorAdd(k_tot, K_copy(xm,ym))
					'End If
				Next
			Next
			
			k_dir = Rhino.PlaneClosestPoint(T(i,j), Rhino.VectorAdd(T(i,j)(0), k_tot))
			k_tot = Rhino.VectorSubtract(k_dir, T(i,j)(0))
			k_tot = Rhino.VectorUnitize(k_tot)
			
			K(i,j) = k_tot
		Next
	Next
	
	SmoothTensorField = True
End Function


if __name__=="__main":
    SurfaceTensorField()
