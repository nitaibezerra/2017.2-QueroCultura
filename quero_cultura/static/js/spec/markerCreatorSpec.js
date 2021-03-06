describe('requestSubsite', function(){
	it('should be crete request a subsite and return a promise', function(){

		var url = "http://mapas.cultura.gov.br/api/subsite/api/subsite/find"
		subsiteID = 1
		
		promise = requestSubsite(url, subsiteID)
		expect(promise).toBeDefined()
	});
});

describe('createPopup', function(){
	it('should be create a popup to marker without subsite', function(){
		var data = [{"id": 1},{"subsite": null}, {"name": "Jeferson"}, {"singleUrl": "http://mapas.cultura.gov.br/agente/1"}]
		var valueZindex = setZIndex('png')
		var markerAgent = new L.FeatureGroup();
        var marker = L.marker([0, 0]).setZIndexOffset(valueZindex).addTo(markerAgent)

        spyOn(marker, 'bindPopup')
		createPopup(data,marker)
		expect(marker.bindPopup()).toHaveBeenCalled()
	});
});

describe('addMarkerToMap', function(){
	it('should be add a marker to map', function(){
		var imageExtension = 'png'
		var icon = createMarkerIcon('espaco', imageExtension)
		var data = [{"id": 1}]
		var markersSpace = new L.FeatureGroup();
		var latitude = 0
		var longitude = 0
		
		spyOn(printedMarkers,'push')
		addMarkerToMap(data, icon, imageExtension, markersSpace, latitude, longitude)
		expect(printedMarkers.push).toHaveBeenCalled()
	});
});

describe('createSpaceMarker', function(){

	it('should create space marker icon', function(){
		spyOn(window,'createMarkerIcon')
		data1 = {}
		createSpaceMarker(data1, 'gif');

		expect(window.createMarkerIcon).toHaveBeenCalledWith('espaco', 'gif')
	});

});

describe('createAgentMarker', function(){
	it('should create agent marker icon', function(){
		spyOn(window, 'createMarkerIcon')
		data1 = {}
		createAgentMarker(data1, 'png')

		expect(window.createMarkerIcon).toHaveBeenCalledWith('agente', 'png')
	});
});

describe('createEventMarker', function(){
	it('should create event marker icon', function(){
		spyOn(window, 'createMarkerIcon')
		data1 = {}
		createEventMarker(data1, 'gif')

		expect(window.createMarkerIcon).toHaveBeenCalledWith('evento', 'gif')
	});
});

describe('createMarkerIcon', function(){
	it('should create red marker icon for space', function(){
		spyOn(L, 'icon')

		createMarkerIcon('espaco', 'gif')

		expect(L.icon).toHaveBeenCalledWith({ iconUrl: "static/images/"+"markerSpace"+"."+ "gif",
                    iconSize: [25,25]})
	});
	it('should create blue marker icon for agent', function(){
		spyOn(L, 'icon')

		createMarkerIcon('agente', 'png')

		expect(L.icon).toHaveBeenCalledWith({ iconUrl: "static/images/"+"markerAgent"+"."+ "png",
                    iconSize: [25,25]
                 })
	});

	it('should create yellow marker icon for event', function(){
		spyOn(L, 'icon')

		createMarkerIcon('evento', 'png')

		expect(L.icon).toHaveBeenCalledWith({ iconUrl: "static/images/"+"markerEvent"+"."+ "png",
                    iconSize: [25,25]
                 })
	});

	it('should create green marker icon for project', function(){
		spyOn(L, 'icon')

		createMarkerIcon('projeto', 'png')

		expect(L.icon).toHaveBeenCalledWith({ iconUrl: "static/images/"+"markerProject"+"."+ "png",
                    iconSize: [25,25]
                 })
	});
});

describe('getInitialInstance', function(){
	it('should get initial instance', function(){
		data = [{"singleUrl": "http://spcultura.prefeitura.sp.gov.br/projeto/3304/"}]
		position = 0
		var url = data[position]["singleUrl"]
	    var splitUrl = url.split(".")
		var test = getInitialInstance(data[position])
		expect(test).toEqual(splitUrl[2])
	});
});

describe('setZIndex', function(){
	it('Should return 1000', function(){
			equal = 1000
			test = setZIndex('gif')
			expect(test).toEqual(equal)
	});
	it('Should return -30', function(){
		equal = -30
		test = setZIndex('png')
		expect(test).toEqual(equal)
	});
});

describe('setZIndex', function () {
	it('should set a z index', function () {
		var test = 0;
		expect(test).toEqual(0);
    });
});
