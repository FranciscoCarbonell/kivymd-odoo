from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivy.properties import StringProperty
from kivymd.app import MDApp


Builder.load_string(
'''

<BaseScreen>:
    MDToolbar:
        title: root.title
        pos_hint:{"top": 1}
        left_action_items: [["menu", lambda x: root.toggle_drawer()]]

'''
)


class BaseScreen(MDScreen):
    title = StringProperty()

    def toggle_drawer(self):
        app = MDApp.get_running_app()
        app.root.ids.navigation_drawer.set_state('toggle')
