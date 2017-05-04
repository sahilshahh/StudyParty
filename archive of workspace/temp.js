function CircleTableFacade() {

	const 	source = document.getElementById("ct"),
			// Components
			ellipse = source.getElementById("ellipse"),
			glare_clip_def = source.getElementById("glare_clip_def"),
			leg = source.getElementById("leg"),
			edge = source.getElementById("edge"),
			top = source.getElementById("top"),
			glare_instance = source.getElementById("glare_instance");
	
	this.updateTilt = function(x) {

		...

		ellipse.setAttributeNS(null, 'ry', c);
		glare_clip_def.setAttributeNS(null, 'y', 50-s);
		leg.setAttributeNS(null, 'height', s);
		leg.setAttributeNS(null, 'y', 50-s);
		leg.setAttributeNS(null, 'rx', 7.5*(c/50));
		edge.setAttributeNS(null, 'y', 50-s);
		edge.transform.baseVal.getItem(0).setScale(1,1+v);
		edge.transform.baseVal.getItem(1).setTranslate(0,o);
		top.setAttributeNS(null, 'y', 50-s);
		glare_instance.setAttributeNS(null, 'height', 2*c);
		glare_instance.setAttributeNS(null, 'y', 50-2*s);
	}
}

function registerTiltHandler(input, display, handler) {
			
			...

			animate = function() {
					var v = min + x*range;
					input.value = v;
					display.value = (90*v).toFixed(0);
					handler(x);
					scheduledAnimationFrame = false;
				},
			
			...
}

var input = document.getElementById("ct_tilter"),
	display = document.getElementById("ct_current_tilt"),
	handler = (new CircleTableFacade()).updateTilt;

registerTiltHandler(input,display,handler);

