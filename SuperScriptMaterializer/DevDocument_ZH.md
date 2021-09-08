# 开发帮助

此文档将叙述一些开发SuperScriptMaterializer中需要被记忆的一些原则。

## 可能的连线

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


## export.db 格式

export.db导出的是当前Virtools文档内的脚本数据，还附带有其内一些Object，例如Mesh, 3D Object, Array等数据，方便后期分析。

表列表：

- 脚本部分
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
- 数据部分
  - dataObj：数据部分存储每个文档里每个元素的基本类型
  - dataHeader：见下
  - dataBody：Header和Body，定义了一个类似于Array的表格，Array就按Array的格式存储，而其他物件，则将属性作为表头，然后本身作为表内的唯一一行数据记录
  - dataParam：如果表内对应的部分是引用，那么引用的数据应该存储在这里，按照类似pData的方式存储，表内使用代替性文字。
  - msg：当前文档内定义的message标号与数值的对应

## env.db 格式

env.db导出的是当前Virtools环境的数据，与文档无关，这部分如果是多个文件共用一个环境，那么只需要导出和在`Decorator`里综合一次即可

表列表：

- attr：attribute
- op：operator，parameter转换的定义
- param：parameter的定义
- plugin：当前环境插件
- variable：全局变量数据

## decorated.db 格式

decorated.db是`Decorator`输出的脚本综合的数据库，包含了所有脚本的连线和图形位置。

表列表：

- block：behavior的图形结构
- cell：类似local parameter的结构
- graph：脚本schematic图形
- link：脚本内的所有连线
- composition：所有被综合的文档的对应表（为每一个被综合的数据库分配一个编号）

## query.db 格式

query.db是`Decorator`输出的数据查询综合的数据库，包含了所有脚本内的数据部分，还有Virtools环境的可查询数据。

表列表：

- scriptParam：脚本里的parameter的数据（从export.db - dataObj综合）
- objectData：同下
- objectHeader：同下
- objectBody：同下
- objectParam：从export.db里类似字段综合
- msg：从export.db - msg综合
- attr：同下
- op：同下
- param：同下
- plugin：同下
- variable：从env.db综合
- composition：所有被综合的文档与本数据库内部的编号的的对应表（为每一个被综合的数据库分配一个编号，但是因为有些部分文档共用一个Virtools环境等，就需要将这些编号转换成共用的）
