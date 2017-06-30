$( document ).ready(function() {
    console.log( "ready!" );
    // alert("asd");
    var container = document.getElementById('graph');
    var graph = null;
    var days = 7;

    function updateGraphs(days) {
        var url = '/get_data?d=7';
        if (days) {
            url = '/get_data?d=' + days;
        }
        $.getJSON(url, {}, function(data) {
            if (graph) {
                graph.destroy();
            }
            var dataset = new vis.DataSet(data.items);
            var options = {
                drawPoints: false
            };
            graph = new vis.Graph2d(container, dataset, options);
        });
    }

    $('#load-range').click(function () {
        console.log('changed');
        days = $('#days-ago').val();
        updateGraphs(days);
    });

    updateGraphs(days);
});