""" Imports """
import os
from hetch_utilities import log


def run_freshclam():
    """ Download freshclam signatures database """
    log("Downloading up Freshclam signatures")
    log(os.system("freshclam"))

    """ Restart the ClamdAV Daemon service. """
    log("Restarting the ClamAV Daemon service...")
    log(os.system("service clamav-daemon restart"))
    log("ClamdAV service started.")