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
                sendMessage:function(){
                    _sendMessage();
                }
            }
    })

});


function _sendMessage(){

    var value = $("#content_text_id").val()

    params = {}


    if(value == null || value.trim() == ""){
    console.log(" value is null --------- " )
        return
    }
    var value = value.trim();

    var wordList = value.split(" ")
    var newWordList = new Array();
    var j =0 ;

    for(i=0; i< wordList.length; i++){

        if(wordList[i] !="" && wordList[i].trim().length > 2){
            newWordList[j++] = wordList[i].trim()
        }

    }

    result = "";
    for(j=0; j< newWordList.length; j++ ){
        result += newWordList[j]
        if(j!=newWordList.length -1){
            result+=" "
        }
    }
    console.log("newMessage --------- ["+result+"]")
    params.word= result;
    console.log("sendMessage --------- ", params)
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


