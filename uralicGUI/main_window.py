import kivy
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.uix.modalview import ModalView
from kivy.uix.gridlayout import GridLayout

from uralicNLP import uralicApi
from uralicNLP import string_processing

from kivy.app import App

class UralicApp(App):
	pass

def show_download():
	view = ModalView(size_hint=(None, None), size=(400, 400))
	layout = GridLayout(cols=1)
	build_download_checkboxes(layout)
	view.add_widget(layout)

def build_download_checkboxes(layout):
	langs = uralicApi.supported_languages()["morph"]
	for lang in langs:
		installed = False
		try:
			uralicApi.model_info(lang)
			installed = True
		except:
			pass
		l = GridLayout(cols=2)
		l.add(CheckBox(active=installed))
		l.add(Label(text=string_processing.iso_to_name(lang) + " - " +lang))
		layout.add(l)