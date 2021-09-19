# 目录

* BallanceTournamentGenerator
    * ExampleGenerator.py：一个用于生成比赛流程样例的程序，已经没有用了，比赛制度和现在的吧赛制度不一样
    * TableGenerator.py：生成Mediawiki用的淘汰赛图表，仍然可以用
* BilibiliPhoneDownloadedVideoMerge：自用的用来生成批量合并Android Bilibili客户端下载的视频的脚本
* BMCodeHelper
    * ComponentGenerator.py：用于生成yyc制图工具链依赖的component文件结构的脚本，从obj转换文件格式到yyc制图工具链可读格式（obj需要为已经转换坐标系为Blender的格式）
    * CaseMigrate：迁移代码中的外置贴图列表的switch，将新的case数值匹配到旧的case代码上
* BMERevenge：内嵌于BallanceBlenderHelper的用于快速生成路面的组件的开发文档
* BMFileSpec：下属文件包括BM的标准文档以及yyc制图工具链的标准文档
* ChemistryEquation：一个解化学方程式的玩意。之前初中写过一个差不多的，这次是重写。初中写的那个手撕了一个词法语法分析器，效率奇差，bug超多。
    * FlexBison：一个用于解析化学方程式并输出Binary语法树方便读取的Flex Bison词法语法分析器模板。虽然用Flex Bison解析化学方程式有点杀鸡用牛刀，但最近在学习编译器就学习一下使用方法。
    * Computer：读取Binary语法树，构建线性齐次方程组，使用线性代数方法求解
* CK2Compare：包含可以批量比较不同版本CK2、VxMath DLL之间API的脚本，以及服务于本人已放弃的Virtools兼容层工程，CK3的生成器，补丁器代码。
* Coconut-leafAssist：名字说的个人制作的日历Coconut-leaf，实际上是把ics转成csv可视化的工具
* DecompSpiritTrail：用于暴力解析Gamepiaynmo所写BML Mod，SpiritTrail的影子球录像文件的代码
* DigitalSignalProcess：个人乱写的数字信号处理的某些函数的手写版，个人锻炼用。
* FreeBallSpeed：给Ballance吧吧务开发的用于极限竞速榜单的改球速工具
* FuckChaoXing：在自己学校里超星客户端上的破解视频离开就停止播放的插件，附带视频中间停止后提示答题的声音，方便快速挂课。
* GamepiaynmoMod：Gamepiaynmo的Mod的存储文件的说明文档，个人制作。目前只有TAS的录制文件格式。
* LCRConnect：在3个元器件内，使用给定元器件数值列表快速找到目标数值元器件的最好拼接方式，支持电阻，电容，电感
* NetworkKeepAlive：个人用的自动拨号器，一旦掉线自动重连，解决学校天天自动给我断网的问题。
* SuperScriptMaterializer：本人的项目SuperScriptMaterializer的个人用的开发记录手册，记录了一些内容方便我在之后快速重拾这个工程。
* VerlogCourseDesign：个人的Verlog课设，出租车计价器（好像是只能模拟不能综合的版本，新版本懒得传了）
* VirtoolsNLP：一个可以解析和回写Virtools Dev的NLP语言包文件的脚本。
