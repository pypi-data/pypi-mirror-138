from qsarmodelingpy.cross_validation_class import CrossValidation
import os
from typing import Dict, Callable, Optional
try:
    from typing import TypedDict # Python 3.8+
except ImportError:
    from typing_extensions import TypedDict # Python 3.7-
import logging

import pandas as pd
from MainHandler import Handler
import gi

from Plots import CrossValidationPlots, Plots
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.overrides import Gtk as Gtk3

class ResultWindowTexts(TypedDict):
    toptext: Optional[str]
    title: Optional[str]
    statistics: Optional[str]

class ResultsHandler(Handler):
    def __init__(self, builder):
        super().__init__(builder)
        self.builder = builder
        self.window = self.builder.get_object('results_window')
        self.window.connect(
            'delete-event', lambda w, e: w.hide() or True)
        # self.window.show_all()

        self.plot_type_selector: Gtk3.ComboBox = self.builder.get_object(
            'plot_selection_combo')

        # TODO: remove this
        # self.show(self.get_object_for_testing_TODO(), CrossValidationPlots())

    def show(self, dataobject, plotter: Plots, texts: Optional[ResultWindowTexts]=None):
        if texts is None:
            texts = ResultWindowTexts(toptext=None, title=None, statistics=None)

        self.dataobject = dataobject
        self.plotter = plotter
        self.init_selector(self.plotter.get_methods())
        self.set_texts(**texts)
        self.window.show_all()

    def set_texts(self, toptext: Optional[str] = "Your job is done.", statistics: Optional[str] = "", title: Optional[str] = ""):
        self.builder.get_object('results_statistics_toptext').set_text(toptext)

        # Set statistics text
        buffer = self.builder.get_object('results_statistics_textview').get_buffer()
        buffer.set_text(statistics)

        # Set window title
        if title != "": 
            self.window.set_title(title)

    def init_selector(self, methods: Dict[str, Callable]):
        model = Gtk.ListStore(str)
        for key in methods:
            model.append([key])
        self.plot_type_selector.set_model(model)
        self.plot_type_selector.set_entry_text_column(0)
        renderer_text = Gtk.CellRendererText()
        self.plot_type_selector.clear()
        self.plot_type_selector.pack_start(renderer_text, False)
        self.plot_type_selector.add_attribute(renderer_text, "text", 0)
        self.plot_type_selector.set_active(0)

    @staticmethod
    def get_selected_method(elem: Gtk3.ComboBox) -> str:
        tree_iter = elem.get_active_iter()
        if tree_iter is not None:
            model = elem.get_model()
            name = model[tree_iter][0]
            return name
        else:
            entry = elem.get_child()
            return entry.get_text()

    def on_plot(self, combobox: Gtk.ComboBox) -> None:
        self.plotter.get_methods()[self.get_selected_method(
            combobox)](self.dataobject)

    # TODO: remove this
    @staticmethod
    def get_object_for_testing_TODO() -> CrossValidation:
        """This is for TESTING ONLY and should be removed

        Returns:
            CrossValidation: The objetct to plot
        """
        directory = "/home/helitonmrf/Documents/QSAR/cancer_prostata/resultados"
        X_matrix_file = "filtered_10_GA_X_sel.csv"
        y_matrix_file = "../atividades.txt"

        df = pd.read_csv(os.path.join(directory, X_matrix_file),
                         sep=';', index_col=0)
        X = df.to_numpy()
        y = pd.read_csv(os.path.join(directory, y_matrix_file),
                        sep=';', header=None).values
        cv = CrossValidation(X, y)
        return cv
