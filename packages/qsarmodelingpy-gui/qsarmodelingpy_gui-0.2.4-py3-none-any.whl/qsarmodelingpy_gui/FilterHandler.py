from MainHandler import Handler
from runCalculations import RunCalculations
import pandas
from gi.repository import Gtk
import os
import gi

gi.require_version('Gtk', '3.0')


class FilterHandler(Handler):
    def __init__(self, builder, handler: Handler):
        super().__init__(builder)
        self.builder = builder
        self.handler = handler
        self.config_varcut_window = self.builder.get_object(
            'config_varcut_window')
        self.config_varcut_window.connect(
            'delete-event', lambda w, e: w.hide() or True)
        self.config_varcut_window = builder.get_object('config_varcut_window')
        self.config_corrcut_window = builder.get_object(
            'config_corrcut_window')
        self.config_autocorrcut_window = builder.get_object(
            'config_autocorrcut_window')

    def run_corrfilter(self, prefix, value) -> bool:
        runMethod = {
            'corrcut': RunCalculations.runCorrCut,
            'autocorrcut': RunCalculations.runAutoCorrCut
        }
        window = {
            'corrcut': self.config_corrcut_window,
            'autocorrcut': self.config_autocorrcut_window
        }
        if prefix not in runMethod:
            return False

        """ TODO:
            In the future, the user will be able to cut the matrix without
            saving it, leaving it temporarily available within the program to
            perform another calculation in the sequence. """
        save = True  # self.builder.get_object(f'{prefix}_save').get_active()
        output = self.builder.get_object(
            f'{prefix}_output').get_text() if save else ""
        new_matrix = runMethod[prefix](
            self.handler.get_X_matrix(), self.handler.get_y_vector(), value, save, output)
        print(
            f'x_matrix:{self.handler.get_X_matrix()}\n\ny_vector:{self.handler.get_y_vector()}\n\nreturn:{new_matrix}')
        # TODO: let user choose whether to replace the active matrix with the new one
        if os.path.isfile(new_matrix):
            self.handler.set_X_matrix(new_matrix)
            self.handler.draw_matrices('matrix')
        window[prefix].hide()
        return True

    def on_varcut_run_button_clicked(self, _) -> None:
        """ Handle Run button from Variance cut screen """
        if self.handler.files_ok():
            value = float(self.builder.get_object('varcut_varcut').get_value())
            # TODO
            """ In the future, the user will be able to cut the matrix without
                saving it, leaving it temporarily available within the program to
                perform another calculation in the sequence. """
            save = True  # self.builder.get_object('varcut_save').get_active()
            output = self.builder.get_object(
                'varcut_output').get_text() if save else ""
            new_matrix = RunCalculations.runVarCut(
                self.handler.get_X_matrix(), value, save, output)
            # TODO: let user choose whether to replace the active matrix with the new one
            if os.path.isfile(new_matrix):
                self.handler.set_X_matrix(new_matrix)
                self.handler.draw_matrices('matrix')
            self.config_varcut_window.hide()

    def on_corrcut_run_button_clicked(self, _) -> None:
        """ Handle Run button from Correlation cut screen """
        if self.handler.files_ok():
            value = float(self.builder.get_object(
                'corrcut_corrcut').get_value())
            self.run_corrfilter('corrcut', value)

    def on_autocorrcut_run_button_clicked(self, _) -> None:
        """ Handle Run button from Autocorrelation cut screen """
        if self.handler.files_ok():
            value = float(self.builder.get_object(
                'autocorrcut_autocorrcut').get_value())
            self.run_corrfilter('autocorrcut', value)

    def on_varcut_save_toggled(self, this) -> None:
        self.on_save_toggled(this, 'varcut')

    def on_corrcut_save_toggled(self, this) -> None:
        self.on_save_toggled(this, 'corrcut')

    def on_autocorrcut_save_toggled(self, this) -> None:
        self.on_save_toggled(this, 'autocorrcut')

    def on_save_toggled(self, this, prefix) -> None:
        """ Handle the toggle of Variance Cut screen save Option """
        box = self.builder.get_object(f'{prefix}_filename_box')
        if this.get_active():
            box.show()
        else:
            box.hide()
