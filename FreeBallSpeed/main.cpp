#include "CKHeader.h"
#include <Windows.h>
#include <iostream>
#include <string>
#include <filesystem>

#define BUFFER_SIZE 65526

int main(int argc, char* argv[]) {

	std::cout << "FreeBallSpeed created by yyc12345" << std::endl <<
		"Source code url: https://github.com/yyc12345/gist/tree/master/FreeBallSpeed" << std::endl << std::endl;

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
	auto CK2_CKContext_CreateObject = CK2Def_CKContext_CreateObject(GetProcAddress(ck2, "?CreateObject@CKContext@@QAEPAVCKObject@@JPADW4CK_OBJECTCREATION_OPTIONS@@PAW4CK_LOADMODE@@@Z"));
	auto CK2_CKLevel_AddObject = CK2Def_CKLevel_AddObject(GetProcAddress(ck2, "?AddObject@CKLevel@@QAEJPAVCKObject@@@Z"));
	auto CK2_CKContext_SetCurrentLevel = CK2Def_CKContext_SetCurrentLevel(GetProcAddress(ck2, "?SetCurrentLevel@CKContext@@QAEXPAVCKLevel@@@Z"));
	auto CK2_CKContext_SetGlobalImagesSaveOptions = CK2Def_CKContext_SetGlobalImagesSaveOptions(GetProcAddress(ck2, "?SetGlobalImagesSaveOptions@CKContext@@QAEXW4CK_TEXTURE_SAVEOPTIONS@@@Z"));
	auto CK2_CKContext_GetObjectListByType = CK2Def_CKContext_GetObjectListByType(GetProcAddress(ck2, "?GetObjectListByType@CKContext@@QAEABVXObjectPointerArray@@JH@Z"));

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
	std::cout << std::endl << "Accepted multiple: " << mult << std::endl;
	wPaper *= mult;
	wStone *= mult;
	wWood *= mult;

	CK2_CKDataArray_SetElementValue(dataarray, 0, 7, &wPaper, sizeof(float));
	CK2_CKDataArray_SetElementValue(dataarray, 1, 7, &wStone, sizeof(float));
	CK2_CKDataArray_SetElementValue(dataarray, 2, 7, &wWood, sizeof(float));

	// try save IC so we need a fake level
	//int idCount = 0;
	//CK_ID* idList = NULL;
	const XObjectPointerArray* objary = &(CK2_CKContext_GetObjectListByType(ctx, CKCID_OBJECT, TRUE));
	CKObject** a = objary->Begin();
	CKObject** b = objary->End();
//#define addObjList(classid) idCount=CK2_CKContext_GetObjectsCountByClassID(ctx,classid);idList=CK2_CKContext_GetObjectsListByClassID(ctx,classid);for(int i=0;i<idCount;i++)CK2_CKLevel_AddObject(levels,CK2_CKContext_GetObjectA(ctx, idList[i]));
	CKLevel* levels = CK2_CKContext_CreateObject(ctx, CKCID_LEVEL, NULL, CK_OBJECTCREATION_NONAMECHECK, NULL);
	CK2_CKContext_SetCurrentLevel(ctx, levels);
	/*addObjList(CKCID_3DOBJECT);
	addObjList(CKCID_3DENTITY);
	addObjList(CKCID_DATAARRAY);
	addObjList(CKCID_GROUP);
	addObjList(CKCID_LIGHT);
	addObjList(CKCID_MATERIAL);
	addObjList(CKCID_MESH);
	addObjList(CKCID_TEXTURE);*/
	for (CKObject** item = objary->Begin(); item != objary->End(); item++) {
		CK2_CKLevel_AddObject(levels, *item);
	}
//#undef addObjList

	// save
	CK2_CKContext_SetGlobalImagesSaveOptions(ctx, CKTEXTURE_EXTERNAL);
	GetTempPath(BUFFER_SIZE, sharedStorage);
	std::filesystem::path ballscmo;
	ballscmo = sharedStorage;
	sprintf(sharedStorage, "0c7666f3e2be44ef9973c2ec88deb829_%d.cmo", GetCurrentProcessId());
	ballscmo /= sharedStorage;
	DeleteFile(ballsnmo.string().c_str());
	DeleteFile(ballscmo.string().c_str());
	CKDependencies* dep = CK2_CKGetDefaultClassDependencies(CK_DEPENDENCIES_SAVE);
	dep->m_Flags = CK_DEPENDENCIES_FULL;
	code = CK2_CKContext_Save(ctx, (char*)ballscmo.string().c_str(), array, 0xFFFFFFFF, dep, NULL);
	checkcode("Fail to save CMO file");
	if (!MoveFile(ballscmo.string().c_str(), ballsnmo.string().c_str())) {
		std::cout << "Fail to move created file!" << std::endl; 
		return 1;
	}

	// clean
	CK2_DeleteCKObjectArray(array);
	CK2_CKCloseContext(ctx);
	CK2_CKShutdown();

	std::cout << "OK" << std::endl;

#undef checkcode
	return 0;
}
