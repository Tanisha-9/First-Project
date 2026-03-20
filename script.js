const apiKey = "8fcb4f616b633eac4a1ceb1a800bb223"; // paste your key

// 🌍 Get weather by city
function getWeather() {
    const city = document.getElementById("city").value;

    if (city === "") {
        alert("Please enter a city name");
        return;
    }

    fetchWeather(city);
}

// 📍 Get weather using location
function getLocationWeather() {
    navigator.geolocation.getCurrentPosition(position => {
        const lat = position.coords.latitude;
        const lon = position.coords.longitude;

        // Current weather
        const url = `https://api.openweathermap.org/data/2.5/weather?lat=${lat}&lon=${lon}&appid=${apiKey}&units=metric`;

        fetch(url)
            .then(res => res.json())
            .then(data => {
                console.log("Current:", data);

                if (data.cod !== 200) {
                    alert("Error: " + data.message);
                    return;
                }

                displayWeather(data);

                // ✅ BEST FIX: use coordinates for forecast
                getForecastByCoords(lat, lon);
            })
            .catch(err => console.log("Location Error:", err));
    });
}

// 🌡️ Fetch weather by city
function fetchWeather(city) {
    const url = `https://api.openweathermap.org/data/2.5/weather?q=${city}&appid=${apiKey}&units=metric`;

    fetch(url)
        .then(res => res.json())
        .then(data => {
            console.log("City Weather:", data);

            if (data.cod !== 200) {
                alert("Error: " + data.message);
                return;
            }

            displayWeather(data);

            // Forecast using city
            getForecast(city);
        })
        .catch(err => console.log("Fetch Error:", err));
}

// 🧾 Display current weather
function displayWeather(data) {
    document.getElementById("cityName").innerText = data.name;
    document.getElementById("temp").innerText = "Temp: " + data.main.temp + "°C";
    document.getElementById("humidity").innerText = "Humidity: " + data.main.humidity + "%";
    document.getElementById("wind").innerText = "Wind: " + data.wind.speed + " m/s";
}

// 📅 Forecast by city
function getForecast(city) {
    const url = `https://api.openweathermap.org/data/2.5/forecast?q=${city}&appid=${apiKey}&units=metric`;

    fetch(url)
        .then(res => res.json())
        .then(data => {
            console.log("Forecast (City):", data);

            if (data.cod !== "200") {
                alert("Forecast Error: " + data.message);
                return;
            }

            displayForecast(data);
        })
        .catch(err => console.log("Forecast Error:", err));
}

// 📍 Forecast by coordinates (BEST METHOD)
function getForecastByCoords(lat, lon) {
    const url = `https://api.openweathermap.org/data/2.5/forecast?lat=${lat}&lon=${lon}&appid=${apiKey}&units=metric`;

    fetch(url)
        .then(res => res.json())
        .then(data => {
            console.log("Forecast (Coords):", data);

            if (data.cod !== "200") {
                alert("Forecast Error: " + data.message);
                return;
            }

            displayForecast(data);
        })
        .catch(err => console.log("Forecast Error:", err));
}

// 📊 Display forecast
function displayForecast(data) {
    const forecastDiv = document.getElementById("forecast");
    forecastDiv.innerHTML = "";

    // every 8th item = next day
    for (let i = 0; i < data.list.length; i += 8) {
        const day = data.list[i];

        const div = document.createElement("div");

        div.innerHTML = `
            <p>${new Date(day.dt_txt).toDateString()}</p>
            <p>${day.main.temp}°C</p>
        `;

        forecastDiv.appendChild(div);
    }
}

// 🌙 Dark mode toggle
function toggleDarkMode() {
    document.body.classList.toggle("dark");
}