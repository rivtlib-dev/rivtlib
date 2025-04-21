import logging
import re
import sys
import warnings


class RvI:
    """ insert commands 

    Commands:

    """

    def __init__(self, folderD, labelD, rivtpD, rivtvD):
        """commands that format a utf doc

        Args:
            paramL (list): _description_
            labelD (dict): _description_
            folderD (dict): _description_
            localD (dict): _description_
        """

        self.cmdL = ["IMG", "IMG2", "TABLE", "TEXT"]
        self.tagsD = {"H]": "hline", "C]": "center", "B]": "centerbold",
                      "E]": "equa", "F]": "figure", "T]": "table",
                      "#]": "foot", "D]": "descrip", "S]": "sympy",
                      "P]": "page", "U]": "url",
                      "[O]]": "blkcode", "[B]]": "blkbold", "[N]]": "blkind",
                      "[I]]": "blkital",  "[T]]": "blkitind",
                      "[L]]": "blklatex",  "[Q]]": "blkquit"}
        self.rivtvD = rivtvD
        self.rivtpD = rivtpD
        self.folderD = folderD
        self.labelD = labelD
        errlogP = folderD["errlogP"]
        modnameS = __name__.split(".")[1]
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)-8s  " + modnameS +
            "   %(levelname)-8s %(message)s",
            datefmt="%m-%d %H:%M",
            filename=errlogP,
            filemode="w",
        )
        warnings.filterwarnings("ignore")
