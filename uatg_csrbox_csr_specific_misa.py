#This code tests csr specific behaviour of the misa register
#Following code disables M extension thereby disabling mul and div instructions

from yapsy.IPlugin import IPlugin
from ruamel.yaml import YAML
import uatg.regex_formats as rf
from typing import Dict, Union, Any, List
import re
import os

class uatg_csrbox_csr_specific_misa(IPlugin):
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
		self.misa=isa_yaml['hart0']['misa']
		   	
		return True
	def generate_asm(self) -> List[Dict[str, Union[Union[str, list], Any]]]:
	     
		asm=f'\tli x4,0x01\n'
		asm+=f'\tli x8,0x00\n'
		asm+=f'\tli x8,0x02\n'
		asm+=f'\tli x8,0x03\n'   
				
		asm+=f'\tcsrrw x3,misa.M,0x1\n'		#setting misa.M to 1 and trying to execute multiply instruction
		asm+=f'\tmul x7,x6,x5\n'			#legal;should execute
		asm+=f'\tcsrrw x3,misa.M,0x0\n'		#setting misa.M to 0 and trying to execute multiply
		asm+=f'\tmul x7,x6,x5\n'			#should raise interrupt
				
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
