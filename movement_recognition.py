from kivy.lang import Builder
import sqlite3
import pandas as np
import numpy as np
from kivy.properties import ObjectProperty
from kivy.core.window import Window
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivy.properties import StringProperty
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.floatlayout import FloatLayout
from kivymd.uix.card import MDCard
from kivymd.uix.list import TwoLineIconListItem, ThreeLineIconListItem
from kivymd.uix.list import TwoLineAvatarListItem, ThreeLineAvatarListItem
from kivymd.uix.list import ImageLeftWidget
from kivymd.uix.datatables import MDDataTable
from kivy.uix.widget import Widget
from kivy.factory import Factory
from kivy.clock import Clock
from datetime import timedelta,datetime
import matplotlib.pyplot as plt
from matplotlib import pyplot as plt


import plyer
from plyer import notification
from kivymd.app import MDApp
from tensorflow import lite

sensor_values  =([[0.75619871, 0.5690195 , 0.26307028],
       [0.75646628, 0.5692639 , 0.26322335],
       [0.75637709, 0.5686529 , 0.26204979],
       [0.75646628, 0.5692639 , 0.26337642],
       [0.75637709, 0.5686529 , 0.26352949],
       [0.75682304, 0.56950829, 0.26327437],
       [0.75664466, 0.5693861 , 0.26347846],
       [0.75673385, 0.5688973 , 0.26276412],
       [0.75022297, 0.57549604, 0.26551944],
       [0.70765697, 0.57512945, 0.2822109 ],
       [0.76004504, 0.57146348, 0.26322335],
       [0.75906394, 0.57024149, 0.26281514],
       [0.76049099, 0.57024149, 0.26317232]])

pause = False
remind = False
Window.size = [300, 450]

class WindowMan (ScreenManager):
    pass

class TasksOptions(Screen):
    conn = sqlite3.connect('userS.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user")
    exercises = cursor.fetchall()
    r = exercises[1][7]
    w =exercises[1][6]
    conn.commit()
    conn.close()
    def selectwalk(self):
        conn = sqlite3.connect('userS.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user")
        chosentask = cursor.fetchall()
        cursor.execute('''UPDATE user SET (MOVEMENT_2)= (?) WHERE id = ?''', (chosentask[1][6] ,1,))
        conn.commit()
        conn.close()
        walk = Notification()
        walk.showtask()
    def selectrun(self):
        conn = sqlite3.connect('userS.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user")
        chosentask = cursor.fetchall()
        cursor.execute('''UPDATE user SET (MOVEMENT_2)= (?) WHERE id = ?''', (chosentask[1][7] ,1,))
        conn.commit()
        conn.close()
        walk = Notification()
        walk.showtask()    
    
class Notification(Screen):
    global priod
    global pause
    global event
    global remind
    global event2
    
    def start(self):
        global pause
        global remind
        global event, event2
        if (pause == False) and (remind == False):
            print("start")
            conn = sqlite3.connect('userS.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM user")
            timer = cursor.fetchall()
            try:
                priod = int(timer[0][6])*60
                conn.commit()
                conn.close()
                event = Clock.schedule_interval(self.callback, priod)
            except:
                conn.commit()
                conn.close()  
                event = Clock.schedule_interval(self.callback, 7200)
        elif pause == True and remind == False:
            event.cancel()
            print("PAUSE") 

        elif pause == False and remind == True:
            event2 = Clock.schedule_once(self.callback2, 1800)
            print("Remind Me") 

    def callback(self, dt):
        print("alarm")
        plyer.notification.notify(title='Alarm', message="Do the task")   
    def callback2(self, dt):
        plyer.notification.notify(title='Reminder', message="Do the task")    
    
    def showtask(self):
        conn = sqlite3.connect('userS.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user")
        show = cursor.fetchall()
        return str(show[0][7])
        conn.commit()
        conn.close() 

class Queries(Screen):
    def Queries(self):
        conn=sqlite3.connect('userS.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user")
        graph = cursor.fetchall()
        walk = 0
        sit = 0
        run = 0
        for i in range (0,847,1) : 
            if int(graph[i][8])==2:
                walk += 1 
            elif int(graph[i][8])==1:
                run += 1 
            elif int(graph[i][8])==0:
                sit += 1
        conn.commit()
        conn.close()   
        x=['sitting', 'Walking', 'Running']
        y=[sit,walk,run]   
        print(sit)
        print(i)  
        #plt.clf()
        plt.bar(x,y)
        plt.title('whole data')
        plt.savefig('pic.png')
        self.root.get_screen('Queries').ids.Image.source= 'pic.png'    

class LoginPage(Screen):
    pass

class SignUp(Screen):
    user = ObjectProperty(None)
    password = ObjectProperty(None)
    def registeration(self):
        conn = sqlite3.connect('userS.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO user(NAME,AGE) VALUES(?,?)", (self.ids.user.text, self.ids.password.text) )
        cursor.execute('''UPDATE user SET (NAME,AGE)= (?,?) WHERE id = ?''', (self.ids.user.text, self.ids.password.text, 1,))
        conn.commit()
        conn.close()

class Setting(Screen):
    pass

class MainScreen(Screen):
    global pause
    def switch_pause(self, switchObject, switchValue):
        global pause
        # Switch value are True and False
        if(switchValue):
            pause = True     
        else:
            pause = False
        p = Notification()
        p.start()     
    
    global remind
    def switch_remind(self, switchObject, switchValue):
        global remind
        # Switch value are True and False
        if(switchValue):
            remind = True     
        else:
            remind = False
        p = Notification()
        p.start()   
    
    def Check_Out(self):
        global Tracemovement
        Tracemovement = False
        print("check_out")
    
    def Check_In(self):
        global k
        global Tracemovement
        k = 0
        Tracemovement = True
        print("Check_In")
        Clock.schedule_interval(self.callback, 30)
        
    def callback(self,dt):
        global k
        if (Tracemovement == True) & (pause == False):
            interpreter = lite.Interpreter(model_path ='app_GRU_model.tflite')
            interpreter.allocate_tensors()
            input_details = interpreter.get_input_details()
            output_details = interpreter.get_output_details()
            input_shape = input_details[0]['shape']
            list = np.array([sensor_values] , dtype=np.float32)
            input_data = list
            interpreter.set_tensor(input_details[0]['index'], input_data)
            interpreter.invoke()
            output_data = interpreter.get_tensor(output_details[0]['index'])
            label = np.argmax(output_data)
            conn = sqlite3.connect('userS.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO user(MOVEMENT) VALUES(?)", (str(label)) )
            cursor.execute('''UPDATE user SET (MOVEMENT)= (?) WHERE id = ?''', (label,k,))
            print(label)
            print(k)
            conn.commit()
            conn.close()
            k = k + 1       
             
class PersonalData(Screen):  
    job = ObjectProperty(None)
    name = ObjectProperty(None)
    age = ObjectProperty(None)
    weight = ObjectProperty(None)
    tall = ObjectProperty(None)
    movement = ObjectProperty(None)
    def submitdata(self): 
        conn = sqlite3.connect('userS.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO user(NAME,AGE,WEIGHT,TALL,JOB) VALUES(?,?,?,?,?)", (self.ids.name.text, self.ids.age.text, self.ids.weight.text, self.ids.tall.text , self.ids.JobPos.text ) )
        cursor.execute('''UPDATE user SET (NAME,AGE,WEIGHT,TALL,JOB)= (?,?,?,?,?) WHERE id = ?''', (self.ids.name.text, self.ids.age.text, self.ids.weight.text, self.ids.tall.text , self.ids.JobPos.text,2,))
        cursor.execute("SELECT * FROM user")
        exercises = cursor.fetchall()
        W = 30
        R = 15
        try:
            if (int(exercises[1][3])) > (int(exercises[1][4])-100) :
                W = W + 30
                R = R + 15
                if (exercises[1][5]) == 'Active' :
                    W = W - 15
                    R = R - 15
                if (int(exercises[1][2])) > 50:
                    W = W - 10
                    R = R - 10
            else:
                if (int(exercises[1][2])) > 50:     
                    W = W - 10
                    R = R - 10       
            w = str('Walk for {} mins'.format(W))
            r = str('Run for {} mins'.format(R))
            cursor.execute('''UPDATE user SET (MOVEMENT_1, MOVEMENT_2)= (?,?) WHERE id = ?''', (w,r,2,))
            #cursor.execute("DELETE FROM user_table WHERE id=3")
            conn.commit()
            conn.close()
        except:
            print("complete profile")  
 
class Allow(Screen):
    pass

class MainApp(MDApp):
    
    def build(self):
        return Builder.load_file('movement_recognition.kv')
    
    def checking(self):
        conn = sqlite3.connect('userS.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user")
        records = cursor.fetchall()
        if (records[0][2] == str(self.root.get_screen("LoginPage").ids.password.text)) and (records[0][1] == self.root.get_screen("LoginPage").ids.user.text):
            #self.root.ids.PersonalData.ids.name = records[1][1]
            self.root.current = "MainScreen"
            alarm = Notification()
            alarm.start()
        conn.commit()
        conn.close()
        
    try:
        conn = sqlite3.connect('userS.db')
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE user(id INTEGER PRIMARY KEY, NAME TEXT, AGE TEXT,WEIGHT TEXT,TALL TEXT,JOB TEXT, MOVEMENT_1 TEXT,MOVEMENT_2 TEXT, MOVEMENT PROFILE TEXT, TIME TEXT)")
        conn.commit()
        conn.close()
        print("created")
    except:
        print("existed")
    
    def submittimer(self): 
        conn = sqlite3.connect('userS.db')
        cursor = conn.cursor()
        cursor.execute('''UPDATE user SET (MOVEMENT_1)= (?) WHERE id = ?''', (self.root.get_screen("Notification").ids.timer.text,1,))
        conn.commit()
        conn.close()
    
    

# run app    
MainApp().run()