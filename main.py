from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import OneLineListItem
from kivymd.theming import ThemableBehavior
from kivymd.uix.list import MDList
from kivy.lang import Builder
from kivy.properties import NumericProperty
from kivy.factory import Factory
import xmlrpc.client


Builder.load_string(
'''
#: import HomeScreen screens.home

<ItemMainMenu>:

<ContentDrawer>:
    orientation: "vertical"
    FloatLayout:
        size_hint_y: None
        height: "200dp"
        BoxLayout:
            id: box_image
            size_hint_y: None
            height: "200dp"
            x: root.x
            pos_hint: {"top": 1}
            
            FitImage:
                source: "menu.png"
        MDLabel:
            text: "Nombre de la empresa"
            size_hint_y: None
            height: self.texture_size[1]
            x: root.x
            y: root.height - box_image.height + dp(10)
    ScrollView:
        DrawList:
            id: list_main_menu

<RootWidget@MDScreen>:
    MDNavigationLayout:
        ScreenManager:
            HomeScreen:
        
        MDNavigationDrawer:
            id: navigation_drawer
            ContentDrawer:
                id: content_drawer
            

'''
)


class ContentDrawer(MDBoxLayout):
    pass


class DrawList(ThemableBehavior, MDList):
    pass


class ItemMainMenu(OneLineListItem):
    menu_id = NumericProperty()

    def __init__(self, *args, **kwargs):
        self.menu_id = kwargs.get('menu_id', None)
        return super(ItemMainMenu, self).__init__(*args, **kwargs)

    def on_release(self):
        app = MDApp.get_running_app()
        menus = app.get_list_menu(self.menu_id)
        app.set_list_menu(menus)
        return super(ItemMainMenu, self).on_release()


class MainWindow(MDApp):

    def on_start(self):
        self.db = 'odoo15'
        self.username = 'admin'
        self.password = 'edb6c67b2afe83e1cdaf16d496926a494cc37ebf'
        self.common = xmlrpc.client.ServerProxy('http://localhost:8069/xmlrpc/2/common', allow_none=True)
        self.models = xmlrpc.client.ServerProxy('http://localhost:8069/xmlrpc/2/object', allow_none=True)
        self.uid_odoo = self.common.authenticate(self.db, self.username, self.password, {})
        root_menus = self.get_list_menu()
        self.set_list_menu(root_menus)

    def build(self):
        return Factory.RootWidget()

    def search_read(self, model, method, domain, args):
        return self.models.execute_kw(self.db, self.uid_odoo, self.password, model,
            method, domain, args)

    def get_list_menu(self, menu_id=None):
        return self.search_read('ir.ui.menu', 'search_read', [[['parent_id', '=', menu_id]]],
            {'fields': ['id', 'name', 'action'], 'context': {'lang': 'es_ES'}})

    def set_list_menu(self, menus):
        app = self.get_running_app()
        list = app.root.ids.content_drawer.ids.list_main_menu
        list.clear_widgets()
        for menu in menus:
            list.add_widget(ItemMainMenu(text=menu['name'], menu_id=menu['id']))

main_window = MainWindow()
main_window.run()
