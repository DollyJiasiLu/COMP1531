$(document).ready(function() {
	var parent = $('#nav');
	var child = $('#line');
	child.css('height',(parent.height()).toString()  +'px');
	child.css('margin-bottom','-20px');
	$('#submit').click(getInputs);
});

function setColour(colour) {
	$('#page').css('background-color','#FFE6B3');
}

/*function getInputs() {
	var data = {};
	data.temp = $('#temp').text().toString();
	data.user = $('#username').val();
	data.password = $('#password').val();
	console.log(data);
	console.log(JSON.stringify(data));
	$.ajax({ 
		type: 'POST',
		url: '/login',
		data: data,//JSON.stringify(data),
		contentType: 'application/x-www-form-urlencoded; charset=UTF-8',
		success: function(data) {
		//$('#temp').innerHTML = (data.temp).toString() + "&deg;C"
		console.log("Recieved :");
		console.log(data);
			$('#dispName').text(data.name);
			$('#email').text(data.email);
			$('#colour').text(data.colour);
			setColour(data.colour);
		}
	});
}*/


//mysql root password: whMxhdOjC3&w