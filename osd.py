import nec_tables

def lookup(lookup_value, lst):
    for value in lst:
        if lookup_value <= value:
            return value

class  Circuit(object):
    """docstring for circuits.
    parent class for dc and ac circuits
    Attributes
    ----------
    name: string
    start: string
        originating equipment of the circuit
    end: string
        terminating equipment of the circuit
    voltage: int
        design voltage for circuit- 480, 277, 120, 12470
    current: float
    length: float
        length of circuit in feet
    parallel_sets: int
        number of paralle sets of conductors
    ccc_count: int
        Current carrying conductors per conduit. Does not include neutral.
        For the conditions of use derate calculations
    height_above_roof: float
        height above roof in inches
    temp_high_amb: float
        Degrees Fahrenheit
        Recommended ASHRAE design 2 percent high
        Passed by parent class in future?
    cond_material: string
        Conductor metal as "Cu" or "Al"
    cond_insulation: string
        Conductor insulation type
    cond_size_base: string
    egc_material: string
        Equipment ground condcutor metal as "Cu" or "Al"
    egc_size_base: string
        Equipment ground condcutor size
    neutral: int
        Use 1 to include neutral in conduit size calculation.
        Integer > 1 to add condcutors the same size as the currenty carrying
    conduit_size_SF: float
        Safety factor for conduit size calculation.
        Default is 1.3
    conduit_type: string

    Internal Attributes
    ___________________
    ocpd
    rooftop_adder
    cond_size_base
    egc_size_base
    v_drop_volts
    v_drop_percent
    v_drop_in_range
    conduit_size

    """
    def __init__(self, name=None, start=None, end=None,
                 voltage=None, current=None, length=None, parallel_sets=1,
                 ccc_count=3, height_above_roof=3.5, temp_high_amb=None,
                 cond_metal=None, cond_insulation=None, cond_size=None,
                 egc_metal='Cu', egc_size_base=None, neutral=1, conduit_size_SF=1.3,
                 conduit_type='EMT'):
        super(Circuit, self).__init__()
        self.name = name
        self.start = start
        self.end = end
        self.voltage = voltage
        self.current = current
        self.length = length
        self.parallel_sets = parallel_sets
        self.ccc_count = ccc_count
        self.height_above_roof = height_above_roof
        self.temp_high_amb = temp_high_amb
        self.cond_metal = cond_metal
        self.cond_insulation = cond_insulation
        self.cond_size = cond_size
        self.egc_metal = egc_metal
        self.egc_size_base = egc_size_base
        self.neutral = neutral
        self.conduit_size_SF = conduit_size_SF
        self.conduit_type = conduit_type

        self.ocpd = lookup(self.current * 1.25, nec_tables.ocpd_sizes)

    def _update_attribute(self, arg):
        """
        Set attribute and recalulate dependent values.
        """
        pass

    def _get_amb_temp_plus_rooftop_adder(self):
        """[Needs to be updated]
        Table removed in NEC 2017 (now only a single value), valid for 2008, 2011, 2014
        Temperatures in Fahrenheit
        """
        if self.height_above_roof == -1:
            return self.temp_high_amb
        elif self.height_above_roof <= 0.5:
            return self.temp_high_amb + 60
        elif self.height_above_roof <= 3.5:
            return self.temp_high_amb + 40
        elif self.height_above_roof <= 12:
            return self.temp_high_amb + 30
        elif self.height_above_roof <= 36:
            return self.temp_high_amb + 25
        elif self.height_above_roof > 36:
            return self.temp_high_amb + 0

    def _amb_temp_correction(self):
        """[Needs to be updated]
        NEC 310.15(B)(2) Ambient Temperatue Correction Factors.
        Temp of conductor assumed to be 90C 194F
        Table temp from 310.15(B)(16) of 30C 86F
        """
        t_amb = self._get_amb_temp_plus_rooftop_adder()
        return(((194.0 - t_amb) / (194.0 - 86)) ** 0.5)

    def _cond_per_raceway_derate(self):
        """[Needs to be updated]
        NEC 310.15(B)(3)(a) Adjustment factors for more than three
        current-carrying conductors in a raceway or cable
        """
        if self.ccc_count < 4:
            return(1.0)
        elif self.ccc_count <= 6:
            return(0.8)
        elif self.ccc_count <= 9:
            return(0.7)
        elif self.ccc_count <= 20:
            return(0.5)
        elif self.ccc_count <= 30:
            return(0.45)
        elif self.ccc_count <= 40:
            return(0.4)
        elif self.ccc_count >= 41:
            return(0.35)


class DcCircuit(Circuit):
    """docstring for DcCircuit.
    Class for AC circuits.

    """
    def __init__(self, name=None, ccc_count=2):
        super(DcCircuit, self).__init__()
        self.name = name
        self.ccc_count = ccc_count

class AcCircuit(Circuit):
    """docstring for AcCircuit.
    Class for AC circuits.
    """
    def __init__(self, arg):
        super(AcCircuit, self).__init__()
        self.arg = arg

if __name__ == '__main__':
    main()
