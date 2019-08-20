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
    setInterval(getData, 10000);
    initChart1();
    initChart2();
});

function getData(){

      console.log("----getData-------- ")

      $.ajax({
              async:true,
              type:"get",
              contentType : "application/json;charset=UTF-8", //类型必填
              url:"https://eilmol743d.execute-api.us-east-1.amazonaws.com/prod",
              dataType:"json",
              success:function(data){
                   console.log(data);

                   var newData = [];

                   if(data.length == 0 ){
                    return;
                   }

                   var j =0 ;
                   for(i = data.length-1; i>=0 ; i--){
                    newData[j++] = data[i];
                   }


                   vue.itemList = newData ;

              },
              error:function(data){
                  console.log(data.result);
              }
     })

}

