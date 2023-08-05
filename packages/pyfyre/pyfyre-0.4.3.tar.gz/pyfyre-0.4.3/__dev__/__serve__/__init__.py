from pyfyre.widgets import *
from pyfyre.pyfyre import runApp
from src.main import MyWebpage
class App(UsesState):
 def __init__(self):
  self.greet="Welcome"
 def build(self):
  None in 5
  return MyWebpage(self.greet)
runApp(
App(),
mount="app-mount"
)
