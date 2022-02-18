import os

from pywps import Process
# from pywps import LiteralInput
from pywps import ComplexInput, ComplexOutput
from pywps import FORMATS
from pywps.app.Common import Metadata
from pywps.app.exceptions import ProcessError

import logging
LOGGER = logging.getLogger("PYWPS")


class ClintAI(Process):
    def __init__(self):
        inputs = [
            ComplexInput('dataset', 'Upload your NetCDF file here',
                         abstract='or enter a URL pointing to a NetCDF file.',
                         min_occurs=0,
                         max_occurs=1,
                         supported_formats=[FORMATS.NETCDF]),
            ComplexInput('dataset_opendap', 'Remote OpenDAP Data URL',
                         abstract="Or provide a remote OpenDAP data URL,"
                                  " for example:"
                                  " http://www.esrl.noaa.gov/psd/thredds/dodsC/Datasets/ncep.reanalysis2.dailyavgs/surface/mslp.2016.nc",  # noqa
                         min_occurs=0,
                         max_occurs=1,
                         supported_formats=[FORMATS.DODS]),
        ]
        outputs = [
            ComplexOutput('output', 'NetCDF Output',
                          abstract='NetCDF Output produced by ClintAI.',
                          as_reference=True,
                          supported_formats=[FORMATS.NETCDF]),
            ComplexOutput('log', 'logfile',
                          abstract='logfile of ClintAI execution.',
                          as_reference=True,
                          supported_formats=[FORMATS.TEXT]),
        ]

        super(ClintAI, self).__init__(
            self._handler,
            identifier="clintai",
            title="ClintAI",
            version="0.1.0",
            abstract="Fills the gaps in your uploaded dataset.",
            metadata=[
                Metadata('Clint AI', 'https://github.com/FREVA-CLINT/climatereconstructionAI'),
                Metadata('Clint Project', 'https://climateintelligence.eu/'),
            ],
            inputs=inputs,
            outputs=outputs,
            status_supported=True,
            store_supported=True,
        )

    def _handler(self, request, response):
        if 'dataset_opendap' in request.inputs:
            dataset = request.inputs['dataset_opendap'][0].url
        elif 'dataset' in request.inputs:
            dataset = request.inputs['dataset'][0].file
        else:
            raise ProcessError("You need to provide a Dataset.")

        response.update_status('starting ...', 0)

        with open(os.path.join(self.workdir, "nc_dump.txt"), 'w') as fp:
            response.outputs['log'].file = fp.name

        response.update_status('done.', 100)
        return response
