var parsedData

//ajax request for radar chart values
fetch('/radar')
    .then(function (response) {
        return response.text();
    }).then(function (text) {
        //console.log('GET response text:');
        //console.log(text); // Print the greeting as text
        parsedData = JSON.parse(text)
        //console.log(parsedData['usage'])

    // based on prepared DOM, initialize echarts instance
    var radarChart = echarts.init(document.getElementById('radarChart'));

    option = {
        title: {
            text: 'Score'
        },
        tooltip: {},
        //legend: {
        //    data: ['Allocated Budget', 'Actual Spending']
        //},
        radar: {
            // shape: 'circle',
            name: {
                textStyle: {
                    color: '#fff',
                    backgroundColor: '#999',
                    borderRadius: 3,
                    padding: [3, 5]
               }
            },
            indicator: [
               { name: 'Usage', max: 100},
               { name: 'Documentation', max: 100},
               { name: 'Naming', max: 100},
            ]
        },
        series: [{
            name: 'Budget vs spending',
            type: 'radar',
            // areaStyle: {normal: {}},
            itemStyle: {
                normal: {
                    color: 'blue'
                }
            },
            data : [
                {
                    value : [parsedData['usage'], parsedData['naming'], parsedData['documentation']],
                    name : 'Allocated Budget'
                }
            ]
        }]
    };

    // use configuration item and data specified to show chart
    radarChart.setOption(option);
});