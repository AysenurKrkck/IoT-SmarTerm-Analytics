#include <Wire.h>                          // TR: I2C haberleşmesini sağlayan standart Arduino kütüphanesi.
                                           // EN: Standard Arduino library that enables I2C communication.

#include <hd44780.h>                       // TR: Gelişmiş LCD ekran kontrolü sağlayan ana kütüphane.
                                           // EN: Main library providing advanced LCD screen control.

#include <hd44780ioClass/hd44780_I2Cexp.h> // TR: I2C genişletici kartı (backpack) ile LCD ekranı sürmek için gerekli alt modül.
                                           // EN: Submodule required to drive the LCD screen with the I2C expander board.

#include <DHT.h>                           // TR: DHT sıcaklık ve nem sensörü kütüphanesi.
                                           // EN: DHT temperature and humidity sensor library.

#define DHTPIN 2                           // TR: DHT11 sensörünün bağlı olduğu dijital pini (Pin 2) tanımlar.
                                           // EN: Defines the digital pin (Pin 2) where the DHT11 sensor is connected.

#define DHTTYPE DHT11                      // TR: Kullanılan sensör modelinin DHT11 olduğunu belirtir.
                                           // EN: Specifies that the sensor model being used is DHT11.

hd44780_I2Cexp lcd;                        // TR: I2C adresini otomatik tarayıp bulabilen LCD nesnesi oluşturur.
                                           // EN: Creates an LCD object that can automatically scan and find the I2C address.

DHT dht(DHTPIN, DHTTYPE);                  // TR: Belirlenen pin ve tip ayarlarıyla DHT nesnesini başlatır.
                                           // EN: Initializes the DHT object with the specified pin and type settings.

int sicaklik = 0;                          // TR: Okunan sıcaklık değerini tutacak tam sayı değişkeni.
                                           // EN: Integer variable to hold the read temperature value.

int nem = 0;                               // TR: Okunan nem değerini tutacak tam sayı değişkeni.
                                           // EN: Integer variable to hold the read humidity value.

String veri;                               // TR: Python tarafına gönderilecek olan virgülle ayrılmış metin yapısı.
                                           // EN: String structure to be sent to the Python side as comma-separated values.

void setup() {
  Serial.begin(9600);                      // TR: Seri haberleşmeyi 9600 baud hızında başlatır.
                                           // EN: Starts serial communication at 9600 baud rate.
  
  dht.begin();                             // TR: DHT sensörünü veri okumaya hazır hale getirir.
                                           // EN: Initializes the DHT sensor for reading data.
  
  // TR: LCD ekranı 16 sütun ve 2 satır olarak başlatır. Hata durumunda sıfırdan farklı bir durum kodu döndürür.
  // EN: Initializes the LCD screen as 16 columns and 2 rows. Returns a non-zero error code if initialization fails.
  int durum = lcd.begin(16, 2);
  if(durum) {
    Serial.println("LCD baslatilamadi!");  // TR: Eğer ekran donanımsal olarak başlatılamazsa seri porttan hata bildirir.
                                           // EN: Logs an error to the serial port if the screen fails to initialize hardware-wise.
  }
  
  lcd.backlight();                         // TR: LCD ekranın arka ışığını (mavi/yeşil aydınlatma) açar.
                                           // EN: Turns on the LCD screen backlight.
}

void loop() {
  nem = dht.readHumidity();                // TR: Sensörden nem oranını okur ve değişkene atar.
                                           // EN: Reads humidity ratio from the sensor and assigns it to the variable.
  
  sicaklik = dht.readTemperature();        // TR: Sensörden sıcaklık değerini okur ve değişkene atar.
                                           // EN: Reads temperature value from the sensor and assigns it to the variable.

  // TR: Sensör verilerinde okuma hatası (bağlantı kopması vs.) olup olmadığını kontrol eder.
  // EN: Checks if there is a reading error (disconnection, etc.) in sensor data.
  if (isnan(nem) || isnan(sicaklik)) {
    Serial.println("0,0");                 // TR: Hata durumunda Python tarafında split çökmesi olmasın diye varsayılan olarak "0,0" gönderir.
                                           // EN: Sends "0,0" by default to prevent a split crash on the Python side in case of error.
    
    // TR: Ekranı temizler ve kullanıcıya sensör hatası olduğunu gösterir.
    // EN: Clears the screen and displays a sensor error to the user.
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Sensor Hatasi!");
    
    delay(2000);                           // TR: 2 saniye bekler.
                                           // EN: Waits for 2 seconds.
    return;                                // TR: Döngünün kalanını çalıştırmadan en başa geri döner.
                                           // EN: Returns to the beginning without executing the rest of the loop.
  }

  // TR: Sıcaklık ve nem değerlerini Python'daki split(',') fonksiyonunun beklediği gibi virgülle birleştirir (Örn: "29,64").
  // EN: Joins temperature and humidity values with a comma as expected by Python's split(',') function (e.g., "29,64").
  veri = String(sicaklik) + "," + String(nem);
  Serial.println(veri);                    // TR: Virgüllü satırı seri port üzerinden satır sonu karakteriyle Python'a iletir.
                                           // EN: Transmits the comma-separated line to Python over the serial port with a newline.

  // --- LCD Ekran Güncelleme Bölümü / LCD Screen Update Section ---
  lcd.clear();                             // TR: Ekrandaki eski yazıları temizler.
                                           // EN: Clears previous text on the screen.
  
  // TR: İmleci ilk satırın başına (0. sütun, 0. satır) getirir ve Sıcaklık değerini yazdırır.
  // EN: Moves cursor to the beginning of the first line (column 0, row 0) and prints Temperature value.
  lcd.setCursor(0, 0); 
  lcd.print("Sicaklik: ");
  lcd.print(sicaklik);
  lcd.print("C");

  // TR: İmleci ikinci satırın başına (0. sütun, 1. satır) getirir ve Nem değerini yazdırır.
  // EN: Moves cursor to the beginning of the second line (column 0, row 1) and prints Humidity value.
  lcd.setCursor(0, 1); 
  lcd.print("Nem: %");
  lcd.print(nem);

  delay(2000);                             // TR: DHT11'in kararlı veri üretebilmesi için döngü sonunda 2 saniye bekler.
                                           // EN: Waits 2 seconds at the end of the loop for the DHT11 to generate stable data.
}
