okunus = ""
ek = "eksi"
yu = "yüz"
basamaklar = ["bin", "milyon", "milyar", "trilyon", "katrilyon"]
birler = ["sıfır", "bir", "iki", "üç", "dört", "beş", "altı", "yedi", "sekiz", "dokuz"]
onlar = ["on", "yirmi", "otuz", "kırk", "elli", "altmış", "yetmiş", "seksen", "doksan"]
bn = 1000

def boslukEkle(okunusb):
    okunusb = okunusb + " "
    return okunusb    

def bir(okunusm, ym):
    if(ym > 0):
        okunusm = okunusm + birler[ym]
        okunusm = boslukEkle(okunusm)
    return okunusm

def on(okunusl, yl):
    if(yl > 0):
        okunusl = okunusl + onlar[yl-1]
        okunusl = boslukEkle(okunusl)
    return okunusl

def yuz(okunusk):
    okunusk = okunusk + yu
    okunusk = boslukEkle(okunusk)
    return okunusk

def yuzdeKontrol(yuzlukKisim, okunusy):
    if(yuzlukKisim>=200):
        okunusy = okunusy + birler[int(yuzlukKisim/100)]
        okunusy = boslukEkle(okunusy)
        okunusy = yuz(okunusy)
        okunusy = on(okunusy, int((yuzlukKisim%100)/10))
        okunusy = bir(okunusy, yuzlukKisim%10)
    elif(yuzlukKisim>=100):
        okunusy = yuz(okunusy)
        okunusy = on(okunusy, int((yuzlukKisim%100)/10))
        okunusy = bir(okunusy, yuzlukKisim%10)
    else:
        if(yuzlukKisim>=10):
            okunusy = on(okunusy, int((yuzlukKisim%100)/10))
            okunusy = bir(okunusy, yuzlukKisim%10)
        else:
            if(yuzlukKisim%10 > 0):
                okunusy = bir(okunusy, yuzlukKisim%10)
    return okunusy

def usAl(sayig, kacKereAl):
    usSayaci = 0
    sayiSonuc = 1
    while(usSayaci < kacKereAl):
        sayiSonuc = sayiSonuc * sayig
        usSayaci += 1
    return sayiSonuc

def yazdir(sayii, okunusi, kacKere):
    yazdirSayac = 0
    while (yazdirSayac < kacKere):
        if(int(sayii/usAl(bn, 1 + kacKere - yazdirSayac)) != 0):
            okunusi = yuzdeKontrol(int(sayii/usAl(bn, 1 + kacKere - yazdirSayac)), okunusi)
            okunusi = okunusi + basamaklar[kacKere - yazdirSayac]
            okunusi = boslukEkle(okunusi)
        sayii = sayii % usAl(bn, 1 + kacKere - yazdirSayac)
        yazdirSayac += 1
    okunusi = biYazdir(sayii, okunusi)
    return okunusi

def biYazdir(sayih, okunush):
    if(sayih>=2*bn):
        okunush = yuzdeKontrol(int(sayih/bn), okunush)
        okunush = okunush + basamaklar[0]
        okunush = boslukEkle(okunush)
        okunush = yuzdeKontrol(sayih%bn, okunush)
    else:
        if(int(sayih/bn) != 0):
            okunush = okunush + basamaklar[0]
            okunush = boslukEkle(okunush)
        okunush = yuzdeKontrol(sayih%bn, okunush)
    return okunush

def basamakYazdir(sayib, okunusa):
    if(sayib >= usAl(bn, 5)):
        okunusa = yazdir(sayib, okunusa, 4)
    elif(sayib >= usAl(bn, 4)):
        okunusa = yazdir(sayib, okunusa, 3)
    elif(sayib >= usAl(bn, 3)):
        okunusa = yazdir(sayib, okunusa, 2)
    elif(sayib >= usAl(bn, 2)):
        okunusa = yazdir(sayib, okunusa, 1)
    elif(sayib>=bn):
        okunusa = biYazdir(sayib, okunusa)
    else:
        okunusa = yuzdeKontrol(sayib, okunusa)
    return okunusa

def buyuklukKontrol(sayia):
    if(sayia>=usAl(bn, 6)):
        return 0
    return 1

sayi = int(input("Lütfen okunuşunu görmek istediğiniz sayıyı giriniz: "))

if(sayi == 0):
    okunus = okunus + birler[0]
    print("Yazdığınız sayının okunuşu: ", okunus)   

elif(sayi > 0):
    if(buyuklukKontrol(sayi) != 0):
        okunus = basamakYazdir(sayi, okunus)
        print("Yazdığınız sayının okunuşu: ", okunus)
    else:
        print("999999999999999999 sayısından büyük sayılar kabul edilmemektedir!")

else:
    okunus = okunus + ek
    okunus = boslukEkle(okunus)
    sayi = sayi * -1
    if(buyuklukKontrol(sayi) != 0):
        okunus = basamakYazdir(sayi, okunus)
        print("Yazdığınız sayının okunuşu: ", okunus)
    else:
        print("-999999999999999999 sayısından küçük sayılar kabul edilmemektedir!")
