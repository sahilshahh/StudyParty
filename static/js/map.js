var dot = document.querySelector("#dot");
var container = document.querySelector("#contentContainer");
 
container.addEventListener("click", getClickPosition, false);
 
function getClickPosition(e) {
	var parentPosition = getPosition(e.currentTarget);
	var xPosition = e.clientX - parentPosition.x - (dot.clientWidth / 2);
	var yPosition = e.clientY - parentPosition.y - (dot.clientHeight / 2);
     
	dot.style.left = xPosition + "px";
	dot.style.top = yPosition + "px";
}
 
function getPosition(el) {
	var xPos = 0;
	var yPos = 0;
 
	while (el) {
		if (el.tagName == "BODY") {
			var xScroll = el.scrollLeft || document.documentElement.scrollLeft;
			var yScroll = el.scrollTop || document.documentElement.scrollTop;
 
			xPos += (el.offsetLeft - xScroll + el.clientLeft);
			yPos += (el.offsetTop - yScroll + el.clientTop);
		} else {
			xPos += (el.offsetLeft - el.scrollLeft + el.clientLeft);
			yPos += (el.offsetTop - el.scrollTop + el.clientTop);
		}
 
		el = el.offsetParent;
	}
	return {
		x: xPos,
		y: yPos
	};
}