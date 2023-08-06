import logging
import time
import os
import gi
from multiprocessing import Process
from threading import Thread
from Interfaces import ConfigOPSInterface
from MainHandler import Handler
from runCalculations import RunCalculations
from Utils import get_current_time_as_string, set_output_matrix_as_input
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class OPSHandler(Handler):
    def __init__(self, builder, handler: Handler):
        super().__init__(builder)
        self.builder = builder
        self.handler = handler
        self.config_OPS_window = builder.get_object('config_OPS_window')
        self.config_OPS_window.connect(
            'delete-event', lambda w, e: w.hide() or True)
        self.ops_config: ConfigOPSInterface
        self.running_process = None

    def _is_running(self) -> bool:
        if self.running_process is None:
            return False
        if self.running_process.is_alive():
            return True
        else:
            self.running_process.terminate()
            return False

    def OPS_confirm_close(self, dialog, response) -> None:
        dialog.hide()
        if response == Gtk.ResponseType.OK and self._is_running():
            self.on_OPS_cancel_button_clicked(None, force=True)

    def on_OPS_cancel_button_clicked(self, _, force: bool = False) -> None:
        """ Handle OPS cancel button """
        if self._is_running():
            if not force:
                self.builder.get_object('OPS_will_kill_all_window').show()
                return
            else:
                logging.warning("Terminating OPS Calculation.")
                self.running_process.terminate()
                self.running_process = None
        self.config_OPS_window.hide()

    def _keep_updating_progress_bar(self) -> None:
        pbar = self.builder.get_object("OPS_progress_bar")
        pbar.show()
        while self._is_running():
            time.sleep(0.1)
            pbar.pulse()
        else:
            pbar.set_fraction(0)
            # If everything is ok, current matrix will be the filtered one.
            set_output_matrix_as_input(self, self.ops_config)

    def on_OPS_run_button_clicked(self, _) -> None:
        if self.handler.files_ok():
            self.ops_config = {
                'XMatrix': self.handler.get_X_matrix(),
                'yvector': self.handler.get_y_vector(),
                'output_matrix': self.builder.get_object('OPS_output_matrix').get_text(),
                'output_cv': self.builder.get_object('OPS_output_cv').get_text(),
                'output_models': self.builder.get_object('OPS_output_models').get_text(),
                'output_PLS_model': self.builder.get_object('OPS_output_model').get_text(),
                'varcut': self.builder.get_object('ops_varcut').get_value(),
                'corrcut': self.builder.get_object('ops_corrcut').get_value(),
                'autoscale': self.builder.get_object('ops_autoscale').get_active(),
                'lj_transform': self.builder.get_object('ops_ljtransform').get_active(),
                'autocorrcut': self.builder.get_object('ops_autocorrcut').get_value(),
                'latent_vars_ops': self.builder.get_object('ops_latent_vars_OPS').get_value(),
                'latent_vars_model': self.builder.get_object('ops_latent_vars_model').get_value(),
                'ops_window': self.builder.get_object('ops_OPS_window').get_value(),
                'ops_increment': self.builder.get_object('ops_OPS_increment').get_value(),
                'vars_percentage': self.builder.get_object('ops_vars_percentage').get_value(),
                'models_to_save': self.builder.get_object('ops_models_to_save').get_value(),
                'yrand': self.builder.get_object('ops_yrand').get_value(),
                'lno': self.builder.get_object('ops_lno').get_value(),
                'ops_type': 'f' if self.builder.get_object('ops_feed_ops').get_active() else 's'
            }

            date_time = get_current_time_as_string()
            if not self.ops_config['output_matrix']:
                self.ops_config['output_matrix'] = os.path.join(os.path.dirname(self.handler.get_X_matrix()), "OPS_output_matrix_{}.csv".format(date_time))
            if not self.ops_config['output_cv']:
                self.ops_config['output_cv'] = os.path.join(os.path.dirname(self.handler.get_X_matrix()), "OPS_output_CV_{}.csv".format(date_time))
            if not self.ops_config['output_models']:
                self.ops_config['output_models'] = os.path.join(os.path.dirname(self.handler.get_X_matrix()), "OPS_output_models_{}.json".format(date_time))
            if not self.ops_config['output_PLS_model']:
                self.ops_config['output_PLS_model'] = os.path.join(os.path.dirname(self.handler.get_X_matrix()), "OPS_output_model_{}.csv".format(date_time))

            self.running_process = Process(target=OPSHandler.call_runner, args=(self.ops_config,))
            self.running_process.start()
            pbthread = Thread(target=self._keep_updating_progress_bar)
            pbthread.start()
            logging.debug(f"Started PID = {self.running_process.pid}")
        else:
            print("Please, go to File > Open... before run a calculation.")

    @staticmethod
    def call_runner(config: ConfigOPSInterface) -> None:
        logging.debug("Calling OPS runner.")
        RunCalculations.runOPS(config)
        logging.debug("Calculation done.")

    