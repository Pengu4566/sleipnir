var treeMap = echarts.init(document.getElementById("fileTreeMap"));


treeMap.showLoading();



//ajax request for radar chart values
fetch("/file_tree_map")
  .then(function(response) {
    return response.text();
  })
  //perform a task with the returned data
  .then(function(diskData) {

    treeMap.showLoading();

    $.get('dist/disk.tree.json', function (diskData) {
        treeMap.hideLoading();

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
                        normal: {
                            borderColor: '#777',
                            borderWidth: 0,
                            gapWidth: 1
                        }
                    },
                    upperLabel: {
                        normal: {
                            show: false
                        }
                    }
                },
                {
                    itemStyle: {
                        normal: {
                            borderColor: '#555',
                            borderWidth: 5,
                            gapWidth: 1
                        },
                        emphasis: {
                            borderColor: '#ddd'
                        }
                    }
                },
                {
                    colorSaturation: [0.35, 0.5],
                    itemStyle: {
                        normal: {
                            borderWidth: 5,
                            gapWidth: 1,
                            borderColorSaturation: 0.6
                        }
                    }
                }
            ];
        }

        treeMap.setOption(option = {

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
                        'Disk Usage: ' + formatUtil.addCommas(value) + ' KB',
                    ].join('');
                }
            },

            series: [
                {
                    name:'Disk Usage',
                    type:'treemap',
                    visibleMin: 300,
                    label: {
                        show: true,
                        formatter: '{b}'
                    },
                    upperLabel: {
                        normal: {
                            show: true,
                            height: 30
                        }
                    },
                    itemStyle: {
                        normal: {
                            borderColor: '#fff'
                        }
                    },
                    levels: getLevelOption(),
                    data: diskData
                }
            ]
        });
    });
});
