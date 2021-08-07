import kivy
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.uix.modalview import ModalView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.recycleview import RecycleView

from uralicNLP import uralicApi
from uralicNLP import string_processing
from kivy.core.window import Window

from kivy.app import App

class UralicApp(App):
	pass

	def show_download(self):
		view = ModalView(size_hint=(None, None), size=(400, 400))
		layout = RecycleView(size_hint=(1, None), size=(400, 300))
		g = GridLayout(cols=1)
		build_download_checkboxes(g)
		layout.add_widget(g)
		view.add_widget(layout)
		view.open()

def build_download_checkboxes(layout):
	langs = uralicApi.supported_languages()["morph"]
	langs.sort()
	for lang in langs:
		installed = False
		try:
			uralicApi.model_info(lang)
			installed = True
		except:
			pass
		l = GridLayout(cols=2, size_hint_y=None, height=40)
		l.add_widget(CheckBox(active=installed))
		l.add_widget(Label(text=string_processing.iso_to_name(lang) + " - " +lang))
		layout.add_widget(l)