from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.middleware import csrf

from models import *
import MySQLdb as mysli

MAX_ROWS = 30

db_settings = {
    'user' : 'root',
    'password' : '',
    'name' : 'reviews',
    'host' : 'localhost',
    'port' : '3306',
}

def index(request):
    review1 = Review("Jethro Tull",
                "Heavy Horses",
                "I prefer the B-side over the A-side. Favourite tracks: Rover, One Brown Mouse and of course the title track.")

    db = mysli.connect(db_settings['host'], db_settings['user'], db_settings['password'], db_settings['name'])

    if(request.method == "POST"):
        if( ('band_name' and 'album' and 'review_text') in request.POST) :
            review = Review(request.POST['band_name'],request.POST['album'],request.POST['review_text'])
            cursor = db.cursor()
            #Adding to database
            try:
                query = """INSERT INTO review VALUE(%s,%s,%s)"""
                cursor.execute(query,(review.band_name,review.album_title,review.review_text))
                db.commit()
            except (mysli.Error, mysli.Warning) as e:
                print e



    db.query("""SELECT * FROM review""")
    #Transforming results from tuple of tuples
    # to a list of dictionaries with keys band_name,album_title & reviews_text
    reviews = map( lambda(x,y,z):{'band_name' : x , 'album_title' : y, 'review_text' : z},db.store_result().fetch_row(MAX_ROWS) );

    template = loader.get_template('index.jinja2')
    context = {'reviews': reviews}
    return HttpResponse(template.render(context,request))

def write(request):
    template = loader.get_template('write.jinja2')
    csrf_token = csrf.get_token(request)
    return render(request, 'write.jinja2')