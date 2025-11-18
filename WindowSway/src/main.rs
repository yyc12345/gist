use comfy_table::Table;
use std::io::{self, Write};
use std::str::FromStr;
use std::thread;
use std::time::Duration;

mod enum_window;
mod scroll_window;
// mod always_active;

fn accept_input<T>() -> Result<T, <T as FromStr>::Err>
where
    T: FromStr,
{
    io::stdout().flush().unwrap();
    let mut input = String::new();
    io::stdin().read_line(&mut input).unwrap();
    input.trim().parse::<T>()
}

fn press_any_key() {
    let mut input = String::new();
    io::stdin().read_line(&mut input).unwrap();
}

fn main() {
    // region: Find all windows

    println!("正在获取窗口列表...");
    let windows = enum_window::get_all_windows();

    println!("当前系统中的窗口：");
    let mut table = Table::new();
    table.load_preset(comfy_table::presets::ASCII_FULL_CONDENSED);
    table.set_header(["序号", "窗口句柄", "是否可见", "标题"]);
    for (i, info) in windows.iter().enumerate() {
        table.add_row([
            i.to_string(),
            format!("0x{:X}", (info.get_hwnd() as isize)),
            (if info.get_is_visible() { "是" } else { "否" }).to_string(),
            info.get_title().to_string(),
        ]);
    }
    println!("{table}");

    // endregion

    // region: Accept user input

    print!("请选择希望移动鼠标的窗口的序号：");
    let window_index: usize = match accept_input::<usize>() {
        Ok(index) => {
            if !((0..windows.len()).contains(&index)) {
                println!("无效的窗口序号！");
                return;
            } else {
                index
            }
        }
        Err(_) => {
            println!("请输入有效的数字！");
            return;
        }
    };

    print!("请输入X坐标: ");
    let window_x: i32 = match accept_input() {
        Ok(v) => v,
        Err(_) => {
            println!("请输入有效的数字！");
            return;
        }
    };
    print!("请输入Y坐标: ");
    let window_y: i32 = match accept_input() {
        Ok(v) => v,
        Err(_) => {
            println!("请输入有效的数字！");
            return;
        }
    };

    // endregion

    // region: Start executing

    let window_hwnd = windows[window_index].get_hwnd();
    let window_title = windows[window_index].get_title();
    println!(
        "已选择窗口0x{:X}。标题为: {}",
        window_hwnd as isize, window_title
    );
    println!(
        "期望于窗口的({}, {})坐标处发送鼠标滚动指令。",
        window_x, window_y
    );

    println!("回车以开始执行。执行过程中按下Ctrl+C随时终止执行。");
    press_any_key();

    // if always_active::prevent_window_from_losing_focus(window_hwnd) {
    //     println!("已安装钩子，窗口将不会失去焦点。");
    // } else {
    //     println!("安装钩子失败");
    //     return;
    // }

    let mut direction_down = true;
    loop {
        if direction_down {
            scroll_window::post_mouse_wheel(window_hwnd, window_x, window_y, -120); // 向下滚动
            println!("向下滚动");
        } else {
            scroll_window::post_mouse_wheel(window_hwnd, window_x, window_y, 120); // 向上滚动
            println!("向上滚动");
        }

        direction_down = !direction_down;

        thread::sleep(Duration::from_secs(5));
    }
}
