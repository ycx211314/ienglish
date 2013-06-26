(function ($) {
    /* 这里放置代码 */
    //$.fn.datagrid=new Object();
    Grid=function(){};
    Grid.prototype = {
        init:function(table,opt){
            this.opt=$.extend({
                idField:"id",
                loadMsg:"数据加载中...",
                pagesize:10,
                pagelist:[10,20,30,50],
                page:1,
                height:300,
                checkbox:false,
                pagination:true
            },opt) ;
            this.cols=[];
            this._table =table;
            this.handTable();
            this.handlerHeader();
            this.askData(this.cols);
            this.bindEvent(this,this._table,this.opt);
        },
        getSelected:function(){
            var keys =[];
            var index = 0;
            $(".datarow input[checked='checked']").each(function(){
                //console.debug($(this).attr("key"))
                keys[index] = $(this).attr("key")/1;
                index ++;
            });
            return keys;
        },
        handlerHeader : function(){
            var colspan = 1;
            if(this.opt.columns && this.opt.columns.length >0){
                var theader ="<table class='table table-hover datagrid'><thead><tr class='datathead'>"
                //var cols =[];
                if (this.opt.checkbox){
                    theader +="<th class='grid-checkbox'><input type='checkbox' class='checkAll' /></th>"
                    this.cols[colspan-1]='id';
                    colspan++;
                }
                for(var i =0;i<this.opt.columns.length;i++){
                    theader +="<th>"+this.opt.columns[i].title+"</th>"
                    this.cols[colspan-1]=this.opt.columns[i].name;
                    colspan++;
                }
                theader +="</tr></thead><tbody class='datagridTable'></tbody></table>";
                var tbody ="<tbody style='height:"+this.opt.height+"px;'></tbody>"
                $(this._table).html(tbody);
                $(this._table).children("tbody").html("<tr><td colspan='"+this.cols.length+"'>"+theader+"</td></tr>")
                return this.cols;
            }
        },
        handTable:function(){
            $(this._table).before("<div class='modal-header datagrid-header'>"+
                '<button type="button" class="close" data-dismiss="modal" aria-hidden="true">×</button>'+
                '<h3>'+this.opt.title+'</h3>'+
                "</div>");
            if(this.opt.toolbar){
                $(this.opt.toolbar).appendTo(this._table);
               // $(this._table).before($(this.opt.toolbar));
                alert(1)
            }
            $(this._table).addClass("table datagrid")
            $(this._table).css("border-left","1px solid #F7F7F7")
            $(this._table).css("border-right","1px solid #F7F7F7")
            if (this.opt.pagination){
                var footer ="<div class='row-fluid'>"
                var pageSelect = "<select class='input-mini pageList' style='margin:0px;'>";
                for(var x=0;x<this.opt.pagelist.length;x++){
                    pageSelect +="<option>"+this.opt.pagelist[x]+"</option>"
                }
                pageSelect +="</select>" ;
                var toobar = "<div class='btn-toolbar pagination'><div class='btn-group'>"+pageSelect+"</div>";
                toobar +="<div class='btn-group'><button class='btn btn-link btn-datagrid pageone'><i class='icon-double-angle-left'></i></button><button class='btn btn-link btn-datagrid pageprev'><i class='icon-angle-left'></i></button></div>"
                toobar +="<div class='btn-group'><div class='input-prepend input-append' style='margin:0px;'><button class='btn changePage'>跳</button><input class='input-mini' type='text'><span class='add-on pages'>页/{0}页</span></div></div>"
                toobar +="<div class='btn-group'><button class='btn btn-link btn-datagrid pagenext'><i class='icon-angle-right'></i></button><button class='btn btn-link btn-datagrid pagelast'><i class='icon-double-angle-right'></i></button><button class='btn btn-link btn-datagrid reaload'><i class='icon-refresh'></i></button></div>"
                toobar +="<div class='btn-group displayText'><button class='btn btn-link btn-datagrid '><span class='messager'>显示{0}到{1}条数据 共100条</span></button></div>"
                toobar +="</div>"
                footer +=toobar;
                footer +="</div>"
            }
            $(this._table).after(footer)
        },
        askData:function(){
            $(this._table).children("tbody").find(".datagridTable").first().html('<tr><td colspan="'+this.cols.length+'" class="progress progress-striped active" style="padding:0px 40px;"><div class="bar" style="width:100%;">'+this.opt.loadMsg+'</div></td></tr>');
            var data  = "page="+this.opt.page+"&pagesize="+this.opt.pagesize;
            var grid = this;
            $.ajax({
                url:this.opt.url,
                type:"post",
                dataType:"json",
                data:data+"&csrfmiddlewaretoken="+ English.Common.cookieTool.getCsrftoken(),
                success:function(json){
                    grid.pages = grid.handerPagination(json.total);
                    grid.handlerData(json.rows);
                }
            })
        },
        handerPagination:function(total){
            var messager = "显示{0}到{1}条数据 共{2}条"
            if (total/this.opt.pagesize>0 && total%this.opt.pagesize > 0){
                var  pages = parseInt(total/this.opt.pagesize)
                pages +=1
            }
            var start = (this.opt.page-1)*this.opt.pagesize +1;
            var end =this.opt.page*this.opt.pagesize>total?total:this.opt.page*this.opt.pagesize;
            var html = $(".pages").first().html().replace("{0}",pages);
            $(".pages").first().html(html)
            $(".pagination input").first().val(this.opt.page);
            $(".messager").first().html(messager.replace("{0}",start).replace("{1}",end).replace("{2}",total));
            this.opt.pages = pages;
            return pages;
        },
        handlerData:function(rows){
            var pW= $(this._table).children("tbody").find(".datagridTable").first().width();
            var body ="";
             for(var index=0;index < rows.length;index++){
                 var tr = "<tr class='datarow'>"
                 for(var j =0;j<this.cols.length;j++){
                     if(this.opt.checkbox && this.cols[j]=="id"){
                         tr +="<td class='grid-checkbox'><input type='checkbox' key='"+rows[index]["id"]+"'/></td>"
                     }else{
                         var widht = (this.opt.columns[j-1].width*(pW-5)/100)+"px";
                         tr +="<td width='"+widht+"'>"+rows[index][this.cols[j]]+"</td>"
                     }

                 }
                 tr +="</tr>"
                 body +=tr;
             }
            $(this._table).children("tbody").find(".datagridTable").html(body);
            $(".datarow").bind("click",function(){
                var node = $(this).find("input[type='checkbox']").first();
                if ($(node).attr("checked")){
                    $(node).removeAttr("checked");
                    $(this).removeClass("info");
                }else{
                    $(node).attr("checked","checked");
                    $(this).addClass("info");
                }
            });
        },
        bindEvent:function(grid,opt,table){
            $(".checkAll").change(function(){
                if($(this).attr("checked")){
                    $(".datarow input[type='checkbox']").attr("checked","checked")
                }else{
                    $(".datarow input[type='checkbox']").removeAttr("checked");
                }
            });
            $(grid._table).find(".pageList").change(function(){
                grid.opt.pagesize=$(grid._table).val()/1;
                grid.askData();

            });
            $(".pageone").click(function(){
                //askData("page=1&pagesize="+this.opt.pagesize,cols,_table);
                grid.opt.page = 1;
                grid.askData();
            });
            $(".pageprev").click(function(){
                var param = 1;
                if(grid.opt.page/1 - 1 >=0){
                    param = 1;
                }else{
                    param = grid.opt.page/1 -1
                }
                grid.opt.page = param
                grid.askData();

            });
            $(".pagenext").click(function(){
                var param = grid.opt.pages;
                if(grid.opt.page/1 + 1 >grid.opt.pages){
                    param = grid.opt.pages;
                }else{
                    param = grid.opt.page/1 +1
                }
                grid.opt.page = param
                //askData("page="+param+"&pagesize="+this.opt.pagesize,cols,_table);
                grid.askData();

            });
            $(".pagelast").click(function(){
                grid.opt.page = grid.opt.pages;
                grid.askData();
            });
            $(".reaload").click(function(){
                grid.askData();
            })
            $(".changePage").click(function(){
                try{
                    var pps = parseInt($(this).first().next().val());
                    if (pps > grid.opt.pages && pps < 1){
                        $(this).first().next().val(grid.opt.page)
                    }else{
                        grid.opt.page = pps
                        grid.askData();
                    }
                }catch(e){
                    $(this).first().next().val(grid.opt.page)
                }

            });
        }
    }
    $.fn.extend({"datagrid":function(options){
        this._table = this;
        this.pages = 0;
        this.opt = options;
        this.cols = [];
        var mygrid = new Grid();
        if (jQuery.isPlainObject(options) ){
            mygrid.init(this,options);
        }else{
            return mygrid[options]();
        }
    }});
})(jQuery);