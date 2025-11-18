use windows_sys::Win32::Foundation::HWND;
use windows_sys::Win32::UI::WindowsAndMessaging::{PostMessageW, WM_MOUSEWHEEL};

pub fn post_mouse_wheel(hwnd: HWND, x: i32, y: i32, delta: i32) {
    // Method 1: Try using SendMessage with WM_MOUSEWHEEL
    unsafe {
        PostMessageW(
            hwnd,
            WM_MOUSEWHEEL,
            (delta << 16) as usize,              // wParam: delta in high word
            ((y << 16) | (x & 0xFFFF)) as isize, // lParam: y in high word, x in low word
        )
    };
}
