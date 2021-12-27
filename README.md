# Csrbox
This repository contains python scripts to verify the generated [CSR module](https://csrbox.readthedocs.io/en/latest/) of the chromite core developed by [InCore Semiconductors](https://incoresemi.com/).
The [CSRBOX](https://csrbox.readthedocs.io/en/latest/) is an external python tool which can generate a bsv CSR module based on the specification provided.

More information about CSRs in RISC-V can be found here: [RISC-V ISA MANUAL](https://riscv.org/wp-content/uploads/2017/05/riscv-privileged-v1.10.pdf)

To generate the assembly test list from the python scripts, use the [UATG tool](https://uatg.readthedocs.io/en/stable/overview.html). Follow the steps given [here](https://uatg.readthedocs.io/en/stable/installation.html).

# CSR 
The Control and Status Register (CSR) are system registers provided by RISC-V to control and monitor system states1. CSR’s can be read, written and bits can be set/cleared. RISC-V provides distinct CSRs for every privilege level. Each CSR has a special name and is assigned a unique function.
Reading and/or writing to a CSR will affect processor operation. CSR’s are used in operations, where a normal register cannot be used. For example, knowing the system configuration, handling exceptions, switching to different privilege modes and handling interrupts are some tasks for which a CSR is needed. The CSR cannot be read/written the way a general register can. A special set of instructions called csr instructions are used to facilitate this process. CSR instructions require an intermediate base register to perform any operation on CSR registers. Further, it is possible to
write immediate values to CSR registers. 

The CSR box is an external python tool which can generate a bsv CSR module based on the specification provided. According to the RISC-V spec, the CSRs are divided into 3 major categories based on the privilege modes supported: Machine, Supervisor and User.
We have verified the Machine CSRs.



# File Structure



# Tests performed



# Description of files

# Contributors





