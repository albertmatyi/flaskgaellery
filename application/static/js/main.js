var postPositions=Array();
var postsPadding = 0;

//10 lmargin 40borders | metrics of the .post.well
var MARGIN_AND_BORDERS = 50;

var stpc = {
	/**
	 *  the element to be scrolled by the drag
	 */
	el: null,
	/**
	 * Stores the destination x
	 */
	destinationX: 0,
	/**
	 * Friction multiplier (how much we decelerate at each iteration)
	 */
	frictionMultiplier: .2,
	/**
	 * Marks a state where we've released the mouse, and we let the scrolled element slide 
	 */
	isSliding: false,
	/**
	 * The timeout value of the movement (in ms)
	 */
	timeout:30, 
}

function slideTowardsPost(){
	
	delta = stpc.destinationX - stpc.el.scrollLeft();
	delta *= stpc.frictionMultiplier;
	old = stpc.el.scrollLeft();
	stpc.el.scrollLeft(old + delta);
	console.log(delta);
	if(Math.abs(delta) < 3 || old == stpc.el.scrollLeft()){
		stpc.isSliding = false;
		stpc.el.scrollLeft(stpc.destinationX)
	}
	if(stpc.isSliding){
		setTimeout(slideTowardsPost, stpc.timeout);
	}
}


function gotoPost(id){
	stpc.isSliding = true;
	stpc.destinationX = postPositions[id];
	console.log(stpc.destinationX);
	setTimeout(slideTowardsPost, stpc.timeout);
	$('.pagination li.active').removeClass('active'); 
	$('.pagination li a[href="#post'+id+'"]').parent().addClass('active');
	return false;
}

function initPostPositions(){
	postPositions=Array();
	els = $('.posts').children();
	w = postsPadding;
	postContainerWidth = $('#post-container').width();
	for(i=0; i<els.size();i++){
		centerDelta = (postContainerWidth-$(els[i]).width()-MARGIN_AND_BORDERS)/2;
		postPositions.push(w-centerDelta);
		console.log(postPositions + ' / ' + $(els[i]).width());
		w += $(els[i]).width()+MARGIN_AND_BORDERS;
	}
	$('.posts').width(w);
	return w;
}


function calculatePositions(){
	//calculate the posts padding
	// TODO figure out wtf is wrong here, and maybe fix it - not urgent
//	postsPadding = $('.span10').width()/4;
	//adds a padding so we can center the first & last elements too
//	$('.posts').css('padding-left', postsPadding);
//	$('.posts').css('padding-right', postsPadding);
	
	//initializes the positions of the posts
	initPostPositions();
	
	// makes posts visible (they were hidden with css for preloading)
	$('.posts').css('position','static');
	$('.posts').css('top', null);
	
	//center paginator
	postsWidth = $('#post-container').width();
	paginationWidth = $('.pagination').width(); 
	$('.pagination').css('margin-left', (postsWidth-paginationWidth)/2+'px');
	// show it (it was hidden by css)
	$('.pagination').css('position', 'static');

	
}

$(window).load(function() {
	stpc.el = $('#post-container');
	calculatePositions();
	// remove the loader 
	$('#loader').remove();
	// scrolls to the 1st post
	gotoPost(0);
});