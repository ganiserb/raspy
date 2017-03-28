$( document ).ready(function() {
    console.log( "ready!" );
    // alert("asd");
    var container = document.getElementById('graph');
    var graph = null;

    function updateGraphs() {
        $.getJSON('/get_data', {}, function(data) {
            if (graph) {
                graph.destroy();
            }
            var dataset = new vis.DataSet(data.items);
            var options = {
                drawPoints: {style: 'circle'}
            };
            graph = new vis.Graph2d(container, dataset, options);
        });
    }

    updateGraphs();
    var intervalID = window.setInterval(updateGraphs, 10000);
});