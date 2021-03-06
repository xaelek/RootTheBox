'''
Created on Mar 13, 2012

@author: moloch
'''

import imghdr
import base64
import logging

from os import path
from uuid import uuid1
from base64 import b64encode
from tempfile import TemporaryFile
from mimetypes import guess_type
from libs.SecurityDecorators import *
from libs.WebSocketManager import WebSocketManager
from libs.Notification import Notification
from models import Team, Box, CrackMe, Action, Challenge, SEChallenge
from handlers.BaseHandlers import AdminBaseHandler
from tornado.web import RequestHandler
from string import ascii_letters, digits

class AdminCreateHandler(AdminBaseHandler):
    
    def get_challenge(self, *args, **kwargs):
        self.render("admin/create_challenge.html")

    def post_challenge(self, *args, **kwargs):
        try:
            name = self.get_argument('name')
            description = self.get_argument('description')
            value = int(self.get_argument('value'))
            token = self.get_argument('token')
        except:
            self.render("admin/error.html", errors = "Failed to create challenge")
        challenge = Challenge(
            name = unicode(name),
            description = unicode(description),
            value = value,
            token = unicode(token)
        )
        self.dbsession.add(challenge)
        self.dbsession.flush()
        self.render("admin/created.html", game_object = "challenge")
        
    def get_action(self, *args, **kwargs):
        self.render("admin/create_action.html", users = User.get_all())
        
    def post_action(self, *args, **kwargs):
        try:
            classification = self.get_argument("classification")
            description = self.get_argument("description")
            value = int(self.get_argument("value"))
            user_name = self.get_argument("user_name")
        except:
            self.render("admin/error.html", errors = "Failed to create action")
        user = User.by_user_name(user_name)
        action = Action(
            classification = unicode(classification),
            description = unicode(description),
            value = value,
            user_id = user.id
        )
        user.dirty = True
        user.actions.append(action)
        self.dbsession.add(user)
        self.dbsession.add(action)       
        self.dbsession.flush()
        self.render("admin/created.html", game_object = "action")
        
        
    def get_team(self, *args, **kwargs):
        self.render("admin/create_team.html")
        
    def post_team(self, *args, **kwargs):
        try:
            team_name = self.get_argument('team_name')
            motto = self.get_argument('motto')
            lport = int(self.get_argument('lport'))
        except:
            self.render("admin/error.html", errors = "Failed to create team")
        team = Team(
            team_name = unicode(team_name),
            motto = unicode(motto),
            listen_port = lport
        )
        self.dbsession.add(team)
        self.dbsession.flush()
        self.render("admin/created.html", game_object = 'team')
    
    def get_user(self, *args, **kwargs):
        pass
    
    def post_user(self, *args, **kwargs):
        pass
    
    def get_box(self, *args, **kwargs):
        self.render("admin/create_box.html")
    
    def post_box(self, *args, **kwargs):
        ''' Creates a box in the database '''
        try:
            box_name = self.get_argument("box_name")
            ip_address = self.get_argument("ip_address")
            description = self.get_argument("description")
            root_key = self.get_argument("root_key")
            root_value = int(self.get_argument("root_value"))
            user_key = self.get_argument("user_key")
            user_value = int(self.get_argument("user_value"))
            difficulty = self.get_argument("difficulty")
            if not difficulty in ['Easy', 'Medium', 'Hard']:
                raise TypeError
            avatar = "default_avatar.gif"
        except:
            self.render("admin/error.html", errors = "Failed to create box")
        if self.request.files.has_key('avatar') and len(self.request.files['avatar']) == 1:
            if len(self.request.files['avatar'][0]['body']) < (1024*1024):
                avatar = unicode(str(uuid1()))
                ext = imghdr.what("", h = self.request.files['avatar'][0]['body'])
                if ext in ['png', 'jpeg', 'gif', 'bmp']:
                    avatar = avatar+'.'+ext
                    file_path = self.application.settings['avatar_dir']+'/'+avatar
                    avatar_file = open(file_path, 'wb')
                    avatar_file.write(self.request.files['avatar'][0]['body'])
                    avatar_file.close()
                else:
                    self.render("admin/error.html", errors = "Invalid image format")
            else:
                self.render("admin/error.html", errors = "The image is too large")
        else:
            self.render("admin/error.html", errors = "No image")
        box = Box(
            box_name = unicode(box_name),
            ip_address = unicode(ip_address),
            description = unicode(description),
            difficulty = unicode(difficulty),
            avatar = unicode(avatar),
            root_key = unicode(root_key),
            root_value = int(root_value),
            user_key = unicode(user_key),
            user_value = int(user_value)
        )
        self.dbsession.add(box)
        self.dbsession.flush()
        self.render("admin/created.html", game_object = "box")
        
    def get_crack_me(self, *args, **kwargs):
        self.render("admin/create_crackme.html")
    
    def post_crack_me(self, *args, **kwargs):
        ''' Saves crack me to file system '''
        try:
            crack_me_name = self.get_argument('crack_me_name')
            description = self.get_argument('description')
            value = int(self.get_argument('value'))
            file_name = self.request.files['crack_me'][0]['filename']
            uuid = str(uuid1())
            token = self.get_argument('token')
            if len(self.request.files['crack_me']) != 1: raise TypeError
        except:
            self.render("admin/error.html", errors = "Failed to create crack me")
            
        filePath = self.application.settings['crack_me_dir']+'/'+uuid
        save = open(filePath, 'wb')
        save.write(b64encode(self.request.files['crack_me'][0]['body']))
        save.close()
        content = guess_type(file_name)

        if content[0] != None:
            crack_me = CrackMe(
                crack_me_name = unicode(crack_me_name),
                description = unicode(description),
                value = value,
                file_name = unicode(path.basename(file_name)),
                uuid = unicode(uuid),
                content = unicode(str(content[0])),
                token = unicode(token)
            )
            self.dbsession.add(crack_me)
            self.dbsession.flush()
            self.render('admin/created.html', game_object = "crack me")
        else:
            self.render('admin/error.html', errors = "Unknown file type, please zip and upload")
    
    def get_se(self, *args, **kwargs):
        self.render("admin/create_se.html")
        
    def post_se(self, *args, **kwargs):
        try:
            name = self.get_argument('name')
            description = self.get_argument('description')
            value = int(self.get_argument('value'))
            token = self.get_argument('token')
            level = int(self.get_argument('level'))
        except:
            self.render("admin/error.html", errors = "Failed to create challenge")
        challenge = SEChallenge(
            name = unicode(name),
            description = unicode(description),
            value = value,
            token = unicode(token),
            level = level
        )
        self.dbsession.add(challenge)
        self.dbsession.flush()
        self.render("admin/created.html", game_object = "challenge")
   

class AdminEditHandler(AdminBaseHandler):
    
    def get_challenge(self, *args, **kwargs):
        pass 
    
    def post_challenge(self, *args, **kwargs):
        pass
    
    def get_action(self, *args, **kwargs):
        pass
    
    def post_action(self, *args, **kwargs):
        pass
    
    def get_team(self, *args, **kwargs):
        pass
        
    def post_team(self, *args, **kwargs):
        pass
    
    def get_user(self, *args, **kwargs):
        self.render("admin/edit_user.html", teams = Team.get_all(), users = User.get_free_agents())
    
    def post_user(self, *args, **kwargs):
        try:
            team_name = self.get_argument('team_name')
            user_name = self.get_argument('user_name')
            team = Team.by_team_name(team_name)
            user = User.by_user_name(user_name)
            if team == None: raise TypeError
            if user == None: raise TypeError
        except:
            self.render("admin/error.html", errors = "Failed to edit user")
        user.team_id = team.id
        self.dbsession.add(user)
        self.dbsession.flush()
        self.render("admin/created.html", game_object = "edit user team")
        
    def get_box(self, *args, **kwargs):
        pass
        
    def post_box(self, *args, **kwargs):
        pass
    
    def get_crack_me(self, *args, **kwargs):
        pass
        
    def post_crack_me(self, *args, **kwargs):
        pass
    
    def get_se(self, *args, **kwargs):
        pass
        
    def post_se(self, *args, **kwargs):
        pass

class AdminNotifyHandler(RequestHandler):
    
    def initialize(self):
        self.ws_manager = WebSocketManager.Instance() #@UndefinedVariable
    
    @authorized("admin")
    @restrict_ip_address
    def get(self, *args, **kwargs):
        self.render("admin/notify.html", classifications = Notification.get_classifications())
    
    @authorized("admin")
    @restrict_ip_address
    def post(self, *args, **kwargs):
        try:
            message = self.get_argument("message")
            title = self.get_argument("title") #@UnusedVariable
            classification = self.get_argument("classification")
            try:
                file_contents = base64.encodestring(self.request.files['image'][0]['body'])
            except:
                file_contents = None
        except:
            self.render("admin/error.html", errors = "Invalid Entry")
        if file_contents == None:
            notification = Notification(title, message, classification)
        else:
            notification = Notification(title, message, file_contents = file_contents)
        self.ws_manager.send_all(notification)
        logging.info("Admin sent a notification")
        self.redirect("/admin/notify")
