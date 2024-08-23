from PyQt5.QtWidgets import QListWidget, QDockWidget, QVBoxLayout, QWidget, QComboBox, QLabel, QPushButton, QLineEdit
from PyQt5.QtCore import pyqtSignal

class DatasetListWidget(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setSelectionMode(QListWidget.ExtendedSelection)

    def add_dataset(self, dataset_name):
        self.addItem(dataset_name)

    def get_selected_datasets(self):
        return [item.text() for item in self.selectedItems()]

class VisualizationOptionsWidget(QDockWidget):
    viz_type_changed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__("Visualization Options", parent)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.viz_type_combo = QComboBox()
        self.viz_type_combo.addItems(["Line Plot", "Scatter Plot", "Bar Chart", "Histogram", "Box Plot", "Heatmap"])
        self.viz_type_combo.currentIndexChanged.connect(self.viz_type_changed.emit)
        layout.addWidget(QLabel("Visualization Type:"))
        layout.addWidget(self.viz_type_combo)

        export_button = QPushButton("Export Graph")
        export_button.clicked.connect(self.parent().export_graph)
        layout.addWidget(export_button)

        widget = QWidget()
        widget.setLayout(layout)
        self.setWidget(widget)

    def get_selected_visualization(self):
        return self.viz_type_combo.currentText()

class FilterWidget(QDockWidget):
    filter_applied = pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__("Filter Options", parent)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.column_combo = QComboBox()
        self.operator_combo = QComboBox()
        self.operator_combo.addItems(["==", "!=", ">", "<", ">=", "<=", "contains"])
        self.value_input = QLineEdit()

        layout.addWidget(QLabel("Column:"))
        layout.addWidget(self.column_combo)
        layout.addWidget(QLabel("Operator:"))
        layout.addWidget(self.operator_combo)
        layout.addWidget(QLabel("Value:"))
        layout.addWidget(self.value_input)

        apply_button = QPushButton("Apply Filter")
        apply_button.clicked.connect(self.apply_filter)
        layout.addWidget(apply_button)

        widget = QWidget()
        widget.setLayout(layout)
        self.setWidget(widget)

    def update_columns(self, columns):
        self.column_combo.clear()
        self.column_combo.addItems(columns)

    def apply_filter(self):
        filter_params = {
            "column": self.column_combo.currentText(),
            "operator": self.operator_combo.currentText(),
            "value": self.value_input.text()
        }
        self.filter_applied.emit(filter_params)