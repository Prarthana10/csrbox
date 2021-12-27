#this code tests the read only informational registers
#there are 4 such registers-mvendorid, marchid,mimpid,mhartid
#Values are obtained from the isa spec


from yapsy.IPlugin import IPlugin
from ruamel.yaml import YAML
import uatg.regex_formats as rf
from typing import Dict, Union, Any, List
import re
import os

class uatg_csrbox_minstret (IPlugin):
	def __init__(self):
		super().__init__()
		pass
		
	def execute(self, core_yaml, isa_yaml):
		self.isa = isa_yaml['hart0']['ISA']
		self.minstret = isa_yaml['hart0']['minstret']
		
		
		if 'RV32' in self.isa:
            		self.isa_bit = 'rv32'
            		self.xlen = 32
            		self.offset_inc = 4
        	else:
            		self.isa_bit = 'rv64'
            		self.xlen = 64
            		self.offset_inc = 8
            	
		
				return True
		
	def generate_asm(self) -> List[Dict[str, Union[Union[str, list], Any]]]:
        """
            Generates the ASM instructions for checking warl(write any read legal) registers
        """
         asm=f'\tli x3,0x20 \n'                                          #load x3 with random test value
    	    asm+=f'\tli x7,2\n'                                              #store 'n' (2 in this case)
         asm+=f'\tcsrr x1,minstret \n'                                    #read value of minstret into x1
         asm+=f'\taddi x2,x3,7 \n'                                        #instructions
         asm+=f'\tmul  x4,x2,x3 \n' 
         asm+=f'\tcsrr x5,minstret \n'                                    #read new value of minstret into x5
         asm+=f'\tsub x6,x5,x1 \n'                                        #x6 should have the value 2   
         asm+=f'\tbne x6,x7,end \n'                                       #end shouldnt get executed as minstret has to be incremented by 2     
         asm+=f'end:\n'
         asm+=f'\taddi x2,x0,1 \n'         
          
         
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


