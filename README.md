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
