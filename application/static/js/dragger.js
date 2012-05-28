var draggerConfig = {
	/**
	 *  the element to be scrolled by the drag
	 */
	el: null,
	/**
	 * is true if the element is dragged
	 */
	isDragging: false,
	/**
	 * the previous position of the mouse (set in startedDragHandler/isDraggingHandler)
	 */ 
	prevX: 0,
	/**
	 * Stores the value of the momentum <br/>
	 * (which is defined based on how fast you moved the mouse before releasing)
	 */
	momentum: 0,
	/**
	 * How fast we decrease the momentum (friction)
	 */
	momentumChange: .9,
	/**
	 * Marks a state where we've released the mouse, and we let the scrolled element slide 
	 */
	isSliding: false,
	/**
	 * The timeout value of the movement (in ms)
	 */
	timeoutL: 30, 
}

$(window).load(function() {
	// disable all clickevents on posts
	$('.posts *').mousedown(function(e){e.preventDefault();});
	// disable ctxt menu
	document.oncontextmenu = function() {return false;};

	//register listeners
	draggerConfig.el = $('#post-container');
	draggerConfig.el.mousedown(startedDragHandler);
	$('body').mouseup(stoppedDragHandler);
	$('body').mouseleave(stoppedDragHandler);
	$('body').mousemove(isDraggingHandler);
});

function stoppedDragHandler(event){
	draggerConfig.isDragging = false;
	draggerConfig.isSliding = true;
	setTimeout(slideAfterDrag, draggerConfig.timeoutL);
}

function slideAfterDrag(){
	
	draggerConfig.el.scrollLeft(draggerConfig.el.scrollLeft() + draggerConfig.momentum);
	draggerConfig.momentum *= draggerConfig.momentumChange;
	if(Math.abs(draggerConfig.momentum) <= 3){
		draggerConfig.momentum = 0;
		draggerConfig.isSliding = false;
	}
	if(draggerConfig.isSliding){
		setTimeout(slideAfterDrag, draggerConfig.timeoutL);
	}
}

function isDraggingHandler(event){
	if(draggerConfig.isDragging){
		draggerConfig.momentum =- event.pageX + draggerConfig.prevX;
		draggerConfig.el.scrollLeft(draggerConfig.el.scrollLeft() + draggerConfig.momentum);
		draggerConfig.prevX = event.pageX;
	}
}

function startedDragHandler(event){
	//stop the event
	event.stopImmediatePropagation();
	draggerConfig.isSliding = false;
	draggerConfig.momentum = 0;
	draggerConfig.isDragging = true;
	draggerConfig.prevX = event.pageX;
}