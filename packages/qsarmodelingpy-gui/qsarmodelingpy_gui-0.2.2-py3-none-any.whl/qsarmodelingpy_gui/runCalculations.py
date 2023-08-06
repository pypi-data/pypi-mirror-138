import numpy as np
import pandas
import os
import json
import logging
from qsarmodelingpy.runGa import run as runGA
from qsarmodelingpy.runOPS import run as runOPS
from qsarmodelingpy.runExtVal import run as runExtVal
from qsarmodelingpy.filter import variance_cut, correlation_cut, autocorrelation_cut
from qsarmodelingpy.cross_validation_class import CrossValidation
from qsarmodelingpy.validate_yr_lno import validate, run_leavenout, run_yrandomization, ValidateYRLNOResult, YRResult, LNOResult
from qsarmodelingpy.Interfaces import ConfigGAInterface, ConfigOPSInterface, ExtValResult, ConfigExtValInterface
from qsarmodelingpy.Utils import load_matrix
from typing import Union


class RunCalculations:

    @staticmethod
    def runGA(config: ConfigGAInterface) -> bool:
        return runGA(config)

    @staticmethod
    def runOPS(config: ConfigOPSInterface) -> bool:
        return runOPS(config)

    @staticmethod
    def runVarCut(filename: str, value: float, save: bool = True, output: str = "") -> str:
        df = load_matrix(filename)
        indVar = variance_cut(df.values, value)
        dfCut = df.loc[:, df.columns[indVar]]
        if save:
            if not output:
                name = os.path.split(filename)[-1][:-4]
                output = os.path.join(os.path.dirname(filename),
                                      "{}_filtered_var_{:.2f}.csv".format(name, value))
            dfCut.to_csv(output)
            return output
        else:
            """ In the future, the user will be able to cut the matrix without 
             saving it, leaving it temporarily available within the program to
             perform another calculation in the sequence. """
            raise NotImplementedError(
                "save=False is reserved for future usage. Please, use save=True.")

    @staticmethod
    def runCorrelationFilter(auto: bool, X_path: str, y_path: str, value: float, save: bool = True, output: str = "") -> str:
        dfX = load_matrix(X_path)
        dfy = pandas.read_csv(y_path, header=None)
        indVar = autocorrelation_cut(dfX.values, dfy, value) if auto else correlation_cut(
            dfX.values, dfy.values, value)
        dfCut = dfX.loc[:, dfX.columns[indVar]]
        if save:
            if not output:
                name = os.path.split(X_path)[-1][:-4]
                output = os.path.join(os.path.dirname(X_path),
                                      "{}_filtered_{}_{:.2f}.csv".format(name, "autocorr" if auto else "corr", value))
            dfCut.to_csv(output)
            return output
        else:
            """ In the future, the user will be able to cut the matrix without 
             saving it, leaving it temporarily available within the program to
             perform another calculation in the sequence. """
            raise NotImplementedError(
                "save=False is reserved for future usage. Please, use save=True.")

    @staticmethod
    def runCorrCut(X_path: str, y_path: str, corrcut: float, save: bool = True, output: str = "") -> str:
        return RunCalculations.runCorrelationFilter(False, X_path, y_path, corrcut, save, output)

    @staticmethod
    def runAutoCorrCut(X_path: str, y_path: str, autocorrcut: float, save: bool = True, output: str = "") -> str:
        return RunCalculations.runCorrelationFilter(True, X_path, y_path, autocorrcut, save, output)

    @staticmethod
    def runCrossValidation(X_path: str, y_path: str, filename: str = "", nLV=None, skipsaving=False) -> CrossValidation:
        if filename == "":
            X_name = os.path.splitext(os.path.basename(X_path))[0]
            filename = os.path.join(os.path.dirname(X_path),
                                    f'{X_name}_CV_output.csv')
        dfX = load_matrix(X_path).values
        dfy = pandas.read_csv(y_path, header=None).values
        logging.debug(dfX.shape)
        logging.debug(dfy.shape)
        logging.debug(dfy)
        cv = CrossValidation(dfX, dfy)
        if not skipsaving:
            cv.saveParameters(filename)
        return cv

    @staticmethod
    def run_yrlno(X_path: str,
                  y_path: str,
                  yr_cut: float = 0.3,
                  lno_cut: float = 0.1,
                  return_object=False
                  ) -> Union[bool, ValidateYRLNOResult]:
        dfX = load_matrix(X_path)
        dfy = pandas.read_csv(y_path, header=None).to_numpy()
        yrresult = run_yrandomization(dfX, dfy, yr_cut)
        lnoresult = run_leavenout(dfX, dfy, lno_cut)

        passed = yrresult["passed"] and lnoresult["passed"]
        
        result = ValidateYRLNOResult({"passed": passed, "yr_result": yrresult, "lno_result": lnoresult})
        if return_object:
            return result
        else:
            return passed



    @staticmethod
    def runExternalValidation(config: ConfigExtValInterface) -> ExtValResult:
        return runExtVal(config)
