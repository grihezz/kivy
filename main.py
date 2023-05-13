import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import AsyncImage
from kivy.uix.screenmanager import Screen, ScreenManager, SlideTransition
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.anchorlayout import AnchorLayout
import os
from kivy.lang import Builder

from kivymd.toast import toast
from kivymd.uix.bottomsheet import MDGridBottomSheet
from kivymd.app import MDApp
from kivy.uix.widget import Widget
from kivymd.app import MDApp

KV = '''
Screen:

    MDToolbar:
        title: 'Example BottomSheet'
        pos_hint: {"top": 1}
        elevation: 10

    MDRaisedButton:
        text: "Open grid bottom sheet"
        on_release: app.show_example_grid_bottom_sheet()
        pos_hint: {"center_x": .5, "center_y": .5}
'''
class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        box_layout = BoxLayout(orientation='vertical', padding=50, spacing=20)
        self.username_input = TextInput(hint_text='Username')
        self.password_input = TextInput(hint_text='Password', password=True)
        box_layout.add_widget(self.username_input)
        box_layout.add_widget(self.password_input)
        login_button = Button(text='Login')
        login_button.bind(on_press=self.go_to_next_screen)
        box_layout.add_widget(login_button)
        self.add_widget(box_layout)

    def go_to_next_screen(self, instance):
        App.get_running_app().root.current = 'second_screen'

from kivymd.uix.dialog import MDDialog
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder


class SecondScreen(Screen):
    def __init__(self, **kwargs):
        super(SecondScreen, self).__init__(**kwargs)
        self.pic_path = os.path.join(os.path.dirname(__file__), 'pic')
        self.file_list = os.listdir(self.pic_path)
        self.current_index = 0

        layout = AnchorLayout(anchor_x='center', anchor_y='top')

        box_layout = BoxLayout(orientation='vertical', height=500, padding=100,
                               spacing=15)
        self.image = Image(source=self.get_current_image_path())
        box_layout.add_widget(self.image)

        layout.add_widget(box_layout)

        button_layout = BoxLayout(orientation='horizontal', size_hint=(1, 1),
                                  spacing=10)
        prev_button = Button(size_hint=(.1, 1), background_color=(0, 0, 0, 0))
        prev_button.bind(on_press=self.show_previous_image)
        next_button = Button(size_hint=(.1, 1), background_color=(0, 0, 0, 0))
        next_button.bind(on_press=self.show_next_image)

        button_layout.add_widget(prev_button)
        button_layout.add_widget(Widget())
        button_layout.add_widget(next_button)

        layout.add_widget(button_layout)

        float_layout = FloatLayout(size_hint=(.8, 1),
                                   pos_hint={'x': 0, 'y': 0})
        circular_button = Button(size_hint=(None, None),
                                 size=(150, 150),
                                 pos_hint={'center_x': .5, 'y': 0},
                                 background_normal='free-icon-power-button-1783327.png',
                                 background_down='free-icon-power-button-1783327.png')
        float_layout.add_widget(circular_button)

        layout.add_widget(float_layout)

        self.add_widget(layout)

    def get_current_image_path(self):
        if self.file_list:
            return os.path.join(self.pic_path, self.file_list[self.current_index])
        else:
            return ""

    def show_previous_image(self, instance):
        if self.file_list:
            self.current_index -= 1
            if self.current_index < 0:
                self.current_index = len(self.file_list) - 1
            self.image.source = self.get_current_image_path()

    def show_next_image(self, instance):
        if self.file_list:
            self.current_index += 1
            if self.current_index >= len(self.file_list):
                self.current_index = 0
            self.image.source = self.get_current_image_path()







class ThirdScreen(Screen):
    def __init__(self, **kwargs):
        super(ThirdScreen, self).__init__(**kwargs)
        self.add_widget(Label(text='Это второй экран'))

class PopUpP(Screen):
    def __init__(self, **kwargs):
        super(PopUpP, self).__init__(**kwargs)
        self.add_widget(Label(text='Это popup'))

class MyScreenManager(ScreenManager):
    def __init__(self, **kwargs):
        super(MyScreenManager, self).__init__(**kwargs)
        self.transition = SlideTransition()

    def on_touch_move(self, touch):
        if self.current == 'second_screen':
            if touch.dx > 50:
                self.transition.direction = 'right'
                self.current = self.next()

        elif self.current == 'other_screen':
            if touch.dy > 50:
                self.transition.direction = 'down'
                self.current = 'second_screen'

        elif self.current == 'third_screen':
            if touch.dx < -50:
                self.transition.direction = 'left'
                self.current = self.previous()
    def show_grid_bottom_sheet(self):
        pass


class MyApp(App):
    def build(self):
        screen_manager = MyScreenManager()
        screen_manager.add_widget(LoginScreen(name='login_screen1'))
        screen_manager.add_widget(SecondScreen(name='second_screen1'))
        screen_manager.add_widget(ThirdScreen(name='third_screen1'))
        screen_manager.add_widget(PopUpP(name='other_screen1'))
        screen_manager.swipe_distance = 50
        return screen_manager


if __name__ == '__main__':
    MyApp().run()
