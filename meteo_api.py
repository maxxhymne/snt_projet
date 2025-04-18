from flask import Flask, request, jsonify
import requests, json, time, os

app = Flask(__name__)

# Vêtements disponibles dans la penderie
wardrobe = {
    "froid": {
        "min_temp": -10,
        "max_temp": 10,
        "conditions": ["clear", "clouds"]
    },
    "tiède": {
        "min_temp": 10,
        "max_temp": 20,
        "conditions": ["clear", "clouds"]
    },
    "chaud": {
        "min_temp": 20,
        "max_temp": 40,
        "conditions": ["clear", "clouds"]
    },
    "pluie": {
        "min_temp": 0,
        "max_temp": 40,
        "conditions": ["rain", "drizzle"]
    },
    "neige": {
        "min_temp": -10,
        "max_temp": 10,
        "conditions": ["clear", "snow"]
    },
}


# Classe pour gérer la mise en cache
class WeatherCache:

    def __init__(self,
                 cache_file='weather_cache.json',
                 cache_duration=1800):
        self.api_key = "8d5011512ff6bce5ac50f5c8e9d4246a"
        self.cache_file = cache_file
        self.cache_duration = cache_duration

    def _load_cache(self, city):
        if os.path.exists(self.cache_file):
            with open(self.cache_file, 'r') as f:
                cache = json.load(f)
                if city in cache:
                    entry = cache[city]
                    if time.time() - entry['timestamp'] < self.cache_duration:
                        return entry['data']
        return None

    def _save_cache(self, city, data):
        cache = {}
        if os.path.exists(self.cache_file):
            with open(self.cache_file, 'r') as f:
                cache = json.load(f)
        cache[city] = {'timestamp': time.time(), 'data': data}
        with open(self.cache_file, 'w') as f:
            json.dump(cache, f)

    def get_weather(self, city='paris'):
        cached = self._load_cache(city)
        if cached:
            return cached

        url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.api_key}&units=metric&lang=fr'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            self._save_cache(city, data)
            return data
        return None


weather_cache = WeatherCache()


# Fonction de recommandation de vêtements
def recommend_clothes(temp, condition):
    results = []
    for item, rule in wardrobe.items():
        if rule['min_temp'] <= temp <= rule['max_temp'] and condition in rule[
                'conditions']:
            results.append(item)
    return results


# Route principale de l’API
@app.route('/getWeather')
def weather_route():
    city = request.args.get('city')
    if not city:
        return jsonify({'error': 'City required'}), 400

    data = weather_cache.get_weather(city)
    if data:
        temp = data['main']['temp']
        condition = data['weather'][0]['main'].lower()

        recommended = recommend_clothes(temp, condition)

        return jsonify({
            'city': data['name'],
            'temp': temp,
            'description': data['weather'][0]['description'],
            'recommended_clothes': recommended
        })
    else:
        return jsonify({'error': 'impossible de fetch'}), 500


if __name__ == '__main__':
    app.run(debug=True)
