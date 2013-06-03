function addfavorite() {
    if (document.all) {
        window.external.addFavorite('http://127.0.0.1:8000/', '收藏夹');
    }
    else if (window.sidebar) {
        window.sidebar.addPanel('英语学习网', 'http://127.0.0.1:8000/', "");
    }
}
$(function () {
    $('#loginFm').ajaxForm({
        beforeSubmit: showRequest,  // pre-submit callback
        success: showResponse  // post-submit callback
    });
});
//验证
function showRequest(formData, jqForm, options) {
    return true;
}
//回调函数
function showResponse(responseText, statusText, xhr, $form) {
    if (statusText == "success") {
        var json = $.evalJSON(responseText);
        if (json && json.flag == "ok") {
            English.index.loginShow(false);
            location.reload();
        } else {

        }
    } else {

    }
}
