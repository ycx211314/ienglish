function addfavorite() {
    if (document.all)
    {
        window.external.addFavorite('http://127.0.0.1:8000/','收藏夹');
    }
    else if (window.sidebar)
    {
        window.sidebar.addPanel('英语学习网', 'http://127.0.0.1:8000/', "");
    }
}
function login(){
    $('#loginDialog').modal("show");
}