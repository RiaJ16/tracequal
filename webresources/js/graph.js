let svg;
let simulation;

$(document).ready(function() {
    const container = $('#graph-container');
    const width = container.width();
    const height = container.height();
    const graphData = JSON.parse($("#graph_data_json").html());
    const typeOrder = ['user_story','requirement','design','code','test']; // <- match your d.type
    const rank = Object.fromEntries(typeOrder.map((t,i)=>[t,i]));

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

    const viewport = svg.append('g').attr('class','viewport');

    const link = viewport.append('g').attr('class','links').selectAll('path')
        .data(links)
        .enter().append('path')
        .attr('id', d => d.id)
        .attr('class', d => 'link ' + d.type)
        .attr('fill', 'none')
        .attr('stroke', '#3b6ea5')
        .attr('stroke-width', 1.4)
        .attr('marker-end', d => 'url(#arrowhead' + d.arrowhead + ')');

    function shrinkSegment(sx, sy, tx, ty, r1 = 0, r2 = 0, arrowPad = 0) {
        const dx = tx - sx, dy = ty - sy;
        const L = Math.hypot(dx, dy) || 1;
        const ux = dx / L, uy = dy / L;
        return {
            sx: sx + ux * r1,
            sy: sy + uy * r1,
            tx: tx - ux * (r2 + arrowPad),
            ty: ty - uy * (r2 + arrowPad)
        };
    }

    function curvedPath(d) {
        const s = d.source, t = d.target;
        const { sx, sy, tx, ty } = shrinkSegment(s.x, s.y, t.x, t.y);
        const dx = tx - sx, dy = ty - sy;
        const dr = Math.hypot(dx, dy) * 0.30;
        return `M${sx},${sy}C${sx + dr},${sy},${tx - dr},${ty},${tx},${ty}`;
    }

    const node = viewport.append('g').attr('class','nodes').selectAll('g')
        .data(nodes)
        .enter().append('g')  // Create a group element for each node
        .attr('class', 'node-group')
        .attr('transform', d => `translate(${d.x || 0}, ${d.y || 0})`);

    // 3) add zoom/pan
    const zoom = d3.zoom()
        .scaleExtent([0.3, 3])               // min/max zoom
        .on('zoom', (ev) => viewport.attr('transform', ev.transform));

    svg.call(zoom);

    const byType = d3.group(nodes, d => d.type);

    /*for (const [type, arr] of byType) { // Sorting de los nodos
        arr.sort((a,b) => d3.ascending(a.key, b.key));
        arr.forEach((n,i) => n._lane = i);
    }*/

    function buildYTargets(h){
        const targets = new Map();
        for (const [type, arr] of byType) {
            const padding = 30;
            const spacing = Math.min(90, (h - padding*2) / (arr.length + 1));
            const start = padding + spacing;
            arr.forEach((n,i) => targets.set(n.id, start + i*spacing));
        }
        return targets;
    }
    let yTargets = buildYTargets(height);

    node.append('circle')
        .attr('class', 'node')
        .attr('r', 10);

    node.append('text')
        .attr('class', 'node-text')
        .attr('dx', 15)
        .attr('dy', -15)
        .text(d => d.key);

    const xForType = t => (rank[t] + 0.5) * (width / typeOrder.length);

    simulation = d3.forceSimulation(nodes)
        .force('link', d3.forceLink(links).id(d => d.id).distance(100))
        .force('charge', d3.forceManyBody().strength(-120))
        .force('collide', d3.forceCollide().strength(1).radius(10).iterations(20))
        .force('x', d3.forceX(d => xForType(d.type)).strength(0.35)) // columns
        .force('y', d3.forceY(d => yTargets.get(d.id)).strength(0.25));

    simulation.on('tick', () => {
        link.attr('d', curvedPath);

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
