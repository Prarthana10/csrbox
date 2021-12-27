
from yapsy.IPlugin import IPlugin
from ruamel.yaml import YAML
import uatg.regex_formats as rf
from typing import Dict, Union, Any, List
import re
import os

class uatg_csrbox_warl_test_mscratch_mepc (IPlugin):
	def __init__(self):
		super().__init__()
		pass
		
	def execute(self, core_yaml, isa_yaml):
		self.isa = isa_yaml['hart0']['ISA']
		self.mepc = isa_yaml['hart0']['mepc']
		self.mscratch = isa_yaml['hart0']['mscratch']
		
		if 'RV32' in self.isa:
            		self.isa_bit = 'rv32'
            		self.xlen = 32
            		self.offset_inc = 4
        	else:
            		self.isa_bit = 'rv64'
            		self.xlen = 64
            		self.offset_inc = 8
            	
		
		self.bitmask_mepc = isa_yaml['hart0']['mepc']['rv64']['base']['type']['warl']['legal']       #assuming bitmask is obtained for mepc
		self.default_val_mepc = isa_yaml['hart0']['mtepc']['reset-val']
		self.default_val_mscratch = isa_yaml['hart0']['mscratch']['reset-val']

		return True
		
	def generate_asm(self) -> List[Dict[str, Union[Union[str, list], Any]]]:
        """
            Generates the ASM instructions for checking warl(write any read legal) registers
        """
         #mepc
         asm=f'\tli x4,0xfffffffffffffffff\n'                             #load test value to x4 for mepc
         asm+=f'\tand x4,x4,{self.bitmask_mepc}\n'                        #test if x4 is legal value of mepc
         asm+=f'\tneg {self.bitmask_mepc},{self.bitmask_mepc}\n'
         asm+=f'\tand x6,{self.default_val_mepc},{self.bitmask_mepc}\n'
         asm+=f'\tori x7,x5,x6\n'                                          #(write_val & bitmask) | (default_val &~bitmask)  
         asm+=f'\tbeq x7,{self.bitmask_mepc},loop1\n'
         asm+=f'\tli x8,0xffffffff\n'                                       #load test val to x8 for mscratch
         asm+=f'\tcsrrw x3,mscratch[0:63],x8\n'                            #illegal write to mscratch(assuming the notation is right)
         asm+=f'\tbne mscratch[0:63],x3,loop2\n'                            
         asm+=f'loop2:\n'
         asm+=f'\taddi x1,x0,1\n'  
         asm+=f'loop1:\n'
         asm+=f'\tcsrrw x2,mepc[63:0],x4\n'                                 #write to mtvec if value is legal
         
          
         
         compile_macros = []
         
         return [{
         'asm_code': asm,
         'asm_sig': '',
        'compile_macros' : compile_macros
        }] 
        
        	
        def check_log(self, log_file_path, reports_dir) -> bool:
        	return False

    	def generate_covergroups(self, config_file) -> str:
        	sv = ""
        	return sv

