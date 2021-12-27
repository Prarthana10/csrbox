#this code tests the registers marked WARL
#WARL registers:
#mtvec,misa,mstatus(mpp,fs,mprv),mscratch,mepc,mtval,mcycle,minstret,mideleg,medeleg,mhpmcounter3,mhpmcounter4,mhpmevent3,mhpmevent4
#Range of legal values and illegal values are obtained from the ISA spec
#Following is test
from yapsy.IPlugin import IPlugin
from ruamel.yaml import YAML
import uatg.regex_formats as rf
from typing import Dict, Union, Any, List
import re
import os

class uatg_csrbox_warl_test_misa(IPlugin):
    def __init__(self):
      super().__init__()
      pass

    def execute(self, core_yaml, isa_yaml):
      self.isa = isa_yaml['hart0']['ISA']
      self.misa=isa_yaml['hart0']['misa']
      if 'RV32' in self.isa:
                  self.isa_bit = 'rv32'
                  self.xlen = 32
                  self.offset_inc = 4
      else:
                  self.isa_bit = 'rv64'
                  self.xlen = 64
                  self.offset_inc = 8

      self.mxl_legal=isa_yaml['hart0']['misa']['rv64']['mxl']['type']['warl']['legal']   #assuming legal value is obtained
      self.extensions_bitmask=isa_yaml['hart0']['misa']['rv64']['extensions']['type']['warl']['legal']
      self.default_val=isa_yaml['hart0']['misa']['reset-val']
      return True

    def generate_asm(self) -> List[Dict[str, Union[Union[str, list], Any]]]:
          """
              Generates the ASM instructions for checking warl(write any read legal) registers
          """       
      asm=f'\tli x2,{self.mxl_legal}\n'            				  #load the default value of misa.mxl into x2
      asm+=f'\tli x4,0xffffffffffffffff\n'					        #Load a test value for extensions
      asm+=f'\tcsrrwi x1,misa.mxl,0x4\n'					          #Write an illegal value to misa.mxl
      asm+=f'\tbne x2,x1,loop1\n'						                 #if old value and new value don't match,loop to loop1
      asm+=f'\tbne x1,misa.mxl,loop2\n'					            #if old value and current value in misa.mxl dont match,goto loop2
      asm+=f'\tand x5,x4,{self.extensions_bitmask}\n'  			#test if test value is legal value
      asm+=f'\tneg {self.extensions_bitmask},{self.extensions_bitmask}\n'
      asm+=f'\tand x6,{self.default_val},{self.extensions_bitmask}\n'
      asm+=f'\tori x7,x5,x6\n' 						                  #(write_val&bitmask)|(default_val&~bitmask)
      asm+=f'\tbeq x7,{self.extensions_bitmask},loop\n' 
      asm+=f'loop:\n'
      asm+=f'\tcsrrw x5,misa[25:0],x4' 					            #write to misa.extensions if value is legal
      asm+=f'loop1:\n'
      asm+=f'\taddi x3,x0,1\n'
      asm+=f'loop2\n'
      asm+=f'\taddi x4,x0,1\n'

      # compile macros for the test
      compile_macros = []

      return [{
          'asm_code': asm,
          'asm_sig': '',
          'compile_macros': compile_macros
      }]

    def check_log(self, log_file_path, reports_dir) -> bool:
            return False

    def generate_covergroups(self, config_file) -> str:
            sv = ""
            return sv
        	
        	
        	
        	
        	  
     
            	
            	
            	
