$(function () {
    layui.use(['layer'], function () {
        var layer = layui.layer; // 将 layer 初始化放在外面

        $(".upload_button").click(function () {
            $.ajax({
                url: './upload.html?type=1', // 确认这个是你用来验证登录状态的API路径
                method: 'GET',
                success: function (data) {
                    console.log(data);
                    if (data.code == 200 | !data.code) { // 假设成功时返回的状态码是200
                        layer.open({
                            type: 2,
                            title: 'Submit Your Task',
                            content: './upload.html?type=1',
                            area: ['700px', '720px'],
                        });
                    } else {
                        layer.msg('Please log in first', {
                            icon: 2, // 可以加上图标
                            time: 2000 // 2秒后自动关闭
                        });
                    }
                },
                error: function () {
                    layer.msg('Please log in first.', {
                        icon: 2,
                        time: 2000 // 2秒后自动关闭
                    });
                }
            });
        });
    });
});
