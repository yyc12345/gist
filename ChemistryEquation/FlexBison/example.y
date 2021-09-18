%{
#include <stdio.h>
#include <string.h>

#define COMPILER_RULE_Atom 1
#define COMPILER_RULE_BracketAtomGroup 2
#define COMPILER_RULE_AtomGroup 3
#define COMPILER_RULE_IntervalPart 4
#define COMPILER_RULE_EquationPart 5
#define COMPILER_RULE_EquationSide 6
#define COMPILER_RULE_Equation 7

int elements_length = 118;
char *elements[] = {"H","He","Li","Be","B","C","N","O","F","Ne","Na","Mg","Al","Si","P","S","Cl","Ar","K",
"Ca","Sc","Ti","V","Cr","Mn","Fe","Co","Ni","Cu","Zn","Ga","Ge","As","Se","Br","Kr","Rb","Sr","Y","Zr",
"Nb","Mo","Tc","Ru","Rh","Pd","Ag","Cd","In","Sn","Sb","Te","I","Xe","Cs","Ba","La","Ce","Pr","Nd","Pm",
"Sm","Eu","Gd","Tb","Dy","Ho","Er","Tm","Yb","Lu","Hf","Ta","W","Re","Os","Ir","Pt","Au","Hg","Tl","Pb",
"Bi","Po","At","Rn","Fr","Ra","Ac","Th","Pa","U","Np","Pu","Am","Cm","Bk","Cf","Es","Fm","Md","No","Lr",
"Rf","Db","Sg","Bh","Hs","Mt","Ds","Rg","Cn","Nh","Fl","Mc","Lv","Ts","Og"
};
int get_elements_id(const char* ele_name) {
    int i;
    for(i = 0; i < elements_length; i++) {
        if (strcmp(ele_name, elements[i]) == 0) return i;
    }
    return -1;
}

//int yydebug = 1;
extern FILE * yyin;
extern FILE * yyout;
FILE * binary_file;
void write_binary_int(int value) {
    fwrite(&value, sizeof(value), 1, binary_file);
}

//在lex.yy.c里定义，会被yyparse()调用。在此声明消除编译和链接错误。
extern int yylex(void); 
// 在此声明，消除yacc生成代码时的告警
extern int yyparse(void); 

int yywrap()
{
	return 1;
}

// 该函数在y.tab.c里会被调用，需要在此定义
void yyerror(const char *s)
{
	printf("[ERROR] %s\n", s);
}

int main(int argc, char *argv[])
{
    if (argc != 4) {
        printf("[ERROR] invalid parameter");
        return 1;
    }
    yyin = fopen(argv[1], "r+");
    yyout = fopen(argv[2], "w+");
    binary_file = fopen(argv[3], "w+");
    if (yyin == NULL || yyout == NULL || binary_file == NULL) {
        printf("[ERROR] invalid file");
        return 1;
    }

	yyparse();
    fclose(binary_file);
	return 0;
}
%}

%union
{
int number;
char *string;
}
%token <number> NUMBER
%token <string> ELEMENTS
%token ADD EQUAL LEFT_BRACKET RIGHT_BRACKET INTERVAL BREAK

/*
How the binary data was written in file:

write rule type
write_binary_int(COMPILER_RULE_Atom);
write the matched rule's index of entire rule
write_binary_int(0);
write attach data for current node
write_binary_str($1);
write more data ... etc...

*/

%%
file:
| file equation
{
    fprintf(yyout, "<file>\n\n");
};

equation:
BREAK
{
    write_binary_int(COMPILER_RULE_Equation);
    write_binary_int(1);
    fprintf(yyout, "<equation>(1)\n");
}
| equation_side EQUAL equation_side BREAK
{
    write_binary_int(COMPILER_RULE_Equation);
    write_binary_int(2);
    fprintf(yyout, "<equation>(2)\n");
};

equation_side:
equation_part
{
    write_binary_int(COMPILER_RULE_EquationSide);
    write_binary_int(1);
    fprintf(yyout, "<equation_side>(1)\n");
}
| equation_part ADD equation_side
{
    write_binary_int(COMPILER_RULE_EquationSide);
    write_binary_int(2);
    fprintf(yyout, "<equation_side>(2)\n");
};

equation_part:
interval_part
{
    write_binary_int(COMPILER_RULE_EquationPart);
    write_binary_int(1);
    fprintf(yyout, "<equation_part>(1)\n");
}
| equation_part INTERVAL interval_part
{
    write_binary_int(COMPILER_RULE_EquationPart);
    write_binary_int(2);
    fprintf(yyout, "<equation_part>(2)\n");
};

interval_part:
atom_group
{
    write_binary_int(COMPILER_RULE_IntervalPart);
    write_binary_int(1);
    fprintf(yyout, "<interval_part>(1)\n");
}
| NUMBER atom_group
{
    write_binary_int(COMPILER_RULE_IntervalPart);
    write_binary_int(2);
    write_binary_int($1);
    fprintf(yyout, "%d <interval_part>(2)\n", $1);
};

// CuSO4 H2SO4 HCl etc...
atom_group:
atom
{
    write_binary_int(COMPILER_RULE_AtomGroup);
    write_binary_int(1);
    fprintf(yyout, "<atom_group>(1) ");
}
| bracket_atom_group
{
    write_binary_int(COMPILER_RULE_AtomGroup);
    write_binary_int(2);
    fprintf(yyout, "<atom_group>(2) ");
}
| atom_group atom
{
    write_binary_int(COMPILER_RULE_AtomGroup);
    write_binary_int(3);
    fprintf(yyout, "<atom_group>(3) ");
}
| atom_group bracket_atom_group
{
    write_binary_int(COMPILER_RULE_AtomGroup);
    write_binary_int(4);
    fprintf(yyout, "<atom_group>(4) ");
};

bracket_atom_group:
LEFT_BRACKET atom_group RIGHT_BRACKET
{
    write_binary_int(COMPILER_RULE_BracketAtomGroup);
    write_binary_int(1);
    fprintf(yyout, "<bracket_atom_group>(1)\n");
}
| LEFT_BRACKET atom_group RIGHT_BRACKET NUMBER
{
    write_binary_int(COMPILER_RULE_BracketAtomGroup);
    write_binary_int(2);
    write_binary_int($4);
    fprintf(yyout, "%d <bracket_atom_group>(2)\n", $4);
};

atom:
ELEMENTS
{
    write_binary_int(COMPILER_RULE_Atom);
    write_binary_int(1);
    write_binary_int(get_elements_id($1));
    fprintf(yyout, "%s <atom>(1) ", $1);
}
| ELEMENTS NUMBER
{
    write_binary_int(COMPILER_RULE_Atom);
    write_binary_int(2);
    write_binary_int(get_elements_id($1));
    write_binary_int($2);
    fprintf(yyout, "%s %d <atom>(2) ", $1, $2);
};

%%