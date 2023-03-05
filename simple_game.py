max_tas = int(input(("Tek seferde alinabilecek maksimum tas sayisini giriniz:")))
toplam_tas_adedi = 100
oyuncu1mi = 1

while toplam_tas_adedi > 0:
    print("Kalan tas adedi: ", toplam_tas_adedi)
    oyuncu = 0
    if oyuncu1mi == 1:
        oyuncu = int(input("1. oyuncu, almak istedigin tas sayisini gir: "))
    else:
        oyuncu = int(input("2. oyuncu, almak istedigin tas sayisini gir: "))
    if oyuncu < 0:
        print("Pozitif bir sayi giriniz.")
    elif oyuncu == 0:
        print("Sifir kabul edilemez")
    elif oyuncu < max_tas:
        if toplam_tas_adedi > oyuncu: 
            toplam_tas_adedi = toplam_tas_adedi - oyuncu
            if oyuncu1mi == 1:
                oyuncu1mi = 0
            else:
                oyuncu1mi = 1
        elif toplam_tas_adedi < oyuncu:
            print("Taslar yetersiz")
        else:
            toplam_tas_adedi = 0
    else:
        print("Gecerli bir sayi giriniz."),
if oyuncu1mi == 1:
    print("1. oyuncu helal")
else:
    print("2. oyuncu helal")