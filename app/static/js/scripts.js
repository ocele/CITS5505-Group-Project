$(function() {
	layui.use(['layer'], function() {
		var layer = layui.layer;
		
		
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

