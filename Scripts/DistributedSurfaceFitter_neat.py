import rhinoscriptsyntax as rs


def DistributedSurfaceFitter():
    srf_id = rs.GetObject("Surface to fit", 8, True, True)
    if not srf_id: return


    pts = rs.GetPointCoordinates("Points to fit to", False)
    if not pts: return

    for n in xrange(10000):
        rs.EnableRedraw(False)
        nSrf, dTrans, dProx = FitSurface(srf_id, pts)
        #Call Rhino.DeleteObject(idSrf)
        rs.EnableRedraw(True)
        rs.Prompt("Translation = %.2f  Deviation = %.2f" % dTrans, dProx)
        if dTrans<0.1 or dProx<0.01: break
        srf_id = nSrf
    print "Final deviation = %.4f" % dProx


def FitSurface(srf_id, samples):
    surf_points = rs.SurfacePoints(srf_id)
    G = rs.SurfaceEditPoints(srf_id, True, True)
    N = GrevilleNormals(srf_id)
    S = ConvertToUVW(srf_id, samples)

    Forces = [(0,0,0) for pt in surf_points]
    Factors = [0.0 for pt in surf_points]
    proximity = 0.0
    translation = 0.0

    for i in range(len(S)):
        proximity += abs(S[i][2])
        for j in range(len(surf_points)):
            local_dist = (S[i][0] - G[j][0])**2 + (S[i][1] - G[j][1])**2
            if local_dist<0.01: local_dist=0.01
            local_factor = 1/local_dist
            local_force = rs.VectorScale(N[j], local_factor*S[i][2])
            Forces[j] = rs.VectorAdd(Forces(j), local_force)
            Factors[j] += local_factor

    Forces = DivideVectorArray(Forces, Factors)

    for i in range(len(surf_points)):
        surf_points[i] = rs.PointAdd(surf_points[i], Forces[i])
        translation += rs.VectorLength(Forces[i])

    srf_N = rs.SurfacePointCount(srf_id)
    srf_K = rs.SurfaceKnots(srf_id)
    srf_W = rs.SurfaceWeights(srf_id)
    srf_D = (rs.SurfaceDegree(srf_id, 0), rs.SurfaceDegree(srf_id, 1))
    return rs.AddNurbsSurface(srf_N, P, srf_K[0], srf_K[1], srf_D, srf_W)


def ConvertToUVW(srf_id, xyz_points):
    uvw_points = []
    for point in xyz_points:
        Suv = rs.SurfaceClosestPoint(srf_id, point)
        Sxyz = rs.EvaluateSurface(srf_id, Suv)
        Snormal = rs.SurfaceNormal(srf_id, Suv)
        dirPos = rs.PointAdd(Sxyz, Snormal)
        dirNeg = rs.PointSubtract(Sxyz, Snormal)
        Sdist = rs.Distance(Sxyz, point)
        if rs.Distance(point, dirPos)>rs.Distance(point,dirNeg):
            Sdist = -Sdist
        uvw_points.append((Suv(0), Suv(1), Sdist))
    return uvw_points


def DivideVectorArray(Vectors, Factors):
    rc = [rs.VectorDivide(Vectors[i], Factors[i]) for i in range(len(Vectors))]
    return rc


def GrevilleNormals(srf_id):
    uvGreville = rs.SurfaceEditPoints(srf_id, True, True)
    return [rs.SurfaceNormal(srf_id, g) for g in uvGreville]


if __name__=="__main__":
    DistributedSurfaceFitter()
