import os
import kivy.weakmethod
import platform
import sys
sys.path.append("/usr/local/bin")
#os.environ['KIVY_GL_BACKEND']='angle_sdl2'
#if platform.system() == 'Darwin':
os.environ["PATH"] += os.pathsep + "/usr/local/bin"

from uralicGUI import UralicApp

UralicApp().run()