import re
import shelve
import tkinter as tk
import tkinter.scrolledtext as tkst
from mysearchengine import crawler, searcher
import time
class AramaEkrani():
    
    def __init__(self, parent):
        self.parent = parent
        self.pagelist = ['https://ois.istinye.edu.tr/bilgipaketi/eobsakts/ogrenimprogrami/program_kodu/0401001/menu_id/p_38/tip/L/submenuheader/2/ln/tr/print/1']

        self.dbtables = {'urllist': 'urllist_dersler3.db',
                         'wordlocation':  'wordlocation_dersler3.db',
                         'link': 'link_dersler3.db',
                         'linkwords': 'linkwords_dersler3.db',
                         'pagerank':  'pagerank_dersler3.db'}


        self.initGui()

        with shelve.open(self.dbtables['urllist'], 'c') as tmp:
            if len(tmp.keys())<1:
                self.T1.delete('1.0', tk.END)
                self.T1.insert(tk.END, 'Arama yapabilmek icin onceden endeksleme yapmalisiniz!')
            else:
                self.T1.insert(tk.END, 'Arama yapabilirsiniz: Lutfen yukaridaki kutuya kelimeleri girin!')

    def initGui(self):

        frame0 = tk.Frame(self.parent, relief=tk.GROOVE, border=10, width=100)

        fr0_buton = tk.Button(
            frame0, text="Emeklemeyi Baslat", command=self.endeksle)
               

        fr0_buton.pack(pady=10)
        frame0.pack()

        frame1 = tk.Frame(self.parent, relief=tk.GROOVE, border=10, width=500)

        f1_label1 = tk.Label(frame1, text="Arama yapilacak kelime(ler)i girin:")

        self.arama_kelimeleri = tk.StringVar()
        f1_entry1 = tk.Entry(frame1, textvariable=self.arama_kelimeleri, width = 50, font=("default",20))

        f1_label1.pack(pady=10)
        f1_entry1.pack(pady=10)

        frame1.pack()

        frame2 = tk.Frame(self.parent)

        self.filtre_kelime_frekansi = tk.BooleanVar()
        f2_cb1 = tk.Checkbutton(frame2, text="Kelime Frekansi",
                            variable=self.filtre_kelime_frekansi)

        self.filtre_gelen_linker = tk.BooleanVar()
        f2_cb2 = tk.Checkbutton(frame2, text="Inbound Link",
                            variable=self.filtre_gelen_linker)

        self.filtre_pagerank = tk.BooleanVar()
        f2_cb3 = tk.Checkbutton(frame2, text="PageRank",
                            variable=self.filtre_pagerank)

        f2_buton1 = tk.Button(frame2, text="Ara", command=self.arama)

        f2_cb1.grid(row=0, column = 0, sticky='WN')
        f2_cb2.grid(row=1, column = 0, sticky='WN')
        f2_cb3.grid(row=2, column = 0, sticky='WN')

        f2_buton1.grid(row=0, column = 1, rowspan=3, padx=10)

        frame2.pack()

        frame3 = tk.Frame(self.parent)

        self.T1 = tkst.ScrolledText(
            frame3, font="Italic 13 bold", width=120, height=20, relief="sunken", bd="5px")
        
        self.T1.pack()
        frame3.pack()

    def arama(self):

        self.T1.delete('1.0', tk.END)
        self.T1.insert(tk.END, 'Arama Baslatildi')

        # Dikkat!: Sozlugun anahtar isimleri, searcher sinifindaki fonksiyon isimleri ile ayni olmali.
        seciliFiltreler = dict()
        seciliFiltreler['frequencyscore'] = int(
            self.filtre_kelime_frekansi.get())

        seciliFiltreler['inboundlinkscore'] = int(
            self.filtre_gelen_linker.get())

        seciliFiltreler['pagerankscore'] = int(
            self.filtre_pagerank.get())

        searcher_ = searcher(self.dbtables)

        
        # Sonradan sinifa ekledigimiz fonksiyon yardimi ile daha once pagerank hesaplandiysa tekrar hesaplamiyoruz:
        if not searcher_.is_pagerank_populated():
            searcher_.calculatepagerank()

        sonuclar = searcher_.query(
            self.arama_kelimeleri.get(), seciliFiltreler)
        
        self.T1.delete('1.0', tk.END)
        self.T1.insert(tk.END, 'Sonuclar:\n')

        # Query bos dondgunde None geliyor, None iterable degil!
        if sonuclar:
            for (score, url) in sonuclar:
                self.T1.insert(tk.END, '{}\t{} -> {}\n'.format(score, searcher_.get_linkwords_from_url(url), url))
        else:
            self.T1.insert(tk.END, "Aradiginiz kelimleler ile sonuc bulunamadi")
        

    def endeksle(self):
        
        self.T1.delete('1.0', tk.END)
        self.T1.insert(tk.END, 'Emekleme Baslatildi\n Lutfen Bekleyin')
        time.sleep(2.0)

        pageList = ['https://ois.istinye.edu.tr/bilgipaketi/eobsakts/ogrenimprogrami/program_kodu/0401001/menu_id/p_38/tip/L/submenuheader/2/ln/tr/print/1']

        self.crawler_ = crawler(self.dbtables)
        self.crawler_.createindextables()
        self.crawler_.crawl(pageList, depth=3)
        self.crawler_.close()

        self.T1.delete('1.0', tk.END)
        self.T1.insert(tk.END, 'Tarama ve Endeksleme Tamamlandi\n')
    
 



        
root = tk.Tk()
root.title("Endeksleme ve Arama")
#root.geometry("650x650+400+100")

AramaEkrani(root)
root.mainloop()


