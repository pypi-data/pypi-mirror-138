from replifactory.culture.blank import BlankCulture
from replifactory.culture.culture_functions import dilute_adjust_drug1
import numpy as np
import time


class ChemostatCulture(BlankCulture):
    """
    Implements a quasi-turbidostat culture in a multi-vial device.
    A discrete dilution is made when the OD reaches the threshold,
    allowing the pumps to sequentially maintain all 7 vials.
    The growth is more similar to a real, continuous-dilution turbidostat
    when the dilution factor is small and dilutions are made more frequently.
    """
    pumps = (1, 4)

    def __init__(self, directory: str = None, vial_number: int = None, name: str = "Species 1",
                 description: str = "Strain 1", default_dilution_volume: float = 10,
                 dead_volume: float = 15):
        # Configuration parameters
        self.default_dilution_volume = default_dilution_volume
        self.dead_volume = dead_volume
        #         self.od_max_limit = od_max_limit
        self.dilution_period_mins = 30
        self.medium2_c_target = 0

        # Running parameters
        super().__init__(directory=directory, vial_number=vial_number, name=name, description=description)

    def lower_od(self):
        dilute_adjust_drug1(culture=self, target_concentration=self.medium2_c_target)

    def make_chemostat_dilution(self):
        self.lower_od()

    # def make_custom_schedule(self):
    #     self.scheduler = schedule.Scheduler()
    #     self.scheduler.every(self.dilution_period_min).minutes.do(self.make_chemostat_dilution)

    def update(self):
        """
        called every minute
        """
        # if self.scheduler is None:
        #     self.make_custom_schedule()
        # if self.scheduler.jobs[0].period.seconds != self.dilution_period_min * 60:
        #     self.make_custom_schedule()
        if self.is_active():
            self.update_growth_rate()
            if time.time() - self._last_dilution_start_time >= self.dilution_period_mins * 60 - 55:
                self.make_chemostat_dilution()

            # self.scheduler.run_pending()

    def description_text(self):
        vial_volume = self.dead_volume
        added_volume = self.default_dilution_volume
        dilution_factor = (vial_volume + added_volume) / vial_volume
        generations_per_dilution = np.log2(dilution_factor)
        generations_per_l = 1000 * generations_per_dilution / added_volume
        flow_rate = self.default_dilution_volume / (self.dilution_period_mins / 60)  # mL/h
        #         dilution_rate_per_hr = flow_rate/self.dead_volume

        dilution_rate_per_hr = np.log(dilution_factor) / (self.dilution_period_mins / 60)
        td = np.log(2) / dilution_rate_per_hr

        t = f"""The {self.dead_volume:.1f}mL culture is diluted with {self.default_dilution_volume:.1f}mL every {self.dilution_period_mins:.0f} min.
dilution factor: 1/{dilution_factor:.2f} ({generations_per_dilution:.2f} generations/dilution) 
     medium use: {flow_rate:.2f} mL/h  ({1000/generations_per_l:.1f} mL/generation)
  doubling time: {td*60:.1f} min (growth rate: {dilution_rate_per_hr:.2f}/h)"""
        return t
