$('a[data-toggle="tab-2"]').click(function (e) {
    var activeTab = $(e.target).text();
    $("#dropdown-2").html(activeTab);
    $('#clear-content').css("display", "block");
    var p_id = $(this).attr('name');

    settings = {
        url: '/update/clear/info/',
        type: 'get',
        data: {"p_id": p_id},
        success: function (data) {
            $('#c-cid').text(data.data.current.c_name + '(' + data.data.current.c_id + ')');
            $('#c-lid').text('第' + data.data.current.level + '关');
            $('#c-rizhi>.c-rizhi').html(data.data.logs);
            var obj = {"p_id": p_id, "c_id": data.data.current.c_id, "l_id": data.data.current.level};
            sessionStorage.obj = JSON.stringify(obj);
        }
    };
    $.ajax(settings)
});
$('.cclear').each(function () {
    $(this).click(function () {
        o = JSON.parse(sessionStorage.obj);
        var type = $(this).attr('name');
        if(type == 2){
            alert('清除当前课时后，可能会课堂督导显示不正常，再学生端进入任一章节即可解决！')
        }
        settings = {
            url: '/update/clear/content/',
            type: 'get',
            data: {"type": type, "p_id": o.p_id, "c_id": o.c_id, "l_id": o.l_id},
            success: function (data) {
                alert(data.message);
                if (data.data.status == 1) {
                    $('#c-cid').text(data.data.current.c_name + '(' + data.data.current.c_id + ')');
                    $('#c-lid').text('第' + data.data.current.level + '关');
                    $('#c-rizhi>.c-rizhi').html(data.data.logs);
                    var obj = {"p_id": o.p_id, "c_id": data.data.current.c_id, "l_id": data.data.current.level};
                    sessionStorage.obj = JSON.stringify(obj);
                }
            }
        };
        $.ajax(settings)
    })
});