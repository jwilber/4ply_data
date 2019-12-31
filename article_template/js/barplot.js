// set the dimensions and margins of the graph
const barMargin = {top: 20, right: 30, bottom: 50, left: 180},
    barWidth = 800 - barMargin.left - barMargin.right,
    barHeight = 500 - barMargin.top - barMargin.bottom;

// append the svg object to the body of the page
let svg = d3.select("#my_dataviz")
  .append("svg")
    .attr("preserveAspectRatio", "xMinYMin meet")
    .attr("viewBox", `0 0 ${(barWidth + barMargin.left + barMargin.right)}
    ${(barHeight + barMargin.top + barMargin.bottom)}`)
  .append("g")
    .attr("transform",
          "translate(" + barMargin.left + "," + barMargin.top + ")");

// Parse the Data
d3.csv("data/top_tricks.csv", function(data) {

  // Add X axis
  let x = d3.scaleLinear()
    .domain([0, 10])
    .range([ 0, barWidth]);

  let xAxis = d3.axisBottom(x).tickSize(0);
  svg.append("g")
    .attr('class', 'x-axis')
    .attr("transform", "translate(0," + barHeight + ")")
    .call(xAxis);

  // Y axis
  let y = d3.scaleBand()
    .range([ 0, barHeight])
    .domain(data.map(function(d) { return d.trick; }))
    .padding(.4);
  svg.append("g")
    .attr('class', 'y-axis')
    .call(d3.axisLeft(y))

  //Bars
  svg.selectAll("myRect")
    .data(data)
    .enter()
    .append("rect")
    .attr("x", x(0) )
    .attr("y", function(d) { return y(d.trick); })
    .attr("width", function(d) { return x(d.count); })
    .attr("height", y.bandwidth() )
    .attr('fill', "#c9a111")
    .style('stroke', '#c9a111')
    .style('stroke-width', 7)

})

// add title
d3.select('svg')
  .append('text')
  .attr('x', (barWidth + barMargin.right) / 2)
  .attr('y', barMargin.top / 1.1)
  .html("Koston Has No 'Standout' Trick")
  .style('font-family', "LeagueGothicRegular")
  .style('font-size', '1.5rem')

// add x-axis
d3.select('svg')
  .append("text")    
  .attr('x', (barWidth + barMargin.right + barMargin.left) / 2)  
  .attr('y', barHeight + barMargin.top + 40)       
  .style("text-anchor", "left")
  .style('font-family', "LeagueGothicRegular")
  .style('font-size', '1.2rem')
  .text("# Occurrences Across All Videos");
