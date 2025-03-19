$(document).ready(function(){
    $('.dropdown-toggle').on('click', function(){
        $(this).next('.dropdown-menu').toggleClass('show');
    });

    $(document).on('click', '.city-link', function(){
        var city = $(this).data('city');
        $('#selected-city').text(city);
        $('.dropdown-menu').removeClass('show');

        fetch('/get_forecast', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ city: city })
        })
        .then(response => response.json())
        .then(data => {
            $('#current-temperature').text(data.current_temperature);
            $('#current-humidity').text(data.current_humidity);
            $('#current-wind').text(data.current_wind);
            $('#city').text(data.cityName);
            $('#current-icon').attr('src', `/static/img/weathericons/${data.icon}`);

            let forecastDates = '<th>Day</th>';
            let forecastTemperatures = '<td>Temperature (°C)</td>';
            let forecastIcons = '<td>Icon</td>';
            data.forecast.forEach(dayForecast => {
                forecastDates += `<th>${new Date(dayForecast.date).toLocaleDateString('en-US', { weekday: 'short' })}</th>`;
                forecastTemperatures += `<td>${dayForecast.forecast_temperature}°C</td>`;
                forecastIcons += `<td><img src="/static/img/weathericons/${dayForecast.icon}" alt="Weather icon"></td>`;
            });
            $('#forecast-dates').html(forecastDates);
            $('#forecast-temperatures').html(forecastTemperatures);
            $('#forecast-icons').html(forecastIcons);
        })
        .catch(error => console.error('Error:', error));
    });

    $('#add-city-btn').on('click', function(){
        $('#add-city-form').show();
    });

    $('#close-city-form-btn').on('click', function(){
        $('#add-city-form').hide();
        $('#new-city-name').val('');
    });

    $('#submit-city-btn').on('click', function(){
        var cityName = $('#new-city-name').val();
        fetch('/add_city', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ city: cityName }),
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message);  // Display alert with the response message
            if (data.success) {
                const dropdown = document.querySelector('.dropdown-menu');
                const newListItem = document.createElement('li');
                newListItem.setAttribute('role', 'presentation');
                newListItem.innerHTML = `<a href="javascript:void(0)" role="menuitem" class="city-link" data-city="${cityName}">${cityName}</a>`;
                dropdown.appendChild(newListItem);
                $('#new-city-name').val('');
                $('#add-city-form').hide();
            }
        })
        .catch(error => console.error('Error:', error));
    });
});
