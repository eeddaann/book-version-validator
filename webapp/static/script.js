pdfjsLib.GlobalWorkerOptions.workerSrc = "static/pdf.worker.js";

	var myState = {
		pdf: null,
		currentPage: 1,
		zoom: 1
	}
	function createTable(data) {
	var table = document.getElementById('resultTable');
	data.forEach(function(object) {
		var tr = document.createElement('tr');
		tr.innerHTML = '<td onclick="goToPage('+object[1]+')">' + object[0] + '</td>' +
		'<td>' + object[3] + '</td>' + '<td>' + object[2] + '</td>'
		table.appendChild(tr);
	});

	}

	function goToPage(i) {
	myState.currentPage = i;
	document.getElementById("current_page").value = myState.currentPage;
	render();
	}

	function render() {
		myState.pdf.getPage(myState.currentPage).then((page) => {
		
			var canvas = document.getElementById("pdf_renderer");
			var ctx = canvas.getContext('2d');
	
			var viewport = page.getViewport(myState.zoom);

			canvas.width = viewport.width;
			canvas.height = viewport.height;
		
			page.render({
				canvasContext: ctx,
				viewport: viewport
			});
		});
	}
	document.getElementById('go_first').addEventListener('click', (e) => {
		if(myState.pdf == null || myState.currentPage == 1) 
			return;
		myState.currentPage = 1;
		document.getElementById("current_page").value = myState.currentPage;
		render();
	});
	document.getElementById('go_previous').addEventListener('click', (e) => {
		if(myState.pdf == null || myState.currentPage == 1) 
			return;
		myState.currentPage -= 1;
		document.getElementById("current_page").value = myState.currentPage;
		render();
	});

	document.getElementById('go_next').addEventListener('click', (e) => {
		if(myState.pdf == null || myState.currentPage > myState.pdf._pdfInfo.numPages) 
			return;
		myState.currentPage += 1;
		document.getElementById("current_page").value = myState.currentPage;
		render();
	});

	document.getElementById('current_page').addEventListener('keypress', (e) => {
		if(myState.pdf == null) return;
		
		// Get key code
		var code = (e.keyCode ? e.keyCode : e.which);
		
		// If key code matches that of the Enter key
		if(code == 13) {
			var desiredPage = 
			document.getElementById('current_page').valueAsNumber;
								
			if(desiredPage >= 1 && desiredPage <= myState.pdf._pdfInfo.numPages) {
				myState.currentPage = desiredPage;
				document.getElementById("current_page").value = desiredPage;
				render();
			}
		}
	});

	document.getElementById('zoom_in').addEventListener('click', (e) => {
		if(myState.pdf == null) return;
		myState.zoom += 0.5;
		render();
	});

	document.getElementById('zoom_out').addEventListener('click', (e) => {
		if(myState.pdf == null) return;
		myState.zoom -= 0.5;
		render();
	});

	Dropzone.autoDiscover = false;
window.onload = function () {
	var dropzoneOptions = {
		timeout: -1,
		init: function () {
			this.on("success", function (file) {
				console.log("success > " + file.name);
				pdfjsLib.getDocument('./uploads/'+file.name).then((pdf) => {
				myState.pdf = pdf;
				render();
				document.getElementById("BigTable").style.display = "block";
				});
			});
			this.on("sending", function(file, xhr, formData){
				xhr.onreadystatechange = function() {
					if (xhr.readyState === 4) {
						var response = JSON.parse(xhr.responseText);
						if (xhr.status === 200) {
							createTable(JSON.parse(response))
							console.log('successful');
						} else {
							console.log('failed');
						}
					}
				}
			});
		}
	};
	var uploader = document.querySelector('#uploader');
	var newDropzone = new Dropzone(uploader, dropzoneOptions);
}