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
    result = db.store_result().fetch_row(MAX_ROWS)

    #Transforming results from tuple of tuples
    # to a list of dictionaries with keys band_name,album_title & reviews_text
    reviews = map( lambda(x,y,z):{'band_name' : x , 'album_title' : y, 'review_text' : z}, result)

    template = loader.get_template('index.html')
    context = {'reviews': reviews}
    return HttpResponse(template.render(context,request))

def write(request):
    return render(request, 'write.html')

def bands(request):
    db = mysli.connect(db_settings['host'], db_settings['user'], db_settings['password'], db_settings['name'])
    cursor = db.cursor()
    query = """SELECT DISTINCT band_name FROM review ORDER BY band_name"""
    cursor.execute(query)
    #Tuples of tuples of strings
    bands = cursor.fetchall()
    #From tuples of tuples into a list
    bands = [x for (x,) in bands]


    template = loader.get_template('bands.html')
    context = {'band_names': bands}


    return HttpResponse(template.render(context,request))
