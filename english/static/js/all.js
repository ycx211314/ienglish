String.prototype.trim = function () {
    return this .replace(/^\s\s*/, '' ).replace(/\s\s*$/, '' );
}
Namespace = new Object();
Namespace.register = function (fullNS) {
    var nsArray = fullNS.split('.');
    var sEval = "";
    var sNS = "";
    for (var i = 0; i < nsArray.length; i++) {
        if (i != 0) sNS += ".";
        sNS += nsArray[i];
        // 依次创建构造命名空间对象（假如不存在的话）的语句
        sEval += "if (typeof(" + sNS + ") == 'undefined') " + sNS + " = new Object();"
    }
    if (sEval != "") eval(sEval);
}
Namespace.register("English.Common");
Namespace.register("English.Validation");
/*********************************************************cookie处理 *******************************/
English.Common.cookieTool = {
    getCookie: function (name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie
                        .substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    },
    getCsrftoken: function () {
        return this.getCookie("csrftoken");
    }
}
/***************************************************************************新闻相关js*****************************************************/
/**
 * 新闻相关处理js
 * @param id
 * @constructor
 */
English.Common.News = function (id) {
    this.id = id;
    this.readUrl = "/news/read/" + this.id + "/"
    this.commentUrl = "/news/comment/add/";
    this.agreeUrl = "/news/comment/agree/"
}
English.Common.News.prototype = {
    newsDetailInit: function (newId) {
        $(".english,.englishCH").css("cursor", "pointer")
        $(".english,.englishCH").tooltip({
            placement: "top",
            trigger: "click",
            html: true,
            title: function () {
                if ($(this).hasClass("english")) {
                    return $(this).next().html()
                } else {
                    return $(this).prev().html()
                }
            }
        });
        setTimeout(function () {
            var news = new English.Common.News(newId);
            var share = 0;
            if ($("#").html() != $(".shareCount")[0].innerHTML) {
                share = $(".shareCount")[0].innerHTML / 1;
            }
            news.readNews(share)
        }, 3000);
        $(".translate").bind("click", function () {
            switch ($(this).attr("data-target")) {
                case "CH":
                    $(".englishCH").show();
                    $(".english").hide();
                    break;
                case "EN":
                    $(".englishCH").hide();
                    $(".english").show();
                    break;
                case "CE":
                    $(".englishCH").show();
                    $(".english").show();
                    $(".english").tooltip("hide");
                    break;
                default:
                    break
            }
        });
    },
    readNews: function (share) {
        $.get(this.readUrl + "?share=" + share)
    },
    addComment: function (formId,ip,ipcname) {
        formData = $("#"+formId).serialize()+"&ip="+ip+"&ipname="+ipcname+"&csrfmiddlewaretoken=" + English.Common.cookieTool.getCsrftoken();
        $.ajax({
            url: this.commentUrl,
            type: 'post',
            data: formData,
            dataType: 'json',
            success: function (data) {
                if (data.flag == "ok") {
                    $("#"+formId+" textarea").val("");
                    $("#commentCount").html(($("#commentCount").html()/1+1));
                    $("#sendInfo").html("发表成功")
                } else{
                    $("#sendInfo").html("发表失败")
                }
            }

        })
    },
    agreeWithComment:function(comId){
        $.get(this.agreeUrl+"up/",{"comId":comId});
    },
    noAgreeWithComment:function(comId){
        $.get(this.agreeUrl+"down/",{"comId":comId});
    }
}
Namespace.register("English.index");
English.index.loginShow = function (flag) {
    if (flag) {
        $('#loginDialog').modal("show");
    } else {
        $('#loginDialog').modal("hide");
    }
}
English.index.loginOut = function () {
    WB2.logout(function(){
    });
    $.get("/user/logout/", {}, function () {
        location.reload()
    })
}
//验证框架
English.Validation.validation = function (node) {
    this.node = node;
    this.msg = ""
}
English.Validation.validation.prototype = {
    validate: function () {
        //验证 长度，正则，必须
        //错误出力
        //样式改变
        if (this.lengthV() && this.patternV() && this.requredV() && this.equalTo()) {
            this.success();
            return true;
        } else {
            this.fail();
            return false;
        }
    },
    lengthV: function () {
        if (this.node.attr("length")) {
            var params = node.attr("length").split(",");
            if (this.node.val().trim().length > (params[0] / 1) && this.node.val().trim().length < params[1] / 1) {
                return true;
            } else {
                this.msg = this.errorMsg.length.replace("[0]", params[0]).replace("[1]", params[1]);
                return false;
            }
        } else {
            return true;
        }
    },
    patternV: function () {
        if (this.node.attr("pattern")) {
            var reg = RegExp(this.node.attr("pattern"));
            if (!(reg.test(this.node.val().trim()))) {
                this.msg = this.errorMsg.pattern;
                return false;
            } else {
                return true;
            }
        } else {
            return true;
        }
    },
    requredV: function () {
        if (this.node.attr("required")) {
            if (this.node.val().trim().length > 0) {
                return true;
            } else {
                this.msg = this.errorMsg.requred;
                return false;
            }
        } else {
            return true;
        }
    },
    equalTo: function () {
        if (this.node.attr("equalTo")) {
            var id = this.node.attr("equalTo");
            if (!(this.node.val().trim() == $("#" + id).val().trim())) {
                this.msg = this.errorMsg.equalTo;
                return false;
            } else {
                return true;
            }
        } else {
            return true;
        }
    },
    remote: function () {
        if (this.node.attr("remote")) {
            var flag = $.get(this.node.attr("remote"), {'name': this.node.val()}, function (data) {
                flag = data
            });
            if (flag.flag == "ok") {
                return true;
            } else {
                this.msg = this.errorMsg.remote;
                return false;
            }
        } else {
            return true;
        }
    },
    success: function () {
        this.node.parents(".control-group").removeClass("error").addClass("success");
        this.node.next().html("<i class='icon-ok'></i>")
    },
    fail: function () {
        this.node.parents(".control-group").removeClass("success").addClass("error");
        this.node.next().html("<i class='icon-remove'></i>" + this.msg)
    },
    errorMsg: {
        "requred": "必填字段",
        "equalTo": '两者不一致',
        'remote': '该名称已经被占用',
        'pattern': '内容格式错误',
        'length': '内容长度必须在[0]和[1]之间'
    }
}
