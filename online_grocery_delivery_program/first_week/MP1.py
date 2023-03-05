import dbm
import pickle
import json


class BazSinif():
    sinif_sayici = 0
    def __init__(self):
        # Her yeni veri nesnesi icin o veri sinifinda o veri ismiyle bir model numarasi olustur
        # Ornegin User-12
        type(self).sinif_sayici +=1
        self.model_id = '{}-{}'.format(type(self).__name__, type(self).sinif_sayici)

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
        if self.stok > transaction.adet:
            self.stok -= transaction.adet
        else:
            raise Exception("{} urununden {} adet kalmis, su satinalmayi yapamazsiniz {}".format(self.isim, self.stok, transaction))
        return self

    def __str__(self):
        return "{} : urun ismi {}, kategorisi {}, fiyati {}, kalan adet {}".format(self.model_id, self.isim, self.kategori, self.fiyat, self.stok)

class DatabaseController():
    def __init__(self):
        self.user_db = dbm.open('mp1_user_db', 'c')
        self.urun_db = dbm.open('mp1_product_db', 'c')
        self.satis_db = dbm.open('mp1_transaction_db', 'c')

    def add(self, record):
        if type(record) == User:
            self.user_db[record.model_id] = pickle.dumps(record)
        elif type(record) == Product:
            self.urun_db[record.model_id] = pickle.dumps(record)
        elif type(record) == Transaction:
            self.satis_db[record.model_id] = pickle.dumps(record)
        else:
            raise Exception("add fonksiyonu user, product ya da transaction sinifi bekliyordu, gelen {}".format(type(record)))

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
            raise Exception(" get fonksiyonu pickle load yapamadi, db bozulmus olabilir")
        except TypeError as e:
            raise Exception('get fonksiyonu icin string yapisinda bir model_id kullanilmali', e)
    
    
    def len(self, sinif_tipi):
        if sinif_tipi == User:
            return len(self.user_db.keys())
        elif sinif_tipi == Product:
            return len(self.urun_db.keys())
        elif sinif_tipi == Transaction:
            return len(self.satis_db.keys())
        else:
            raise Exception("len fonksiyonu user, product ya da transaction sinifi bekliyordu, gelen {}".format(type(record)))

        

class UserInteraction():

    def __init__(self):

        self.dbi = DatabaseController()
        self.verileri_hazirla()
        print("-----------Veriler Hazirlandi--------------")
        self.print_dbs()
        print("-" *50)

        print("-----------Islemler Basliyor--------------")
        basla = True
        while(basla):
            basla = self.kullaniciya_sor()
            continue

        self.db_sync()
        
        print("-" *50)
        self.print_dbs()
        print("-" *50)

        print("-----------Kullanici harcaamalari raporlaniyor--------------")
        for k in self.dbi.user_db.keys():
            self.harcama_raporla(k)

    def verileri_hazirla(self):
        ''' Bu fonksiyon eger daha once gerekli veri yapilari yaratilmamissa verileri iceri aktarir ve 2 adet dummy kullanici yaratir'''
        if (self.dbi.len(User)) > 0:
            print("Kullanici listesi iceri aktarilmis, DB kullaniliyor")
        else:
            self.dummy_kullanici_yarat()

        if (self.dbi.len(Product)) > 0:
            print("Kullanici listesi iceri aktarilmis, DB kullaniliyor")
        else:
            self.urunleri_oku('urunler_temiz.json')

    def dummy_kullanici_yarat(self):
        self.dbi.add(User('isim1'))
        self.dbi.add(User('isim2'))
    
    def urunleri_oku(self, dosya_ismi):
        file = open(dosya_ismi, 'r')
        urunler = json.load(file)
        for satir in urunler:
            p = Product(satir['isim'], satir['aciklama'], satir['marka'],satir['marka'], float(satir['fiyat']), satir['kategori'], int(satir['stok']))
            self.dbi.add(p)
        file.close()
    
    def kullaniciya_sor(self):
        if input("Yeni bir islem girmek isyor musunuz? [E, H]").lower() !='e':
            return False

        # Birden fazla kullanici tanimli oldugu durum - Sizin yapmaniza gerek yoktu
        u_no = input(" Lutfen Kullanici Numarasi secin [1 veya 2]: ")
        if u_no == '1' or u_no == '2':
            u_secili = 'User-'+u_no
        else:
            print("Dogru bir kullanici secmediniz, programdan cikiliyor")
            return False
        p_no = input("Lutfen bir urun kodu seciniz [1--17]: ")
        
        # Bir baska yontem de direk olarak olusturdugunuz bu anahtar urun_db icerisinde var mi diye bakabilirsiniz
        olasi_urunler = []
        for i in range(1, len(self.dbi.urun_db.keys())+1):
            olasi_urunler.append(str(i))

        if p_no in olasi_urunler:
            p_secili = 'Product-{}'.format(p_no)
        else:
            print("Dogru bur urun numarasi girmediniz, programdan cikiliyor")
            return False

        adet = input("Lutfen satinalma adeti girin: ")
        if not adet.isnumeric():
            print("sayi girmeniz gerekiyor, programdan cikiliyor")
            return False
        
        urun_fiyati = self.dbi.get(p_secili).fiyat

        t = Transaction(u_secili, p_secili, int(adet), urun_fiyati)
        self.dbi.add(t)
        soru = input("Baska bir urun girmek ister misiniz? [E, H]")
        if soru.lower() == 'e':
            print('\n')
            return True
        return False

    def db_sync(self):
        for t_key in self.dbi.satis_db.keys():
            t = self.dbi.get(t_key)
            self.dbi.add(self.dbi.get(t.kullanici).alsat(t))
            self.dbi.add(self.dbi.get(t.urun).alsat(t))

    def harcama_raporla(self, kullanici_kodu):
        u = self.dbi.get(kullanici_kodu)
        print("Kullanici {} toplamda  {} adet siparis vermis ve {} harcamis".format(u.model_id, len(u.siparisler), u.toplam_harcama))


    def print_dbs(self):
        print("Urunler")
        for k in self.dbi.urun_db.keys():
            print(self.dbi.get(k))
        print("Kullanicilar")
        for k in self.dbi.user_db.keys():
            print(self.dbi.get(k))
        print("Islemler")
        for k in self.dbi.satis_db.keys():
            print(self.dbi.get(k))


c = UserInteraction()