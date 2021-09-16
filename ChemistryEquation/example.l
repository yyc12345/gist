%{
#include <stdio.h>
#include "y.tab.h"
%}

%%
H|He|Li|Be|B|C|N|O|F|Ne|Na|Mg|Al|Si|P|S|Cl|Ar|K|Ca|Sc|Ti|V|Cr|Mn|Fe|Co|Ni|Cu|Zn|Ga|Ge|As|Se|Br|Kr|Rb|Sr|Y|Zr|Nb|Mo|Tc|Ru|Rh|Pd|Ag|Cd|In|Sn|Sb|Te|I|Xe|Cs|Ba|La|Ce|Pr|Nd|Pm|Sm|Eu|Gd|Tb|Dy|Ho|Er|Tm|Yb|Lu|Hf|Ta|W|Re|Os|Ir|Pt|Au|Hg|Tl|Pb|Bi|Po|At|Rn|Fr|Ra|Ac|Th|Pa|U|Np|Pu|Am|Cm|Bk|Cf|Es|Fm|Md|No|Lr|Rf|Db|Sg|Bh|Hs|Mt|Ds|Rg|Cn|Nh|Fl|Mc|Lv|Ts|Og printf("ELEMENTS<%s> ", yytext); return ELEMENTS;
[1-9][0-9]* printf("NUMBER<%s> ", yytext); return NUMBER;
\+ printf("ADD "); return ADD;
= printf("EQUAL "); return EQUAL;
\( printf("LEFT_BRACKET "); return LEFT_BRACKET;
\) printf("RIGHT_BRACKET "); return RIGHT_BRACKET;
· printf("INTERVAL "); return INTERVAL;
\n printf("BREAK\n"); return BREAK;
[ \t]+ /* ignore whitespace */;
%%