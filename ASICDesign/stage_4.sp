* Shit test
* Parameters and models
.options post=1 list
.MODEL MP PMOS (LEVEL=1 VTO=-0.4 KP=30u GAMMA=0.4 LAMBDA=0.1)
.MODEL MN NMOS (LEVEL=1 VTO=0.4  KP=115u GAMMA=0.4 LAMBDA=0.06)

* Simulation netlist and Stimulus
* MOS format: node_name S G D SUB
MP1     6   0   5   6   MP L=0.25u W=0.375u
MN1     5   1   9   0   MN L=0.25u W=1.5u
MN2     9   2   8   0   MN L=0.25u W=1.5u
MN3     8   3   7   0   MN L=0.25u W=1.5u
MN4     7   4   0   0   MN L=0.25u W=1.5u
VDD     6   0   DC  5
VIN1    1   0   DC  0
VIN2    2   0   DC  5
VIN3    3   0   DC  5
VIN4    4   0   DC  5

* Stimulus
.dc     VIN1    0   5   0.1

.END