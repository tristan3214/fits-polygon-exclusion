#What It Is
The provided code attempts to allow the user to effectively draw polygons on a .fits image that will then output the vertices of said polygon.  This polygon can be used further to exclude any points within it, assuming you have a set of points that are in conjunction with the .fits image.  For example, one can overplot PSF stars  associated with their image and if there are bad stars that need to be exclude by hand one will be able to draw a simple polygon around the bad data and effectively exclude it.

What is supplied here is a means to draw these polygons efficiently and interactively versus the alternative of using an application like DS9 to get vertex coordinates comprising of a polygon.  The aforementioned technique is slow and easily messed up, thus wasting time on testing.  The other supplied functionality is the encapsulation of one of these polygons which is provided with a function to see if a given point (like a PSF star) is within the polygon.

#Directions
**Dependencies**
The above code was made with the following Python libraries:
1. numpy
2. matplotlib
3. astropy
4. wxpython

###Making A Polygon

####Synopsis
There are two ways to make a polygon, by hand or using the supplied GUI to draw one on (note the dependencies for the latter case).  The first thing to consider when making a polygon is to consider the coordinates being used.  The GUI will only output in the image X and Y pixel coords but can be easily transformed to RA and DEC using astropy.

For the purpose of X and Y as well as RA and DEC they are essentially flat against the FITS image making the code compatibale across both types.  However, if you were to generate points to make in a polygon one needs to take care about the coordinates.  For, example generating a circle in RA and DEC versus hand making one requires a transformation.

Skip to "Encapsulating the Polygon" section for details on how to use the work horse of this code.

####Running it
First you need to run MakePolygon.py with `python MakePolygon.py`.  The application will open up with an empty matplotlib figure box, the matplotlib toolbar, a file and edit menu, a contrast slider, and a read-only text box.

####Loading Image
To load a fit/fits/fits.gz image open up the **file** menu and click on **Open Image**.  This will open up a find file dialog where you can search through your directories for the image of choice.  Once selected the image is loaded into the empty matplotlib figure with.  The GUI window can be increased in size and the image will grow with it, but depending on the image size itself you will crop the plot window if shrunken to small.

**NOTE:** Depending on the image size it may take a little while for the image to load.  Testing was done using approximately a 4000x4000 pixel Hubble image with low enough image load time.  Anything too large will likely lead to an indefinite hanging of the application.

####Loading Data
To load a data such as PSF points, you need to feed the application a basic DS9 inspired region file.  This format of this file is as follows:

pointShape  Xcoord  Ycoord  shapeSize (one per point)

Delimiter: One only needs white space between each line parameter and it does not matter how much.

pointShape: This is were you specify your point shape, currently it is not implemented but some shapes that you will be able to use are cirlces, squares, and triangles.

Xcoord: The user specifies the x-coordinate of their point here.

Ycoord: The user specifies the y-coordinate of their point here.

shapeSize: A double that will specify you want your shape.

Following this format the data file must be saved with the extension ".reg".

**Loading in the data:** Once the ".reg" file has been made you can click on the file menu item and choose the *Open Data* option.  This will, like the Open Image option, open a file search dialog.  Open up your specified ".reg" file and it will be plotted atop the fits image in the matplotlib figure window.  Below is an example image of what yours may look like.  If it looks messy don't worry you if you are familiar with the matplotlib toolbar you will be able to zoom in.

Example Data Loading Result:

![alt text](https://github.com/tristan3214/fits-polygon-exclusion/blob/master/data_ex.png)

####Changing Contrast
The slider can be used to change the contrast of the pixels.  It only sets it once the slider has stopped, and more than likely the option it is already set on is close to the most optimal setting.

####Making Polygons
First you will want to use the zoom tool given by the matplotlib toolbar so you can close in on the object that you will be drawing your polygon around.  An example of this would be zooming around a large foreground star or background galaxy that is being fitted with PSF stars.  Once zoomed in you will be holding the ctrl button down while clicking around your object to specify the vertices of your polgyon as you go the polygon will be plotted out along the way.  Once you are satisfied with the polygon simply release the ctrl button and the polygon coordinates will be outputed to the read-only text box for visual confirmation.  Below will be an example image of a completed polygon around a target you would want to exclude points from. 

**IMPORTANT:** Currently the way you draw your polygon you must release ctrl to complete your polygon rather than closing your polygon with another specified point.  For example, if I were to create a box around a target I specify three points with the mouse and then release ctrl to close the polgyon up by connecting to the first point.  This is an unintuitive functionality that will be resolved in the future.

If say you messed up the making of your polygon or you are not satisfied with the results and just want to simply redraw it.  You will have the chance to undo the polygon you made with the undo functionality under the edit menu.  Any undos you do can be redrawn as well with a click of the redo.  However, the moment you start creating a new polygon the redo will be reset.  You will be allowed to effectively undo all the drawn polygons and redo all of them assuming you don't start drawing a new one.

####Saving Polygons
Once you have all your necessary polygons you can go to the file menu and click on *Save Polys* and it will prompt you with a name and desitnation to save in.  This will output all your vertices as x and y delimted by white space for each float.

Example polygon:

![alt text](https://github.com/tristan3214/fits-polygon-exclusion/blob/master/polygon_ex.png)

### Encapsulating The Polygons

The next bit of code is held within **pointCross.py**.  Within it are classes that handle the encapsulation of a polygon given a list of vertices written as tuples of (x, y).

#### Conducting encapsulation
For convenience, one can use the provided method in **pointCross.py** called *getPolygons* that will take a path string to your MakePolygon.py polygon file and will return a list of Polygon objects.  

To encapsulate polygons by yourself just load in the polygon file making each line as a list of vertices written as tuples of (x, y).  To instantiate a Polygon instance simple do the following: `var = pointCross.Polygon(points)`.  This will give you a Polygon object that you can store in a data structure.  The pointCross is there because you will need to import the py file to access the class, that looks like `import pointCross` assuming the py file is in the current directory.

Now say you have some point that has x and y coordinates corresponding to your fits image you can feed the instance function in the polygon to determine whether it is held within the polygon.  This instance function is the "isInside" method.  You will feed this method a point given as a tuple and it will return a boolean value of whether it is containted in the polygon.  A call of this method would look something like the following: `poly.isInside(point)`.  

####Examples
#####Determining if a point resides in a polygon
```python
vertices = [] # will hold tuples representing the x and y coordinates (i.e. (x, y) or (ra, dec))
# Making a 5 x 5 square by adding the vertices of this polygon
vertices.append((0,0)) # Vertex 1
vertices.append((0,5)) # Vertex 2
vertices.append((5,5)) # Vertex 3
vertices.append((5,0)) # Vertex 4

# Make the polygon now that we have made our points.
square = pointCross.Polygon(vertices)

# Define some point, as a tuple of (x, y), that is inside the square.
point = (1, 3)

print(poly.isInside(point))

"""
The above line will return a boolean and so can easily be used in an if statement.  In this case
I print the boolean and it will come out to be True.
"""
```
#####Determining if polygons overlap
```python
# I am going to make two squares this time.
vertices = [] # will hold tuples representing the x and y coordinates (i.e. (x, y) or (ra, dec))

# Making a 5 x 5 square by adding the vertices of this polygon
vertices.append((0,0)) # Vertex 1
vertices.append((0,5)) # Vertex 2
vertices.append((5,5)) # Vertex 3
vertices.append((5,0)) # Vertex 4

# Make the polygon now that we have made our points.
square1 = pointCross.Polygon(vertices)

square2 = pointCross.Polygon([(1,1), (6, 1), (6, -4), (1, -4)])

print(square2.isInsidePolygon(square1))

"""
The above line deconstructs square2 in a set of points and checks if they are inside square1.
"""

```



#### How it works
The algorithm in play to determine whether a point is contained in a polygon is called the even-odd rule.  This is part of a larger problem class known as *point-in-polygon* which has other various algorithms to take on this problem.  However, with the precision fits images give you in x and y coordinates the even-odd rule is plenty effective.

The idea behind it is that we draw a line segment to the right of the point and if it intersects and odd number of times with a polygons edges then it is contained within it, and vice-versa for an even number of collisions.

Here is a more information on the problem space: <https://en.wikipedia.org/wiki/Point_in_polygon>

#Shortcomings
When checking for overlapping polygons if a larger square's edge cuts through a smaller square and you check that the larger one is in the small one, in this case, it will not work.  You have to choose the polygon that you know will be in the other one as the object to call ".isInsidePolygon()".


#Features To Work In
* Undoing polygon vertices as one is in the progress of drawing them.
* Solving the issue of faster image load times, starting with the reduction of precision.
* Add better source code in-line documentation.



