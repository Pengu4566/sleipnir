// based on prepared DOM, initialize echarts instance
var myChart = echarts.init(document.getElementById("projectStructure"));

myChart.title = "Project Structure";
myChart.showLoading();
$(document).ready(function() {
  //$.get('dist/project_structure_graph.gexf', function (xml) {

  //ajax request for radar chart values
  fetch("/structure")
    .then(function(response) {
      return response.text();
    })
    .then(function(text) {
      parsedData = JSON.parse(text);
      if (parsedData["gexf"] != null) {
        myChart.hideLoading();
        // console.log(parsedData["gexf"]);
        var graph = echarts.dataTool.gexf.parse(parsedData["gexf"]);

        //var graph = echarts.dataTool.gexf.parse(xml);
        var categories = [];

        graph.nodes.forEach(function(node) {
          node.itemStyle = null;
          node.symbolSize = 10;
          node.value = node.symbolSize;
          //node.category = node.attributes.modularity_class;
          // Use random x, ylabel
          node.x = node.y = null;
          node.draggable = true;
          node.color = "blue";
        });

        option = {
          title: {
            // Workflow Invocation Network
            text: "",
            subtext: "",
            top: "top",
            left: "center"
          },
          tooltip: {},
          legend: [
            {
              // selectedMode: 'single',
              data: categories.map(function(a) {
                node;
                return a.name;
              })
            }
          ],
          animation: true,
          series: [
            {
              name: "Node",
              type: "graph",
              layout: "force",
              data: graph.nodes,
              itemStyle: {
                normal: {
                  color: "blue"
                }
              },
              links: graph.links,
              edgeSymbol: ["", "arrow"],
              edgeSymbolSize: 10,
              zoom: 1,
              categories: categories,
              roam: true,
              label: {
                normal: {
                  position: "right",
                  show: "true",
                  color: "grey"
                }
              },
              force: {
                repulsion: 100
              }
            }
          ]
        };
        myChart.setOption(option);
      }
      //}, 'xml');}
      else {
        myChart.hideLoading();
        option = {
          title: {
            text: "",
            subtext:
              "There is no invoking relationship in the project you uploaded.",
            top: "top",
            left: "left"
          }
        };
        myChart.setOption(option);
      }
    });
});
//});
