/*

COPYRIGHT WARNING

This file is not follwoing this project's LICENSE.
These code comes from AheadLib project. If you want
to use it, you should follow AheadLib's License.

*/
#include <Windows.h>
#include <cassert>

#define NORMALEXPORT __declspec(dllexport) __declspec(naked)
#define HANDEXPORT __declspec(dllexport)

HMODULE m_CK2Module = NULL;
HMODULE m_VxMathModule = NULL;

inline BOOL WINAPI Load()
{
    TCHAR tzPath[MAX_PATH];

    lstrcpy(tzPath, TEXT("CK2.dll"));
    m_CK2Module = LoadLibrary(tzPath);
    lstrcpy(tzPath, TEXT("VxMath.dll"));
    m_VxMathModule = LoadLibrary(tzPath);
    return (m_CK2Module != NULL) && (m_VxMathModule != NULL);	
}
    
inline VOID WINAPI Free()
{
    if (m_CK2Module)
        FreeLibrary(m_CK2Module);
    if (m_VxMathModule)
        FreeLibrary(m_VxMathModule);
}

FARPROC WINAPI GetAddress(HMODULE module, PCSTR pszProcName)
{
    FARPROC fpAddress;
    fpAddress = GetProcAddress(module, pszProcName);
    assert(fpAddress != NULL);
    return fpAddress;
}

BOOL WINAPI DllMain(HMODULE hModule, DWORD dwReason, PVOID pvReserved)
{
	if (dwReason == DLL_PROCESS_ATTACH)
	{
		DisableThreadLibraryCalls(hModule);
		return Load();
	}
	else if (dwReason == DLL_PROCESS_DETACH)
	{
		Free();
	}

	return TRUE;
}

{#
renderData for each item

for modify(0): (type, module, functionName, targetDecoratedName, targetDemangledName, pointToDecoratedName, pointToDemangledName)
for hand(1): (type, module, functionName, targetDecoratedName, targetDemangledName, pointToDecoratedName, pointToDemangledName)
for keep(2): (type, module, functionName, decoratedName, originalName)

#}
{% for item in renderData %}
{% if item[0] == 0 %}
NORMALEXPORT void {{ item[2] }}()
{
    //redirect
    //need: {{ item[4] }}
    //      {{ item[3] }}
    //point to: {{ item[6] }}
	GetAddress(m_{{ item[1] }}Module, "{{ item[5] }}");
	__asm JMP EAX;
}
{% elif item[0] == 1 %}
HANDEXPORT void {{ item[2] }}()
{
    //TODO: hand process
    //need: {{ item[4] }}
    //      {{ item[3] }}
    //point to: {{ item[6] }}
	GetAddress(m_{{ item[1] }}Module, "{{ item[5] }}");
	__asm JMP EAX;
}
{% elif item[0] == 2 %}
NORMALEXPORT void {{ item[2] }}()
{
    //keep
    //function: {{ item[4] }}
	GetAddress(m_{{ item[1] }}Module, "{{ item[3] }}");
	__asm JMP EAX;
}
{% else %}
//lost target
{% endif %}
{% endfor %}