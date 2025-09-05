'''
pm.
    Dont delete any codes or else the code gets fucked
'''

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import *

import math, random, pathlib, os, json, sys

app = QApplication([])
size = QDesktopWidget().size()
print(f"Ideal Size: {size}")

# Folders
ref = pathlib.Path().resolve().parent

food_fol = ref/"moving-test"/"foods"
sound_fol = ref/"moving-test"/"sounds"
random_snd = ref/"moving-test"/"random_sounds"
bgr_fol = ref/"moving-test"/"bgr"
img_fol = ref/"moving-test"/"imgs"
log_fol = ref/"moving-test"/"logos"
spec_fol = ref/"moving-test"/"special_bgr"


# Pet Screen
main_screen = QWidget()
main_lay = QVBoxLayout()

main_screen.setFixedSize(200,200)


# Faces
smile = "ت"
sad = "˙◠˙"
medium = "•_•"

# Sound Effects
eat = QMediaContent(QUrl.fromLocalFile(str(sound_fol/"eat.mp3")))
pat = QMediaContent(QUrl.fromLocalFile(str(sound_fol/"pat.mp3")))
shop = QMediaContent(QUrl.fromLocalFile(str(sound_fol/"shop-open.mp3")))
deny = QMediaContent(QUrl.fromLocalFile(str(sound_fol/"lack.mp3")))
notif = QMediaContent(QUrl.fromLocalFile(str(sound_fol/"notif.mp3")))
money = QMediaContent(QUrl.fromLocalFile(str(sound_fol/"money.mp3")))
stinky = QMediaContent(QUrl.fromLocalFile(str(sound_fol/"stinky.mp3")))
pet_die = QMediaContent(QUrl.fromLocalFile(str(sound_fol/"pet-die.mp3")))
pet_hit = QMediaContent(QUrl.fromLocalFile(str(sound_fol/"pet-hit.mp3")))
npc_hit = QMediaContent(QUrl.fromLocalFile(str(sound_fol/"npc-hit.mp3")))
raid_soon = QMediaContent(QUrl.fromLocalFile(str(sound_fol/"raid-coming.mp3")))
shoot = QMediaContent(QUrl.fromLocalFile(str(sound_fol/"shoot.mp3")))
save = QMediaContent(QUrl.fromLocalFile(str(sound_fol/"save.mp3")))
hap_sound = QMediaContent(QUrl.fromLocalFile(str(sound_fol/"satisfied.mp3")))
win = QMediaContent(QUrl.fromLocalFile(str(sound_fol/"win.mp3")))
coming = QMediaContent(QUrl.fromLocalFile(str(sound_fol/"hecoming.mp3")))
buff = QMediaContent(QUrl.fromLocalFile(str(sound_fol/"buff.mp3")))

# Oh my fucking god, look at that list of sounds. 
# I could make a function to make this less cancerous to read
# ...
# But I don't feel like it


# Random Sounds List
rs_list = os.listdir(random_snd)


# System
tray = QSystemTrayIcon(QIcon(str(log_fol/"exec.png")),parent=app)
tray.show()

# Check-up Dialoges
dials = [
    "How are you today?",
    "Hope you are doing well!",
    "Hmm? What are you doing??",
    "It's nice to live in your computer!"
]

# =========
# Classes
# =========
# Special Windows
special_list = []
'''
    contains the order of the special windows

    the first item is always put up first

    it is determined through their id

'''

class Special(QWidget):
    
    # You do not know how long it took me to get this working. Jesus Christ.
    def __init__(self):
        super().__init__()
        self.id = random.randint(1,999)

    def return_focus(self):
        global special_list

        if len(special_list) > 0:
            if special_list[0] == self.id:

                if not self.isActiveWindow():
                   
                    self.setFocus()
                    self.activateWindow()
                    
                    self.raise_()

                
            
                if self.isHidden():
                    special_list.remove(self.id)
                    
                else:
                    QTimer.singleShot(100, self.return_focus)
            else:
                QTimer.singleShot(100, self.return_focus)
            
    def showEvent(self, a0):
        global special_list
        super().showEvent(a0)
        special_list.insert(0, self.id)
        print(f"Register Order: {special_list}")
        self.return_focus()

# Food Classes
class Food_Wid(QWidget):
    def __init__(self, item):
        global foods
        super().__init__()
        layout = QVBoxLayout()

        self.item = item

        img_holder = QLabel()

        layout.addWidget(img_holder)

        try:
            img_holder.setPixmap(QPixmap(str(food_fol/self.item)))
        except Exception as e:
            img_holder.setText("N/A")
        
        
        # Set Random Position
        get_geom = self.geometry()

        random_cord = (random.randint(0, 1000), random.randint(0, 500))
        get_geom.setX(random_cord[0])
        get_geom.setY(random_cord[1])
        get_geom.setWidth(150)
        get_geom.setHeight(100)

        self.setGeometry(get_geom)

        self.setWindowTitle(self.item)
        
        self.setLayout(layout)
        self.show()
        foods.append(self)

        # Food Data
        if item not in Food_Data:
            self.hunger = 5
            self.hap = 0
            self.override = False
        else:
            self.hunger = Food_Data[item]["hunger"]
            self.hap = Food_Data[item]["happiness"]
            self.override = Food_Data[item]["override"]
        
class FS_Layout(QVBoxLayout):
    def __init__(self, food_item):
        super().__init__()
        self.food = food_item

        # Img Hold
        img_holder = QLabel()
        img_holder.setFixedSize(200,200)

        try:
            img_main = QPixmap(str(food_fol/Food_Data[self.food]["img"]))
        except:
            img_main = QPixmap(str(img_fol/"null.png"))
        
        img_main.scaled(200,200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        img_holder.setPixmap(img_main)

        self.addWidget(img_holder)

        # Food Name
        name_label = QLabel(food_item)
        self.addWidget(name_label)

        # Buy Btn
        self.bybtn = QPushButton()
        self.addWidget(self.bybtn)

        # init_data
        self.req = Food_Data[self.food]["price"]
        self.init_funct()
    
    def init_funct(self):
        global cash

        def create_funct():
            global cash
            if cash >= self.req:
                cash -= self.req
                create_food(self.food)
            else:
                play_sound(deny)
            
            print(f"Process {self.food}'s create_funct complete")

        self.bybtn.clicked.connect(create_funct)
        self.bybtn.setText(str(self.req))

# Shop Item
class Shop_Item(QVBoxLayout):
    def __init__(self, item, custom_item = None):
        super().__init__()
        # =========
        # Values
        # =========

        self.shopitem = item

        if not custom_item:
            custom_item = "null.png"

        self.item_img = custom_item

        # =========
        # UI
        # =========


        
        img_hold = QPixmap(str(img_fol/self.item_img))
        img_hold = img_hold.scaled(120, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        img_label = QLabel()
        img_label.setPixmap(img_hold)
        img_label.setFixedSize(120,120)
        img_label.setAlignment(Qt.AlignCenter)
        
        
        self.addWidget(img_label, alignment=Qt.AlignCenter)

        item_name = QLabel(item)
        self.addWidget(item_name)

        self.desc_label = QLabel()
        self.desc_label.setWordWrap(True)
        self.addWidget(self.desc_label)

        price_label = QLabel()
        self.addWidget(price_label)

        buy_btn = QPushButton("Get")
        self.addWidget(buy_btn)

        self.p_label = price_label
        self.by_btn = buy_btn

        self.load_item_data()
  
    def item_price(self):
        get_data = load_data()

        item_price = get_data["shop-data"][self.shopitem][0]
        item_type = get_data["shop-data"][self.shopitem][1]

        self.price = item_price
        self.type = item_type
        self.details = get_data["shop-data"][self.shopitem][2]

        try:
            self.desc_label.setText(get_data["shop-data"][self.shopitem][3])
        except:
            self.desc_label.setText("Null")

    def load_item_data(self):
        self.item_price()
        self.p_label.setText(f"Price: {self.price}")
        get_data = load_data()

        def on_buy():
            global cash
            init_price = self.price
            get_data = load_data()
            if cash >= init_price:
                
                
                if self.type == "activ":
                    if self.shopitem not in get_data["player-data"]["unlocks"]:
                        cash -= init_price
                        
                        # get_data["player-data"]["unlocks"][self.shopitem] = True
                        if self.details["replace"] in get_data["player-data"]["unlocks"]:
                            get_data["player-data"]["unlocks"].pop(self.details["replace"])
                            get_data["player-data"]["rep_items"].append(self.details["replace"])
                        
                        get_data["player-data"]["unlocks"][self.shopitem] = self.details

                        push_data(get_data)
                        notification("Purchased", f"You purchased the {self.shopitem}", False)
                elif self.type == "npc":
                    if self.shopitem not in get_data["player-data"]["npc"]:
                        cash -= init_price
                        np_data = self.details
                        get_data["player-data"]["npc"][self.shopitem] = np_data
                        push_data(get_data)
                        notification("Purchased", f"You purchased the {self.shopitem}", False)

                        reload_npcs()
                elif self.type == "buff":
                    if self.shopitem not in get_data["player-data"]["buffs"]:
                        cash -= init_price
                        np_det = self.details
                        get_data["player-data"]["buffs"][self.shopitem] = np_det
                        push_data(get_data)
                        notification("Purchased", f"You purchased the {self.shopitem}", False)
                        reload_buffs()
                elif self.type == "event":
                    if self.shopitem not in get_data["player-data"]["ev_start"]:
                        cash -= init_price
                        event_det = self.details
                        get_data["player-data"]["ev_start"][self.shopitem] = event_det
                        push_data(get_data)
                        notification("Purchased", f"You purchased the {self.shopitem}", False)
                        load_eventgo()
                        



                self.load_item_data()
                save_data(play_save=False)
            else:
                play_sound(deny)
                notification("You're too poor, lmao", "Poor Ass", False)

                
        if self.shopitem not in  get_data["player-data"]["unlocks"] and self.shopitem not in get_data["player-data"]["npc"] and  self.shopitem not in get_data["player-data"]["buffs"] and self.shopitem not in get_data["player-data"]["rep_items"]:
            self.by_btn.clicked.connect(on_buy)
        else:
            self.by_btn.setText("Already Have")
            self.by_btn.setEnabled(False)

# Npc Item
class Npc(QWidget):
    def __init__(self, movefunct, funct,img = "null.png", name = "Some Random Thing", pos=(0,0)):
        
        super().__init__()
        
        self.setWindowTitle(name)
        self.movefun = movefunct
        self.prefun = funct
        self.img = img
        self.active = False
        self.posgo = None
        self.stuck_meter = 0


        grab_geometry = self.geometry()
        

        grab_geometry.setX(pos[0])
        grab_geometry.setY(pos[1])

        self.setGeometry(grab_geometry)
        

        layout = QVBoxLayout()
        img_hold = QLabel()
        img = QPixmap(str(img_fol/img))
        img = img.scaled(120,120, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        
        img_hold.setPixmap(img)
        img_hold.setFixedSize(120,120)
        img_hold.setAlignment(Qt.AlignCenter)
        
        layout.addWidget(img_hold)
        self.setFixedSize(150,150)
        self.setLayout(layout)

        self.pixmap = img
    
    def update(self):
        self = self.movefun(self)
        self.run_prefun()

        # reference: (1270, 756)

        # prevent from collaging together
        is_collide = False
        for x in np_aval:
            target_geometry = x.geometry()
            target_x, target_y = (target_geometry.x(), target_geometry.y())
            phx, phy, dist = return_moveresult(self, (target_x, target_y))

            if dist <= 150 and x.isVisible():
                new_geom = self.geometry()

                # for x
                if phx < 150:
                    original_x = new_geom.x()
                    if new_geom.x() > target_x:
                        new_geom.setX(new_geom.x()+10)
                        is_collide = True
                       
                    elif new_geom.x() < target_x:
                        new_geom.setX(new_geom.x()-10)
                        is_collide = True
                        
                    
                    if new_geom.x() < 0 or new_geom.x() > 1270:
                        new_geom.setX(original_x)
                    
                
                # for y
                if phy < 150:
                    original_y = new_geom.x()
                    if new_geom.y() > target_y:
                        new_geom.setY(new_geom.y()+10)
                        is_collide = True
                        
                    elif new_geom.y() > target_y:
                        new_geom.setY(new_geom.y()-10)
                        is_collide = True
                        
                    
                    if new_geom.y() < 0 or new_geom.y() > 756:
                        new_geom.setX(original_y)
                    
                
                self.setGeometry(new_geom)
                
                
                break
        
        if is_collide:
            self.stuck_meter += 1
            print(f"Collide Update: {int(self.stuck_meter)} | {self.windowTitle()}")
            
        else:
            self.stuck_meter -= 0.1
            if self.stuck_meter < 0:
                self.stuck_meter = 0
        
        if self.stuck_meter > 10:
            self.move(random.randint(0,size.width()), random.randint(0, size.height()))
            self.stuck_meter = 0
            print(f"Unstucked {self.windowTitle()}")

        if self not in np_aval:
            self.deleteLater()
    
    def run_prefun(self):
        if self.prefun:
            if self.prefun == multiplier:
                self.prefun(self, self.mult)

            self = self.prefun(self)

# Achev Item
class Achieve_Item(QVBoxLayout):
    def __init__(self, ach):
        super().__init__()

        self.ach = ach

        header_lay = QHBoxLayout()
        self.ach_name = QLabel()
        self.status_label = QLabel()

        header_lay.addWidget(self.ach_name)
        header_lay.addWidget(self.status_label)

        self.ach_desc = QLabel()
        self.ach_req = QLabel()

        self.addLayout(header_lay)
        self.addWidget(self.ach_desc, alignment=Qt.AlignCenter)
        self.addWidget(self.ach_req, alignment=Qt.AlignCenter)

        self.data_update()
    
    def data_update(self):
        grab_original = load_data()
        
        ach_got = grab_original["player-data"]["ach_got"]
        ach_ava = grab_original["achev"]

        home_data = ach_ava[self.ach]
        self.ach_name.setText(self.ach)
        self.ach_desc.setText(ach_ava[self.ach]["desc"])

        try:
            self.ach_req.setText(home_data["req_desc"])
        except:
            self.ach_req.setText("I don't know lol, figure it out yourself L")
        
        if self.ach in ach_got:
            self.status_label.setText("Achieved")
            self.status_label.setStyleSheet("color:green;")
        else:
            self.status_label.setText("Locked")
            self.status_label.setStyleSheet("color:red;")
        
# Crap
class Shit(QWidget):
    def __init__(self, QSpawner):
        super().__init__()
        self.setWindowTitle("Shit")
        self.to_close = random.randint(10,20)
        self.prog = 0
        
        self.setGeometry(QSpawner.geometry())
        self.setFixedSize(250,200)
        self.show()
        
        layout = QVBoxLayout()

        img_hold = QLabel()
        img_main = QPixmap(str(img_fol/"crap.jpg"))
        img_main.scaled(150,100, Qt.KeepAspectRatio)
        img_hold.setPixmap(img_main)
        layout.addWidget(img_hold)

        self.btnrem = QPushButton("Clean")
        layout.addWidget(self.btnrem)
        self.btnrem.clicked.connect(self.try_close)

        clean_prog = QProgressBar()
        clean_prog.setMaximum(self.to_close)
        self.prog_dis = clean_prog
        layout.addWidget(clean_prog)

        self.setLayout(layout)
    
    def try_close(self):
        global shits_made
        self.prog += 1
        self.prog_dis.setValue(self.prog)
        
        if self.prog >= self.to_close:
            shits_made.remove(self)
            self.deleteLater()
    
    def closeEvent(self, event):
        
        if self.prog < self.to_close:
            event.ignore()
            self.show()
        else:
            event.accept()

# Launcher
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.label = QLabel("Press Ctrl+Q anywhere in this app", self)
        self.setCentralWidget(self.label)

        feed_short = QShortcut(QKeySequence("F"), self)
        feed_short.setContext(Qt.ApplicationShortcut)
        feed_short.activated.connect(open_foodmen)

        stats_short = QShortcut(QKeySequence("S"), self)
        stats_short.setContext(Qt.ApplicationShortcut)
        stats_short.activated.connect(view_status)

        opt_short = QShortcut(QKeySequence("O"), self)
        opt_short.setContext(Qt.ApplicationShortcut)
        opt_short.activated.connect(view_set)

        shop_short = QShortcut(QKeySequence("T"), self)
        shop_short.setContext(Qt.ApplicationShortcut)
        shop_short.activated.connect(open_shop)

        ach_short = QShortcut(QKeySequence("A"), self)
        ach_short.setContext(Qt.ApplicationShortcut)
        ach_short.activated.connect(open_ach)

        es_short = QShortcut(QKeySequence("E"), self)
        es_short.setContext(Qt.ApplicationShortcut)
        es_short.activated.connect(open_escreen)

# Enemeies
class Bandit(QWidget):
    def __init__(self, speed = 2, img = "null.png"):
        super().__init__()

        # Set properties
        
        get_geom = self.geometry()
        self.setFixedSize(150, 150)
        get_geom.setX(random.choice([0,1000]))
        get_geom.setY(random.randint(-500, 500))
        self.setGeometry(get_geom)
        self.speed = speed
        self.atktick = 0
        self.hp = 5
        self.original = 5

       

        # Setting UI
        layout = QVBoxLayout()

        img_holder = QLabel()
        img_main = QPixmap(str(img_fol/img))
        img_holder.setPixmap(img_main)
        layout.addWidget(img_holder)

        atk_btn = QPushButton("Hit Here")
        layout.addWidget(atk_btn)

        hp_progbar = QProgressBar()
        hp_progbar.setMaximum(self.original)
        hp_progbar.setValue(self.hp)
        layout.addWidget(hp_progbar)

        self.atk_here = atk_btn
        self.hp_here = hp_progbar

        self.atk_here.clicked.connect(self.damage)

        self.setLayout(layout)
        
    
    def update(self):
        get_target = main_screen.geometry()
        self_pos = self.geometry()
        target_x, target_y = (get_target.x(), get_target.y())
        self_x, self_y = self_pos.x(),self_pos.y()

        dx = target_x - self_x
        dy = target_y - self_y

        dist = math.hypot(dx,dy)

        if dist != 0:
            dx /= dist
            dy /= dist
        
        if dist < 45:
            global hunger
            if self.atktick <= 0:
                hunger -= 5
                play_sound(pet_hit)
                self.atktick = 1000
        
        self.atktick -= 10

        self_pos.setX(int(self_x + (self.speed * dx)))
        self_pos.setY(int(self_y + (self.speed * dy)))

        self.setGeometry(self_pos)

        self.hp_here.setValue(int(self.hp))
        self.show()
    
    def damage(self, dmg = None):
        global enem_list, kill_crnt
        if not dmg:
            dmg = atk_power
        self.hp -= dmg
        if self.hp <= 0:
            enem_list.remove(self)
            kill_crnt += 1
            self.deleteLater()

class King(QWidget):
    def __init__(self, speed = 5, img = "null.png"):
        super().__init__()
        self.speed = speed
        self.atk_tick = 0
        self.prev = ""
        self.hp = 3000
        self.original = 3000
        self.moves = ["Summon", "Rain"]
        self.proj_load = []

        self.gox, self.goy = None, None

        layout = QVBoxLayout()

        img_holder = QLabel()
        img_main = QPixmap(str(img_fol/img))
        img_holder.setPixmap(img_main)
        layout.addWidget(img_holder)

        atk_btn = QPushButton("Hit Here")
        layout.addWidget(atk_btn)

        hp_progbar = QProgressBar()
        hp_progbar.setMaximum(self.original)
        hp_progbar.setValue(self.hp)
        layout.addWidget(hp_progbar)

        self.atk_here = atk_btn
        self.hp_here = hp_progbar

        self.atk_here.clicked.connect(lambda: self.damage())

        self.atk_here.clicked.connect(self.damage)

        self.setLayout(layout)
        self.setFixedSize(250, 250)
    
    def damage(self, dmg = None):
        global enem_list, confirm_achlist
        if not dmg or not type(dmg) == int:
            dmg = atk_power
        
        self.hp -= dmg/2
        self.hp_here.setValue(int(self.hp))

        
        if self.hp <= 0:
            confirm_achlist.append("King")
            self.deleteLater()
            enem_list.remove(self)
            for x in self.proj_load:
                x.deleteLater()
    
    def update(self):
        global enem_list
        # Movement
        if not self.gox or not self.goy:
            self.gox, self.goy = (random.randint(0, 1470), random.randint(0, 956))
        
        self_geometry = self.geometry()

        dx, dy, dist = return_moveresult(self, (self.gox, self.goy))

        self_geometry.setX(int(self_geometry.x() + (self.speed * dx)))
        self_geometry.setY(int(self_geometry.y() + (self.speed * dy)))

        self.setGeometry(self_geometry)

        if dist <= 150:
            self.gox, self.goy = (random.randint(0, 1470), random.randint(0, 956))
        
        # Attacks
        self.atk_tick -= 10
        
        
        if self.atk_tick <= 0:
            move_choose = random.choice(self.moves)
            self.atk_tick = 5000

            while move_choose == self.prev:
                move_choose = random.choice(self.moves)
            
            self.prev = move_choose
            print(move_choose)

            if move_choose == "Summon":
                if not len(enem_list) > 9:
                    for x in range(random.randint(5,7)):
                        play_sound(shoot)
                        NewBandit = Bandit()
                        enem_list.append(NewBandit)
                        if len(enem_list) > 9:
                            break
                else:
                    print("Choose the other")
                    move_choose = "Rain"

            if move_choose == "Rain":
                for x in range(random.randint(10,20)):
                    def create():
                        pos_make = (random.randint(0,1440), 1440)
                        local_proj = Falling_Type(start=pos_make)
                        self.proj_load.append(local_proj)
                        local_proj.show()
                    
                    QTimer.singleShot(100*x, create)
            
        for x in self.proj_load:
            try:
                x.update()
            except Exception as e:
                self.proj_load.remove(x)
                print(f"Couldn't Find {x} \n - {e}")

        self.show()

# Hit Projectile
class Collide_Type(QWidget):
    def __init__(self, image = "null.png", size = (75,75), target = main_screen):
        super().__init__()

        Layout = QVBoxLayout()
        self.image_holder = QPixmap(str(img_fol/image))
        self.image_holder.scaled(size[0], size[1], Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.target = target

        self.image_main = QLabel()
        self.image_main.setPixmap(self.image_holder)
        self.image_main.setFixedSize(size[0], size[1])
        self.image_main.setAlignment(Qt.AlignCenter)

        self.setFixedSize(size[0]+5, size[1]+5)

        Layout.addWidget(self.image_main)
        self.setLayout(Layout)
    
    def check_col(self):
        global hunger, happiness
        dx, dy, dist = return_moveresult(self, (self.target.geometry().x(), self.target.geometry().y()))

        if dist <= 100:
            hunger -= 25
            happiness -= 5
            self.deleteLater()

class Falling_Type(Collide_Type):
    def __init__(self, image="null.png", size=(75, 75), target=main_screen, start = (1470, 956)):
        super().__init__(image, size, target)
        # Setting position
        self.move(start[0], start[1])
    
    def update(self):
        
        self.show()
        self_geometry = self.geometry()
        self_geometry.setY(self_geometry.y() - 10)
        self.setGeometry(self_geometry)
        self.check_col()

       
        if self_geometry.y() <=45:
            self.deleteLater()
# This mf is the one that lags the game whenver a shitload of these are summoned. I don't feel like fixing it.
# Maybe if the bug is too bad, then I'll "try" to fix it


# Event Handlers
class Event_Atk():
    def __init__(self, enem_list, name = "Null"):
        self.enemies_aval = []
        self.event_list = enem_list
        self.name = name
    
    def generate_enems(self):
        global enem_list
        # Note, all of them must be enemy classes already
        for x in self.event_list:
            enem_list.append(x)
            self.enemies_aval.append(x)
    
    def self_update(self):
        for x in self.enemies_aval:
            if x.hp <= 0:
                self.enemies_aval.remove(x)
                print(f"Remaining: {len(self.enemies_aval)}")

        if not len(self.enemies_aval) > 0:
            notification(f"Event Finished", f"f{self.name}",True, win)
            del self
        else:
            print(f"Current List: {self.enemies_aval}")
            QTimer.singleShot(500, self.self_update)
    
    def begin(self):
        print(f"Event: {self.name} has started")
        notification(f"The {self.name} has begun!", "yooo", False)
        self.generate_enems()
        self.self_update()

class Event_Buff():
    '''
        {
            "tick":10000,
            "buffs":{
                "cash_gain":10
            }
        }
    '''

    def __init__(self, data, name = "Null"):
        
        self.name = name
        self.buffs = data["buffs"]
        self.tick = data["tick"]

    def init_buffs(self):
        global cash_gain, mult
        for x in self.buffs:
            if x in globals():
                globals()[x] += self.buffs[x]
            else:
                print(f"Couldn't find {x} in globals")
        
        print(f"Updated: \n Cash Gain: {cash_gain} \n Mult: {mult}")
        self.update_tick()
    
    def update_tick(self):
        global cash_gain, mult
        self.tick -= 10
        if self.tick <= 0:
            for x in self.buffs:
                if x in globals():
                    globals()[x] -= self.buffs[x]
                else:
                    print(f"Couldn't find {x} in globals")
            print("Ended.")
        else:
            
            QTimer.singleShot(10, lambda:self.update_tick())

    def begin(self):
        self.init_buffs()
        play_sound(buff)

class Event_Starter(QVBoxLayout):
    def __init__(self, event):
        super().__init__()
        self.ev_main = event
        grab_data = load_data()
        events_reach = grab_data["player-data"]["ev_start"]
        self.n_event = events_reach[event]["name"]

        if self.ev_main in events_reach:
            self.command = events_reach[self.ev_main]["command"]

            try:
                self.tick_start = events_reach[self.n_event]["tick"]
            except:
                self.tick_start = 1000
        else:
            print(f"Couldn't find {event}/{self.n_event} in {events_reach}")
        
        # UI

        self.event_label = QLabel(self.n_event)
        self.push_btn = QPushButton("Start")

        self.addWidget(self.event_label)
        self.addWidget(self.push_btn)

        self.init_funct()
    
    def init_funct(self):
        def event_push():
            global ce_dict
            if not self.n_event in ce_dict:
                eval(self.command)
                print(f"{self.n_event} has been initialized")
            else:
                self.push_btn.setEnabled(False)
            

            if self.n_event in ce_dict:
                self.push_btn.setEnabled(False)
            else:
                print(f"{self.n_event} not in {ce_dict}")
                self.push_btn.setEnabled(True)

        self.push_btn.clicked.connect(event_push)

# ========= 
# variables 
# ========= 

# Fixed Data
Food_Data = {
    "Burger":{
        "happiness":0,
        "hunger":35,
        "override":False,
        "price":35
    },
    "Special Spaghetti":{
        "happiness":45,
        "hunger":65,
        "override":True,
        "price":10000,
        "img":"spag.png"
    }
}

# Others
foods = []
target = ""
np_aval = []
rs_count = 10000

# Craps
crap_cntr = 0
shits_made = []

# Raid System
enem_list = []
on_raid = False
pre_raid = False
can_raid = True
raid_cntr = raid_cntr = random.randint(300000, 900000)
is_retr = False
prev_pos = None
kill_target = 0
kill_crnt = 0

# Movement
can_go = True
on_reach = None

# Screen Data
x_go, y_go = (random.randint(0, 1000), random.randint(0, 500))
speed = 5
can_move = True

# Timer set
timer = 0

# virtual data
recent_mood = ""
recent_hung = "good"

stat_tick = 50
happiness = 100
hunger = 100

max_hunger = 100
max_hap = 100

crnt_tick = 0

# dial
can_dial = True
rd_tick = 10000
rd_crnt = 5000

# player data
cash = 0
cash_gain = 1
mult = 1

atk_power = 10

sounds = []
stations = {}
confirm_achlist = []

bgr_player = None


# =========
# functions
# =========

# Sounds
def play_sound(sound):
    global sounds
    new_sound = QMediaPlayer()
    new_sound.setMedia(sound)
    new_sound.setVolume(load_data()["settings"]["sfx-value"])
    sounds.append(new_sound)
    if len(sounds) > 100:
        for x in range(50):
            sounds.pop(x)

    new_sound.play()
    if new_sound.stateChanged == QMediaPlayer.StoppedState:
        new_sound.deleteLater()

def bgr_onlaunch():
    global bgr_player, bgr_pl  
    bgr_player = QMediaPlayer()
    bgr_pl = QMediaPlaylist()
    list_songs = os.listdir(bgr_fol)
    for song in list_songs:
        bgr_pl.addMedia(QMediaContent(QUrl.fromLocalFile(str(bgr_fol/song))))
        print(bgr_fol/song)
    bgr_pl.setPlaybackMode(QMediaPlaylist.Loop)
    bgr_player.setPlaylist(bgr_pl)
    bgr_player.playlist().setCurrentIndex(random.randint(0, len(list_songs)))
    bgr_player.setVolume(load_data()["settings"]["background-value"])
    bgr_player.play()
    update_sl()
    bgr_player.playlist().currentIndexChanged.connect(lambda _: update_sl())

def change_bgr(val):
    global bgr_player
    bgr_player.setVolume(val)
    get_data = load_data()
    get_data["settings"]["background-value"] = val

    push_data(get_data)

def change_bgmedia(media):
    global bgr_player
    bgr_player.setMedia(media)
    bgr_pl.setPlaybackMode(QMediaPlaylist.Loop)
    bgr_player.play()

def change_sfxvol(val):
    for x in sounds:
        x.setVolume(val)

    get_data = load_data()
    get_data["settings"]["sfx-value"] = val

    push_data(get_data)
    
def random_sound():
    grab_sound = QMediaContent(QUrl.fromLocalFile(str(random_snd/random.choice(rs_list))))
    play_sound(grab_sound)

def next_song():
    global bgr_player
    try:
        bgr_player.playlist().next()
    except:
        pass

# Movements
def move_location():
    get_crntpos = main_screen.geometry()
    crnt_x, crnt_y = get_crntpos.x(), get_crntpos.y()
    dist_x = x_go - crnt_x
    dist_y = y_go - crnt_y
    dist = math.hypot(dist_x, dist_y)
    if dist != 0:
        dist_x /= dist
        dist_y /= dist
    get_crntpos.setX(crnt_x + int(dist_x * speed))
    get_crntpos.setY(crnt_y + int(dist_y * speed))
    main_screen.setGeometry(get_crntpos)
    return dist < 100

# Update
def update():
    global timer,x_go, y_go, recent_mood, recent_hung,rd_crnt, target, foods, speed
    global happiness, crnt_tick, hunger, crap_cntr, cash, raid_cntr, is_retr, prev_pos, can_go, on_reach, rs_count
    global confirm_achlist


    main_screen.show()
    hap_bar.setMaximum(max_hap)
    hun_bar.setMaximum(max_hunger)
    

    # Path
    '''
        Enemy Spotted
        Not Spotted 
            --> Normal Movement (random position)
            --> Can't go Normal
                --> Go to target position
    '''
    
    if len(foods) <= 0:
        if not len(enem_list) != 0 and can_go:
            if timer > 0:
                timer -= 1
                if timer <= 0:
                    x_go, y_go = (random.randint(0, 1470), random.randint(0, 956))
            elif timer <= 0 and can_move:
                if move_location():
                    timer = 300
        elif not len(enem_list) > 0 and not can_go:
            if move_location():
                on_reach()
                can_go = True      
        else:
            
            # For some fuckass reason, bro starts having a seizure. I'm too lazy to do the math
            # If u have any suggestions, be my guest.
            if is_retr:
                if move_location():
                    is_retr = False
               

            local_enlist = sorted(
                enem_list,
                key= lambda x: 
                math.hypot(
                    (x.geometry().x() - main_screen.geometry().x()),
                    (x.geometry().y() - main_screen.geometry().y())
                )
            )
            
            mainnew_geom = main_screen.geometry()
            crnt_x, crnt_y = mainnew_geom.x(), mainnew_geom.y()

            nearest_enem = local_enlist[0]
            nearest_geom = nearest_enem.geometry()
            dx = nearest_geom.x() - main_screen.geometry().x()
            dy = nearest_geom.y() - main_screen.geometry().y()


            new_x = int(crnt_x - (speed * dx))
            new_y = int(crnt_y - (speed * dy))

            new_x = max(0, min(new_x, size.width() - main_screen.width()))
            new_y = max(0, min(new_y, size.height() - main_screen.height()))
            max_x = size.width() - main_screen.width()
            max_y = size.height() - main_screen.height()

            
            x_go, y_go = new_x, new_y
            if (x_go, y_go) != prev_pos:
                prev_pos = (x_go, y_go)
                move_location()
            else:
                x_go, y_go = (random.randint(0, 1470), random.randint(0, 956))
                is_retr = True


            # reference: (1270, 756)
    else:
        if target not in foods:
            target = foods[0]
        target_geom = target.geometry()
        x_go, y_go = target_geom.x(), target_geom.y()
        if move_location():
            happiness += target.hap
            hunger += target.hunger

            if happiness > max_hap and not target.override:
                happiness = max_hap
            
            if hunger > max_hunger and not target.override:
                hunger = max_hunger
            
            oh_cap = max_hunger * 2
            # Set a cap
            if hunger > oh_cap:
                hunger = oh_cap
                confirm_achlist.append("overcap")


            target.deleteLater()
            foods.remove(target)
    crnt_tick -= 1

    if crnt_tick <= 0:
        happiness -= 0.5
        hunger -= 0.3
        if happiness < 0:
            happiness = 0
        if hunger <= 0:
            hunger = 0
            play_sound(pet_die)
            notification("You're so bad at taking care of pets, your virtual pet died", "R.I.P. WindowPet")
            update_achievements()
            try:
                cash /= 2
                cash = int(cash)
            except:
                pass
            QTimer.singleShot(500,terminate)
        crnt_tick = stat_tick

    rs_count -= 10

    if rs_count <= 0:
        random_sound()
        rs_count = random.randint(19000, 20000)

    if happiness > 50:
        if recent_mood != "smile":
            dialogue("Happy dialogue")
            recent_mood = "smile"
        face_label.setText(smile)
        speed = 5
    elif happiness < 50 and happiness > 10:
        if recent_mood != "medium":
            dialogue("...")
            recent_mood = "medium"
        face_label.setText(medium)
        speed = 3.5
    elif happiness < 10:
        if recent_mood != "sad":
            dialogue("Please pet me :(")
            recent_mood = "sad"
            notification("Your pet gettin sad, entertain it.", 
                "Pet demands your attention.",
                image=QIcon(str(log_fol/"sad.png"))
            )
        
        # try to find entertainment
        for x in stations:
            if stations[x] == "happy":
                x_geom = x.geometry()

                x_go, y_go = x_geom.x(),x_geom.y()
                can_go = False
                on_reach = on_happy
                break

        face_label.setText(sad)
        speed = 2.5
    

    hap_bar.setValue(int(happiness))
    hap_prec.setText(f"{happiness}%")
    

    
    if hunger > 150:
        if recent_hung != "good":
            recent_hung = "good"
            dialogue("I thinks that's enough food!",10)
        speed = 5
    elif hunger < 150 and hunger > 100:
        if recent_hung != "ok":
            recent_hung = "ok"
            dialogue("I'm getting a bit hungry....",10)
    elif hunger < 100 and hunger > 50:
        if recent_hung != "medio":
            recent_hung = "medio"
            dialogue("Ok... I'm getting a bit too hungry",10)
    elif hunger < 50:
        if recent_hung != "low":
            recent_hung = "low"
            dialogue("I'm hungry!!!!",10)
            notification("Your pet is getting hungry. Feed it nigga", "Pet demands your attention.")
        
    hun_bar.setValue(int(hunger))
    hun_perc.setText(f"{int(hunger)}%")

    if hunger > max_hunger:
        hun_perc.setStyleSheet("color:gold;")
    else:
        hun_perc.setStyleSheet("")

    rd_crnt -= 5
    if rd_crnt <= 0:
        dialogue(random.choice(dials), 10)
        rd_crnt = rd_tick

    crap_cntr -= 10
    
    if crap_cntr <= 0:
        crap()
        
        crap_cntr = 50000
    # System
    try:
        cash_label.setText(f"Cash: {cash}")
    except:
        cash_label.setText(f"Cash: Null")

    load_activs()
    update_npcs()
    update_achievements()

    for x in foods:
        x.show()
    
    # Raid functions
    update_enemies()
    if not raid_cntr <= 0:
        raid_cntr -= 10

    # Init
    if raid_cntr <= 0:
        if not on_raid:
            start_raid()
    
    # Warning
    if raid_cntr == 60000:
        notification("Prepare. A raid is coming. Keep your pets hunger as high as possible. Protect it.", 
            "Raid Warning", 
            True,
            raid_soon
        )

    # Special
    update_events()
    



    # Begin Another
    QTimer.singleShot(10, update)

def update_sl():
    if bgr_player.playlist():
        current_index = bgr_player.playlist().currentIndex()
        media = bgr_player.playlist().media(current_index)
        url = media.canonicalUrl()
        song_name = QFileInfo(url.path()).fileName()

        notification(
            song_name,
            "Now Playing....",
            False
        )
    else:
        song_name = "Can't fetch song"

    audio_label.setText(f"Now playing: {song_name}")



# Activ Variable
activs_ticks = {}
'''
    Example:
        "activ":{"tick":0, "start-tick":100}
'''

food_feed = "Null"

def load_activs():
    global activs_ticks
    fetch_data = load_data()
    activs = fetch_data["player-data"]["unlocks"]

    for x in activs:
        x_data = activs[x]

        if x not in activs_ticks:
            activs_ticks[x] = x_data["tick"]
        
        activs_ticks[x] -= 10

        if activs_ticks[x] <= 0:
            try:
                eval(x_data["function"])
                activs_ticks[x] = x_data["tick"]
            except Exception as e:
                print(f"Removing {x} | Error: {e}")
                activs_ticks.pop(x)
        
        # Try to remove the old, if it exists
        try:
            if x_data["replace"] in activs:
                print(f"Removing {x_data["replace"]} as replaced by {x}")
                fetch_data["player-data"]["unlocks"].pop(x_data["replace"])
                fetch_data["player-data"]["rep_items"].append(x_data["replace"])
                push_data(fetch_data)
                print(f"Removed {x_data["replace"]} success")
                break
        except Exception as e:
            print(f"Error at removing the replacement | {e}")
            pass

def reload_npcs():
    global np_aval
    fetch_data = load_data()
    npcs = fetch_data["player-data"]["npc"]

    np_aval.clear()

    for x in npcs:
        npc_data = npcs[x]
        
        # Getting move
        function_move = None
        move_str = npc_data["movefunct"]

        function_move = eval(move_str)
        
        # Getting funct
        purp_function = None
        purp_str = npc_data["funct"]

        purp_function = eval(purp_str)

        # Getting Position Start (Optional)
        if "pos" in npc_data:
            position = (npc_data["pos"][0], npc_data["pos"][1])
        else:
            position = (0,0)
        
        if "img" in npc_data:
            img = npc_data["img"]
        else:
            img = "null.png"
        
        np_class = Npc(function_move, purp_function,name=x, pos=position, img=img)

        np_class.type = npc_data["type"]

        if "purpose" in npc_data:
            np_class.purpose = npc_data["purpose"]
       
        if purp_function == multiplier:
            if not hasattr(np_class, "mult"):
                np_class.mult = npc_data["mult"]

        if np_class not in np_aval:
            np_aval.append(np_class)
        
def update_npcs():
    global np_aval
    try:
        settings_data = load_data()["settings"]
    except:
        # Repeat until fetched
        while not settings_data:
            settings_data = load_data()["settings"]

    for x in np_aval:
        if settings_data["hide_minors"]:
            if x.type == "minor":
                x.hide()
                try:
                    
                    x.run_prefun()
                except:
                    
                    pass
            else:
                x.show()
                x.update()
        else:
            x.show()
            x.update()
        
def update_enemies():
    global enem_list, spec_player, bgr_player, pre_raid, on_raid, raid_cntr
    settings = load_data()["settings"]
    spec_player = QMediaPlayer()
    spec_player.setVolume(settings["background-value"])
    spec_player.setMedia(QMediaContent(QUrl(str(spec_fol/"raid.mp3"))))

    if pre_raid != on_raid:
        if not on_raid:
            
            raid_cntr = random.randint(300000, 900000)

    pre_raid = on_raid
    if on_raid:
        if kill_crnt == kill_target:
            on_raid = False
            raid_cntr = random.randint(300000, 900000)
            bgr_onlaunch()
            notification("They're gone for now", "You survived the raid")
            play_sound(win)

        
       

    
    for x in enem_list:
        x.update()

def start_raid():
    global on_raid, kill_target, kill_crnt
    notification("Bandits are spotted \n Protect your pet!", "Alert! Emergency!", True)

    def spawn_in():
        global enem_list
        enem_list.append(Bandit())
    
    random_total = random.randint(8,14)
    kill_target = random_total
    kill_crnt = 0
    on_raid = True
    change_bgmedia(QMediaContent(QUrl.fromLocalFile(str(spec_fol/"raid.mp3"))))
    for x in range(random_total):
        QTimer.singleShot(500*x, spawn_in)
    
def reload_buffs():
    global max_hunger, max_hap, atk_power, cash_gain

    # From default
    max_hunger = 100
    max_hap = 100
    atk_power = 1

    buffs = load_data()["player-data"]["buffs"]
    

    for x in buffs:
        x_data = buffs[x]
        var_name = x_data["do"]
        add_val = x_data["add"]
        if var_name in globals():
            globals()[var_name] += add_val
        else:
            print(f"Error when loading {x} with global variable {var_name}")

    print(f"Updated Stats: \n New Hunger: {max_hunger} \n New Happiness: {max_hap} \n New Attack: {atk_power} \n New Cash Gain : {cash_gain * mult} ({cash_gain}*{mult})")

    hap_bar.setMaximum(max_hap)
    hun_bar.setMaximum(max_hunger)

def update_achievements():
    get_data = load_data()

    achieve_grab = get_data["achev"]

    for a in achieve_grab:
        if eval(achieve_grab[a]["condition"]):
            
            if a not in get_data["player-data"]["ach_got"]:
                get_data["player-data"]["ach_got"].append(a)
                print(f"{eval(achieve_grab[a]["condition"])} - {a}")
                notification(
                    
                    achieve_grab[a]["desc"],
                    f"Acheivement Unlocked: {a}",
                    True,
                    win,
                    QIcon(str(log_fol/"acheivement.jpg"))
                )
                print("Acheivement new. Updating achievement display")
                regen_adis()
                push_data(get_data)
    
def regen_adis():
    global ad_scroll_lay

    # This fucking piece of shit of a progra decided it's a good idea to do anything but remove the old items
    # Go fuck yourself


    while ad_scroll_lay.count() > 0:

        item = ad_scroll_lay.takeAt(0)
        
        try:
            wid = item.widget()
            wid.deleteLater()
        except:
            lay = item.layout()
            lay.deleteLater()
        
        print(f"For Checking ad_scroll_lay: {ad_scroll_lay.count()}")

    
    # Reloading Items
    ori_data = load_data()
    achi_list = list(ori_data["achev"].keys())

    for x in achi_list:
        ach_local = Achieve_Item(x)
        ach_local.data_update()
        ad_scroll_lay.addLayout(ach_local)

'''
    As independent update to prevent lag
'''  

# Actions
def on_pet():
    global happiness
    play_sound(pat)
    dialogue("Yippie Pats!!!", 10)
    happiness += 3
    if happiness > max_hap:
        happiness = max_hap

def get_money():
    global cash, mult
    play_sound(money)

    cash_to_get = cash_gain * mult
    if happiness < 50 and happiness > 10:
        cash_to_get /= 2
    elif happiness < 10:
        cash_to_get /= 3
    elif happiness > max_hap:
        cash_to_get *= 3

    cash += (cash_to_get)
    cash = int(cash)

def create_food(item_name):
    # For some reason if I remove the new_item, it doesn't work.
    new_item = Food_Wid(item_name)

def crap():
    global shits_made
    shits_made.append(Shit(main_screen))
    play_sound(stinky)

    def check_len():
        if len(shits_made) >= 2:
            notification(
                "Clean up the place, it's filled with shit",
                "Stop being lazy")
    
    QTimer.singleShot(3000, check_len)

# UI Handlers
def view_status():
    statusScreen.show()

def open_foodmen():
    feedScreen.show()

def view_set():
    set_screen.show()
    bm_set.setValue(bgr_player.volume())

def open_again():
    main_screen.show()

def open_shop():
    if not shopScreen.isVisible():
        shopScreen.show()
        play_sound(shop)

def open_ach():
    if not ad_screen.isVisible():
        ad_screen.show()

def open_escreen():
    Even_Screen.show()

# Dialogue
def dialogue(text, tick=100):
    global can_dial

    wait_cancel = 0
    if not can_dial:
        while not can_dial:
            app.processEvents()
            wait_cancel += 1
            if wait_cancel >= 200:
                # Cancel the dialogue
                return
    can_dial = False
    def return_can():
        global can_dial
        speech_label.setText(text)
        can_dial = True
    def add_letter(x):
        speech_label.setText(
            speech_label.text() + x
        )
    speech_label.clear()
    for index, let in enumerate(text):
        QTimer.singleShot(tick*index, lambda ltr = let: add_letter(ltr))
    QTimer.singleShot(tick*len(text), return_can)

# System
def update_name(name):
    main_screen.setWindowTitle(name)

def terminate():
    app.closeAllWindows()
    save_data()
    QTimer.singleShot(5000,sys.exit())
      
def notification(msg, title, dosound = True, sfx = None, image = QSystemTrayIcon.Information):
    global tray
    if not sfx:
        sfx = notif
    tray.showMessage(
        title,
        msg,
        image,
        10000
    )
    if dosound:
        play_sound(sfx)

def hide_check(bool):
    grab_data = load_data()
    if bool:
        grab_data["settings"]["hide_minors"] = True
    else:
        grab_data["settings"]["hide_minors"] = False
    
    push_data(grab_data)

# Events
ce_dict = {}
'''
    Custom Event Example:
        {"event_item":{"tick":60000, "event":event_or_smth_idk}}
'''

def create_event(name, type, data, tick = 60000):
    global ce_dict
    if type.lower() == "attack":
        event_new = Event_Atk(data, name)
    elif type.lower() == "buff":
        event_new = Event_Buff(data, name)
    
    print(f"pushing event: {name, type, data, tick}")
    ce_dict[name] = {"tick":tick, "event":event_new.begin}
    print(f"New:{ce_dict}")

def update_events():
    for x in ce_dict:
        ce_dict[x]["tick"] -= 10
        if ce_dict[x]["tick"] <= 0:
            ce_dict[x]["event"]()
            print(f"Initializing {x} start.")
            ce_dict.pop(x)
            notification(
                f"{x} has started!",
                "Event started"
            )
            break
        
# Data Manage
def load_data():
    with open("data.json", "r") as file:
        try:
            return json.load(file)
        except:
            return None

def push_data(data):
    with open("data.json", "w") as file:
        json.dump(data, file, indent= 4)

def save_data(play_save = True):
    get_data = load_data()
    while not get_data:
        get_data = load_data()
    
    # This code is ass, it just saves cash and settings.
    # Will improve it if I feel like it.


    # Player Data
    get_data["player-data"]["cash"] = cash


    # Settings Daa
    get_data["settings"]["background-value"] = bgr_player.volume()

    get_data["settings"]["sfx-value"] = sfx_set.value()

    push_data(get_data)

    if play_save:
        print("playing save")
        play_sound(save)
    else:
        print(play_save)
    
def restate_data():
    global bgr_player, cash, max_hunger, max_hap, hunger, happiness
    get_data = load_data()

    settings = get_data["settings"]
    game_data = get_data["player-data"]

    # state settings
    bgr_player.setVolume(settings["background-value"])
    sfx_set.setValue(settings["sfx-value"])
    hide_min.setCheckState(settings["hide_minors"])
    

    # game data
    cash = game_data["cash"]

    hunger = max_hunger
    happiness = max_hap

# Shop Manage
def load_items():
    get_data = load_data()
    shop_data = get_data["shop-data"]
    shop_items = list(get_data["shop-data"].keys())
    items_per_row = 5 

    for i in range(0, len(shop_items), items_per_row):
        row_layout = QHBoxLayout()
        for item_name in shop_items[i:i+items_per_row]:
            item_data = shop_data[item_name]

            if len(item_data) >= 5:
                item_img = item_data[4]
            else:
                item_img = "null.png"

            shop_item = Shop_Item(item_name, item_img)
            row_layout.addLayout(shop_item)
        shop_items_layout.addLayout(row_layout)

# Events Manage
def load_eventgo():
    fetch_data = load_data()
    events = fetch_data["player-data"]["ev_start"]

    for x in events:
        local = Event_Starter(x)
        es_scrollay.addLayout(local)

# Food Manage
def load_foods():
    for x in Food_Data:
        local_item = FS_Layout(x)
        food_layout.addLayout(local_item)

# Pet functions
def multiplier(class_use, by = 2):
    global mult
    if not class_use.active:
        class_use.active = True
        mult += by
    
    return class_use

def purpose(class_use):
    global stations
    if not class_use.active:
        if not hasattr(class_use, "purpose"):
            purp = "Null"
        else:
            purp = class_use.purpose

        class_use.active = True
        stations[class_use] = purp

        print(stations)
    
# Pet Movement
def return_moveresult(class_move, pos=()):
    get_geom = class_move.geometry()
    class_x, class_y = get_geom.x(), get_geom.y()
    targt_x, targt_y = pos

    dx = targt_x - class_x
    dy = targt_y - class_y

    dist = math.hypot(dx, dy)

    if dist != 0:
        dx /= dist
        dy /= dist
    
    return dx, dy, dist

def go_random(class_use):
    class_geom = class_use.geometry()
    class_target = class_use.posgo
    if not class_target:
        class_target = (random.randint(0, 1470), random.randint(0, 956))
    class_x, class_y = class_geom.x(), class_geom.y()

    dx = class_target[0] - class_x
    dy = class_target[1] - class_y

    dist = math.hypot(dx, dy)

    if dist != 0:
        dx /= dist
        dy /= dist
    
    if dist <= 200:
        class_target = (random.randint(0, 1470), random.randint(0, 956))
    
    class_geom.setX(int(class_x + int(dx * 2)))
    class_geom.setY(int(class_y + int(dy * 2)))


    class_use.setGeometry(class_geom)
    class_use.posgo = class_target

    return class_use

def manage_craps(class_use):
    global shits_made
    if not hasattr(class_use, "clean_targ"):
        class_use.clean_targ = None
    
    if not hasattr(class_use, "clean_tick"):
        class_use.clean_tick = 0
    
    if class_use.clean_tick > 0:
        class_use.clean_tick -= 10
    
    if len(shits_made) > 0:
        if class_use.clean_targ not in shits_made:
            class_use.clean_targ = shits_made[0]
        
        self_geometry = class_use.geometry()
        self_x, self_y = self_geometry.x(), self_geometry.y()

        dx, dy, dist = return_moveresult(
            class_use, 
            (class_use.clean_targ.geometry().x(), class_use.clean_targ.geometry().y())
        )

        self_geometry.setX(int(self_x + (3 * dx)))
        self_geometry.setY(int(self_y + (3 * dy)))

        if dist <= 150 and class_use.clean_tick <= 0:
            class_use.clean_targ.try_close()
            class_use.clean_tick = 500

        
        class_use.setGeometry(self_geometry)
        return class_use
    else:
        return go_random(class_use)

def stationary(class_use):
    if not hasattr(class_use, "station"):
        class_use.station = class_use.geometry()
    
    class_use.setGeometry(class_use.station)
    return class_use

# For Melee
def on_guard(class_use):
    global enem_list



    # Adding attributes
    if not hasattr(class_use, "target"):
        class_use.target = None
    
    if not hasattr(class_use, "atk_tick"):
        class_use.atk_tick = 0

    if not hasattr(class_use, "prev_type"):
        class_use.prev_type = "def"
    
    if not hasattr(class_use, "crnt_type"):
        class_use.crnt_type = ""
    
    # Running ticks
    if class_use.atk_tick > 0:
        class_use.atk_tick -= 10
    
    try:
        class_use.cnrt_type = load_data()["settings"]["def_ty"]
    except:
        print(f"{class_use} couldn't grab type, going ")
        class_use.cnrt_type = "atk"
    
    
    # Running Movement
    if len(enem_list) > 0:
        self_position = class_use.geometry()

        if class_use.crnt_type != class_use.prev_type:
            class_use.prev_type = class_use.crnt_type
            print(f"switching type: {class_use.crnt_type}")
            if class_use.crnt_type == "def":
                # sort by nearest to pet
                order_enemy = sorted(enem_list, 
                    key= lambda x: return_moveresult(x, (main_screen.geometry().x(), main_screen.geometry().y()))[2]
                )
                
            elif class_use.crnt_type == "atk":
                order_enemy = sorted(enem_list, 
                    key= lambda x: x.hp
                )
            else:
                order_enemy = enem_list
            
            class_use.target = order_enemy[0]
        else:
            if class_use.target not in enem_list:
                if class_use.crnt_type == "def":
                    # sort by nearest to pet
                    order_enemy = sorted(enem_list, 
                        key= lambda x: return_moveresult(x, (main_screen.geometry().x(), main_screen.geometry().y()))[2]
                    )
                
                elif class_use.crnt_type == "atk":
                    order_enemy = sorted(enem_list, 
                    key= lambda x: x.hp
                    )
                else:
                    order_enemy = enem_list
            
                class_use.target = order_enemy[0]
        if class_use.crnt_type == "def":
                    # sort by nearest to pet
            order_enemy = sorted(enem_list, 
                key= lambda x: return_moveresult(x, (main_screen.geometry().x(), main_screen.geometry().y()))[2]
            )
            class_use.target = order_enemy[0]
        
        class_use.prev_type = class_use.crnt_type
        enemy_position = class_use.target.geometry()
        enem_x, enem_y = enemy_position.x(), enemy_position.y()

        getdx, getdy, dist = return_moveresult(class_use, (enem_x, enem_y))

        if dist > 150:
            self_position.setX(int(self_position.x() + (getdx * 4)))
            self_position.setY(int(self_position.y() + (getdy * 4)))
            class_use.setGeometry(self_position)
        else:
            self_position.setX(int(self_position.x() - (getdx * 2)))
            self_position.setY(int(self_position.y() - (getdy * 2)))
            class_use.setGeometry(self_position)


        if dist <= 200 and class_use.atk_tick <= 0:
            play_sound(npc_hit)
            class_use.target.damage(2)
            class_use.atk_tick = 500


        

        return class_use
    else:
        return go_random(class_use)

# For Ranged
def on_range(class_use):
    global enem_list
    if not hasattr(class_use, "target"):
        class_use.target = None
    
    if not hasattr(class_use, "atk_tick"):
        class_use.atk_tick = 0
    
    if class_use.atk_tick > 0:
        class_use.atk_tick -= 10

    if not hasattr(class_use, "prev_type"):
        class_use.prev_type = "def"
    
    if not hasattr(class_use, "crnt_type"):
        class_use.crnt_type = ""
    
    try:
        class_use.cnrt_type = load_data()["settings"]["def_ty"]
    except:
        class_use.cnrt_type = "atk"
  
    if len(enem_list) > 0:
        if class_use.crnt_type != class_use.prev_type:
            class_use.crnt_type = class_use.prev_type

            if class_use.crnt_type == "def":
                # sort by nearest to pet
                order_enemy = sorted(enem_list, 
                    key= lambda x: return_moveresult(x, (main_screen.geometry().x(), main_screen.geometry().y()))[2]
                )
                
            elif class_use.crnt_type == "atk":
                order_enemy = sorted(enem_list, 
                    key= lambda x: x.hp
                )
            else:
                order_enemy = enem_list
            
            class_use.target = order_enemy[0]
        else:
            if class_use.target not in enem_list:
                if class_use.crnt_type == "def":
                    # sort by nearest to pet
                    order_enemy = sorted(enem_list, 
                        key= lambda x: return_moveresult(x, (main_screen.geometry().x(), main_screen.geometry().y()))[2]
                    )
                
                elif class_use.crnt_type == "atk":
                    order_enemy = sorted(enem_list, 
                    key= lambda x: x.hp
                    )
                else:
                    order_enemy = enem_list
            
                class_use.target = order_enemy[0]

        if class_use.crnt_type == "def":
                    # sort by nearest to pet
            order_enemy = sorted(enem_list, 
                key= lambda x: return_moveresult(x, (main_screen.geometry().x(), main_screen.geometry().y()))[2]
            )
            class_use.target = order_enemy[0]
      
        self_pos = class_use.geometry()
        self_x, self_y = class_use.x(), class_use.y()
        if class_use.target not in enem_list:
            class_use.target = enem_list[0]
        
        dx, dy, dist = return_moveresult(class_use, (class_use.target.geometry().x(), class_use.target.geometry().y()))

        if dist < 250:
            self_pos.setX(int(self_x - (dx * 2)))
            self_pos.setY(int(self_y - (dy * 2)))
        elif dist > 250 and dist < 350:
            self_pos.setX(int(self_x - (dx * 4)))
            self_pos.setY(int(self_y - (dy * 4)))
        else:
            pass
        
        if class_use.atk_tick <= 0:
            class_use.target.damage(0.1)
            class_use.atk_tick = 100
            play_sound(shoot)
        
        class_use.setGeometry(self_pos)

        return class_use

    else:
        return go_random(class_use)
    
# My dumbass dont know why its target type still attacks the same enemy even tho its changed.
# I might be stupid... cuz why does the fix feel so obvious.

# Stations
def on_happy():
    global happiness
    happiness += 35
    play_sound(hap_sound)

# Cash Bringers
def bring_cash(cash_get, Title="Cash Arrived"):
    global cash

    final_cash = cash_get * mult
    cash += final_cash
    notification(
        f"Recieved {final_cash}",
        Title,
        False
    )


# =========
# User Interface
# =========

#Pet UI



pet_btn = QPushButton("Pat")
pet_btn.clicked.connect(on_pet)
main_lay.addWidget(pet_btn)

money_btn = QPushButton("Get Money")
money_btn.clicked.connect(get_money)
main_lay.addWidget(money_btn)

face_label = QLabel(smile)
face_label.setStyleSheet("font-size:25px;")

speech_label = QLabel()
speech_label.setWordWrap(True)

main_lay.addWidget(face_label, alignment=Qt.AlignCenter)
main_lay.addWidget(speech_label)

# Shop UI
shopScreen = Special()
shopScreen.setWindowTitle("Shitpost Central")
shopLay = QVBoxLayout(shopScreen)

cash_label = QLabel("Cash: Null")
shopLay.addWidget(cash_label, alignment=Qt.AlignLeft)

shopScreen.setFixedWidth(850)

# Create a scroll area for shop items
shop_scroll = QScrollArea()
shop_scroll.setWidgetResizable(True)

shop_items_widget = QWidget()
shop_items_layout = QVBoxLayout(shop_items_widget)

shopScreen.setLayout(shopLay)

shop_scroll.setWidget(shop_items_widget)
shopLay.addWidget(shop_scroll)
# Status Screen
statusScreen = Special()
status_lay = QVBoxLayout()

pet_name = QLineEdit()
pet_name.setPlaceholderText("Pet Name Here")
pet_name.textChanged.connect(update_name)

status_lay.addWidget(pet_name)

hap_lay = QHBoxLayout()
hap_lab = QLabel("Happiness")
hap_bar = QProgressBar()
hap_prec = QLabel()

hun_lay = QHBoxLayout()
hun_lab = QLabel("Hunger")
hun_bar = QProgressBar()
hun_perc = QLabel()

hap_lay.addWidget(hap_lab)
hap_lay.addWidget(hap_bar)
hap_bar.setMaximum(max_hap)
hap_lay.addWidget(hap_prec)
status_lay.addLayout(hap_lay)

hun_lay.addWidget(hun_lab)

hun_lay.addWidget(hun_bar)
hun_bar.setMaximum(max_hunger)
hun_lay.addWidget(hun_perc)
status_lay.addLayout(hun_lay)

statusScreen.setLayout(status_lay)
# Feed UI
feedScreen = Special()
feed_lay = QVBoxLayout()

food_layout = QHBoxLayout()

feed_lay.addLayout(food_layout)



feedScreen.setLayout(feed_lay)

# Settings UI
set_screen = Special()
set_lay = QVBoxLayout()

bm_lay = QHBoxLayout()
bm_lab = QLabel("Music")
bm_set = QSlider(Qt.Horizontal)


bm_set.setMaximum(100)
bm_set.setMinimum(0)

bm_set.valueChanged.connect(change_bgr)

bm_lay.addWidget(bm_lab)
bm_lay.addWidget(bm_set)
set_lay.addLayout(bm_lay)


sfx_lay = QHBoxLayout()
sfx_lab = QLabel("Sound Effects")
sfx_set = QSlider(Qt.Horizontal)

hide_min = QCheckBox()
hide_min.setText("Hide Minors (Not what you're thinking)") # Diddy Reference?!?!?!?!?
set_lay.addWidget(hide_min)

sfx_set.setMaximum(100)
sfx_set.setMinimum(0)

sfx_lay.addWidget(sfx_lab)
sfx_lay.addWidget(sfx_set)
set_lay.addLayout(sfx_lay)

sfx_set.valueChanged.connect(change_sfxvol)
hide_min.stateChanged.connect(hide_check)

audio_label = QLabel()
audio_label.setWordWrap(True)
set_lay.addWidget(audio_label)

next_btn = QPushButton("-->")
next_btn.clicked.connect(next_song)
set_lay.addWidget(next_btn)

warn_label = QLabel("For some fuckass reason, there are times it could show the wrong song. Just wanna point that out.")
warn_label.setWordWrap(True)
warn_label.setStyleSheet("color:red;")
set_lay.addWidget(warn_label)

set_screen.setLayout(set_lay)

# Achievement Display
ad_screen = Special()

ad_lay = QVBoxLayout()
ad_scrollHolder = QWidget()
ad_scroll_lay = QVBoxLayout(ad_scrollHolder)
ad_scroll = QScrollArea()

ad_scroll.setWidget(ad_scrollHolder)
ad_scroll.setWidgetResizable(True)

ad_lay.addWidget(ad_scroll)
ad_screen.setLayout(ad_lay)

# Set Launcher
Launcher_Window = MainWindow()

LauncherWidget = QWidget()
LLayout = QVBoxLayout(LauncherWidget)

LW_Title = QLabel("WindowPet")
LLayout.addWidget(LW_Title, alignment=Qt.AlignCenter)

# Does this even have a purpose anymore
# Yk what, I'll prob make a hard-reset with dis (If I remember.... and if I know how to do it)
reviewPet = QPushButton("Pet Restore")
reviewPet.clicked.connect(open_again)
LLayout.addWidget(reviewPet)

saveBtn = QPushButton("Save Data")
saveBtn.clicked.connect(lambda: save_data(play_save=True))
LLayout.addWidget(saveBtn)

Quit_Btn = QPushButton("Terminate")
LLayout.addWidget(Quit_Btn)

Quit_Btn.clicked.connect(terminate)

Launcher_Window.setCentralWidget(LauncherWidget)
Launcher_Window.setWindowTitle("WindowPet Launcher")
Launcher_Window.closeEvent = lambda event: sys.exit()
Launcher_Window.show()
Launcher_Window.setWindowState(Qt.WindowMinimized)


# Activate Event Stuff
Even_Screen = Special()

Even_lay = QVBoxLayout()

es_scrollay = QVBoxLayout()
es_scrollwid = QWidget()
es_scrollwid.setLayout(es_scrollay)

es_scroll = QScrollArea()
es_scroll.setWidget(es_scrollwid)
es_scroll.setWidgetResizable(True)

Even_lay.addWidget(es_scroll)

Even_Screen.setLayout(Even_lay)

# Admin Panel

# Placeholder here hahahaha yes
 

# Launching....
bgr_onlaunch()
restate_data()
load_items()
reload_npcs()
regen_adis()
load_foods()
QTimer.singleShot(1500, reload_buffs)
load_eventgo()
update()

update_sl()
bgr_player.playlist().currentIndexChanged.connect(lambda _: update_sl())


# =========
# Testing Start
# =========

# If ur reading this section, ignore this.
# This is just wear I test the thingys

# =========
# Testing End
# =========

main_screen.setLayout(main_lay)
main_screen.show()

# Update Notes:
log_screen = Special()
log_lay = QVBoxLayout()
log_screen.setWindowTitle("Update Notes.")

log_scroll = QScrollArea()
log_holder = QWidget()
log_hlay = QVBoxLayout()

log_scroll.setWidget(log_holder)
log_scroll.setWidgetResizable(True)

notes_label = QLabel(
    "- Game is now out! Still in beta tho. \n\n- Expect some bugs tho there might be quite a lot."
)

log_hlay.addWidget(notes_label)
log_holder.setLayout(log_hlay)

log_lay.addWidget(log_scroll)
log_screen.setLayout(log_lay)
log_screen.show()

app.exec()

# =========
# Other Notes:
# =========

# To-do: 
    # Finish editing the shop data

# Comment to self: The progress on this is so slow holy shit.
#           Also ik what ur saying guys.. pyqt5..?
#           I swear it was better in my mind trust me.



