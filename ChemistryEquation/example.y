%{
#include <stdio.h>
#include <string.h>

int yydebug = 1;

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

int main()
{
	yyparse();
	return 0;
}
%}

%token ELEMENTS NUMBER ADD EQUAL LEFT_BRACKET RIGHT_BRACKET INTERVAL BREAK

%%
file:
| file equation
{
    printf("<file>\n");
};

equation:
BREAK
| equation_side EQUAL equation_side BREAK
{
    printf("<equation>\n");
};

equation_side:
equation_part
| equation_part ADD equation_side
{
    printf("<equation_side>\n");
};

equation_part:
interval_part
| equation_part INTERVAL interval_part
{
    printf("<equation_part>\n");
};

interval_part:
atom_group
| NUMBER atom_group
{
    printf("<interval_part>\n");
};

// CuSO4 H2SO4 HCl etc...
atom_group:
atom
| bracket_atom_group
| atom_group atom
| atom_group bracket_atom_group
{
    printf("<atom_group>\n");
};

bracket_atom_group:
LEFT_BRACKET atom_group RIGHT_BRACKET
| LEFT_BRACKET atom_group RIGHT_BRACKET NUMBER
{
    printf("<bracket_atom_group>\n");
};

atom:
ELEMENTS
| ELEMENTS NUMBER
{
    printf("<atom>\n");
};

%%