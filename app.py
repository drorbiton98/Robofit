import os
import requests
from flask import Flask, render_template, request


KEY = os.getenv("WEATHER_API")


class Weather:
    def __init__(self, city):
        self.city = city
        self.deg = self.get_weather()

    def get_weather(self):
        req = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={self.city}&units=metric&appid={KEY}")
        det = req.json()
        try:
            return det['main']['temp']
        except KeyError:
            return None


class Robofit:
    def __init__(self, deg, pref, event):
        self.deg = deg
        self.pref = pref
        self.event = event
        self.heat_wave_dict = {
            'casual': {
                'hot': "we recommend some short chinos and a nice colorful t-shirt, add in some shades and you'll be looking extra fine!",
                'cold': "we recommend some short jeans and light button up shortsleeve shirt, add in another accessory that will match your shirt for some nice oomf!"
            },

            'sport': {
                'hot': "we really don't recommend for you to got work out with that weather, but if you have to, we will still recommend you going late at night or early at the morning, wear some light shorts and a tank top and drink a lot of water!",
                'cold': "please make sure you drink a lot of water! we recommend you going with some shorts and a light t-shirt."
            },

            'formal': {
                'hot': "we recommend you going for some light fitted trousers, and a nice roll sleeve shirt. bonus tip: wear a light undershirt to prevent unwanted armpit stains!",
                'cold': "we recommend you some plain fitted jeans and a nice shortsleeve shirt, add in a nice belt to emphasize your look!"
            },

            'elegant': {
                'hot': 'grab your favorite pair of jeans and a nice flattering t-shirt, to spice things up, got for some nice leather shoes!',
                'cold': 'we recommend a nice pair of your favorite jeans and a fitted button up shirt. play with the accessories to make it even more exciting!'
            }, 

            'comfy': {
                'hot': "it's a hot day and you don't want to feel to tight, we recommend a nice comfy shirt a loose, airy tank-top",
                'cold': "we recommend some nice, smooth shorts and a light oversized t-shirt, pair with some flip-flops for maximum comfiness!"
            },
        }

        self.hot_day_dict = {
            'casual': {
                'hot': "we recommend a nice pair of long chinos and your favorite t-shirt, grab a nice pair of sneakers and your good to go!",
                'cold': "we recommend a nice pair of jeans with a nice polo shirt for that sophisticated yet chill look! for bonus: add a nice matching watch!"
            },

            'sport': {
                'hot': "we recommend going for some shorts and light t-shirt, get yourself some nice comfortable shoes and don't forget to train harder then last time!",
                'cold': "your might still get a little chilly, go for some nice and stretchy shorts and light longsleeve t-shirt, go get it champ!"
            },

            'formal': {
                'hot': "we recommend some nice fitted trousers grouped together with a nice longsleeve button up, grab yourself a nice leather belt to compliment the look!",
                'cold': "it might be sweather time already for you, keep the colores neutral but don't be afraid to play around with the patters!"
            },

            'elegant': {
                'hot': "it's still hot out there, but not too much for your look to suffer! grab a nice pair of jeans and button up, to make your look, play around with the accessories"
            },

            'comfy': {
                'hot': "grab some comfy shorts and a nice comfy t-shirt, grab some slippers and make yourself nice and chill.",
                'cold': "we recommend you wearing some nice shorts and a light longsleeve t-shirt, make sure you choose a fabric that you like!"
            },
        }

        self.normal_day_dict = {
            'casual': {
                'hot': "Grab some nice cargo pants and pair it with a t-shirt and open jacket combo, and if you want to make it even better, add a nice bracelet to finish the look!",
                'cold': "Put on some nice jeans and a hoodie with a jacket on top, don't be afraid of layering your outfit, and make sure your sneaker game is on point!"
            },
            
            'sport': {
                'hot': "You might be a little chilly at start, but when you'll warmup it'll get better, grab some nice shorts and a comfy longsleeve.",
                'cold': "We recommend some nice and light joggers paired with a light hoodie, add in some warm socks to keep your ankles warm and secure!"
            },

            'formal': {
                'hot': "It's the time of the year we start seeing suits at the office, make sure they're fitted for an extra sharp look!",
                'cold': "Even better then the suit's, it's sweathers season! grab some nice trousers with your favorite sweather, and if you still need it add in a jacket on top!"
            },

            'elegant': {
                'hot': "Put on a nice pair of jeans with a nice button up, and add your favorite jacket on top! to make it even better choose some matching leather shoes and belt!",
                'cold': "Choose a nice and thick pair of jeans and pair it with a nice sweather and jacket combo! grab som nice boots to finish the look."
            },

            'comfy': {
                'hot': "Grab a nice pair of some baggy sweatpants with a nice and comfy hoodie, to finish off grab some nice boots without laces for extra laziness.",
                'cold': "We recommend some a nice comfy pair of sweatpants with hoodie and a thick undershirt to keep you extra warm!"
            },
        }

        self.cold_day_dict = {
            'casual': {
                'hot': "It's getting chilly... we recommend some nice cargo pants and jacket with light coat on top, grab some nice pair of boots to match the look!",
                'cold': "Grab a thick pair of cargo pants and pair with a nice hoodie and jacket combo, add to that a nice coat to make sure you warm but still looking fresh!"
            },

            'sport': {
                'hot': "We recommend a nice pair of joggers with a light longsleeve sweatshirt, put on some nice socks to keep your feet warm!",
                'cold': "Grab a nice pair of joggers and a thick hoodie, and if your planning to work out outside, grab some gloves to keep your hands from freezing!"
            },
            
            'formal': {
                'hot': "We recommend some nice and thick trousers and a nice blazer, add a nice long parka to keep your blazer fresh and dry!",
                'cold': "It's cold outside! put on some trousers and a nice and thick sweather with a jacket on top, add to that a nice puffy coat to keep you extra warm!"
            },

            'elegant': {
                'hot': "We recommend your favorite chinos with a nice jacket, add a nice coat on top and a nice pair of fancy boots!",
                'cold': "We recommend a nice pair of some thick jeans with a nice plain base sweatshirt, add a jacket on top and grab yourself a nice fury coat to finish the look and keep you warm!"
            },

            'comfy': {
                'hot': 'We recommend a nice pair of swatpants with a nice warm hoodie, keep it simple and warm but without a lot of layers.',
                'cold': "Even when it's cold we want to stay comfy! grab some thick pair of seatpants with a thick oversized hoodie, and a big puffy coat to keep you cosey!"
            },
        }

        self.super_cold_Day = {
            'casual': {
                'hot': "Put on a nice pair of thick chinos with a nice and warm jacket, top it off with a warm coat and some nice boots to finish the look!",
                'old': "Grab yourself a thick pair of cargopants and a hoodie and jacket combo, add a coat on top to keep yourself warm!"
            },

            'sport': {
                'hot': "Put on somme thick joggers and sweatshirt, some nice and thick socks and gloves. bonus tip - keep your heart rate up to keep yourself warm!",
                'cold': "Grab some thick sweatpants, a undershirt with a thick hoodie, make sure to warm up propely before you start your workout!"
            },

            'formal': {
                'hot': "Pair a nice pair of thick jeans with a thick sweather, put a nice blazer on top and make sure you grab your coat from the hanger!",
                'cold': "Grab some thick black jeans, put an undershirt with a thick sweather on top, and top it with a warm jacket. you'll probably need a coat when your out of the office!"
            },

            'elegant': {
                'hot': "Grab some nice thick denim and a thick sweatshirt, add a nice jacket on top and grab some gloves!",
                'cold': "We recommend some nice and warm jeans and a hoodie-jacket combo, top it with your favorite coat and put on some thick socks!"
            },

            'comfy': {
                'hot': "Grab some sweatpants and pair the with a nice hoodie, add a coat on top and make sure your not feeling to tight.",
                'cold': "We recommend you grabbing some thick sweatpants, grab a thick undershirt and pot a sweatshirt on top, add a big comfy coat and a pair of gloves!"
            }
        }

    def answer(self):
        if self.deg > 35:
            return self.heat_wave_dict[self.event][self.pref]
        elif self.deg > 25 and self.deg < 35:
            return self.hot_day_dict[self.event][self.pref]
        elif self.deg > 15 and self.deg < 25:
            return self.normal_day_dict[self.event][self.pref]
        elif self.deg > 5 and self.deg < 15:
            return self.cold_day_dict[self.event][self.pref]
        else:
            return self.super_cold_Day[self.event][self.pref]


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/result.html', methods=['post'])
def result():
    city = request.form['city']
    pref = request.form['temp']
    event = request.form['event']

    weather = Weather(city)
    if weather.deg:
        robot = Robofit(weather.deg, pref, event)
        answer = robot.answer()
    else:
        answer = "Sorry, RobotFIT couldn't find your desired location, please spell check so we can help you!"
    return render_template('result.html', answer=answer)

if __name__ == "__main__":
    app.run(threaded=True, port=5000)