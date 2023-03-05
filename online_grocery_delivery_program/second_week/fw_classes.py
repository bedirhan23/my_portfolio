import dbm
import pickle
import json

from sqlalchemy import true


class BazSinif():
    sinif_sayici = 0
    def __init__(self):
        # Her yeni veri nesnesi icin o veri sinifinda o veri ismiyle bir model numarasi olustur
        # Ornegin User-12
        type(self).sinif_sayici +=1
        self.model_id = '{}'.format(type(self).sinif_sayici)

class User(BazSinif):
    def __init__(self, isim):
        super().__init__()
        self.siparisler = []
        self.isim = isim
        self.toplam_harcama = 0.0

    def alsat(self, transaction):
        if transaction.kullanici != self.model_id:
            # Bu baska user icin
            print('[]', transaction.kullanici, self.model_id)
        else:
            self.siparisler.append({'urun': transaction.urun, 'adet': transaction.adet})
            self.toplam_harcama += transaction.adet * transaction.fiyat
        return self

    def __str__(self):
        return "{} : Kullanici ismi {} ve siparisleri {}".format(self.model_id, self.isim, self.siparisler)

class Transaction(BazSinif):
    def __init__(self, user_id, product_id, adet, fiyat):
        super().__init__()
        self.kullanici = user_id
        self.urun = product_id
        self.fiyat = fiyat
        self.adet = adet
        print(self.adet)

    def __str__(self):
        return "{} : Fatura kullanici ismi {} ve urun {} ve adedi {}".format(self.model_id, self.kullanici, self.urun, self.adet)

class Product(BazSinif):

    def __init__(self, isim, tanim, marka, link, fiyat, kategori, stok):
        super().__init__()
        self.isim = isim
        self.tanim = tanim
        self.link = link
        self.fiyat = fiyat
        self.marka = marka
        self.kategori = kategori
        self.stok = stok

    def fiyat_arttir(self, artis_miktari):
        self.fiyat += artis_miktari
    
    def kampanya(self, yuzde):
        ''' Yapilan kampanya yuzdesi oraninda indirim yapar. Ornegin yuzde:10 indirim icin urun fiyati 0.9 ile carpilir
        '''
        self.fiyat *= (1-yuzde) 
    
    def alsat(self, transaction):
        ## Bu fonksiyonu MP2 icin guncelledik:

        if self.stok >= transaction.adet:
            self.stok -= transaction.adet
            return True
        else:
            return False

    def __str__(self):
        return "{} : urun ismi {}, kategorisi {}, fiyati {}, kalan adet {}".format(self.model_id, self.isim, self.kategori, self.fiyat, self.stok)

class DatabaseController():
    def __init__(self):
        self.user_db = dbm.open('user_db', 'c')
        self.urun_db = dbm.open('urun_db', 'c')
        self.satis_db = dbm.open('satis_db', 'c')

    def add(self, record):
        if type(record) == User:
            self.user_db[record.model_id] = pickle.dumps(record)
        elif type(record) == Product:
            self.urun_db[record.model_id] = pickle.dumps(record)
        elif type(record) == Transaction:
            self.satis_db[record.model_id] = pickle.dumps(record)
        else:
            raise Exception("add fonksiyonu user ya da product sinifi bekliyordu, gelen {}".format(type(record)))


    def get(self, model_id):
        # model_id string nesnesi gelirse byte haline cevir once
        if type(model_id)==str:
            model_id = model_id.encode()

        try:
            if model_id in self.user_db.keys():
                record = pickle.loads(self.user_db[model_id])
            elif model_id in self.urun_db.keys():
                record = pickle.loads(self.urun_db[model_id])
            elif model_id in self.satis_db.keys():
                record = pickle.loads(self.satis_db[model_id])
            else:
                record = None
            return record

        except pickle.PickleError as e:
            raise Exception(" get_user fonksiyonu pickle load yapamadi, db bozulmus olabilir")
        except TypeError as e:
            raise Exception('get_user fonksiyonu icin string yapisinda bir model_id kullanilmali', e)
            
        
