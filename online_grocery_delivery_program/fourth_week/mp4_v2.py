import json
from math import prod
from msilib.schema import Error
import re
from clusters import matrise_cevir, hcluster, kcluster, printclust
import tkinter as tk
import tkinter.filedialog as fd
import tkinter.messagebox as msgbox
import tkinter.scrolledtext as tkst
from terminal2tkintertext import print_terminalden, printcluster_terminalden

class FileParser():

    def __init__(self, fileName):
        file = open(fileName, 'r')
        self.user_dict = {}
        self.procudt_dict = {}
        try:
            veriler = json.load(file)
        except json.JSONDecodeError as e:
                print("Bu dosyayi yukleyemedim",file, "Cunku:", e)
        else:
            for satir in veriler:
                kullanici = satir['reviewerID']
                urun = satir['asin']
                search_text = satir['summary'] + ' ' + satir['reviewText']
                self.user_dict.setdefault(kullanici, {})
                self.procudt_dict.setdefault(urun, {})
                # Extract a list of words
                kelime_saymasi = {}
                words = self.getWords(search_text)
                for word in words:
                    self.user_dict[kullanici].setdefault(word,0)
                    self.user_dict[kullanici][word] += 1

                    self.procudt_dict[urun].setdefault(word,0)
                    self.procudt_dict[urun][word] += 1


    
    def getWords(self, text):
        # Remove all the HTML tags
        #<a class="read-more" href="https://m.signalvnoise.com/reiterating-our-use-restrictions-policy/">
        txt=re.compile(r'<[^>]+>').sub('',text)

        # Split words by all non-alpha characters
        words=re.compile(r'[^A-Z^a-z]+').split(text)
        
        # Convert to lowercase
        return [word.lower() for word in words if word!='']



class Kumelemeci():

    def __init__(self, yontem):
        self.yontem = yontem
        self.siniflar = None
        self.textbox_context = []


    def kumele(self, input_sozluk, k_means_sinif_sayisi = 3):
        data, self.names, words = matrise_cevir(input_sozluk)

        if self.yontem:
            # HCLUSTER
            self.siniflar = hcluster(data)
            # Iki tane alternatif cozumu gosteriyorum. 
            # Ilkinde ekte verilen ve terminal'e yazilan goruntuleri stream olarak iceri aktarabilirsiniz
            # self.textbox_context = printcluster_terminalden(self.siniflar, names)
            # Ikincisinde ise print_cluster fonksiyonunu bir listeye yazmak icin modifiye ettim:
            self.textbox_context = []
            self.text_write(self.siniflar)
        else:
            #KMeans:
            self.textbox_context = []
            self.siniflar = kcluster(data, k=k_means_sinif_sayisi)
            for sinif in range(len(self.siniflar)):
                self.textbox_context.append((sinif, [self.names[r] for r in self.siniflar[sinif]]))
                self.textbox_context.append('\n')
                

            
        return self.textbox_context

    def text_write(self, clust,  n=0):
        """
        Hiyerarşik kümelemenin sonucunun dendogram şeklinde bir listeye atilacak sekilde 
        clusters.py modulündeki printclust fonksiyonunu text widgeta yazabilecek şeklide revize ettim.
        """
        for i in range(n):
            self.textbox_context.append("{}".format(" "*i))

        if clust.id < 0:
            self.textbox_context.append("{}".format('-'))
        else:
            self.textbox_context.append( "{}".format(self.names[clust.id]))

        self.textbox_context.append( "\n")
        if clust.left != None: self.text_write(clust.left,  n=n + 1)
        if clust.right != None: self.text_write(clust.right, n=n + 1)




class KumelemeEkrani():

    def __init__(self, parent):
        self.parent = parent
        self.dosya_okuyucu = None
        self.initDosyaGui()
        self.initOptionsGui()
        self.initOutputGui()
        

    def initDosyaGui(self):

        # Frame 1 : Txt dosyasi yukleme
        frame1 = tk.Frame(self.parent,relief=tk.GROOVE, border=10, width=200)

        fr1_label = tk.Label(
            frame1, text="Yandaki butonu kullanarak verilen dosyayi girebilirsiniz")
        fr1_buton = tk.Button(
            frame1, text="Dosya Sec", command=self.aktar)

        fr1_label.pack(side=tk.LEFT)
        fr1_buton.pack(side=tk.RIGHT)
        frame1.pack()
        #########
    
    def initOptionsGui(self):

        # Frame 2: Kategorileri sectirme ve kumeleme belirleme ve kumele butonu
        frame2 = tk.Frame(self.parent,relief=tk.GROOVE, border=10, width=200)
        fr2_label1 = tk.Label(frame2, text = "Kumeleme Kriteri Secin")
        self.rb_kriter = tk.BooleanVar()
        self.rb_kriter.set(True)
        kullanici_rb = tk.Radiobutton(frame2,
                                     text="Kullaniciya Gore Kumeleme",
                                     variable=self.rb_kriter,
                                     value=True
                                     )

        urun_rb = tk.Radiobutton(frame2,
                                      text="Urune Gore Kumeleme",
                                      variable=self.rb_kriter,
                                      value=False
                                      )

        ana_label = tk.Label(
            frame2, text="Kumeleme Ekrani", font='Helvetica 18 bold')
        self.rb_yontem = tk.BooleanVar()
        self.rb_yontem.set(True)

        hiyerarsik_rb = tk.Radiobutton(frame2,
                                     text="Hiyerarsik Kumeleme",
                                     variable=self.rb_yontem,
                                     value=True
                                     )

        kmeans_rb = tk.Radiobutton(frame2,
                                      text="KMeans Kumeleme",
                                      variable=self.rb_yontem,
                                      value=False
                                      )

        fr2_label2 = tk.Label(frame2, text="KMeans Kume Sayisi")

        self.kmeans_kumeno = tk.IntVar()
        fr2_entry1 = tk.Entry(
            frame2, textvariable=self.kmeans_kumeno)

        fr2_buton1 = tk.Button(frame2, text="Kumele !", command=self.kumele)

        ana_label.grid(row=0, column=0, columnspan=4)

        fr2_label1.grid(row= 1, column = 0)
        kullanici_rb.grid(row=2, column=0)
        urun_rb.grid(row=3, column=0)
        
        hiyerarsik_rb.grid(row=2, column=1, sticky='w')
        kmeans_rb.grid(row=3, column=1, sticky='w')
        
        fr2_label2.grid(row=2, column=2)
        fr2_entry1.grid(row=3, column=2)
        
        fr2_buton1.grid(row=2, column=3, rowspan=2, padx=30)

        frame2.pack()
        #############

    def initOutputGui(self):

        # Frame 3: Goruntu ekrani
        frame3 = tk.Frame(self.parent,relief=tk.GROOVE, border=10, width=200)
        # Burda bir buton widgetı oluşturuyoruz, seçeneklerini belirliyoruz ve pencerimizde yerini belirliyoruz.
        self.Textbox1 = tkst.ScrolledText(frame3, font="Italic 13 bold", width=80, height=20, relief="sunken",
                       bd="5px")
      
        self.Textbox1.pack()
        frame3.pack()
        ###########

    def kumele(self):
        ''' Dosyayi okumak icin gerekli fonksiyonlari cagirir ve secili opsiyona gore kumeleme islemini yapar. 
        '''

        if self.dosya_okuyucu is None:
            msgbox.showerror(title="Dosya Yukleme hatasi",
                             message="Once veri dosyasi yuklemelisiniz")
            return 

        kumeleme_yardimcisi = Kumelemeci(self.rb_yontem.get())

        if self.rb_kriter.get():
            # Kullanici:
            self.contents = kumeleme_yardimcisi.kumele(self.dosya_okuyucu.user_dict)
        else:
            self.contents = kumeleme_yardimcisi.kumele(self.dosya_okuyucu.procudt_dict)

        # Textbox i temizle (daha onceden yazili olanlari sil)
        self.Textbox1.delete('1.0', tk.END)
        for c in self.contents:
            self.Textbox1.insert(tk.END, c)

    def aktar(self):
        dosya_ismi = fd.askopenfilename()
        try:
            self.dosya_okuyucu = FileParser(dosya_ismi)
            print(self.dosya_okuyucu.procudt_dict)
        except Exception as e:
            msgbox.showerror(title="Dosya Yukleme hatasi",
                             message=e)




root = tk.Tk()
root.title("Veri Ayiklama ve Kumeleme")
#root.geometry("650x650+400+100")

KumelemeEkrani(root)
root.mainloop()
