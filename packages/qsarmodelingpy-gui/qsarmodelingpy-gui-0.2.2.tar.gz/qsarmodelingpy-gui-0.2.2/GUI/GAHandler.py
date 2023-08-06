import os
import gi
import time
import logging
from multiprocessing import Process
from threading import Thread
from Interfaces import ConfigGAInterface
from MainHandler import Handler
from runCalculations import RunCalculations
from Utils import set_output_matrix_as_input, get_current_time_as_string
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class GAHandler(Handler):
    def __init__(self, builder, handler: Handler):
        super().__init__(builder)
        self.builder = builder
        self.handler = handler
        self.config_GA_window = self.builder.get_object('config_GA_window')
        self.config_GA_window.connect(
            'delete-event', lambda w, e: w.hide() or True)
        self.ga_config: ConfigGAInterface
        self.running_process = None

    def _is_running(self) -> bool:
        if self.running_process is None:
            return False
        if self.running_process.is_alive():
            return True
        else:
            self.running_process.terminate()
            return False

    def GA_confirm_close(self, dialog, response) -> None:
        dialog.hide()
        if response == Gtk.ResponseType.OK and self._is_running():
            self.on_GA_cancel_button_clicked(None, force=True)

    def on_GA_cancel_button_clicked(self, _, force: bool = False) -> None:
        """ Handle GA cancel button """
        if self._is_running():
            logging.debug(f"running_process = {self.running_process}")
            if not force:
                self.builder.get_object('GA_will_kill_all_window').show()
                return
            else:
                logging.warning("Terminating GA Calculation.")
                self.running_process.terminate()
                self.running_process = None
        self.config_GA_window.hide()

    def _keep_updating_progress_bar(self) -> None:
        pbar = self.builder.get_object("GA_progress_bar")
        pbar.show()
        while self._is_running():
            time.sleep(0.1)
            pbar.pulse()
        else:
            pbar.set_fraction(0)
            # If everything is ok, current matrix will be the filtered one.
            set_output_matrix_as_input(self, self.ga_config)

    def on_GA_run_button_clicked(self, _) -> None:
        if self._is_running():
            logging.warning(
                f"Already running with PID = {self.running_process.pid}")
            return

        if self.handler.files_ok():
            self.ga_config = {
                'XMatrix': self.handler.get_X_matrix(),
                'yvector': self.handler.get_y_vector(),
                'output_matrix': self.builder.get_object('GA_output_matrix').get_text(),
                'output_cv': self.builder.get_object('GA_output_cv').get_text(),
                'output_q2': self.builder.get_object('GA_output_q2').get_text(),
                'output_selected': self.builder.get_object('GA_output_selected_variables').get_text(),
                'output_PLS_model': self.builder.get_object('GA_output_model').get_text(),
                'varcut': self.builder.get_object('ga_varcut').get_value(),
                'corrcut': self.builder.get_object('ga_corrcut').get_value(),
                'autoscale': self.builder.get_object('ga_autoscale').get_active(),
                'lj_transform': self.builder.get_object('ga_ljtransform').get_active(),
                'autocorrcut': self.builder.get_object('ga_autocorrcut').get_value(),
                'max_latent_model': self.builder.get_object('ga_max_latent_model').get_value(),
                'min_vars_model': self.builder.get_object('ga_min_vars_model').get_value(),
                'max_vars_model': self.builder.get_object('ga_max_vars_model').get_value(),
                'population_size': self.builder.get_object('ga_population_size').get_value(),
                'migration_rate': self.builder.get_object('ga_migration_rate').get_value(),
                'crossover_rate': self.builder.get_object('ga_crossover_rate').get_value(),
                'mutation_rate': self.builder.get_object('ga_mutation_rate').get_value(),
                'generations': self.builder.get_object('ga_generations').get_value(),
                'yrand': self.builder.get_object('ga_yrand').get_value(),
                'lno': self.builder.get_object('ga_lno').get_value()
            }

            date_time = get_current_time_as_string()
            if not self.ga_config['output_matrix']:
                self.ga_config['output_matrix'] = os.path.join(os.path.dirname(self.handler.get_X_matrix()),
                                                               "GA_output_matrix_{}.csv".format(date_time))
            if not self.ga_config['output_cv']:
                self.ga_config['output_cv'] = os.path.join(os.path.dirname(self.handler.get_X_matrix()),
                                                           "GA_output_CV_{}.csv".format(date_time))
            if not self.ga_config['output_q2']:
                self.ga_config['output_q2'] = os.path.join(os.path.dirname(self.handler.get_X_matrix()),
                                                           "GA_output_Q2_{}.csv".format(date_time))
            if not self.ga_config['output_selected']:
                self.ga_config['output_selected'] = os.path.join(os.path.dirname(self.handler.get_X_matrix()),
                                                                 "GA_output_selected_{}.csv".format(date_time))
            if not self.ga_config['output_PLS_model']:
                self.ga_config['output_PLS_model'] = os.path.join(os.path.dirname(self.handler.get_X_matrix()),
                                                                 "GA_output_model_{}.csv".format(date_time))

            logging.debug("Ok, I'll call RunCalculations.runGA().")
            self.running_process = Process(target=GAHandler.call_runner, args=(self.ga_config,))
            self.running_process.start()
            pbthread = Thread(target=self._keep_updating_progress_bar)
            pbthread.start()
            logging.debug(f"Started PID = {self.running_process.pid}")

        else:
            logging.error("Please, open the files in File > Open...")

    @staticmethod
    def call_runner(config: ConfigGAInterface) -> None:
        logging.debug("Calling GA runner")
        RunCalculations.runGA(config)
        logging.debug("Calculation done.")