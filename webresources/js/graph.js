let svg;
let simulation;

$(document).ready(function() {
    const container = $('#graph-container');
    const width = container.width();
    const height = container.height();
    const graphData = JSON.parse($("#graph_data_json").html());

    svg = d3.select('#graph-container').append('svg')
        .attr('width', width)
        .attr('height', height);

    const arrowhead = svg.append('defs')
        .append('marker')
        .attr('id', 'arrowhead')
        .attr('markerWidth', 6)   // Adjust as needed
        .attr('markerHeight', 6)  // Adjust as needed
        .attr('refX', 7.5)          // Adjust as needed (half of markerWidth)
        .attr('refY', 3)          // Adjust as needed (half of markerHeight)
        .attr('orient', 'auto');

    arrowhead.append('line')
        .attr('x1', 0)
        .attr('y1', 0)
        .attr('x2', 4)            // Adjust as needed (markerWidth)
        .attr('y2', 3);           // Adjust as needed (half of markerHeight)

    arrowhead.append('line')
        .attr('x1', 0)
        .attr('y1', 6)            // Adjust as needed (markerHeight)
        .attr('x2', 4)            // Adjust as needed (markerWidth)
        .attr('y2', 3);           // Adjust as needed (half of markerHeight)

    const arrowhead2 = svg.append('defs')
        .append('marker')
        .attr('id', 'arrowhead2')
        .attr('markerWidth', 6)   // Adjust as needed
        .attr('markerHeight', 6)  // Adjust as needed
        .attr('refX', 8)          // Adjust as needed (half of markerWidth)
        .attr('refY', 3)          // Adjust as needed (half of markerHeight)
        .attr('orient', 'auto');

    arrowhead2.append('line')
        .attr('x1', 0)
        .attr('y1', 0)
        .attr('x2', 4)            // Adjust as needed (markerWidth)
        .attr('y2', 3);           // Adjust as needed (half of markerHeight)

    arrowhead2.append('line')
        .attr('x1', 0)
        .attr('y1', 6)            // Adjust as needed (markerHeight)
        .attr('x2', 4)            // Adjust as needed (markerWidth)
        .attr('y2', 3);           // Adjust as needed (half of markerHeight)

    const nodes = graphData.nodes;
    const links = graphData.links;

    const link = svg.selectAll('.link')
        .data(links)
        .enter().append('line')
        .attr('id', d => d.id)
        .attr('class', d => 'link ' + d.type)
        .attr('marker-end', d => 'url(#arrowhead'+ d.arrowhead + ')');

    const node = svg.selectAll('.node')
        .data(nodes)
        .enter().append('g')  // Create a group element for each node
        .attr('class', 'node-group')
        .attr('transform', d => `translate(${d.x || 0}, ${d.y || 0})`);

    node.append('circle')
        .attr('class', 'node')
        .attr('r', 10);

    node.append('text')
        .attr('class', 'node-text')
        .attr('dx', 15)
        .attr('dy', -15)
        .text(d => d.key);

    simulation = d3.forceSimulation(nodes)
        .force('link', d3.forceLink(links).id(d => d.id).distance(100))
        .force('charge', d3.forceManyBody().strength(-50))
        .force('center', d3.forceCenter(width/2, height/2))
        .force('collide', d3.forceCollide().strength(1).radius(10).iterations(20));

    simulation.on('tick', () => {
        link.attr('x1', d => d.source.x)
            .attr('y1', d => d.source.y)
            .attr('x2', d => d.target.x)
            .attr('y2', d => d.target.y);

        node.attr('transform', d => `translate(${d.x},${d.y})`);
        node.attr('cx', d => d.x)
            .attr('cy', d => d.y)
            .attr('data-toggle', 'tooltip')
            .attr('data-placement', 'top')
            .attr('data-html', true)
            .attr('title', d => d.name)
            .attr('class', d => "node " + d.type + " " + d.main)
            .on('mouseover', function () {
                $(this).tooltip('show');
            })
            .on('mouseout', function () {
                $(this).tooltip('hide');
            })
            .on('click', function(d) {
                let data = d3.select(this).datum();
                window.location.href = data.url;
            });
    });
});

$(window).resize(function() {
    const container = $('#graph-container');
    const width = container.width();
    const height = container.height();
    svg.attr('width', width*.8)
       .attr('height', height);
    simulation.force('center', d3.forceCenter(width/2, height/2)).alpha(1).restart();
});
