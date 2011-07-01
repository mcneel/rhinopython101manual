import rhinoscriptsyntax as rs


def main():
    srf_id = rs.GetObject("Surface to recurse", 8, True, True)
    if not srf_id: return
    udomain = rs.SurfaceDomain(srf_id, 0)
    vdomain = rs.SurfaceDomain(srf_id, 1)
    RecurseSurface(srf_id, udomain[0], udomain[1], vdomain[0], vdomain[1])


def RecurseSurface( srf_id, u0, u1, v0, v1):
    A = rs.EvaluateSurface(srf_id, (u0,v0))
    B = rs.EvaluateSurface(srf_id, (u1,v0))
    C = rs.EvaluateSurface(srf_id, (u1,v1))
    D = rs.EvaluateSurface(srf_id, (u0,v1))

    gauss = SurfaceCurvature(srf_id, u0, u1, v0, v1)
    diag = rs.Distance(A, C)
    factor = abs(diag*gauss)
    
    print "Gauss:", round(gauss,4),
    print "    Diagonal:", round(diag,2),
    print "    Factor:", round(factor, 3)

    if factor<10:
        rs.AddCurve( (A, B, C, D, A), 3)
    else:
        um = u0 + 0.5 * (u1-u0)
        vm = v0 + 0.5 * (v1-v0)
        RecurseSurface(srf_id, u0, um, v0, vm)
        RecurseSurface(srf_id, um, u1, v0, vm)
        RecurseSurface(srf_id, u0, um, vm, v1)
        RecurseSurface(srf_id, um, u1, vm, v1)


def SurfaceCurvature( srf_id, u0, u1, v0, v1):
    gsum = 0.0
    ustep = 0.1 * (u1-u0)
    vstep = 0.1 * (v1-v0)
    u = u0
    while u<u1+(0.5*ustep):
        v = v0
        while v<v1+(0.5*vstep):
            gdat = rs.SurfaceCurvature(srf_id, (u,v))
            if gdat: gsum += gdat[6]
            v += vstep
        u += ustep
    return gsum


if __name__=="__main":
    main()