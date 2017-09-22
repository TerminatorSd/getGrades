/**
 * Created by xsd on 17-9-21.
 */

$().ready(function () {


    $("#post").click(function () {
        $.ajax({
            url:'http://39.108.163.91:5000/android/',
            dataType:'JSON',
            type:'POST',
            data:{
                name:'haha',
                value:'123'
            },
            success:function (data) {
                console.log(data);
            },
            error:function () {
                console.log("error!");
            }
        })
    })
});