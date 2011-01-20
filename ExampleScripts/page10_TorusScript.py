import rhinoscriptsyntax as rs

major_radius = rs.GetReal("Major radius", 10.0, 1.0, 1000.0)
minor_radius = rs.GetReal("Minor radius", 2.0, 0.1, 100.0)
sides = rs.GetInteger("Number of sides", 6, 3, 20)

point1 = " w" + str(major_radius) + ",0,0"
point2 = " w" + str(major_radius + minor_radius) + ",0,0"

rs.Command("_SelNone")
rs.Command("_Polygon _NumSides=" + str(sides) + " w0,0,0" + point1)
rs.Command("_SelLast")
rs.Command("-_Properties _Object _Name Rail _Enter _Enter")
rs.Command("_SelNone")
rs.Command("_Polygon _NumSides=" + str(sides) + point1 + point2)
rs.Command("_SelLast")
rs.Command("_Rotate3D w0,0,0 w1,0,0 90")
rs.Command("-_Properties _Object _Name Profile _Enter _Enter")
rs.Command("_SelNone")
rs.Command("-_Sweep1 _SelName Rail _SelName Profile _Enter _Closed=Yes Enter")
rs.Command("_SelName Rail")
rs.Command("_SelName Profile")
rs.Command("_Delete")
