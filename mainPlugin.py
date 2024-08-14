import os
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction
from qgis.core import QgsProject
from .PackageStyler_dialog import PackageStylerDialog

class PackageStyler:
    def __init__(self, iface):
        self.iface = iface
        self.plugin_dir = os.path.dirname(__file__)
        self.action = None
        self.dialog = None

    def initGui(self):
        icon_path = os.path.join(self.plugin_dir, 'icon.png')
        self.action = QAction(QIcon(icon_path), "PackageStyler", self.iface.mainWindow())
        self.action.triggered.connect(self.run)
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu("&PackageStyler", self.action)

    def unload(self):
        self.iface.removeToolBarIcon(self.action)
        self.iface.removePluginMenu("&PackageStyler", self.action)

    def run(self):
        if not self.dialog:
            self.dialog = PackageStylerDialog(self.iface)
        self.dialog.show()
        result = self.dialog.exec_()

        if result:
            configurations = self.dialog.get_configurations()
            self.apply_styles(configurations)

    def apply_styles(self, configurations):
        layers = QgsProject.instance().mapLayers().values()
        for keyword, qml_path in configurations:
            for layer in layers:
                if keyword.lower() in layer.name().lower():
                    layer.loadNamedStyle(qml_path)
                    layer.triggerRepaint()
