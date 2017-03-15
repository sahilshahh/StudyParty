var dotVar = document.querySelector("#dot");
var container = document.querySelector("#contentContainer");
container.addEventListener("click", updateLocation);
function updateLocation(){
	document.getElementById('top_label').value = dotVar.style.top.replace("px", "");
	document.getElementById('left_label').value = dotVar.style.left.replace("px", "");
	//document.forms["generateLink"].submit();
}