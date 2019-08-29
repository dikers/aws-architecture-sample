var vue ;
console.log("----init -------- ")
$(function(){

    vue = new Vue({
            el: '#main',
            data:{
                itemList: {}
             }
    })

    getData();
    setInterval(getData, 5000);
    initChart1();
    initChart2();
    initChart3();
    initChart4();
});

function getData(){

      console.log("----getData-------- ")

      $.ajax({
              async:true,
              type:"get",
              contentType : "application/json;charset=UTF-8", //类型必填
              url:"https://87l7yigsmk.execute-api.us-west-2.amazonaws.com/prod",
              //url:"https://eilmol743d.execute-api.us-east-1.amazonaws.com/prod",
              dataType:"json",
              success:function(data){
                   console.log(data);

                   var newData = [];

                   if(data.length == 0 ){
                    return;
                   }

                   var j =0 ;
                   var count = 0;
                   for(i = data.length-1; i>=0&& count< 6 ; i--){
                    newData[j++] = data[i];
                    count ++;
                   }


                   vue.itemList = newData ;

              },
              error:function(data){
                  console.log(data.result);
              }
     })

}




function initChart1(){

      var dom = document.getElementById("chart1");
      var myChart = echarts.init(dom);
      var app = {};
      option = null;
      var data = [
           {name: '沈阳', value: 285},
           {name: '哈尔滨', value: 238},
           {name: '大同', value: 289},
           {name: '白色', value: 341},
           {name: '淄博', value: 242}
      ];
      var geoCoordMap = {
          '沈阳':[123.22,41.48],
          '哈尔滨':[126.42,45.76],
          '大同':[113.19,40.03],
          '白色':[105.07,24.62],
          '淄博':[117.52,36.3],
      };

      var convertData = function (data) {
          var res = [];
          for (var i = 0; i < data.length; i++) {
              var geoCoord = geoCoordMap[data[i].name];
              if (geoCoord) {
                  res.push({
                      name: data[i].name,
                      value: geoCoord.concat(data[i].value)
                  });
              }
          }
          return res;
      };

      option = {
          title: {
              text: '各地区次数统计',
              subtext: ' 示例数据 ',
              sublink: 'https://www.amazonaws.cn',
              left: 'center'
          },
          tooltip : {
              trigger: 'item'
          },
          bmap: {
              center: [112.114129, 35.850339],
              zoom: 5,
              roam: true,
              mapStyle: {
                  styleJson: [{
                      'featureType': 'water',
                      'elementType': 'all',
                      'stylers': {
                          'color': '#d1d1d1'
                      }
                  }, {
                      'featureType': 'land',
                      'elementType': 'all',
                      'stylers': {
                          'color': '#f3f3f3'
                      }
                  }, {
                      'featureType': 'railway',
                      'elementType': 'all',
                      'stylers': {
                          'visibility': 'off'
                      }
                  }, {
                      'featureType': 'highway',
                      'elementType': 'all',
                      'stylers': {
                          'color': '#fdfdfd'
                      }
                  }, {
                      'featureType': 'highway',
                      'elementType': 'labels',
                      'stylers': {
                          'visibility': 'off'
                      }
                  }, {
                      'featureType': 'arterial',
                      'elementType': 'geometry',
                      'stylers': {
                          'color': '#fefefe'
                      }
                  }, {
                      'featureType': 'arterial',
                      'elementType': 'geometry.fill',
                      'stylers': {
                          'color': '#fefefe'
                      }
                  }, {
                      'featureType': 'poi',
                      'elementType': 'all',
                      'stylers': {
                          'visibility': 'off'
                      }
                  }, {
                      'featureType': 'green',
                      'elementType': 'all',
                      'stylers': {
                          'visibility': 'off'
                      }
                  }, {
                      'featureType': 'subway',
                      'elementType': 'all',
                      'stylers': {
                          'visibility': 'off'
                      }
                  }, {
                      'featureType': 'manmade',
                      'elementType': 'all',
                      'stylers': {
                          'color': '#d1d1d1'
                      }
                  }, {
                      'featureType': 'local',
                      'elementType': 'all',
                      'stylers': {
                          'color': '#d1d1d1'
                      }
                  }, {
                      'featureType': 'arterial',
                      'elementType': 'labels',
                      'stylers': {
                          'visibility': 'off'
                      }
                  }, {
                      'featureType': 'boundary',
                      'elementType': 'all',
                      'stylers': {
                          'color': '#fefefe'
                      }
                  }, {
                      'featureType': 'building',
                      'elementType': 'all',
                      'stylers': {
                          'color': '#d1d1d1'
                      }
                  }, {
                      'featureType': 'label',
                      'elementType': 'labels.text.fill',
                      'stylers': {
                          'color': '#999999'
                      }
                  }]
              }
          },
          series : [
              {
                  name: '次数',
                  type: 'scatter',
                  coordinateSystem: 'bmap',
                  data: convertData(data),
                  symbolSize: function (val) {
                      return val[2] / 10;
                  },
                  label: {
                      normal: {
                          formatter: '{b}',
                          position: 'right',
                          show: false
                      },
                      emphasis: {
                          show: true
                      }
                  },
                  itemStyle: {
                      normal: {
                          color: 'purple'
                      }
                  }
              },
              {
                  name: 'Top 5',
                  type: 'effectScatter',
                  coordinateSystem: 'bmap',
                  data: convertData(data.sort(function (a, b) {
                      return b.value - a.value;
                  }).slice(0, 6)),
                  symbolSize: function (val) {
                      return val[2] / 10;
                  },
                  showEffectOn: 'render',
                  rippleEffect: {
                      brushType: 'stroke'
                  },
                  hoverAnimation: true,
                  label: {
                      normal: {
                          formatter: '{b}',
                          position: 'right',
                          show: true
                      }
                  },
                  itemStyle: {
                      normal: {
                          color: 'purple',
                          shadowBlur: 10,
                          shadowColor: '#333'
                      }
                  },
                  zlevel: 1
              }
          ]
      };
      if (option && typeof option === "object") {
          myChart.setOption(option, true);
      }
  }



function initChart2(){
    var myChart = echarts.init(document.getElementById('chart2'));
    option = {
        title : {
            text: '总次数统计',
            subtext: ' '
        },
        tooltip : {
            trigger: 'axis'
        },
        calculable : true,
        xAxis : [
            {
                type : 'category',
                boundaryGap : false,
                data : ['周一','周二','周三','周四','周五','周六','周日']
            }
        ],
        yAxis : [
            {
                type : 'value',
                axisLabel : {
                    formatter: '{value} '
                }
            }
        ],
        series : [
            {
                name:'次数',
                type:'line',
                data:[15, 12, 12, 8, 7, 21, 23],
                markPoint : {
                    data : [
                        {name : '最低', value : -2, xAxis: 1, yAxis: -1}
                    ]
                },
                markLine : {
                    data : [
                        {type : 'average', name : '平均值'}
                    ]
                }
            }
        ]
    };

    myChart.setOption(option);

}






function initChart3(){
    var dom = document.getElementById("chart3");
    var myChart = echarts.init(dom);
    var app = {};
    option = null;
    app.title = '单轴散点图';

    var hours = ['12a', '1a', '2a', '3a', '4a', '5a', '6a',
            '7a', '8a', '9a','10a','11a',
            '12p', '1p', '2p', '3p', '4p', '5p',
            '6p', '7p', '8p', '9p', '10p', '11p'];
    var days = ['周一', '周二', '周三',
            '周四', '周五', '周六', '周日'];

    var data = [[0,0,5],[0,1,1],[0,2,0],[0,3,0],[0,4,0],[0,5,0],[0,6,0],[0,7,0],[0,8,0],[0,9,0],[0,10,0],[0,11,2],[0,12,4],[0,13,1],[0,14,1],[0,15,3],[0,16,4],[0,17,6],[0,18,4],[0,19,4],[0,20,3],[0,21,3],[0,22,2],[0,23,5],[1,0,7],[1,1,0],[1,2,0],[1,3,0],[1,4,0],[1,5,0],[1,6,0],[1,7,0],[1,8,0],[1,9,0],[1,10,5],[1,11,2],[1,12,2],[1,13,6],[1,14,9],[1,15,11],[1,16,6],[1,17,7],[1,18,8],[1,19,12],[1,20,5],[1,21,5],[1,22,7],[1,23,2],[2,0,1],[2,1,1],[2,2,0],[2,3,0],[2,4,0],[2,5,0],[2,6,0],[2,7,0],[2,8,0],[2,9,0],[2,10,3],[2,11,2],[2,12,1],[2,13,9],[2,14,8],[2,15,10],[2,16,6],[2,17,5],[2,18,5],[2,19,5],[2,20,7],[2,21,4],[2,22,2],[2,23,4],[3,0,7],[3,1,3],[3,2,0],[3,3,0],[3,4,0],[3,5,0],[3,6,0],[3,7,0],[3,8,1],[3,9,0],[3,10,5],[3,11,4],[3,12,7],[3,13,14],[3,14,13],[3,15,12],[3,16,9],[3,17,5],[3,18,5],[3,19,10],[3,20,6],[3,21,4],[3,22,4],[3,23,1],[4,0,1],[4,1,3],[4,2,0],[4,3,0],[4,4,0],[4,5,1],[4,6,0],[4,7,0],[4,8,0],[4,9,2],[4,10,4],[4,11,4],[4,12,2],[4,13,4],[4,14,4],[4,15,14],[4,16,12],[4,17,1],[4,18,8],[4,19,5],[4,20,3],[4,21,7],[4,22,3],[4,23,0],[5,0,2],[5,1,1],[5,2,0],[5,3,3],[5,4,0],[5,5,0],[5,6,0],[5,7,0],[5,8,2],[5,9,0],[5,10,4],[5,11,1],[5,12,5],[5,13,10],[5,14,5],[5,15,7],[5,16,11],[5,17,6],[5,18,0],[5,19,5],[5,20,3],[5,21,4],[5,22,2],[5,23,0],[6,0,1],[6,1,0],[6,2,0],[6,3,0],[6,4,0],[6,5,0],[6,6,0],[6,7,0],[6,8,0],[6,9,0],[6,10,1],[6,11,0],[6,12,2],[6,13,1],[6,14,3],[6,15,4],[6,16,0],[6,17,0],[6,18,0],[6,19,0],[6,20,1],[6,21,2],[6,22,2],[6,23,6]];

    option = {
        tooltip: {
            position: 'top'
        },
        title: [],
        singleAxis: [],
        series: []
    };

    echarts.util.each(days, function (day, idx) {
        option.title.push({
            textBaseline: 'middle',
            top: (idx + 0.5) * 100 / 7 + '%',
            text: day
        });
        option.singleAxis.push({
            left: 150,
            type: 'category',
            boundaryGap: false,
            data: hours,
            top: (idx * 100 / 7 + 5) + '%',
            height: (100 / 7 - 10) + '%',
            axisLabel: {
                interval: 2
            }
        });
        option.series.push({
            singleAxisIndex: idx,
            coordinateSystem: 'singleAxis',
            type: 'scatter',
            data: [],
            symbolSize: function (dataItem) {
                return dataItem[1] * 4;
            }
        });
    });

    echarts.util.each(data, function (dataItem) {
        option.series[dataItem[0]].data.push([dataItem[1], dataItem[2]]);
    });;
    if (option && typeof option === "object") {
        myChart.setOption(option, true);
    }

}



function initChart4(){
    var dom = document.getElementById("chart4");
    var myChart = echarts.init(dom);
    option = {
        title: {
            text: '各地区次数统计'
        },
        xAxis: {
            type: 'category',
            data: ['沈阳', '哈尔滨', '大同', '白色', '淄博']
        },
        yAxis: {
            type: 'value'
        },
        series: [{
            data: [20, 40, 30, 20, 19],
            type: 'bar'
        }]
    };

    myChart.setOption(option, true);


}
