from kivy.app import App
# from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget 
from kivy.uix.camera import Camera
from kivy.uix.popup import Popup
from pyzbar.pyzbar import decode
from kivy_garden.zbarcam import ZBarCam
import cv2
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.uix.image import AsyncImage
from kivy.uix.spinner import Spinner
import requests
import json
from kivy.network.urlrequest import UrlRequest
import json
import qrcode
from kivy.uix.recycleview import RecycleView
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, NumericProperty, ListProperty
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.spinner import SpinnerOption
from kivy.factory import Factory
from datetime import datetime

from kivy.lang import Builder



# I set the color constants to then color the text on the buttons (this is optional)
red = (255 / 255, 67 / 255, 67 / 255)
green = (0 / 255, 158 / 255, 60 / 255)




class MainApp(App):
    def build(self):
        sm = ScreenManager()
        var = None
        
        # here I add the main and second screens to the manager, this class does nothing else
        sm.add_widget(MainScreen())
        
        sm.add_widget(AutorizationScreen())
        sm.add_widget(RegistretionScreen())
        sm.add_widget(ProfilScreen())
        sm.add_widget(ScannerScreen())
        sm.add_widget(ProductScreen())
        sm.add_widget(SaleScreen())
        sm.add_widget(MarketQRScreen())
        sm.add_widget(QRScreen())
        sm.add_widget(HistoryScreen())
        sm.add_widget(HistoryPageScreen())
        return sm  # I return the manager to work with him later


class MainScreen(Screen):
    def __init__(self):
        super().__init__()

        self.name = 'Main'  # setting the screen name value for the screen manager
         #(it's more convenient to call by name rather than by class)

        main_layout = FloatLayout()  # creating an empty layout that's not bound to the screen

        self.add_widget(main_layout)  # adding main_layout on screen

        # Button
        Go_AuthScreen = Button(text='Вход',
                            size_hint=(.5, .2),
                            pos_hint={'center_x': .5, 'center_y': .8},
                            color=red)
        
        Go_RegScreen = Button(text='Регистрация',
                            size_hint=(.5, .2),
                            pos_hint={'center_x': .5, 'center_y': .2},
                            color=red)

        Go_AuthScreen.bind(on_press=self.to_auth_scrn)  # setting up a button to perform an action when clicked
         
        Go_RegScreen.bind(on_press = self.to_reg_scrn)

        main_layout.add_widget(Go_AuthScreen)  # adding button on layout

        main_layout.add_widget(Go_RegScreen)

    def to_auth_scrn(self, *args):
        self.manager.current = 'Autorization'  # selecting the screen by name (in this case by name "Second")
        return 0  # this line is optional
    def to_reg_scrn(self,*args):
        self.manager.current = 'Registretion'
        return 0
    
class AutorizationScreen(Screen):
    def __init__(self):
        super().__init__()
    # on this screen, I do everything the same as on the main screen to be able to switch back and forth
        self.name = 'Autorization'
        second_layout = FloatLayout()
        b = BoxLayout()
        self.add_widget(second_layout)
        self.add_widget(b)

        # Button
        Go_Back = Button(text='Go to Main screen',
                         size_hint=(.2, .2),
                         pos_hint={'center_x': .1, 'center_y': .9},
                         color=green)

        Go_Back.bind(on_press=self.to_main_scrn)

        
        my_text_input_name = TextInput(
                         size_hint=(.2, .055),
                pos_hint={'center_x': .5, 'center_y': .6},
               hint_text = "e-mail",
                multiline=False)
        
        self.ids['my_text_input_name'] = my_text_input_name
        my_text_input_name = self.ids.my_text_input_name

        my_text_input_password = TextInput(
                         size_hint=(.2, .055),
                pos_hint={'center_x': .5, 'center_y': .4},
               hint_text = "password", password = True, multiline=False
               )
        
        self.ids['my_text_input_password'] = my_text_input_password
        my_text_input_password = self.ids.my_text_input_password
        
        Form_button = Button(text='Enter',
                         size_hint=(.2, .15),
                         pos_hint={'center_x': .5, 'center_y': .1},
                         color=red
                         )
        Form_button.bind(on_press=self.auth_press)

        second_layout.add_widget(Go_Back)
        
        second_layout.add_widget(my_text_input_name)
        second_layout.add_widget(my_text_input_password)
        second_layout.add_widget(Form_button)
    
    def get_var(self):
        from kivy.app import App
        App.get_running_app().var = self.ids.my_text_input_name.text
        return App.get_running_app().var

    def auth_press(self, instance):
        username = self.ids.my_text_input_name.text
        
        password = self.ids.my_text_input_password.text
        url = 'http://127.0.0.1:5000/auth'
        data = {'username': username, 'password': password}
        
        response = requests.get(url, json=data)
        if response.status_code == 200:
            data = response.json()
            user_id = data.get('user_id')
            ProfilScreen = self.manager.get_screen('Profil')
            self.manager.get_screen('Profil').label_user_id.text = str(user_id)
            ProfilScreen.update_label(self.ids.my_text_input_name.text,user_id)
            self.manager.current = ('Profil') 
        else:
            self.manager.current = 'Autorization'
        #print(name)
    

    def to_main_scrn(self, *args):  # together with the click of the button, it transmits info about itself.
        # In order not to pop up an error, I add *args to the function
        self.manager.current = 'Main'
        return 0


class RegistretionScreen(Screen):
    def __init__(self):
        super().__init__()
    # on this screen, I do everything the same as on the main screen to be able to switch back and forth
        self.name = 'Registretion'
        second_layout = FloatLayout()
        self.add_widget(second_layout)

        # Button
        Go_Back = Button(text='Назад',
                         size_hint=(.1, .1),
                         pos_hint={'center_x': .1, 'center_y': .9},
                         color=green)

        Go_Back.bind(on_press=self.to_main_scrn)

        Label_hi = Label(text = "Зарегистрируйтесь в приложении!", 
                        size_hint = (0.5,0.5),
                        pos_hint ={'center_x': .5, 'center_y': .9 })
        
        my_text_input_reg_name = TextInput(
                         size_hint=(.2, .055),
                pos_hint={'center_x': .5, 'center_y': .7},
               hint_text = "first name")
        
        self.my_text_input_reg_sname = TextInput(
                         size_hint=(.2, .055),
                pos_hint={'center_x': .5, 'center_y': .63},
               hint_text = "second name")
        
        self.my_text_input_reg_email = TextInput(
                         size_hint=(.2, .055),
                pos_hint={'center_x': .5, 'center_y': .56},
               hint_text = "e-mail")
        my_text_input_reg_emaill = TextInput(
                         size_hint=(.2, .1),
                pos_hint={'center_x': .5, 'center_y': .5},
               hint_text = "e-mail")

        self.sec_layout = BoxLayout(orientation = 'horizontal')
        self.sec_layout.pos = (320,280)
        self.day_input = TextInput(hint_text='DD', size_hint=(None, None), size=(45, 30))
        self.month_input = TextInput(hint_text='MM', size_hint=(None, None), size=(45, 30))
        self.year_input = TextInput(hint_text='YYYY', size_hint=(None, None), size=(70, 30))
        
        self.sec_layout.add_widget(self.day_input)
        self.sec_layout.add_widget(self.month_input)
        self.sec_layout.add_widget(self.year_input)

        second_layout.add_widget(self.sec_layout)
        
        self.ids['my_text_input_reg_name'] = my_text_input_reg_name
        my_text_input_reg_name = self.ids.my_text_input_reg_name

        my_text_input_reg_pass = TextInput(
                         size_hint=(.2, .1),
                pos_hint={'center_x': .5, 'center_y': .4},
               hint_text = "password",
               password = True
               )
        
    
        
        self.ids['my_text_input_reg_pass'] = my_text_input_reg_pass
        my_text_input_reg_pass = self.ids.my_text_input_reg_pass

        Reg_button = Button(text='Enter',
                         size_hint=(.2, .15),
                         pos_hint={'center_x': .5, 'center_y': .1},
                         color=red
                         )
        
        Reg_button.bind(on_press=self.reg_press)
        

        second_layout.add_widget(Go_Back)
        second_layout.add_widget(Label_hi)
        second_layout.add_widget(my_text_input_reg_name)
        second_layout.add_widget(self.my_text_input_reg_sname)
        second_layout.add_widget(self.my_text_input_reg_email)
        second_layout.add_widget(my_text_input_reg_pass)
        second_layout.add_widget(Reg_button)

       
    def reg_press(self,instance):
        first_name = self.ids.my_text_input_reg_name.text

        second_name = self.my_text_input_reg_sname.text

        email = self.my_text_input_reg_email.text

        password = self.ids.my_text_input_reg_pass.text

        day = self.day_input.text
        monhts = self.month_input.text
        year = self.year_input.text

        date = year + '-' + monhts +'-' + day

        print(date)

        url = 'http://127.0.0.1:5000/reg'
        data = {'first_name': first_name, 'second_name': second_name, 'email': email , 'date': date, 'password': password}
        
        response = requests.get(url, json=data)

        
        if response.status_code == 200:
            data = response.json()
            user_id = data.get('user_id')
            print(user_id)
            print('User registered successfully')
            ProfilScreen = self.manager.get_screen('Profil')
            ProfilScreen.update_label(self.ids.my_text_input_reg_name.text, user_id)
            self.manager.current = ('Profil') 
        else:
            print('Error:', response.json().get('error'))
            self.manager.current = 'Autorization'
        #db.conn_db(name, password)
        if data == 200:
            #db.conn_addUser_db(name,password)
            pass
        else:
            pass



    def to_main_scrn(self, *args):  # together with the click of the button, it transmits info about itself.
        # In order not to pop up an error, I add *args to the function
        self.manager.current = 'Main'
        return 0
class MySpinnerOption(SpinnerOption):
    pass

class MyWidget(RelativeLayout):
    def spinner_selected(self, text):
        print(f'Spinner selected: {text}')
    
class ProfilScreen(Screen):
    def on_spinner_change(self, spinner, text):
        # Функция, которая будет вызываться при изменении значения Spinner
        print(f'Spinner value changed to: {text}')

    def __init__(self,**kwargs):
        super().__init__()
    # on this screen, I do everything the same as on the main screen to be able to switch back and forth
        self.name = 'Profil'
        self.second_layout = FloatLayout()
        self.add_widget(self.second_layout)

        # Button
        Go_Back = Button(text='Выход',
                         size_hint=(.1, .1),
                         pos_hint={'center_x': .1, 'center_y': .9},
                         color=green)

        Go_Back.bind(on_press=self.to_main_scrn)

        layout_addres = BoxLayout()

        self.adress = []
        widget = MyWidget()

        Factory.register('MySpinnerOption', cls=MySpinnerOption)

        self.spiner = Spinner(text = 'self.adress[0]',
                         option_cls=MySpinnerOption,
                         size_hint = (None,None),
                         size = (220,80),
                         pos_hint={'center_x': .85, 'center_y': .9})
        
        self.spiner.bind(text=widget.spinner_selected)
        
        self.second_layout.add_widget(self.spiner)

        Marker_QR = Button(text='QR магазина',
                         size_hint=(.15, .1),
                         pos_hint={'center_x': .5, 'center_y': .9},
                         color=green)
        self.second_layout.add_widget(Marker_QR)

        Marker_QR.bind(on_press = self.to_skan_market_qr)

        Go_Scan = Button(text='Scan',
                         size_hint=(.1, .1),
                         pos_hint={'center_x': .5, 'center_y': .3},
                         color=green)

        Go_Scan.bind(on_press=self.to_scan_scrn)

        Go_History = Button(text='Scan',
                         size_hint=(.1, .1),
                         pos_hint={'center_x': .5, 'center_y': .5},
                         color=green)

        Go_History.bind(on_press=self.to_history_scrn)

        self.user = Label(text = "8",)

        self.spiner = Spinner(
                         
                         size_hint = (None,None),
                         size = (220,80),
                         pos_hint={'center_x': .85, 'center_y': .9})
        
        #self.spiner.bind(on_text = self.on_spiner_selection)
        #self.spiner.bind(on_release = self.show_selected_value(self.spiner,self.spiner.text))
        self.second_layout.add_widget(self.spiner)
       
        
        self.label = Label(text='Текст из ввода будет здесь')
        self.add_widget(self.label)
        self.labelName = Label()

        self.label_user_id = Label(text='Текст из ввода будет здесь')

        self.second_layout.add_widget(Go_Back)
        self.second_layout.add_widget(Go_Scan)
        self.second_layout.add_widget(Go_History)

        self.code = Label()
        self.if_btn = Label()
        self.guid = Label()

    def show_selected_value(self,spiner, text):
        c = 5555555555555555
        print(c)

    def to_skan_market_qr(self, instance):
        market_code = self.code.text
        type = 'QR'
        self.manager.get_screen('Scanner').update_barcode(type, market_code)
        self.manager.current = 'Scanner'

    def to_history_scrn(self, instance):
        
        #type = 'History'
        self.manager.get_screen('History').update_history(self.labelName.text)
        self.manager.current = 'History'

    def update_detected_qr(self,market_code):

        url = 'http://127.0.0.1:5000/qr?market_code=' + market_code
        #params = {'market_code': market_code }
        
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            print(data)
            username = data.get('data')
            print(username)
            result_string = ''.join(username)
            self.spiner.text = result_string
       # Дальнейшая обработка полученного значения
        else:
            print('Failed to get data from server')
        
        address = 1 # db.get_address(market_code)
        
        #values_str = ' '.join(map(str, address))
        #print(values_str)
        #self.spiner.text = values_str
        #print(self.spiner.text)


    #def on_spiner_selection(self, *args):
        #print("Выбран адресс:", args[1])
       
    def update_label(self, text, uset_id):
        self.labelName.text = text
        self.label.text = f"Здравствуйте, {text}"
        self.label_user_id.text = str(uset_id)
        print(uset_id)
        print('-------------------------')
        print()
        print('-------------------------')
        url = 'http://127.0.0.1:5000/get_address?market_code =' + str(uset_id)
        response = requests.get(url)

        if response.status_code == 200:
           
            #formatted_addresses = [{'text': address, 'index': str(index)} for index, address in enumerate(user_addresses)]
            data = response.json()
            print(data) #вывод - {'data': "['Московская 167', 'Российская 46', 'Петра Метальникова 5', 'Мечникова 130']"}
            user_id = data.get('data')
            print(user_id)
            print(user_id[0])
            
                
            self.adress = []
            self.spiner.text = user_id[0]
            self.spiner.values = user_id
        print('-------------------------')
        print(self.spiner.text)
        print('-------------------------')



        data = {'user_id': uset_id, 'address': self.spiner.text}
        
        url = 'http://127.0.0.1:5000/get_orders?user_id =' + str(self.label_user_id.text)
        response = requests.get(url,json=data)
        datas = response.json()
        order_sum = datas.get('order_sum')
        order_id = datas.get('order_id')
        market_address = datas.get('address')
        print(market_address)
        if order_sum > 0:
            self.guid.text = order_id
            self.if_btn.text = '1'
            self.Go_sales_back = Button(text='назад к покупке',
                         size_hint=(.1, .1),
                         pos_hint={'center_x': .3, 'center_y': .3},
                         color=green)
            #self.Go_sales_back.bind(on_press=ProfilScreen.to_last_buy(order_id ,market_address ))
            
            self.second_layout.add_widget(self.Go_sales_back)
            self.Go_sales_back.bind(on_press=lambda instance: self.to_last_buy(order_id, market_address))
        
    def to_last_buy(self, order_id,market_address):
        
        self.manager.get_screen('Sale').last_cart(order_id,self.labelName.text, market_address)
        self.manager.current = 'Sale'
        self.second_layout.remove_widget(self.Go_sales_back)
        self.if_btn.text = '0'
        

    def to_scan_scrn(self, type):
        if self.if_btn.text == '1':
            self.second_layout.remove_widget(self.Go_sales_back)
            self.if_btn.text = '0'
            datas = {'guid': self.guid.text, 'user_id': self.label_user_id.text}
            url = f'http://127.0.0.1:5000/end_buy'
        
            response = requests.get(url, json=datas)


        type = 'BarCode'
        data = {'user_id': self.labelName.text, 'address': self.spiner.text}

        url = f'http://127.0.0.1:5000/uuid'
         
        
        response = requests.get(url, json=data)

        if response.status_code == 200:
            data = response.json()
            guid = data.get('guid')
            market_code = data.get('market_code')
            self.code.text = market_code
            print(market_code)
            print(guid)

            self.manager.get_screen('Scanner').update_qr(type,self.code.text,guid, self.labelName.text)
        self.manager.current = 'Scanner'
        

    def to_main_scrn(self, *args):  # together with the click of the button, it transmits info about itself.
        # In order not to pop up an error, I add *args to the function
        self.manager.current = 'Main'
        return 0
    
    #def update_detected_barcode(self, barcode):

        
    #    result = db.get_image(barcode)

    #    self.spiner.text = result
    #    print(result)
        
    

class ScannerScreen(Screen):
    def __init__(self,**kwargs):
        super().__init__()
    # on this screen, I do everything the same as on the main screen to be able to switch back and forth
        self.name = 'Scanner'
        second_layout = FloatLayout()
        self.add_widget(second_layout)

        # Button
        Go_Back = Button(text='Выход',
                         size_hint=(.1, .1),
                         pos_hint={'center_x': .1, 'center_y': .9},
                         color=green)

        Go_Back.bind(on_press=self.to_main_scrn)

        

        self.zbar = ZBarCam(
                        
                         size_hint=(.9, .3),
               pos_hint={'center_x': .5, 'center_y': .4}
               
               )
        #self.zbar.disabled=True
        #self.zbar.stop()

        self.type = Label()
        self.guid = Label()
        self.user_id = Label()
        self.address = Label()
        
        #self.ids['self.zbar'] = self.zbar
        #self.zbar = self.ids.zbar

        self.zbar.bind(symbols=self.on_symbols)

        ladel = Label(text='Scan a barcode...')

        second_layout.add_widget(Go_Back)
        second_layout.add_widget(self.zbar)
        second_layout.add_widget(ladel)

    def update_barcode(self, type, market_address):
        self.type.text = type
        self.address.text = market_address
        print("////////////////////////////////////")
        print(self.address.text)
        print(market_address)
        self.zbar.size_hint = (0.5,0.5)

    def update_qr(self,type,market_address, guid, user_id):
        self.type.text = type
        self.address.text = market_address
        self.guid.text = guid
        self.user_id.text = user_id
        print(f"Sale_guid:{guid},   Label guid: {self.guid.text}")
        print("////////////////////////////////////1111111111111111111")
        print(self.address.text)
        self.zbar.size_hint = (0.8,0.3)
    def on_symbols(self,instance, symbols):

        if self.type.text == 'BarCode':
            if symbols:
                product_code = str(symbols[0].data)
                product_code = product_code.strip("b")
                product_code = product_code.strip("'")
                print("Barcode detected:", (product_code))
                print(self.address.text)
                #print(self.address.text)
                print(self.guid.text)
                print(self.user_id.text)

                self.manager.get_screen('Product').update_detected_barcode(product_code, self.address.text, self.guid.text, self.user_id.text)
                self.manager.current = 'Product'

        if self.type.text == 'QR':
            if symbols:
                market_code = str(symbols[0].data)
                market_code = market_code.strip("b")
                market_code = market_code.strip("'")
                print("Barcodeeeeeee detected:", (market_code))
                self.manager.get_screen('Profil').update_detected_qr(market_code)
                self.manager.current = 'Profil'

            
            

    def clear_cart(self, sale_screen_instance):
        # Очищаем корзину покупок (очищаем details_layout на экране Sale)
        sale_screen_instance.card_layout.clear_widgets()
        sale_screen_instance.update_price() 


    def to_main_scrn(self, *args):  # together with the click of the button, it transmits info about itself.
        # In order not to pop up an error, I add *args to the function
        self.manager.current = 'Profil'
        sale = SaleScreen()
        self.manager.get_screen('Sale').clear_cart()
        
        """
        необходимо дописать функциональность 

        1. переход на страницу подтверждения сброса покупки
        2. если покупка сброшена, то в бд меняется запись покупки(отменена) и переход на гравный экран
        3. если покупка не отменена, то переход обратно в режим сканера!

        """
        return 0

        
class ProductScreen(Screen):
    def __init__(self,**kwargs):
        super().__init__()
    # on this screen, I do everything the same as on the main screen to be able to switch back and forth
        self.name = 'Product'
        second_layout = FloatLayout()
        self.add_widget(second_layout)



        Go_Scan = Button(text='Scan',
                         size_hint=(.1, .1),
                         pos_hint={'center_x': .1, 'center_y': .9},
                         color=green)
        
        Go_Buy = Button(text='Go_Buy',
                         size_hint=(.1, .1),
                         pos_hint={'center_x': .1, 'center_y': .1},
                         color=green)

        Go_Scan.bind(on_press=self.to_scan_scrn)
        Go_Buy.bind(on_press = lambda instance: self.add_product_to_card(product))
        

        self.img = AsyncImage(size_hint=(.3, .3),
                              allow_stretch=True,
                         pos_hint={'center_x': .85, 'center_y': .8}) 

        self.add_widget(self.img)
        self.add_widget(Go_Buy)

        self.price = Label(text = ' Текст из ввода будет здесь',
                           pos_hint = {'center_x': 0.5, 'center_y': 0.5})
        self.add_widget(self.price)

        self.barcode = Label(text = '')
        
        self.label = Label(text='Текст из ввода будет здесь',
                           size_hint=(.5, .5),
                           pos_hint={'center_x': .5, 'center_y': .8})
        self.add_widget(self.label)

        Go_Sale = Button(text = 'В корзину',
                         size_hint=(.2, .1),
                         pos_hint={'center_x': .5, 'center_y': .3},
                         color=green)
        Go_Sale.bind(on_press = self.to_sale_scrn)

        self.labelprod = Label(text='Текст из ввода будет здесь',
                           size_hint=(.5, .5),
                           pos_hint={'center_x': .5, 'center_y': .6})
        self.add_widget(self.labelprod)

        second_layout.add_widget(Go_Scan)
        second_layout.add_widget(Go_Sale)
        self.n = 1
        self.label_count = Label(text = str(self.n),
                                 size_hint=(.2, .1),
                         pos_hint={'center_x': .5, 'center_y': .5}
                         )
        second_layout.add_widget(self.label_count)

        plus = Button(text = '+',
                         size_hint=(.05, .05),
                         pos_hint={'center_x': .7, 'center_y': .5},
                         color=green)
        plus.bind(on_press = self.plus_count)
        second_layout.add_widget(plus)

        minus = Button(text = '-',
                         size_hint=(.05, .05),
                         pos_hint={'center_x': .3, 'center_y': .5},
                         color=green)
        minus.bind(on_press = self.minus_count)
        second_layout.add_widget(minus)

        self.address = Label()
        self.guid = Label()
        self.user_id = Label()
        self.prod_id = Label()
        product = Product(self.label.text, self.price.text, self.labelprod.text, self.img.source,self.barcode.text,self.label_count.text)

    def plus_count(self, instance):
        self.n += 1
        self.label_count.text = str(self.n)

    def minus_count(self, instance):
        if self.n != 1:
            self.n -= 1
            self.label_count.text = str(self.n)

    def add_product_to_card(self,product):
         #db.add_product_sale(self.label.text,self.labelprod.text,self.img.source)
         SaleScreen = self.manager.get_screen('Sale')
         f = self.barcode.text
         bar_code = str(f)
         address = self.address.text
         #result,price, res, textprod, f = db.get_image(v)
         data = {'bar_code': bar_code, 'address': address, 'guid': self.guid.text, 'user_id': self.user_id.text}
        
        

         url = f'http://127.0.0.1:5000/barcode'
         #params = {'market_code': market_code }
        
         response = requests.get(url, json=data)

         if response.status_code == 200:
            data = response.json()
            image_path = data.get('image_path')
            print(image_path)
            #image_path = ''.join(image_path)

            price = data.get('priceprod')
            price = str(price)
            #price = ''.join(price)

            name = data.get('nameprod')
            #name = ''.join(name)

            textprod = data.get('textprod')
            #textprod= ''.join(textprod)

            product = data.get('codeprod')
            #product = ''.join(product)
            print(image_path,price,name,textprod,product)

            url2 = f'http://127.0.0.1:5000/add_prod_to_cart'
            data1 = {'bar_code': self.prod_id.text, 'address': address, 'guid': self.guid.text, 'user_id': self.user_id.text, 'count': self.label_count.text, 'price': price}
            response = requests.get(url2, json=data1)

         product = Product(name,price, textprod, image_path, f, self.label_count.text)
         SaleScreen.add_to_card(product, self.guid.text)
         SaleScreen.update_price()
         self.manager.current = ('Sale')
         self.n = 1
         self.label_count.text = str(self.n)

    def to_sale_scrn(self, instance):
        pass
        #SaleScreen = self.manager.get_screen('Sale')
        #SaleScreen.update_screen(self.label.text,self.labelprod.text,self.img.source)
        #self.manager.current = ('Sale') 
        #db.add_product_sale(self.label.text,self.labelprod.text,self.img.source)

    def sale(self, instance):
        SaleScreen = self.manager.get_screen('Sale')
        SaleScreen.update_screen_buy(self.img.source)
        SaleScreen.update_price()
        self.manager.current = ('Sale') 


    def update_detected_barcode(self, barcode, address, guid, user_id):

        bar_code = barcode
        self.guid.text = guid
        self.address.text = address
        self.user_id.text = user_id
        print("-------------------------")
        print(self.address.text)
        print("-------------------------")

        self.barcode.text = barcode
        #result,price, res, textprod, codeprod = db.get_image(barcode)
        #price = str(price)
        #print(result,price, res, textprod)
        #
       
        data = {'bar_code': bar_code, 'address': address}
        
        

        url = f'http://127.0.0.1:5000/barcode'
        #params = {'market_code': market_code }
        
        response = requests.get(url, json=data)

        if response.status_code == 200:
            data = response.json()
            image_path = data.get('image_path')
            print(image_path)
            #image_path = ''.join(image_path)

            price = data.get('priceprod')
            price = str(price)
            #price = ''.join(price)

            name = data.get('nameprod')
            #name = ''.join(name)

            textprod = data.get('textprod')
            #textprod= ''.join(textprod)

            product = data.get('codeprod')

            prod_id = data.get('prod_id')

            self.prod_id.text = str(prod_id)
            #product = ''.join(product)
            print(image_path,price,name,textprod,product)


        self.img.source = image_path 
        self.label.texture_update()
        self.label.text = name
        
        self.price.text = "Цена: " +price
        self.labelprod.text = textprod
        print(self.price.text, self.label.text)
        print(product)
        product = Product(name,price, textprod, image_path, product, self.label_count.text)
         
        

    def to_scan_scrn(self,instance):
        self.manager.current = 'Scanner'
        

    def to_main_scrn(self, *args):  # together with the click of the button, it transmits info about itself.
        # In order not to pop up an error, I add *args to the function
        self.manager.current = 'Main'
        return 0
    

class SaleScreen(Screen):
    def __init__(self,**kwargs):
        super().__init__()
    # on this screen, I do everything the same as on the main screen to be able to switch back and forth
        self.name = 'Sale'
        second_layout = FloatLayout()
        self.add_widget(second_layout)

        self.card_layout = BoxLayout(orientation ='vertical', size_hint = (.8,.8))

        #self.scroller = ScrollView()
        #self.scroller.add_widget(self.card_layout)

        #second_layout.add_widget(self.scroller)
        self.add_widget(self.card_layout)

        #second_layout.add_widget(self.scrollview)

        Go_Menu = Button(text='End Buy',
                         size_hint=(.1, .1),
                         pos_hint={'center_x': .9, 'center_y': .9},
                         color=green)
        

        Go_Scan = Button(text='Scan',
                         size_hint=(.1, .1),
                         pos_hint={'center_x': .1, 'center_y': .9},
                         color=green)
        
        self.total_price_lable = Label(  pos_hint={'center_x': .5, 'center_y': .1})

        second_layout.add_widget(self.total_price_lable)

        Go_Scan.bind(on_press=self.to_scan_scrn)
        Go_Menu.bind(on_press= self.get_label_values)

        self.layout = GridLayout()
        self.add_widget(self.layout)

        second_layout.add_widget(Go_Scan)
        second_layout.add_widget(Go_Menu)
        self.guid = Label()
        

    def update_price(self):
        label_values = []
        total_price = 0.0
        for child in self.card_layout.children:
            if isinstance(child, CardItem):
                label_values.append({
                    'name': child.name_label.text,
                    'price': child.price_label.text,
                    'count': child.label_count.text
                })
        for i in range(len(label_values)):

            price = label_values[i]['price'] 
            total_price += float(price)
            self.total_price_lable.text = f'Общая цена = {str(total_price)}'
            #total_price *=0

    def last_cart(self,guid,user_id, address):
        scanner_screen = self.manager.get_screen('Scanner')
        print(guid,user_id, address)
        scanner_screen.user_id.text = str(user_id)
        scanner_screen.type.text = 'BarCode'
        scanner_screen.guid.text = str(guid)
        scanner_screen.address.text = str(address)
        #self.type = Label()
        #self.guid.text = guid
        
        #self.address = Label()

        data = {'guid': guid}
        
        

        url = f'http://127.0.0.1:5000/last_sale'
        #params = {'market_code': market_code }
        
        response = requests.get(url, json=data)


        """self.name = name
        self.price = price
        self.productinfo = productinfo
        self.image_path = image_path
        self.barcode = barcode
        self.count = count"""
        datas = response.json()
        for item in datas:
            
            product_name = item['product_name']
            product_price = item['product_price']
            product_info = item['product_info']
            image_path = item['image_path']
            bar_code = item['bar_code']
            product_qty = item['product_qty']

            product = Product(product_name,product_price, product_info, image_path, bar_code, product_qty)
            self.add_to_card(product, guid)
        self.update_price()


    def to_menu_scrn(self,instance):
        self.manager.current = 'Profil'
        
    def add_to_card(self,product, guid):
        
        self.guid.text = guid
        self.card_item = CardItem(product)
        self.card_layout.add_widget(self.card_item)
        self.update_price()
        #print(self.card_layout.name_label.text)

    def clear_cart(self, instance):
        # Очищаем корзину покупок (очищаем details_layout)
        self.card_layout.clear_widgets()
        self.update_price() 

    def remove_item(self, index):
        # Удаляем элемент из card_layout по индексу
        self.card_layout.remove_widget(self.card_layout.children[index])
        # Перемещаем элементы поднимающееся выше
        for i in range(index + 1, len(self.card_layout.children)):
            self.card_layout.remove_widget(self.card_layout.children[i])
            self.card_layout.add_widget(self.card_layout.children[i], index=i-1)
       

    def get_label_values(self, instance):
        #label_values = []
        #for child in self.card_layout.children:
        #    if isinstance(child, CardItem):
        #        label_values.append({
        #            'name': child.name_label.text,
        #            'price': child.price_label.text,
        #            'count': child.label_count.text,
        #            'code': child.barcode_label.text
        #        })
        ## создание словаря с данными товаров
        #items = []
        #for i in range(len(label_values)):
            
        #    name = label_values[i]['name']
        #    price = label_values[i]['price']
        #    count = label_values[i]['count']
        #    code = label_values[i]['code']
        #    item_dict = {'name': name, 'price': price, 'count': count, 'code': code}
        #    items.append(item_dict)

            #a = a+ (code + ' ' + count + ' ' )
        #    print(f'название товара - {name}, цена товара - {price}, колличество - {count}, код - {code}')
            
        #data = json.dumps({'items': items})
        self.manager.get_screen('QRScreen').update_qr(self.guid.text)
        self.manager.current = 'QRScreen'
        #print(items)
        #self.manager.current = 'QRScreen'
        self.manager.get_screen('QRScreen').clear_cart(self)

    def clear_cart(self):
        # Очищаем корзину покупок (очищаем details_layout на экране Sale)
        self.card_layout.clear_widgets()
        self.update_price() 
    
    def update_screen_buy(self, imageprod):
        
        url = 'http://127.0.0.1:5000/barcode'
        #params = {'market_code': market_code }
        
        #response = requests.get(url, json=data)


        #res, cur = db.get_sale(imageprod)
        #self.layout.cols = len(res[0])
        
        #for column in cur:
        #    self.layout.add_widget(Label(text=column.name))
#
        #for r in res:
        #    for data in r:
        #        self.layout.add_widget(Label(text=str(data)))

    def to_scan_scrn(self,instance):
        self.manager.current = 'Scanner'
        

    def to_main_scrn(self, *args):  # together with the click of the button, it transmits info about itself.
        # In order not to pop up an error, I add *args to the function
        self.manager.current = 'Main'
        return 0
    

class QRScreen(Screen):
    def __init__(self,**kwargs):
        super().__init__()
    # on this screen, I do everything the same as on the main screen to be able to switch back and forth
        self.name = 'QRScreen'
        second_layout = FloatLayout()
        self.add_widget(second_layout)

        Go_Menu = Button(text='End buy',
                         size_hint=(.3, .1),
                         pos_hint={'center_x': .9, 'center_y': .9},
                         color=green)
        
        Go_Menu.bind(on_press=self.to_main_scrn)
        second_layout.add_widget(Go_Menu)
        self.guid = Label()
        """
        self.qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        self.qr.make(fit=True)

        qr_code_image = Image(source='qrcode.png')
        self.add_widget(qr_code_image)
        """
    def clear_cart(self, sale_screen_instance):
        # Очищаем корзину покупок (очищаем details_layout на экране Sale)
        sale_screen_instance.card_layout.clear_widgets()
        sale_screen_instance.update_price()  # Пересчитываем общую цену

    def to_main_scrn(self, *args):  # together with the click of the button, it transmits info about itself.
        # In order not to pop up an error, I add *args to the function
        url = 'http://127.0.0.1:5000/end_buy'
        data = {'guid': self.guid.text }
         
        response = requests.post(url, json=data)
        self.manager.current = 'Profil'
        return 0
    
    def update_qr(self,val):
        QR_code = val
        
        #url = 'http://127.0.0.1:5000/qr'

        #response = requests.get(url, json=val)

        #text = response.json()['qr_code']

        #print(text)

        #data = text
        self.guid.text = val
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(QR_code)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        img.save("qr_code.png")

        #SaleScreen.clear_cart()

        qr_image = Image(source="qr_code.png")
        self.add_widget(qr_image)

class DataRow(BoxLayout):
    text = StringProperty('')
    price = NumericProperty(0)
    quantity = NumericProperty(0)
    total = NumericProperty(0)
    number = NumericProperty(0)
    uuid = StringProperty('')


       
class HistoryScreen(Screen):
    def __init__(self):
        self.buttons = []
        super().__init__()
        second_layout = FloatLayout()
        self.add_widget(second_layout)

        self.name = 'History' 
        
        Go_Menu = Button(text='End buy',
                         size_hint=(.3, .1),
                         pos_hint={'center_x': .9, 'center_y': .9},
                         color=green)
        Go_Menu.bind(on_press=self.to_main_scrn)
        second_layout.add_widget(Go_Menu)

    def to_main_scrn(self, *args):
        for button in self.buttons:
            self.scroll_layout.remove_widget(button)
        self.manager.current = 'Profil'


    def update_history(self, user):
        user_id = user
        url = 'http://127.0.0.1:5000/history_sale'

        data = {'user_id': user }
        response = requests.get(url, json=data)
        data = response.json()

        self.scroll_layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.scroll_layout.bind(minimum_height= self.scroll_layout.setter('height'))
        
        for item in (data):
            date = item['date_order']
            date_obj = datetime.strptime(date, '%a, %d %b %Y %H:%M:%S %Z')
            
# Преобразование объекта datetime в строку с нужным форматом
            formatted_date = date_obj.strftime('%d.%m.%Y')
            print(date)
            price = item['price_order']
            order_id = item['order_id']
            button_text = f"{formatted_date} \n Price: {price}"
            button = Button(text=button_text, size_hint_y=None, height=50)
            button.ids['order_id'] = order_id
            self.buttons.append(button)
            self.scroll_layout.add_widget(button)
            button.bind(on_press=self.print_history)

        scroll_view = ScrollView(size_hint=(.5, 1), pos_hint={'top': .7})
        scroll_view.add_widget(self.scroll_layout)
        self.add_widget(scroll_view)

    def print_history(self, instance):
        order_id = str(instance.ids.get('order_id', 'No id found'))
        print("Button ID:", order_id)

        self.manager.get_screen('HistoryPage').current_order_id = order_id
        self.manager.get_screen('HistoryPage').update_history()
        self.manager.current = 'HistoryPage'

        

        #response = requests.get(url)
        
        
class HistoryPageScreen(Screen):
    def __init__(self):
        self.buttons = []
        self.current_order_id = None
        super().__init__()
        self.second_layout = FloatLayout()
        self.add_widget(self.second_layout)
        

        self.name = 'HistoryPage' 
        
        Go_Menu = Button(text='К истории покупок',
                         size_hint=(.3, .1),
                         pos_hint={'center_x': .9, 'center_y': .9},
                         color=green)
        Go_Menu.bind(on_press=self.to_main_scrn)
        self.second_layout.add_widget(Go_Menu)

    def clear_history_details(self):
        self.details_layout.clear_widgets()

    def to_main_scrn(self, *args):
        #for button in self.buttons:
        #self.scroll_layout.remove_widget(button)
        self.clear_history_details()
        self.manager.current = 'History'    

    def update_history(self):
        if self.current_order_id:
            print(self.current_order_id)
        else:
            print("No order_id passed")
        url = 'http://127.0.0.1:5000/history'

        order_id = self.current_order_id
        data = {'order_id': self.current_order_id }
        response = requests.get(url, json=data)

        datas = response.json()

        self.details_layout = GridLayout(cols=1, spacing=35, size_hint_y=None)
        self.details_layout.bind(minimum_height=self.details_layout.setter('height'))

        scroll_view = ScrollView(size_hint=(.5, 1), pos_hint={'top': .7})

        # Добавить ScrollView к second_layout перед добавлением виджетов
        self.second_layout.add_widget(scroll_view)

        scroll_view.add_widget(self.details_layout)

        self.l = Label()
        self.details_layout.add_widget(self.l)

        for purchase in datas:
            item_label = Label(text=f"{purchase['prod_name']} - {purchase['prod_price']} руб. - {purchase['prod_count']} шт. - {purchase['prod_sum']} руб.")
            self.details_layout.add_widget(item_label)
            
            #item_image = AsyncImage(source=purchase['image'])
            #self.ids.history_layout.add_widget(item_image)
        print(datas)
        

    
class Product:
    def __init__(self, name,price,productinfo,image_path, barcode, count):
        self.name = name
        self.price = price
        self.productinfo = productinfo
        self.image_path = image_path
        self.barcode = barcode
        self.count = count

class CardItem(BoxLayout):
    def __init__(self, product, **kwargs):
        super(CardItem,self).__init__(**kwargs)

        self.orientation = 'horizontal'

        self.image = AsyncImage(source = product.image_path,
                           size_hint = (0.3,0.3),pos_hint={'center_x': .1, 'center_y': .5}, )
        self.add_widget(self.image)

        self.details_layout = BoxLayout(orientation = 'horizontal')
        self.add_widget(self.details_layout)

        self.name_label = Label(text = product.name)
        
        self.price_db = str(round ((float(product.price) * int(product.count)), 2))
        self.bar_code = str(product.barcode)

        self.barcode_label = Label(text = self.bar_code)
        

        self.details_layout.add_widget(self.name_label)

        self.price_label = Label(text = self.price_db)

        self.plus_btn = Button(text = '-', size_hint = (0.1,0.1),pos_hint={'center_x': .8, 'center_y': .5}, on_press = self.label_plus)
        
        self.n = product.count
        self.first = SaleScreen()
        self.details_layout.add_widget(self.price_label)

        self.minus_btn = Button(text = '+', size_hint = (0.1,0.1),pos_hint={'center_x': .6, 'center_y': .5}, on_press = self.label_minus)
        self.label_count = Label(text = str(product.count), pos_hint={'center_x': .7, 'center_y': .5},)
        self.details_layout.add_widget(self.plus_btn)
        self.details_layout.add_widget(self.label_count)
        self.details_layout.add_widget(self.minus_btn)
        
        #self.details_layout.add_widget(self.barcode_label)

        

    def label_plus(self, instance):
        #SaleScreen = self.manager.get_screen('Sale')
        n = int(self.label_count.text)
        if n > 1:
            n -= 1
            price = float(self.price_db) * n
            self.price_label.text = str(price)
            self.label_count.text = str(n)
            sale_screen = self.parent.parent.parent.get_screen('Sale')
            sale_screen.update_price()
        else:
            n -= 1
            price = float(self.price_db) * n
            self.price_label.text = str(price)
            self.label_count.text = str(n)
            sale_screen = self.parent.parent.parent.get_screen('Sale')
            sale_screen.update_price()
            # Вызываем метод remove_item для удаления элемента из SaleScreen
            sale_screen.remove_item(sale_screen.card_layout.children.index(self))
            
    def label_minus(self, instance):
        #SaleScreen = self.manager.get_screen('Sale')
        n = int(self.label_count.text)
        sale_screen = self.parent.parent.parent.get_screen('Sale')
        n += 1
        price = float(self.price_db) * n
        self.label_count.text = str(n)
        self.price_label.text = str(price)
        sale_screen.update_price()


class MarketQRScreen(Screen):
    def __init__(self,**kwargs):
        super().__init__()
    # on this screen, I do everything the same as on the main screen to be able to switch back and forth
        self.name = 'MarketQR'
        second_layout = FloatLayout()
        self.add_widget(second_layout)

        # Button
        Go_Back = Button(text='Выход',
                         size_hint=(.1, .1),
                         pos_hint={'center_x': .1, 'center_y': .9},
                         color=green)

        Go_Back.bind(on_press=self.to_main_scrn)

        second_layout.add_widget(Go_Back)

        

        

    def to_main_scrn(self, *args):  # together with the click of the button, it transmits info about itself.
        # In order not to pop up an error, I add *args to the function
        self.manager.current = 'Profil'
        return 0
        



if __name__ == '__main__':
    MainApp().run()