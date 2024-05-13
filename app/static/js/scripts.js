$(function() {
	layui.use(['layer'], function() {
		var layer = layui.layer;
		auto_login()
		$(".nav_login").click(function() {
			auto_login()
		})
		function auto_login(){
			layer.open({
				type: 2, 
				title: 'Login', 
				content: './index.html?type=1', 
				area: ['700px', '720px'], 
			});
		}
		$(".upload_button").click(function() {
			layer.open({
				type: 2, 
				title: 'Submmit Your Task', 
				content: './upload.html?type=1', 
				area: ['700px', '720px'], 
			});	
		})
	});
})