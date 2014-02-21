$(function() {
    var d1 = [
        [0, 10],
        [1, 20],
        [2, 33],
        [3, 24],
        [4, 45],
        [5, 36],
        [6, 47],
        [7, 38],
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
            min:2,

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

$(function () {
// Use Morris.Area instead of Morris.Line
    Morris.Area({
        element: 'graph-area',
        padding: 10,
        behaveLikeLine: true,
        gridEnabled: false,
        gridLineColor: '#dddddd',
        axes: true,
        fillOpacity:.7,
        data: [
            {period: '2010 Q1', iphone: 10, ipad: 10, itouch: 10},
            {period: '2010 Q2', iphone: 1778, ipad: 7294, itouch: 18441},
            {period: '2010 Q3', iphone: 4912, ipad: 12969, itouch: 3501},
            {period: '2010 Q4', iphone: 3767, ipad: 3597, itouch: 5689},
            {period: '2011 Q1', iphone: 6810, ipad: 1914, itouch: 2293},
            {period: '2011 Q2', iphone: 5670, ipad: 4293, itouch: 1881},
            {period: '2011 Q3', iphone: 4820, ipad: 3795, itouch: 1588},
            {period: '2011 Q4', iphone: 25073, ipad: 5967, itouch: 5175},
            {period: '2012 Q1', iphone: 10687, ipad: 34460, itouch: 22028},
            {period: '2012 Q2', iphone: 1000, ipad: 5713, itouch: 1791}


        ],
        lineColors:['#ED5D5D','#D6D23A','#32D2C9'],
        xkey: 'period',
        ykeys: ['iphone', 'ipad', 'itouch'],
        labels: ['iPhone', 'iPad', 'iPod Touch'],
        pointSize: 0,
        lineWidth: 0,
        hideHover: 'auto'

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

