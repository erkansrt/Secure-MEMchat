# 🔒 Secure-MEMchat Güvenli Mesajlaşma ve Steganografi Projesi

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-SocketIO-black?style=for-the-badge&logo=flask)
![Security](https://img.shields.io/badge/Security-DES%20%26%20LSB-red?style=for-the-badge&logo=lock)
![Platform](https://img.shields.io/badge/Platform-Cross--Platform-lightgrey?style=for-the-badge)

<p align="center">
  <strong>Görüntü İşleme (LSB), Simetrik Şifreleme (DES) ve Modern Soket Mimarisi kullanılarak geliştirilmiş<br>Uçtan Uca Güvenli Mesajlaşma Simülasyonu.</strong>
</p>

[Özellikler](#-özellikler) • [Mimari](#-mimari-ve-mantık) • [Kurulum](#-kurulum) • [Kullanım](#-kullanım)

</div>

---

## 📖 Proje Hakkında

Bu proje, **Bilgi Güvenliği** dersi kapsamında geliştirilmiştir. Amaç, modern ağ programlama tekniklerini (WebSocket) klasik güvenlik yöntemleriyle (Steganografi ve DES) birleştirerek güvenli bir iletişim kanalı oluşturmaktır.

Sistem, kullanıcıların **şifrelerini bir resim dosyasının piksellerine gizleyerek (LSB Steganography)** sunucuya iletmesini sağlar. Mesajlaşma sırasında ise her mesaj, göndericinin anahtarıyla şifrelenir (**DES**), sunucuda çözülür ve alıcının anahtarıyla tekrar şifrelenerek iletilir.

## ✨ Özellikler

* **🖼️ LSB Steganografi (Resim İçine Gizleme):** Kullanıcı kayıt ve giriş işlemleri sırasında şifreler ağ üzerinde düz metin (plaintext) olarak değil, bir PNG resminin içine gizlenerek taşınır.
* **🔐 DES Şifreleme:** İletilen tüm mesajlar DES (Data Encryption Standard) algoritması ile şifrelenir. Sunucu bir "Tercüman" görevi görür.
* **⚡ Gerçek Zamanlı İletişim:** `Flask-SocketIO` altyapısı sayesinde mesajlar anlık iletilir (Polling gerekmez).
* **💾 Çevrimdışı Mesajlaşma:** Alıcı o an çevrimdışı olsa bile mesajlar veritabanında (SQLite) şifreli saklanır ve kullanıcı bağlandığında teslim edilir.
* **🎨 Modern Arayüz:** `CustomTkinter` kütüphanesi ile tasarlanmış, karanlık mod destekli, şık ve kullanıcı dostu masaüstü arayüzü.
* **🌍 Dağıtık Mimari:** Sunucu (Ubuntu Host) ve İstemciler (Windows/Kali VM) arasında sorunsuz çalışacak şekilde tasarlanmıştır.

## 🛠️ Mimari ve Mantık

### Proje Yapısı
```text
GuvenliMesajlasma/
├── common/             # Ortak Modüller (Server ve Client kullanır)
│   ├── crypto.py       # DES Şifreleme/Çözme Kodları
│   └── steganography.py# LSB (Resme Gizleme) Kodları
├── server/             # Sunucu Tarafı
│   ├── app.py          # Flask & SocketIO Sunucusu
│   └── database_manager.py # SQLite Veritabanı Yönetimi
├── client/             # İstemci Tarafı
│   ├── main_modern.py  # GUI (Arayüz) Kodu
│   └── api_client.py   # Sunucu İletişim Modülü


Akış Diyagramı

    Kayıt: Client -> Şifreyi Resme Göm (LSB) -> Resmi Sunucuya Yükle -> Sunucu Şifreyi Çıkarır -> DB'ye Kaydeder.

    Mesajlaşma: Client A (Şifrele) -> Sunucu (Çöz & B için Şifrele) -> Client B (Çöz & Oku).

🚀 Kurulum

Projeyi yerel ortamınızda veya sanal makinelerde çalıştırmak için aşağıdaki adımları izleyin.
Gereksinimler

    Python 3.8 veya üzeri

    pip paket yöneticisi

1. Depoyu Kopyalayın
Bash

git clone [https://github.com/kullaniciadiniz/secure-stegochat.git](https://github.com/kullaniciadiniz/secure-stegochat.git)
cd secure-stegochat

2. Sanal Ortam Oluşturun (Önerilen)
Bash

# Linux/Mac
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate

3. Kütüphaneleri Yükleyin

Tüm gerekli paketleri yüklemek için:
Bash

pip install Flask Flask-SocketIO eventlet Pillow pycryptodome gunicorn requests python-socketio customtkinter packaging

💻 Kullanım

Sistemi test etmek için önce sunucuyu, ardından bir veya daha fazla istemciyi başlatmalısınız.
Adım 1: Sunucuyu Başlat (Server)

Sunucu terminalinde:
Bash

# Geliştirme modu için:
python server/app.py

# VEYA Prodüksiyon (Gunicorn) modu için:
gunicorn --worker-class eventlet -w 1 --bind 0.0.0.0:5000 server.app:app

Sunucu varsayılan olarak 5000 portunda çalışır.
Adım 2: İstemciyi Başlat (Client)

Farklı bir terminalde veya başka bir bilgisayarda:
Bash

python client/main_modern.py

    Uygulama açıldığında Sunucu IP adresini girin (Aynı makine ise localhost veya 127.0.0.1).

    Kayıt Ol: Bir kullanıcı adı, şifre belirleyin ve PNG formatında bir resim seçerek kayıt olun.

    Giriş Yap: Aynı bilgilerle giriş yapın.

📸 Ekran Görüntüleri
Giriş Ekranı	Sohbet Arayüzü
	
(Buraya kendi ekran görüntülerini ekleyebilirsin)	
⚠️ Yasal Uyarı

Bu proje eğitim amaçlıdır.

    Kullanılan DES algoritması günümüzde güvenli kabul edilmemektedir (AES tercih edilmelidir), ancak akademik gösterim için kullanılmıştır.

    LSB steganografi basit bir gizleme yöntemidir, profesyonel analizlerle tespit edilebilir.

    Gerçek dünyada hassas veriler için kullanılmamalıdır.

🤝 Katkıda Bulunma

Pull request'ler kabul edilir. Büyük değişiklikler için önce tartışma bölümünde konu açınız.
📜 Lisans

MIT


### Yapman Gerekenler:
1.  Bu metni bir metin editörüne yapıştır.
2.  `git clone` kısmındaki URL'yi kendi GitHub linkinle değiştir.
3.  Eğer ekran görüntüsü aldıysan (az önce bana attığın gibi), onları bir klasöre koy ve `Running Screen` linklerini o resimlerin yollarıyla değiştir. Resim yoksa o kısmı silebilirsin.



