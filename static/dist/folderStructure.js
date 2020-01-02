fetch("/folder")
  .then(function(response) {
    return response.text();
  })
  .then(function(text) {
    var diskData = JSON.parse(text);

    myChart.showLoading();

    var sunburst = echarts.init(document.getElementById("folderStructure"));

    sunburst.setOption(option = {

        title: {
            text: 'Disk Usage',
            left: 'center'
        },

        tooltip: {
            formatter: function (info) {
                var value = info.value;
                var treePathInfo = info.treePathInfo;
                var treePath = [];

                for (var i = 1; i < treePathInfo.length; i++) {
                    treePath.push(treePathInfo[i].name);
                }

                return [
                    '<div class="tooltip-title">' + formatUtil.encodeHTML(treePath.join('/')) + '</div>',
                    'Disk Usage: ' + formatUtil.addCommas((value/1024).toFixed(2)) + ' KB',
                ].join('');
            }
        },

        series: [
            {
                name: 'Project Disk Usage',
                type: 'treemap',
                visibleMin: 100,
                label: {
                    show: true,
                    formatter: '{b}'
                },
                upperLabel: {
                    show: true,
                    height: 22
                },
                itemStyle: {
                    borderColor: '#fff'
                },
                levels: getLevelOption(),
                data: diskData
            }
        ]
    });
  });

function colorMappingChange(value) {
        var levelOption = getLevelOption(value);
        chart.setOption({
            series: [{
                levels: levelOption
            }]
        });
    }

    var formatUtil = echarts.format;

    function getLevelOption() {
        return [
            {
                itemStyle: {
                    borderColor: '#777',
                    borderWidth: 0,
                    gapWidth: 1
                },
                upperLabel: {
                    show: false
                }
            },
            {
                itemStyle: {
                    borderColor: '#555',
                    borderWidth: 5,
                    gapWidth: 1
                },
                emphasis: {
                    itemStyle: {
                        borderColor: '#ddd'
                    }
                }
            },
            {
                colorSaturation: [0.35, 0.5],
                itemStyle: {
                    borderWidth: 3,
                    gapWidth: 1,
                    borderColorSaturation: 0.6
                }
            }
        ];
    }