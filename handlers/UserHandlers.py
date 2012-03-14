'''
Created on Mar 13, 2012

@author: moloch
'''

from libs.SecurityDecorators import authenticated
from tornado.web import RequestHandler #@UnresolvedImport

class HomeHandler(RequestHandler):
    
    def initialize(self, dbsession):
        self.dbsession = dbsession
    
    @authenticated
    def get(self, *args, **kwargs):
<<<<<<< Updated upstream
        ''' Display the default user page '''
        self.render('user.html', header='User Page')
=======
        self.render("blank.html")
>>>>>>> Stashed changes
    
class SettingsHandler(RequestHandler):
    
    def initialize(self, dbsession):
        self.dbsession = dbsession
    
    def get(self, *args, **kwargs):
<<<<<<< Updated upstream
        ''' Display the user settings '''
        self.render('user_settings.html', header='User Settings')
    
class TeamHandler(RequestHandler):
    
    def initialize(self, dbsession):
        self.dbsession = dbsession
    
    def get(self, *args, **kwargs):
        pass
    
class BoxesHandler(RequestHandler):
    
    def initialize(self, dbsession):
        self.dbsession = dbsession
    
    def get(self, *args, **kwargs):
        pass
    
class ScoreBoardHandler(RequestHandler):
    
    def initialize(self, dbsession):
        self.dbsession = dbsession
    
    def get(self, *args, **kwargs):
        pass
=======
        self.render("blank.html")

class LogoutHandler(RequestHandler):
    
    def get(self):
        self.clear_all_cookies()
        self.redirect("/")
>>>>>>> Stashed changes
