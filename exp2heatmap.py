'''
Script to take gene expression data, calculate distance and make JSON output for display heatmap in D3.js

Usage: exp2heatmap.py yourData > data.js

output data structure:

A 2d array in the same order as the sorted data matrix where each element contains the expression z-score, row index, column index.
The maximum expression z-score 
The minimum expression z-score
The ordered row headers
The column headers

HTML/Javascript with D3.js

Here is the html/javascript code to display the previously generated output (data.js) 
as a heatmap. I added some interactivity where mouse over will reveal the gene name 
and expression values. Code is commented:

'''
open("heatmap.html", 'w').write(\
"""
<html>
   <head>
   <script type="text/javascript" src="d3.v2.js"></script>
   <script type="text/javascript" src="data.js"></script>
   <style>
      body {
         margin: 0px;
         padding: 0px;
         font: 12px Arial;
      }
   </style>
   </head>
   <body>
   <script type="text/javascript">
      //height of each row in the heatmap
      var h = 5;
      //width of each column in the heatmap
      var w = 70;

      //attach a SVG element to the document's body
      var mySVG = d3.select("body")
         .append("svg")
         .attr("width", (w * cols.length) + 400) 
         .attr("height", (h * rows.length + 100))
         .style('position','absolute')
         .style('top',0)
         .style('left',0);

      //define a color scale using the min and max expression values
      var colorScale = d3.scale.linear()
        .domain([minData, 0, maxData])
        .range(["blue", "white", "red"]);

      //generate heatmap rows
      var heatmapRow = mySVG.selectAll(".heatmap")
         .data(data)
         .enter().append("g");

      //generate heatmap columns
      var heatmapRects = heatmapRow
         .selectAll(".rect")
         .data(function(d) {
            return d;
         }).enter().append("svg:rect")
         .attr('width',w)
         .attr('height',h)
         .attr('x', function(d) {
            return (d[2] * w) + 25;
         })
         .attr('y', function(d) {
            return (d[1] * h) + 50;
         })
         .style('fill',function(d) {
            return colorScale(d[0]);
         });

      //label columns
      var columnLabel = mySVG.selectAll(".colLabel")
         .data(cols)
         .enter().append('svg:text')
         .attr('x', function(d,i) {
            return ((i + 0.5) * w) + 25;
         })
         .attr('y', 30)
         .attr('class','label')
         .style('text-anchor','middle')
         .text(function(d) {return d;});

      //expression value label
      var expLab = d3.select("body")
         .append('div')
         .style('height',23)
         .style('position','absolute')
         .style('background','FFE53B')
         .style('opacity',0.8)
         .style('top',0)
         .style('padding',10)
         .style('left',40)
         .style('display','none');

      //heatmap mouse events
      heatmapRow
         .on('mouseover', function(d,i) {
            d3.select(this)
               .attr('stroke-width',1)
               .attr('stroke','black')

            output = '<b>' + rows[i] + '</b><br>';
            for (var j = 0 , count = data[i].length; j < count; j ++ ) {
               output += data[i][j][0] + ", ";
            }
            expLab
               .style('top',(i * h))
               .style('display','block')
               .html(output.substring(0,output.length - 3));
      })
      .on('mouseout', function(d,i) {
         d3.select(this)
            .attr('stroke-width',0)
            .attr('stroke','none')
         expLab
            .style('display','none')
      });
   </script>
   </body>
</html>
""")


import sys, numpy, scipy
import scipy.cluster.hierarchy as hier
import scipy.spatial.distance as dist

#import the data into a native 2d python array
inFile = open(sys.argv[1],'r')
colHeaders = inFile.next().strip().split()[1:]
rowHeaders = []
dataMatrix = []
for line in inFile:
	data = line.strip().split()
	rowHeaders.append(data[0])
	dataMatrix.append([float(x) for x in data[1:]])

#convert native python array into a numpy array
dataMatrix = numpy.array(dataMatrix)

#calculate distance matrix and convert to squareform
distanceMatrix = dist.pdist(dataMatrix)
distanceSquareMatrix = dist.squareform(distanceMatrix)

#calculate linkage matrix
linkageMatrix = hier.linkage(distanceSquareMatrix)

#get the order of the dendrogram leaves
heatmapOrder = hier.leaves_list(linkageMatrix)

#reorder the data matrix and row headers according to leaves
orderedDataMatrix = dataMatrix[heatmapOrder,:]
rowHeaders = numpy.array(rowHeaders)
orderedRowHeaders = rowHeaders[heatmapOrder,:]

#output data for visualization in a browser with javascript/d3.js
matrixOutput = []
row = 0
for rowData in orderedDataMatrix:
	col = 0
	rowOutput = []
	for colData in rowData:
		rowOutput.append([colData, row, col])
		col += 1
	matrixOutput.append(rowOutput)
	row += 1

print 'var maxData = ' + str(numpy.amax(dataMatrix)) + ";"
print 'var minData = ' + str(numpy.amin(dataMatrix)) + ";"
print 'var data = ' + str(matrixOutput) + ";"
print 'var cols = ' + str(colHeaders) + ";"
print 'var rows = ' + str([x for x in orderedRowHeaders]) + ";"
