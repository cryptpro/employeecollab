$(document).ready(function(){
	$('div.tooltip').hide();
	
	$('.datepick input').datepicker({
    format: "yyyy-mm-dd"
	});	
	$('.datepick input').on('change', function (ev) {

        $('.datepicker').hide();

    });
	
	$('#formpost').submit(function(event){
		event.preventDefault();
		form_data = JSON.stringify($(this).serializeArray());
		fd = new FormData();
		if ($('#fileupload')[0].files[0]){
		fd.append("fileupload", $('#fileupload')[0].files[0]);
		}
		$.each($.parseJSON(form_data), function(index, value){
			fd.append(value["name"], value["value"]);
		});
		console.log(fd);
		fd.append("txtlocation", $("#spanlocation").html());
		console.log(fd);
		$.ajax({
		       url: "/postcontent",
		       type: "POST",
		       data: fd,
		       processData: false,
		       contentType: false,
		       success: function(response) {
		           $('#pre_post').replaceWith("<div id='pre_post'></div>"+response);
		           $('#formpost').find('input').val('');
		           $('#formpost').find('textarea').val('');
				   $("#uploadedpic").html("");
		       },
		       error: function(jqXHR, textStatus, errorMessage) {
		           console.log(errorMessage); // Optional
		       }
		    });

	});
});

$(document).on("click",".alike", function(event){
		event.preventDefault();
		post_id = $(this).parent().parent().parent().parent().attr("id")
		type = $(this).attr("type");
		if(type == "like"){
			url = "/likepost"
			txt = "Unlike"
			typeset = "unlike"
		}
		else{
			url = "/unlikepost"
			txt = "Like"
			typeset = "like"
		}
		that = this;
		$.ajax({
		       url: url,
		       type: "GET",
		       data: {"post_id" : post_id},
		       success: function(response) {
		           $(that).text(response+txt);
		           $(that).attr("type", typeset);
		       }
		    });
	});

$(document).on("click",".acommentlike", function(event){
		event.preventDefault();
		comment_id = $(this).parent().parent().parent().attr("id");
		console.log($(this).parent().parent().parent().attr("class"));
		type = $(this).attr("type");
		if(type == "like"){
			url = "/likecomment"
			txt = "Unlike"
			typeset = "unlike"
		}
		else{
			url = "/unlikecomment"
			txt = "Like"
			typeset = "like"
		}
		that = this;
		$.ajax({
		       url: url,
		       type: "GET",
		       data: {"comment_id" : comment_id},
		       success: function(response) {
		           $(that).text(response+txt);
		           $(that).attr("type", typeset);
		       }
		    });
	});

$(document).on("click",'#linkupload', function(event){
		event.preventDefault();
		$("#fileupload").trigger("click");
	});
$(document).on("change",'#fileupload', function(event){
		event.preventDefault();
		filevalue = $("#fileupload").val().split("\\");
		$("#uploadedpic").html(filevalue[filevalue.length-1]);
	});

$(document).on("click",'#changephoto', function(event){
		event.preventDefault();
		$("#picupload").trigger("click");
	});
$(document).on("change", "#picupload", function(event){
	$("#formchangephoto").trigger("submit");
});

$(document).on("submit", "#formchangephoto", function(event){
	event.preventDefault();
	console.log("in")
	fd = new FormData();
	if ($('#picupload')[0].files[0]){
	fd.append("picupload", $('#picupload')[0].files[0]);
	}
	$.ajax({
		       url: "/changephoto",
		       type: "POST",
		       data: fd,
		       processData: false,
		       contentType: false,
		       success: function(response) {
		          $("#imgprofilepic").attr("src","static/uploads/"+response);
		       },
		       error: function(jqXHR, textStatus, errorMessage) {
		           console.log(errorMessage); // Optional
		       }
		    });

});

$(document).on("click",'.togmsg', function(event){
		event.preventDefault();
		$(this).parent().parent().find(".msgcontent").toggle();
	});

	$(document).on("click",'.acomment',function(event){
		event.preventDefault();
		console.log($(this).parent().parent().attr('class'));
		$(this).parent().parent().siblings('.divcomment').toggle();
		$(this).parent().parent().siblings('.divcomments').toggle();								
	});

$(document).on("click",'.edit_details',function(event){
	event.preventDefault();
	column = $(this).parent().find("input").attr("col-type");
	column_value = $(this).parent().find("input").val();
	that= this
	if(column_value != ""){
		$.ajax({
		       url: "/updateprofile",
		       type: "GET",
		       data: {"value" : column_value, "column" : column},
		       success: function(response) {
			       	$(that).parent().find("input").attr("placeholder", column_value);
			       	$(that).parent().find("input").val("");
			       	if(column=="first_name"){
			       	$(document).find(".txt_wall_first_name").text(column_value);
			       }
		       }
		    });
	}
});

$(document).on("submit", ".formcomment", function(event){
	event.preventDefault();
	comment = $(this).children().find(".txtcomment").val();
	post_id = $(this).children().find(".txtcomment").attr("post_id");
	that = this;
	$.ajax({
		       url: "/comment",
		       type: "GET",
		       data: {"post_id" : post_id, "comment" : comment},
		       success: function(response) {
		           $(that).parent().parent().find(".divcomments").append(response);
		       }
		    });
});


$(document).on("click", "#iconlocation", function(){
	if($(this).attr("active") == "1"){
	geoFindMe();
	}
	else{
		$("#spanlocation").html("");
		$(this).attr("active", "1");
	}
});
function geoFindMe() {

  if (!navigator.geolocation){
    output.innerHTML = "<p>Geolocation is not supported by your browser</p>";
    return;
  }
function success(position) {
    latitude  = position.coords.latitude;
    longitude = position.coords.longitude;
    $.ajax({ 
    		url:'http://maps.googleapis.com/maps/api/geocode/json?latlng='+ latitude +','+ longitude +'&sensor=true',
         	success: function(data){
             $("#spanlocation").html(data.results[0].formatted_address);
			 $("#iconlocation").attr("active", "0");
             /*or you could iterate the components for only the city and state*/
         	}
	});
  };

  function error() {
    output.innerHTML = "Unable to retrieve your location";
  };

  navigator.geolocation.getCurrentPosition(success, error);
}

$(document).on("click", ".btnaddfriend", function(event){
	event.preventDefault();
	profile_id = $(this).attr('profile_id');
	that = this;
	$.ajax({ 
    		url:"/addfriend",
    		data: {profile_id : profile_id},
         	success: function(data){
             $(that).attr("class", "btn btn-warning btn-sm btncancel");
             $(that).attr("request_id", data);
             $(that).html("Cancel");
             /*or you could iterate the components for only the city and state*/
         	}
	});
});

$(document).on("click", ".btncancel", function(event){
	event.preventDefault();
	request_id = $(this).attr('request_id');
	that = this;
	$.ajax({ 
    		url:"/cancelfriend",
    		data: {request_id : request_id},
         	success: function(data){
             $(that).attr("class", "btn btn-primary btn-sm btnaddfriend");
             $(that).html("Add friend");
             /*or you could iterate the components for only the city and state*/
         	}
	});
});

$(document).on("click", ".btnconfirm", function(event){
	event.preventDefault();
	request_id = $(this).attr('request_id');
	profile_id = $(this).attr('profile_id');
	that = this;
	$.ajax({ 
    		url:"/confirmfriend",
    		data: {request_id : request_id, profile_id : profile_id},
         	success: function(data){
         		if($(that).parent().attr("class") == "divrequests"){
         			$(that).parent().remove();
         		}
         		else{
         			btnunfriend_text = '<button profile_id="'+profile_id+'" class="btn btn-danger btn-sm btnunfriend">Unfriend</button>'
	             $(that).parent().html(btnunfriend_text)
	             $(that).parent().attr("class", "col-md-3");
	         	}
         	}
	});
});


$(document).on("click", ".btnunfriend", function(event){
	event.preventDefault();
	profile_id = $(this).attr('profile_id');
	that = this;
	$.ajax({
    		url:"/unfriend",
    		data: {profile_id : profile_id},
         	success: function(data){
             $(that).attr("class", "btn btn-primary btn-sm btnaddfriend");
             $(that).html("Add friend");
         	}
	});
});

$(document).on("change", ".searchfilter", function(event){
	event.preventDefault();
	category = $(this).val();
	query = $('.searchtxt').html();
	$.ajax({
    		url:"/search",
    		data: {category : category, query : query },
         	success: function(data){
             $("#resultsarea").html(data);
         	}
	});
});

$(document).on("click", ".sendmsg", function(event){
	event.preventDefault();
	user_id = $(this).attr("user_id");
	$("#totext").attr("to_id", user_id);
	first_name = $(this).attr("first_name");
	 $("#txtmsg").val("");
	$("#totext").html("To&nbsp;:&nbsp;"+first_name);
	$("#msg-modal").modal();
});

$(document).on("click", "#btnsendmsg", function(event){
	event.preventDefault();
	msg = $("#txtmsg").val();
	user_id = $("#totext").attr("to_id");
	$.ajax({
    		url:"/sendmessage",
    		data: {to_id : user_id, msg : msg},
         	success: function(data){
             $("#msg-modal").modal("hide");
         	}
	});
});


$(document).on('click', '.decline', function(event){
	event.preventDefault();
	profile_id = $(this).attr("profile_id");
	request_id = $(this).attr("request_id");
	that = this;
	$.ajax({
    		url:"/decline",
    		data: {profile_id : profile_id, request_id : request_id},
         	success: function(data){
         		if($(that).parent().attr("class") == "divrequests"){
         			$(that).parent().remove();
         		}
             $(that).parent().attr("class", "col-md-3");
         		btn_text = '<button profile_id="'+profile_id+'" class="btn btn-primary btn-sm btnaddfriend">Add friend</button>';
             $(that).parent().html(btn_text);
         	}
	});
});

$(document).on('change', '.editpostsvisibility', function(event){
	event.preventDefault();
	column_value = $(this).val();
	$.ajax({
		       url: "/updateprofile",
		       type: "GET",
		       data: {"value" : column_value, "column" : "post_visibility_id"},
		       success: function(response) {
			       }
		    });
});

$(document).on('change', '.editfriendsvisibility', function(event){
	event.preventDefault();
	column_value = $(this).val();
	$.ajax({
		       url: "/updateprofile",
		       type: "GET",
		       data: {"value" : column_value, "column" : "friends_visibility_id"},
		       success: function(response) {
			       }
		    });
});

