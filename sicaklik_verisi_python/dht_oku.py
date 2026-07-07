import serial               # TR: Seri port haberleşmesi için gerekli kütüphane.
                            # EN: Library required for serial port communication.

import matplotlib.pyplot as plt  # TR: Grafik çizimi ve görselleştirme için kullanılan kütüphane.
                                 # EN: Library used for data plotting and visualization.

import numpy as np          # TR: Matematiksel ve istatistiksel işlemler (ortalama, medyan, std) için kullanılan kütüphane.
                            # EN: Library used for mathematical and statistical operations (mean, median, std).

# TR: Grafik ekranının donmadan canlı olarak güncellenebilmesi için interaktif modu açar.
# EN: Enables interactive mode so the plot window updates dynamically without freezing.
plt.ion()

# TR: 'COM3' portundan 9600 baud hızında seri haberleşme bağlantısı başlatır.
# EN: Initializes the serial communication connection on 'COM3' port at 9600 baud rate.
ser = serial.Serial('COM3', 9600, timeout=1)

sicaklik = []               # TR: Sıcaklık verilerini biriktiren boş liste.
                            # EN: Empty list to accumulate temperature values.

nem = []                    # TR: Nem verilerini biriktiren boş liste.
                            # EN: Empty list to accumulate humidity values.

# TR: Grafik penceresini (fig) ve çizim eksenini (ax) oluşturur.
# EN: Creates the plot figure (fig) and axes (ax).
fig, ax = plt.subplots()

# TR: Sıcaklık (kırmızı) ve Nem (mavi) için boş çizgiler tanımlar ve etiketlerini belirler.
# EN: Defines empty line plots for Temperature (red) and Humidity (blue) with labels.
line1, = ax.plot([], [], label="Sicaklik", color="red")
line2, = ax.plot([], [], label="Nem", color="blue")
ax.legend()                 # TR: Grafik üzerine gösterge (lejant) kutusunu ekler.
                            # EN: Adds the legend box onto the plot.

# TR: Grafik eksen sınırlarını ve isimlendirmelerini yapılandırır.
# EN: Configures plot axis limits and labels.
ax.set_xlim(0, 10)          # TR: X eksenini 0 ile 10 örnek arasında sınırlandırır.
                            # EN: Limits the X-axis between 0 and 10 samples.
ax.set_ylim(0, 80)          # TR: Y eksenini değer boyutu olarak 0 ile 80 arasında sınırlandırır.
                            # EN: Limits the Y-axis value scale between 0 and 80.
ax.set_xlabel("Örnek Sayisi") # TR: X ekseninin adını belirler.
                            # EN: Sets the label for the X-axis.
ax.set_ylabel("Değerler")     # TR: Y ekseninin adını belirler.
                            # EN: Sets the label for the Y-axis.

# TR: Grafik ekranı üzerinde istatistiksel sonuçların yazılacağı yer tutucu metin alanlarını oluşturur.
# EN: Creates placeholder text areas on the plot window where statistical results will be displayed.
text_sicaklik = plt.text(0, 85, "Sicaklik_ortalama", fontsize=12, color='blue')
text_nem = plt.text(4, 85, "nem_ortalama", fontsize=12, color='blue')

text_sicaklik_medyan = plt.text(0, 81, "sicaklik_medyan", fontsize=12, color='red')
text_nem_medyan = plt.text(4, 81, "nem_medyan", fontsize=12, color='red')

text_sicaklik_std = plt.text(0, 89, "sicaklik_std", fontsize=12, color='black')
text_nem_std = plt.text(4, 89, "nem_std", fontsize=12, color='black')

while True:
    # TR: Seri port tamponunda okunmayı bekleyen veri olup olmadığını kontrol eder.
    # EN: Checks if there is any incoming data waiting to be read in the serial buffer.
    if ser.in_waiting > 0:      
        # TR: Gelen veriyi satır satır okur, metne çevirir ve sonundaki boşlukları temizler.
        # EN: Reads data line by line, decodes it into text, and strips trailing spaces.
        data = ser.readline().decode('utf-8').rstrip()
        print(f"Gelen veri: {data}") # TR: Ham veriyi terminale basar.
                                     # EN: Prints raw data to the terminal.

        try:
            # TR: Arduino'dan gelen virgüllü metni ikiye böler ve float tipine dönüştürür.
            # EN: Splits the comma-separated string from Arduino and converts parts to floats.
            deger1, deger2 = data.split(',')
            deger1 = float(deger1) 
            deger2 = float(deger2) 
            
            sicaklik.append(deger1) # TR: Sıcaklık değerini listeye ekler.
                                    # EN: Appends temperature value to the list.
            nem.append(deger2)      # TR: Nem değerini listeye ekler.
                                    # EN: Appends humidity value to the list.
            
            # TR: 10 adet veri örneği toplandığında hesaplama ve çizim aşamasına geçer.
            # EN: Once 10 data samples are collected, starts calculation and plotting.
            if len(sicaklik) == 10 and len(nem) == 10:
                print(sicaklik, nem)

                # TR: Sıcaklık ve nem listelerinin aritmetik ortalamasını hesaplar ve terminale yazar.
                # EN: Calculates the arithmetic average of temperature and humidity lists and prints to terminal.
                sicaklik_ort = np.average(sicaklik)
                nem_ort = np.average(nem)
                print("ORTALAMA: ", sicaklik_ort, nem_ort)

                # TR: Sıcaklık ve nem listelerinin medyan (ortanca) değerini hesaplar ve terminale yazar.
                # EN: Calculates the median value of temperature and humidity lists and prints to terminal.
                sicaklik_medyan = np.median(sicaklik)
                nem_medyan = np.median(nem)
                print("MEDYAN: ", sicaklik_medyan, nem_medyan)

                # TR: Sıcaklık ve nem listelerinin standart sapmasını hesaplar ve terminale yazar.
                # EN: Calculates the standard deviation of temperature and humidity lists and prints to terminal.
                sicaklik_std = np.std(sicaklik)
                nem_std = np.std(nem)
                print("STANDAART SAPMA: ", sicaklik_std, nem_std)

                # TR: Grafik penceresindeki ortalama metin alanlarını günceller.
                # EN: Updates the average text fields on the plot window.
                text_sicaklik.set_text(sicaklik_ort)
                text_nem.set_text(nem_ort)

                # TR: Grafik penceresindeki medyan metin alanlarını günceller.
                # EN: Updates the median text fields on the plot window.
                text_sicaklik_medyan.set_text(sicaklik_medyan)
                text_nem_medyan.set_text(nem_medyan)

                # TR: Grafik penceresindeki standart sapma metin alanlarını günceller.
                # EN: Updates the standard deviation text fields on the plot window.
                text_sicaklik_std.set_text(sicaklik_std)
                text_nem_std.set_text(nem_std)

                # TR: Çizgilerin X ve Y eksenindeki verilerini yeni listelerle günceller.
                # EN: Updates the X and Y data of the plot lines with new lists.
                line1.set_ydata(sicaklik)
                line1.set_xdata(range(len(sicaklik)))

                line2.set_ydata(nem)
                line2.set_xdata(range(len(nem)))

                # TR: Grafik penceresini yeni çizimlerle yeniler ve arayüzü günceller.
                # EN: Redraws the plot canvas with updated lines and flushes GUI events.
                fig.canvas.draw()
                fig.canvas.flush_events()

                plt.pause(0.1)      # TR: Grafik arayüzünün işlenmesi için programı kısa süreliğine duraklatır.
                                    # EN: Briefly pauses execution to allow the plot GUI to render.
                
                # TR: Sonraki 10'lu paket veri akışı için mevcut listeleri tamamen temizler.
                # EN: Clears the current lists to prepare for the next batch of 10 samples.
                sicaklik.clear()
                nem.clear()
                
        except ValueError:
            # TR: Hatalı veya eksik veri gelmesi durumunda programın çökmesini engeller, adımı atlar.
            # EN: Prevents the program from crashing if data is corrupted or incomplete; skips to next loop.
            continue