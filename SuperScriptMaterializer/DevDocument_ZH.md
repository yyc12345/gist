# 开发帮助

此文档将叙述一些开发SuperScriptMaterializer中需要被记忆的一些原则。

# 可能的连线

该程序中最重要的事情之一是生成链接，而最困难的是pLink。 下图显示了将在此程序中分析的所有pLink情况。

```
 +--------------+              +-----------------+
 | pLocal       +-------------->                 |
 +--------------+              |                 |
                               |  pIn (bb/oper)  |
 +--------------+              |                 |
 | pIn (bb)     +-------------->       /         |
 +--------------+              |                 |
                               |   pTarget (bb)  |
 +----------------+            |                 |
 | pOut (bb/oper) +------------>                 |
 +----------------+            +-----------------+




+------------------+           +--------------+
|                  +-----------> pOut (bb)    |
|                  |           +--------------+
| pOut (bb/oper)   |
|                  |           +--------------+
|                  +-----------> pLocal       |
+------------------+           +--------------+

```

如果链接的一个端点不在当前图形中，则此端点将创建为快捷方式。 但是，如果链接的一个端点是当前分析的Building Graph的pIO，并且与另一个端点具有相同的CK_ID，则应创建一个eLink。

# 数据库

SuperScriptMaterializer处理流程里会涉及很多不同的数据库文件，以下是这些数据库和其内表的格式。  
其中这些是Materializer直接输出的基于文档的数据库：

* script.db
* data.db
* env.db

这些数据库是上面数据库经过Decorator处理可以被Viewer接受的数据库：

* decorated.db
* sheet.db
* query.db
* composition.db

## script.db 格式

script.db导出的是当前Virtools文档内的脚本数。

表列表：

- behavior：behavior本身，包括behavior graph和prototype behavior之类的
- bIn：behavior的行为输入
- bOut：behavior的行为输出
- eLink：export link
- pAttr：attribute类型的parameter
- pData：parameter参数属性，以类似字典的形式存储每个parameter参数的各个部分
- pIn：behavior的parameter输入
- pLink：parameter link
- pLocal：local parameter
- pOper：parameter operator
- pOut：behavior的parameter输出
- pTarget：behavior的target输入，实际上是一个特殊的parameter输入
- script：文档里的每个脚本

### behavior

|字段|类型|含义|
|:---|:---|:---|
|thisObj|INTEGER|当前对象的`CK_ID`，后文无特殊说明则默认相同的名称均为此含义|
|name|TEXT||
|type|INTEGER||
|proto_name|TEXT||
|proto_guid|TEXT||
|flags|INTEGER||
|priority|INTEGER||
|version|INTEGER||
|pin_count|TEXT||
|parent|INTEGER||

### bIn / bOut

|字段|类型|含义|
|:---|:---|:---|
|thisObj|INTEGER|同上|
|index|INTEGER||
|name|TEXT||
|belong_to|INTEGER|当前对象所归属对象的`CK_ID`，用于递归查询上一级。后文无特殊说明则默认相同的名称均为此含义|

### bLink

|字段|类型|含义|
|:---|:---|:---|
|input|INTEGER||
|output|INTEGER||
|delay|INTEGER||
|input_obj|INTEGER||
|input_type|INTEGER||
|input_index|INTEGER||
|output_obj|INTEGER||
|output_type|INTEGER||
|output_index|INTEGER||
|belong_to|INTEGER||

### eLink

|字段|类型|含义|
|:---|:---|:---|
|export_obj|INTEGER||
|internal_obj|INTEGER||
|is_in|INTEGER||
|index|INTEGER||
|belong_to|INTEGER||

### pAttr

|字段|类型|含义|
|:---|:---|:---|
|thisObj|INTEGER|同上|
|name|TEXT||
|type|TEXT||
|type_guid|TEXT||

### pData

|字段|类型|含义|
|:---|:---|:---|
|field|TEXT|键值对的键|
|data|TEXT|键值对的值|
|belong_to|INTEGER||

### pIn

|字段|类型|含义|
|:---|:---|:---|
|thisObj|INTEGER|同上|
|index|INTEGER||
|name|TEXT||
|type|TEXT||
|type_guid|TEXT||
|belong_to|INTEGER||
|direct_source|INTEGER||
|shard_source|INTEGER||

`shard_source`是笔误，应为`shared_source`，可能会在将来的版本内修正。

### pLink

|字段|类型|含义|
|:---|:---|:---|
|input|INTEGER||
|output|INTEGER||
|input_obj|INTEGER||
|input_type|INTEGER||
|input_is_bb|INTEGER||
|input_index|INTEGER||
|output_obj|INTEGER||
|output_type|INTEGER||
|output_is_bb|INTEGER||
|output_index|INTEGER||
|belong_to|INTEGER||

### pLocal

|字段|类型|含义|
|:---|:---|:---|
|thisObj|INTEGER||
|name|TEXT||
|type|TEXT||
|type_guid|TEXT||
|is_setting|INTEGER||
|belong_to|INTEGER||

### pOper

|字段|类型|含义|
|:---|:---|:---|
|thisObj|INTEGER||
|op|TEXT||
|op_guid|TEXT||
|belong_to|INTEGER||

### pOut

|字段|类型|含义|
|:---|:---|:---|
|thisObj|INTEGER||
|index|INTEGER||
|name|TEXT||
|type|TEXT||
|type_guid|TEXT||
|belong_to|INTEGER||

### pTarget

|字段|类型|含义|
|:---|:---|:---|
|thisObj|INTEGER||
|name|TEXT||
|type|TEXT||
|type_guid|TEXT||
|belong_to|INTEGER||
|direct_source|INTEGER||
|shard_source|INTEGER||

### script

|字段|类型|含义|
|:---|:---|:---|
|thisObj|INTEGER||
|name|TEXT||
|index|INTEGER||
|behavior|INTEGER||

## data.db 格式

data.db导出的是当前文档内的除脚本外的一些基本类型的CKObject，例如Mesh, 3D Object, Array等数据。

- obj：数据部分存储每个文档里每个元素的基本类型
- objHeader：见下
- objBody：Header和Body，定义了一个类似于Array的表格，Array就按Array的格式存储，而其他物件，则将属性作为表头，然后本身作为表内的唯一一行数据记录
- objParam：Body部分存储了对应值的字符串代替表示形式（用于良好的可视化），而其准确的属性上的描述由此表存储，按照类似pData的方式存储。
- msg：当前文档内定义的message标号与数值的对应

### msg

|字段|类型|含义|
|:---|:---|:---|
|index|INTEGER||
|name|TEXT||

## env.db 格式

env.db导出的是当前Virtools环境的数据，与文档无关，这部分如果是多个文件共用一个环境，那么只需要导出和在`Decorator`里综合一次即可

表列表：

- attr：attribute
- op：operator，parameter转换的定义
- param：parameter的定义
- plugin：当前环境插件
- variable：全局变量数据

### attr

|字段|类型|含义|
|:---|:---|:---|
|index|INTEGER||
|name|TEXT||
|category_index|INTEGER||
|category_name|TEXT||
|flags|INTEGER||
|param_index|INTEGER||
|compatible_classid|INTEGER||
|default_value|TEXT||

### op

|字段|类型|含义|
|:---|:---|:---|
|funcptr|INTEGER||
|in1_guid|TEXT||
|in2_guid|TEXT||
|out_guid|TEXT||
|op_guid|TEXT||
|op_name|TEXT||
|op_code|INTEGER||

### param

|字段|类型|含义|
|:---|:---|:---|
|index|INTEGER||
|guid|TEXT||
|derived_from|TEXT||
|type_name|TEXT||
|default_size|INTEGER||
|func_CreateDefault|INTEGER||
|func_Delete|INTEGER||
|func_SaveLoad|INTEGER||
|func_Check|INTEGER||
|func_Copy|INTEGER||
|func_String|INTEGER||
|func_UICreator|INTEGER||
|creator_dll_index|INTEGER||
|creator_plugin_index|INTEGER||
|dw_param|INTEGER||
|dw_flags|INTEGER||
|cid|INTEGER||
|saver_manager|TEXT||

### plugin

|字段|类型|含义|
|:---|:---|:---|
|dll_index|INTEGER||
|dll_name|TEXT||
|plugin_index|INTEGER||
|category|TEXT||
|active|INTEGER||
|needed_by_file|INTEGER||
|guid|TEXT||
|desc|TEXT||
|author|TEXT||
|summary|TEXT||
|version|INTEGER||
|func_init|INTEGER||
|func_exit|INTEGER||

### variable

|字段|类型|含义|
|:---|:---|:---|
|name|TEXT||
|description|TEXT||
|flags|INTEGER||
|type|INTEGER||
|representation|TEXT||
|data|TEXT||

## composition.db 格式

composition.db是`Decorator`输出的所有被综合的文档与接下来三个数据库分别的内部的编号的的对应表（为每一个被综合的数据库分配一个编号，但是因为有些部分文档共用一个Virtools环境等，就需要将这些编号转换成共用的）  
使用此表是为了保证网页URL基于编号的命名方式可以在三个表中正常通行，而不会出现在这个表中的编号在另一个表里指示的是另一个Virtools文件。  
因此在查询其他数据库前需要先读取此数据库获得对应各个数据库的内部编号，进而在剩下的数据库中以内部编号继续查询。

表只有一个：composition。

## decorated.db 格式

decorated.db是`Decorator`输出的脚本综合的数据库，包含了所有脚本的连线和图形位置。

表列表：

- block：behavior的图形结构
- cell：类似local parameter的结构
- graph：脚本schematic图形
- link：脚本内的所有连线
- param：脚本里的parameter的数据

### block

|字段|类型|含义|
|:---|:---|:---|
|belong_to_graph|INTEGER||
|thisobj|INTEGER||
|name|TEXT||
|assist_text|TEXT||
|pin-ptarget|TEXT||
|pin-pin|TEXT||
|pin-pout|TEXT||
|pin-bin|TEXT||
|pin-bout|TEXT||
|x|REAL||
|y|REAL||
|width|REAL||
|height|REAL||
|expandable|INTEGER||

### cell

|字段|类型|含义|
|:---|:---|:---|
|belong_to_graph|INTEGER||
|thisobj|INTEGER||
|name|TEXT||
|assist_text|TEXT||
|x|REAL||
|y|REAL||
|type|INTEGER||

### graph

|字段|类型|含义|
|:---|:---|:---|
|graph|INTEGER||
|graph_name|TEXT||
|width|INTEGER||
|height|INTEGER||
|index|INTEGER||
|belong_to|TEXT||

### param

param为原来的info

|字段|类型|含义|
|:---|:---|:---|
|target|INTEGER||
|attach_bb|INTEGER||
|is_setting|INTEGER||
|name|TEXT||
|field|TEXT||
|data|TEXT||

### link

|字段|类型|含义|
|:---|:---|:---|
|belong_to_graph|INTEGER||
|delay|INTEGER||
|start_interface|INTEGER||
|end_interface|INTEGER||
|startobj|INTEGER||
|endobj|INTEGER||
|start_type|INTEGER||
|end_type|INTEGER||
|start_index|INTEGER||
|end_index|INTEGER||
|x1|REAL||
|y1|REAL||
|x2|REAL||
|y2|REAL||

## sheet.db 格式

sheet.db是`Decorator`输出的文档数据综合的数据库，包含了所有脚本的连线和图形位置。

表列表：

- data：同下
- header：同下
- body：同下
- param：与data.db几乎一致

## query.db 格式

query.db是`Decorator`输出的数据查询综合的数据库，包含了所有脚本内的数据部分，还有Virtools环境的可查询数据。

表列表：
- msg：从data.db - msg综合
- attr：同下
- op：同下
- param：同下
- plugin：同下
- variable：从env.db综合
