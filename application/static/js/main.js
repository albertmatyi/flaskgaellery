var postPositions = Array();
var postsPadding = 0;

// 10 lmargin 40borders | metrics of the .post.well
var MARGIN_AND_BORDERS = 50;

function SlideCfg() {
	/**
	 * the element to be scrolled by the drag
	 */
	this.el = null;
	/**
	 * Stores the destination x
	 */
	this.destinationX = 0;
	/**
	 * Friction multiplier (how much we decelerate at each iteration)
	 */
	this.frictionMultiplier = .2;
	/**
	 * Marks a state where we've released the mouse, and we let the scrolled
	 * element slide
	 */
	this.isSliding = false;
	/**
	 * The timeout value of the movement (in ms)
	 */
	this.timeout = 30;
}

function slideTo(slideCfg) {
	delta = slideCfg.destinationX - slideCfg.el.scrollLeft();
	delta *= slideCfg.frictionMultiplier;
	old = slideCfg.el.scrollLeft();
	slideCfg.el.scrollLeft(old + delta);
	if (Math.abs(delta) < 1 || old == slideCfg.el.scrollLeft()) {
		slideCfg.isSliding = false;
		slideCfg.el.scrollLeft(slideCfg.destinationX)
	}
	if (slideCfg.isSliding) {
		setTimeout(function() {
			slideTo(slideCfg)
		}, slideCfg.timeout);
	}
}

var postSlideCfg = new SlideCfg();

var paginationSlideCfg = new SlideCfg();

function gotoPost(id) {
	postSlideCfg.isSliding = true;
	postSlideCfg.destinationX = postPositions[id];
	slideTo(postSlideCfg);
	$('.post-pagination li.active').removeClass('active');
	$('.post-pagination li a[href="#post' + id + '"]').parent().addClass('active');
	pos = Math.max(0, paginatorNumberPositions[id]
			- $('.post-pagination .number-container').width() / 2);
	paginationSlideCfg.isSliding = true;
	paginationSlideCfg.destinationX = pos;
	slideTo(paginationSlideCfg);
//	$('.post-pagination .number-container ul').css('left', -nrPos + 'px');
	return false;
}

function gotoPrevPost() {
	id = 0;
	while (postPositions[id] < postSlideCfg.el.scrollLeft()) {
		id++;
	}
	gotoPost(id == 0 ? 0 : id - 1);
	return false;
}

function gotoNextPost() {
	id = 0;
	while (postPositions[id] < postSlideCfg.el.scrollLeft()) {
		id++;
	}
	gotoPost(id == postPositions.size - 1 ? postPositions.size - 1 : id + 1);
	return false;
}

function initPostPositions() {
	postPositions = Array();
	els = $('.posts').children();
	w = postsPadding;
	postContainerWidth = $('#post-container').width();
	for (i = 0; i < els.size(); i++) {
		centerDelta = (postContainerWidth - $(els[i]).width() - MARGIN_AND_BORDERS) / 2;
		postPositions.push(w - centerDelta);
		w += $(els[i]).width() + MARGIN_AND_BORDERS;
	}
	$('.posts').width(w);
	return w;
}

var paginatorNumberPositions;

function initPagination() {
	mul = $('.post-pagination .number-container ul');
	els = mul.children();
	paginatorNumberPositions = Array();
	for (i = 0; i < els.size(); i++) {
		paginatorNumberPositions.push($(els[i]).width()
				+ (i > 0 ? paginatorNumberPositions[i - 1] : 0))
	}
	mul.width(paginatorNumberPositions[els.size()-1]);
}

function calculatePositions() {
	// calculate the posts padding
	// TODO figure out wtf is wrong here, and maybe fix it - not urgent
	// postsPadding = $('.span10').width()/4;
	// adds a padding so we can center the first & last elements too
	// $('.posts').css('padding-left', postsPadding);
	// $('.posts').css('padding-right', postsPadding);

	// initializes the positions of the posts
	initPostPositions();

	initPagination();

	// makes posts visible (they were hidden with css for preloading)
	$('.posts').css('position', 'static');
	$('.posts').css('top', null);

	// center paginator
	postsWidth = $('#post-container').width();
	paginationWidth = $('.post-pagination').width();
	// show it (it was hidden by css)
	$('.post-pagination').css('position', 'static');

}

$(window).load(function() {
	postSlideCfg.el = $('#post-container');
	paginationSlideCfg.el = $('.post-pagination .number-container');
	calculatePositions();
	// remove the loader
	$('#loader').remove();
	// scrolls to the 1st pos
	postSlideCfg.el.scrollLeft(500);
	gotoPost(0);
});