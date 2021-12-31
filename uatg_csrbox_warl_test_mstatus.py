#this code tests the registers marked WARL
#WARL registers:
#mtvec,misa,mstatus(mpp,fs,mprv),mscratch,mepc,mtval,mcycle,minstret,mideleg,medeleg,mhpmcounter3,mhpmcounter4,mhpmevent3,mhpmevent4
#Range of legal values and illegal values are obtained from the ISA spec
#Following is test for mstatus WARL fields

from yapsy.IPlugin import IPlugin
from ruamel.yaml import YAML
import uatg.regex_formats as rf
from typing import Dict, Union, Any, List
import re
import os

class uatg_csrbox_warl_test_mstatus(IPlugin):
	def __init__(self):
		super().__init__()
		pass
		
	def execute(self, core_yaml, isa_yaml):
		self.isa = isa_yaml['hart0']['ISA']
		self.mstatus=isa_yaml['hart0']['mstatus']
		
		if 'RV32' in self.isa:
			self.isa_bit = 'rv32'
			self.xlen = 32
			self.offset_inc = 4
		else:
			self.isa_bit = 'rv64'
			self.xlen = 64
			self.offset_inc = 8
            	
		self.fs_legal=isa_yaml['hart0']['mstatus']['rv64']['fs']['type']['warl']['legal']   #assuming legal value is obtained
            	
            	
		self.mprv_legal=isa_yaml['hart0']['mstatus']['rv64']['mprv']['type']['warl']['legal']
            	
            	
		self.reset_val=isa_yaml['hart0']['mstatus']['reset-val']
            	
		return True
	
	def generate_asm(self) -> List[Dict[str, Union[Union[str, list], Any]]]:
              
		asm=f'\tli x2,0x34\n'            				#load test float value
		asm=f'\tli x8,0x56\n'
		asm=f'\tcsrrw x4,mstatus.fs,0x04\n' 				#writing illegal values to fs
		asm+=f'\tbe {self.fs_legal},mstatus.fs,loop1\n'					
		asm+=f'\tcsrrw x4,mstatus.fs,0x00\n'					#setting fs to 0 and trying to execute float inst after that
		asm+=f'\tfmul x7,x8\n'						
		asm+=f'\tcsrrw x4,mstatus.mprv,0x05 \n'				#illegal writ
		asm+=f'\tbe {self.mprv_legal},mstatus.mprv,loop2\n'  			
		asm+=f'\tcsrrw x5,mstatus.mprv,0x00\n'				#legal write
		asm+=f'\tbe x5,mstatus.mprv,loop3\n'
		asm+=f'loop1:\n'
		asm+=f'\taddi x7,x0,1' 					
		asm+=f'loop2:\n'
		asm+=f'\taddi x7,x0,1 \n'
		asm+=f'loop3:\n'
		asm+=f'\taddi x8,x0,1\n'
        	
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
