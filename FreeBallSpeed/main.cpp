#include "CKHeader.h"
#include <Windows.h>
#include <iostream>
#include <string>
#include <filesystem>

#define BUFFER_SIZE 65526

int main(int argc, char* argv[]) {

	char* sharedStorage = (char*)malloc(sizeof(char) * BUFFER_SIZE);
	if (sharedStorage == NULL) {
		std::cout << "Fail to alloc cache memory" << std::endl;
		return 2;
	}

	HMODULE ck2 = LoadLibrary("CK2.dll");
	if (ck2 == NULL) {
		std::cout << "Fail to load CK2 dll" << std::endl;
		return 2;
	}


	// init function
	auto CK2_CKStartUp = CK2Def_CKStartUp(GetProcAddress(ck2, "?CKStartUp@@YAJXZ"));
	auto CK2_CKShutdown = CK2Def_CKShutdown(GetProcAddress(ck2, "?CKShutdown@@YAJXZ"));
	auto CK2_CKGetPluginManager = CK2Def_CKGetPluginManager(GetProcAddress(ck2, "?CKGetPluginManager@@YAPAVCKPluginManager@@XZ"));
	auto CK2_CKPluginManager_ParsePlugins = CK2Def_CKPluginManager_ParsePlugins(GetProcAddress(ck2, "?ParsePlugins@CKPluginManager@@QAEHPAD@Z"));
	auto CK2_CreateCKObjectArray = CK2Def_CreateCKObjectArray(GetProcAddress(ck2, "?CreateCKObjectArray@@YAPAVCKObjectArray@@XZ"));
	auto CK2_DeleteCKObjectArray = CK2Def_DeleteCKObjectArray(GetProcAddress(ck2, "?DeleteCKObjectArray@@YAXPAVCKObjectArray@@@Z"));
	auto CK2_CKGetDefaultClassDependencies = CK2Def_CKGetDefaultClassDependencies(GetProcAddress(ck2, "?CKGetDefaultClassDependencies@@YAPAVCKDependencies@@W4CK_DEPENDENCIES_OPMODE@@@Z"));
	auto CK2_CKContext_Load = CK2Def_CKContext_Load(GetProcAddress(ck2, "?Load@CKContext@@QAEJPADPAVCKObjectArray@@W4CK_LOAD_FLAGS@@PAUCKGUID@@@Z"));
	auto CK2_CKContext_Save = CK2Def_CKContext_Save(GetProcAddress(ck2, "?Save@CKContext@@QAEJPADPAVCKObjectArray@@KPAVCKDependencies@@PAUCKGUID@@@Z"));
	auto CK2_CKContext_GetObjectByNameAndClass = CK2Def_CKContext_GetObjectByNameAndClass(GetProcAddress(ck2, "?GetObjectByNameAndClass@CKContext@@QAEPAVCKObject@@PADJPAV2@@Z"));
	auto CK2_CKDataArray_SetElementValue = CK2Def_CKDataArray_SetElementValue(GetProcAddress(ck2, "?SetElementValue@CKDataArray@@QAEHHHPAXH@Z"));
	auto CK2_CKDataArray_GetElementValue = CK2Def_CKDataArray_GetElementValue(GetProcAddress(ck2, "?GetElementValue@CKDataArray@@QAEHHHPAX@Z"));
	auto CK2_CKCreateContext = CK2Def_CKCreateContext(GetProcAddress(ck2, "?CKCreateContext@@YAJPAPAVCKContext@@PAXHK@Z"));
	auto CK2_CKCloseContext = CK2Def_CKCloseContext(GetProcAddress(ck2, "?CKCloseContext@@YAJPAVCKContext@@@Z"));

	// init engine
#define checkcode(err_reason) if (code != CK_OK) {std::cout << err_reason << std::endl; return 1;}

	CKERROR code = CK2_CKStartUp();
	checkcode("Fail to execute CKStartUp()");

	std::filesystem::path rootPath, rePath, magPath, plgPath, bbPath;
	GetModuleFileName(NULL, sharedStorage, BUFFER_SIZE);
	rootPath = sharedStorage;
	rootPath = rootPath.parent_path().parent_path();
	rePath = rootPath / "RenderEngines";
	magPath = rootPath / "Managers";
	plgPath = rootPath / "Plugins";
	bbPath = rootPath / "BuildingBlocks";

	CKPluginManager* pluginManager = CK2_CKGetPluginManager();
	int k = 0;
	k += CK2_CKPluginManager_ParsePlugins(pluginManager, (char*)rePath.string().c_str());
	k += CK2_CKPluginManager_ParsePlugins(pluginManager, (char*)magPath.string().c_str());
	k += CK2_CKPluginManager_ParsePlugins(pluginManager, (char*)plgPath.string().c_str());
	k += CK2_CKPluginManager_ParsePlugins(pluginManager, (char*)bbPath.string().c_str());
	std::cout << "Total loaded modules count: " << k << std::endl;

	CKContext* ctx = NULL;
	code = CK2_CKCreateContext(&ctx, NULL, 0, 0);
	checkcode("Fail to execute CKCreateContext()");

	// real load
	std::filesystem::path ballsnmo;
	ballsnmo = rootPath / "3D Entities" / "Balls.nmo";
	CKObjectArray* array = CK2_CreateCKObjectArray();
	code = CK2_CKContext_Load(ctx, (char*)ballsnmo.string().c_str(), array, CK_LOAD_DEFAULT, NULL);
	checkcode("Fail to load CMO file");

	CKDataArray* dataarray = CK2_CKContext_GetObjectByNameAndClass(ctx, "Physicalize_GameBall", CKCID_DATAARRAY, NULL);
	// read and output first
	float rPaper = 0.0, oPaper = 0.065, wPaper = 0.065;
	float rStone = 0.0, oStone = 0.92, wStone = 0.92;
	float rWood = 0.0, oWood = 0.43, wWood = 0.43;
	float mult = 0.0;
	CK2_CKDataArray_GetElementValue(dataarray, 0, 7, &rPaper);
	CK2_CKDataArray_GetElementValue(dataarray, 1, 7, &rStone);
	CK2_CKDataArray_GetElementValue(dataarray, 2, 7, &rWood);
	std::cout << "Ball status:" << std::endl <<
		"Paper: " << rPaper << " (" << rPaper / oPaper << "x)" << std::endl <<
		"Stone: " << rStone << " (" << rStone / oStone << "x)" << std::endl <<
		"Wood: " << rWood << " (" << rWood / oWood << "x)" << std::endl;

	// accept input and write
	std::cout << "Input multiple: ";
	std::cin >> mult;
	wPaper *= mult;
	wStone *= mult;
	wWood *= mult;

	CK2_CKDataArray_SetElementValue(dataarray, 0, 7, &wPaper, sizeof(float));
	CK2_CKDataArray_SetElementValue(dataarray, 1, 7, &wStone, sizeof(float));
	CK2_CKDataArray_SetElementValue(dataarray, 2, 7, &wWood, sizeof(float));

	// save
	DeleteFile(ballsnmo.string().c_str());
	code = CK2_CKContext_Save(ctx, (char*)ballsnmo.string().c_str(), array, 0xFFFFFFFF, CK2_CKGetDefaultClassDependencies(CK_DEPENDENCIES_SAVE), NULL);
	checkcode("Fail to save CMO file");

	// clean
	CK2_DeleteCKObjectArray(array);
	CK2_CKCloseContext(ctx);
	CK2_CKShutdown();

#undef checkcode
	return 0;
}
