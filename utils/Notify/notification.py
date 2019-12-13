import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.config import Config
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition, SlideTransition
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

class PopupWidget(Widget):
    pass

class Notify():
    """Notification Prompts. Create pop-up notifcations"""

    def basic(self,notifymsg, notifytitle):
            notifybasic = Popup(title=notifytitle,
                                content=Label(text=notifymsg),  
                                size_hint=(None, None), size=(400, 300))  
            
            notifybasic.open()

    def one_button(self,notify_title, notify_msg, notify_btn, btn_action):
            box = BoxLayout(orientation='vertical')
            try:
                message = Label(text=notify_msg)
                message.bind(size=message.setter('text_size'))
                box.add_widget(message)
                button = Button(text=notify_btn,size_hint = (1,.25))
                button.bind(on_release=btn_action)
                box.add_widget(button)
                notify_one_button = Popup(title=notify_title,
                                content=box,  
                                size_hint=(None, None), size=(400, 300))  
            
                notify_one_button.open()
            except Exception as e:
                pass

    def dismiss_current(self):
         if isinstance(App.get_running_app().root_window.children[0], Popup):
            App.get_running_app().root_window.children[0].dismiss()

    def dismiss_all(self):
        for widget in App.get_running_app().root_window.children:
            if isinstance(widget, Popup):
                widget.dismiss()




            


  

