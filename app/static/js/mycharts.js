$(document).ready(function() {
  var dataPointsA = []
  var dataPointsB = []

  $.getJSON("https://api.myjson.com/bins/1fsr6a", function(field) {
    for (var i = 0; i < field.length; i++) {
      dataPointsA.push({
        x: field[i].time,
        y: field[i].xxx
      });
      dataPointsB.push({
        x: field[i].time,
        y: field[i].yyy
      });
    }


    var chart = new CanvasJS.Chart("chartContainer", {
      title: {
        text: "Recent Performance"
      },

      data: [{
        type: "line",
        name: "line1",
        dataPoints: dataPointsA
      }, {
        type: "line",
        name: "line2",
        dataPoints: dataPointsB
      }, ]
    });

    chart.render();
  })
})