$(function() {
    var d1 = [
        [0, 55],
        [1, 20],
        [2, 21],
        [3, 24],
        [4, 12],
        [5, 36],
        [6, 47],
        [7, 8],
        [8, 21],
        [9, 33],
        [10, 21]

    ];
    var data = ([{
        label: "Too",
        data: d1,
        lines: {
            show: true,
            fill: true,
            lineWidth:2,
            fillColor: {
                colors: [ "rgba(255,255,255,.1)","rgba(160,220,220,.8)"]
            }
        }
    }
    ]);
    var options = {
        grid: {
            backgroundColor: { colors: [ "#fff", "#fff" ] },
            borderWidth:0,borderColor:"#f0f0f0",
            margin:0,
            minBorderMargin:0,
            labelMargin:20,
            hoverable: true,
            clickable: true
        },
// Tooltip
        tooltip: true,
        tooltipOpts: {
            content: "%s X: %x Y: %y",
            shifts: {
                x: -60,
                y: 25
            },
            defaultTheme: false
        },

        legend: {
            labelBoxBorderColor: "#ccc",
            show: false,
            noColumns: 0
        },
        series: {
            stack: true,
            shadowSize: 0,
            highlightColor: 'rgba(30,120,120,.5)'

        },
        xaxis: {
            tickLength: 0,
            tickDecimals: 0,
            show:true,
            min:0,

            font :{

                style: "normal",


                color: "#666666"
            }
        },
        yaxis: {
            ticks: 3,
            tickDecimals: 0,
            show:true,
            tickColor: "#f0f0f0",
            font :{

                style: "normal",


                color: "#666666"
            }
        },
//        lines: {
//            show: true,
//            fill: true
//
//        },
        points: {
            show: true,
            radius: 2,
            symbol: "circle"
        },
        colors: ["#87cfcb", "#48a9a7"]
    };
    var plot = $.plot($("#daily-visit-chart"), data, options);
});

$(function() {

    var dataPie = [
        { label: "TV",  data: 50},
        { label: "Washing machine",  data: 50},
        { label: "Fridge",  data: 100},
        { label: "Fan",  data: 10},
        { label: "AC",  data: 100},
    ];
// DONUT
    $.plot($(".sm-pie"), dataPie,
        {
            series: {
                pie: {
                    innerRadius: 0.7,
                    show: true,
                    stroke: {
                        width: 0.1,
                        color: '#ffffff'
                    }
                }
            },

            legend: {
                show: true
            },
            grid: {
                hoverable: true,
                clickable: true
            },

            colors: ["#ffdf7c", "#b2def7", "#efb3e6"]
        });
});

/*Knob*/
var opts = {
    lines: 12, // The number of lines to draw
    angle: 0, // The length of each line
    lineWidth: 0.48, // The line thickness
    pointer: {
        length: 0.6, // The radius of the inner circle
        strokeWidth: 0.03, // The rotation offset
        color: '#464646' // Fill color
    },
    limitMax: 'true', // If true, the pointer will not go past the end of the gauge
    colorStart: '#fa8564', // Colors
    colorStop: '#fa8564', // just experiment with them
    strokeColor: '#F1F1F1', // to see which ones work best for you
    generateGradient: true
};
var target = document.getElementById('gauge'); // your canvas element
var gauge = new Gauge(target).setOptions(opts); // create sexy gauge!
gauge.maxValue = 3000; // set max gauge value
gauge.animationSpeed = 32; // set animation speed (32 is default value)
gauge.set(1150); // set actual value
gauge.setTextField(document.getElementById("gauge-textfield"));

