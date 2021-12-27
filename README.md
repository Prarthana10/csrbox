# Csrbox
This repository contains python scripts to verify the generated [CSR module](https://csrbox.readthedocs.io/en/latest/) of the chromite core developed by [InCore Semiconductors](https://incoresemi.com/).
The [CSRBOX](https://csrbox.readthedocs.io/en/latest/) is an external python tool which can generate a bsv CSR module based on the specification provided.

More information about CSRs in RISC-V can be found here: [RISC-V ISA MANUAL](https://riscv.org/wp-content/uploads/2017/05/riscv-privileged-v1.10.pdf)

To generate the assembly test list from the python scripts, use the [UATG tool](https://uatg.readthedocs.io/en/stable/overview.html). Follow the steps given [here](https://uatg.readthedocs.io/en/stable/installation.html).

## CSR 
The Control and Status Register (CSR) are system registers provided by RISC-V to control and monitor system states. CSRs can be read, written and bits can be set/cleared. RISC-V provides distinct CSRs for every privilege level. Each CSR has a special name and is assigned a unique function.
Reading and/or writing to a CSR will affect processor operation. CSR’s are used in operations, where a normal register cannot be used. For example, knowing the system configuration, handling exceptions, switching to different privilege modes and handling interrupts are some tasks for which a CSR is needed. The CSR cannot be read/written the way a general register can. A special set of instructions called csr instructions are used to facilitate this process. CSR instructions require an intermediate base register to perform any operation on CSR registers. Further, it is possible to write immediate values to CSR registers. 

The CSR box is an external python tool which can generate a bsv CSR module based on the specification provided. According to the RISC-V spec, the CSRs are divided into 3 major categories based on the privilege modes supported: Machine, Supervisor and User.
We have verified the Machine CSRs.



## File Structure

```bash
├── reference assembly codes
│   ├── test1.txt
|   └── test2.txt
|   └── test3.txt
|   └── test4.txt
│   └── test5.txt
├── README.md -- Describes the idea behind each test
├── uatg_csrbox_read_only_registers.py -- Generates ASM to check whether the CSRs hold the same value,even after using different csr instructions
├── uatg_csrbox_warl_test_misa.py -- Generates ASM to check whether reset value of misa matches the ISA spec
├── uatg_csrbox_warl_test_mtvec.py -- Generates ASM to check whether reset value of mtvec matches the ISA spec
├── uatg_csrbox_warl_test_mscratch_mepc.py -- Generates ASM to check whether reset value of mscratch,mepc matches the ISA spec
├── uatg_csrbox_warl_test_mstatus.py -- Generates ASM to check whether reset value of mstatus matches the ISA spec
├── uatg_csrbox_csr_specific_misa.py -- Generates ASM to check the .M extension of misa
├── uatg_csrbox_misa_c_ext.py -- Generates ASM to check .C extension of misa
└── uatg_csrbox_minstret.py -- Generates ASM to check whether minstret is being correctly incremented

```

## Description of files
#### uatg_csrbox_read_only_registers.py
- This code tests generates tests to write to read-only registers: ```mvendorid```, ```marchid``` ,```mimpid```,```mhartid```

- The above registers are read-only and the values are pre-coded and obtained from the ISA spec

- All the csr access instructions, ```csrrw```,```csrrs```,```csrrc``` and their immediate variants,```csrrwi```,```csrrsi```,```csrrci``` are used and a test value is written

- Illegal exception has to be raised for writing into those registers

#### uatg_csrbox_warl_test_misa.py
- This code tests generates tests to write to check the WARL property of the ```misa``` register.

- ```misa``` has two fields, ```mxl[1:0]``` and an extensions field which is 26 bits wide,which have the WARL property.

- Legal values for the two fields are obtained from the ISA spec. 

- For ```misa.mxl```,illegal write is performed.A branch condition has been used to check if the write was successful.Contents of register ```x3``` will be incremented in case the value was changed.
- Similarly for ```misa.extensions```, the test write_val is first checked if it is legal.If the value is legal,its written into ```misa.extensions```.  

#### uatg_csrbox_warl_test_mtvec.py
- This code tests generates tests to write to read-only registers: ```mvendorid```, ```marchid``` ,```mimpid```,```mhartid```

- The above registers are read-only and the values are pre-coded and obtained from the ISA spec

- All the csr access instructions, ```csrrw```,```csrrs```,```csrrc``` and their immediate variants,```csrrwi```,```csrrsi```,```csrrci``` are used and a test value is written

- Illegal exception has to be raised for writing into those registers

#### uatg_csrbox_warl_test_mstatus.py
- ```mstatus``` register encodes the contents of the floating point/accelerator architectural state.

- Setting the ```mstatus.fs``` will enable floating point instructions and clearing it will disable the same.```mstatus.fs``` is also WARL.  

- We have conducted one test by making an illegal write operation to the fs bits.

- Another test is performed by executing ```fmul``` instruction after clearing the fs bits,and executing it again by setting the fs bits. The former should raise an illegal trap.
- ```mstatus.mprv``` ,bits that modify priviledge levels for registers,is also WARL, which is tested by performing an illegal write operation.


#### uatg_csrbox_warl_test_mscratch_mepc.py
- This code tests generates tests to write to read-only registers: ```mvendorid```, ```marchid``` ,```mimpid```,```mhartid```

- The above registers are read-only and the values are pre-coded and obtained from the ISA spec

- All the csr access instructions, ```csrrw```,```csrrs```,```csrrc``` and their immediate variants,```csrrwi```,```csrrsi```,```csrrci``` are used and a test value is written

- Illegal exception has to be raised for writing into those registers

#### uatg_csrbox_csr_specific_misa.py
- This code tests 

- The above registers are read-only and the values are pre-coded and obtained from the ISA spec

- All the csr access instructions, ```csrrw```,```csrrs```,```csrrc``` and their immediate variants,```csrrwi```,```csrrsi```,```csrrci``` are used and a test value is written

- Illegal exception has to be raised for writing into those registers

#### uatg_csrbox_misa_c_ext.py
- This code tests generates tests to write to read-only registers: ```mvendorid```, ```marchid``` ,```mimpid```,```mhartid```

- The above registers are read-only and the values are pre-coded and obtained from the ISA spec

- All the csr access instructions, ```csrrw```,```csrrs```,```csrrc``` and their immediate variants,```csrrwi```,```csrrsi```,```csrrci``` are used and a test value is written

- Illegal exception has to be raised for writing into those registers

#### uatg_csrbox_minstret.py
- This code tests generates tests to write to read-only registers: ```mvendorid```, ```marchid``` ,```mimpid```,```mhartid```

- The above registers are read-only and the values are pre-coded and obtained from the ISA spec

- All the csr access instructions, ```csrrw```,```csrrs```,```csrrc``` and their immediate variants,```csrrwi```,```csrrsi```,```csrrci``` are used and a test value is written

- Illegal exception has to be raised for writing into those registers


## Contributors
Prarthana Bhat (<prarthana.bhat20@gmail.com> )

B.N. Vismaya( <vismayanavile@gmail.com> )




