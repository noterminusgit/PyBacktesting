"""Module to run the program - use optimization tool if asked"""
from pnl import PnL
from manip_data import ManipData as md
from date_manip import DateManip as dm
from optimize.genetic_algorithm import GenAlgo as ga
from indicator import Indicator

class Optimize(PnL):

    def __init__(self):
        super().__init__()
        self.init_series()
        self.reset_value()

    def __call__(self):

        # If we optimize
        if self.is_walkfoward:
            self.walk_foward()
        else :
            self.pnl_()
            self.first_write = md.write_csv_(self.dir_output, self.name_out, self.first_write, add_doc="",
                                             is_walkfoward=self.is_walkfoward, **self.pnl_dict)

    def execute_(self,add_doc=""):
        """ Just runs the whole program without optimization

         Load data (and clean), calculate indicators, check for signal, calculate pnl + write results to file
         """


    def walk_foward(self):
        md_ = md

        _first_time = True
        self.dict_date_ = dm.date_dict(self.date_debut, self.date_fin,
                                       **self.dict_name_)

        if (len(self.dict_date_)) == 0:
            raise Exception("Total period not long enough for optimization")

        for key,_ in self.dict_date_.items():
            for key_, _ in self.dict_name_.items():
                self.date_debut = self.dict_date_[key][key_][0]
                self.date_fin = self.dict_date_[key][key_][1]
                if _first_time :
                    md_(self.dir_output,self.name_out,extension = key_).erase_content()
                self.init_series()
                Indicator.calcul_indicator(self)
                if key_ == self.training_name_: #we only optimize for the training period
                    self.optimize_param()
                    self.pnl_dict,self.op_param = ga(self).__call__()
                else : #test period, we use the optimized parameters in the training period
                    self.pnl_()

                md.write_csv_(self.dir_output, self.name_out, add_doc=key_,
                              is_walkfoward=self.is_walkfoward, **self.pnl_dict)
                md.write_csv_(self.dir_output, self.name_out, add_doc=key_,
                              is_walkfoward=self.is_walkfoward, **self.op_param)

            _first_time = False