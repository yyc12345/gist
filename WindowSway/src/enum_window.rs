use windows_sys::Win32::Foundation::{HWND, LPARAM};
use windows_sys::Win32::UI::WindowsAndMessaging::{
    EnumWindows, GetWindowTextLengthW, GetWindowTextW, IsWindowVisible,
};
use windows_sys::core::BOOL;

#[derive(Debug)]
pub struct WindowInfo {
    hwnd: HWND,
    title: String,
    is_visible: bool,
}

impl WindowInfo {
    pub fn get_hwnd(&self) -> HWND {
        self.hwnd
    }

    pub fn get_title(&self) -> &str {
        self.title.as_str()
    }

    pub fn get_is_visible(&self) -> bool {
        self.is_visible
    }
}

extern "system" fn enum_windows_proc(hwnd: HWND, lparam: LPARAM) -> BOOL {
    let len = unsafe { GetWindowTextLengthW(hwnd) };
    let mut window_text = vec![0u16; (len + 1).try_into().unwrap()];
    let len = unsafe { GetWindowTextW(hwnd, window_text.as_mut_ptr(), 256) };
    let title = String::from_utf16_lossy(&window_text[..len as usize]);

    let is_visible = unsafe { IsWindowVisible(hwnd) != 0 };

    let windows = unsafe { &mut *(lparam as *mut Vec<WindowInfo>) };
    windows.push(WindowInfo {
        hwnd,
        title,
        is_visible,
    });

    return 1;
}

pub fn get_all_windows() -> Vec<WindowInfo> {
    let mut windows: Vec<WindowInfo> = Vec::new();
    unsafe {
        EnumWindows(Some(enum_windows_proc), &mut windows as *mut _ as LPARAM);
    }
    windows
}
