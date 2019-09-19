fetch("/folder")
  .then(function(response) {
    return response.text();
  })
  .then(function(text) {
    var data = JSON.parse(text);

    var sunburst = echarts.init(document.getElementById("folderStructure"));
    option = {
      tooltip: {
        show: true,
        formatter: function(params) {
          let name = params.data.name;
          let size = (params.data.value * 0.001).toFixed(0);
          return `<div>${name}: ${size}KB</div>`;
        }
      },
      series: {
        type: "sunburst",
        data: data,
        highlightPolicy: "ancestor",
        radius: ["0%", "100%"],
        label: {
          show: true,
          rotate: "radial"
        },
        itemStyle: {
          borderWidth: 2
        },
        sort: null
      }
    };
    sunburst.setOption(option);
  });
