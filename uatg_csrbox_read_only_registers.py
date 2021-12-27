#this code tests the read only informational registers
#there are 4 such registers-mvendorid, marchid,mimpid,mhartid
#Values are obtained from the isa spec


from yapsy.IPlugin import IPlugin
from ruamel.yaml import YAML
import uatg.regex_formats as rf
from typing import Dict, Union, Any, List
import re
import os

class uatg_csrbox_read_only_registers.(IPlugin):
	def __init__(self):
		super().__init__()
		pass
		
	def execute(self, core_yaml, isa_yaml):
		self.isa = isa_yaml['hart0']['ISA']
		if 'RV32' in self.isa:
            		self.isa_bit = 'rv32'
            		self.xlen = 32
            		self.offset_inc = 4
        	else:
            		self.isa_bit = 'rv64'
            		self.xlen = 64
            		self.offset_inc = 8
            		
		self.hart=isa_yaml['hart0']
		self.vendor_reg=hart['mvendorid']
		self.vendor_default=vendor_reg['reset-val']
		
		self.arch_reg=hart['marchid']
		self.arch_default=arch_reg['reset-val']
		
		self.imp_reg=hart['mimpid']
		self.imp_default=imp_reg['reset-val']
		
		self.hart_reg=hart['mhartid']
		self.hart_default=hart_reg['reset-val']
		
		return True
		
	def generate_asm(self) -> List[Dict[str, Union[Union[str, list], Any]]]:
        """
            Generates the ASM instructions for writing to read only registers
        """
        	csr=[self.vendor_reg,self.arch_reg,self.imp_reg,self.hart_reg]
        	
        	asm=f'\tli x3,0x3\n'
        	asm+=f'\tli x2,0x0\n'
        	        	
        	for reg in csr:
        		asm+=f'\tcsrrw x5,{reg},x3\n'
        		asm+=f'\tbne x5,{reg},loop\n'
        	for reg in csr:
        		asm+=f'\tcsrrs x5,{reg},x3\n'
        		asm+=f'\tbne x5,{reg},loop\n'
        	for reg in csr:
        		asm+=f'\tcsrrc x5,{reg},x3\n'
        		asm+=f'\tbne x5,{reg},loop\n'
        	for reg in csr:
        		asm+=f'\tcsrrwi x5,{reg},0x4\n'
        		asm+=f'\tbne x5,{reg},loop\n'
        	for reg in csr:
        		asm+=f'\tcsrrsi x5,{reg},0x4\n'
        		asm+=f'\tbne x5,{reg},loop\n'
        	for reg in csr:
        		asm+=f'\tcsrrci x5,{reg},0x4\n'
        		asm+=f'\tbne x5,{reg},loop\n'
        	asm+=f'loop:\n'
        	asm+=f'\taddi x2,x2,0x1\n'
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
        		
