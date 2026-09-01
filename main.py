import tkinter as tk
from tkinter import messagebox
import ctypes
import json
import os
from ctypes import wintypes

# =====================================
# 설정
# =====================================

WINDOW_WIDTH = 380
WINDOW_HEIGHT = 300

COLORS = {
    "노랑": ("#FFF9C4", "#F7E98E"),
    "파랑": ("#DDEEFF", "#B9D7F5"),
    "초록": ("#E0F2D9", "#B9DFA8"),
    "분홍": ("#FFE1EA", "#F5B8C8"),
    "보라": ("#E9DDF8", "#CDB5E8"),
}

DEFAULT_COLOR = "노랑"

DATA_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "memo_data.json"
)

# =====================================
# 저장 데이터
# =====================================

x = 50
y = 50
saved_text = ""
saved_color = DEFAULT_COLOR
saved_alpha = 1.0

if os.path.exists(DATA_FILE):
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        x = data.get("x", 50)
        y = data.get("y", 50)
        saved_text = data.get("text", "")
        saved_color = data.get("color", DEFAULT_COLOR)
        saved_alpha = data.get("alpha", 1.0)

    except (json.JSONDecodeError, OSError):
        pass

if saved_color not in COLORS:
    saved_color = DEFAULT_COLOR

try:
    saved_alpha = float(saved_alpha)
except (ValueError, TypeError):
    saved_alpha = 1.0


# =====================================
# Windows API
# =====================================

user32 = ctypes.windll.user32

PROGMAN = user32.FindWindowW("Progman", None)

user32.SendMessageTimeoutW(
    PROGMAN,
    0x052C,
    0,
    0,
    0,
    1000,
    None
)

workerw = None


def enum_windows(hwnd, lParam):
    global workerw

    shell_view = user32.FindWindowExW(
        hwnd,
        0,
        "SHELLDLL_DefView",
        None
    )

    if shell_view:
        workerw = user32.FindWindowExW(
            0,
            hwnd,
            "WorkerW",
            None
        )

    return True


EnumWindowsProc = ctypes.WINFUNCTYPE(
    ctypes.c_bool,
    wintypes.HWND,
    wintypes.LPARAM
)

user32.EnumWindows(
    EnumWindowsProc(enum_windows),
    0
)


# =====================================
# 메인 창
# =====================================

root = tk.Tk()

root.title("Desktop Memo")

root.geometry(
    f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x}+{y}"
)

root.overrideredirect(True)

bg_color, title_color = COLORS[saved_color]

root.configure(bg=bg_color)

root.attributes("-alpha", saved_alpha)


# =====================================
# 제목 영역
# =====================================

title_bar = tk.Frame(
    root,
    bg=title_color,
    height=42
)

title_bar.pack(fill="x")

title_bar.pack_propagate(False)


title = tk.Label(
    title_bar,
    text="📝  Desktop Memo",
    bg=title_color,
    fg="#333333",
    font=("맑은 고딕", 11, "bold")
)

title.pack(
    side="left",
    padx=14
)


# =====================================
# 닫기 버튼
# =====================================

def on_close():
    save_data()
    root.destroy()


close_button = tk.Button(
    title_bar,
    text="×",
    command=on_close,
    bg=title_color,
    fg="#E57373",
    activebackground=title_color,
    activeforeground="#C62828",
    relief="flat",
    bd=0,
    font=("맑은 고딕", 16, "bold"),
    cursor="hand2"
)

close_button.pack(
    side="right",
    padx=8
)


# =====================================
# 메모 영역
# =====================================

text_frame = tk.Frame(
    root,
    bg=bg_color
)

text_frame.pack(
    fill="both",
    expand=True,
    padx=12,
    pady=(8, 12)
)


text = tk.Text(
    text_frame,
    font=("맑은 고딕", 12),
    fg="#333333",
    bg=bg_color,
    insertbackground="#333333",
    selectbackground="#D0D0D0",
    bd=0,
    highlightthickness=0,
    wrap="word",
    padx=4,
    pady=4
)

text.pack(
    fill="both",
    expand=True
)

text.insert(
    "1.0",
    saved_text
)


# =====================================
# 드래그
# =====================================

drag_x = 0
drag_y = 0


def start_drag(event):
    global drag_x, drag_y

    drag_x = event.x
    drag_y = event.y


def drag_window(event):
    new_x = root.winfo_x() + event.x - drag_x
    new_y = root.winfo_y() + event.y - drag_y

    root.geometry(
        f"+{new_x}+{new_y}"
    )


title_bar.bind(
    "<Button-1>",
    start_drag
)

title_bar.bind(
    "<B1-Motion>",
    drag_window
)

title.bind(
    "<Button-1>",
    start_drag
)

title.bind(
    "<B1-Motion>",
    drag_window
)


# =====================================
# 저장
# =====================================

def save_data():
    data = {
        "x": root.winfo_x(),
        "y": root.winfo_y(),
        "text": text.get("1.0", "end-1c"),
        "color": saved_color,
        "alpha": root.attributes("-alpha")
    }

    try:
        with open(
            DATA_FILE,
            "w",
            encoding="utf-8"
        ) as f:
            json.dump(
                data,
                f,
                ensure_ascii=False,
                indent=4
            )

    except OSError:
        pass


# =====================================
# 색상 변경
# =====================================

def change_color(color_name):
    global saved_color

    saved_color = color_name

    bg, title_bg = COLORS[color_name]

    root.configure(bg=bg)

    title_bar.configure(
        bg=title_bg
    )

    title.configure(
        bg=title_bg
    )

    close_button.configure(
        bg=title_bg,
        activebackground=title_bg
    )

    text_frame.configure(
        bg=bg
    )

    text.configure(
        bg=bg
    )

    save_data()


# =====================================
# 투명도
# =====================================

def set_alpha(value):
    alpha = float(value)

    root.attributes(
        "-alpha",
        alpha
    )

    save_data()


# =====================================
# 메모 삭제
# =====================================

def clear_memo():
    answer = messagebox.askyesno(
        "메모 삭제",
        "메모 내용을 전부 삭제할까요?"
    )

    if answer:
        text.delete(
            "1.0",
            "end"
        )

        save_data()


# =====================================
# 우클릭 메뉴
# =====================================

menu = tk.Menu(
    root,
    tearoff=0
)

menu.add_command(
    label="🗑️ 메모 내용 삭제",
    command=clear_memo
)

menu.add_separator()

color_menu = tk.Menu(
    menu,
    tearoff=0
)

for color_name in COLORS:
    color_menu.add_command(
        label=color_name,
        command=lambda c=color_name: change_color(c)
    )

menu.add_cascade(
    label="🎨 색상",
    menu=color_menu
)

alpha_menu = tk.Menu(
    menu,
    tearoff=0
)

alpha_values = {
    "100%": 1.0,
    "90%": 0.9,
    "80%": 0.8,
    "70%": 0.7,
    "60%": 0.6
}

for label, value in alpha_values.items():
    alpha_menu.add_command(
        label=label,
        command=lambda v=value: set_alpha(v)
    )

menu.add_cascade(
    label="👻 투명도",
    menu=alpha_menu
)


def show_menu(event):
    try:
        menu.tk_popup(
            event.x_root,
            event.y_root
        )
    finally:
        menu.grab_release()


root.bind(
    "<Button-3>",
    show_menu
)


# =====================================
# 바탕화면에 붙이기
# =====================================

if workerw:

    root.update_idletasks()

    hwnd = root.winfo_id()

    user32.SetParent(
        hwnd,
        workerw
    )


# =====================================
# Alt + Tab 숨기기
# =====================================

root.update_idletasks()

hwnd = root.winfo_id()

GWL_EXSTYLE = -20

WS_EX_TOOLWINDOW = 0x00000080
WS_EX_APPWINDOW = 0x00040000

if ctypes.sizeof(ctypes.c_void_p) == 8:
    GetWindowLong = user32.GetWindowLongPtrW
    SetWindowLong = user32.SetWindowLongPtrW
else:
    GetWindowLong = user32.GetWindowLongW
    SetWindowLong = user32.SetWindowLongW

GetWindowLong.restype = ctypes.c_longlong
SetWindowLong.restype = ctypes.c_longlong

style = GetWindowLong(
    hwnd,
    GWL_EXSTYLE
)

style |= WS_EX_TOOLWINDOW
style &= ~WS_EX_APPWINDOW

SetWindowLong(
    hwnd,
    GWL_EXSTYLE,
    style
)


# =====================================
# 실행
# =====================================

root.mainloop()