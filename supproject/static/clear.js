$('a[data-toggle="tab-2"]').click(function (e) {
    var activeTab = $(e.target).text();
    $("#dropdown-2").html(activeTab);
    $('#clear-content').css("display", "block");
    var p_id = $(this).attr('name');
    var ubd = $(this).attr('ubd');
    settings = {
        url: '/update/clear/info/',
        type: 'get',
        data: {"p_id": p_id,"user_book_id":ubd},
        success: function (data) {
            $('#c-cid').text(data.data.current.c_name + '(' + data.data.current.c_id + ')');
            $('#c-lid').text('第' + data.data.current.level + '关');
            $('#c-rizhi>.c-rizhi').html(data.data.logs);
            var obj = {"p_id": p_id, "c_id": data.data.current.c_id, "l_id": data.data.current.level,"ubd":data.data.user_book_id};
            sessionStorage.obj = JSON.stringify(obj);
        }
    };
    $.ajax(settings)
});
$('.cclear').each(function () {
    $(this).click(function () {

        o = JSON.parse(sessionStorage.obj);
        var type = $(this).attr('name');
        var catalog_id = $("#catalog_id").val();
        var level_id = $('#level_id').val();
        if (type == 2) {
            alert('清除当前课时后，可能会导致课堂督导显示不正常，再学生端进入任一章节即可解决！')
        } else if (type == 3) {
            alert('即将清除所选关卡后面所有的关卡数据')
        } else if (type == 4) {
            alert('即将抹除所有该生数据，恢复出厂状态！请谨慎操作！！！')
        }
        if (type == 3) {
            data1 = {"type": type, "p_id": o.p_id, "c_id": catalog_id, "l_id": level_id,"user_book_id":o.ubd}
        } else {
            data1 = {"type": type, "p_id": o.p_id, "c_id": o.c_id, "l_id": o.l_id,"user_book_id":o.ubd}
        }
        settings = {
            url: '/update/clear/content/',
            type: 'get',
            data: data1,
            success: function (data) {
                if (data.status == -1) {
                    var msg = '此操作为敏感操作，您还没有权限或您的权限已过期，是否获取五分钟超级权限？';
                    if (confirm(msg) == true) {
                        $.ajax({
                            url: '/update/get/super/',
                            type: 'get',
                            success: function (data) {
                                alert(data.message);
                            }
                        });
                        return None
                    } else {
                        alert('操作取消');
                        return None
                    }
                }
                alert(data.message);
                if (data.data.status == 1) {
                    $('#c-cid').text(data.data.current.c_name + '(' + data.data.current.c_id + ')');
                    $('#c-lid').text('第' + data.data.current.level + '关');
                    $('#c-rizhi>.c-rizhi').html(data.data.logs);
                    //重新定义新数值
                    var obj = {"p_id": o.p_id, "c_id": data.data.current.c_id, "l_id": data.data.current.level,"ubd":data.data.user_book_id};
                    sessionStorage.obj = JSON.stringify(obj);
                }
            }
        };
        $.ajax(settings)
    })
});