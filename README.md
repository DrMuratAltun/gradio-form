# 📋 Gradio Kayıt ve Veri Yönetim Paneli

Bu proje, yerel bir `form.csv` dosyasına yeni kayıtlar eklemek ve mevcut kayıt listesini anlık olarak takip etmek için geliştirilmiş modern ve premium tasarıma sahip bir Gradio Blocks uygulamasıdır.

## 🚀 Özellikler

* **Sekmeli (Tabs) Modern Tasarım**:
  * **Sekme 1 (Yeni Kayıt Ekle)**: Ad, Soyad, E-posta, Yaş, Cinsiyet, Bölüm ve İş Durumu bilgilerinin doğrulama kurallarıyla girilebildiği form.
  * **Sekme 2 (Mevcut Kayıtlar)**: `form.csv` dosyasından okunan ve anlık olarak güncellenen veri tablosu (`gr.Dataframe`) ile listeyi manuel yenileme butonu.
* **Veri Doğrulaması**: Gerekli tüm form alanları için boş bırakılamaz kuralları, geçerli e-posta biçimi ve yaş sınırı doğrulamaları.
* **Türkçe Karakter Uyumlu**: Dosya okuma ve yazma işlemlerinde UTF-8 standartlarına tam uyumluluk.
* **Global Paylaşım (share=True)**: Dış ağlardan da erişim sağlanabilmesi için Gradio üzerinden geçici genel paylaşım linki oluşturma desteği.

---

## 🛠️ Kurulum ve Çalıştırma

### 1. Depoyu Klonlayın
```bash
git clone https://github.com/DrMuratAltun/gradio-form.git
cd gradio-form
```

### 2. Sanal Ortam Oluşturun ve Aktifleştirin
```bash
python3 -m venv .venv
source .venv/bin/activate  # macOS/Linux için
# veya
.venv\Scripts\activate     # Windows için
```

### 3. Bağımlılıkları Yükleyin
```bash
pip install -r requirements.txt
```

### 4. Uygulamayı Başlatın
```bash
python app.py
```

Uygulama başarıyla başlatıldığında yerel olarak `http://localhost:7860` adresinden veya terminale yansıyan global `.gradio.live` linki üzerinden erişilebilir hale gelecektir.
