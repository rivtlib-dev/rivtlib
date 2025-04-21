import logging
import re
import sys
import warnings


class RvT:
    """ tools commands 

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

        self.cmdL = ["python"]
        self.tagsD = {}
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
