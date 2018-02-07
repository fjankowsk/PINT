from __future__ import absolute_import, print_function, division
from pint import ls,GMsun,Tsun
from .stand_alone_psr_binaries.DDK_model import DDKmodel
from .binary_dd import BinaryDD
from . import parameter as p
from .timing_model import MissingParameter
import astropy.units as u
from astropy import log


class BinaryDDK(BinaryDD):
    """This is a PINT pulsar binary ddk model class a subclass of DD model.
    It is a wrapper for independent DDKmodel class defined in
    ./stand_alone_psr_binary/DDK_model.py
    All the detailed calculations are in the independent DDKmodel.
    The aim for this class is to connect the independent binary model with PINT platform
    DDKmodel special parameters:
    KIN inclination angle
    KOM the longitude of the ascending node, Kopeikin (1995) Eq 9. OMEGA
    Reference
    ---------
    KOPEIKIN. 1995, 1996
    """
    register = True
    def __init__(self,):
        super(BinaryDDK, self).__init__()
        self.binary_model_name = 'DDK'
        self.binary_model_class = DDKmodel

        self.add_param(p.floatParameter(name='KIN', value=0.0, units="deg",
                       description="Inclination angle"))
        self.add_param(p.floatParameter(name='KOM', value=0.0, units="deg",
                       description="The longitude of the ascending node"))
        self.add_param(p.boolParameter(name='K96',
                       description="Flag for Kopeikin binary model proper motion" + \
                       " correction"))
        self.interal_params += ['PMRA_DDK', 'PMDEC_DDK']

    @property
    def PMRA_DDK(self):
        params = self.get_params_as_ICRS()
        par_obj = p.floatParameter(name="PMRA",
            units="mas/year", value=params["PMRA"],
            description="Proper motion in RA")
        return par_obj

    @property
    def PMDEC_DDK(self):
        params = self.get_params_as_ICRS()
        par_obj = p.floatParameter(name="PMDEC",
            units="mas/year", value=params["PMDEC"],
            description="Proper motion in DEC")
        return par_obj


    def setup(self):
        """Check out parameters setup.
        """
        super(BinaryDDK,self).setup()
        log.info("Using ICRS equatorial coordinate. The parameter KOM is"
                 " measured respect to equatorial North.")
        if 'PMRA' not in self._parent.params or 'PMDEC' not in self._parent.params:
            # Check ecliptic coordinates proper motion.
            if 'PMELONG' not in self._parent.params or 'PMELAT' not in self._parent.params:
                raise MissingParameter("DDK", "DDK model needs proper motion parameters.")