// This file is very messy because I am bad at JS
// But basically it puts graphs in the main pages DOM using d3js
// Graphs are currently hardcoded, I'll get around to changing this at some point...

var margin = {top: 50, right:50, left: 50, bottom:50}
    width = 960 - margin.left - margin.right
    height = 500 - margin.top - margin.bottom

// set the ranges
var x = d3.scaleTime().range([0, width]);
var y = d3.scaleLinear().range([height, 0]);

var valueline = d3.line()
    .x(function(d) { return x(d[0]); })
    .y(function(d) { return y(d[1]); });

var svg = d3.select(".mystery_graph").append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
            .append("g").attr("transform",
               "translate(" + margin.left + "," + margin.top + ")");

var svg_hab = d3.select(".hab_graph").append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
            .append("g").attr("transform",
               "translate(" + margin.left + "," + margin.top + ")");

const http = new XMLHttpRequest();
const url='/plant_data';
http.open("GET", url);
http.send();
http.onreadystatechange=(e)=>{
    if (http.readyState != 4) return;

    //document.getElementById("raw_data").innerHTML = http.responseText;
    var data = JSON.parse(http.responseText)

    // set the ranges
var x = d3.scaleTime().range([0,width]);
var y = d3.scaleLinear().range([height, 0]);

var valueline = d3.line()
    .x(function(d) { return x(Math.round(d[0]*1000)); })
    .y(function(d) { return y(d[1]); });

    x.domain(d3.extent(data, function(d) {return d[0]*1000}));
    y.domain([300,900]);

    svg.append("path").data([data]).attr("class", "line").attr("d", valueline);
    svg.append("g").attr("transform", "translate (0," + height + ")").call(d3.axisBottom(x));
    svg.append("g").call(d3.axisLeft(y));

}

const http2 = new XMLHttpRequest();
const url2='/plant_data/habanero';
http2.open("GET", url2);
http2.send();
http2.onreadystatechange=(e)=>{
    if (http2.readyState != 4) return;

    //document.getElementById("raw_data").innerHTML = http.responseText;
    var data = JSON.parse(http2.responseText)

    // set the ranges
var x = d3.scaleTime().range([0,width]);
var y = d3.scaleLinear().range([height, 0]);

var valueline = d3.line()
    .x(function(d) { return x(Math.round(d[0]*1000)); })
    .y(function(d) { return y(d[1]); });

    x.domain(d3.extent(data, function(d) {return d[0]*1000}));
    y.domain([300,900]);

    svg_hab.append("path").data([data]).attr("class", "habline").attr("d", valueline);
    svg_hab.append("g").attr("transform", "translate (0," + height + ")").call(d3.axisBottom(x));
    svg_hab.append("g").call(d3.axisLeft(y));

}
