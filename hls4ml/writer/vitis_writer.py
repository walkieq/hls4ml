import os
import glob
from shutil import copy
from hls4ml.writer.vivado_writer import VivadoWriter

class VitisWriter(VivadoWriter):

    def __init__(self):
        super().__init__()

    def write_nnet_utils_overrides(self, model):
        ###################
        ## nnet_utils
        ###################

        filedir = os.path.dirname(os.path.abspath(__file__))

        srcpath = os.path.join(filedir,'../templates/vitis/nnet_utils/')
        dstpath = '{}/firmware/nnet_utils/'.format(model.config.get_output_dir())

        headers = [os.path.basename(h) for h in glob.glob(srcpath + '*.h')]

        for h in headers:
            copy(srcpath + h, dstpath + h)

    def write_hls(self, model):
        """
        Write the HLS project. Calls the steps from VivadoWriter, adapted for Vitis
        """
        super(VitisWriter, self).write_hls(model)
        self.write_nnet_utils_overrides(model)
