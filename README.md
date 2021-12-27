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

- For the CSRs which are read-only we are checking if the CSRs hold the same value even after writing a different value using all CSR instructions. 

#### uatg_csrbox_warl_test_misa.py
- This code tests generates tests to check the WARL property of the ```misa``` register.

- ```misa``` has two fields, ```mxl[1:0]``` and an extensions field which is 26 bits wide,which have the WARL property.

- Legal values for the two fields are obtained from the ISA spec. 

- For ```misa.mxl```,illegal write is performed.A branch condition has been used to check if the write was successful.Contents of register ```x3``` will be incremented in case the value was changed.

- We are testing if the reset value of the misa is alegal value and if it matches the reset value in the ISA spec.
 
- Similarly for ```misa.extensions```, the test write_val is first checked if it is legal.If the value is legal,its written into ```misa.extensions```.  

#### uatg_csrbox_warl_test_mtvec.py
- This code tests generates tests to check the WARL property of the ```mtvec``` register.

- Machine Trap Vector Base Address (MTVEC) register is used to store the address of the Trap handler.In simple terms mtvec tells where to trap.

- The ```mtvec``` register has the address of the trap handler. When a trap occurs, the hardware set’s the program counter (PC) set to the value in the ```mtvec``` register. This causes a jump to the first instruction in the trap handler routine.

- Some basic properties of ```mtvec``` register is:
      - BASE must always be aligned on a 4-byte boundary
      - BASE can be hardwired to hold a constant
      - MODE is irect then pc is set to BASE
      - MODE is vectored when pc is set to BASE + 4*(cause)

- We are testing if the reset value of the ```mtvec``` is a legal value and if it matches the reset value in the ISA spec.


#### uatg_csrbox_warl_test_mstatus.py
- ```mstatus``` register encodes the contents of the floating point/accelerator architectural state.

- Setting the ```mstatus.fs``` will enable floating point instructions and clearing it will disable the same.```mstatus.fs``` is also WARL.  

- We have conducted one test by making an illegal write operation to the fs bits.

- Another test is performed by executing ```fmul``` instruction after clearing the fs bits,and executing it again by setting the fs bits. The former should raise an illegal trap.

- ```mstatus.mprv``` ,bits that modify priviledge levels for registers,is also WARL, which is tested by performing an illegal write operation.


#### uatg_csrbox_warl_test_mscratch_mepc.py
- This code tests generates tests to check the WARL property of the ```mscratch``` and ```mepc``` registers.

- Machine Exception Program Counter (MEPC) is an XLEN-bit read/write register, which holds the address of the instruction which resulted in a trap.

- Some basic properties about ```mepc``` register:
      - It is written with virtual address of the instruction at which a trap was taken in machine mode.
      - ```mepc``` = 0 always
      - When IALIGN = 32, ```mepc```[1:0] = 0

- ```mepc``` register cannot hold a program counter (pc) value that would cause an Instruction Address Misaligned exception.

-  Scratch Register (MSCRATCH) for Machine Mode Trap Handler. This register allows us to store the context of trap handlers in other privilege levels. This is of much use only in case of system switching privilege modes.

- In order to prevent overwrite and lose of the previous values, when a machine mode trap handler is invoked, the use of at least one general purpose register is needed.

- ```mscratch``` gives the software a register loaded with a base value, which can subsequently be used to save all remaining processor state.

- Some basic properties about ```mscratch``` register:
   - It is a read/write register.
   -  Useful as temporary storage in save/restore routines.

- In simple terms ```mscratch``` and ```mepc``` tell us how to return from a trap.


#### uatg_csrbox_csr_specific_misa.py
- This code tests 

- The above registers are read-only and the values are pre-coded and obtained from the ISA spec

- All the csr access instructions, ```csrrw```,```csrrs```,```csrrc``` and their immediate variants,```csrrwi```,```csrrsi```,```csrrci``` are used and a test value is written

- Illegal exception has to be raised for writing into those registers

#### uatg_csrbox_misa_c_ext.py
- This code tests generates tests to write 

- 

- Disabling the misa.C extension requires the CSR instruction to be 4 byte aligned. else the disabling will be ignored. 

- 

#### uatg_csrbox_minstret.py
- This code tests generates tests to write ```minstret```

- We read ```minstret```, execute n operations and check if the ```minstret``` value must be +n from the previous readings.

- The ```minstret``` CSR holds a count of the number of instructions the hart has retired since some arbitrary time in the past. 

- 


## Contributors
Prarthana Bhat (<prarthana.bhat20@gmail.com> )

B.N. Vismaya( <vismayanavile@gmail.com> )




