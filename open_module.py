import webapp2
import jinja2
import os

from google.appengine.api import users
from google.appengine.ext import ndb
from webapp2_extras import json

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), "template"))
)

DEFAULT_COLLECTION_NAME = "snippets";

def snippet_key(snippet_collection_name=DEFAULT_COLLECTION_NAME):
    return ndb.Key('Snippets', snippet_collection_name);

class Snippet(ndb.Model):
    headline = ndb.StringProperty(indexed=True)
    link = ndb.StringProperty(indexed=False)
    copy = ndb.TextProperty(indexed=False)

class SnippetBase(webapp2.RequestHandler):
    def list(self):
        snippets_query = Snippet.query()
        snippets = snippets_query.fetch(25)

        template = jinja_environment.get_template('list_snippets.html')
        self.response.out.write(template.render(snippets=snippets))

    def put(self, snippet):
        snippet.headline = self.request.get('headline')
        snippet.link = self.request.get('link')
        snippet.copy = self.request.get('copy')

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
        self.response.out.write(template.render())


class ListSnippits(SnippetBase):
    def render(self):
        self.list()

class Create(SnippetBase):
    def process(self):
        snippet = Snippet()
        self.put(snippet)
        self.list()

class Preview(SnippetBase):
    def render(self):
       id = self.request.get("id")
       snippet = Snippet.get_by_id(long(id))
       template = jinja_environment.get_template("view_snippet.html")
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
        template = jinja_environment.get_template("view_snippet.html")
        html = template.render(snippet=snippet, id=id)
        jsonResponse = {
            'html' : html,
            'headline' : snippet.headline,
            'link' : snippet.link,
            'copy' : snippet.copy,
            'id' : id
        }

        self.response.headers['cache-control'] = 'max-age=900s'
        self.response.headers['Access-Control-Allow-Origin:'] = '*'
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json.encode(jsonResponse))

app = webapp2.WSGIApplication([
    ('/', Index),
    ('/create', Create),
    ('/list', ListSnippits),
    ('/preview', Preview),
    ('/update', Update),
    ('/delete', Delete),
    ('/view', View)
])