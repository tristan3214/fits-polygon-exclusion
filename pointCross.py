class Polygon():
	"""
	Make some polygon with edges and vertices.
	"""
	def __init__(self, points):
		"""
		Takes in list of tuple points specifying each vertex.
		"""

		## Build polygon rith a list of edges
		self.edges = []
		for i in range(len(points)):
			if(i < (len(points) - 1)):
				# construct with the vertices of i to len - 2
				vi = Vertex(points[i][0], points[i][1])
				vj = Vertex(points[i+1][0], points[i+1][1])
				e_current = Edge(vi, vj)
				self.edges.append(e_current)
			else:
				# construct last vertex that connects back to beginning
				vi = Vertex(points[i][0], points[i][1])
				vj = Vertex(points[0][0], points[0][1])
				e_current = Edge(vi, vj)
				self.edges.append(e_current)


	def isInside(self, P):
		"""
		Takes in a tuple P and sees if this point is inside the instance of polygon.
		"""
		P = Vertex(P[0], P[1])
		collisions = 0
		for e in self.edges:
			if(((e.getStartPoint().y <= P.y) and (e.getEndPoint().y > P.y)) or ((e.getStartPoint().y > P.y) and (e.getEndPoint().y <= P.y))):
				vt = 1.0 * (P.y - e.getStartPoint().y) / (e.getEndPoint().y - e.getStartPoint().y)
				if(P.x < e.getStartPoint().x + vt * (e.getEndPoint().x - e.getStartPoint().x)):
					collisions += 1

		if collisions % 2 == 1:
			return True
		else:
			return False

        def isInsidePolygon(self, poly):
                # get list of this polygon's vertices.
                vertices = []
                for e in self.edges:
                        vertices.append(e.vi)

                for v in vertices: # if any vertex is in the other polygon then they are overlapping
                        if poly.isInside((v.x, v.y)):
                                return True
                return False

	def getSize(self):
		return len(self.edges)


	def toString(self):
		string = ""
		for e in self.edges:
			string += (e.toString() + "\n")
 		return string



class Edge():
	"""
	Consruct an edge from two vertices vi, vj.
	"""
	def __init__(self, vi, vj):
		self.vi = vi
		self.vj = vj

	def getStartPoint(self):
		return self.vi


	def getEndPoint(self):
		return self.vj

	def toString(self):
		return "Edge from " + self.vi.toString() + " to " + self.vj.toString() + "."





class Vertex():
	"""
	Construct a vertex out of x and y coordinates
	"""
	def __init__(self, x, y):
		self.x = float(x)
		self.y = float(y)

	def toString(self):
		return "(" + str(self.x) + ", " + str(self.y) + ")"


# convenience function of getting the polygons from the standard file format outputted by the application MakePolygon
def getPolygons(fileName):
        polygons = []
        f = open(fileName, "r")
        for line in f:
                # line is split by white space and coordinates are in order of x y x y etc...
                line = line.split()
                points = []
                for xy in range(0, len(line), 2):
                        points.append((float(line[xy]), float(line[xy + 1])))
                polygons.append(Polygon(points))
        return polygons

def inPolygons(polygons, X, Y):
        for poly in polygons:
                if poly.isInside((X,Y)):
                        return True
                
        return False

def decDecimalDegrees(dec):
    """
    Takes in a declination in the standard format of Dec coordinate (deg:arcmin:arcsec.XX)
    """
    dec = dec.split(":")
    decimal = 0
    if (float(dec[0]) > 0):
        decimal = float(dec[0]) + float(dec[1])/60.0 + float(dec[2])/3600.0
    else:
        decimal = float(dec[0]) - float(dec[1])/60.0 - float(dec[2])/3600.0

    return decimal

def raDecimalDegrees(ra):
    """
    Takes in an RA in the standard format of an RA coordinate (hour:min:sec.XX).
    This is then converted to decimal degrees (15 deg / hour).
    """
    ra = ra.split(":")
    return 15.0 * (float(ra[0]) + float(ra[1])/60.0 + float(ra[2])/3600.0)






