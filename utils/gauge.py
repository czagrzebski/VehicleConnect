import kivy
import obd
from utils.obdutility import OBDUtility
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.properties import StringProperty, ListProperty, ObjectProperty, NumericProperty
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.config import Config
from kivy.clock import mainthread, Clock
from utils.obdutility import OBDUtility
import threading
import time
import re


