
    // let age = document.getElementById("age-btns");

	// age.addEventListener('click', function onClick() {
	// 	activeOption = '';
	// 	// console.log('lunch Pressed');
	// 	age.style.backgroundColor = "#ff9f46";
	// 	dinnerButton.style.backgroundColor = '';

	// });

	let activeRaces = {};
	let races = document.getElementsByClassName("raceButtons");

	let raceSelected = false;

	// console.log(races);

	for (btn of races) {
		// console.log(btn);
		activeRaces[btn.id] = false;
	}

	function updateRaces() {
		
		for (let i = 0; i < races.length; i++) {
			let btn = races[i];
			if (btn.getAttribute("value") == "Unknown") {
				btn.style.backgroundColor = "#ff911f";
				activeRaces[btn.id] = true;
			}

			btn.addEventListener('click',
				function () {
					let race = btn.id;
					// select Dhall
					if (!activeRaces[race]) {
						btn.style.backgroundColor = "#ff911f";
						activeRaces[race] = true;
					}
					else {
						btn.style.backgroundColor = "";
						activeRaces[race] = false;
					}
	
				});
		}

	}


	// function check(tagName)
	// {
	// 	var check=document.getElementsByTagName(tagName);
	// 	if (!check[i].checked){
	// 		check[i].checked=true;
	// 	}
	// }
	// function uncheck(tagName)
	// {
	// 	var uncheck=document.getElementsByTagName(tagName);
	// 	if (uncheck[i].checked){
	// 		uncheck[i].checked=false;
	// 	}
	// }
	function validateForm() {
		
		var x = document.forms["patronForm"]["guessed"].value;
		console.log(x)
		if (x == '') {
		alert("Please select True or False for Guess.");
			return false;
		}
		return true;
	}
	

	// clearAll.addEventListener('click',
	// 	function(){

	// 		if(raceSelected) {
    //             for(let i = 0; i < dHallButtons.length; i++)
	// 		    {
    //                 let btn = races[i];
                    
    //                 // deactivate all buttons
    //                 activeRaces[btn.id] = false;
    //                 btn.style.backgroundColor = "";
	// 		    }
	// 		// flip active flag
	// 		raceSelected = !raceSelected;

    //         }
	// 	});


	// update url to contain proper match request information
	function updateUrl() {
		// let url = $('#patronForm').attr('action');

        // url += "&race=";
		if (validateForm()) {
			let raceOptions = "";

			for (var race of races) {
				if (activeRaces[race.id]) {
					raceOptions += (race.value + "-");
				}
			}

			if (!Object.values(activeRaces).every(x => !x)) {
				raceOptions = raceOptions.substring(0, raceOptions.length - 1);
			}

			$('#race-input-for-submission').val(raceOptions);
		}
		
		// url += raceOptions;

		// return url;
		// $('#patronForm').attr('action', url);
	}

	function setup() {
		updateRaces();
		// $('#patronForm').on('submit', event => {
		// 	// event.preventDefault();
		// 	console.log("hello")
		// 	updateUrl();
		// });
		// return;
		$('#submit').on('click', updateUrl);
	}

    $('document').ready(setup);
