// Copyright 2001-2003 Villario, villario@yahoo.com

function TableOut(){
	clearTimeout(TimerID);
    TimerID = setTimeout("ShowLayers('None')", TimeLayerOut);
}

function TableOver(ActiveLayer){
	clearTimeout(TimerID);
	if(ActiveLayer == LinkLayer){
		clearTimeout(TimerIDLink);
		WaitLink = 0;
	}
	ShowLayers(ActiveLayer);
}

function ResetWaitLink(ActiveLayer){
	WaitLink = 0;
	clearTimeout(TimerIDLink);
	ShowLayers(ActiveLayer);
}

function LinkOut(ActiveLayer){
	IsLink = "NO";
	WaitLink = 1;
    TimerIDLink = setTimeout("ResetWaitLink('" + ActiveLayer + "')", TimeLinkOut);
	TableOut();
}

function LinkOver(ActiveLayer){
	clearTimeout(TimerID);
	clearTimeout(TimerIDLink);
	WaitLink = 0;
	LinkLayer = ActiveLayer;
	IsLink = ActiveLayer;
	ShowLayers(ActiveLayer);
}

function ShowLayers(ActiveLayer){
	
	if (IsLink != "NO") ActiveLayer = IsLink;

	if (ActiveLayer == "None"){
		var imgCount = 1;
		do {
			imageId = ("I" + imgCount);
			imageOff = (imageId + "off");
			imgCount++;	 
			changeImages(imageId, imageOff);
		} while (imgCount <= numOfImages); 
	}

	if (PrevLayer != ActiveLayer && WaitLink == 0){
	
		for(i=0; i<layerCount;i++){
			if (is_nav4) {
				document.layers[layersList[i]].visibility='hide';
			} else if (is_ie4) {
				document.all[layersList[i]].style.visibility='hidden';
			} else if (is_domcom) {
				document.getElementById(layersList[i]).style.visibility='hidden';
			}

			if (ActiveLayer.search(layersList[i]) > -1){
				if (is_nav4) {
					document.layers[layersList[i]].visibility='show';
				} else if (is_ie4) {
					document.all[layersList[i]].style.visibility='visible';
				} else if (is_domcom) {
					document.getElementById(layersList[i]).style.visibility='visible';
				}
			}
		}
		PrevLayer = ActiveLayer;
	}
}

function showMenu(ActiveLayer, image){
	
	var imgCount = 1

	do {
		var imageId = ("I" + imgCount);
		var imageOn = (imageId + "on");
		var imageOff = (imageId + "off");
		imgCount++;	 
		if (image == imageId) {
			changeImages(image, imageOn);
		} else {
			changeImages(imageId, imageOff);
		}
	} while (imgCount <= numOfImages); 

	LinkOver(ActiveLayer);
}

function hideMenu(){
	LinkOut('');
}
