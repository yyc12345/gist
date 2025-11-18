use std::sync::atomic::Ordering;

use windows_sys::Win32::Foundation::{HWND, LPARAM, LRESULT, WPARAM};
use windows_sys::Win32::System::LibraryLoader::GetModuleHandleW;
use windows_sys::Win32::System::Threading::GetCurrentThreadId;
use windows_sys::Win32::UI::WindowsAndMessaging::{
    CallNextHookEx, HC_ACTION, MSG, SetWindowsHookExW, UnhookWindowsHookEx, WH_GETMESSAGE,
};
use windows_sys::Win32::UI::WindowsAndMessaging::{
    WA_INACTIVE, WM_ACTIVATE, WM_ACTIVATEAPP, WM_NCACTIVATE,
};

static TARGET_HWND: std::sync::atomic::AtomicIsize = std::sync::atomic::AtomicIsize::new(0);
static HOOK: std::sync::atomic::AtomicIsize = std::sync::atomic::AtomicIsize::new(0);

extern "system" fn get_message_hook(code: i32, wparam: WPARAM, lparam: LPARAM) -> LRESULT {
    if code >= 0 && (code as u32) >= HC_ACTION {
        let msg = unsafe { &*(lparam as *const MSG) };
        let target_hwnd = TARGET_HWND.load(Ordering::SeqCst) as HWND;

        if msg.hwnd == target_hwnd {
            // Block activation messages to prevent losing focus
            if msg.message == WM_ACTIVATE
                || msg.message == WM_ACTIVATEAPP
                || msg.message == WM_NCACTIVATE
            {
                if msg.wParam == WA_INACTIVE as WPARAM {
                    // Block the message - don't call CallNextHookEx
                    return 1; // Indicate message is processed and should not be further processed
                }
            }
        }
    }

    unsafe { CallNextHookEx(std::ptr::null_mut(), code, wparam, lparam) }
}

pub fn prevent_window_from_losing_focus(hwnd: HWND) -> bool {
    TARGET_HWND.store(hwnd as isize, Ordering::SeqCst);

    unsafe {
        // Install the hook
        let hmod = GetModuleHandleW(std::ptr::null());
        let hook = SetWindowsHookExW(
            WH_GETMESSAGE,
            Some(get_message_hook),
            hmod,
            GetCurrentThreadId(),
        );

        if !hook.is_null() {
            HOOK.store(hook as isize, Ordering::SeqCst);
            true
        } else {
            false
        }
    }
}
