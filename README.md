# 🌐 IoT-SmarTerm-Analytics

[![Arduino](https://img.shields.io/badge/Hardware-Arduino-00979D?style=flat-for-the-badge&logo=arduino&logoColor=white)](https://www.arduino.cc/)
[![Python](https://img.shields.io/badge/Software-Python%203.x-3776AB?style=flat-for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-for-the-badge)](https://opensource.org/licenses/MIT)

---

## 🌍 Language / Dil
Select your preferred language / İstediğiniz dili seçin:
* [🇹🇷 Türkçe](#-türkçe-dokümantasyon)
* [🇺🇸 English](#-english-documentation)

---

# `TR` Türkçe Dokümantasyon

**IoT-SmarTerm-Analytics**, ortamdaki sıcaklık ve nem verilerini donanım katmanından (Arduino Uno & DHT11) anlık olarak toplayan, I2C destekli bir LCD ekran üzerinde lokal olarak gösteren ve aynı zamanda Seri Port (UART) üzerinden bilgisayara aktararak Python ortamında gerçek zamanlı istatistiksel analiz (Ortalama, Medyan, Standart Sapma) ve dinamik grafik görselleştirmesi sunan uçtan uca bir IoT (Nesnelerin İnterneti) projesidir.

## 📌 Özellikler
* **Gerçek Zamanlı Veri Toplama:** DHT11 sensörü aracılığıyla her 2 saniyede bir kararlı sıcaklık ve nem verisi okunur.
* **Lokal Donanım Göstergesi:** Veriler, adres tarama özellikli gelişmiş `hd44780` kütüphanesi kullanılarak 16x2 I2C LCD ekranda anlık güncellenir.
* **Hata Yönetimi (Fault Tolerance):** Sensör bağlantı kopmaları veya okuma hatalarında sistem donmaz; LCD ekran üzerinde uyarı verilir ve Python tarafının çökmesini engellemek adına güvenli varsayılan veri (`0,0`) iletilir.
* **Seri Haberleşme Hattı:** Veriler veri paketleri halinde (`Sıcaklık,Nem`) yapılandırılarak 9600 Baud hızında Python terminaline akar.
* **Canlı Analitik ve Görselleştirme:** Python (`matplotlib`) interaktif modu yardımıyla grafik ekranı donmadan, her 10 veri örneğinde bir (pencereli akış modelinde) güncellenir.
* **İleri Düzey İstatistiksel Hesaplamalar:** `numpy` kütüphanesi entegrasyonuyla her veri paket grubu için anlık **Ortalama**, **Medyan (Ortanca)** ve **Standart Sapma** değerleri hesaplanır ve grafik üzerinde dinamik metin kutularında gösterilir.

## 🛠️ Donanım Mimarisi ve Bağlantı Şeması
### Gerekli Bileşenler
1. Arduino Uno (ATmega328P)
2. DHT11 Sıcaklık ve Nem Sensörü
3. 16x2 LCD Ekran (I2C Genişletici / Backpack Modülü ile)
4. Jumper Kablolar ve Breadboard

### Fiziksel Bağlantı Tablosu (Pinout)
| Bileşen | Modül Pini | Arduino Pini | Açıklama |
| :--- | :--- | :--- | :--- |
| **DHT11** | VCC | 5V | Güç Beslemesi |
| **DHT11** | GND | GND | Toprak Hattı |
| **DHT11** | DATA | Pin 2 | Dijital Veri Hattı |
| **I2C LCD** | VCC | 5V | Güç Beslemesi (+ Hattı) |
| **I2C LCD** | GND | GND | Toprak Hattı (- Hattı) |
| **I2C LCD** | SDA | A4 (SDA) | I2C Seri Veri Hattı |
| **I2C LCD** | SCL | A5 (SCL) | I2C Seri Saat Hattı |

## 📂 Depo (Repository) Klasör Yapısı
```text
IoT-SmarTerm-Analytics/
│
├── sicaklik_verisi/
│   ├── sicaklik_verisi.ino        # Gömülü sistem Arduino C++ kodu
│   └── circuit.jpg                # Devre şeması ve bağlantı görseli
│
├── sicaklik_verisi_python/
│   └── dht_oku.py                 # Veri analitiği ve görselleştirme Python kodu
│
└── README.md                      # Proje ana dökümantasyonu
```

## 💻 Kurulum ve Çalıştırma Adımları
**Sistemin kararlı çalışabilmesi için çalıştırma sırası oldukça önemlidir. Lütfen aşağıdaki adımları sırasıyla takip ediniz 🚀:**

 **1. Önemli Aşama:** Gömülü Yazılımın Yüklenmesi (C++)
  * Sistem başlatılmadan önce ilk olarak donanım yazılımının Arduino Uno'ya yüklenmiş olması gerekir.

   * Arduino IDE üzerinden Kütüphane Yöneticisi yardımıyla DHT sensor library ve hd44780 kütüphanelerini kurun.

  * Depodaki sicaklik_verisi/sicaklik_verisi.ino dosyasını açarak Arduino Uno kartınıza yükleyin.

 * Yükleme tamamlandıktan sonra LCD ekranda sıcaklık ve nem verilerinin lokal olarak basılmaya başladığını doğrulayın.

 **2. Aşama:** Python Ortamının Hazırlanması ve Çalıştırılması
* C++ kodu başarıyla yüklenip donanım veri üretmeye başladıktan sonra Python arayüzü tetiklenmelidir.

* Python bağımlılıklarını terminale aşağıdaki komutu yazarak yükleyin:
```text
 pip install pyserial matplotlib numpy
```

* sicaklik_verisi_python/dht_oku.py dosyası içerisindeki 'COM3' port bilgisini, Arduino kartınızın bilgisayarınızda bağlı olduğu port numarasıyla (Örn: COM4, /dev/ttyUSB0) güncelleyin.

* Son adım olarak terminalden Python betiğini çalıştırın:
```text
python sicaklik_verisi_python/dht_oku.py
```

* Ekranda anlık olarak güncellenen canlı grafik ve analitik veriler belirecektir.

📊 **Örnek Analiz Çıktıları**
Sistem veri toplamaya başladığında oluşturulan grafik ekranı üzerinde şu veriler anlık analiz edilir:

* **Ortalama (Average):** Ortam sıcaklık ve neminin genel eğilimini gösterir.

* **Medyan (Median):** Anlık hatalı okumaların (gürültülerin) analizi saptırmasını engeller.

* **Standart Sapma (Standard Deviation):** Ortam şartlarının ne kadar kararlı olduğunu veya ne kadar dalgalandığını gösterir.

📄 **Lisans**
Bu proje MIT Lisansı altında lisanslanmıştır.

# `EN` English Documentation

**IoT-SmarTerm-Analytics** is an end-to-end IoT (Internet of Things) project that collects real-time temperature and humidity data from the hardware layer (Arduino Uno & DHT11), displays it locally on an I2C-supported LCD screen, and simultaneously transmits it to a computer via Serial Port (UART) to provide real-time statistical analysis (Mean, Median, Standard Deviation) and dynamic graph visualization in a Python environment.

## 📌 Features
* **Real-Time Data Collection:** Stable temperature and humidity data are read every 2 seconds via the DHT11 sensor.
* **Local Hardware Display:** Data is updated instantly on a 16x2 I2C LCD screen using the advanced `hd44780` library with address auto-scanning capabilities.
* **Fault Tolerance:** The system does not freeze during sensor disconnections or read errors; a warning is displayed on the LCD screen, and safe default data (`0,0`) is transmitted to prevent the Python side from crashing.
* **Serial Communication Pipeline:** Data is structured into data packets (`Temperature,Humidity`) and streams to the Python terminal at a 9600 Baud rate.
* **Live Analytics & Visualization:** Using Python (`matplotlib`) interactive mode, the graph screen updates every 10 data samples (in a windowed streaming model) without freezing the UI.
* **Advanced Statistical Calculations:** Integrated with the `numpy` library, real-time **Mean**, **Median**, and **Standard Deviation** values are calculated for each data packet group and displayed in dynamic text boxes on the graph.

## 🛠️ Hardware Architecture and Pinout Diagram
### Required Components
1. Arduino Uno (ATmega328P)
2. DHT11 Temperature and Humidity Sensor
3. 16x2 LCD Display (with I2C Explorer / Backpack Module)
4. Jumper Wires and Breadboard

### Physical Connection Table (Pinout)
| Component | Module Pin | Arduino Pin | Description |
| :--- | :--- | :--- | :--- |
| **DHT11** | VCC | 5V | Power Supply |
| **DHT11** | GND | GND | Ground |
| **DHT11** | DATA | Pin 2 | Digital Data Line |
| **I2C LCD** | VCC | 5V | Power Supply (+ Line) |
| **I2C LCD** | GND | GND | Ground (- Line) |
| **I2C LCD** | SDA | A4 (SDA) | I2C Serial Data Line |
| **I2C LCD** | SCL | A5 (SCL) | I2C Serial Clock Line |

## 📂 Repository Structure
```text
IoT-SmarTerm-Analytics/
│
├── sicaklik_verisi/
│   ├── sicaklik_verisi.ino        # Embedded system Arduino C++ code
│   └── circuit.jpg                # Circuit diagram and connection visual
│
├── sicaklik_verisi_python/
│   └── dht_oku.py                 # Data analytics and visualization Python code
│
└── README.md                      # Main project documentation
```

## 💻 Installation and Execution Steps
**The execution order is critical for the system to operate stably. Please follow the steps below sequentially 🚀:**

**Step 1: Flashing the Firmware (C++)**
* Before starting the system, the firmware must first be uploaded to the Arduino Uno.
* Install the **DHT sensor library** and **hd44780** libraries via the Library Manager in the Arduino IDE.
* Open the `sicaklik_verisi/sicaklik_verisi.ino` file in the repository and upload it to your Arduino Uno board.
* Once the upload is complete, verify that the temperature and humidity data are being printed locally on the LCD screen.

**Step 2: Preparing and Running the Python Environment**
* The Python interface should be triggered only after the C++ code is successfully uploaded and the hardware begins generating data.
* Install the Python dependencies by running the following command in your terminal:
  
```text
pip install pyserial matplotlib numpy
```
* Update the `'COM3'` port information inside the `sicaklik_verisi_python/dht_oku.py` file with the actual port number your Arduino board is connected to (e.g., `COM4`, `/dev/ttyUSB0`).

* As the final step, run the Python script from the terminal:
```text
python sicaklik_verisi_python/dht_oku.py
```
* A live graph and real-time analytical data updating instantly will appear on the screen.

📊 **Sample Analysis Outputs**
When the system starts collecting data, the following metrics are analyzed in real time on the generated graph screen:

* **Mean (Average):** Shows the general trend of ambient temperature and humidity.
* **Median:** Prevents momentary faulty readings (noise) from skewing the statistical analysis.
* **Standard Deviation:** Indicates how stable or fluctuating the environmental conditions are.

📄 **License**
This project is licensed under the MIT License.

