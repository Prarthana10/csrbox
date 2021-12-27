
from yapsy.IPlugin import IPlugin
from ruamel.yaml import YAML
import uatg.regex_formats as rf
from typing import Dict, Union, Any, List
import re
import os

class uatg_csrbox_misa_c_ext (IPlugin):
	def __init__(self):
		super().__init__()
		pass
		
	def execute(self, core_yaml, isa_yaml):
		self.isa = isa_yaml['hart0']['ISA']
		self.misa = isa_yaml['hart0']['misa']
		
		
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
         asm=f'\tauipc x2,0x0004\n'                                         #making pc 4 byte aligned
    	    asm+=f'\tcsrrc x7,misa, 0x4\n'                                     # disables C ext;x7 willl have old misa value
         asm+=f'\c.li x7,0x500\n'                                           #should raise interrupt
         asm+=f'\tauipc x2,0x0002\n'                                        #making pc 2 byte aligned
         asm+=f'\tcsrrc x7,misa, 0x4\n'                                     # ignores disabling C ext 
         asm+=f'\tc.li x7,0x500 \n'                                         #no interrupt
                  
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



