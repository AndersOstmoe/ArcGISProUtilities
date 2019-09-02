import arcpy


def cutPolygonWithLines(polygon, lst_lines, pntg_center):
    for line in lst_lines:
        try:
            lst_pols = polygon.cut(line)
        except:
            lst_pols = [polygon]
        polygon = getCorrectPolygon(lst_pols, pntg_center)
    return polygon


def getCorrectPolygon(lst_pols, pntg_center):
    correct_polygon = None
    for polygon in lst_pols:
        if polygon.contains(pntg_center):
            correct_polygon = polygon
            break
    return correct_polygon


def getPoints(polyline, dist, tolerance):
    d1 = dist - tolerance if dist - tolerance > 0 else 0
    d2 = dist + tolerance if dist + tolerance < polyline.length else polyline.length
    pntg_d1 = polyline.positionAlongLine(d1, False)
    pntg_d2 = polyline.positionAlongLine(d2, False)
    pntg_dist = polyline.positionAlongLine(dist, False)
    return pntg_d1, pntg_d2, pntg_dist


def getAngle(pntg1, pntg2):
    return pntg1.angleAndDistanceTo(pntg2, method='PLANAR')[0]


def createPerpendicularCutLine(pntg, angle, dist, sr):
    pntg_cut_1 = pntg.pointFromAngleAndDistance(angle - 90, dist * 2.0, 'PLANAR')
    pntg_cut_2 = pntg.pointFromAngleAndDistance(angle + 90, dist * 2.0, 'PLANAR')
    cut_line = arcpy.Polyline(arcpy.Array([pntg_cut_1.firstPoint, pntg_cut_2.firstPoint]), sr)
    return cut_line


def main():

    fc = r'C:\Users\anders.ostmoe\OneDrive - Asplan Viak\Prosjekter\616937_E134\Veglinjer\TestBUffer.gdb\Linje1'
    fc_out = r'C:\Users\anders.ostmoe\OneDrive - Asplan Viak\Prosjekter\616937_E134\Veglinjer\TestBUffer.gdb\buffers1'
    length_section = 100.0 # each 100 meters
    buffer_dist = 10.0
    tol_dist = 0.1 #
    sr = arcpy.Describe(fc).spatialReference

    # get polyline (first one from fc)
    polyline = arcpy.da.SearchCursor(fc, ('SHAPE@')).next()[0]

    lst_buffers = []
    start = 0
    end = length_section
    print("polyline.length", polyline.length)
    while start < polyline.length:
        segment = polyline.segmentAlongLine(start, end, False)
        buffer1 = segment.buffer(buffer_dist)

        if end > polyline.length:
            end = polyline.length
        print(" - start", start, "  end", end)

        # get points around start and end of segment to determine angles
        pntg_d1, pntg_d2, pntg_start = getPoints(polyline, start, tol_dist)
        pntg_d3, pntg_d4, pntg_end = getPoints(polyline, end, tol_dist)
        pntg_center = polyline.positionAlongLine((start + end) / 2.0, False)

        # angle at start and end of segment
        angle_start = getAngle(pntg_d1, pntg_d2)
        angle_end = getAngle(pntg_d3, pntg_d4)

        # create perpendicular cutline
        cut_line_start = createPerpendicularCutLine(pntg_start, angle_start, buffer_dist, sr)
        cut_line_end = createPerpendicularCutLine(pntg_end, angle_end, buffer_dist, sr)

        # cut buffer polygon
        polygon = cutPolygonWithLines(buffer1, [cut_line_start, cut_line_end], pntg_center)
        lst_buffers.append(polygon)

        # for next segment
        start = end
        end += length_section

    # store results
    arcpy.CopyFeatures_management(lst_buffers, fc_out)


main()
