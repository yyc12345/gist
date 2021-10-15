* Shit test
* Parameters and models
.options post=1 list
.MODEL MP PMOS (LEVEL=1 VTO=-0.4 KP=30u GAMMA=0.4 LAMBDA=0.1)
.MODEL MN NMOS (LEVEL=1 VTO=0.4  KP=115u GAMMA=0.4 LAMBDA=0.06)

* Simulation netlist and Stimulus
* MOS format: node_name S G D SUB
MP1     6   0   5   6   MP L=0.25u W=0.375u
MN1     5   1   9   0   MN L=0.25u W=0.375u
MN2     9   2   8   0   MN L=0.25u W=0.375u
MN3     8   3   7   0   MN L=0.25u W=0.375u
MN4     7   4   0   0   MN L=0.25u W=0.375u
VDD     6   0   DC  5
VIN1    1   0   PWL(0   0   8n     0       10n     5       18n     5   20n     0    R)
VIN2    2   0   PWL(0   0   18n    0       20n     5       38n     5   40n     0    R)
VIN3    3   0   PWL(0   0   38n    0       40n     5       78n     5   80n     0    R)
VIN4    4   0   PWL(0   0   78n    0       80n     5       158n    5   160n    0    R)

* Stimulus
.tran  4n 200n

.END