import rhinoscriptsyntax as rs


def DistributedSurfaceFitter():
    srf_id = rs.GetObject("Surface to fit", 8, True, True)
    if not srf_id: return

    pts = rs.GetPointCoordinates("Points to fit to", False)
    if not pts: return

    for n in range(1,100):
        nSrf = FitSurface(srf_id, pts)
        rs.DeleteObject(srf_id)
        srf_id = nSrf


def FitSurface(srf_id, samples):
    ptSurface = rs.SurfacePoints(srf_id)
    grSurface = rs.SurfaceEditPoints(srf_id, True, True)
    nrSurface = GrevilleNormals(srf_id)

    uvSamples = XYZ_To_UVW(srf_id, samples)
    vecForce = [(0,0,0) for p in ptSurface]
    vecFactor = [0 for p in ptSurface]

    #Create null vectors for all control-point forces
    for sample in uvSamples:
        for j in range(len(grSurface)):
            local_distance = (sample[0] - grSurface[j][0])**2 + (sample[1] - grSurface[j][1])**2
            local_factor = 100/(local_distance**2)
            local_force = nrSurface[j]
            local_force = rs.VectorScale(local_force, local_factor*sample[2])
            vecForce[j] = rs.VectorAdd(vecForce[j], local_force)
            vecFactor[j] = vecFactor[j] + local_factor


    for i in range(len(ptSurface)):
        ptSurface[i] = rs.PointAdd(ptSurface[i], rs.VectorDivide(vecForce[i], vecFactor[i]))
	
    srf_CP_Count = rs.SurfacePointCount(srf_id)
    srf_Knots = rs.SurfaceKnots(srf_id)
    srf_Weights = rs.SurfaceWeights(srf_id)
    srf_Degree = (rs.SurfaceDegree(srf, 0), rs.SurfaceDegree(srf_id, 1))
    return rs.AddNurbsSurface(srf_CP_Count, ptSurface, srf_Knots[0], srf_Knots[1], srf_Degree, srf_Weights)


def XYZ_To_UVW(srf_id, pXYZ):
    pUVW = []
    for pt in pXYZ:
        uvClosest = rs.SurfaceClosestPoint(srf_id, pt)
        ptClosest = rs.EvaluateSurface(srf_id, uvClosest)
        srfNormal = rs.SurfaceNormal(srf_id, uvClosest)
        pPositive = rs.PointAdd(ptClosest, srfNormal)
        pNegative = rs.PointSubtract(ptClosest, srfNormal)
        fDistance = rs.Distance(ptClosest, pt)

        if rs.Distance(pt,pPositive)>rs.Distance(pt,pNegative):
            fDistance = -fDistance
        pUVW.append( (uvClosest[0], uvClosest[1], fDistance) )
    return pUVW


def GrevilleNormals(srf_id):
    uvGreville = rs.SurfaceEditPoints(srf_id, True, True)
    return [rs.SurfaceNormal(srf_id, g) for g in uvGreville]


if __name__=="__main__":
    DistributedSurfaceFitter()
