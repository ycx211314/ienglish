Namespace = new Object();
Namespace.register = function(fullNS)
{
    var nsArray = fullNS.split('.');
    var sEval = "";
    var sNS = "";
    for (var i = 0; i < nsArray.length; i++)
    {
        if (i != 0) sNS += ".";
        sNS += nsArray[i];
        // 依次创建构造命名空间对象（假如不存在的话）的语句
        sEval += "if (typeof(" + sNS + ") == 'undefined') " + sNS + " = new Object();"
    }
    if (sEval != "") eval(sEval);
}
Namespace.register("English.Common");
English.Common.News = function(id){
    this.id = id;
}
English.Common.News.prototype={
    readNews:function(){
        $.get("/news/read/"+this.id+"/")
    }
}
Namespace.register("English.index");
English.index.loginShow=function(flag){
    if(flag){
        $('#loginDialog').modal("show");
    }else{
        $('#loginDialog').modal("hide");
    }
}
English.index.loginOut=function(){
    $.get("/user/logout/",{},function(){
        location.reload()
    })
}
