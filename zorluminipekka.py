import json
import pickle
import dbm
import os

def eskisiniSil(isim):
    if os.path.exists(isim+".bak"):
        os.remove(isim+".bak")
    if os.path.exists(isim+".dat"):
        os.remove(isim+".dat")
    if os.path.exists(isim+".dir"):
        os.remove(isim+".dir")

def urunleri_oku(dosya_ismi):
    itemListe = []
    file = open(dosya_ismi, 'r')
    urunler = json.load(file)
    for satir in urunler:
        itemListe.append(Item(satir['isim'], satir['marka'], float(satir['fiyat']), int(satir['stok']), satir['aciklama'], satir['kategori'], "ITEM-"+str(len(itemListe)+1), satir["link"]))
    file.close()
    return itemListe

class Item(object):
    """This is the class for items."""
    def __init__(self, item_name, item_brand, item_price, item_stock, item_definition, list_of_category, item_uuid , item_link):
        self.item_name = item_name
        self.item_brand = item_brand
        self.list_of_category = list_of_category
        self.item_price = item_price
        self.item_link = item_link
        self.item_stock = item_stock
        self.item_definition = item_definition
        self.item_uuid = item_uuid

    def raise_price(self, raise_amount):
        self.item_price = self.item_price + raise_amount
        return self.item_price

    def discount(self, discount_per):
        self.item_price = self.item_price - self.item_price*discount_per/100
        return self.item_price

    def item_info(self):
        print("\nItem name is {},the price of this item is {} and stock of this item is {}. ".format(self.item_name, self.item_price, self.item_stock))
    
    def set_stock(self, order):
        if(self.item_stock >= order.order_piece):
            self.item_stock = self.item_stock - order.order_piece
            return True
        return False

class Order(object):
    """This is the class for consumers order."""
    def __init__(self, order_uuid, user, item, order_piece):
        self.order_piece = order_piece
        if item.set_stock(self):
            self.order_uuid = order_uuid
            self.user_uuid = user.user_uuid
            self.item_price = item.item_price 
            self.order_item = item
            self.spending = self.item_price * self.order_piece
            user.spending = user.spending + self.spending
            orderList.append(self)

        else:
            raise Exception("There is not enough stock for this item. \n")

class User(object):
    """This is the class for consumers wallet."""

    def __init__(self, user_name, user_uuid, spending, order_list):
        self.user_name = user_name
        self.user_uuid = user_uuid
        self.spending = spending
        self.order_list = order_list

dbi = dbm.open("items", 'c')
dbu = dbm.open("users", 'c')
dbo = dbm.open("orders", 'c')

itemsEmpty = True
itemList = []
for key in dbi:
    itemsEmpty = False
    itemList.append(pickle.loads(dbi[key]))

if(itemsEmpty):
    itemList = urunleri_oku("urunler_temiz.json")

usersEmpty = True
userList = []
for key in dbu:
    userList.append(pickle.loads(dbu[key]))
    usersEmpty = False

if(usersEmpty):
    userList.append(User("Ahmet", "USER-"+str(len(userList)+1), 0, []))
    userList.append(User("Mehmet", "USER-"+str(len(userList)+1), 0, []))

orderList = []
for key in dbo:
    orderList.append(pickle.loads(dbo[key]))

dbi.close()
dbu.close()
dbo.close()

buluna = True

while(buluna):
    arkadan = "Kullanici secimi yapiniz: \n"
    i = 1
    for user in userList:
        arkadan += str(i) + ": " + user.user_name + "\n"
        i = i + 1
    kullanici_secim = int(input(arkadan))
    agzina = True
    while(agzina):
        onden = "Urun secimi yapiniz: \n"
        j = 1
        for item in itemList:
            onden += str(j) + ": " + item.item_name + "\n"
            j = j + 1
        urun_secim = int(input(onden))
        piece = int(input("Lutfen satin alma adedi girin: "))
        try:
            userList[kullanici_secim-1].order_list.append(Order("ORDER-"+str(len(userList[kullanici_secim-1].order_list)), userList[kullanici_secim-1], itemList[urun_secim-1], piece))
        except Exception as e:
            print(e)
        if input("Baska bir urun girmek ister misiniz? [E, H]: ") == "H":
            agzina = False
    for item in itemList:
        item.item_info()
    
    print("\nKullanici "+str(userList[kullanici_secim-1].user_uuid)+" toplamda "+str(len(userList[kullanici_secim-1].order_list))+" adet siparis vermis ve "+str(userList[kullanici_secim-1].spending)+" harcamis. ")
    if input("Kullanici girisi yapmak ister misiniz? [E, H]: ") == "H":
        buluna = False
        eskisiniSil("items")
        dbi = dbm.open("items", 'c')
        for item in itemList:
            dbi[item.item_uuid] = pickle.dumps(item)
        dbi.close()
        eskisiniSil("users")
        dbu = dbm.open("users", 'c')
        for user in userList:
            dbu[user.user_uuid] = pickle.dumps(user)
        dbu.close()
        eskisiniSil("orders")
        dbo = dbm.open("orders", 'c')
        for order in orderList:
            dbo[order.order_uuid] = pickle.dumps(order)
        dbo.close()
