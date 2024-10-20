# Project Title

Here is the setup image for this project:

![Setup](setup.png)



Python Skript für das ReViCat Projekt. Die Beschreibung von dem Skripten liegen im "A4 CE-Bericht_ReViCaT Projektdoku.docx"

Prerequisites: • opencv (und deren Abhängigkeiten) -> Videodatenaufnahme (Streaming, Recording, Bilder machen und verarbeiten). • gstreamer (und deren Abhängigkeiten) -> Übertragung der Videodaten – Streaming Pipeline erstellen. • ufw – Konfiguration des Firewalls. • picamera2 – Konfiguration der Pi-Kamera. • paho-mqtt – Konfiguration der MQTT-Schnittstellen. • lsof – Überprüfen der bertragene Ports. • pyModbusTCP – Konfiguration der TCP-Modbus-Schnittstellen. ...

5.3 Pi-Server (Pi 1)

5.3.1 Überblick Das Pi an der Serverseite hat folgende Aufgaben: Streaming Video: • Festlegung des UDP-Ports und Konfiguration als UDP-Server. • Videodatenaufnahme mit bestimmter Konfiguration (640x480 und RGB888 als Farbformat. Bei anderen Farbformat kann es passieren, dass diese auf dem HMI-Gerät falsch angezeigt werden). • Enkodierung der Videodaten im H.264-Format. • Erstellung einer Übertragungspipeline über den eingestellten UDP-Port und Senden der Videodaten. Streaming Metadaten: • Konfiguration der MQTT-Schnittstellen für die Übertragung von Metadaten (Festlegung als MQTT-Subscriber und Abonnierung des Brokers mit der eingestellten IP-Adresse des zweiten Pis, Konfiguration der zu abonnierenden MQTT-Topics). • Generierung zufälliger Daten für Geschwindigkeit, Distanz und die Koordinaten der Bounding Boxen [x1, y1, x2, y2], wobei x1, y1 die linke obere und x2, y2 die rechte untere Koordinate der Bounding Box darstellen. Die Parameter x1 und x2 liegen im Bereich von 0 bis 1280, sowie y1 und y2 im Bereich von 0 bis 960. Die Daten der Bounding Boxen werden als Array von JSON-Elementen gespeichert und an den Broker verschickt. Die Geschwindigkeits- und Distanzdaten sollten so generiert werden, dass sie die Form „xxx,x“ behalten, also eine Kommazahl mit einer Nachkommastelle. • Übertragung der Metadaten über MQTT an den Broker.

5.3.2 Implementierung

Für die Implementierung wurden drei Python-Skripte genutzt, welche im SharePoint unter dem Speicherort „D:\Projekte-SVNĸ08-ReViCaT runk\Python_Script\pi_server\“ abgelegt wurden: • Metadatas_MQTT_Subscriber.py – Streaming von Metadaten • Videodatas_UDP_Sender.py.py – Streaming von Videodaten • main.py – Startet beide Skripte gleichzeitig

Diese Skripte wurden auf dem ersten Pi erstellt, der mit einer Kamera verbunden ist. Der Projektbaum sieht wie folgt aus: home |_ admin |_Desktop |_Metadatas_MQTT_Subscriber.py |_Videodatas_UDP_Sender.py |_main.py Falls die Skripte in einem anderen Verzeichnis des Projekts gespeichert werden, muss der Pfad zu den Dateien in der main_2.py-Datei entsprechend angepasst werden.

5.4 Pi-Client (Pi 2)

5.4.1 Überblick

Das Pi an der Clientseite erfüllt folgenden Aufgaben:

Empfängt die Videodaten und streamt weiter an das HMI-Gerät: • Konfiguriert die UDP-Schnittstellen zur Videoübertragung, wobei das System gleichzeitig als Empfänger fungiert, um die Videodaten vom ersten Pi zu erhalten, und als Sender, um die Videodaten an das HMI-Gerät weiterzuleiten. Wichtig hierbei ist, dass der Empfänger- und der Sender-Port unterschiedlich sein müssen. • Empfängt Videodaten über eine GStreamer-Pipeline, enkodiert sie im H.264-Format und sendet sie weiter über einen konfigurierten UDP-Port.

Empfängt und bearbeitet die Metadaten über MQTT und sende diese über TCP-Modbus an das HMI-Gerät: • Konfiguriert das Pi als MQTT-Broker mit der IP-Adresse des zweiten Pis und den entsprechenden abonnierten Topics. • Konfiguriert das Pi als TCP-Modbus-Server, der Daten an den TCP-Modbus-Client (HMI-Gerät) überträgt. • Empfängt Nachrichten von MQTT-Subscriber mit den entsprechenden MQTT-Topics. • Verarbeitet die Daten durch Skalierung der empfangenen Daten (dieser Schritt sollte eigentlich auf der HMI-Seite durchgeführt werden): o Die Bounding Box-Werte werden skaliert, indem sie mit dem entsprechenden Skalierungsfaktor multipliziert werden. Anschließend werden sie in Integerwerte konvertiert. x_Skalierungsfaktor = (StreamingVideoWidget_x) / (Videoauflösung_x) y_Skalierungsfaktor = (StreamingVideoWidget_y) / (Videoauflösung_y)) • Überträgt die Daten über Modbus-TCP an das HMI-Gerät mit vordefinierten Registernummern (0: Geschwindigkeit, 1: Distanz, 2-21: Bounding Box-Koordinaten, nur 20 Register für die Bounding Boxen, da laut Informationen der Kamera maximal 5 Personen erkannt werden können).

5.4.2 Implementierung

Für die Implementierung wurden drei Python-Skripte genutzt, welche im SharePoint unter dem Speicherort „D:\Projekte-SVNĸ08-ReViCaT runk\Python_Script\pi_hmi\modbusTCP\“ abgelegt wurden: • Metadatas_MQTT_Broker_ModbusTCP.py – Streaming von Metadaten • Videodatas_UDP_Receiver.py – Streaming von Videodaten • main.py – Startet beide Skripte gleichzeitig

Diese Skripte wurden auf dem zweiten Pi erstellt, der mit einer Kamera verbunden ist. Der Projektbaum sieht wie folgt aus: home |_ admin |_Desktop |_Metadatas_MQTT_Broker_ModbusTCP.py |_Videodatas_UDP_Receiver.py |_main.py Falls die Skripte in einem anderen Verzeichnis des Projekts gespeichert werden, muss der Pfad zu den Dateien in der main.py-Datei entsprechend angepasst werden.
