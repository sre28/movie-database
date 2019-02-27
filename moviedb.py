#!/usr/bin/env python

# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START imports]
import os
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
# [END imports]

DEFAULT_GENRE = 'action'
genrer = ""
genre2 = ""

# We set a parent key on the 'Greetings' to ensure that they are all
# in the same entity group. Queries across the single entity group
# will be consistent. However, the write rate should be limited to
# ~1/second.

def genre_key(genre=DEFAULT_GENRE):
    """Constructs a Datastore key for a Guestbook entity.
    We use guestbook_name as the key.
    """ 
    
    return ndb.Key('Guestbook', genre)


# [START Movie]
class Author(ndb.Model):
    """Sub model for representing an author."""
    identity = ndb.StringProperty(indexed=False)
    email = ndb.StringProperty(indexed=False)


class Movie(ndb.Model):
    """A main model for representing an individual movie entry."""
    author = ndb.StructuredProperty(Author)
    name = ndb.StringProperty(indexed=False)
    director = ndb.StringProperty(indexed=False)
    actor = ndb.StringProperty(indexed=False)
    actor2 = ndb.StringProperty(indexed=False)
    year = ndb.StringProperty(indexed=False)
    duration = ndb.StringProperty(indexed=False)
    date = ndb.DateTimeProperty(auto_now_add=True)
# [END Movie]


class DisplayPage(webapp2.RequestHandler):

    def get(self):
        genre_name = self.request.get('genre_name',
                                          DEFAULT_GENRE).lower()
        movies_query = Movie.query(
            ancestor=genre_key(genre_name)).order(-Movie.date)
        movies = movies_query.fetch(50)

        user = users.get_current_user()
     

        template_values = {
            'user': user,
            'movies': movies,
            'genre_name': urllib.quote_plus(genre_name),
        }

        template = JINJA_ENVIRONMENT.get_template('displaymodel.html')
        self.response.write(template.render(template_values))

class SearchPage(webapp2.RequestHandler):

    def get(self):
	global genre2
	genre = self.request.get('genre_name').lower()

	if genre == "":
		if genre2 == "":
			genre = self.request.get('genre_name',DEFAULT_GENRE).lower()
		else:
			genre = genre2
	else:
		genre2 = genre;
       	

	template_values = {
            'genre_name': urllib.quote_plus(genre),
        }
        template = JINJA_ENVIRONMENT.get_template('searchmodel.html')
        self.response.write(template.render(template_values))

    def post(self):

	#temp variable      
	movies_query1 = Movie.query(
           		ancestor=genre_key("-")).order(-Movie.date)
        movies1 = movies_query1.fetch(1)
	tempo = movies1

	global genre2
	genre = self.request.get('genre_name').lower()
	flag = -1
	flag2 = -1

	if genre == "":
		if genre2 == "": #first time and search
			genre = self.request.get('genre_name',DEFAULT_GENRE).lower()
			movies_query = Movie.query(
           		ancestor=genre_key(genre)).order(-Movie.date)
        		movies = movies_query.fetch(50)

			movie = Movie(parent=genre_key(genre))
			movie.name = self.request.get('name')
       		        movie.actor = self.request.get('actor')
			movie.director = self.request.get('director')
			movie.year = self.request.get('year')

			if movie.year == "" and movie.name =="" and movie.actor == "" and movie.director == "":
				flag = 0;

			
			if flag != 0:
				for i in movies:
					if i.name.lower().find(movie.name.lower(), 0, len(i.name)) != -1:
						if i.actor.lower().find(movie.actor.lower(), 0, len(i.actor)) != -1 or i.actor2.lower().find(movie.actor.lower(), 0, len(i.actor2)) != -1:
							if i.director.lower().find(movie.director.lower(), 0, len(i.director)) != -1:
								if i.year == movie.year or movie.year == "":
									
																			tempo.append(i)
								
			if not tempo:
				flag2 = 0		
		else: 
			genre = genre2
			movies_query = Movie.query(
           		ancestor=genre_key(genre)).order(-Movie.date)
			movies = movies_query.fetch(50)
			
			movie = Movie(parent=genre_key(genre))
			movie.name = self.request.get('name')
       		        movie.actor = self.request.get('actor')
			movie.director = self.request.get('director')
			movie.year = self.request.get('year')
			if movie.year == "" and movie.name =="" and movie.actor == "" and movie.director == "":
				flag = 0;
			if flag != 0: 
				for i in movies:
					if i.name.lower().find(movie.name.lower(), 0, len(i.name)) != -1:
						if i.actor.lower().find(movie.actor.lower(), 0, len(i.actor)) != -1 or i.actor2.lower().find(movie.actor.lower(), 0, len(i.actor2)) != -1:
							if i.director.lower().find(movie.director.lower(), 0, len(i.director)) != -1:
								if i.year == movie.year or movie.year == "":
					
									tempo.append(i)

				
				if not tempo:
					flag2 = 0;
							       
			
	else:#switch
		genre2 = genre;
		movies_query = Movie.query(
           	ancestor=genre_key("-")).order(-Movie.date)
		tempo = movies_query.fetch(1)
		


        template_values = {
            'genre_name': urllib.quote_plus(genre),
	    'movies': tempo,
	    'flag': flag,
	    'flag2':flag2,
        }

	template = JINJA_ENVIRONMENT.get_template('searchmodel.html')
        self.response.write(template.render(template_values))


class EnterPage(webapp2.RequestHandler):


    def get(self):
	global genrer
	genre = self.request.get('genre_name').lower()

	if genre == "":
		if genrer == "":
			genre = self.request.get('genre_name',DEFAULT_GENRE).lower()
		else:
			genre = genrer
	else:
		genrer = genre;


        template_values = {
            'genre_name': urllib.quote_plus(genre),
        }

        template = JINJA_ENVIRONMENT.get_template('entermodel.html')
        self.response.write(template.render(template_values))

    def post(self):
        # We set the same parent key on the 'Greeting' to ensure each
        # Greeting is in the same entity group. Queries across the
        # single entity group will be consistent. However, the write
        # rate to a single entity group should be limited to
        # ~1/second.
	global genrer
	genre = self.request.get('genre_name').lower()
	flag = -1

	if genre == "":
		if genrer == "": # first time and search
			genre = self.request.get('genre_name',DEFAULT_GENRE).lower()
			movie = Movie(parent=genre_key(genre))
			movie.name = self.request.get('name')
        		movie.actor = self.request.get('actor')
			movie.actor2 = self.request.get('actor2')
			movie.director = self.request.get('director')
      		  	movie.year = self.request.get('year')
     		        movie.duration = self.request.get('duration')

			if movie.year == "" or movie.name =="" or movie.director == "" or movie.duration == "":
				flag = 0;
		else:
			genre = genrer
			movie = Movie(parent=genre_key(genre))
			movie.name = self.request.get('name')
        		movie.actor = self.request.get('actor')
			movie.actor2 = self.request.get('actor2')
			movie.director = self.request.get('director')
       			movie.year = self.request.get('year')
        		movie.duration = self.request.get('duration')

			if movie.year == "" or movie.name =="" or movie.director == "" or movie.duration == "":
				flag = 0;
	else: #switch
		genrer = genre;
		movie = Movie(parent=genre_key(genre))
		movie.name = self.request.get('name')
       	        movie.actor = self.request.get('actor')
		movie.actor2 = self.request.get('actor2')
		movie.director = self.request.get('director')
        	movie.year = self.request.get('year')
        	movie.duration = self.request.get('duration')

		flag = -1		

			
     
        

	if movie.name != "":
		if movie.director != "":
			if movie.year != "":
				if movie.duration != "":
        				movie.put()
	

        template_values = {
            'genre_name': urllib.quote_plus(genre),
	    'flag': flag,
        }

	#query_params = {'genre_name': genre}
        #self.redirect('/enter?' + urllib.urlencode(query_params))
	template = JINJA_ENVIRONMENT.get_template('entermodel.html')
        self.response.write(template.render(template_values))


# [START main_page]
class MainPager(webapp2.RequestHandler):

    def get(self):
        
        template = JINJA_ENVIRONMENT.get_template('index1.html')
        self.response.write(template.render())
# [END main_page]


# [START movieinfo]



# [START app]
app = webapp2.WSGIApplication([
    ('/', MainPager),
    ('/sign', DisplayPage),('/search', SearchPage),('/enter', EnterPage),
], debug=True)
# [END app]
