$(function(){
    $('#loginFm').ajaxForm({
        beforeSubmit:  showRequest,  // pre-submit callback
        success:       showResponse  // post-submit callback
    });
    if(WB2.checkLogin()){
       // $('#notloginlog').hide();
       // $('#notloginreg').hide();
        $('#wblog').show();
    }else{
        $('#notloginlog').show();
        $('#notloginreg').show();
       // $('#wblog').hide();
    }
});
//验证
function showRequest(formData, jqForm, options) {

    return true;
}
//回调函数
function showResponse(responseText, statusText, xhr, $form)  {
    if(statusText == "success"){
        var json = $.evalJSON(responseText);
        if(json && json.flag == "ok"){
//            $('#index_loginForm').resetForm();
//            $("#userInfoDiv").show();
//            $("#loginDiv").hide();
            location=this.location;
            English.index.loginShow(false);

        }else{

        }
    }else{

    }
}
function isLogin(flag){
    if(flag){
        $("#userInfoDiv").show();
        $("#loginDiv").hide();
    }else{
        $("#userInfoDiv").hide();
        $("#loginDiv").show();
    }
}
function logout(){
    $.ajax({
        url:'/user/logout/',
        type:'GET',
        dataType:"json",
        success:function(data){
             if(data.flag){
                 isLogin(false);
             }
        }
    });
    isLogin(false);

}

function wbdl(){
    var uid;
    var nickName;
    var photo;
    WB2.anyWhere(function(W){
        W.parseCMD("/oauth2/get_token_info",function(sResult, bStatus){
            uid = sResult.uid;
            WB2.anyWhere(function(W){
                W.parseCMD("/users/show.json",function(rs, bStatus){
                    nickName= rs.screen_name;
                    photo=rs.avatar_large;
                    $.ajax({
                        url:'/user/wblogin/',
                        type:'post',
                        data:'uid='+uid+'&photo='+photo+'&nickName='+nickName+'&csrfmiddlewaretoken='+English.Common.cookieTool.getCsrftoken(),
                        success:function(value){
                            location='/index/'
                        },
                        error:function(){
                            alert('出问题了!!');
                        }
                    });
                },{
                    uid:uid
                },{
                    method : 'get'
                });
            });
        },{
            method : 'post'
        });
    });



    English.index.loginShow(false);
}
/**
function wblogin(o){
    //alert(o.screen_name);
   // location=this.location;
}
function wblogout(){
    location.reload();
}

WB2.anyWhere(function(W){
    W.widget.connectButton({
        id: "wb_connect_btn",
        type: '3,2',
        callback : {
            login:function(o){
                alert(o.screen_name)
            },
            logout:function(){
                alert('logout');
            }
        }
    });
});
 */