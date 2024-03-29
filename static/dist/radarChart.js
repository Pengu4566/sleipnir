var parsedData;

//ajax request for radar chart values
fetch("/radar")
  .then(function(response) {
    return response.text();
  })
  .then(function(text) {
    //console.log('GET response text:');
    //console.log(text); // Print the greeting as text
    parsedData = JSON.parse(text);
    //console.log(parsedData['usage'])

    // based on prepared DOM, initialize echarts instance
    var radarChart = echarts.init(document.getElementById("radarChart"));

    option = {
      title: {
        text: "",
        subtext: "",
        top: "top",
        left: "center"
      },
      tooltip: {},
      // legend: {
      //   data: ["Actual Score", "Tolerance"]
      // },
      radar: {
        // shape: 'circle',
        name: {
          textStyle: {
            color: "#fff",
            backgroundColor: "#999",
            borderRadius: 3,
            padding: [3, 5]
          }
        },
        indicator: [
          { name: "Usage", max: 100 },
          { name: "Documentation", max: 100 },
          { name: "Naming", max: 100 }
        ]
      },
      series: [
        {
          name: "Score",
          type: "radar",
          // areaStyle: {normal: {}},
          itemStyle: {
            normal: {
              color: "rgb(233,97,111)"
            }
          },
          data: [
            {
              value: [
                parsedData["usage"],
                parsedData["documentation"],
                parsedData["naming"]
              ],
              name: "Score"
            }
          ]
        }
      ]
    };

    // use configuration item and data specified to show chart
    radarChart.setOption(option);
  });
