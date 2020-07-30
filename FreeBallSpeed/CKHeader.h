#if !defined(_YYC_TOOLS_H__CKHEADER__INCLUDED_)
#define _YYC_TOOLS_H__CKHEADER__INCLUDED_

#include <Windows.h>

typedef enum CK_LOAD_FLAGS {
	CK_LOAD_ANIMATION = 1 << 0,	// Load animations
	CK_LOAD_GEOMETRY = 1 << 1,	// Load geometry.
	CK_LOAD_DEFAULT = CK_LOAD_GEOMETRY | CK_LOAD_ANIMATION,	// Load animations & geometry
	CK_LOAD_ASCHARACTER = 1 << 2, // Load all the objects and create a character that contains them all .
	CK_LOAD_DODIALOG = 1 << 3, // Check object name unicity and warns the user with a dialog box when duplicate names are found. 
	CK_LOAD_AS_DYNAMIC_OBJECT = 1 << 4, // Objects loaded from this file may be deleted at run-time or are temporary
	CK_LOAD_AUTOMATICMODE = 1 << 5, // Check object name unicity and automatically rename or replace according to the options specified in CKContext::SetAutomaticLoadMode
	CK_LOAD_CHECKDUPLICATES = 1 << 6, // Check object name unicity (The list of duplicates is stored in the CKFile class after a OpenFile call
	CK_LOAD_CHECKDEPENDENCIES = 1 << 7, // Check if every plugins needed are availables
	CK_LOAD_ONLYBEHAVIORS = 1 << 8, // 
} CK_LOAD_FLAGS;

typedef enum CK_DEPENDENCIES_OPMODE {
	CK_DEPENDENCIES_COPY = 1,
	CK_DEPENDENCIES_DELETE = 2,
	CK_DEPENDENCIES_REPLACE = 3,
	CK_DEPENDENCIES_SAVE = 4,
	CK_DEPENDENCIES_BUILD = 5,
	CK_DEPENDENCIES_OPERATIONMODE = 0xF
} CK_DEPENDENCIES_OPMODE;

typedef enum CK_OBJECTCREATION_OPTIONS {
	CK_OBJECTCREATION_NONAMECHECK = 0,
	CK_OBJECTCREATION_REPLACE = 1,
	CK_OBJECTCREATION_RENAME = 2,
	CK_OBJECTCREATION_USECURRENT = 3,
	CK_OBJECTCREATION_ASK = 4,
	CK_OBJECTCREATION_FLAGSMASK = 0x0000000F,
	CK_OBJECTCREATION_DYNAMIC = 0x00000010,
	CK_OBJECTCREATION_ACTIVATE = 0x00000020,
	CK_OBJECTCREATION_NONAMECOPY = 0x00000040
} CK_OBJECTCREATION_OPTIONS;

typedef enum CK_LOADMODE {
	CKLOAD_INVALID = -1,// Use the existing object instead of loading 
	CKLOAD_OK = 0,		// Ignore ( Name unicity is broken )
	CKLOAD_REPLACE = 1,	// Replace the existing object (Not yet implemented)
	CKLOAD_RENAME = 2,	// Rename the loaded object
	CKLOAD_USECURRENT = 3,// Use the existing object instead of loading 
} CK_LOADMODE, CK_CREATIONMODE;

typedef enum CK_TEXTURE_SAVEOPTIONS {
	CKTEXTURE_RAWDATA = 0,
	CKTEXTURE_EXTERNAL = 1,
	CKTEXTURE_IMAGEFORMAT = 2,
	CKTEXTURE_USEGLOBAL = 3,
	CKTEXTURE_INCLUDEORIGINALFILE = 4,
} CK_TEXTURE_SAVEOPTIONS;


#pragma region CK_ERROR

//----------------------------------------------------------////
//			Error Codes										////
//----------------------------------------------------------////
// Note : When adding Error code, update the CKErrorToString function in CKMain.cpp
// and documentation in Papers\overview.gls

// Operation successful

#define CK_OK										 0

// One of the parameter passed to the function was invalid

#define CKERR_INVALIDPARAMETER						-1

// One of the parameter passed to the function was invalid

#define CKERR_INVALIDPARAMETERTYPE					-2

// The parameter size was invalid

#define CKERR_INVALIDSIZE							-3

// The operation type didn't exist

#define CKERR_INVALIDOPERATION						-4

// The function used to execute the operation is not yet implemented

#define CKERR_OPERATIONNOTIMPLEMENTED				-5

// There was not enough memory to perform the action

#define CKERR_OUTOFMEMORY							-6

// The function  is not yet implemented

#define CKERR_NOTIMPLEMENTED						-7

// There was an attempt to remove something not present

#define CKERR_NOTFOUND								-11

// There is no level currently created

#define CKERR_NOLEVEL								-13

// 

#define CKERR_CANCREATERENDERCONTEXT				-14

// The notification message was not used

#define CKERR_NOTIFICATIONNOTHANDLED				-16

// Attempt to add an item that was already present 

#define CKERR_ALREADYPRESENT						-17

// the render context is not valid

#define CKERR_INVALIDRENDERCONTEXT					-18

// the render context is not activated for rendering

#define CKERR_RENDERCONTEXTINACTIVE					-19

// there was no plugins to load this kind of file

#define CKERR_NOLOADPLUGINS							-20

// there was no plugins to save this kind of file

#define CKERR_NOSAVEPLUGINS							-21

// attempt to load an invalid file

#define CKERR_INVALIDFILE							-22

// attempt to load with an invalid plugin

#define CKERR_INVALIDPLUGIN							-23

// attempt use an object that wasnt initialized

#define  CKERR_NOTINITIALIZED						-24

// attempt use a message type that wasn't registred

#define  CKERR_INVALIDMESSAGE						-25

// attempt use an invalid prototype

#define	CKERR_INVALIDPROTOTYPE			            -28

// No dll file found in the parse directory

#define CKERR_NODLLFOUND							-29

// this dll has already been registred 

#define CKERR_ALREADYREGISTREDDLL					-30

// this dll does not contain information to create the prototype

#define CKERR_INVALIDDLL							-31

// Invalid Object (attempt to Get an object from an invalid ID)

#define CKERR_INVALIDOBJECT							-34

// Invalid window was provided as console window 

#define CKERR_INVALIDCONDSOLEWINDOW					-35

// Invalid kinematic chain ( end and start effector may not be part of the same hierarchy )

#define CKERR_INVALIDKINEMATICCHAIN					-36 


// Keyboard not attached or not working properly

#define CKERR_NOKEYBOARD							-37 

// Mouse not attached or not working properly

#define CKERR_NOMOUSE								-38 

// Joystick not attached or not working properly

#define CKERR_NOJOYSTICK							-39 

// Try to link imcompatible Parameters

#define CKERR_INCOMPATIBLEPARAMETERS				-40

// There is no render engine dll 

#define CKERR_NORENDERENGINE						-44	

// There is no current level (use CKSetCurrentLevel )

#define CKERR_NOCURRENTLEVEL						-45	

// Sound Management has been disabled

#define CKERR_SOUNDDISABLED							-46	

// DirectInput Management has been disabled

#define CKERR_DINPUTDISABLED						-47	

// Guid is already in use or invalid 

#define CKERR_INVALIDGUID							-48	

// There was no more free space on disk when trying to save a file

#define CKERR_NOTENOUGHDISKPLACE					-49	

// Impossible to write to file (write-protection ?)

#define CKERR_CANTWRITETOFILE						-50	

// The behavior cannnot be added to this entity 

#define CKERR_BEHAVIORADDDENIEDBYCB					-51	

// The behavior cannnot be added to this entity 

#define CKERR_INCOMPATIBLECLASSID					-52	

// A manager was registered more than once

#define CKERR_MANAGERALREADYEXISTS					-53	

// CKprocess or TimeManager process while CK is paused will fail

#define CKERR_PAUSED								-54	

// Some plugins were missing whileloading a file

#define CKERR_PLUGINSMISSING						-55	

// Virtools version too old to load this file

#define CKERR_OBSOLETEVIRTOOLS						-56	

// CRC Error while loading file

#define CKERR_FILECRCERROR							-57

// A Render context is already in Fullscreen Mode

#define CKERR_ALREADYFULLSCREEN						-58

// Operation was cancelled by user

#define CKERR_CANCELLED								-59


// there were no animation key at the given index

#define CKERR_NOANIMATIONKEY						-121

// attemp to acces an animation key with an invalid index

#define CKERR_INVALIDINDEX							-122

// the animation is invalid (no entity associated or zero length)

#define CKERR_INVALIDANIMATION						-123

#pragma endregion

#pragma region CK_CLASSID

//----------------------------------------------------------//
//		Class Identifier List								//
//----------------------------------------------------------//

#define  CKCID_OBJECT					1		
#define  CKCID_PARAMETERIN				2	
#define  CKCID_PARAMETEROPERATION		4	
#define  CKCID_STATE					5	
#define  CKCID_BEHAVIORLINK				6	
#define  CKCID_BEHAVIOR					8	
#define  CKCID_BEHAVIORIO				9	
#define  CKCID_RENDERCONTEXT			12	
#define  CKCID_KINEMATICCHAIN			13	
#define  CKCID_SCENEOBJECT				11		
#define  CKCID_OBJECTANIMATION			15	
#define  CKCID_ANIMATION				16	
#define  CKCID_KEYEDANIMATION		18	
#define  CKCID_BEOBJECT					19	
#define	 CKCID_DATAARRAY			52	
#define  CKCID_SCENE				10	
#define  CKCID_LEVEL				21	
#define  CKCID_PLACE				22	
#define  CKCID_GROUP				23	
#define  CKCID_SOUND				24	
#define  CKCID_WAVESOUND		25	
#define  CKCID_MIDISOUND		26	
#define  CKCID_MATERIAL				30	
#define  CKCID_TEXTURE				31	
#define  CKCID_MESH					32	
#define CKCID_PATCHMESH			53	
#define  CKCID_RENDEROBJECT			47	
#define  CKCID_2DENTITY			27	
#define  CKCID_SPRITE		28	
#define  CKCID_SPRITETEXT	29	
#define  CKCID_3DENTITY				33	
#define CKCID_GRID				50	
#define  CKCID_CURVEPOINT		36	
#define  CKCID_SPRITE3D			37	
#define  CKCID_CURVE			43	
#define  CKCID_CAMERA			34	
#define  CKCID_TARGETCAMERA	35	
#define  CKCID_LIGHT			38	
#define  CKCID_TARGETLIGHT	39	
#define  CKCID_CHARACTER		40	
#define  CKCID_3DOBJECT			41	
#define  CKCID_BODYPART		42	
#define  CKCID_PARAMETER				46		
#define  CKCID_PARAMETERLOCAL		45	
#define  CKCID_PARAMETERVARIABLE	55	
#define  CKCID_PARAMETEROUT			3	
#define CKCID_INTERFACEOBJECTMANAGER	48	
#define CKCID_CRITICALSECTION			49	
#define CKCID_LAYER						51	
#define CKCID_PROGRESSIVEMESH			54	
#define CKCID_SYNCHRO					20	

#ifdef _XBOX
#define CKCID_MAXCLASSID				56		
#else
#define CKCID_3DPOINTCLOUD				56	
#define CKCID_VIDEO						57	
#define CKCID_MAXCLASSID				58		
#endif

#pragma endregion

typedef char* CKSTRING;
typedef long CKERROR;
typedef long CK_CLASSID;
typedef unsigned long CKDWORD;
typedef int CKBOOL;
typedef unsigned long CK_ID;

typedef void CKContext;
typedef void CKPluginManager;
typedef void CKGUID;
typedef void CKObjectArray;
typedef void CKObject;
typedef void CKLevel;
typedef void CKDataArray;
typedef void CKDependencies;

typedef CKERROR(__cdecl* CK2Def_CKStartUp)();
typedef CKERROR(__cdecl* CK2Def_CKShutdown)();
typedef CKPluginManager* (__cdecl* CK2Def_CKGetPluginManager)();
typedef int(__thiscall* CK2Def_CKPluginManager_ParsePlugins)(CKPluginManager*, CKSTRING);
typedef CKObjectArray* (__cdecl* CK2Def_CreateCKObjectArray)();
typedef void(__cdecl* CK2Def_DeleteCKObjectArray)(CKObjectArray*);
typedef CKDependencies* (__cdecl* CK2Def_CKGetDefaultClassDependencies)(CK_DEPENDENCIES_OPMODE);	// choose CK_DEPENDENCIES_SAVE
typedef CKERROR(__thiscall* CK2Def_CKContext_Load)(CKContext*, CKSTRING, CKObjectArray*, CK_LOAD_FLAGS, CKGUID*);
typedef CKERROR(__thiscall* CK2Def_CKContext_Save)(CKContext*, CKSTRING, CKObjectArray*, CKDWORD, CKDependencies*, CKGUID*);
typedef CKObject* (__thiscall* CK2Def_CKContext_GetObjectByNameAndClass)(CKContext*, CKSTRING, CK_CLASSID, CKObject*);
typedef CKBOOL(__thiscall* CK2Def_CKDataArray_SetElementValue)(CKDataArray*, int, int, void*, int);
typedef CKBOOL(__thiscall* CK2Def_CKDataArray_GetElementValue)(CKDataArray*, int, int, void*);
typedef CKERROR(__cdecl* CK2Def_CKCreateContext)(CKContext**, HWND, int, unsigned long);
typedef CKERROR(__cdecl* CK2Def_CKCloseContext)(CKContext*);
typedef int(__thiscall* CK2Def_CKContext_GetObjectsCountByClassID)(CKContext*, CK_CLASSID);
typedef CK_ID* (__thiscall* CK2Def_CKContext_GetObjectsListByClassID)(CKContext*, CK_CLASSID);
typedef CKObject* (__thiscall* CK2Def_CKContext_GetObjectA)(CKContext*, CK_ID);
typedef CKObject* (__thiscall* CK2Def_CKContext_CreateObject)(CKContext*, CK_CLASSID, CKSTRING, CK_OBJECTCREATION_OPTIONS, CK_LOADMODE*);	// default value: x NULL, CK_OBJECTCREATION_NONAMECHECK, NULL
typedef CKERROR(__thiscall* CK2Def_CKLevel_AddObject)(CKLevel*, CKObject*);
typedef void(__thiscall* CK2Def_CKContext_SetCurrentLevel)(CKContext*, CKLevel*);
typedef void(__thiscall* CK2Def_CKContext_SetGlobalImagesSaveOptions)(CKContext*, CK_TEXTURE_SAVEOPTIONS);

#endif