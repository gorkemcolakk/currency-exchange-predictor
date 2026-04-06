# 📈 GOBA INVEST - Profesyonel Döviz Analiz ve Tahmin Platformu

<div align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white" />
  <img src="https://img.shields.io/badge/Prophet-008080?style=for-the-badge&logo=meta&logoColor=white" />
  <img src="https://img.shields.io/badge/Yahoo_Finance-7B0099?style=for-the-badge&logo=yahoo&logoColor=white" />
</div>

---

## 🚀 Proje Hakkında

**GOBA INVEST**, döviz piyasalarını yapay zeka ile analiz eden, anlık veriler sunan ve geleceğe yönelik projeksiyonlar hazırlayan yeni nesil bir finansal analiz platformudur. Geleneksel yöntemlerin aksine, Meta'nın geliştirdiği **Prophet** kütüphanesini kullanarak 2 yıla kadar uzanan isabetli tahminler üretir.

### ✨ Temel Özellikler

- 🤖 **Yapay Zeka Destekli Tahmin:** Facebook (Meta) Prophet algoritmaları ile 1 haftadan 2 yıla kadar döviz ve emtia projeksiyonları.
- ⚡ **10 Saniyelik Veri Güncelleme:** Yahoo Finance API üzerinden her 10 saniyede bir güncellenen canlı piyasa verileri.
- 📊 **İnteraktif Grafikler:** Plotly kütüphanesi kullanılarak oluşturulan, teknik analiz odaklı interaktif grafik arayüzü.
- 💱 **Hızlı Döviz Çevirici:** Anlık kurlar üzerinden hesaplama yapan, kullanıcı dostu döviz çevirici.
- 🌗 **Karanlık/Aydınlık Tema:** Göz yormayan, premium "Glassmorphism" tasarımı ve tema desteği.
- 🌐 **Çoklu Dil Desteği:** Türkçe ve İngilizce dil seçenekleri.
- 💹 **Geniş Ürün Yelpazesi:** USD, EUR, GBP, Ons Altın, Gümüş, Gram Altın ve türev altın ürünleri (Çeyrek, Yarım, Cumhuriyet vb.).

---

## 🛠️ Teknoloji Yığını

- **Backend:** Python / Flask
- **Veri & Analiz:** Pandas, Requests, yfinance
- **Yapay Zeka:** Facebook Prophet (Time Series Forecasting)
- **Frontend:** HTML5, Modern CSS (Glassmorphism), Vanilla JavaScript
- **Görselleştirme:** Plotly.js
- **İkonlar:** FontAwesome 6

---

## 📸 Ekran Görüntüleri

<div align="center">
  <img src="https://via.placeholder.com/800x450?text=Dashboard+Overview" alt="Dashboard" width="800">
  <p><em>Modern ve Kullanıcı Dostu Dashboard Arayüzü</em></p>
  <img src="https://via.placeholder.com/800x450?text=AI+Forecast+Charts" alt="Analytics" width="800">
  <p><em>Yapay Zeka Destekli Tahmin Grafikleri</em></p>
</div>

---

## ⚙️ Kurulum ve Çalıştırma

Projenizi yerel ortamınızda çalıştırmak için aşağıdaki adımları izleyin:

1. **Depoyu klonlayın:**
   ```bash
   git clone https://github.com/gorkemcolakk/currency-exchange-predictor.git
   cd currency-exchange-predictor
   ```

2. **Gerekli kütüphaneleri kurun:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Uygulamayı başlatın:**
   ```bash
   python app.py
   ```
   *Uygulama varsayılan olarak `http://127.0.0.1:5000` adresinde çalışacaktır.*

---

## 🧠 Nasıl Çalışır?

GOBA INVEST, Yahoo Finance üzerinden son 5 yıllık geçmiş verileri çeker. Bu veriler üzerinde:
1. **Veri Temizliği:** Eksik ve hatalı veriler Pandas ile optimize edilir.
2. **Model Eğitimi:** Prophet modeli; yıllık mevsimsellik, Türkiye tatil takvimi ve trend değişim noktaları (changepoints) hesaba katılarak eğitilir.
3. **Tahmin:** Eğitilen model, gelecek 730 gün için tahmin aralıklarını (yhat, yhat_lower, yhat_upper) hesaplar.
4. **Görselleştirme:** Elde edilen veriler Plotly ile kullanıcıya interaktif bir şekilde sunulur.

---

## 📄 Lisans

Bu proje MIT Lisansı ile lisanslanmıştır. Daha fazla bilgi için `LICENSE` dosyasına göz atabilirsiniz.

---

## 📧 İletişim

**Eren Görkem Çolak** - [GitHub](https://github.com/gorkemcolakk) - [LinkedIn](https://linkedin.com/in/gorkemcolakk)

*"Finansal geleceğinizi yapay zeka ile öngörün."*
