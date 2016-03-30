#What It Is
The provided code attempts to allow the user to effectively draw polygons on a .fits image that will then output the vertices of said polygon.  This polygon can be used further to exclude any points within it, assuming you have a set of points that are in conjunction with the .fits image.  For example, one can overplot PSF fits of stars associated with their image and if there are bad stars that need to be exclude by hand one will be able to draw a simple polygon around the bad data and effectively exclude it.

What is supplied here is a means to draw these polygons efficiently and interactively versus the alternative of using an application like DS9 to get vertex coordinates comprising of a polygon.  The aforementioned technique is slow and easily messed up, thus wasting time on testing.  The other supplied functionality is the encapsulation of one of these polygons which is provided with a function to see if a given point (like a PSF star) is within the polygon.

#Directions
**Dependencies**



#Shortcomings



#Features To Work In


