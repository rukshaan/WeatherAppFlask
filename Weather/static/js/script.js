//Add city script
document.getElementById('searchX').onsubmit = function(event) {
    event.preventDefault(); // Prevent default form submission
    addCity();
};

function addCity() {
    const cityName = document.getElementById("cityInput").value.trim();
    if (!cityName) {
        alert("Please enter a city name.");
        return false; // Prevent form submission
    }

    const requestData = {
        city_name: cityName
    };
    
console.log(requestData.city_name)
    fetch('/add_city', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        
        body:  JSON.stringify(requestData),

        
    })
    .then(response => response.json())
    .then(data => {
        
       alert(data.data)
    })
    .catch(error => {
        console.error('Error:', error);
        alert('There was an error adding the city. Please try again.');
    });

    return false; // Prevent form submission
}



// Function to fetch prediction files and populate the select input
function populatePredictionFiles() {
    fetch('/get_prediction_files')
        .then(response => response.json())
        .then(files => {
            const citySelect = document.getElementById('city');
            if (citySelect) {
                // Clear existing options
                citySelect.innerHTML = '<option value="">Choose a city</option>';

                // Add new options for each prediction file
                files.forEach(file => {
                    // const cityName = file.replace('_next_7_days_predictions.xlsx', '');
                    // const cityName = file.replace('_next_7_days_predictions.pdf', '');
                    const cityName = file.split('next')[0].replace(/_/g, ' ');
                    const option = document.createElement('option');
                    option.value = cityName;
                    option.textContent = cityName;
                    citySelect.appendChild(option);
                });
            }
        })
        .catch(error => console.error('Error fetching prediction files:', error));
}

// Call the function when the report modal is opened
const reportBtn = document.getElementById('reportBtn');
if (reportBtn) {
    reportBtn.addEventListener('click', () => {
        populatePredictionFiles(); // Populate the select input when the modal is opened
    });
}
// ============ For Report Modal ============//
// Report Modal Functionality
const modal = document.getElementById("reportModal");
const btn = document.getElementById("reportBtn");
const span = document.getElementsByClassName("close")[0];

if (btn && modal && span) {
    btn.onclick = () => {
        console.log("Report button clicked"); // Debugging
        modal.style.display = "block";
    };
    span.onclick = () => {
        console.log("Close button clicked"); // Debugging
        modal.style.display = "none";
    };
    window.onclick = (event) => {
        if (event.target === modal) {
            console.log("Modal background clicked"); // Debugging
            modal.style.display = "none";
        }
    };
}

// City Selection Functionality for Report Modal
const addBtn = document.querySelector('.add-btn');
const cityList = document.getElementById('cityList');
const citySelect = document.getElementById('city');
const cityTable = document.getElementById('cityTable');
const noCitiesMessage = document.getElementById('noCities');

if (addBtn && cityList && citySelect && cityTable && noCitiesMessage) {
    addBtn.addEventListener('click', () => {
        const selectedOption = citySelect.options[citySelect.selectedIndex];
        if (!selectedOption.value) {
            console.log("No city selected"); // Debugging
            return;
        }

        const cityName = selectedOption.textContent;
        const existingCities = [...cityList.children].map(row => row.cells[0].textContent);

        if (existingCities.includes(cityName)) {
            console.log("City already added:", cityName); // Debugging
            alert('This city is already added!');
            return;
        }

        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${cityName}</td>
            <td><button class="remove-btn">Remove</button></td>
        `;

        row.querySelector('.remove-btn').addEventListener('click', () => {
            console.log("Remove button clicked for city:", cityName); // Debugging
            row.remove();
            updateTableVisibility();
        });

        cityList.appendChild(row);
        console.log("City added to list:", cityName); // Debugging
        updateTableVisibility();
    });

    function updateTableVisibility() {
        const hasCities = cityList.children.length > 0;
        cityTable.classList.toggle('show', hasCities);
        noCitiesMessage.classList.toggle('hidden', hasCities);
        console.log("Table visibility updated. Has cities:", hasCities); // Debugging
    }
}

// Form Submission Handler for Report Modal
const reportForm = document.getElementById('reportForm');
if (reportForm) {
    reportForm.onsubmit = function(e) {
        e.preventDefault();

        const cities = [...cityList.children].map(row => ({
            name: row.cells[0].textContent,
            value: row.cells[0].textContent.toLowerCase()// Convert city name to match backend format  .replace(' ', '_') 
        }));

        if (cities.length === 0) {
            console.log("No cities selected for report"); // Debugging
            alert('Please add at least one city!');
            return;
        }

        const email = document.getElementById('email').value;
        const formData = {
            email: email,
            cities: cities
        };

        console.log('Submitting report data:', formData); // Debugging

        // Send the data to the Flask backend
        fetch('/send_report', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Email sent successfully!');
                modal.style.display = "none";
                reportForm.reset();
                cityList.innerHTML = '';
                updateTableVisibility();
            } else {
                alert('Failed to send email: ' + data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while sending the email.');
        });
    };
}
// =========== End Report Modal ============ //
document.getElementById('getWeatherBtn').addEventListener('click', function(event) {
    event.preventDefault();
    const cityName = document.getElementById('city_select').value;
    if (!cityName) {
        alert('Please select a city.');
        return;
    }

    // Fetch current weather data for the selected city
    fetch('/cityName', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ city_name: cityName })
    })
    .then(response => response.json())
    .then(data => {
        // console.log("Received",data)
        const weatherDetails = data.weather_details;
        const predictions_name=data.predictions;
        // console.log("checking...",weatherDetails)
        console.log("checking Prediction...",predictions_name)
            const localTime = new Date(weatherDetails.localtime);  // Convert to Date object

            const options = { weekday: 'short', day: 'numeric', month: 'short', year: 'numeric' };
            const formattedDate = localTime.toLocaleDateString('en-GB', options);

            const timeOptions = { hour: '2-digit', minute: '2-digit', hour12: true };
            const formattedTime = localTime.toLocaleTimeString('en-GB', timeOptions);
            
         //   Update the HTML with the received current weather data
            document.getElementById('cityDisplay').innerText = weatherDetails.name+', ' + weatherDetails.country;; // City name
            document.getElementById('descriptionDisplay').innerText = weatherDetails.condition; // Weather description
            document.getElementById('windDisplay').innerText = `wind : ${weatherDetails.wind_kph}   kph`; // Wind speed
            document.getElementById('humidityDisplay').innerText = `Humidity :${weatherDetails.humidity}  %`; // Humidity
            document.getElementById('dateDisplay').innerText = formattedDate
            document.getElementById('timeDisplay').innerText = formattedTime;
            // document.getElementById('cityDisplay').innerText = formattedTime;

              // Display 7-day predictions
              const forecastContainer = document.getElementById('forecastContainer');
              const forecastGrid1 = document.createElement('div');
              
              forecastGrid1.style.display="flex";
              forecastGrid1.style.flexDirection = "row";
              forecastGrid1.style.justifyContent = "space-around";
              
            //   const days = ['Tue', 'Wed', 'Thu', 'Fri', 'Sat','Sun', 'Mon']; // Expanded days for additional temps
              
                
              const days = getNextSevenDays(localTime);  // Get dynamic days for the forecast 
              // Display the forecast for each day
              predictions_name.forEach((temperature, index) => {


                const forecastGrid = document.createElement('div');
                forecastGrid.style.display = "flex";
                forecastGrid.style.flexDirection = "column";
              
                //   const category = getTemperatureCategory(temperature); // Get category based on temperature
                //   const day = days[index % days.length]; // Cycle through days array (this handles index overflow)
                const day = days[index]
                const temperature1 = temperature.toFixed(1); 

                const img = document.createElement('img');
                if (temperature <= -10) {
                    img.src = "static/img/25.svg";  // -10°C and below
                } else if (temperature > -10 && temperature <= -5) {
                    img.src = "static/img/15.svg";  // -9°C to -5°C
                } else if (temperature > -5 && temperature <= 0) {
                    img.src = "static/img/16.svg";  // -4°C to 0°C
                } else if (temperature > 0 && temperature <= 2) {
                    img.src = "static/img/14.svg";  // 1°C to 2°C
                } else if (temperature > 2 && temperature <= 4) {
                    img.src = "static/img/17.svg";  // 3°C to 4°C
                } else if (temperature > 4 && temperature <= 6) {
                    img.src = "static/img/12.svg";  // 5°C to 6°C
                } else if (temperature > 6 && temperature <= 8) {
                    img.src = "static/img/11.svg";  // 7°C to 8°C
                } else if (temperature > 8 && temperature <= 10) {
                    img.src = "static/img/31.svg";  // 9°C to 10°C
                } else if (temperature > 10 && temperature <= 12) {
                    img.src = "static/img/27.svg";  // 11°C to 12°C
                } else if (temperature > 12 && temperature <= 14) {
                    img.src = "static/img/26.svg";  // 13°C to 14°C
                } else if (temperature > 14 && temperature <= 16) {
                    img.src = "static/img/23.svg";  // 15°C to 16°C
                } else if (temperature > 16 && temperature <= 18) {
                    img.src = "static/img/24.svg";  // 17°C to 18°C
                } else if (temperature > 18 && temperature <= 20) {
                    img.src = "static/img/23.svg";  // 19°C to 20°C
                } else if (temperature > 20 && temperature <= 25) {
                    img.src = "static/img/35.svg";  // 21°C to 25°C
                } else if (temperature > 25 && temperature <= 30) {
                    img.src = "static/img/36.svg";  // 26°C to 30°C
                } else {
                    img.src = "static/img/3200.svg";  // Above 30°C (extreme heat)
                }
                
                img.alt = "weather icon";
                img.style.width = "40px";
                img.style.height = "40px";

        const temp = document.createElement('h6');
        temp.innerText = `${temperature1}°C`; 
        temp.style.color = 'red';

        const dayElement = document.createElement('h6');
        dayElement.innerText = day;
                
                forecastGrid.appendChild(dayElement)
                forecastGrid.appendChild(img)
                forecastGrid.appendChild(temp)
                forecastContainer.innerHTML = ""; 
                forecastGrid1.appendChild(forecastGrid);

                
              
                  // Display image for the category
                 
              
                  // Append the forecast div to the forecast container
                //   forecastContainer.appendChild(forecastDiv);
              });
              forecastContainer.appendChild(forecastGrid1);
              



    })
    .catch(error => {
        console.error('Error:', error);
        alert(error);
    });
});

// Function to get the next 7 days dynamically
function getNextSevenDays(currentDate) {
    const days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
    const currentDayIndex = currentDate.getDay(); // Get the index of the current day (0 for Sunday, 1 for Monday, etc.)

    let forecastDays = [];
    for (let i = 0; i < 7; i++) {
        const nextDayIndex = (currentDayIndex + i) % 7; // Cycle through the week
        forecastDays.push(days[nextDayIndex]);
    }

    return forecastDays;
}