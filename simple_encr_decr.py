secim = int(input("Lutfen yapacaginiz islemin numarasini giriniz:\n1: Sifreleme\n2: Sifre cozme\n"))
if(secim == 1):
    mesaj = input("Sifrelenecek mesaji giriniz: ")
    n = int(input("Sifre kaydirma sayisini giriniz: "))
    result = ""
    devam = 1
    nfor = n
    i = 0
    if(n <= 0):
        devam = 0
    if(devam == 0):
        print("Lutfen pozitif bir kaydirma sayisi giriniz!")
    else:
        for karakter in mesaj:
            i = ord(karakter)
            if(i == 32):
                result += chr(i)
            elif(i >= 48 and i <= 57):
                nfor = n % 10
                if(i + nfor > 57):
                    result += chr(i + nfor - 10)
                else:
                    result += chr(i + nfor)
            elif(i >= 65 and i <= 90):
                nfor = n % 26
                if(i + nfor> 90):
                    result += chr(i + nfor - 26)
                else:
                    result += chr(i + nfor)
            elif(i >= 97 and i <= 122):
                nfor = n % 26
                if(i + nfor> 122):
                    result += chr(i + nfor - 26)
                else:
                    result += chr(i + nfor)
            else:
                devam = 0
                break
        if(devam == 0):
            print("Lutfen harf, sayi ve bosluk disinda karakter girmeyiniz!")
        else:
            print(result)
elif(secim == 2):
    mesaj = input("Sifresi cozulecek mesaji giriniz: ")
    n = int(input("Sifre kaydirma sayisini giriniz: "))
    result = ""
    devam = 1
    nfor = n
    i = 0
    if(n <= 0):
        devam = 0
    if(devam == 0):
        print("Lutfen pozitif bir kaydirma sayisi giriniz!")
    else:
        for karakter in mesaj:
            i = ord(karakter)
            if(i == 32):
                result += chr(i)
            elif(i >= 48 and i <= 57):
                nfor = n % 10
                if(i - nfor < 47):
                    result += chr(i - nfor + 10)
                else:
                    result += chr(i - nfor)
            elif(i >= 65 and i <= 90):
                nfor = n % 26
                if(i - nfor < 65):
                    result += chr(i - nfor + 26)
                else:
                    result += chr(i - nfor)
            elif(i >= 97 and i <= 122):
                nfor = n % 26
                if(i - nfor < 97):
                    result += chr(i - nfor + 26)
                else:
                    result += chr(i - nfor)
            else:
                devam = 0
                break
        if(devam == 0):
            print("Lutfen harf, sayi ve bosluk disinda karakter girmeyiniz!")
        else:
            print(result)
else:
    print("Lutfen gecerli bir numara tuslayiniz!")