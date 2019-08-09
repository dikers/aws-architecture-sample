var vue ;
$(function(){
    vue = new Vue({
            el: '#root_div',
            data:{
                name: 'alice',
                age: 19,
                pictures: []
             },
            methods:{
                send:function(){
                }
            }
    })
    getData()


});





    function getData( ) {


        var params={};
        params.word= 'html world test help help ' ;
        console.log("-------------------------- getData")
        $.ajax({
            async:true,
            type:"post",
            contentType : "application/json;charset=UTF-8", //类型必填
            url:"https://37257els9e.execute-api.us-east-1.amazonaws.com/prod/KinesisDemo",
            data:JSON.stringify(params),    //转json串或不转 配合后端即可
            dataType:"json",
            success:function(data){

                console.log(JSON.stringify(data))
            },
            error:function(data){
                console.log(data.result);
            }
        })
    }


        function getData2( ) {



        var params={};
        params.username="admin"
        params.password="admin123"

            var params="username=admin&password=admin123";
            console.log("---------------------- getData")
            $.ajax({
                async:true,
                type:"post",
                contentType : "application/json;charset=UTF-8", //类型必填
                url:"https://1slc362uw4.execute-api.cn-northwest-1.amazonaws.com.cn/api/login",
                data:JSON.stringify(params),    //转json串或不转 配合后端即可
                dataType:"json",
                success:function(data){

                    console.log(JSON.stringify(data))
                },
                error:function(data){
                    console.log(data.result);
                }
            })
        }


