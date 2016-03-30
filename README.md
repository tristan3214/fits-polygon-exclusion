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




#Shortcomings



#Features To Work In


