from typing import Callable, Dict
import numpy as np
import logging, logger
from qsarmodelingpy.external_validation import ExternalValidation
import matplotlib.pyplot as plt  # TODO: add do dependecies
logger.silence_matplotlib_logger()
from abc import ABC, abstractmethod
from qsarmodelingpy.cross_validation_class import CrossValidation
from qsarmodelingpy.yrandomization import YRandomization
import Utils



class Plots(ABC):

    def __init__(self) -> None:
        matplolib_config = Utils.read_config("matplotlib")
        plt.rcParams.update(matplolib_config)

    @abstractmethod
    def get_methods(self) -> Dict[str, Callable]:
        pass


class CrossValidationPlots(Plots):

    def __init__(self) -> None:
        super().__init__()

    def Q2_R2_evolution(self, cv: CrossValidation):
        xaxis = range(1, cv.nLVMax + 1)
        y1 = cv.R2()
        y2 = cv.Q2()
        plt.plot(xaxis, y1, label="R²", marker='o')
        plt.plot(xaxis, y2, label="Q²", marker='o')
        plt.legend()
        plt.title("Cross-Validation error - PLS")
        plt.xlabel("nLV")
        plt.ylabel(r"$R^2 / Q^2$")
        plt.show()

    def scatter_Q2_R2(self):
        raise NotImplementedError()

    def y_versus_ŷ_CV(self, cv: CrossValidation):
        nLV = int(cv.returnParameters().loc["nLV"][0])
        xaxis = np.array(cv.y)
        yaxis = list(cv.ycv[:, nLV-1])
        plt.plot(xaxis, xaxis, color="red", linewidth=1, label="y = x line")
        plt.plot(xaxis, yaxis, linestyle="None", marker="o", label="Data")
        plt.title("Cross-Validation prediction")
        plt.xlabel("Experimental activity")
        plt.ylabel("Predicted activity")
        plt.show()

    def y_versus_ŷ_cal(self, cv: CrossValidation):
        nLV = int(cv.returnParameters().loc["nLV"][0])
        xaxis = np.array(cv.y)
        yaxis = list(cv.ycal[:, nLV-1])
        plt.plot(xaxis, xaxis, color="red", linewidth=1, label="y = x line")
        plt.plot(xaxis, yaxis, linestyle="None", marker="o", label="Data")
        plt.title("Calibration prediction")
        plt.xlabel("Experimental activity")
        plt.ylabel("Predicted activity")
        plt.show()

    def get_methods(self) -> Dict[str, Callable]:
        return {
            "Q² and R² × Latent Variables (cross-validation)": self.Q2_R2_evolution,
            "Exprimental × Predicted (calibration)": self.y_versus_ŷ_cal,
            "Exprimental × Predicted (cross-validation)": self.y_versus_ŷ_CV,
        }

class YRandomizationPlots(Plots):
    def __init__(self) -> None:
        super().__init__()

    def Q2_versus_R2(self, yr: YRandomization):
        R2_rand = yr.R2[:-1]
        Q2_rand = yr.Q2[:-1]
        R2_best = yr.R2[-1]
        Q2_best = yr.Q2[-1]
        plt.plot(R2_rand, Q2_rand, linestyle="None", marker='o', label="Randomized")
        plt.plot(R2_best, Q2_best, linestyle="None", marker='o', label="Best model")
        plt.title("y-randomization")
        plt.xlabel("R²")
        plt.ylabel("Q²")
        plt.show()

    def get_methods(self) -> Dict[str, Callable]:
        return {
            "Q² and R² × Latent Variables (y-randomization)": self.Q2_versus_R2,
        }


if __name__ == "__main__":
    import pandas as pd
    import os
    import coloredlogs
    import logging
    logging_level = logging.DEBUG
    coloredlogs.install(
        fmt="%(filename)s:%(lineno)s %(funcName)s() %(levelname)s  %(message)s", level=logging_level)
    coloredlogs.DEFAULT_FIELD_STYLES = {'filename': {'color': 'blue'}, 'lineno': {
        'color': 'blue'}, 'funcName': {'color': 'magenta'}, 'levelname': {'bold': True, 'color': 'black'}}

    directory = "/home/helitonmrf/Documents/QSAR/cancer_prostata/resultados"
    X_matrix_file = "filtered_10_GA_X_sel.csv"
    y_matrix_file = "../atividades.txt"

    df = pd.read_csv(os.path.join(directory, X_matrix_file),
                     sep=';', index_col=0)
    X = df.to_numpy()
    y = pd.read_csv(os.path.join(directory, y_matrix_file),
                    sep=';', header=None).values
    cv = CrossValidation(X, y)
    methods = CrossValidationPlots().get_methods()
    # logging.debug(f"{methods = }")

    # for method in methods:
    #     methods[method](cv)
    #     break

    yr = YRandomization(X,y,cv.nLVMax)
    yrp = YRandomizationPlots()
    yrp.Q2_versus_R2(yr)
