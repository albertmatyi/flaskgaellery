var positions=Array();
var postsPadding = 0;

function gotoPost(id){
	//window.location=(window.location+'').split('#')[0]+'#post'+id;
	centerDelta = ($('#post-container').width()-$('#post'+id).width()-50)/2;
	$('#post-container').scrollLeft(positions[id]+postsPadding-centerDelta);
	$('.pagination li.active').removeClass('active'); 
	$('.pagination li a[href="#post'+id+'"]').parent().addClass('active');
	return false;
}

function initPosts(){
	positions=Array();
	els = $('.posts').children();
	w = 0;
	for(i=0; i<els.size();i++){
		positions.push(w);
		w += $(els[i]).width()+50; //10 lmargin 40borders
	}
	$('.posts').width(w);
}

$(window).load(function() {
	initPosts();
	$('.posts').css('padding-left', $('.span10').width()/4);
	$('.posts').css('padding-right', $('.span10').width()/4);
	postsPadding = parseInt($('.posts').css('padding-right'));
	gotoPost(0);
	$('.posts').css('position','static');
	$('.posts').css('top', null);
	$('#loader').remove();
//	$('#slider').slider();
	//TODO try make the custom scrollbar work
	
//    $("#post-container").mCustomScrollbar("horizontal",400,"easeOutCirc",1.05,"auto","yes","yes",10);
});