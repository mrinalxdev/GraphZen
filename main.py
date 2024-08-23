import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QDragEnterEvent, QDropEvent
from ui import DatasetListWidget, VisualizationOptionsWidget, FilterWidget
from data_controller import DataProcessor

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Interactive Data Visualization Tool")
        self.setGeometry(100, 100, 1200, 800)
        self.setAcceptDrops(True)

        self.data_processor = DataProcessor()
        self.init_ui()

    def init_ui(self):
        self.dataset_list = DatasetListWidget(self)
        self.setCentralWidget(self.dataset_list)

        self.viz_options = VisualizationOptionsWidget(self)
        self.addDockWidget(Qt.RightDockWidgetArea, self.viz_options)

        self.filter_widget = FilterWidget(self)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.filter_widget)

        self.dataset_list.itemSelectionChanged.connect(self.update_visualization)
        self.viz_options.viz_type_changed.connect(self.update_visualization)
        self.filter_widget.filter_applied.connect(self.apply_filter)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            self.load_dataset(file_path)

    def load_dataset(self, file_path):
        try:
            dataset_name = self.data_processor.load_dataset(file_path)
            self.dataset_list.add_dataset(dataset_name)
            self.filter_widget.update_columns(self.data_processor.get_columns(dataset_name))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load dataset: {str(e)}")

    def update_visualization(self):
        selected_datasets = self.dataset_list.get_selected_datasets()
        viz_type = self.viz_options.get_selected_visualization()
        if selected_datasets:
            try:
                self.data_processor.create_visualization(selected_datasets, viz_type)
            except Exception as e:
                QMessageBox.warning(self, "Visualization Error", str(e))

    def apply_filter(self, filter_params):
        try:
            self.data_processor.apply_filter(filter_params)
            self.update_visualization()
        except Exception as e:
            QMessageBox.warning(self, "Filter Error", str(e))

    def export_graph(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Export Graph", "", "PNG Files (*.png);;SVG Files (*.svg)")
        if file_path:
            self.data_processor.export_graph(file_path)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())