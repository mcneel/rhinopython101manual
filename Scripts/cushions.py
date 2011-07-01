#Script written by David Rutten and adapted to python by Steve Baer
#Script copyrighted by Robert McNeel & Associates
#Script version Wednesday, January 19, 2011


def main():
    curves_a = GetCurveSeries("Pick ordered curves in first direction. Press Enter to complete.")
    if not curves_a: return #no curves were picked

    rs.LockObjects(curves_a) #Prevent these curves from being picked again

    curves_b = GetCurveSeries("Pick ordered curves in second direction. Press Enter to complete.")
    rs.UnlockObjects(curves_a)

    if not curves_b: return #no curves were picked

    #We now have a set of ordered curves in two directions, A & B:
    # A =  0  1  2  3  4  5  6
    #      │  │  │  │  │  │  │
    #      │  │  │  │  │  │  │
    #      │  │  │  │  │  │  │
    #      │  │  │  │  │  │  │
    #
    # B = ─────────────────────0
    #     ─────────────────────1
    #     ─────────────────────2
    #     ─────────────────────3
    #     ─────────────────────4
    #
    #We need to intersect them 2 by 2, so we iterate over all 'intersection squares' 
    #Each square of curves A, B, C, D gives us 4 intersection points: K, L, M, N
    #      C      D
    #      │      │
    #      │      │
    #  ────K──────L────A
    #      │      │
    #  ────M──────N────B
    #      │      │
    #      │      │

    #Shorthand function for curve curve intersction
    #Returns either None if curves do not intersect or just the first intersection point
    def CCX( idCurve1, idCurve2):
        datX = rs.CurveCurveIntersection(idCurve1, idCurve2)
        if datX: return datX[0][1]

    for i in range(len(curves_a)-1):
        for j in range(len(curves_b)-1):
            A = curves_a[i]
            B = curves_a[i+1]
            C = curves_b[j]
            D = curves_b[j+1]
            K = CCX(A, C)
            L = CCX(A, D)
            M = CCX(B, C)
            N = CCX(B, D)
            if not K or not L or not M or not N:
                pass
                #At least one intersection wasn't found, we have to skip this combination
            else:
                rs.AddSrfPt((K, L, N))
                rs.AddSrfPt((K, N, M))


#Asks the user to select a set of curves, one by one
def GetCurveSeries(prompt):
    curve_ids = []
    dot_ids = []
    for i in xrange(1000000): #Assume nobody will pick more than 1 million curves by hand
        id = rs.GetObject(prompt, 4, False, True)
        if not id: break
        dot_ids = rs.AddTextDot(i+1, rs.CurveMidPoint(id))
        curve_ids.append(id)

    rs.DeleteObjects(dot_ids)
    return curve_ids


if __name__=="__main__":
    main()