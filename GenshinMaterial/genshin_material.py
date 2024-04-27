import os, typing
import tkinter
import tkinter.ttk

class MainWindow():

    __cExpCountPresets: list[str] = [
        '角色Lv 90',
        '角色Lv 80',
        '角色技能Lv 6',
        '角色技能Lv 8',
        '角色技能Lv 9',
        '角色技能Lv 10',
    ]

    __cCraftSkills: list[str] = [
        '无',
        '行秋抄书（合成角色天赋素材时，有25％概率返还部分合成材料。）',
        '绫华复制（合成武器突破素材时，有10%概率获得2倍产出。）'
    ]

    __mWindow: tkinter.Tk
    __mInputExpPreset: tkinter.ttk.Combobox
    __mCraftSkill: tkinter.ttk.Combobox

    __mImgMaterial: tuple[tkinter.PhotoImage, tkinter.PhotoImage, tkinter.PhotoImage, tkinter.PhotoImage]
    __mInputExpected: tuple[tkinter.StringVar, tkinter.StringVar, tkinter.StringVar, tkinter.StringVar]
    __mInputAvailable: tuple[tkinter.StringVar, tkinter.StringVar, tkinter.StringVar, tkinter.StringVar]
    __mOutputResult: tuple[tkinter.StringVar, tkinter.StringVar, tkinter.StringVar, tkinter.StringVar]
    __mOutputSummary: tkinter.StringVar

    def __init__(self):
        # ===== init window first =====
        self.__mWindow = tkinter.Tk()
        self.__mWindow.title("原神材料计算")
        self.__mWindow.grid_columnconfigure(0, weight=1)
        self.__mWindow.grid_rowconfigure(0, weight=1)

        # ===== load and init resources =====
        # load image
        img_filenames: tuple[str, str, str, str] = ('mtl_green.png', 'mtl_blue.png', 'mtl_purple.png', 'mtl_gold.png')
        self.__mImgMaterial = tuple(map(lambda filename: tkinter.PhotoImage(file=self.__get_local_image_path(filename)), img_filenames))
        # init string variables
        self.__mInputExpected = tuple(map(lambda _: tkinter.StringVar(value=str(0)), range(4)))
        self.__mInputAvailable = tuple(map(lambda _: tkinter.StringVar(value=str(0)), range(4)))
        self.__mOutputResult = tuple(map(lambda _: tkinter.StringVar(value=str(0)), range(4)))
        # init output summary
        self.__mOutputSummary = tkinter.StringVar(value="啊？你怎么能看到这条文字？")

        # ===== init window content =====
        # init frame first
        frm = tkinter.ttk.Frame(self.__mWindow)
        frm.grid(column=0, row=0, sticky=tkinter.W+tkinter.E+tkinter.N+tkinter.S, padx=20, pady=20)
        for i in range(1, 6, 1):
            frm.grid_columnconfigure(i, weight=1)
        frm.grid_rowconfigure(4, weight=1)

        # init info row
        tkinter.ttk.Label(frm, text="材料类别").grid(column=0, row=0)
        for i, label_name in enumerate(('绿色材料', '蓝色材料', '紫色材料', '金色材料')):
            lb = tkinter.ttk.Label(frm, text=label_name, image=self.__mImgMaterial[i], compound='top')
            lb.grid(column=i + 1, row=0, padx=10, pady=10)

        # init expected count input row
        tkinter.ttk.Label(frm, text="期望").grid(column=0, row=1)
        for i in range(4):
            ibox = tkinter.ttk.Entry(frm, textvariable=self.__mInputExpected[i])
            ibox.grid(column=i + 1, row=1, padx=10, pady=10)
            self.__mInputExpected[i].trace_add('write', self.__inputbox_updated)
        # an extra region served for covenient input
        expfrm = tkinter.ttk.Frame(frm)
        expfrm.grid(column=5, row=1, padx=5, pady=5, sticky=tkinter.E+tkinter.W)
        self.__mInputExpPreset = tkinter.ttk.Combobox(expfrm, values=self.__cExpCountPresets, state='readonly') # readonly mean user only can pick value from list
        self.__mInputExpPreset.grid(column=0, row=0, padx=5, pady=5)
        tkinter.ttk.Button(expfrm, text="添加", command=self.__btn_append_exp).grid(column=1, row=0, padx=5, pady=5)
        tkinter.ttk.Button(expfrm, text="清空", command=self.__btn_clear_exp).grid(column=2, row=0, padx=5, pady=5)

        # init available count input row
        tkinter.ttk.Label(frm, text="现存").grid(column=0, row=2)
        for i in range(4):
            ibox = tkinter.ttk.Entry(frm, textvariable=self.__mInputAvailable[i])
            ibox.grid(column=i + 1, row=2, padx=10, pady=10)
            self.__mInputAvailable[i].trace_add('write', self.__inputbox_updated)
        # an extra region served for covenient input
        expfrm = tkinter.ttk.Frame(frm)
        expfrm.grid(column=5, row=2, padx=5, pady=5, sticky=tkinter.E+tkinter.W)
        tkinter.ttk.Button(expfrm, text="清空", command=self.__btn_clear_avail).grid(column=0, row=0, padx=5, pady=5)

        # init craft skill
        tkinter.ttk.Label(frm, text="合成技能").grid(column=0, row=3)
        self.__mCraftSkill = tkinter.ttk.Combobox(frm, values=self.__cCraftSkills, state='readonly')
        self.__mCraftSkill.grid(column=1, row=3, columnspan=4, sticky=tkinter.W+tkinter.E, padx=10, pady=10)

        # output header
        tkinter.ttk.Label(frm, text="计算结果", relief='groove').grid(column=0, row=4, columnspan=5, sticky=tkinter.W+tkinter.E+tkinter.S)

        # init shortage count output row
        tkinter.ttk.Label(frm, text="缺少").grid(column=0, row=5)
        for i in range(4):
            lb = tkinter.ttk.Label(frm, textvariable=self.__mOutputResult[i])
            lb.grid(column=i + 1, row=5, sticky=tkinter.W, padx=10, pady=10)

        # init compution result summary
        tkinter.ttk.Label(frm, textvariable=self.__mOutputSummary).grid(column=1, row=6, columnspan=4, sticky=tkinter.W, padx=10, pady=10)

        # ===== immediate do a compute first =====
        self.__compute()

    def run(self) -> None:
        self.__mWindow.mainloop()

    def __get_local_image_path(self, relative_path: str) -> str:
        return os.path.join(os.path.dirname(__file__), relative_path)

    def __inputbox_updated(self, *args) -> None:
        self.__compute()

    def __btn_append_exp(self) -> None:
        pass

    def __btn_clear_exp(self) -> None:
        for i in range(4):
            self.__mInputExpected[i].set(str(0))

    def __btn_clear_avail(self) -> None:
        for i in range(4):
            self.__mInputAvailable[i].set(str(0))

    def __compute(self) -> None:
        try:
            # try parsing data from input box
            exp_count: list[int] = list(
                map(lambda x: int(x.get()), self.__mInputExpected)
            )
            avail_count: list[int] = list(
                map(lambda x: int(x.get()), self.__mInputAvailable)
            )
            # check whether value is negative
            for val in exp_count + avail_count:
                if val < 0: raise Exception('neg val')
        except:
            # set default value
            for i in range(4):
                self.__mOutputResult[i].set('N/A')
            self.__mOutputSummary.set('数值无效')
            return

        # do a virtual crafting
        # with the compensation of expected count
        crafted_count: list[int] = list(avail_count)
        for i in range(3):
            diff: int = crafted_count[i] - exp_count[i]
            if diff > 0:
                num = diff // 3
                crafted_count[i] -= num * 3
                crafted_count[i + 1] += num

        # show shortage
        has_shortage = False
        for i in range(4):
            shortage_count: int = exp_count[i] - crafted_count[i]
            if shortage_count > 0:
                has_shortage = True
                self.__mOutputResult[i].set(str(shortage_count))
            else:
                self.__mOutputResult[i].set(str(0))

        # show summary
        if has_shortage:
            self.__mOutputSummary.set('缺少材料')
        else:
            self.__mOutputSummary.set('材料齐全')

if __name__ == '__main__':
    window = MainWindow()
    window.run()
