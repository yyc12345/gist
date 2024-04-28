import os, enum
import tkinter
import tkinter.ttk
import tkinter.font

class ExpectedPreset(enum.Enum):
    CharMobLv80 = '角色Lv 80大世界普怪素材'
    CharMobLv90 = '角色Lv 90大世界普怪素材'
    SkillMobLv6 = '角色技能Lv 6大世界普怪素材'
    SkillMobLv8 = '角色技能Lv 8大世界普怪素材'
    SkillMobLv9 = '角色技能Lv 9大世界普怪素材'
    SkillMobLv10 = '角色技能Lv 10大世界普怪素材'
    SkillBookLv6 = '角色技能Lv 6天赋书'
    SkillBookLv8 = '角色技能Lv 8天赋书'
    SkillBookLv9 = '角色技能Lv 9天赋书'
    SkillBookLv10 = '角色技能Lv 10天赋书'
EXPECTED_PRESET_LIST: list[str] = list(
    map(lambda x: x.value, ExpectedPreset)
)
EXPECTED_PRESET_DICT: dict[ExpectedPreset, tuple[int, int, int, int, int]] = {
    ExpectedPreset.CharMobLv80: (18, 30, 12, 0, 0),
    ExpectedPreset.CharMobLv90: (18, 30, 36, 0, 0),
    ExpectedPreset.SkillMobLv6: (6, 22, 0, 0, 0),
    ExpectedPreset.SkillMobLv8: (6, 22, 10, 0, 0),
    ExpectedPreset.SkillMobLv9: (6, 22, 19, 0, 0),
    ExpectedPreset.SkillMobLv10: (6, 22, 31, 0, 0),
    ExpectedPreset.SkillBookLv6: (0, 3, 21, 0, 0),
    ExpectedPreset.SkillBookLv8: (0, 3, 21, 10, 0),
    ExpectedPreset.SkillBookLv9: (0, 3, 21, 22, 0),
    ExpectedPreset.SkillBookLv10: (0, 3, 21, 38, 0),
}

IMG_FILENAME: tuple[str, str, str, str] = (
    'mtl_grey.png', 
    'mtl_green.png', 
    'mtl_blue.png', 
    'mtl_purple.png', 
    'mtl_gold.png'
)

PADDING: int = 10

class MainWindow():

    __mWindow: tkinter.Tk
    __mBoldFont: tkinter.font.Font
    __mExpectedPresetCombobox: tkinter.ttk.Combobox

    __mImgMaterial: tuple[tkinter.PhotoImage, tkinter.PhotoImage, tkinter.PhotoImage, tkinter.PhotoImage, tkinter.PhotoImage]
    __mExpected: tuple[tkinter.StringVar, tkinter.StringVar, tkinter.StringVar, tkinter.StringVar, tkinter.StringVar]
    __mAvailable: tuple[tkinter.StringVar, tkinter.StringVar, tkinter.StringVar, tkinter.StringVar, tkinter.StringVar]
    __mShortage: tuple[tkinter.StringVar, tkinter.StringVar, tkinter.StringVar, tkinter.StringVar, tkinter.StringVar]
    __mSummary: tkinter.StringVar

    def __init__(self):
        # ===== init window first =====
        # create window
        self.__mWindow = tkinter.Tk()
        # set title
        self.__mWindow.title("原神材料计算")
        # order its single frame child resizable
        self.__mWindow.grid_columnconfigure(0, weight=1)
        self.__mWindow.grid_rowconfigure(0, weight=1)

        # ===== load and init resources =====
        # load font
        self.__mBoldFont = tkinter.font.Font(weight='bold')
        # load image
        self.__mImgMaterial = tuple(
            map(lambda filename: tkinter.PhotoImage(file=self.__get_local_image_path(filename)), IMG_FILENAME)
        )
        # init intput string
        self.__mExpected = tuple(map(lambda _: tkinter.StringVar(value=str(0)), range(5)))
        self.__mAvailable = tuple(map(lambda _: tkinter.StringVar(value=str(0)), range(5)))
        # init output string and summary
        self.__mShortage = tuple(map(lambda _: tkinter.StringVar(value='あ？'), range(5)))
        self.__mSummary = tkinter.StringVar(value="あ？何で君はこの文字を見えますが？")

        # ===== init window content =====
        # init frame
        frm = tkinter.ttk.Frame(self.__mWindow)
        frm.grid(column=0, row=0, padx=PADDING, pady=PADDING, sticky=tkinter.NSEW)
        # let its child resizable
        # every columns should be resizable, however, title column should not.
        for i in range(1, 7, 1):
            frm.grid_columnconfigure(i, weight=1)
        # only result banner is resizable
        frm.grid_rowconfigure(4, weight=1)

        # init material info row
        tkinter.ttk.Label(frm, text="材料类别").grid(column=0, row=0, padx=PADDING, pady=PADDING)
        for i, label_name in enumerate(('灰色材料', '绿色材料', '蓝色材料', '紫色材料', '金色材料')):
            lb = tkinter.ttk.Label(frm, text=label_name, image=self.__mImgMaterial[i], compound='top')
            lb.grid(column=i + 1, row=0, padx=PADDING, pady=PADDING)

        # input header
        hdrfrm = tkinter.ttk.Frame(frm, relief='groove')
        hdrfrm.grid(column=0, row=1, columnspan=6, sticky=tkinter.EW)
        hdrfrm.columnconfigure(0, weight=1)
        tkinter.ttk.Label(hdrfrm, text="现实状况", font=self.__mBoldFont).grid(padx=PADDING, pady=PADDING)

        # init expected count input row
        tkinter.ttk.Label(frm, text="期望").grid(column=0, row=2, padx=PADDING, pady=PADDING)
        for i in range(5):
            # create widget
            ibox = tkinter.ttk.Entry(frm, textvariable=self.__mExpected[i])
            ibox.grid(column=i + 1, row=2, sticky=tkinter.EW, padx=PADDING, pady=PADDING)
            # update computed result when value changed
            self.__mExpected[i].trace_add('write', self.__inputbox_updated)
        # an extra frame served for covenient input
        operfrm = tkinter.ttk.Frame(frm)
        operfrm.grid(column=6, row=2, padx=PADDING, pady=PADDING, sticky=tkinter.EW)
        for i in range(3):
            operfrm.columnconfigure(i, weight=1)
        # create a combobox within frame with readonly state which force user only can pick item from list,
        # and block manual input.
        # in addition, we set its index to first entry
        self.__mExpectedPresetCombobox = tkinter.ttk.Combobox(operfrm, values=EXPECTED_PRESET_LIST, state='readonly')
        self.__mExpectedPresetCombobox.grid(column=0, row=0, sticky=tkinter.EW, padx=PADDING, pady=PADDING)
        self.__mExpectedPresetCombobox.current(newindex=0)
        tkinter.ttk.Button(operfrm, text="累加", command=self.__btn_append_exp).grid(column=1, row=0, sticky=tkinter.EW, padx=PADDING, pady=PADDING)
        tkinter.ttk.Button(operfrm, text="清空", command=self.__btn_clear_exp).grid(column=2, row=0, sticky=tkinter.EW, padx=PADDING, pady=PADDING)

        # init available count input row
        tkinter.ttk.Label(frm, text="现存").grid(column=0, row=3, padx=PADDING, pady=PADDING)
        for i in range(5):
            # create widget
            ibox = tkinter.ttk.Entry(frm, textvariable=self.__mAvailable[i])
            ibox.grid(column=i + 1, row=3, sticky=tkinter.EW, padx=PADDING, pady=PADDING)
            # update computed result when value changed
            self.__mAvailable[i].trace_add('write', self.__inputbox_updated)
        # an extra region served for covenient input
        operfrm = tkinter.ttk.Frame(frm)
        operfrm.grid(column=6, row=3, padx=PADDING, pady=PADDING, sticky=tkinter.EW)
        operfrm.columnconfigure(0, weight=1)
        tkinter.ttk.Button(operfrm, text="清空", command=self.__btn_clear_avail).grid(sticky=tkinter.EW, padx=PADDING, pady=PADDING)

        # output header
        hdrfrm = tkinter.ttk.Frame(frm, relief='groove')
        hdrfrm.grid(column=0, row=4, columnspan=6, sticky=tkinter.EW+tkinter.S)
        hdrfrm.columnconfigure(0, weight=1)
        tkinter.ttk.Label(hdrfrm, text="计算结果", font=self.__mBoldFont).grid(padx=PADDING, pady=PADDING)

        # init shortage count output row
        tkinter.ttk.Label(frm, text="缺少").grid(column=0, row=5, padx=PADDING, pady=PADDING)
        for i in range(5):
            # create widget
            lb = tkinter.ttk.Label(frm, textvariable=self.__mShortage[i])
            lb.grid(column=i + 1, row=5, sticky=tkinter.W, padx=PADDING, pady=PADDING)

        # init compution result summary
        tkinter.ttk.Label(frm, text="结论").grid(column=0, row=6, padx=PADDING, pady=PADDING)
        tkinter.ttk.Label(frm, textvariable=self.__mSummary).grid(column=1, row=6, columnspan=5, sticky=tkinter.W, padx=PADDING, pady=PADDING)

        # ===== immediate do a compute first =====
        self.__compute()

    def run(self) -> None:
        self.__mWindow.mainloop()

    def __get_local_image_path(self, relative_path: str) -> str:
        return os.path.join(os.path.dirname(__file__), relative_path)

    def __inputbox_updated(self, *args) -> None:
        self.__compute()

    def __btn_append_exp(self) -> None:
        # get selected index return in invalid scenario
        idx: int = self.__mExpectedPresetCombobox.current()
        if idx < 0 or idx >= len(EXPECTED_PRESET_LIST):
            return
        # get preset type from index
        exp_type: ExpectedPreset = ExpectedPreset(EXPECTED_PRESET_LIST[idx])

        # get value tuple from dict
        exp_count = EXPECTED_PRESET_DICT[exp_type]
        # then increase input by gotten data
        for i in range(5):
            # try parsing current value with fallback (0)
            try:
                parsed_int = int(self.__mExpected[i].get())
            except:
                parsed_int = 0
            # add into previous value
            self.__mExpected[i].set(str(parsed_int + exp_count[i]))

    def __btn_clear_exp(self) -> None:
        for i in range(5):
            self.__mExpected[i].set(str(0))

    def __btn_clear_avail(self) -> None:
        for i in range(5):
            self.__mAvailable[i].set(str(0))

    def __compute(self) -> None:
        try:
            # try parsing data from input box
            expected_counts: list[int] = list(
                map(lambda x: int(x.get()), self.__mExpected)
            )
            available_counts: list[int] = list(
                map(lambda x: int(x.get()), self.__mAvailable)
            )
            # check whether value is negative
            for val in expected_counts + available_counts:
                if val < 0: raise Exception('neg val')
        except:
            # if fail to parse value
            # set error value and return to notice user
            for i in range(5):
                self.__mShortage[i].set('N/A')
            self.__mSummary.set('数值无效')
            return

        # do a virtual crafting.
        # we try craft higher material as many as possible
        # in the premise that we can compensate the order of lower material.
        crafted_counts: list[int] = list(available_counts)
        for i in range(5 - 1):
            diff: int = crafted_counts[i] - expected_counts[i]
            if diff > 0:
                crafted_count= diff // 3
                crafted_counts[i] -= crafted_count * 3
                crafted_counts[i + 1] += crafted_count

        # show shortage and check whether have shortage
        has_shortage = False
        for i in range(5):
            shortage_count: int = expected_counts[i] - crafted_counts[i]
            if shortage_count > 0:
                has_shortage = True
                self.__mShortage[i].set(str(shortage_count))
            else:
                self.__mShortage[i].set(str(0))

        # show summary according to the status about computed shortage
        if has_shortage:
            self.__mSummary.set('材料不够，赶紧去刷')
        else:
            self.__mSummary.set('材料齐全，睡大觉喽')

if __name__ == '__main__':
    window = MainWindow()
    window.run()
