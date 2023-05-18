import os

import requests
from bs4 import BeautifulSoup
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import AsyncImage
from kivy.uix.screenmanager import Screen, ScreenManager, SlideTransition
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.anchorlayout import AnchorLayout
from kivymd.uix.bottomsheet import MDCustomBottomSheet
from kivy.factory import Factory
from kivymd.app import MDApp
from kivymd.uix.toolbar import MDTopAppBar
from kivy.uix.textinput import TextInput


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
        # self.autification()
        MDApp.get_running_app().root.current = 'second_screen'

    def get_image_task():
        return self.dict_task_image

    def autification(self):
        ses = requests.Session()
        ses.post('https://api.100points.ru/login',
                 data={'email': str(self.username_input.text),
                       'password': str(self.password_input.text),
                       '_xsrf': '_xsrf',
                       'remember': '1'})

        ses.post("https://api.100points.ru/shift/start",
                 data={"checked_25": "25"})  # запрос начать смену
        student = ses.get("https://api.100points.ru/exchange/index")
        print(student.text)
        soup_student = BeautifulSoup(student.text, 'lxml')
        id_student_mat = student.url
        id_student = re.search(r'/\d+', id_student_mat)
        id_student = id_student[0][1:]
        name_student = soup_student.find(attrs={"readonly": not (None)})
        name_student = name_student.get("value").strip()
        # ses.post("https://api.100points.ru/exchange/block/" + id_student)  # запрос начать проверку
        # student.response = Error.ckeced_500(student.href.get('href'))
        # soup_student = BeautifulSoup(student.response.text, 'lxml')

        point_name = soup_student.find_all("select",
                                           class_="form-control")
        checked_name = soup_student.find_all(
            class_="custom-control-input")
        comment_name = soup_student.find_all("textarea",
                                             class_="form-control comment-form-children")
        size_c_n = len(checked_name)
        l = 0
        while (l < size_c_n):
            checked_name[l] = checked_name[l].get("name")
            if checked_name[l] == None:
                checked_name.pop(l)
                size_c_n -= 1
                l = l - 1
            l += 1
        for l in range(len(point_name)):
            point_name[l] = point_name[l].get("name")
            comment_name[l] = comment_name[l].get("name")
        blocks = soup_student.find_all(string="Прикрепленный документ")

        checked_files = [0] * len(blocks)
        solition_task = [0] * len(blocks)

        solition_task_count = 0
        dict_task_image = {}
        for l in range(len(blocks)):
            block_files = blocks[
                l].parent.parent.parent.next_sibling.next_sibling
            if (block_files.text.find("Файлы ученика") != -1):
                checked_files[l] = 1
                solition_task[solition_task_count] = str(blocks[
                                                             l].parent.parent.parent)  # решение конкретной задачи
                solition_task_count += 1
                self.dict_task_image["task_" + str(l + 1)] = ""
                # os.mkdir("dz/task_" + str(l + 1))
                files = blocks[
                    l].parent.parent.parent.next_sibling.next_sibling.find(
                    "ul", class_="mailbox-attachments")
                if files == None:
                    continue
                files = files.find_all("li")
                for i in range(len(files)):
                    files[i] = files[i].find("a")["href"]
                    rashirenie = str(files[i]).split('.')
                    rashirenie = rashirenie[-1]
                    mas_image_task = []
                    mas_image_task.append(files[i])
                    # urllib.request.urlretrieve(files[i],
                    # "dz/task_" + str(
                    #  l + 1) + "/" + str(
                    #  i + 1) + "." + rashirenie)
                self.dict_task_image["task_" + str(l + 1)] = mas_image_task

        count_w = 0
        point = [-1] * len(point_name)
        comment = [""] * len(comment_name)

        while len(point_name) > count_w:
            if checked_files[count_w] == 0:  # нет файла в задании
                point[count_w] = 0
                comment[count_w] = ""

            count_w = count_w + 1

        # solition_task
        # student.set_data(id_student, checked_name, point_name, point,
        # comment_name, comment)
        # self.student = student
        # if not (1 in checked_files):


class SecondScreen(Screen):
    def __init__(self, **kwargs):
        super(SecondScreen, self).__init__(**kwargs)
        self.pic_path = os.path.join(os.path.dirname(__file__), 'pic')
        self.file_list = os.listdir(self.pic_path)
        self.current_index = 0

        layout = AnchorLayout(anchor_x='center', anchor_y='top')

        box_layout = BoxLayout(orientation='vertical', height=500, padding=100,
                               spacing=15)
        self.image = AsyncImage(source='http://mywebsite.com/logo.png')
        box_layout.add_widget(self.image)

        layout.add_widget(box_layout)

        button_layout = BoxLayout(orientation='horizontal', size_hint=(1, 1),
                                  spacing=10)
        prev_button = Button(size_hint=(.1, 1), background_color=(0, 0, 0, 0))
        prev_button.bind(on_press=self.show_previous_image)
        next_button = Button(size_hint=(.1, 1), background_color=(0, 0, 0, 0))
        next_button.bind(on_press=self.show_next_image)

        button_layout.add_widget(prev_button)

        button_layout.add_widget(next_button)

        layout.add_widget(button_layout)

        float_layout = FloatLayout(size_hint=(.8, 1),
                                   pos_hint={'x': 0, 'y': 0})
        circular_button = Button(size_hint=(None, None),
                                 size=(150, 150),
                                 pos_hint={'center_x': .5, 'y': 0},
                                 background_normal='free-icon-power-button-1783327.png',
                                 background_down='free-icon-power-button-1783327.png',
                                 on_press=self.open_bottomsheet)
        float_layout.add_widget(circular_button)

        layout.add_widget(float_layout)

        self.add_widget(layout)

    def open_bottomsheet(self, obj):
        self.topappbar = MDTopAppBar(title='fff')
        self.textarea = TextInput(hint_text='Enter text...')
        self.obj = MDCustomBottomSheet(screen=Factory.CustomBottomSheet(),animation=True, radius=20)

        self.obj.open()

    def get_current_image_path(self):
        if self.file_list:
            return os.path.join(self.pic_path,
                                self.file_list[self.current_index])
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

class CustomBottomSheet(BoxLayout):
    my_variable = StringProperty("Hello, World!")
class ThirdScreen(Screen):
    def __init__(self, **kwargs):
        super(ThirdScreen, self).__init__(**kwargs)
        self.add_widget(Label(text='Это второй экран'))


class MyScreenManager(ScreenManager):
    my_title = ObjectProperty(None)
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


class MyApp(MDApp):
    def build(self):
        self.screen_manager = MyScreenManager()
        self.screen_manager.add_widget(LoginScreen(name='login_screen1'))
        self.screen_manager.add_widget(SecondScreen(name='second_screen1'))
        self.screen_manager.add_widget(ThirdScreen(name='third_screen1'))
        self.screen_manager.swipe_distance = 50
        return self.screen_manager


if __name__ == '__main__':
    MyApp().run()
