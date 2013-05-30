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
Namespace.register("English.Validation");
English.Common.News = function(id){
    this.id = id;
}
English.Common.News.prototype={
    readNews:function(share){
        $.get("/news/read/"+this.id+"/",{"share":share})
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
//验证框架
English.Validation.validation = function(node){
    this.node = node;
    this.msg = ""
}
English.Validation.validation.prototype={
    validate:function(){
        //验证 长度，正则，必须
        //错误出力
        //样式改变
        if (this.lengthV() && this.patternV() && this.requredV() && this.equalTo()){
              this.success();
            return true;
        }else{
               this.fail();
            return false;
        }
    },
    lengthV:function(){
        if(this.node.attr("length")){
            var params = node.attr("length").split(",");
            if (this.node.val().trim().length > (params[0]/1) && this.node.val().trim().length < params[1]/1){
                return true;
            }else{
                this.msg = this.errorMsg.length.replace("[0]",params[0]).replace("[1]",params[1]);
                return false;
            }
        }else{
            return true;
        }
    },
    patternV:function(){
         if(this.node.attr("pattern")){
             var reg = RegExp(this.node.attr("pattern"));
             if (!(reg.test(this.node.val().trim()))) {
                 this.msg = this.errorMsg.pattern;
                 return false;
             } else {
                 return true;
             }
         }else{
             return true;
         }
    },
    requredV:function(){
         if(this.node.attr("required")){
              if(this.node.val().trim().length > 0){
                  return true;
              }else{
                  this.msg = this.errorMsg.requred;
                  return false;
              }
         }else{
             return true;
         }
    },
    equalTo:function(){
        if(this.node.attr("equalTo")){
            var id = this.node.attr("equalTo");
            if (!(this.node.val().trim() == $("#"+id).val().trim())){
                this.msg = this.errorMsg.equalTo;
                return false;
            }else{
                return true;
            }
        }else{
            return true;
        }
    },
    remote:function(){
        if (this.node.attr("remote")){
            var flag = $.get(this.node.attr("remote"),{'name':this.node.val()}, function(data){flag = data});
            if(flag.flag == "ok"){
                return true;
            }else{
                this.msg = this.errorMsg.remote;
                return false;
            }
        }else{
            return true;
        }
    },
    success:function(){
        this.node.parents(".control-group").removeClass("error").addClass("success");
        this.node.next().html("<i class='icon-ok'></i>")
    },
    fail:function(){
        this.node.parents(".control-group").removeClass("success").addClass("error");
        this.node.next().html("<i class='icon-remove'></i>"+this.msg)
    },
    errorMsg:{
        "requred":"必填字段",
        "equalTo":'两者不一致',
        'remote':'该名称已经被占用',
        'pattern':'内容格式错误',
        'length':'内容长度必须在[0]和[1]之间'
    }
}
