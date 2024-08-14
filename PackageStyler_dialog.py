import os
import json
from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QFileDialog, QListWidgetItem
from qgis.core import QgsProject, Qgis

# Load the UI file
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'PackageStyler_dialog_base.ui'))

class PackageStylerDialog(QDialog, FORM_CLASS):
    def __init__(self, iface, parent=None):
        super(PackageStylerDialog, self).__init__(parent)
        self.setupUi(self)
        self.iface = iface
        self.configGroupBox.setVisible(False)  # Initially hide the configuration group box
        self.browseButton.clicked.connect(self.browse)
        self.configureButton.clicked.connect(self.show_configuration)
        self.addButton.clicked.connect(self.add_configuration)
        self.removeButton.clicked.connect(self.remove_configuration)
        self.saveConfigButton.clicked.connect(self.save_configuration)
        self.runButton.clicked.connect(self.run)
        self.saveLayerButton.clicked.connect(self.save_layer_styles)

        # List to store configurations
        self.configurations = []

        # Load saved configurations
        self.load_configurations()

    def show_configuration(self):
        self.configGroupBox.setVisible(True)
        self.configureButton.setVisible(False)
        self.runButton.setVisible(False)
        self.saveLayerButton.setVisible(False)

    def add_configuration(self):
        keyword = self.keywordLineEdit.text()
        qml_path = self.qmlPathLineEdit.text()
        if keyword and qml_path:
            config_item = f"{keyword}: {qml_path}"
            self.configListWidget.addItem(config_item)
            self.configurations.append((keyword, qml_path))
            self.keywordLineEdit.clear()
            self.qmlPathLineEdit.clear()

    def remove_configuration(self):
        selected_items = self.configListWidget.selectedItems()
        if not selected_items:
            return
        for item in selected_items:
            index = self.configListWidget.row(item)
            self.configListWidget.takeItem(index)
            self.configurations.pop(index)

    def save_configuration(self):
        self.configGroupBox.setVisible(False)
        self.configureButton.setVisible(True)
        self.runButton.setVisible(True)
        self.saveLayerButton.setVisible(True)
        self.save_configurations()

    def browse(self):
        qml_file, _ = QFileDialog.getOpenFileName(self, "Select QML file", "", "QML files (*.qml)")
        self.qmlPathLineEdit.setText(qml_file)

    def get_configurations(self):
        return self.configurations

    def run(self):
        self.accept()

    def save_layer_styles(self):
        layers = QgsProject.instance().mapLayers().values()
        for layer in layers:
            if layer.type() == layer.VectorLayer:
                qml_path = os.path.join(os.path.dirname(layer.dataProvider().dataSourceUri()), f"{layer.name()}.qml")
                layer.saveNamedStyle(qml_path)
                layer.saveStyleToDatabase(layer.name(), "", True, "")
        self.iface.messageBar().pushMessage("Success", "Layer styles saved to database", level=Qgis.Info)

    def save_configurations(self):
        config_file = os.path.join(os.path.dirname(__file__), 'configurations.json')
        with open(config_file, 'w') as f:
            json.dump(self.configurations, f)

    def load_configurations(self):
        config_file = os.path.join(os.path.dirname(__file__), 'configurations.json')
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                self.configurations = json.load(f)
                for keyword, qml_path in self.configurations:
                    config_item = f"{keyword}: {qml_path}"
                    self.configListWidget.addItem(config_item)
