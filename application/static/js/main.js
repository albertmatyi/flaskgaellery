var positions=Array();
var postsPadding = 0;

//10 lmargin 40borders | metrics of the .post.well
var MARGIN_AND_BORDERS = 50;

function gotoPost(id){
	centerDelta = ($('#post-container').width()-$('#post'+id).width()-MARGIN_AND_BORDERS)/2;
	dst = positions[id]+postsPadding-centerDelta;
	$('#post-container').scrollLeft(dst);
	$('.pagination li.active').removeClass('active'); 
	$('.pagination li a[href="#post'+id+'"]').parent().addClass('active');
	return false;
}

function initPostPositions(){
	positions=Array();
	els = $('.posts').children();
	w = 0;
	for(i=0; i<els.size();i++){
		positions.push(w);
		w += $(els[i]).width()+MARGIN_AND_BORDERS;
	}
	$('.posts').width(w);
	return w;
}


function calculatePositions(){
	//initializes the positions of the posts
	initPostPositions();
	//adds a padding so we can center the first & last elements too
	$('.posts').css('padding-left', $('.span10').width()/4);
	$('.posts').css('padding-right', $('.span10').width()/4);
	//retrieves the padding for the posts container
	postsPadding = parseInt($('.posts').css('padding-right'));
	// scrolls to the 1st post
	gotoPost(0);
	// makes posts visible (they were hidden with css for preloading)
	$('.posts').css('position','static');
	$('.posts').css('top', null);
	// remove the loader 
	$('#loader').remove();
	
	//center paginator
	postsWidth = $('#post-container').width();
	paginationWidth = $('.pagination').width(); 
	$('.pagination').css('margin-left', (postsWidth-paginationWidth)/2+'px');
	// show it (it was hidden by css)
	$('.pagination').css('position', 'static');
}

$(window).load(function() {
	calculatePositions();
});