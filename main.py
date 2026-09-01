import tkinter as tk
from tkinter import messagebox, simpledialog
import ctypes
import json
import os
from ctypes import wintypes

# =====================================
# 설정
# =====================================

WINDOW_WIDTH = 400
WINDOW_HEIGHT = 470

COLORS = {
    "노랑": {
        "bg": "#FFFBEA",
        "header": "#F6D96B",
        "accent": "#D9A900",
        "text": "#333333"
    },
    "파랑": {
        "bg": "#F0F7FF",
        "header": "#A9CFF5",
        "accent": "#4C8ED9",
        "text": "#333333"
    },
    "초록": {
        "bg": "#F2FAEF",
        "header": "#B9DFA8",
        "accent": "#6BA856",
        "text": "#333333"
    },
    "분홍": {
        "bg": "#FFF2F6",
        "header": "#F5B8C8",
        "accent": "#D96B8A",
        "text": "#333333"
    },
    "보라": {
        "bg": "#F7F1FC",
        "header": "#CDB5E8",
        "accent": "#936BC4",
        "text": "#333333"
    }
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
saved_tasks = []

if os.path.exists(DATA_FILE):
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        x = data.get("x", 50)
        y = data.get("y", 50)
        saved_text = data.get("text", "")
        saved_color = data.get("color", DEFAULT_COLOR)
        saved_alpha = data.get("alpha", 1.0)
        saved_tasks = data.get("tasks", [])

    except (json.JSONDecodeError, OSError):
        pass

if saved_color not in COLORS:
    saved_color = DEFAULT_COLOR

try:
    saved_alpha = float(saved_alpha)
except (ValueError, TypeError):
    saved_alpha = 1.0

if not isinstance(saved_tasks, list):
    saved_tasks = []

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



# 메인 창


root = tk.Tk()

root.title("Desktop Memo")

root.geometry(
    f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x}+{y}"
)

root.overrideredirect(True)

theme = COLORS[saved_color]

root.configure(
    bg=theme["bg"]
)

root.attributes(
    "-alpha",
    saved_alpha
)


# 저장


task_data = []


def save_data():
    tasks = []

    for task in task_data:
        tasks.append({
            "text": task["text"],
            "done": task["done"].get()
        })

    data = {
        "x": root.winfo_x(),
        "y": root.winfo_y(),
        "text": text.get("1.0", "end-1c"),
        "color": saved_color,
        "alpha": root.attributes("-alpha"),
        "tasks": tasks
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


# =====================================
# 상단바
# =====================================

header = tk.Frame(
    root,
    bg=theme["header"],
    height=50
)

header.pack(
    fill="x"
)

header.pack_propagate(False)

header.bind(
    "<Button-1>",
    start_drag
)

header.bind(
    "<B1-Motion>",
    drag_window
)


title = tk.Label(
    header,
    text="📝  Desktop Memo",
    bg=theme["header"],
    fg=theme["text"],
    font=("맑은 고딕", 11, "bold")
)

title.pack(
    side="left",
    padx=16
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
# 닫기 버튼
# =====================================

def on_close():
    save_data()
    root.destroy()


close_button = tk.Button(
    header,
    text="×",
    command=on_close,
    bg=theme["header"],
    fg="#555555",
    activebackground=theme["header"],
    activeforeground="#222222",
    relief="flat",
    bd=0,
    font=("맑은 고딕", 17),
    cursor="hand2"
)

close_button.pack(
    side="right",
    padx=10
)

# =====================================
# 메인 컨테이너
# =====================================

main = tk.Frame(
    root,
    bg=theme["bg"]
)

main.pack(
    fill="both",
    expand=True,
    padx=16,
    pady=14
)

# =====================================
# 체크리스트 제목
# =====================================

task_header = tk.Frame(
    main,
    bg=theme["bg"]
)

task_header.pack(
    fill="x"
)

task_title = tk.Label(
    task_header,
    text="☑  오늘 할 일",
    bg=theme["bg"],
    fg=theme["text"],
    font=("맑은 고딕", 11, "bold")
)

task_title.pack(
    side="left"
)

# =====================================
# 할 일 추가
# =====================================

def add_task():
    task_text = simpledialog.askstring(
        "할 일 추가",
        "할 일을 입력하세요:",
        parent=root
    )

    if task_text is None:
        return

    task_text = task_text.strip()

    if not task_text:
        return

    create_task(
        task_text,
        False
    )

    save_data()


add_button = tk.Button(
    task_header,
    text="+ 추가",
    command=add_task,
    bg=theme["header"],
    fg=theme["text"],
    activebackground=theme["header"],
    relief="flat",
    bd=0,
    padx=10,
    pady=3,
    font=("맑은 고딕", 9, "bold"),
    cursor="hand2"
)

add_button.pack(
    side="right"
)

# =====================================
# 체크리스트 영역
# =====================================

task_list = tk.Frame(
    main,
    bg=theme["bg"]
)

task_list.pack(
    fill="x",
    pady=(7, 12)
)


def delete_task(task):
    if task in task_data:
        task["frame"].destroy()
        task_data.remove(task)
        save_data()


def create_task(task_text, done=False):
    frame = tk.Frame(
        task_list,
        bg=theme["bg"]
    )

    frame.pack(
        fill="x",
        pady=2
    )

    done_var = tk.BooleanVar(
        value=done
    )

    check = tk.Checkbutton(
        frame,
        text=task_text,
        variable=done_var,
        command=save_data,
        bg=theme["bg"],
        activebackground=theme["bg"],
        selectcolor=theme["bg"],
        fg=theme["text"],
        font=("맑은 고딕", 10),
        anchor="w"
    )

    check.pack(
        side="left",
        fill="x",
        expand=True
    )

    delete = tk.Button(
        frame,
        text="×",
        command=lambda: delete_task(task),
        bg=theme["bg"],
        fg="#AAAAAA",
        activebackground=theme["bg"],
        activeforeground="#777777",
        relief="flat",
        bd=0,
        font=("맑은 고딕", 11),
        cursor="hand2"
    )

    delete.pack(
        side="right"
    )

    task = {
        "text": task_text,
        "done": done_var,
        "frame": frame
    }

    task_data.append(task)


for task in saved_tasks:
    if isinstance(task, dict):

        task_text = task.get(
            "text",
            ""
        )

        task_done = task.get(
            "done",
            False
        )

        if task_text:
            create_task(
                task_text,
                bool(task_done)
            )

# =====================================
# 메모 제목
# =====================================

memo_title = tk.Label(
    main,
    text="📝  메모",
    bg=theme["bg"],
    fg=theme["text"],
    font=("맑은 고딕", 11, "bold")
)

memo_title.pack(
    anchor="w",
    pady=(2, 6)
)

# =====================================
# 메모 입력창
# =====================================

text_container = tk.Frame(
    main,
    bg=theme["header"]
)

text_container.pack(
    fill="both",
    expand=True
)

text = tk.Text(
    text_container,
    font=("맑은 고딕", 11),
    fg=theme["text"],
    bg=theme["bg"],
    insertbackground=theme["text"],
    selectbackground="#D8D8D8",
    bd=0,
    highlightthickness=0,
    wrap="word",
    padx=10,
    pady=10
)

text.pack(
    fill="both",
    expand=True,
    padx=2,
    pady=2
)

text.insert(
    "1.0",
    saved_text
)

# =====================================
# 색상 변경
# =====================================

def change_color(color_name):
    global saved_color, theme

    saved_color = color_name
    theme = COLORS[color_name]

    bg = theme["bg"]
    header_bg = theme["header"]
    fg = theme["text"]

    root.configure(bg=bg)

    header.configure(bg=header_bg)
    title.configure(
        bg=header_bg,
        fg=fg
    )

    close_button.configure(
        bg=header_bg,
        activebackground=header_bg
    )

    main.configure(bg=bg)

    task_header.configure(bg=bg)
    task_title.configure(
        bg=bg,
        fg=fg
    )

    add_button.configure(
        bg=header_bg,
        activebackground=header_bg
    )

    task_list.configure(bg=bg)

    memo_title.configure(
        bg=bg,
        fg=fg
    )

    text_container.configure(
        bg=header_bg
    )

    text.configure(
        bg=bg,
        fg=fg,
        insertbackground=fg
    )

    for task in task_data:

        task["frame"].configure(
            bg=bg
        )

        for widget in task["frame"].winfo_children():

            if isinstance(
                widget,
                tk.Checkbutton
            ):
                widget.configure(
                    bg=bg,
                    activebackground=bg,
                    selectcolor=bg,
                    fg=fg
                )

            elif isinstance(
                widget,
                tk.Button
            ):
                widget.configure(
                    bg=bg,
                    activebackground=bg
                )

    save_data()


# 투명도


def set_alpha(value):

    root.attributes(
        "-alpha",
        float(value)
    )

    save_data()


# 메모 삭제


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

# 색상 메뉴
color_menu = tk.Menu(
    menu,
    tearoff=0
)

for color_name in COLORS:

    color_menu.add_command(
        label=color_name,
        command=lambda c=color_name:
            change_color(c)
    )

menu.add_cascade(
    label="🎨 테마",
    menu=color_menu
)

# 투명도 메뉴
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
        command=lambda v=value:
            set_alpha(v)
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

if ctypes.sizeof(
    ctypes.c_void_p
) == 8:

    GetWindowLong = (
        user32.GetWindowLongPtrW
    )

    SetWindowLong = (
        user32.SetWindowLongPtrW
    )

else:

    GetWindowLong = (
        user32.GetWindowLongW
    )

    SetWindowLong = (
        user32.SetWindowLongW
    )

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