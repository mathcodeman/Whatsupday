from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
import json,glob
from datetime import datetime
from pathlib import Path
import random
from hoverable import HoverBehavior


Builder.load_file('design.kv')

class LoginScreen(Screen):
    def sign_up(self):
        self.manager.current = "sign_up_screen"

    def login(self,uname,pword):
        with open('users.json') as file:
            users=json.load(file)
        if uname in users:
            if users[uname]['password'] == pword:
                self.manager.current = "log_in_success"
            else:
                self.ids.login_wrong.text = "Wrong password!"
        else:
            self.ids.login_wrong.text = "Wrong username!"
        

class SignUpScreen(Screen):
    def add_user(self,uname,pword):
        with open("users.json") as file:
            users = json.load(file)
        
        users[uname] = {'username':uname,'password':pword,
        'created':datetime.now().strftime("%Y-%m-%d %H-%M-%S")}
        print(users)

        with open("users.json",'w') as file:
            json.dump(users,file)
        self.manager.current = "sign_up_success"

class SignUpSuccess(Screen):
    def redirect(self):
        self.manager.transition.direction = "right"
        self.manager.current = "Login_screen"

class LoginSuccess(Screen):
    def logout(self):
        self.manager.transition.direction = "right"
        self.manager.current = "Login_screen"
    def get_quote(self,feel):
        feel=feel.lower()
        available_feeling = glob.glob("quotes/*txt")
    
        feels = []
        for feeling in available_feeling:
            feels.append(Path(feeling).stem)
        
        if feel in feels:
            with open(f"quotes/{feel}.txt",encoding='utf-8') as file:
                lines = file.readlines()
            self.ids.quote.text = random.choice(lines)
        else:
            self.ids.quote.text = "Your feeling is not found please try again!!"

class ImageButton(ButtonBehavior,HoverBehavior,Image):
    pass


class RootWidget(ScreenManager):
    pass

class MainApp(App):
    def build(self):
        return RootWidget()

if __name__ == "__main__":
    MainApp().run()