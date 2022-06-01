function buildGraphFromInput(N, input) {
    var graph = { vertices: [] };
    
    for (var i = 0; i < N; i++) {
        graph.vertices.push({edges: [], edgeLength: [], visited: false, distance: 0});
    }
    for (var i = 0; i < input.length; i++) {
        var v1 = parseInt(input[i].split(' ')[0]);
        var v2 = parseInt(input[i].split(' ')[1]);
        var l = parseInt(input[i].split(' ')[2]);
        graph.vertices[v1 - 1].edges.push(v2);
        graph.vertices[v2 - 1].edges.push(v1);
        graph.vertices[v1 - 1].edgeLength.push(l);
        graph.vertices[v2 - 1].edgeLength.push(l);
    }
    return graph;
}

function findShortestReach(graph, startNode) {
    var output = [];
    var queue = [];
    graph.vertices[startNode - 1].visited = true;
    queue.push(startNode);

    var item = null;
    while (item = queue.shift()) {
        var vertice = graph.vertices[item - 1];
        for (var i = 0; i < vertice.edges.length; i++) {
            if ((graph.vertices[vertice.edges[i] - 1].distance > (vertice.edgeLength[i] + vertice.distance)) ||
                (graph.vertices[vertice.edges[i] - 1].distance === 0)) {
                if (graph.vertices[vertice.edges[i] - 1].distance !== 0) {
                    queue.push(vertice.edges[i]);
                }
                graph.vertices[vertice.edges[i] - 1].distance = vertice.edgeLength[i] + vertice.distance;
            }
            if (!graph.vertices[vertice.edges[i] - 1].visited) {
                queue.push(vertice.edges[i]);
                graph.vertices[vertice.edges[i] - 1].visited = true;
            }
        }
    }

    for (var i = 0; i < graph.vertices.length; i++) {
        if (!graph.vertices[i].visited) {
            output.push(-1);
        } else if ((i + 1) !== startNode) {
            output.push(graph.vertices[i].distance);
        }
    }

    return output.join(' ');
}

function processData(input) {
    var lines = input.split('\n');
    var T = parseInt(lines[0]);
    var index = 1;
    for (var i = 0; i < T; i++) {
        var N = parseInt(lines[index].split(' ')[0]);
        var M = parseInt(lines[index].split(' ')[1]);
        var graphInput = lines.slice(index + 1, M + index + 1);
        index += M + 1;
        var S = parseInt(lines[index]);
        index += 1;
        var graph = buildGraphFromInput(N, graphInput);
        console.log(findShortestReach(graph, S));
    }  
} 

process.stdin.resume();
process.stdin.setEncoding("ascii");
_input = "";
process.stdin.on("data", function (input) {
    _input += input;
});

process.stdin.on("end", function () {
   processData(_input);
});
