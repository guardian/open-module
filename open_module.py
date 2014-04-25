import webapp2
import jinja2
import os
import datetime
import update_schema

from google.appengine.api import users, app_identity
from google.appengine.ext import ndb
from google.appengine.ext import deferred
from webapp2_extras import json
from models import Snippet


jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), "template"))
)

server_url = app_identity.get_default_version_hostname()

DEFAULT_COLLECTION_NAME = "snippets";

PAGE_SIZE = 25

def snippet_key(snippet_collection_name=DEFAULT_COLLECTION_NAME):
    return ndb.Key('Snippets', snippet_collection_name);


class SnippetBase(webapp2.RequestHandler):
    def list(self):

        cursor = None
        bookmark = self.request.get('bookmark')
        if bookmark:
            cursor = ndb.Cursor.from_websafe_string(bookmark)

        snippets_query = Snippet.query().order(-Snippet.created)
        snippets, next_cursor, more = snippets_query.fetch_page(PAGE_SIZE, start_cursor=cursor)

        next_bookmark = None
        if more:
            next_bookmark = next_cursor.to_websafe_string()

        template = jinja_environment.get_template('list.html')
        self.response.out.write(template.render(snippets=snippets, bookmark=next_bookmark, server_url=server_url, pageName='list'))

    def put(self, snippet):
        snippet.headline = self.request.get('headline')
        snippet.link = self.request.get('link')
        snippet.copy = self.request.get('copy')
        if ( self.request.get('label') ):
            snippet.label = self.request.get('label')
        if ( self.request.get('button_text') ):
            snippet.button_text = self.request.get('button_text')

        snippet.put()

    def get(self):
        user = users.get_current_user()


        if user:
            self.render()
        else:
            self.redirect(users.create_login_url(self.request.uri))

    def post(self):
        user = users.get_current_user()

        if user:
            self.process()
        else:
            self.redirect(users.create_login_url(self.request.uri))

class Index(SnippetBase):
    def render(self):
        template = jinja_environment.get_template('create.html')
        self.response.out.write(template.render(pageName='create'))


class ListSnippits(SnippetBase):
    def render(self):
        self.list()

class Create(SnippetBase):
    def process(self):
        snippet = Snippet()
        self.put(snippet)
        self.redirect('/list')

class Preview(SnippetBase):
    def render(self):
       id = self.request.get("id")
       snippet = Snippet.get_by_id(long(id))
       template = jinja_environment.get_template("preview.html")
       self.response.out.write(template.render(snippet=snippet, id=id))

class Delete(SnippetBase):
    def render(self):
        id = self.request.get("id")
        key = ndb.Key("Snippets", long(id) )
        snippet = Snippet.get_by_id(long(id))
        snippet.key.delete()
        self.list()

class Update(SnippetBase):
    def render(self):
        id = self.request.get("id")
        snippet = Snippet.get_by_id(long(id))
        template = jinja_environment.get_template("update.html")
        self.response.out.write(template.render(snippet=snippet, id=id))

    def process(self):
        id = self.request.get("id")
        snippet = Snippet.get_by_id(long(id))
        self.put(snippet)
        self.list()

class View(webapp2.RequestHandler):
    def get(self):
        id = self.request.get("id")
        snippet = Snippet.get_by_id(long(id))

        template = jinja_environment.get_template("view.html")
        html = template.render(snippet=snippet, id=id)
        jsonResponse = {
            'html' : html,
            'headline' : snippet.headline,
            'link' : snippet.link,
            'copy' : snippet.copy,
            'id' : id
        }

        self.response.headers['cache-control'] = 'max-age=900s'
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json.encode(jsonResponse))

class Populate(SnippetBase):

    def render(self):

        for i in range (200):
            snippet = Snippet()
            snippet.headline = 'Headline ' + str(i)
            snippet.link = 'Link ' + str(i)
            snippet.copy = 'Headline ' + str(i)
            snippet.put()

class UpdateSchema(webapp2.RequestHandler):
    def get(self):
        deferred.defer(update_schema.UpdateSchema)
        self.response.out.write('Schema migration succesfully inititated.')

app = webapp2.WSGIApplication([
    ('/', ListSnippits),
    ('/new', Index),
    ('/create', Create),
    ('/list', ListSnippits),
    ('/preview', Preview),
    ('/update', Update),
    ('/delete', Delete),
    ('/view', View),
    ('/populate', Populate),
    ('/update-schema', UpdateSchema)

])