## BM 文件标准更改历史

### v1.4

* 指定bmx这个zip文档中的文件名必须使用UTF8编码，并设定指定的flag。
* 对zip文档的格式做出更为详细的规定以确保通用性。
* 删除`object.bm`的字段`IS_FORCED_NO_COMPONENT`。
  - 此字段因为Ballance中的机关替换功能而引入。考虑到BMX已经有相应字段记录是否是COMPONENT，并且此字段与不同工具链的命名规则高度相关，因此删除此项。
  - 命名规则是各个导入导出工具各自进行实现的，不应由BMX文件本身负责。
  - 对于YYC工具链标准，保留所谓的NoComponentGroup。在导入的时候对COMPONENT为TRUE的物体进行命名分析，如果其命名不符合任何一种通用机关，则将其视为FORCED_COMPONENT，并将其置于相关组中。导出时则直接根据NoConponentGroup组中是否存在来进行判断。
* 在`material.bm`新增4个字段：`ALPHA_TEST`，`ALPHA_BLEND`，`Z_BUFFER`，`TWO_SIDED`用于描述更多专用于Ballance的材质特性。

### v1.3

* 在`object.bm`新增字段`GROUP_LIST`表示物体的归组信息。

### v1.2

* 将zip压缩文件的后缀名从`bm`改为`bmx`。由 @BLumia 建议。

### v1.1

* 进一步详细规定字符串的标准写入读取方法。
* 重新设定了bool的写入读取方法。
* 在`object.bm`新增字段`IS_FORCED_NO_COMPONENT`，`IS_HIDDEN`。
* 在`material.bm`重命名字段
  - `KA` -> `AMBIENT`
  - `KD` -> `DIFFUSE`
  - `KS` -> `SPECULAR`
* 在`material.bm`新增字段`SPECULAR_POWER`并详细注解字段含义及数值范围。

### v1.0

初始化标准，添加最基本的内容。
