#include <CKAll.h>
#include <cstdio>

int main(int argc, char* argv[]) {

	CKERROR err = CKStartUp();

	CKPluginManager* plugin_manager = CKGetPluginManager();
	plugin_manager->ParsePlugins("RenderEngines");
	plugin_manager->ParsePlugins("Managers");
	plugin_manager->ParsePlugins("Plugins");
	plugin_manager->ParsePlugins("BuildingBlocks");

	CKContext* ctx;
	CKCreateContext(&ctx, NULL, 0);

	CKObjectArray* obj_array = CreateCKObjectArray();
	ctx->Load("MenuLevel.nmo", obj_array, CK_LOAD_DEFAULT);

	CK3dObject* stone_ball = (CK3dObject*)ctx->GetObjectByNameAndClass("I_Ball_Stone", CKCID_3DOBJECT, NULL);
	int stone_ball_anime_count = stone_ball->GetObjectAnimationCount();
	CKObjectAnimation* stone_ball_anime = stone_ball->GetObjectAnimation(0);

#define ANIME_STATUS(name) std::fprintf(stdout, #name ": %s\n", stone_ball_anime->name() ? "true" : "false")
	ANIME_STATUS(HasMorphInfo);
	ANIME_STATUS(HasMorphNormalInfo);
	ANIME_STATUS(HasPositionInfo);
	ANIME_STATUS(HasRotationInfo);
	ANIME_STATUS(HasScaleAxisInfo);
	ANIME_STATUS(HasScaleInfo);
#undef ANIME_STATUS

	CKAnimController* pos_ctl = stone_ball_anime->GetPositionController();
	CKAnimController* rot_ctl = stone_ball_anime->GetRotationController();
	CKAnimController* scale_ctl = stone_ball_anime->GetScaleController();

	{
		FILE* fs = std::fopen("stone_ball_pos.bin", "wb");
		int key_count = pos_ctl->GetKeyCount();
		std::fprintf(stdout, "Position Key Count : %d\n", key_count);
		for (int i = 0; i < key_count; ++i) {
			CKPositionKey* key = (CKPositionKey*)pos_ctl->GetKey(i);
			std::fwrite(&key->TimeStep, 1u, sizeof(key->TimeStep), fs);
			std::fwrite(&key->Pos, 1u, sizeof(key->Pos), fs);
		}
		std::fclose(fs);
	}
	{
		FILE* fs = std::fopen("stone_ball_rot.bin", "wb");
		int key_count = rot_ctl->GetKeyCount();
		std::fprintf(stdout, "Rotation Key Count : %d\n", key_count);
		for (int i = 0; i < key_count; ++i) {
			CKRotationKey* key = (CKRotationKey*)rot_ctl->GetKey(i);
			std::fwrite(&key->TimeStep, 1u, sizeof(key->TimeStep), fs);
			std::fwrite(&key->Rot, 1u, sizeof(key->Rot), fs);
		}
		std::fclose(fs);
	}
	{
		FILE* fs = std::fopen("stone_ball_scale.bin", "wb");
		int key_count = scale_ctl->GetKeyCount();
		std::fprintf(stdout, "Scale Key Count : %d\n", key_count);
		for (int i = 0; i < key_count; ++i) {
			CKScaleKey* key = (CKScaleKey*)scale_ctl->GetKey(i);
			std::fwrite(&key->TimeStep, 1u, sizeof(key->TimeStep), fs);
			std::fwrite(&key->Pos, 1u, sizeof(key->Pos), fs);
		}
		std::fclose(fs);
	}

	DeleteCKObjectArray(obj_array);
	CKCloseContext(ctx);
	CKShutdown();

	std::fputs("DONE!\n", stdout);

}
