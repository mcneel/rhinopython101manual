import rhinoscriptsyntax as rs


def PrincipalCurvatureMapper():
    select = rs.GetSurfaceObject("Point on surface to start from", False, True)
    if not select: return
    if select[2]!=1:
        print "You must pick on a surface for this to work"
        return
    srf_id = select[0]
    uvPt = select[4]


	
	Dim idSrf : idSrf = dSelect(0)
	Dim uvPt : uvPt = dSelect(4)
	
	Dim uvPts() : ReDim uvPts(0) : uvPts(0) = uvPt
	Dim i, nUVPt
    uvPts = [uvPt]	
    for i in range(10000):
        nUVPt = MapCurvatureStep(srf_id, upPts[i], True, True, 0.1)
        if not nUVPt: break
        uvPts.append(nUVPt)

    if uvPts: rs.AddInterpCrvOnSrfUV(srf_id, uvPts) 


def MapCurvatureStep(srf_id, uvPt, max, reverse, accuracy):
    data_curvature = rs.SurfaceCurvature(srf_id, uvPt)
    if not data_curvature: return
    vec = data_curvature[5]
    if max: vec = data_curvature[3]

    if reverse: vec = rs.VectorReverse(vec)
    vec = rs.VectorUnitize(vec)
    vec = rs.VectorScale(vec, accuracy)

    dPoint = rs.VectorAdd(data_curvature[0], vec)
    nPoint = rs.SurfaceClosestPoint(srf_id, dPoint)
    mPoint = rs.EvaluateSurface(srf_id, nPoint)

    if rs.Distance(mPoint, data_curvature[0])< (0.5*accuracy): return
    return nPoint


if __name__=="__main__":
    PrincipalCurvatureMapper()