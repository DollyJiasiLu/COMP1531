// $(document).ready(function() {
// 	var parent = $('#nav');
// 	var child = $('#line');
// 	child.css('height',(parent.height())  +'px');
// 	child.css('margin-bottom','-20px');
// //	$('#submit').click(getInputs);
// });

function setColour(colour) {
	$('#page').css('background-color','#FFE6B3');
}

function addAnswer() {
	i = $("input").length - 1;
	if (i > 6) return false;
	$input =  $(".answerBox:first").clone(true);
	$input = $input.attr("name", "a" + i);
	$input = $input.val("");
	$delete = $(".deleteAnswer:first").clone(true);
	$delete = $delete.val(i.toString());
	$li = $("<li>", {class: "answerList", id: "l" + i});
	$($li).append($input);
	$li = $li.append($delete);
	$("#answers").append($li);

	return false;
}

function deleteAnswer(button) {
	if ($(".answerBox").length <= 2) return;
	var id = $(button).val();
	$(button).remove();
	$("#l"+id).remove(); //remove list
	$("[name='"+ "a" + id + "]").remove(); //remove inputbox

	var i = 0;
	$(".answerBox").each(function() {
		$(this).attr("name", "a" + i);
		console.log(i);
		i += 1;
	});

	i = 0;
	$(".answerList").each(function() {
		$(this).attr("id", "l" + i);
		i += 1;
	});

	i = 0;
	$(".deleteAnswer").each(function() {
		$(this).attr("value", i.toString());
		i += 1;
	});
}

function eraseCourse(course) {
	var addedList = $(".addedCourse");
	var toDel = $(course).parent()
	var indx = addedList.index(toDel);
	var IDlst = $("#course-IDs").val().split(",").map(Number)
	console.log("Before splice: " + IDlst);
	if (IDlst.length == 0) IDlst = -1;
	course = IDs[courses.indexOf(toDel.text())]
	IDlst.splice(indx,1);
	toDel.remove();
	console.log("After splice: " + IDlst)
	$("#course-IDs").val(IDlst);
}

function add_course() {

	var selected = $("#courseInput").val();

	if (courses.indexOf(selected) == -1) return false;
	var chosenID = IDs[courses.indexOf(selected)];

	var selectedCourses = $("#course-IDs").val().split(",").map(Number);
	if (selectedCourses[0] == -1 || selectedCourses[0] == NaN) selectedCourses[0] = chosenID;
	else  {
		if (selectedCourses.indexOf(chosenID) == -1) selectedCourses.push(chosenID);
		else return false;
	}
	$("#course-IDs").val(selectedCourses);

	if ($("#selected-courses").text() == "") {
		$toAdd = $("<span>", {"class":"addedCourse"});
		$delBtn = $("<input>",{"type":"button","onclick":"eraseCourse(this)","value":"-",
	 		"class":"deleteCourse"});
		$toAdd.text(selected);
		$toAdd.append($delBtn);
		console.log("selected: " + selected);
		$("#selected-courses").append($toAdd);
	} else {
		$toAdd = $("<span>", {"class":"addedCourse"});
		$toAdd.text(", " + selected);
		$delBtn = $("<input>",{"type":"button","onclick":"eraseCourse(this)","value":"-",
			"class":"deleteCourse"});
		$toAdd.append($delBtn);
		$("#selected-courses").append($toAdd);
	}
}

function checkBoxes() {
	if ($(".question:checkbox:checked").length > 0) {
		console.log("x > 0")
		return true;
	}
	console.log("x == 0")
	return false;
}

function checkCourses() {
	var selectedCourses = $("#course-IDs").val().split(",").map(Number);

	if (selectedCourses[0] == -1) return false;

	for (var i = 0; i < selectedCourses.length; i++) {
		if (IDs.indexOf(selectedCourses[i]) == -1) return false;
	}

	return true;
}

function verifyPass() {
	if ($("#password1").val() != $("#password2").val()) {
		$("#password2").css("border-color","red");
		$("#password1").css("border-color","red");
	}


}

function checkPass() {
	if ($("#password1").val() != $("#password2").val()) return false;
	if (!checkCourses()) return false;
}

function checkForm() {
	return (checkBoxes() && checkCourses());
}

function toggleDisplay(btn) {
	qID = $(btn).attr("id");
	if ($("#textAnswer"+qID).css("display") == "none") {
		$("#textAnswer"+qID).show("slow");
		$(btn).text("- Hide text responses");
	} else {
		$("#textAnswer"+qID).hide("slow");
		$(btn).text("+ Show text responses");
	}
}

function checkDates() {
	$open = $("#activation");
	if ($open.val() == "") {
		return;
	}
	$close = $("#close")
	if ($close.val() == "") {
		return;
	}
	if ($close.val() < $open.val()) {
		$close.val($open.val());
	}
}

function checkmultDates(input) {
	console.log("its been blurred")
	id = Number($(input).attr("id").split("-")[0]);
	$open = $("#" + id + "-activation");
	$close = $("#" + id + "-close");

	if ($open.is(":invalid") || $close.is(":invalid")) {
		if ($open.is(":invalid")) {
			$open.addClass("error")
			alert("Activation Date Incomplete!")
		}
		if ($close.is(":invalid")) {
			$close.addClass("error")
			alert("Closure Date Incomplete!")
		}
		return;
	}
	$open.removeClass("error");
	$close.removeClass("error");

	if ($close.val() != "" && $open.val() != "") {
		if ($close.val() < $open.val()) {
			$close.val($open.val());
			alert("Closure date must be past activation date.\nThe time you entered was not saved.")
			return;
		}
		usrDate = new Date($close.val());
		currDate = new Date()
		if (usrDate < currDate) {
			currDate.setHours(currDate.getHours() + 1)
			min = (currDate.getMinutes()/10) ? currDate.getMinutes() : "0"+currDate.getMinutes();
			hr = (currDate.getHours()/10) ? currDate.getHours() : "0"+currDate.getHours();
			mth = ((currDate.getMonth()+1)/10) ? (currDate.getMonth()+1) : "0"+(currDate.getMonth()+1);
			day = (currDate.getDate()/10) ? currDate.getDate() : "0"+currDate.getDate();
			yr = currDate.getFullYear();
			format = yr+'-'+mth+'-'+day+'T'+hr+':'+min;
			$close.val(format)
			alert("Closure time must be past current time.\nOnce a survey has passed its close time it will be closed PERMANENTLY. To permanently close a survey click the 'close survey' button below")
			return;
		}

	}



	$("#chosenSurvey").val(id);
  $.ajax({
      url: '/surveys',
      data: $('#main-form').serialize(),
      type: 'POST',
      success: function(response) {
				console.log(response)
        processTimeUpdate(response,id);
      },
      error: function(error) {
          console.log(error);
      }
  });
}

function processTimeUpdate(response,id) {
	if (response == "") return;
	action = response.split("?")[0];
	data = response.split("?")[1];
	console.log(id)
	console.log(action)
	if (action == "activate") {
		$("#status"+id).text("Active Survey");
		$("#status"+id).removeClass("badge-secondary").addClass("badge-approved");
	} else if (action == "close") {
		$("#status"+id).removeClass("badge-approved").addClass("badge-secondary");
		var d = new Date(data);
		dt = (d.getHours()%12 == 0) ? 12 : d.getHours()%12;
		dt += ":"+d.getMinutes();
		dt += (d.getHours()/12 == 0) ? "AM" : "PM";
		dt += " " + d.getDate() + "/" + (d.getMonth()+1) + "/" + d.getFullYear()
		$("#status"+id).text("Opening at: " + dt);
	} else if (action == "keep") {
		var d = new Date(data);
		dt = (d.getHours()%12 == 0) ? 12 : d.getHours()%12;
		dt += ":"+d.getMinutes();
		dt += (d.getHours()/12 == 0) ? "AM" : "PM";
		dt += " " + d.getDate() + "/" + (d.getMonth()+1) + "/" + d.getFullYear()
		$("#status"+id).text("Opening at: " + dt);
	}
}
