#include <Windows.h>

#define NAKED __declspec(naked)
#define EXPORT __declspec(dllexport)
#define EXPORTCPP EXPORT NAKED

HMODULE m_hModule = NULL;
DWORD m_dwReturn[{{ funcCount }}] = {0};

inline BOOL WINAPI Load()
{
    TCHAR tzPath[MAX_PATH];
    TCHAR tzTemp[MAX_PATH * 2];

    lstrcpy(tzPath, TEXT("CK2"));
    m_hModule = LoadLibrary(tzPath);
    assert(m_hModule != NULL);
    return (m_hModule != NULL);	
}
    
inline VOID WINAPI Free()
{
    if (m_hModule)
        FreeLibrary(m_hModule);
}

FARPROC WINAPI GetAddress(PCSTR pszProcName)
{
    FARPROC fpAddress;
    fpAddress = GetProcAddress(m_hModule, pszProcName);
    assert(fpAddress != NULL);
    return fpAddress;
}

BOOL WINAPI DllMain(HMODULE hModule, DWORD dwReason, PVOID pvReserved)
{
	if (dwReason == DLL_PROCESS_ATTACH)
	{
		DisableThreadLibraryCalls(hModule);

		for (INT i = 0; i < sizeof(m_dwReturn) / sizeof(DWORD); i++)
			m_dwReturn[i] = TlsAlloc();
		return Load();
	}
	else if (dwReason == DLL_PROCESS_DETACH)
	{
		for (INT i = 0; i < sizeof(m_dwReturn) / sizeof(DWORD); i++)
			TlsFree(m_dwReturn[i]);
		Free();
	}

	return TRUE;
}

{#
renderData for each item

for modify: (type, functionName, currentDecoratedName, originalName, currentName)
for keep: (type, functionName, decoratedName, originalName)
for field: (type, fieldName, originalName)

#}
{% for item in renderData %}
{% if item[0] == 0 %}
EXPORTCPP {{ item[1] }}
{
    //need: {{ item[3] }}
    //point to: {{ item[4] }}
	__asm PUSH m_dwReturn[{{ loop.index0 }} * TYPE long];
	__asm CALL DWORD PTR [TlsSetValue];

	GetAddress("{{ item[2] }}")();

	__asm PUSH EAX;
	__asm PUSH m_dwReturn[{{ loop.index0 }} * TYPE long];
	__asm CALL DWORD PTR [TlsGetValue];
	__asm XCHG EAX, [ESP];
	__asm RET;
}
{% elif item[0] == 1 %}
EXPORTCPP {{ item[1] }}
{
    //function: {{ item[3] }}
	GetAddress("{{ item[2] }}");
	__asm JMP EAX;
}
{% elif item[0] == 2 %}
//field: {{ item[2] }}
EXPORT {{ item[1] }};
{% else %}
//lost target
{% endif %}
{% endfor %}