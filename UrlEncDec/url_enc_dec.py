import tkinter as tk
from tkinter import scrolledtext
import urllib.parse

class URLEncoderDecoderApp:

    root: tk.Tk
    updating: bool

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("URL 编码/解码工具")
        self.root.geometry("700x500")
        
        # 防止双向更新时产生循环触发
        self.updating = False
        
        self.create_widgets()
    
    def create_widgets(self):
        # ========== 上半部分 ==========
        top_frame = tk.Frame(self.root)
        top_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(10, 5))
        
        label_original = tk.Label(top_frame, text="原始文本", font=("Arial", 10, "bold"))
        label_original.pack(anchor=tk.W, pady=(0, 5))
        
        self.text_original = scrolledtext.ScrolledText(
            top_frame, 
            wrap=tk.WORD, 
            font=("Consolas", 10),
            height=10
        )
        self.text_original.pack(fill=tk.BOTH, expand=True)
        self.text_original.bind("<<Modified>>", self.on_original_change)
        
        # ========== 下半部分 ==========
        bottom_frame = tk.Frame(self.root)
        bottom_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(5, 10))
        
        label_encoded = tk.Label(bottom_frame, text="URL编码文本", font=("Arial", 10, "bold"))
        label_encoded.pack(anchor=tk.W, pady=(0, 5))
        
        self.text_encoded = scrolledtext.ScrolledText(
            bottom_frame, 
            wrap=tk.WORD, 
            font=("Consolas", 10),
            height=10
        )
        self.text_encoded.pack(fill=tk.BOTH, expand=True)
        self.text_encoded.bind("<<Modified>>", self.on_encoded_change)
        
        # 初始状态清除 Modified 标志
        self.text_original.edit_modified(False)
        self.text_encoded.edit_modified(False)
    
    def on_original_change(self, event=None):
        """上半部分文本变化时 → URL 编码，更新下半部分"""
        if self.updating:
            self.text_original.edit_modified(False)
            return
        
        if self.text_original.edit_modified():
            original_text = self.text_original.get("1.0", tk.END).rstrip("\n")
            
            # URL 编码（针对 UTF-8）
            encoded_text = urllib.parse.quote(original_text, safe='')
            
            # 更新下半部分
            self.updating = True
            self.text_encoded.delete("1.0", tk.END)
            self.text_encoded.insert("1.0", encoded_text)
            # 恢复正常颜色（如果之前是红色）
            self.text_encoded.config(fg="black")
            self.text_encoded.edit_modified(False)
            self.updating = False
            
            self.text_original.edit_modified(False)
    
    def on_encoded_change(self, event=None):
        """下半部分文本变化时 → URL 解码，更新上半部分"""
        if self.updating:
            self.text_encoded.edit_modified(False)
            return
        
        if self.text_encoded.edit_modified():
            encoded_text = self.text_encoded.get("1.0", tk.END).rstrip("\n")
            
            try:
                # URL 解码
                decoded_text = urllib.parse.unquote(encoded_text, encoding='utf-8', errors='strict')
                
                # 解码成功：更新上半部分
                self.updating = True
                self.text_original.delete("1.0", tk.END)
                self.text_original.insert("1.0", decoded_text)
                self.text_original.edit_modified(False)
                
                # 恢复下半部分文字颜色为黑色
                self.text_encoded.config(fg="black")
                self.updating = False
                
            except Exception as e:
                # 解码失败：上半部分清空
                self.updating = True
                self.text_original.delete("1.0", tk.END)
                self.text_original.edit_modified(False)
                
                # 将下半部分文字颜色变为红色
                self.text_encoded.config(fg="red")
                self.updating = False
            
            self.text_encoded.edit_modified(False)

if __name__ == "__main__":
    root = tk.Tk()
    app = URLEncoderDecoderApp(root)
    root.mainloop()
