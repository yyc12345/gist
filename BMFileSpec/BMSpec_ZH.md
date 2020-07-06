# BM 文件标准

BM文件，全称Ballance Map文件，一种专门用于在Virtools和其他3D绘图软件之间交换Ballance地图信息的文件格式。创造此文件格式的目的在于解决传统obj文件用于交换制图信息的不足之处，而一些专有格式存在Ballance不需要的功能且与Virtools相性不佳，不适合做交换格式。

本格式将随着制图需求进行改进，文件格式设计的时候将考虑前向兼容性，若要查看旧版本的文件标准，请使用git记录功能。

本文档只是介绍BM文件格式，并不会介绍格式中某些项目具体会被导入导出程序如何应用，这是导入导出程序设计者定义行为。不同的导入导出程序将会有不一样的行为，因此请查看相关程序的设定文档。

此标准正在制定，在此句话移除之前，都不算一个单独版本，因此也不会考虑前后兼容。

## 前言

* 本标准中数字类型数据遵循小端序存储模式
* 本标准中浮点数使用IEEE-754标准
* 本标准字符串使用`char32_t`，文件存储使用UTF-32小端序模式，不需要附加BOM，末尾不需要存储`\0`
* 本标准中，字符串的存储是先存储一个`unsigned int32_t`，标识整个字符串的长度（不是比特长度，而是字符个数），接下来再存储字符串
* 本标准中，文件中的`bool`使用`unsigned int32_t`写入

## 基础文件构成

```
+-- file.bm
    +-- index.bm
    +-- object.bm
    +-- mesh.bm
    +-- material.bm
    +-- texture.bm
    +-- Texture
        +-- ExternalTexture.png
        +-- etc...
```

`file.bm`是最终导出的BM文件，本质上是一个zip文件，将下属各个文件进行压缩得到。

`Texture`是一个文件夹，其下放置了用于内置贴图的原始贴图文件。

后续将对各个内部的BM文件格式进行叙述。此外，BM文件中各个层级之间的依赖关系是`object->mesh->material->texture`并且不会越级依赖，因此对于任何导入导出操作，从`texture`向`object`进行处理将会具有优势。

## index.bm

`index.bm`记录了这个bm文件的版本等信息以及各个下属bm文件中各个块对应的名称和偏移量。`index.bm`在BM文件导入时需要被优先读取，用于判断当前BM文件格式版本，并让用户确认导入选项，例如与当前项目具有重复名称的物体应当被如何处理等。

|助记符|类型|
|:---|:---|
|VERSION|unsigned int32_t|
|LIST|-|

`LIST`中每一项具有如下格式

|助记符|类型|
|:---|:---|
|NAME|char32_t \*|
|TYPE|unsigned int8_t|
|OFFSET|unsigned int64_t|

### VERSION

当前BM文件格式的版本号，对于当前标准，这个数值为10。

### NAME

表示当前物体的名称，这些名称不允许重复（也就是整个BM文件中各个类型物体的名称都是唯一的），后文不在叙述。

### TYPE

表示当前描述对象的类型，这表征了当前叙述对象需要到哪个BM文件中进行寻找。其数值如下表：

|助记符|值|含义|
|:---|:---|:---|
|OBJECT|0|物体|
|MESH|1|网格|
|MATERIAL|2|材质|
|TEXTURE|3|贴图|

在`LIST`中，属于同一`TYPE`的各个对象的排列先后顺序必须是按照其对应BM文件中的先后顺序，但是不同种`TYPE`之前的先后顺序没有要求。

### OFFSET

表示在对应文件中的偏移量，用于快速查找和导入。

## object.bm

`index.bm`记录了本文档中所有物体的信息。

|助记符|类型|
|:---|:---|
|IS_COMPONENT|bool|
|WORLD_MATRIX|float\[4\]\[4\]|
|MESH_INDEX|unsigned int32_t|

### IS_COMPONENT

IS_COMPONENT表述当前OBJECT是否是COMPONENT类型

COMPONENT是BM文件中特有的一种物体类型，它只记录物体的移动，旋转和缩放，这对应着Ballance中的机关（PH），因为游戏会在初始化阶段用标准机关模型替换这些机关，因此这些机关物体不需要任何模型信息，只需要记录对应的世界变换矩阵即可。

### WORLD_MATRIX

WORLD_MATRIX（世界变换矩阵）表征物体的移动，旋转和缩放，在BM文件中，我们使用Virtools的内部格式作为标准格式，若Virtools中的WORLD_MATRIX具有如下格式：

|Virtools|**mat[][0]**|**mat[][1]**|**mat[][2]**|**mat[][3]**|
|:---|:---:|:---:|:---:|:---:|
|**mat[0][]**|mat[0][0]|mat[0][1]|mat[0][2]|mat[0][3]|
|**mat[1][]**|mat[1][0]|mat[1][1]|mat[1][2]|mat[1][3]|
|**mat[2][]**|mat[2][0]|mat[2][1]|mat[2][2]|mat[2][3]|
|**mat[3][]**|mat[3][0]|mat[3][1]|mat[3][2]|mat[3][3]|

则其与3ds Max中的物体变换矩阵具有如下关系（反向转换时不存在的填写成0，对角线上的填写1）：

|3ds Max|**mat[][0]**|**mat[][1]**|**mat[][2]**|
|:---|:---:|:---:|:---:|
|**mat[0][]**|mat[0][0]|mat[0][2]|mat[0][1]|
|**mat[1][]**|mat[2][0]|mat[2][2]|mat[2][1]|
|**mat[2][]**|mat[1][0]|mat[1][2]|mat[1][1]|
|**mat[3][]**|mat[3][0]|mat[3][2]|mat[3][1]|

则其与Blender中的物体变换矩阵具有如下关系（下方矩阵需要进行转置才能应用到Blender中，此处为了展示与Virtools的明显关系，故写做这样）：

|Blender|**mat[][0]**|**mat[][1]**|**mat[][2]**|**mat[][3]**|
|:---|:---:|:---:|:---:|:---:|
|**mat[0][]**|mat[0][0]|mat[0][2]|mat[0][1]|mat[0][3]|
|**mat[1][]**|mat[2][0]|mat[2][2]|mat[2][1]|mat[2][3]|
|**mat[2][]**|mat[1][0]|mat[1][2]|mat[1][1]|mat[1][3]|
|**mat[3][]**|mat[3][0]|mat[3][2]|mat[3][1]|mat[3][3]|


### MESH_INDEX

指向物体的MESH，如果物体是COMPONENT类型，那么MESH_INDEX指代的是此物体在游戏内部的一个名为PH_Groups表中的所在行，表征机关类型。如果不是COMPONENT类型，那么将是一个从0开始的数字x，指向`mesh.bm`中的第x块，表示此物体将使用此MESH。

游戏内部的PH_Groups表可在下面查看：

|行号|机关类型|
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

### mesh.bm

`mesh.bm`记录了本文档中所有网格的信息。

|助记符|类型|
|:---|:---|
|V_COUNT|unsigned int32_t|
|V_LIST|-|
|VT_COUNT|unsigned int32_t|
|VT_LIST|-|
|VN_COUNT|unsigned int32_t|
|VN_LIST|-|
|FACE_COUNT|unsigned int32_t|
|FACE_LIST|-|

### V_COUNT，VT_COUNT，VN_COUNT

V_COUNT表示V_LIST中组的个数
VT_COUNT表示VT_LIST中组的个数
VN_COUNT表示VN_LIST中组的个数
FACE_COUNT表示FACE_LIST中组的个数

### V_LIST

顶点列表，每一组数据由3个连续的`float`数据进行存储，依次代表X，Y，Z

### VT_LIST

纹理坐标列表，每一组数据由2个连续的`float`数据进行存储，依次代表U，V

### VN_LIST

顶点法线列表，每一组数据由3个连续的`float`数据进行存储，依次代表X，Y，Z

### FACE_LIST

面列表，BM文件中只支持三角面。每一组数据由9个连续的`unsigned int32_t`数据进行存储。存储顺序与obj文件格式中的f语句是一致的：

|助记符|类型|
|:---|:---|
|VERTEX_1|unsigned int32_t|
|TEXTURE_1|unsigned int32_t|
|NORMAL_1|unsigned int32_t|
|VERTEX_2|unsigned int32_t|
|TEXTURE_2|unsigned int32_t|
|NORMAL_2|unsigned int32_t|
|VERTEX_3|unsigned int32_t|
|TEXTURE_3|unsigned int32_t|
|NORMAL_3|unsigned int32_t|
|USE_MATERIAL|bool|
|MATERIAL_INDEX|unsigned int32_t|

前9项与obj中的面语句一致：`f Vertex1/Texture1/Normal1 Vertex2/Texture2/Normal2 Vertex3/Texture3/Normal3`，用以构造一个面。而与obj语句不一致的是，这些编号是以0起使对应VT_LIST，VN_LIST，FACE_LIST中的项。

USE_MATERIAL标识当前面是否使用材质，如果为是，MATERIAL_INDEX为一个从0起始的，指向`material.bm`中对应的材质；如果为否，则忽略MATERIAL_INDEX。

### material.bm

`material.bm`记录了本文档中所有材质的信息。

|助记符|类型|
|:---|:---|
|KA|float\[3\]|
|KD|float\[3\]|
|KS|float\[3\]|
|USE_TEXTURE|bool|
|MAP_KD|unsigned int32_t|

### KA，KD，KS

KA表示材质的阴影色（ambient color），其中的数据依次表示R，G，B
KD表示材质的固有色（diffuse color），其中的数据依次表示R，G，B
KS表示材质的高光色（specular color），其中的数据依次表示R，G，B

### USE_TEXTURE

表示是否使用贴图

### MAP_KD

如果USE_TEXTURE为否，此项将被忽略，如果为是，此项为一个从0起始的，指向TEXTURE块中对应的贴图

### texture.bm

`texture.bm`记录了本文档中所有贴图的信息。

|助记符|类型|
|:---|:---|
|FILENAME|char32_t \*|
|IS_EXTERNAL|bool|

### FILENAME

此文件的文件名，不包含任何路径。BM文件只会存储文件名，不会涉及任何相对或绝对路径的写入，这主要是为了通用性考虑。

### IS_EXTERNAL

表示此贴图是否是外置的，如果贴图是外置的，那么在文件结构中的`Texture`文件夹将将存储贴图文件的原始格式（未解码格式），并且其文件名与`FILENAME`一致。

对于Ballance而言，所有贴图应均使用外置，这样不仅可以减小BM文件和导出后的NMO地图文件大小，也可以让地图可以引用用户自定义的材质包。除非地图中用到了特殊的自制贴图，否则不应当使用内置贴图。
