# yyc 制图工具链标准

BM 文件标准只定义了文件中的一些字段的要求，并没有指明这些字段应该被如何设置，本标准将介绍所有由yyc开发的制图工具链所遵守的标准。如果您使用此工具链进行制图操作，除了阅读BM文件标准外，还需通读此标准。

本格式将随着制图需求进行改进，文件格式设计的时候将考虑前向兼容性，若要查看旧版本的文件标准，请使用git记录功能。

本文档不涉及其余人制作的工具链的标准，如若兼容性问题，请查阅对应的标准文件。

此标准正在制定，在此句话移除之前，都不算一个单独版本，因此也不会考虑前后兼容。

## COMPONENT标准

如果一个物体是COMPONENT，其MESH_INDEX（机关编号）取决于游戏内部的一个名为PH_Groups表中的所在行

在标准中，这些表达式通过判断名称是否以这些类型名开头来进行判断。

|MESH_INDEX（机关编号）|机关类型|
|:---|:---|
|0|P_Extra_Life|
|1|P_Extra_Point|
|2|P_Trafo_Paper|
|3|P_Trafo_Stone|
|4|P_Trafo_Wood|
|5|P_Ball_Paper|
|6|P_Ball_Stone|
|7|P_Ball_Wood|
|8|P_Box|
|9|P_Dome|
|10|P_Modul_01|
|11|P_Modul_03|
|12|P_Modul_08|
|13|P_Modul_17|
|14|P_Modul_18|
|15|P_Modul_19|
|16|P_Modul_25|
|17|P_Modul_26|
|18|P_Modul_29|
|19|P_Modul_30|
|20|P_Modul_34|
|21|P_Modul_37|
|22|P_Modul_41|

## 外置贴图标准

以下贴图将被默认视作外置贴图。

检测方式是将贴图路径的文件名提取并全文比对，完全相等则视为外置贴图，因此如果你的某些内置贴图与下列有重名，请进行改名。

* Ball_LightningSphere1.bmp
* Ball_LightningSphere2.bmp
* Ball_LightningSphere3.bmp
* Ball_Paper.bmp
* Ball_Stone.bmp
* Ball_Wood.bmp
* Brick.bmp
* Button01_deselect.tga
* Button01_select.tga
* Button01_special.tga
* Column_beige.bmp
* Column_beige_fade.tga
* Column_blue.bmp
* Cursor.tga
* Dome.bmp
* DomeEnvironment.bmp
* DomeShadow.tga
* ExtraBall.bmp
* ExtraParticle.bmp
* E_Holzbeschlag.bmp
* FloorGlow.bmp
* Floor_Side.bmp
* Floor_Top_Border.bmp
* Floor_Top_Borderless.bmp
* Floor_Top_Checkpoint.bmp
* Floor_Top_Flat.bmp
* Floor_Top_Profil.bmp
* Floor_Top_ProfilFlat.bmp
* Font_1.tga
* Gravitylogo_intro.bmp
* HardShadow.bmp
* Laterne_Glas.bmp
* Laterne_Schatten.tga
* Laterne_Verlauf.tga
* Logo.bmp
* Metal_stained.bmp
* Misc_Ufo.bmp
* Misc_UFO_Flash.bmp
* Modul03_Floor.bmp
* Modul03_Wall.bmp
* Modul11_13_Wood.bmp
* Modul11_Wood.bmp
* Modul15.bmp
* Modul16.bmp
* Modul18.bmp
* Modul18_Gitter.tga
* Modul30_d_Seiten.bmp
* Particle_Flames.bmp
* Particle_Smoke.bmp
* PE_Bal_balloons.bmp
* PE_Bal_platform.bmp
* PE_Ufo_env.bmp
* Pfeil.tga
* P_Extra_Life_Oil.bmp
* P_Extra_Life_Particle.bmp
* P_Extra_Life_Shadow.bmp
* Rail_Environment.bmp
* sandsack.bmp
* SkyLayer.bmp
* Sky_Vortex.bmp
* Stick_Bottom.tga
* Stick_Stripes.bmp
* Target.bmp
* Tower_Roof.bmp
* Trafo_Environment.bmp
* Trafo_FlashField.bmp
* Trafo_Shadow_Big.tga
* Tut_Pfeil01.tga
* Tut_Pfeil_Hoch.tga
* Wolken_intro.tga
* Wood_Metal.bmp
* Wood_MetalStripes.bmp
* Wood_Misc.bmp
* Wood_Nailed.bmp
* Wood_Old.bmp
* Wood_Panel.bmp
* Wood_Plain.bmp
* Wood_Plain2.bmp
* Wood_Raft.bmp

## 命名标准

本工具链的自动归组功能需要遵守一定的命名标准才能起作用，如果您不需要自动归组功能，可以忽略这一节。

自动归组通过检测名称开头是否符合前缀，进而进行归组判断。

自动归组器不支持999小节加载器的命名。

当前版本不支持归影子组。

### 机关

属于下列类型的机关的命名标准

* P_Extra_Life
* P_Extra_Point
* P_Trafo_Paper
* P_Trafo_Stone
* P_Trafo_Wood
* P_Ball_Paper
* P_Ball_Stone
* P_Ball_Wood
* P_Box
* P_Dome
* P_Modul_01
* P_Modul_03
* P_Modul_08
* P_Modul_17
* P_Modul_18
* P_Modul_19
* P_Modul_25
* P_Modul_26
* P_Modul_29
* P_Modul_30
* P_Modul_34
* P_Modul_37
* P_Modul_41

命名格式：`AAAAA_XX_YY`

`AAAAA_`为机关的名称，也就是上文列表中的名字（注意要加上下划线）。`XX`为归到的小节组的表示，必定是2位，不足补0。`_YY`为机关去重名部分，一般为2位数字，字符数不限。

### 道路

道路共3种，路面，钢轨，木板，它们遵守的命名规则如下：

* `A_Floor_XX`
* `A_Rail_XX`
* `A_Wood_XX`

`_XX`为去重名部分，一般为2位数字，字符数不限。

### 死亡区

* `DepthCubes_XX`

`_XX`为去重名部分，一般为2位数字，字符数不限。

### Stopper

* `A_Stopper_XX`

`_XX`为去重名部分，一般为2位数字，字符数不限。

由于游戏限制，Stopper组中只有第一个元素会有声音，因此可以直接在3D软件中附加所有的Stopper并命名为`A_Stopper`，如果不想附加，自动归组器也支持重命名部分的检测

### 特殊物件

* 开头盘点火：`PS_FourFlames_01`
* 终点飞船：`PE_Balloon_01`
* 小节盘点火：`PC_TwoFlames_XX`
* 重生点：`PR_Resetpoint_XX`

开头盘点火和终点飞船命名唯一

小节盘点火和重生点中的`_XX`为其编号，具体含义请查看制图教程。

### 装饰品

装饰品由于不涉及任何归组内容，所以没有任何要求，只要不影响前面所叙述的判断即可。

不过需要注意的是，如果装饰品需要被物理化，例如在螺旋形轨道中的需要被实例化，具有碰撞效果的灯柱等，需要按照路面来进行命名，根据材质的质感选择需要归入钢轨组还是路面组。

当然建议材质以`D_`开头进行命名，但不强求。

天空云彩最好命名为`SkyLayer`，漩涡则是`SkyLayer_Votex`，但这些都不强求。