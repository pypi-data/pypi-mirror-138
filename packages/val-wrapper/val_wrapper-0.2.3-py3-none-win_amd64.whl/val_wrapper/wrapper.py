#!/usr/bin/env python3
import string
import sys
import subprocess
import os

VALID_EXEC_NAME =   [   
                        "Analyse", "DomainView", "HowWhatWhen",
                        "Instantiate", "Parser", "PinguPlan",
                        "PlanRec", "PlanSeqStep", "PlanToValStep",
                        "Relax", "TIM", "ToFn", "TypeAnalysis",
                        "Validate", "ValStep", "ValueSeq"
                    ]

def val_main(exec_name: str, args: list=[]):
    """A wrapper to execute KCL-VAL binaries

    :param exec_name: name of the binary [Exact]
    :type exec_name: String
    :param args: list of string arguments
    :type args: list
    """
    if isinstance(exec_name, str) and exec_name in VALID_EXEC_NAME:
        EXEC_PATH=os.path.join(os.path.dirname(__file__), "bin/"+exec_name)
        return subprocess.call([EXEC_PATH]+args)
    else:
        raise ValueError("Incorrect program name. Choose from the list: ", VALID_EXEC_NAME)