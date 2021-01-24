# weather api service
небольшое апи, возвращающее погоду по ip-адресу в формате ответа api.openweathermap.org

## сборка и установка
1. в папке с кодом выполнить
`bash buildrpm.sh ip2w.spec`
2. установить rpm
`sudo yum install ~/rpm/RPMS/noarch/ip2w-0.0.1-1.noarch.rpm`

## конфигурация
Конфиг сервиса находится по пути /usr/local/etc/ip2w/config.json

Для работы сервиса критичными являются параметры weather_api_token и proxies.

Для получения токена необходимо зарегистрироваться на openweathermap.org.

proxies описывается в виде словаря с ключами http и https.

Пример конфига:
```
{
    "proxies": {
       "http": "http://my.proxy.local:8080",
       "https": "http://my.proxy.local:8080"
    },
    "weather_api_url": "http://api.openweathermap.org/data/2.5/weather",
    "weather_api_token": "your-secret",
    "ipinfo_api_url": "https://ipinfo.io",
    "api_request_timeout": 10
}
```


## пример использования
`curl http://localhost/ip2w/176.14.221.123`

вывод (отформатирован для читаемости)
```
{
    "base": "stations",
    "clouds": {
        "all": 90
    },
    "cod": 200,
    "coord": {
        "lat": 55.7522,
        "lon": 37.6156
    },
    "dt": 1611496413,
    "id": 524901,
    "main": {
        "feels_like": 269.83,
        "humidity": 100,
        "pressure": 1011,
        "temp": 274.42,
        "temp_max": 274.82,
        "temp_min": 274.15
    },
    "name": "Moscow",
    "snow": {
        "1h": 0.27
    },
    "sys": {
        "country": "RU",
        "id": 9027,
        "sunrise": 1611466630,
        "sunset": 1611495946,
        "type": 1
    },
    "timezone": 10800,
    "visibility": 2400,
    "weather": [
        {
            "description": "mist",
            "icon": "50n",
            "id": 701,
            "main": "Mist"
        },
        {
            "description": "light snow",
            "icon": "13n",
            "id": 600,
            "main": "Snow"
        }
    ],
    "wind": {
        "deg": 140,
        "speed": 4
    }
}
```
