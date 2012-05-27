function gotoPost(id){
	window.location=(window.location+'').split('#')[0]+'#post'+id;
	$('.pagination li.active').removeClass('active'); 
	$('.pagination li a[href="#post'+id+'"]').parent().addClass('active');
	return false;
}

$(window).load(function() {
	els = $('#posts')
	for(int i)
//	$('#slider').slider();
	//TODO try make the custom scrollbar work
	
//    $("#post-container").mCustomScrollbar("horizontal",400,"easeOutCirc",1.05,"auto","yes","yes",10);
});