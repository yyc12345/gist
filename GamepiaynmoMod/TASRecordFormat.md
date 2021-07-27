# TAS Record File Format

本文为Gamepiaynmo所作Ballance Mod，TAS其对应的记录文件的非官方格式文档。本文档不能保证与原作者最新的Mod相匹配，请以原作者程序所写为准，本文档仅供参考。

## 基本结构

|助记符|大小与类型|
|:---|:---|
|HEADER|4 byte / int32_t|
|ZLIB_BODY|可变|

### ZLIB_BODY

ZLIB_BODY表示了TAS的数据，其使用了Zlib进行压缩（压缩率为9）然后写入文件。要获取或写入TAS数据，首先需要对ZLIB_BODY部分进行Zlib相关的处理。

### HEADER

HEADER指示了后面的BODY区块原本的长度，因为ZLIB_BODY区块使用Zlib进行压缩，所以HEADER中读取的数值是ZLIB_BODY解压后的长度。

## 解压后的ZLIB_BODY

解压后的ZLIB_BODY结构（后称为BODY）如下图所示

|助记符|大小与类型|
|:---|:---|
|TAS_CHUNK|8 byte|
|TAS_CHUNK|8 byte|
|...|...|

BODY可以由任意多个TAS_CHUNK前后连接组成。

## TAS_CHUNK

每个TAS_CHUNK结构如下

|助记符|大小与类型|
|:---|:---|
|DELTA_TIME|4 byte / float|
|KEY_STATES|4 byte|

### DELTA_TIME

DELTA_TIME为一个浮点数，将在TAS Mod中被输入Virtools引擎以控制当前帧的长度，通常来说，在一个TAS文件中，所有帧的此数值应一致，但不排除例外。也有例子反馈在不同机器上此数值不同，且不同数值机器上的TAS记录文件不能互相播放。

### KEY_STATES

KEY_STATES表示当前帧的按键状态，此数值是按位进行分析的，它的结构如下

|位|31-9|8|7|6|5|4|3|2|1|0|
|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|
|助记符|-|KEY_ENTER|KEY_ESC|KEY_Q|KEY_SPACE|KEY_SHIFT|KEY_RIGHT|KEY_LEFT|KEY_DOWN|KEY_UP|
|含义|保留部分，不使用|回车|Esc|Q|空格|Shift|右箭头|左箭头|下箭头|上箭头|

对应键被按下，则对应位被设置为`1`，否则，设置为`0`，保留的`31-9`位为恒为`0`。  
需要注意的是，对应按键如果在设置中可替换的话（例如上下左右等），读取的是设置中真实设置的按键，表格中`对应按键`则为其对应功能的默认按键