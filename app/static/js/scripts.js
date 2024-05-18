$(function () {
    layui.use(['layer'], function () {
        var layer = layui.layer; 

        $(".upload_button").click(function () {
            $.ajax({
                url: './upload.html?type=1', 
                method: 'GET',
                success: function (data) {
                    console.log(data);
                    if (data.code == 200 | !data.code) { 
                        layer.open({
                            type: 2,
                            title: 'Submit Your Task',
                            content: './upload.html?type=1',
                            area: ['700px', '720px'],
                        });
                    } else {
                        layer.msg('Please log in first', {
                            icon: 2, 
                            time: 2000 
                        });
                    }
                },
                error: function () {
                    layer.msg('Please log in first.', {
                        icon: 2,
                        time: 2000 
                    });
                }
            });
        });
    });
});
