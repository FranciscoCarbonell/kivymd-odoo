from kivy.lang import Builder
from screens.base import BaseScreen


Builder.load_string(
'''

<MenusScreen>:
    MDBoxLayout:
        orientation: 'vertical'
        ScrollView:
            do_sroll_y: False
            do_scroll_x: True
            MDList:
                Button:
        MDBoxLayout:
            Button:

'''
)


class MenusScreen(BaseScreen):
    pass