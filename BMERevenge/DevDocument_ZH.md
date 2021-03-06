# 开发帮助

BMERevenge是内置于BallanceBlenderPlugin内的一套路面生成器（原本之前打算做新的2D编辑器，后来放弃了，改为直接Blender内生成）

此文档是BMERevenge开发中遵守的一些规定

## Prototype

### 坐标系

* 坐标系系统使用Blender的右手坐标系
* UV系统使用右手坐标系，具体参考后图
* 原型中为了书写方便，使用四边形面，并且Blender也支持四边形面，可以直接写入。四边形面顶点序使用右手定则确定正面指向（OpenGL默认用右手坐标系，默认用右手定则确认正面；DirectX默认用左手坐标系，默认用左手定则确认正面）。原型中同时也使用三角形面，规定与四边形面一致
* 各个面的定义按方块左上角顶面位置为原点，以3D坐标系定义（不要使用Screen坐标系）（如果顶面左上角有下沉，则按未下沉的位置定义）
* 每种方块具有延伸方向的属性，对于Column模式的方块，其延伸方向即为延伸方向指定的方向，而对于Freedom模式的方块，由于是可以沿着两个方向进行延伸，则规定延伸方向指定的方向为第一延伸方向，第二延伸方向在第一方向顺时针旋转后的下一个方向
* 方块的Mesh内的旋转方向定义为Z轴的右手螺旋方向（+Z与右手螺旋指向一致，螺旋方向为旋转方向）

```
     +-----------------------------+
+V   |                             |
     | Image                       |
 ^   |                             |
 |   |                             |
 |   |                             |
 |   |                             |
 |   |                             |
 |   |                             |
 |   |                             |
 |   |                             |
 |   |                             |
 |   +-----------------------------+
 |
 +----------------------->  +U

 UV coordinate system

```

```
Blender coordinate system

                  +Z

                   X
                   X
                   X
                   X
                   X
                   X
                   X
                   X
                   X
                   X
                   XXXXXXXXXXXXXXXXXXXXXXXXX
                 XX                          +Y
               XXX
              XX
             XX
           XXX
          XX
        XXX
       XX
      XX
      X

+X

```


```
                                       +                             ^
Expand direction        +-->           |            <--+             |
                                       v                             +

                   +---------+    +---------+    +---------+    +---------+
                   |         |    |         |    |         |    |         |
                   |         |    |         |    |    ^    |    |    ^    |
Freedom block      |         |    |         |    |    |    |    |    |    |
                   |    +--> |    | <--+    |    | <--+    |    |    +--> |
                   |    |    |    |    |    |    |         |    |         |
                   |    v    |    |    v    |    |         |    |         |
                   |         |    |         |    |         |    |         |
                   +---------+    +---------+    +---------+    +---------+

                   +---------+    +---------+    +---------+    +---------+
                   |         |    |         |    |         |    |         |
                   |         |    |         |    |         |    |    ^    |
                   |         |    |         |    |         |    |    |    |
Column block       |    +--> |    |    +    |    | <--+    |    |    +    |
                   |         |    |    |    |    |         |    |         |
                   |         |    |    v    |    |         |    |         |
                   |         |    |         |    |         |    |         |
                   +---------+    +---------+    +---------+    +---------+

```

### 单位

* 贴图边框的条纹宽16像素（换算成UV为0.125）
* 下沉路面下沉0.7单位，对应的贴图减少到0.86（减少0.14）

### 网格

#### 顶点

原型的网格的每个顶点的三维坐标格式：`x,y,z;x_offset;y_offset;z_offset`

其中`xyz`表示坐标，为浮点或整数（整数当作浮点处理）

`offset`可以由下列字符中的任何一个填写，每个字符表述对应的坐标份量是否受某个轴的延伸所影响，并指定延伸方向。如果`offset`不存在，留空。在任何情况下，分号都不可以省略

X和Y方向，大方块每次延伸5，小方块每次延伸2.5。Z方向则无论大小方块，都为延伸倍数x5。延伸方向的正负实际上是决定是否为延伸方向数值取相反数再加到原数值上。实际计算的时候遵循`x += unit * d * (direction ? 1 : -1)`

* `+d1` 主延伸方向正向
* `-d1` 主延伸方向反向
* `+d2` 次延伸方向正向
* `-d2` 次延伸方向反向
* `+d3` 高度延伸方向正向
* `-d3` 高度延伸方向反向

一些示例：
* `1,1,1;;;`
* `1.0,1.0,1.0;;;`
* `1.0,1.0,1.2;+d1`
* `1.0,2,3.3;+d3+d2-d1`


#### 顶点UV

原型的网格的每个顶点的顶点UV坐标格式：`u,v;u_offset;v_offset`

其中`uv`表示坐标，为浮点或整数（整数当作浮点处理）

`u_offset`和`v_offset`可以由下列字符中的任何一个填写，每个字符表述对应的坐标份量是否受某个轴的延伸所影响，并指定延伸方向。在任何情况下，分号都不可以省略

X和Y方向，大方块每次延伸1，小方块每次延伸0.5。Z方向则无论大小方块，都为延伸倍数x1。延伸方向的正负实际上是决定是否为延伸方向数值取相反数再加到原数值上。实际计算的时候遵循`u += unit * d * (direction ? 1 : -1)`

* `+d1` 主延伸方向正向
* `-d1` 主延伸方向反向
* `+d2` 次延伸方向正向
* `-d2` 次延伸方向反向
* `+d3` 高度延伸方向正向
* `-d3` 高度延伸方向反向

一些示例：
* `0.2,0.2;;`
* `0.2,0.1;;+d2`
* `0.2,0.1;+d1;`
* `0.2,0.1;-d3;+d2`

### 构建

#### Vanilla block

一个物体的构建遵循如下过程：

将起始方块的中心当作坐标原点开始构建，因为默认是以左上角为原点的，因此需要根据方块大小平移一定位置（小块1.25，大块2.5来达到上述要求）

然后读取延伸规定，按默认延伸方向延伸。

然后读取旋转参数，对模型中的每一个三维坐标乘以旋转矩阵，达到旋转目的，之后再平移到正确的起始方块位置。

#### Derived block

拆分成Vanilla block然后构建。

### Smashed vanilla blocks

#### StartPosition & ExpandPosition

表述方块的起始和延伸位置的二维坐标格式：`x,y;xSyncOffset,xSync,ySyncOffset,ySync`

其中`xy`表示坐标（起始点）或d1, d2的数值（延伸数值，根据延伸模式，可能有些数值不会被使用），为非负整数，分号和逗号不可以省略。

`SyncOffset`，整数，表示当后续同步设置时，会将同步选项所同步的长度加上此指定数值（若为负数则相当于减去）。如果不存在，默认为0。

`Sync`可以由下列字符其中之一，表述当前指定方向与主方块的哪个延伸方向进行同步。如果`Sync`不存在，表述不同步。

计算方法遵循`x += unit * (d + syncOffset) * (direction ? 1 : -1)`

* `d1` 同步主延伸方向数值
* `d2` 同步次延伸方向数值

一些示例：
* `0,0;,,,`
* `0,0;,d1,d2`
* `1,1;2,d1,-2,d2`

*似乎Offset和初始数值重复了，不过因为懒就不打算将其合并了*

#### SideSync

指定Derived block中Smashed vanilla block的边同步属性，遵循如下格式`2dTop;2dRight;2dBottom;2dLeft;3dTop;3dBottom`

其中每一项可以是下面列表中的任意一项，分隔符分号不可省略，不可留空：

直接指定是否要这个面：

* `True`
* `False`

与主方块同步属性：

* `2dTop`
* `2dRight`
* `2dBottom`
* `2dLeft`
* `3dTop`
* `3dBottom`

示例：

* `True;False;2dLeft;3dTop;3dTop;3dBottom`
* `True;True;True;True;True;True`

### 杂项

* Derived block中的unit大小指的是判断起始坐标偏移Unit是按大方块还是小方块方式偏移
* Vanilla block和Basic block是一个东西，只是因为前后改名的缘故导致不一致
* Derived block或者Vanilla block的延伸长度并不一定指代其最终长度是`length * unit`。例如Derived block - NormalPlatform，其具有一个最小大小，延伸为0时其为最小状态（3 x Small unit的正方形），延伸指的是它在最小状态向外延伸的长度
* 设计上，方块的有边缘纹路的边侧才需要使用FloorSide，其余的边（即正常不应该有的边侧）应当使用全白的材质（就是那个无边框路面材质）
* Faces中的Type指定了面的类型，RECTANGLE为四边形，TRIANGLE为三角形
