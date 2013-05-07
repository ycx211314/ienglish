$(function(){
    $('#index_loginForm').ajaxForm({
        beforeSubmit:  showRequest,  // pre-submit callback
        success:       showResponse  // post-submit callback
    });
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
            $('#index_loginForm').resetForm();
            $("#userInfoDiv").show();
            $("#loginDiv").hide();
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
}