import os
from typing import Type, Union, List
import pandas
import qsarmodelingpy.Utils
import Utils
import logging
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from Constants import DEBUG_MODE

import warnings
warnings.filterwarnings("ignore")

class Handler(object):

    __childrens: List[object] = []

    def __init__(self, builder):
        self.builder = builder
        # Saving windows
        self.main_window = builder.get_object('main_window')
        self.results_window = builder.get_object('results_window')
        self.config_OPS_window = builder.get_object('config_OPS_window')
        self.config_GA_window = builder.get_object('config_GA_window')
        self.about_window = builder.get_object('about_window')
        self.csv_file_filter = builder.get_object('open_filter')
        self.main_window_stack = builder.get_object('main_window_stack')
        self.config_varcut_window = builder.get_object('config_varcut_window')
        self.config_corrcut_window = builder.get_object(
            'config_corrcut_window')
        self.config_autocorrcut_window = builder.get_object(
            'config_autocorrcut_window')
        self.config_cv_window = builder.get_object('config_cv_window')
        self.config_yrlno_window = builder.get_object('config_yrlno_window')
        self.config_extval_window = builder.get_object('config_extval_window')

        # Saving elements
        self.main_window_pages = [builder.get_object(
            'main_window_welcome'), builder.get_object('main_window_tables')]
        self.treeview_X = builder.get_object('treeview_X')
        self.treeview_y = builder.get_object('treeview_y')

        # connect destroy signal
        self.main_window.connect('destroy', Gtk.main_quit)
        self.about_window.connect(
            'delete-event', lambda w, e: w.hide() or True)
        self.results_window.connect(
            'delete-event', lambda w, e: w.hide() or True)

        # Setting file filters
        self.csv_file_filter.set_name('CSV Files (*.csv)')

        # Handling files
        self.X_matrix = None
        self.y_vector = None
        self.last_opened_path = ""
        self.last_saved_path = ""

        # TODO: remove these stuff

    def register_handler(self, handler) -> None:
        """Register a new handler 

        Args:
            handler (Handler): The handler to be registered
        """        
        if handler not in self.__childrens:
            self.__childrens.append(handler)
    
    def get_handlers(self) -> list:
        """ Get all handlers """
        return self.__childrens

    def get_handler(self, _type: Type) -> object:
        for handler in self.__childrens:
            if isinstance(handler, _type):
                return handler
        raise ValueError(f"No handler of type {_type} found.")

    def on_menu_openlog_activate(self, _) -> None:
        """ Open the log """
        Utils.open_external(Utils.get_log_file())

    def on_menu_ops_model_activate(self, _) -> None:
        """ Handle menu Generate > OPS """
        self.config_OPS_window.show_all()

    def on_menu_ga_model_activate(self, _) -> None:
        """ Handle menu Generate > GA """
        self.config_GA_window.show_all()

    def on_menu_varcut_activate(self, _) -> None:
        """ Handle menu Filter > Variance cut """
        self.config_varcut_window.show()

    def on_menu_corrcut_activate(self, _) -> None:
        """ Handle menu Filter > Correlation cut """
        self.config_corrcut_window.show()

    def on_menu_autocorrcut_activate(self, _) -> None:
        """ Handle menu Filter > Autocorrelation cut """
        self.config_autocorrcut_window.show()

    def on_menu_cv_activate(self, _) -> None:
        """ Handle menu Validation > Cross Validation """
        self.config_cv_window.show()

    def on_menu_yrlno_activate(self, _) -> None:
        """ Handle menu Validation > Y-Randomization / Leave-N-Out """
        self.config_yrlno_window.show()

    def on_menu_extval_activate(self, _) -> None:
        """ Handle menu Validation > External Validation """
        self.config_extval_window.show()

    def open_file(self, use_last_path=True) -> str:
        """
        Show an Open File dialog

        :param use_last_path: Whether or not to start at the last folder opened
        :return: the selected filename
        """
        file_chooser = Gtk.FileChooserDialog(
            title="Open...", action=Gtk.FileChooserAction.OPEN)
        file_chooser.add_buttons(
            "Cancel", Gtk.ResponseType.CANCEL, "Open", Gtk.ResponseType.OK)
        file_chooser.set_default_response(Gtk.ResponseType.OK)
        file_chooser.add_filter(self.csv_file_filter)
        if self.last_opened_path and use_last_path:
            file_chooser.set_current_folder(self.last_opened_path)
        response = file_chooser.run()
        filename = ""
        if response == Gtk.ResponseType.OK:
            filename = file_chooser.get_filename()
            self.last_opened_path = os.path.dirname(os.path.abspath(filename))
        file_chooser.destroy()
        return filename

    def save_file(self) -> str:
        file_chooser = Gtk.FileChooserDialog(
            title="Save...", action=Gtk.FileChooserAction.SAVE)
        file_chooser.add_buttons(
            "Cancel", Gtk.ResponseType.CANCEL, "Save", Gtk.ResponseType.OK)
        file_chooser.set_default_response(Gtk.ResponseType.OK)
        file_chooser.add_filter(self.csv_file_filter)
        if self.last_saved_path:
            file_chooser.set_current_folder(self.last_saved_path)
        elif self.last_opened_path:
            file_chooser.set_current_folder(self.last_opened_path)
        filename = ""
        response = file_chooser.run()
        if response == Gtk.ResponseType.OK:
            filename = file_chooser.get_filename()
            self.last_saved_path = filename
        file_chooser.destroy()
        return filename

    def on_save_file(self, entry: Gtk.Entry) -> None:
        filename = self.save_file()
        if filename:
            entry.set_text(filename)

    def on_open_file(self, entry: Gtk.Entry) -> None:
        filename = self.open_file()
        if filename:
            entry.set_text(filename)

    def block_menus_until_file_load(self) -> None:
        """ Block menus while files is not properly loaded """
        menus = [
            self.builder.get_object('menu_generate'),
            self.builder.get_object('menu_validate'),
            self.builder.get_object('menu_filter'),
        ]
        if self.X_matrix and self.y_vector:
            for elem in menus:
                elem.set_sensitive(True)
        else:
            for elem in menus:
                elem.set_sensitive(False)

    def on_menu_open_matrix_activate(self, _) -> None:
        """ Handle menu File > Open... > Open matrix """
        filename = self.open_file()
        if filename:
            # self.X_matrix = filename
            logging.debug(f"Selected {filename}.")
            self.set_X_matrix(filename)
            logging.debug(f"Setted {self.get_X_matrix()}.")
            self.draw_matrices('matrix')

    def on_menu_open_vector_activate(self, _) -> None:
        """ Handle menu File > Open... > Open vector """
        filename = self.open_file()
        if filename:
            # self.y_vector = filename
            logging.debug(f"Selected {filename}.")
            self.set_y_vector(filename)
            logging.debug(f"Setted {self.get_y_vector()}.")
            self.draw_matrices('vector')

    def draw_matrices(self, what_to_draw) -> None:
        """ Draw a pandas matrix or vector in the main screen.
            Works like a Factory to draw_pandas_matrix() and draw_pandas_vector(). """
        show = False
        if what_to_draw == 'matrix' and self.X_matrix and os.path.isfile(self.X_matrix):
            # Draw matrix
            self.draw_pandas_matrix(self.treeview_X, self.X_matrix)
            show = True
        if what_to_draw == 'vector' and self.y_vector and os.path.isfile(self.y_vector):
            # Draw vector
            self.draw_pandas_vector(self.treeview_y, self.y_vector)
            show = True

        if show:
            self.main_window_stack.set_visible_child(self.main_window_pages[1])
        else:
            self.main_window_stack.set_visible_child(self.main_window_pages[0])

        self.block_menus_until_file_load()

    def draw_pandas_matrix(self, treeview, path, print_index=True) -> None:
        """ Draws in treeview a pandas matrix from path (csv) """
        df = qsarmodelingpy.Utils.load_matrix(path, usecols=list(range(10)))

        print_et_cetera_column = False
        if df.shape[1] > 10:
            df = df.iloc[:, 0:10]
            print_et_cetera_column = True
        liststore_args = [str] if print_index else []
        liststore_args += [float] * int(df.shape[1]) # type: ignore
        if print_et_cetera_column:
            liststore_args += [str]
        liststore = Gtk.ListStore(*liststore_args)
        df_indexes = df.index.values
        for i in range(df.shape[0]):
            appendix = [str(df_indexes[i])] if print_index else []
            appendix += list(df.iloc[i, :])
            if print_et_cetera_column:
                appendix += ["..."]
            liststore.append(appendix)
        self.clear_treeview(treeview)
        current_model = treeview.get_model()
        if current_model is not None:
            current_model.clear()
        treeview.set_model(liststore)

        # Draw index column
        if print_index:
            renderer_text = Gtk.CellRendererText()
            column_text = Gtk.TreeViewColumn('Molecule', renderer_text, text=0)
            treeview.append_column(column_text)

        # Draw data columns
        for i in range(df.shape[1]):
            renderer_text = Gtk.CellRendererText()
            text = i + 1 if print_index else i
            column_text = Gtk.TreeViewColumn(
                df.columns[i], renderer_text, text=text)
            treeview.append_column(column_text)

        # Draw et cetera column
        if print_et_cetera_column:
            renderer_text = Gtk.CellRendererText()
            text = df.shape[1] + 1 if print_index else df.shape[1]
            column_text = Gtk.TreeViewColumn(
                '...', renderer_text, text=df.shape[1] + 1)
            treeview.append_column(column_text)

    def draw_pandas_vector(self, treeview, path: str) -> None:
        """ Draws in treeview a pandas vector from path (csv/txt) """
        df = pandas.read_csv(path, header=None, sep=",")

        self.clear_treeview(treeview)

        liststore = Gtk.ListStore(float)

        # df should be a vector
        data = list(df.iloc[0, :]) if df.shape[0] == 1 else list(df.iloc[:, 0])

        for i in range(max(df.shape[0], df.shape[1])):
            liststore.append([data[i]])
        treeview.set_model(liststore)

        # Draw data column
        renderer_text = Gtk.CellRendererText()
        column_text = Gtk.TreeViewColumn('Vector', renderer_text, text=0)
        treeview.append_column(column_text)

    def on_menu_about_activate(self, _) -> None:
        """ Handle menu About """

        self.about_window.run()

    def get_X_matrix(self) -> str:
        return self.X_matrix

    def get_y_vector(self) -> str:
        return self.y_vector

    def set_X_matrix(self, new_value: str) -> None:
        if new_value is None or os.path.isfile(str(new_value)):
            self.X_matrix = new_value
            self.block_menus_until_file_load()
        else:
            raise TypeError(f"File {new_value} is not a valid file.")

    def set_y_vector(self, new_value: str) -> None:
        if new_value is None or os.path.isfile(str(new_value)):
            self.y_vector = new_value
            self.block_menus_until_file_load()
        else:
            raise TypeError(f"File {new_value} is not a valid file.")

    @staticmethod
    def on_auto_state_set(obj, active: bool) -> None:
        """Set an object as active (editable) or not. Usually called by switchers."""
        if active:
            obj.set_value(0)
            obj.set_editable(False)
            obj.set_sensitive(False)
        else:
            obj.set_editable(True)
            obj.set_sensitive(True)

    def files_ok(self) -> bool:
        matp = self.get_X_matrix()
        logging.debug(f"mat = {matp}")
        mat = os.path.isfile(matp)
        logging.debug(f"mat = {mat}")
        vecp = self.get_y_vector()
        logging.debug(f"vec = {vecp}")
        vec = os.path.isfile(vecp)
        logging.debug(f"vec = {vec}")
        return os.path.isfile(self.get_X_matrix()) and os.path.isfile(self.get_y_vector())

    @staticmethod
    def on_close_modal(modal) -> None:
        modal.hide()

    @staticmethod
    def clear_treeview(treeview) -> None:
        columns = treeview.get_columns()
        for col in columns:
            treeview.remove_column(col)

    @staticmethod
    def on_about_window_destroy(_) -> bool:
        return True

    @staticmethod
    def gtk_main_quit(_) -> None:
        Gtk.main_quit()
