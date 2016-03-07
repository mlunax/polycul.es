'use strict';

// set up SVG for D3
var width  = 960,
    height = 500,
    selected_node = null,
    selected_link = null,
    mousedown_link = null,
    mousedown_node = null,
    mouseup_node = null,
    editing = false;

var svg = d3.select('#graph')
  .append('svg')
  .attr('oncontextmenu', 'return false;')
  .attr('width', width)
  .attr('height', height);

window.graph.links.forEach(function(link) {
  window.graph.nodes.forEach(function(node) {
    if (node.id === link.source.id) {
      link.source = node;
    }
    if (node.id === link.target.id) {
      link.target = node;
    }
  });
});

// init D3 force layout
var force = d3.layout.force()
    .nodes(window.graph.nodes)
    .links(window.graph.links)
    .size([width, height])
    .linkDistance(function(d) { return Math.log(3 / d.strength * 10) * 50; })
    .charge(-500)
    .on('tick', tick)


// line displayed when dragging new nodes
var drag_line = svg.append('line')
  .attr('class', 'link dragline hidden');

// handles to link and node element groups
var path = svg.append('g').selectAll('.link'),
    node = svg.append('g').selectAll('.node');

// update force layout (called automatically each iteration)
function tick() {
  path.select('line')
    .attr('x1', function(d) { return d.source.x; })
    .attr('y1', function(d) { return d.source.y; })
    .attr('x2', function(d) { return d.target.x; })
    .attr('y2', function(d) { return d.target.y; })
  node.attr('transform', function(d) {
    return 'translate(' + d.x + ',' + d.y + ')';
  });
}

// update graph (called when needed)
function restart() {
  // path (link) group
  path = path.data(window.graph.links);

  // update existing links
  path.classed('selected', function(d) { return d === selected_link; });


  // add new links
  var pathG = path.enter()
    .append('g')
    .classed('link', true)
    .classed('selected', function(d) { return d === selected_link; });
  pathG.append('line')
    .attr('x1', function(d) { return d.source.x; })
    .attr('y1', function(d) { return d.source.y; })
    .attr('x2', function(d) { return d.target.x; })
    .attr('y2', function(d) { return d.target.y; })
    .attr('stroke-width', function(d) { return d.strength; })
    .attr('stroke-dasharray', function(d) {
      if (d.dashed) {
        return '' + [d.strength / 1.5, d.strength / 1.5];
      }
    });
  // remove old links
  path.exit().remove();

  path.select('line')
    .attr('stroke-width', function(d) { return d.strength; })
    .attr('stroke-dasharray', function(d) {
      if (d.dashed) {
        return '' + [d.strength / 1.5, d.strength / 1.5];
      }
    });
  path.select('.center-text')
    .text(function(d) { return d.centerText; });
  path.select('.source-text')
    .text(function(d) { return d.sourceText; });
  path.select('.target-text')
    .text(function(d) { return d.targetText; });

  // circle (node) group
  // NB: the function arg is crucial here! nodes are known by id, not by index!
  node = node.data(window.graph.nodes, function(d) { return d.id; });

  // add new nodes
  var nodeG = node.enter()
    .append('g')
    .classed('node', true);

  nodeG.append('circle')
    .attr('class', 'node')
    .attr('r', function(d) { return d.r; })
    .attr('style', function(d) {
      if (d.dashed) {
        return 'fill:#ccc!important';
      }
    })
    .attr('stroke-dasharray', function(d) {
      if (d.dashed) {
        return '' + [d.r / 4, d.r / 4];
      }
    });

  // show node IDs
  nodeG.append('text')
    .attr('x', 0)
    .attr('y', function(d) { return -d.r - 2; })
    .attr('class', 'id')
    .attr('text-anchor', 'middle')
    .text(function(d) { return d.name; });

  node.select('circle')
    .attr('r', function(d) { return d.r; })
    .attr('style', function(d) {
      if (d.dashed) {
        return 'fill:#ccc!important';
      }
    })
    .attr('stroke-dasharray', function(d) {
      if (d.dashed) {
        return '' + [d.r / 4, d.r / 4];
      }
    });

  node.select('.id')
    .attr('y', function(d) { return -d.r - 2; })
    .text(function(d) { return d.name; });

  // remove old nodes
  node.exit().remove();

  // set the graph in motion
  force.start();
  if (d3.select('#graph').classed('build')) {
    try {
      writeGraph();
    } catch(e) {
      console.log(e);
    }
  } else {
    node.call(force.drag);
  }
}

// app starts here
restart();
