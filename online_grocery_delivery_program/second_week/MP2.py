from sympy import true
from MP1_siniflar import User, Product, Transaction
from tkinter import messagebox

import tkinter as tk
import dbm
import pickle 

class StokEkrani():

    def __init__(self, parent):
        self.parent = parent

        self.db_baslat()

        frame_kullanici_girdi = tk.Frame(self.parent,relief=tk.GROOVE, border=10, width=200)
        frame_kullanici_girdi.pack(fill=tk.Y, expand=True)
        self.initGirdi(frame_kullanici_girdi)

        frame_al_sat = tk.Frame(self.parent, relief=tk.GROOVE, border=10, width=200)
        frame_al_sat.pack(fill=tk.Y, expand=True, pady=10)
        self.initAlSat(frame_al_sat)
        self.urun_liste_guncelle()

    def db_baslat(self):
        self.db_urun = dbm.open("urunler5.db", 'c')
        self.db_satislar = dbm.open("satislar5.db", 'c')

    def initGirdi(self, frame):
        self.listbox_kategori = tk.Listbox(frame)
        kategoriler = ['Yiyecek', 'Icecek', 'Giyim', 'Elektronik', 'Ev']
        for kategori in kategoriler:
            self.listbox_kategori.insert(tk.END, kategori)

        self.isim_var = tk.StringVar()
        self.tanim_var = tk.StringVar()
        self.marka_var = tk.StringVar()
        self.link_var = tk.StringVar()
        self.stok_var = tk.IntVar()
        self.fiyat_var = tk.DoubleVar()

        label_isim = tk.Label(frame, text='Isim')
        entry_isim = tk.Entry(frame, textvariable=self.isim_var)

        label_marka = tk.Label(frame, text='Marka')
        entry_marka = tk.Entry(frame, textvariable=self.marka_var)
    
        label_tanim = tk.Label(frame, text='Tanim')
        entry_tanim = tk.Entry(frame, textvariable=self.tanim_var)

        label_stok = tk.Label(frame, text='Stok')
        entry_stok = tk.Entry(frame, textvariable=self.stok_var)

        label_fiyat = tk.Label(frame, text='Fiyat')
        entry_fiyat = tk.Entry(frame, textvariable=self.fiyat_var)

        label_link = tk.Label(frame, text='Link')
        entry_link  = tk.Entry(frame, textvariable=self.link_var)

        buton = tk.Button(frame, text="Ekle", command=self.urun_ekle_girdi)

        self.listbox_kategori.grid(rowspan=2)
        label_isim.grid(row=0, column=1, padx=10)
        entry_isim.grid(row=1, column=1, padx=10)

        label_marka.grid(row=0, column=2, padx=10)
        entry_marka.grid(row=1, column=2, padx=10)

        label_tanim.grid(row=0, column=3, padx=10)
        entry_tanim.grid(row=1, column=3, padx=10)
        
        label_stok.grid(row=0, column=4, padx=10)
        entry_stok.grid(row=1, column=4, padx=10)

        label_fiyat.grid(row=0, column=5, padx=10)
        entry_fiyat.grid(row=1, column=5, padx=10)

        label_link.grid(row=0, column=6, padx=10)
        entry_link.grid(row=1, column=6, padx=10)

        buton.grid(row=0, column=7, rowspan=2, padx=10)
    
    def urun_ekle_girdi(self):
        if (not self.listbox_kategori.curselection()):
            messagebox.showerror(title="Hata",message="En az bir kategori secmelisiniz")
            return

        u = Product(self.isim_var.get(), self.tanim_var.get(), self.marka_var.get(), self.link_var.get(), 
        self.fiyat_var.get(), self.listbox_kategori.get(self.listbox_kategori.curselection()), 
        self.stok_var.get())
        print(u.model_id, u)
        self.urun_ekle(u)
    
    def initAlSat(self, frame):
        self.urunler_listbox = tk.Listbox(frame, bg = "white", width=155,exportselection=0)
        self.urunler_listbox.pack(side=tk.LEFT, padx=10)
        self.buton_ekle = tk.Button(frame, text="1 Adet Sat", command = self.satis)
        self.buton_ekle.pack(side=tk.LEFT, padx=10)

    def satis(self):
        if (not self.urunler_listbox.curselection()):
            messagebox.showerror(title="Hata",message="En az bir urun secmelisiniz")
            return

        # Urun anahtari Product-1 ile basliyor - listbox ise 0'dan
        urun_anahtari = '{}'.format(self.urunler_listbox.curselection()[0] + 1)

        # Burada direk olarak pickled geldigini varsayiyoruz
        # Dosyalar ile ugrasirken try-except kullanmak bir best practice dir!
        u = pickle.loads(self.db_urun[urun_anahtari])
        t = Transaction('Kullanici', u.model_id, 1, u.fiyat)
        self.db_satislar[t.model_id] = pickle.dumps(t)
        if (u.alsat(t)):
            # Basarili bir sekilde satis yaptik:
            self.db_urun[u.model_id] = pickle.dumps(u)
            self.urun_liste_guncelle()
        else:
            messagebox.showerror(title="Hata",message="Satmaya calistiginiz urunden kalmadi")
            # Burada alternatif olarak bu urun DB'den ve listeden silinebilir
            self.db_urun.pop(u.model_id, None)
            self.urun_liste_guncelle()

 

    def urun_ekle(self, urun:Product):
        self.db_urun[urun.model_id] = pickle.dumps(urun)
        
        urun_string = "Kategori: {} | {} - {}, {}TL, stok: {}".format(urun.kategori,
                urun.isim, urun.marka, urun.fiyat, urun.stok)
        # Alternatif olarak Product sinifinin __str__ metodu da kullanilabilirdi

        self.urunler_listbox.insert(tk.END, urun_string)

    def urun_liste_guncelle(self):
        count =0
        self.urunler_listbox.delete(0, tk.END)  #clear listbox
        for key, value in self.db_urun.items():
            count +=1
            self.urun_ekle(pickle.loads(value))
        Product.sinif_sayici = count

    def __del__(self):
        # Bu urunden bir nesne yok olurken cagirilir (Destructor)
        self.db_satislar.close()
        self.db_urun.close()



def main():
    root = tk.Tk()
    app = StokEkrani(root)
    root.mainloop()

main()