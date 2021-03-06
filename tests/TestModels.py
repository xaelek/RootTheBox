'''
Created on Mar 12, 2012

@author: moloch
'''

from hashlib import md5
from models import * #@UnusedWildImport

DROP = False

# Common functions used by all tests
def createUser(name = 'tester', handle='moloch', team=None):
    user = User(
        user_name = unicode(name),
        display_name = unicode(handle),
        password = unicode('asdf'),
        team_id = team
    )
    dbsession.add(user) #@UndefinedVariable
    dbsession.flush() #@UndefinedVariable

def createTeam(name = 'The A Team'):
    team = Team(
        team_name = unicode(name),
        motto = unicode("Pdc"),
        score = 0
    )
    dbsession.add(team) #@UndefinedVariable
    dbsession.flush() #@UndefinedVariable

def createBox(name = 'The Gibson'):
    box = Box(
        box_name = unicode(name),
        ip_address = unicode('127.0.0.1'),
        description = unicode('A Super Computer'),
        root_key = unicode('123456'),
        root_value = 50,
        user_key = unicode('654321'),
        user_value = 25
    )
    dbsession.add(box) #@UndefinedVariable
    dbsession.flush() #@UndefinedVariable

def createAction():
    user = User.by_user_name(unicode('tester'))
    action = Action(
        classification = unicode("Box"),
        description = unicode("Pwned a box"),
        value = 100,
        user_id = user.id
    )
    dbsession.add(action) #@UndefinedVariable
    dbsession.flush() #@UndefinedVariable   

def createCrackMe(name = 'Enigma', fname = 'a.exe', fuuid = '1234', toke = 'asdf'):
    crack_me = CrackMe(
        crack_me_name = unicode(name),
        description = unicode('German encryption machine'),
        value = 100,
        file_name = unicode(fname),
        file_uuid = unicode(fuuid),
        token = unicode(toke)
    )
    dbsession.add(crack_me)
    dbsession.flush()
    return crack_me

# ------[ User Test Class ] -------------------------------------
class TestUser():
    
    def setUp(self):
        if User.by_user_name("tester") == None:
            createUser()
        if Team.by_team_name("The A Team") == None:
            createTeam()
    
    def tearDown(self):
        if DROP:
            user = User.by_user_name('tester')
            team = Team.by_team_name('The A Team')
            dbsession.delete(user) #@UndefinedVariable
            dbsession.delete(team) #@UndefinedVariable
            dbsession.flush() #@UndefinedVariable
    
    def test_by_user_name(self):
        user = User.by_user_name('tester')
        assert not user == None
        hashTest = md5()
        hashTest.update(unicode('asdf'))
        assert user.password ==  hashTest.hexdigest()
        
    def test_by_team_name(self):
        team = Team.by_team_name("The A Team")
        assert not team == None

    def test_add_user_to_team(self):
        user = User.by_user_name("tester")
        user.add_to_team("The A Team")
        
    def test_user_team_name(self):
        user = User.by_user_name("tester")
        assert user != None
        self.test_add_user_to_team()
        assert user.team_name == unicode("The A Team")
    
    def test_14(self):
        assert True
         
# ------[ Box Test Class ] -------------------------------------
class TestBox():
    
    def setUp(self):
        if Box.by_box_name("The Gibson") == None:
            createBox()
    
    def tearDown(self):
        if DROP:
            box = Box.by_box_name("The Gibson")
            dbsession.delete(box) #@UndefinedVariable
            dbsession.flush() #@UndefinedVariable
    
    def test_by_box_name(self):
        box = Box.by_box_name('The Gibson')
        assert box.ip_address == unicode('127.0.0.1')
        box2 = Box.by_ip_address('')
        assert box2 == None
    
    def test_by_ip_address(self):
        box = Box.by_ip_address('127.0.0.1')
        assert box.box_name == unicode('The Gibson')
        box2 = Box.by_ip_address('')
        assert box2 == None

# ------[ Action Test Class ] -------------------------------------
class TestAction():
    
    def setUp(self):
        if User.by_user_name(unicode("tester")) == None:
            createUser()
        if Team.by_team_name(unicode("The A Team")) == None:
            createTeam()
        team = Team.by_team_name(unicode("The A Team"))
        user = User.by_user_name(unicode("tester"))
        user.team_id = team.id
        dbsession.add(user) #@UndefinedVariable
        dbsession.flush() #@UndefinedVariable
        
    def teadDown(self):
        if DROP:
            user = User.by_user_name(unicode('tester'))
            dbsession.delete(user) #@UndefinedVariable
            dbsession.flush() #@UndefinedVariable
        
    def test_create_action(self):
        createAction()

# ------[ Team Test Class ] -------------------------------------
class TestTeam():
    
    def setUp(self):
        if User.by_user_name("tester") == None:
            createUser()
        if Team.by_team_name("The A Team") == None:
            createTeam()
        self.team = Team.by_team_name("The A Team")
        if User.by_user_name('john') == None:
            createUser('john', 'johnyboy', self.team.id)
        user = User.by_user_name('john')
        user.team_id = self.team.id
        dbsession.add(user) #@UndefinedVariable
        dbsession.flush() #@UndefinedVariable
        createAction()
        createAction()
  
    def teadDown(self):
        if DROP:
            user = User.by_user_name(unicode('tester'))
            dbsession.delete(user) #@UndefinedVariable
            dbsession.flush() #@UndefinedVariable
            user = User.by_user_name(unicode('john'))
            dbsession.delete(user) #@UndefinedVariable
            dbsession.flush() #@UndefinedVariable
    
    def test_team_members(self):
        team = Team.by_team_name("The A Team")
        assert len(team.members) == 2
        
    def test_give_control(self):
        self.team.give_control("The Gibson")
        assert self.team.is_controlling("The Gibson")
    
    def test_lost_control(self):
        self.team.give_control("The Gibson")
        assert self.team.is_controlling("The Gibson")
        self.team.lost_control("The Gibson")
        assert not self.team.is_controlling("The Gibson")

# ------[ Crack Me Test Class ] -------------------------------------
class TestCrackMe():
    
    def setUp(self):
        if User.by_user_name("tester") == None:
            createUser()
        if Team.by_team_name("The A Team") == None:
            createTeam()
        if CrackMe.by_id(1) == None:
            crack_me = createCrackMe()
        else:
            crack_me = CrackMe.by_id(1)
        if CrackMe.by_id(2) == None:
            crack_me = createCrackMe(name="Cipher", fname = 'b.exe', fuuid = '4321', toke = 'fdsa' )
        self.team = Team.by_team_name("The A Team")
        self.team.crack_me_id = crack_me.id
    
    def tearDown(self):
        if DROP:
            user = User.by_user_name('tester')
            dbsession.delete(user) #@UndefinedVariable
            dbsession.flush() #@UndefinedVariable
            team = Team.by_team_name("The A Team")
            dbsession.delete(team) #@UndefinedVariable
            dbsession.flush() #@UndefinedVariable
    
    def test_crack_me(self):
        assert self.team.crack_me != None
    
    def test_next_crack_me(self):
        self.team.solved_crack_me()
        assert self.team.crack_me != None
        self.team.solved_crack_me()
        assert self.team.crack_me == None

# ------[ Permission Test Class ] -------------------------------------
class TestPermission():
    
    def setUp(self):
        if User.by_user_name("tester") == None:
            createUser()
        if User.by_user_name('john') == None:
            createUser('john', 'johnyboy')

    def teadDown(self):
        if DROP:
            user = User.by_user_name('tester')
            dbsession.delete(user) #@UndefinedVariable
            dbsession.flush() #@UndefinedVariable

    def test_has_permission(self):
        user = User.by_user_name("tester")
        permission = Permission(
            permission_name = unicode('admin'),
            user_id = user.id
        )
        dbsession.add(permission) #@UndefinedVariable
        dbsession.flush() #@UndefinedVariable
        assert user.has_permission('admin')
        user = User.by_user_name("john")
        assert not user.has_permission('admin')
