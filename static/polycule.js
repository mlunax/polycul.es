'use strict';

// set up SVG for D3
var width  = 960,
    height = 500,
    selected_node = null,
    selected_link = null,
    mousedown_link = null,
    mousedown_node = null,
    mouseup_node = null,
    editing = false,
    scale = window.graph.scale || 1;

var svg = d3.select('#panel')
  .attr('oncontextmenu', 'return false;')
  .attr('width', width)
  .attr('height', height)
  .append('g')
  .attr('transform', 'scale(' + scale + ')');

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

d3.select('#zoom #in')
  .on('click', function() {
    scale += 0.2;
    window.graph.scale = scale;
    try {
      writeGraph();
    } catch (e) {
      //
    }
    svg.attr('transform', 'scale(' + scale + ')');
  });
d3.select('#zoom #out')
  .on('click', function() {
    scale -= 0.2;
    window.graph.scale = scale;
    try {
      writeGraph();
    } catch (e) {
      //
    }
    svg.attr('transform', 'scale(' + scale + ')');
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
  if (!drag_line.classed('hidden')) {
    return;
  }
  path.select('line')
    .attr('x1', function(d) { return d.source.x; })
    .attr('y1', function(d) { return d.source.y; })
    .attr('x2', function(d) { return d.target.x; })
    .attr('y2', function(d) { return d.target.y; })
  path.select('.source-text')
    .attr('dx', function(d) { return d.source.x})
    .attr('dy', function(d) { return d.source.y + d.source.r * 2});
  path.select('.target-text')
    .attr('dx', function(d) { return d.target.x})
    .attr('dy', function(d) { return d.target.y + d.target.r * 2});
  path.select('.center-text')
    .attr('dx', function(d) {
        return (d.source.x + ((d.target.x - d.source.x) / 2));
    })
    .attr('dy', function(d) {
        return (d.source.y + ((d.target.y - d.source.y) / 2)) - 10;
    });
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
  pathG.append('text')
    .attr('class', 'center-text meaning hidden');
  pathG.append('text')
    .attr('class', 'source-text meaning hidden');
  pathG.append('text')
    .attr('class', 'target-text meaning hidden');
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
  path.on('mouseover', function(d) {
      d3.select(this).selectAll('.meaning')
        .classed('hidden', false);
    })
    .on('mouseout', function(d) {
      d3.select(this).selectAll('.meaning')
        .classed('hidden', true);
    });

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
  try {
    writeGraph();
  } catch(e) {
    node.call(force.drag);
  }
}

// app starts here
restart();
