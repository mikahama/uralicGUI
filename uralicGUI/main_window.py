import kivy
from kivy.config import Config
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.uix.modalview import ModalView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.recycleview import RecycleView

from uralicNLP import uralicApi
from uralicNLP import string_processing
from uralicNLP.cg3 import Cg3

from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView
from kivy.app import App

from kivy.effects.scroll import ScrollEffect
from kivy.uix.popup import Popup

from mikatools import *
from glob import glob
import os

from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize



def download_async(lang, popup):
	try:
		uralicApi.download(lang)
	except:
		show_popup("Error", "Error downloading models for " + lang)
	popup.dismiss()

def uninstall_async(lang, popup):
	try:
		uralicApi.uninstall(lang)
	except:
		show_popup("Error", "Error removing models for " + lang)
	popup.dismiss()

def show_popup(title, text):
	popup = Popup(title=title, content=Label(text=text), size_hint=(None, None), size=(400, 400))
	popup.open()

class UralicApp(App):
	def on_start(self, **kwargs):
		self.populate_langs()
		try:
			word_tokenize(["ok","pk"])
		except:
			import nltk
			nltk.download("punkt")

	def populate_langs(self):
		fs = getattr(uralicApi, "__model_base_folders")()
		langs = []
		d_langs = []
		for p in fs:
			for f in glob(os.path.join(p, "*/")):
				sep = "/"
				if "\\" in f:
					sep = "\\"
				if f.endswith(sep):
					f = f[:-1]
				l = f.split(sep)[-1]
				if (lang_installed(l)):
					langs.append(l)
					if os.path.isfile(f + sep + "cg"):
						d_langs.append(l)

		self.root.ids.lang_selector.values = [string_processing.iso_to_name(lang) + " - " +lang for lang in langs] + [ "Add languages..."]
		self.root.ids.lang_selector_cg.values = [string_processing.iso_to_name(lang) + " - " +lang for lang in d_langs] + [ "Add languages..."]

	def cg(self):
		lang = self.root.ids.lang_selector_cg.text.split(" - ")
		if len(lang) < 2:
			show_popup("Select a language", "Please, select a language first")
			return
		lang = lang[-1]	
		text = self.root.ids.cg_input.text
		cg = Cg3(lang)
		sentence_results = []
		for sentence in sent_tokenize(text):
			words = word_tokenize(sentence)
			try:
				res = cg.disambiguate(words)
			except:
				show_popup("Cg not found", "Please install CG3. See\n https://mikalikes.men/how-to-install-visl-cg3-on-mac-windows-and-linux/")
				return
			r = ""
			for disamb_word in res:
				r += disamb_word[0] + ": \n"
				for possibility in disamb_word[1]:
					r += possibility.lemma + " - " + ", ".join(possibility.morphology) +"\n"
				r += "\n"
			sentence_results.append(r)
		self.root.ids.cg_output.text = "\n --- \n\n".join(sentence_results)


	def analyze(self):
		lang = self.root.ids.lang_selector.text.split(" - ")
		if len(lang) < 2:
			show_popup("Select a language", "Please, select a language first")
			return
		lang = lang[-1]
		text = self.root.ids.morph_input.text
		res = ["\t".join([str(x) for x in r]) for r in uralicApi.analyze(text, lang)]
		self.root.ids.morph_output.text = "\n".join(res)

	def generate(self):
		lang = self.root.ids.lang_selector.text.split(" - ")
		if len(lang) < 2:
			show_popup("Select a language", "Please, select a language first")
			return
		lang = lang[-1]
		text = self.root.ids.morph_input.text
		res = ["\t".join([str(x) for x in r])  for r in uralicApi.generate(text, lang)]
		self.root.ids.morph_output.text = "\n".join(res)

	def show_download_cg(self):
		if self.root.ids.lang_selector_cg.text != "Add languages...":
			return
		self.download_modal_view()

	def show_download(self):
		if self.root.ids.lang_selector.text != "Add languages...":
			return
		self.download_modal_view()

	def download_modal_view(self):
		view = ModalView(size_hint=(None, None), size=(400, 400))
		layout = ScrollView(size_hint=(1, None), size=(400, 300), do_scroll_y=True, always_overscroll=True, scroll_type=['bars',"content"],bar_width=10,effect_cls="ScrollEffect")
		g = GridLayout(cols=1, spacing=10, size_hint_y=None)
		g.bind(minimum_height=g.setter('height'))
		build_download_checkboxes(g)
		layout.add_widget(g)
		view.add_widget(layout)
		view.bind(on_dismiss=self.clear_selection)
		view.open()

	def clear_selection(self, crappa):
		self.populate_langs()
		self.root.ids.lang_selector.text = "Select a language"
		self.root.ids.lang_selector_cg.text = "Select a language"

def checkbox_language_action(checkbox, value):
	print(checkbox.iso_code)
	if value:
		popup = Popup(title="Downloading", content=Label(text="Downloading " + checkbox.iso_code), size_hint=(None, None), size=(400, 200), auto_dismiss=False)
		popup.open()

		t = WorkerRunner(download_async, [{"lang": checkbox.iso_code, "popup": popup}], 1,run_as_threads=True)
		t.start(join=False)
	else:
		popup = Popup(title="Uninstalling", content=Label(text="Removing " + checkbox.iso_code), size_hint=(None, None), size=(400, 200), auto_dismiss=False)
		popup.open()
		t = WorkerRunner(uninstall_async, [{"lang": checkbox.iso_code, "popup": popup}], 1,run_as_threads=True)
		t.start(join=False)


def lang_installed(lang):
	try:
		uralicApi.model_info(lang)
		return True
	except Exception as e:
		print(e)
		return False


def build_download_checkboxes(layout):
	try:
		langs = uralicApi.supported_languages()["morph"]
	except:
		show_popup("Error", "Error downloading the language list.")
	langs.sort()
	for lang in langs:
		installed = lang_installed(lang)

		l = GridLayout(cols=2, size_hint_y=None, height=40)
		cb = CheckBox(active=installed, size_hint_x= None, width=40)
		setattr(cb, "iso_code", lang)
		cb.bind(active=checkbox_language_action)
		l.add_widget(cb)
		l.add_widget(Label(text=string_processing.iso_to_name(lang) + " - " +lang, size_hint_x= None, width=150))
		layout.add_widget(l)