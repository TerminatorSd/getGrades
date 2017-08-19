/**
 * Created by xsd on 17-8-18.
 */
window.onload = function () {

    var no = getCookie("no");
    var psw = getCookie("psw");
    var csrf = document.getElementsByTagName("input")[0].value;
    if(no && psw) {
        var info = {};
        document.getElementsByClassName("input-info")[0].style.display = "none";
        document.getElementsByClassName("wait")[0].style.display = "block";

        info.no = no;
        info.psw = psw;
        info.csrfmiddlewaretoken=csrf;

        getGradesInfo(info);
    }
};

function getGrades() {

    var info = {};
    var no = document.getElementsByTagName("input")[1].value;
    var psw = document.getElementsByTagName("input")[2].value;
    var csrf = document.getElementsByTagName("input")[0].value;
    info.no = no;
    info.psw = psw;
    info.csrfmiddlewaretoken = csrf;
    // console.log(info);

    document.getElementsByClassName("input-info")[0].style.display = "none";
    document.getElementsByClassName("wait")[0].style.display = "block";
    getGradesInfo(info);
}


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

//删除Cookie
function delCookie(name)
{
    var exp = new Date();
    exp.setTime(exp.getTime() - 1);
    var cval=getCookie(name);
    if(cval!=null)
        document.cookie= name + "="+cval+";expires="+exp.toGMTString();
}

//获取成绩信息
function getGradesInfo(info) {

    $.ajax({
        url: '/getGrades/',
        dataType: 'JSON',
        type: 'POST',
        data: info,
        success: function (data) {
            setCookie("no", info.no, 7);
            setCookie("psw", info.psw, 7);
            //console.log(data);
            var name = data[0].split('(')[0];
            var str = '<div class="card"><p>姓名：' + name　+'</p><hr>';
            console.log(name);
            for(var item in data) {
                if((parseInt(item) - 15) % 11 === 0) {
                    str += '<p>' + data[item] + '：';
                }
                if((parseInt(item) - 17) % 11 === 0) {
                    str += data[item] + '</p>'
                }
            }
            str += '</div>';

            document.getElementsByClassName("wait")[0].style.display = "none";
            document.getElementsByClassName("info")[0].innerHTML = str;
        },
        fail: function () {
            console.log("fail!");
        }
    });
}