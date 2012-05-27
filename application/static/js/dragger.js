//the dragged draggerElement

var draggerEl;
var isDragging = false;
var startX = 0
var prevX = 0;


$(window).load(function() {
	//disable all clickevents on posts
	$('.posts *').mousedown(function(e){e.preventDefault();});
	//register listeners
	draggerEl = $('#post-container');
	draggerEl.mousedown(startedDragHandler);
	$('body').mouseup(stoppedDragHandler);
	$('body').mouseleave(stoppedDragHandler);
	$('body').mousemove(isDraggingHandler);
});

function stoppedDragHandler(event){
	isDragging = false;
}

function isDraggingHandler(event){
	if(isDragging){
		draggerEl.scrollLeft(draggerEl.scrollLeft() - event.pageX + prevX);
		prevX = event.pageX;
	}
}

function startedDragHandler(event){
	//stop the event
	event.stopImmediatePropagation();
	isDragging = true;
	prevX = event.pageX;
}