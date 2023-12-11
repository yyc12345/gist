# 开发帮助

BMERevenge是内置于BallanceBlenderPlugin内的一套路面生成器（原本之前打算做新的2D编辑器，后来放弃了，改为直接Blender内生成）。  
此文档是BMERevenge开发中遵守的一些规定。此文档是第二版BMERevenge所用的标准，对应于BallanceBlenderPlugin 4.0及后续版本。

## 坐标系

* 坐标系系统使用Blender的右手坐标系。
* UV系统使用右手坐标系，具体参考后图。
* 面片支持N边形（N至少为3），其中以四边形和三角形面片的使用最为常见。面片的顶点序使用右手定则确定正面指向（OpenGL默认用右手坐标系，默认用右手定则确认正面；DirectX默认用左手坐标系，默认用左手定则确认正面）。

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

## 常用数据

* 贴图边框的条纹宽16像素（换算成UV为0.125）
* 下沉路面下沉0.7单位，对应的贴图减少到0.86（减少0.14）

## 原型

原型（Prototype）描述了一个组件是如何被顶点和面片组合而成的，是BMERevenge中的基础构建单元。BMERevenge中的所有结构都是由一个个原型组合而成的。  
原型使用JSON文本进行描述。下面是一个原型的描述的示例：

```json
{
    "identifier": "test",
    "showcase": {
        "title": "Test Block",
        "icon": "Flat",
    },
    "params": [
        {
            "field": "length",
            "type": "float",
            "title": "Length",
            "desc": "The size of block.",
            "default": 5.0
        },
        {
            "field": "count",
            "type": "int",
            "title": "Count",
            "desc": "Some count of this block.",
            "default": 0
        },
        {
            "field": "has_side",
            "type": "bool",
            "title": "Has Side",
            "desc": "Whether has xxx side.",
            "default": true
        }
    ],
    "vars": [
        {
            "field": "radius",
            "type": "float",
            "data": "length / 2"
        },
        {
            "field": "half_count",
            "type": "int",
            "data": "count // 2"
        },
        {
            "field": "use_long_side",
            "type": "bool",
            "data": "not has_side"
        }
    ],
    "vertices": [
        {
            "skip": "False",
            "data": "(0, 0, 0)",
        },
        {
            "skip": "has_side",
            "data": "(2.5 + radius, 0, 0)",
        },
        {
            "skip": "use_long_side",
            "data": "(2.5 + length, sin(half_count * pi * 2), 0)",
        },
        {
            "skip": "False",
            "data": "(0, 2.5 if use_long_side else 5.0, 0)",
        }
    ],
    "faces": [
        {
            "skip": "use_long_side",
            "texture": "FloorTopBorderless",
            "indices": "(0, 1, 2, 3)",
            "uvs": [
                "(0, 0.5)",
                "(0, 0)",
                "(0.5, 0 + radius * 5)",
                "(0.5, 0.5)"
            ]
        },
        {
            "skip": "not use_long_side",
            "texture": "FloorTopBorderless_ForSide",
            "indices": "(3, 2, 1, 0)",
            "uvs": [
                "(0, 0.5)",
                "(0, 0)",
                "(0.5, 0 + radius * 5)",
                "(0.5, 0.5)"
            ]
        },
    ],
    "instances": [
        {
            "identifier": "another_test",
            "skip": "not use_long_side",
            "params": {
                "arg1": "not use_long_side",
                "arg2": "length != 0"
            },
            "transform": "translate(2.5, 2.5, 0) @ rot(0, 0, 90)"
        },
        {
            "identifier": "another_test",
            "skip": "not use_long_side",
            "params": {
                "arg1": "not use_long_side",
                "arg2": "length != 0"
            },
            "transform": "translate(-2.5, -2.5, 0) @ rot(0, 0, -90)"
        }
    ]
}
```

### 标识符

标识符（`identifier`字段）表示了当前原型的全局唯一名称。该名称不得重复定义。

### 展示与模板

展示（`showcase`字段）表示了当前原型显示在插件创建菜单里所需要的数据。  
其中标题（`title`字段）表示了其显示的名称。图标（`icon`字段）决定了图标。这些图标被存储在专用的图标文件夹内。图标字段的值为对应图标的文件名部分（去除后缀名）。  

原型有模板与非模板之分。只有非模板的原型才会被显示在插件的创建菜单中。模板原型不会被显示，他们只能作为其它原型的基础组件被引用来进行使用。  
由于只有非模板原型才会被显示，因此也只有非模板原型才需要展示字段。所以展示字段的另一个功能是用来区分模板与非模板原型。当展示字段为`null`时，表示这是一个模板原型。否则其应当为一个非模板原型并具有上述结构。

### 参数

参数（`params`字段）定义了当前原型接受的参数，与函数调用中的参数类似，其决定了这个原型内的一些重要尺寸与结构。

参数字段是一个列表，列表中每一项定义一个参数。参数定义由以下几个方面组成：

* `field`：参数名称。不得重复定义。
* `type`：参数类型。只能是float, int, bool其中之一。
* `title`：参数显示名称。参数在插件创建界面显示的名称。
* `desc`：参数解释。参数在插件创建界面触碰时显示的提示说明文本。
* `default`：参数的默认值。默认值类型由参数类型决定。

当从插件创建界面接受用户输入时，根据参数类型，参数数值具有一些约束。这些约束是：

* float：总是不小于0
* int：总是不小于0
* bool：只能为true或false

需要注意的是，当从`instances`调用子原型，设定参数并传递时则没有这些约束。这些约束只是由于用户界面的设定而被约束的。即约束只对顶级原型的参数有效。

### 可编程字段

BMERevenge使用可编程字段来使得模型可以按照用户需要的大小与需求，在尽可能减少多边形数量的情况下进行构建。  
可编程字段在底层使用Python的`eval`函数进行计算。可编程字段可以使用大多数的Python语法内容，但可使用的函数是受限的。下表列出了一些可编程字段中常用的运算，以及引擎提供的函数：

* `()`：括号，强制结合。
* `+-*/`：四则运算，优先级与数学一致。
* `// @ **`：各种Python专有运算符。其中`@`可用于`mathutils.Matrix`矩阵之间的乘法。
* 立即数：即显式指定的浮点数或整数。
* 参数字段中指定的变量名：由参数字段决定的有限的只读变量的引用。
* 变量字段中指定的变量名：由变量字段决定的有限的只读变量的引用。请注意在计算变量时不会提供这些。
* `abs sqrt pow sin cos tan asin acos atan`：各式数学函数
* `pi`：数学常量

### 变量

变量（`vars`字段）定义了当前原型所需要用到的一些额外数据。有些时候原型的创建中需要频繁用到某一项组合计算数值，那么可以将其独立成变量，先行计算，再在后续内容中引用它即可。  
请注意，虽然名义上是变量，但其实际上是常量。其数值在参数传入后计算，并且不可以在可编程字段中更改。

变量字段是一个列表，列表中每一项定义一个变量。与参数列表类似。

* `field`：参数名称。不得重复定义。
* `type`：参数类型。只能是float, int, bool其中之一。
* `data`：一个可编程字段。其结果为计算得到的参数值。其返回的数据类型必须与参数类型指定的一致。

### 顶点

变量（`vertices`字段）定义了当前原型的网格顶点数据。

### 面

面（`faces`字段）定义了当前原型的网格面数据。

### 实例

实例（`instances`字段）定义了当前原型所引用的子原型。可以通过多个子原型来拼接得到一个大原型。

## 构建

构建从用户选取的原型开始。首先获取用户输入。这些输入是被钳制在一定范围内的，然后将其输入用户选取的原型，即顶层原型。  
然后根据参数计算原型的变量字段。获取执行所需要的全部数据。  
然后根据顶点和面字段，按需求创建顶点和面。  
如果实例字段有指定，则计算传递给实例的参数，并递归调用本过程，继续为当前Mesh添加数据，直到顶层原型的所有实例创建完毕。
