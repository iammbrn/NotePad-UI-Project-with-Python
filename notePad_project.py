import sys #Komut satırı argümanlarını almak için dahil edildi.

import os #Dosya işlemeleri için dahil edildi.

from PyQt5.QtWidgets import QWidget, QApplication, QTextEdit, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit, \
    QFileDialog # arayüz penceresi olşturmak ve özellikler eklemek için dahil edildiler.

from PyQt5.QtWidgets import QMainWindow, QAction, qApp #Arayüz ana penceresi için dahil edildi.


class NotePad(QWidget): #NotePad sınıfına inheritance ile Qwidget sınıfı davranış ve özellikleri miras alındı.

    def __init__(self):

        super().__init__() # QWidget sınıfı özellikleri NotePad() sınıfına dahil edildi.

        self.init_ui()

    def init_ui(self):

        self.write_area = QTextEdit()
        self.clean_button = QPushButton("Temizle")
        self.register_button = QPushButton("Kaydet")
        self.source_open_button = QPushButton("Dosya Aç")

        v_box = QVBoxLayout()
        v_box.addWidget(self.write_area)
        h_box = QHBoxLayout()
        h_box.addWidget(self.clean_button)
        h_box.addWidget(self.register_button)
        h_box.addWidget(self.source_open_button)

        v_box.addLayout(h_box)

        self.setLayout(v_box)

        self.setGeometry(100, 100, 640, 480)
        self.setWindowTitle("NotePad")

        self.clean_button.clicked.connect(self.clean_file)
        self.register_button.clicked.connect(self.register_file)
        self.source_open_button.clicked.connect(self.open_file)

    def clean_file(self):

        self.write_area.setText("")

    def register_file(self):
        #Burada verilen dizin üzerinde iletişim kutusu açılarak,
        # kullanıcının dosya ismi ve yolu belirleyip dosyayı kaydetmesi sağlanır.
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Source", os.getenv("HOME")) 

        # kullanıcı işlemi iptal ederse dosya ismi yerine NONE değer döner, dosya ismi olmadığı için dosya işlemleri gerçekleşmez, bu durum işlem yapmayı gerektirmez.
        if file_name:  # Burada if ile kontrol edilerek programın çökmesi engellenir.
            with open(file_name, "w", encoding="utf-8") as file1:
                file1.write(self.write_area.toPlainText())
                # toPlainText ile kullanıcının girdiği tüm metin alınır.
                # file1.write ile alınan metin dosyaya yazılır.

    def open_file(self):
        # Burada verilen dizin üzerinde iletişim kutusu açılarak,
        # kullanıcının dosya seçmesi, seçtiği dosyayı açması sağlanır.
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Source",os.getenv("HOME"))  # HOME yerine Desktop' da kullanılabilir.
        if file_name:
            with open(file_name, "r", encoding="utf-8") as file:
                self.write_area.setText(file.read())
                # seçilen dosya üzerindeki tüm metin okunarak self.write_area değişkenine yazılır.


class Menu(QMainWindow):

    def __init__(self):

        super().__init__()

        self.window = NotePad() # NotePad() sınıfından bir nesne oluşturuldu.

        self.setCentralWidget(self.window) #self.window nesnesi ana pencerenin merkezine alındı.

        self.setWindowTitle("Metin Editörü")

        self.create_menues()

    def create_menues(self):

        menubar = self.menuBar() #menubar oluşturduk.

        file = menubar.addMenu("Dosya") # menubara menüler ekkledik.

        edit = menubar.addMenu("Düzenle")

        exit = QAction("Çıkış Yap", self) #actionlar(eylemler) oluşturduk.
        exit.setShortcut("Ctrl+Q")        #actionlarımıza kısayol ekledik.

        open_file = QAction("Dosya Aç", self)
        open_file.setShortcut("Ctrl+O")

        save_file = QAction("Dosya Kaydet", self)
        save_file.setShortcut("Ctrl+S")

        clean = QAction("Temizle", self)
        clean.setShortcut("Ctrl+D")

        file.addAction(open_file) #actionları menubar üzerindeki menulere ekledik.
        file.addAction(save_file)
        file.addAction(exit)

        edit.addAction(clean)

        file.triggered.connect(self.response) # file menusu üzerindeki eylemlere tıklandığında connect ile yaplıcak işleve bağladık.
        edit.triggered.connect(self.clean)

        self.show()


    def clean(self, action):
        if action.text() == "Temizle":
            self.window.clean_file() #NotePad() nesnesi kullanılarak NotePad() fonksiyonlarına erişilip, fonksiyonlar kullanıldı.

    def response(self, action):

        if action.text() == "Dosya Aç":
            self.window.open_file()

        elif action.text() == "Dosya Kaydet":
            self.window.register_file()

        elif action.text() == "Çıkış Yap":
            qApp.quit() # qApp te bulunan özel bir fonksiyon ile programımızı sonlandırdık.


app = QApplication(sys.argv) #uygulama objesi oluşturuldu.

menu = Menu() #Menu sınıfından bir nesne oluşturuldu.

sys.exit(app.exec_()) # pencere döngüye alınarak açık kalması sağlandı.
