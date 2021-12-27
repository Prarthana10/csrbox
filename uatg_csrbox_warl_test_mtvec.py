#this code tests the read only informational registers
#there are 4 such registers-mvendorid, marchid,mimpid,mhartid
#Values are obtained from the isa spec


from yapsy.IPlugin import IPlugin
from ruamel.yaml import YAML
import uatg.regex_formats as rf
from typing import Dict, Union, Any, List
import re
import os

class uatg_csrbox_warl_test_mtvec.(IPlugin):
	def __init__(self):
		super().__init__()
		pass
		
	def execute(self, core_yaml, isa_yaml):
		self.isa = isa_yaml['hart0']['ISA']
		self.mtvec = isa_yaml['hart0']['mtvec']
		if 'RV32' in self.isa:
            		self.isa_bit = 'rv32'
            		self.xlen = 32
            		self.offset_inc = 4
        	else:
            		self.isa_bit = 'rv64'
            		self.xlen = 64
            		self.offset_inc = 8
            	
		self.bitmask = isa_yaml['hart0']['mtvec']['rv64']['base']['type']['warl']['legal']       #assuming bitmask is obtained
		self.default_val = isa_yaml['hart0']['mtvec']['reset-val']
		 
	        return True
		
	def generate_asm(self) -> List[Dict[str, Union[Union[str, list], Any]]]:
        """
            Generates the ASM instructions for checking warl(write any read legal) registers
        """
        	asm=f'\tli x4,0xfffffffffffffffff\n'                    #load test value to x4
        	asm+=f'\tand x5,x4,{self.bitmask}\n'                   #test if x4 is legal value
        	asm+=f'\tneg {self.bitmask},{self.bitmask}\n'
        	asm+=f'\tand x6,{self.default_val},{self.bitmask}\n'
        	asm+=f'\tori x7,x5,x6\n'                                #(write_val & bitmask) | (default_val &~bitmask)   
        	asm+=f'\tbeq x7,{self.bitmask},loop\n'
        	asm+=f'loop:\n'
        	asm+=f'\tcsrrw x5,mtvec[61:0],x4\n'                      #write to mtvec if value is legal   
         
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
