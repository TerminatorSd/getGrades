/**
 * Created by xsd on 17-8-18.
 */

function getGrades() {

    var info = {};
    var no = document.getElementsByTagName("input")[1].value;
    var psw = document.getElementsByTagName("input")[2].value;
    var csrf = document.getElementsByTagName("input")[0].value;
    info.no = no;
    info.psw = psw;
    info.csrfmiddlewaretoken = csrf;
    console.log(info);
    // window.location.href = "grades.html";

    $.ajax({
        url: '/getGrades/',
        dataType: 'JSON',
        type: 'POST',
        data: info,
        success: function (data) {

            //console.log(data);
            var name = data[0].split('(')[0];
            var str = '<div class="card"><p>姓名：' + name　+'</p><hr>';
            console.log(name);
            for(var item in data) {
                if((parseInt(item) - 15) % 11 == 0) {
                    str += '<p>' + data[item] + '：';
                    // console.log(data[item]);
                }
                if((parseInt(item) - 17) % 11 == 0) {
                    console.log(data[item]);
                    // str += data[item] + '</p><hr>'
                }
            }
            str += '</div>';

            // document.getElementsByClassName("input-info")[0].style.display = "none";
            document.getElementsByClassName("info")[0].innerHTML = str;

            // window.location.href = "grades.html?data=" + encodeURI(JSON.stringify(data));
        },
        fail: function () {
            console.log("fail!");
        }
    });
    // window.location.href = "grades.html";
}

    // function ajax(options) {
    //     options = options || {};
    //     options.type = (options.type || "GET").toUpperCase();
    //     options.dataType = options.dataType || "json";
    //     var params = formatParams(options.data);
    //
    //     //创建 - 非IE6 - 第一步
    //     if (window.XMLHttpRequest) {
    //         var xhr = new XMLHttpRequest();
    //     } else { //IE6及其以下版本浏览器
    //         var xhr = new ActiveXObject('Microsoft.XMLHTTP');
    //     }
    //
    //     //接收 - 第三步
    //     xhr.onreadystatechange = function () {
    //         if (xhr.readyState == 4) {
    //             var status = xhr.status;
    //             if (status >= 200 && status < 300) {
    //                 options.success && options.success(xhr.responseText, xhr.responseXML);
    //             } else {
    //                 options.fail && options.fail(status);
    //             }
    //         }
    //     }
    //
    //     //连接 和 发送 - 第二步
    //     if (options.type == "GET") {
    //
    //         var str = options.url;
    //         if (str.indexOf("?") > 0) {
    //             xhr.open("GET", options.url + "&" + params, true);
    //         } else {
    //             xhr.open("GET", options.url + "?" + params, true);
    //         }
    //
    //         xhr.send(null);
    //     } else if (options.type == "POST") {
    //         xhr.open("POST", options.url, true);
    //         //设置表单提交时的内容类型
    //         xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    //         xhr.send(params);
    //     }
    // }
//设置cookie
function setCookie(name,value,days)
{
	var exp = new Date();
	exp.setTime(exp.getTime() + days*24*60*60*1000);
	document.cookie = name + "="+ escape (value) + ";expires=" + exp.toGMTString();
}


//查找cookie
function getCookie(name)
{
	var arr,reg=new RegExp("(^| )"+name+"=([^;]*)(;|$)");
	if(arr=document.cookie.match(reg))
		return unescape(arr[2]);
	else
		return null;
}