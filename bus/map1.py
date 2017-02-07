"""
1. Shape containing multiple parts(polygon) was seperated to the ones containing one part.

References
｢日々適当 Shapefileを読んでみる(Wing it everyday: Reading Shapefile)｣
    http://blog.goo.ne.jp/m4g/e/08276f066b3953e07281f2a06f606536

ESRI Shapefile Technical Description
    (English Ed.)   http://www.esrij.com/cgi-bin/wp/wp-content/uploads/documents/shapefile.pdf
    (Japanese Ed.)  http://www.esrij.com/cgi-bin/wp/wp-content/uploads/documents/shapefile_j.pdf

ESRI Shapefile Technical DescriptionPolygon  page 9
    Polygon he following are important notes about Polygon shapes.
        The rings are closed (the first and last vertex of a ring MUST be the same).
"""


def display_shapefile(name, iwidth=500, iheight=500, method=0):
    import shapefile
    from PIL import Image, ImageDraw
    r = shapefile.Reader(name)
    mleft, mbottom, mright, mtop = r.bbox
    # map units
    mwidth = mright - mleft
    mheight = mtop - mbottom
    # scale map units to image units
    hscale = iwidth/mwidth
    vscale = iheight/mheight
    img = Image.new("RGB", (iwidth, iheight), "white")
    draw = ImageDraw.Draw(img)

    shapes = r.shapes()
    for i in range(len(shapes)):
        shape = shapes[i]
        points = shape.points
        parts = shape.parts

        for k in range(len(parts)):
            startnum = parts[k]
            if k < len(parts)-1:
                endnum = parts[k+1]
            else:
                endnum = len(points)

            pixels = []
            for j in range(startnum, endnum):
                x = int(iwidth - ((mright - points[j][0]) * hscale))
                y = int((mtop - points[j][1]) * vscale)
                pixels += [(x, y)]
            if shape.shapeType == shapefile.POLYGON:
                draw.polygon(pixels, outline='black')
            elif shape.shapeType == shapefile.POLYLINE:
                draw.line(pixels, fill='black')
    img.show()

if __name__ == '__main__':
    import sys
    display_shapefile(sys.argv[1], 700, 700)
