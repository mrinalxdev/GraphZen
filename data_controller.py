import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

class DataProcessor:
    def __init__(self):
        self.datasets = {}
        self.current_figure = None

    def load_dataset(self, file_path):
        dataset_name = file_path.split("/")[-1].split(".")[0]
        if file_path.endswith('.csv'):
            self.datasets[dataset_name] = pd.read_csv(file_path)
        elif file_path.endswith('.xlsx'):
            self.datasets[dataset_name] = pd.read_excel(file_path)
        else:
            raise ValueError("Unsupported file format. Please use CSV or Excel files.")
        return dataset_name

    def get_columns(self, dataset_name):
        return list(self.datasets[dataset_name].columns)

    def apply_filter(self, filter_params):
        for dataset_name, df in self.datasets.items():
            column = filter_params['column']
            operator = filter_params['operator']
            value = filter_params['value']

            if operator == "==":
                df = df[df[column] == value]
            elif operator == "!=":
                df = df[df[column] != value]
            elif operator == ">":
                df = df[df[column] > float(value)]
            elif operator == "<":
                df = df[df[column] < float(value)]
            elif operator == ">=":
                df = df[df[column] >= float(value)]
            elif operator == "<=":
                df = df[df[column] <= float(value)]
            elif operator == "contains":
                df = df[df[column].str.contains(value, case=False)]

            self.datasets[dataset_name] = df

    def create_visualization(self, selected_datasets, viz_type):
        if len(selected_datasets) == 0:
            raise ValueError("No datasets selected")

        if viz_type == "Line Plot":
            self.create_line_plot(selected_datasets)
        elif viz_type == "Scatter Plot":
            self.create_scatter_plot(selected_datasets)
        elif viz_type == "Bar Chart":
            self.create_bar_chart(selected_datasets)
        elif viz_type == "Histogram":
            self.create_histogram(selected_datasets)
        elif viz_type == "Box Plot":
            self.create_box_plot(selected_datasets)
        elif viz_type == "Heatmap":
            self.create_heatmap(selected_datasets)
        else:
            raise ValueError("Unsupported visualization type")

    def create_line_plot(self, selected_datasets):
        fig = go.Figure()
        for dataset_name in selected_datasets:
            df = self.datasets[dataset_name]
            for column in df.select_dtypes(include=['float64', 'int64']).columns:
                fig.add_trace(go.Scatter(x=df.index, y=df[column], name=f"{dataset_name} - {column}"))
        fig.update_layout(title="Line Plot", xaxis_title="Index", yaxis_title="Value")
        self.current_figure = fig
        fig.show()

    def create_scatter_plot(self, selected_datasets):
        fig = make_subplots(rows=len(selected_datasets), cols=1, subplot_titles=selected_datasets)
        for i, dataset_name in enumerate(selected_datasets, start=1):
            df = self.datasets[dataset_name]
            numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
            if len(numeric_cols) < 2:
                continue
            fig.add_trace(
                go.Scatter(x=df[numeric_cols[0]], y=df[numeric_cols[1]], mode='markers', name=dataset_name),
                row=i, col=1
            )
        fig.update_layout(height=300*len(selected_datasets), title_text="Scatter Plots")
        self.current_figure = fig
        fig.show()

    def create_bar_chart(self, selected_datasets):
        fig = make_subplots(rows=len(selected_datasets), cols=1, subplot_titles=selected_datasets)
        for i, dataset_name in enumerate(selected_datasets, start=1):
            df = self.datasets[dataset_name]
            numeric_col = df.select_dtypes(include=['float64', 'int64']).columns[0]
            fig.add_trace(
                go.Bar(x=df.index, y=df[numeric_col], name=dataset_name),
                row=i, col=1
            )
        fig.update_layout(height=300*len(selected_datasets), title_text="Bar Charts")
        self.current_figure = fig
        fig.show()

    def create_histogram(self, selected_datasets):
        fig = make_subplots(rows=len(selected_datasets), cols=1, subplot_titles=selected_datasets)
        for i, dataset_name in enumerate(selected_datasets, start=1):
            df = self.datasets[dataset_name]
            numeric_col = df.select_dtypes(include=['float64', 'int64']).columns[0]
            fig.add_trace(
                go.Histogram(x=df[numeric_col], name=dataset_name),
                row=i, col=1
            )
        fig.update_layout(height=300*len(selected_datasets), title_text="Histograms")
        self.current_figure = fig
        fig.show()

    def create_box_plot(self, selected_datasets):
        fig = go.Figure()
        for dataset_name in selected_datasets:
            df = self.datasets[dataset_name]
            numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
            for col in numeric_cols:
                fig.add_trace(go.Box(y=df[col], name=f"{dataset_name} - {col}"))
        fig.update_layout(title="Box Plots")
        self.current_figure = fig
        fig.show()

    def create_heatmap(self, selected_datasets):
        fig = make_subplots(rows=len(selected_datasets), cols=1, subplot_titles=selected_datasets)
        for i, dataset_name in enumerate(selected_datasets, start=1):
            df = self.datasets[dataset_name]
            corr_matrix = df.select_dtypes(include=['float64', 'int64']).corr()
            fig.add_trace(
                go.Heatmap(z=corr_matrix.values, x=corr_matrix.columns, y=corr_matrix.columns, colorscale='Viridis'),
                row=i, col=1
            )
        fig.update_layout(height=400*len(selected_datasets), title_text="Correlation Heatmaps")
        self.current_figure = fig
        fig.show()

    def export_graph(self, file_path):
        if self.current_figure:
            self.current_figure.write_image(file_path)
        else:
            raise ValueError("No visualization to export")