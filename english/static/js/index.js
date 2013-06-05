$(function(){
    $('#loginFm').ajaxForm({
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
//            $('#index_loginForm').resetForm();
//            $("#userInfoDiv").show();
//            $("#loginDiv").hide();
            alert(1)
        }else{

        }
    }else{

    }
}