import tkinter as tk
from tkinter import ttk
import threading
import time
import serial
import serial.tools.list_ports
import pygame
import keyboard
import mouse
import random
import msvcrt
import ctypes

# 创建主窗口
root = tk.Tk()
root.title("GPLTT")
root.geometry("640x720")

# 创建父 Notebook
parent_notebook = ttk.Notebook(root)
parent_notebook.pack(fill='both', expand=True)

# 创建父 Notebook 的第一个选项卡
parent_tab1 = ttk.Frame(parent_notebook)
parent_notebook.add(parent_tab1, text="Tab 1")

# 创建父 Notebook 的第二个选项卡
parent_tab2 = ttk.Frame(parent_notebook)
parent_notebook.add(parent_tab2, text="Tab 2")

# 在父 Tab 1 中创建一个左对齐的布局框架
row0_fr = tk.Frame(parent_tab1)
row0_fr.grid(row=0, column=0, columnspan=2, sticky="nsew")
device_type = tk.IntVar()
ttk.Label(row0_fr, text="输入设备类型：").pack(side="left")
for i, device in enumerate(["手柄按键", "手柄摇杆/扳机", "键盘", "鼠标右键", "鼠标移动"]):
    ttk.Radiobutton(row0_fr, text=device, variable=device_type, value=i).pack(side="left", padx=5)
device_type.set(0)

row1_fr = tk.Frame(parent_tab1)
row1_fr.grid(row=1, column=0, columnspan=2, sticky="nsew")
ttk.Label(row1_fr, text="每次操作时间不超过").pack(side="left")
interval_var = tk.IntVar()
for i, interval in enumerate(["200ms", "500ms", "1500ms"]):
    ttk.Radiobutton(row1_fr, text=interval, variable=interval_var, value=i).pack(side="left", padx=5)
interval_var.set(1)

row2_fr = tk.Frame(parent_tab1)
row2_fr.grid(row=2, column=0, columnspan=2, sticky="nsew")

keyboard_option_frame = ttk.Frame(row2_fr)
ttk.Label(keyboard_option_frame, text="键盘操作：").pack(side="left")
key_var = tk.IntVar()
for i, key in enumerate(["w键", "a键", "s键", "d键"]):
    ttk.Radiobutton(keyboard_option_frame, text=key, variable=key_var, value=i).pack(side="left", padx=5)
key_var.set(1)

axis_fr = ttk.Frame(row2_fr)
axis_fr.grid(row=0, column=2, sticky="nsew")  # 确保 axis_fr 被正确放置

axis_option_row1 = ttk.Frame(axis_fr)
axis_option_row1.grid(row=0, column=0, sticky="nsew")

axis_option_row2 = ttk.Frame(axis_fr)
axis_option_row2.grid(row=1, column=0, sticky="nsew")

axis_num_var = tk.IntVar()
ttk.Label(axis_option_row1, text="轴编号:").pack(side="left")
for i, axis in enumerate(["左摇杆x轴", "左摇杆y轴", "右摇杆x轴", "右摇杆y轴", "左扳机", "右扳机"]):
    ttk.Radiobutton(axis_option_row1, text=axis, variable=axis_num_var, value=i).pack(side="left", padx=5)
axis_num_var.set(2)

threshold_var = tk.DoubleVar(value=5)  # 初始化阈值为5%
ttk.Label(axis_option_row2, text="触发阈值:").pack(side="left")
tk.Scale(axis_option_row2, from_=1, to=99, orient="horizontal", variable=threshold_var, resolution=1, length=300).pack(side="left")

# 添加切换阈值的按钮
def toggle_threshold():
    current_value = threshold_var.get()
    if current_value == 5:
        threshold_var.set(95)
    else:
        threshold_var.set(5)

toggle_button = ttk.Button(axis_option_row2, text="切换5%/95%阈值", command=toggle_threshold)
toggle_button.pack(side="left", padx=5)

def update_options(*args):
    device = device_type.get()
    if device == 2:  # 当选择键盘
        keyboard_option_frame.grid(row=0, column=0, padx=5)
        axis_fr.grid_remove()
    elif device == 1:  # 当选择手柄摇杆/扳机
        axis_fr.grid(row=0, column=0, padx=5)
        keyboard_option_frame.grid_remove()
    else:
        keyboard_option_frame.grid_remove()
        axis_fr.grid_remove()

device_type.trace_add("write", update_options)

row3_fr = tk.Frame(parent_tab1)
row3_fr.grid(row=3, column=0, columnspan=2, sticky="nsew")

row4_fr = tk.Frame(parent_tab1)
row4_fr.grid(row=4, column=0, columnspan=2, sticky="nsew")
# 配置 Parent Tab 1 的 grid
parent_tab1.grid_rowconfigure(0, weight=0)
parent_tab1.grid_rowconfigure(1, weight=0)
parent_tab1.grid_rowconfigure(2, weight=0)
parent_tab1.grid_rowconfigure(3, weight=0)
parent_tab1.grid_rowconfigure(4, weight=1)

parent_tab1.grid_columnconfigure(0, weight=0)
parent_tab1.grid_columnconfigure(1, weight=1)

class StatisticApp:
    def __init__(self, parent, hide_generate_button=False):
        self.parent = parent
        self.hide_generate_button = hide_generate_button
        
        # 设置窗口标题
        if isinstance(parent, tk.Tk):
            parent.title("随机数生成器")
        
        # 数据存储
        self.numbers = []
        self.check_vars = []
        self.button_refs = []  # 存储所有生成的 Checkbutton
        
        # 初始化界面
        self.create_widgets()
    
    def create_widgets(self):
        # 顶部按钮
        button_frame = ttk.Frame(self.parent)
        button_frame.pack(pady=10)
        
        if not self.hide_generate_button:
            self.generate_button = ttk.Button(button_frame, text="生成随机数", command=self.generate_number)
            self.generate_button.pack(side="left", padx=5)
        
        self.clear_button = ttk.Button(button_frame, text="清空", command=self.clear_data)
        self.clear_button.pack(side="left", padx=5)
        
        # Checkbutton 容器
        self.check_frame = ttk.Frame(self.parent)
        self.check_frame.pack(pady=10, fill="x")
        
        # 统计数据标签
        self.stats_label = ttk.Label(self.parent, text="统计数据：\n最大值: N/A\n最小值: N/A\n平均值: N/A")
        self.stats_label.pack(pady=10)
    
    def generate_number(self):
        # 生成随机小数 (0到100之间，保留2位小数)
        random_number = round(random.uniform(0, 100), 2)
        self._add_number(random_number)
        print(f"生成的随机数为：{random_number}")
        
    def generate_specific_number(self, number):
        # 检查传入的参数是否为数字
        try:
            number = float(number)
        except ValueError:
            print("传入的参数必须是一个数字")
            return
        
        # 确保数字保留两位小数
        number = round(number, 2)
        self._add_number(number)
    
    def _add_number(self, number):
        """内部方法：添加数字并创建对应的Checkbutton"""
        self.numbers.append(number)
        
        # 创建 Checkbutton
        var = tk.BooleanVar(value=True)
        self.check_vars.append(var)
        
        # 格式化数字为两位小数
        formatted_number = "{:.2f}".format(number)
        check = ttk.Checkbutton(self.check_frame, text=formatted_number, variable=var, command=self.update_stats)
        self.button_refs.append(check)
        check.grid(row=0, column=0, padx=5, pady=5)  # 初始布局（稍后在 on_resize 中重新计算）
        
        # 更新布局和统计
        self.update_layout()
        self.update_stats()
    
    def clear_data(self):
        # 清空数据
        self.numbers.clear()
        self.check_vars.clear()
        self.button_refs.clear()
        
        # 清空 Checkbutton
        for widget in self.check_frame.winfo_children():
            widget.destroy()
        
        # 重置统计数据
        self.stats_label.config(text="统计数据：\n最大值: N/A\n最小值: N/A\n平均值: N/A")
    
    def update_stats(self):
        # 统计被勾选的数字
        selected_numbers = [num for num, var in zip(self.numbers, self.check_vars) if var.get()]
        
        if selected_numbers:
            max_val = max(selected_numbers)
            min_val = min(selected_numbers)
            avg_val = sum(selected_numbers) / len(selected_numbers)
            
            # 格式化统计值为两位小数
            max_val = "{:.2f}".format(max_val)
            min_val = "{:.2f}".format(min_val)
            avg_val = "{:.2f}".format(avg_val)
        else:
            max_val = min_val = avg_val = "N/A"
        
        # 更新统计数据标签
        self.stats_label.config(text=f"统计数据：\n最大值: {max_val}\n最小值: {min_val}\n平均值: {avg_val}\n测试次数: {len(selected_numbers)
            }\n单位：ms")
    
    def update_layout(self):
        # 获取窗口宽度
        frame_width = self.check_frame.winfo_width()
        
        if frame_width > 0 and self.button_refs:
            # 计算每行可容纳的 Checkbutton 数量
            button_width = 70  # 每个 Checkbutton 的宽度（增加以适应小数显示）
            col_count = max(1, frame_width // button_width)  # 至少 1 列
            
            for i, button in enumerate(self.button_refs):
                row = i // col_count
                col = i % col_count
                button.grid(row=row, column=col, padx=5, pady=5, sticky="w")

app1 = StatisticApp(row4_fr, hide_generate_button=True) 

class DeviceDetector:
    def __init__(self):
        self.running = False
        self.thread = None
        pygame.init()
        
    def detect_devices(self):
        self.running = True
        print("\n--- 开始检测设备 ---")
        
        # 检测串口
        self.serial_connection = None
        ports = list(serial.tools.list_ports.comports())
        if len(ports) == 0:
            print("没有找到可用的串口设备")
        elif len(ports) == 1:
            port = ports[0]
            print(f"找到1个串口设备: {port.device} - 自动连接")
            try:
                self.serial_connection = serial.Serial(port.device, 115200, timeout=1)
                print(f"已成功连接到 {port.device}")
            except Exception as e:
                # if not self.serial_connection:
                    print(f"连接失败: {e}")
        else:
            print("找到多个串口设备:")
            for i, port in enumerate(ports):
                print(f"{i+1}: {port.device} - {port.description}")
            selection = input("请输入要连接的串口编号，按下回车键以确认: ")
            try:
                selected = ports[int(selection)-1]
                print(f"尝试连接: {selected.device}")
                self.serial_connection = serial.Serial(selected.device, 115200, timeout=1)
                print(f"已成功连接到 {selected.device}")
            except (ValueError, IndexError):
                print("无效的选择")
            except Exception as e:
                print(f"连接失败: {e}")
        
        # 检测游戏手柄
        pygame.joystick.init()
        joystick_count = pygame.joystick.get_count()
        if joystick_count == 0:
            print("没有找到可用的游戏手柄")
        elif joystick_count == 1:
            joystick = pygame.joystick.Joystick(0)
            joystick.init()
            print(f"找到1个游戏手柄: {joystick.get_name()} - 自动连接")
        else:
            print("找到多个游戏手柄:")
            for i in range(joystick_count):
                joystick = pygame.joystick.Joystick(i)
                print(f"{i+1}: {joystick.get_name()}")
            selection = input("请输入要连接的手柄编号，按下回车键以确认: ")
            try:
                selected = pygame.joystick.Joystick(int(selection)-1)
                selected.init()
                print(f"已选择: {selected.get_name()}")
            except:
                print("无效的选择")
        
        print("--- 设备连接完成 ---\n")
        axis_num = int(axis_num_var.get())
        stick_threshold = threshold_var.get()/100
        def stick_go():
            if abs(joystick.get_axis(axis_num)) > stick_threshold:
                return True
            else:
                return False
            
        def trigger_down():
            if joystick.get_axis(axis_num) > stick_threshold*2-1:
                return True
            else:
                return False
                    
        def judge_axis():
            pass
        
        if axis_num in [0,1,2,3]:
            judge_axis = stick_go
        else:
            judge_axis = trigger_down

        def choose_get_end_time(device_type):
            def wait_gamepad_button():
                pygame.event.clear()
                while True:
                    time.sleep(0)
                    for event in pygame.event.get([pygame.JOYBUTTONDOWN, pygame.JOYHATMOTION]):
                        if event.type == pygame.JOYBUTTONDOWN or (event.type == pygame.JOYHATMOTION and event.value != (0, 0)):
                            return time.perf_counter()
            def wait_gamepad_axis():
                while True:
                    time.sleep(0)
                    pygame.event.clear()
                    if judge_axis():
                        return time.perf_counter()

            def clear_input_buffer():
                while msvcrt.kbhit():
                    msvcrt.getch()

            match key_var.get():
                case 0:
                    listened_key = 'w'
                case 1:
                    listened_key = 'a'
                case 2:
                    listened_key = 's'
                case 3:
                    listened_key = 's'
            def wait_keyboard_key():
                clear_input_buffer()
                keyboard.wait(listened_key)
                return time.perf_counter()
            def wait_mouse_click():
                mouse.wait(button='right', target_types='down')
                return time.perf_counter()
            def wait_mouse_move():
                initial_position = mouse.get_position()
                while True:
                    current_position = mouse.get_position()
                    if current_position != initial_position:
                        return
            match device_type:
                case 0:
                    return wait_gamepad_button
                case 1:
                    return wait_gamepad_axis
                case 2:
                    return wait_keyboard_key
                case 3:
                    return wait_mouse_click
                case 4:
                    return wait_mouse_move
        get_end_time = choose_get_end_time(device_type.get())

        match interval_var.get():
            case 0:
                self.serial_connection.write(b'x')
                test_interval = 200
            case 1:
                self.serial_connection.write(b'y')
                test_interval = 500
            case 2:
                self.serial_connection.write(b'z')
                test_interval = 1500

        print("开始测试...")
        timeout_seconds = 0.2
        def test():
            get_end_time() # 等待手柄/键鼠信号
            self.serial_connection.write(b'p')
            start_time = time.perf_counter()
            # print("收到设备输入")
            while not self.serial_connection.in_waiting:
                if time.perf_counter() - start_time > timeout_seconds:
                    print("误触")
                    return
            data = self.serial_connection.readline().decode('utf-8').strip()
            try:
                print(data)
                delay = int(data)/1000
                app1.generate_specific_number(delay)
            except Exception as e:
                print(f"错误: {str(e)}")
            time.sleep(test_interval/1000)
        while True:
            test()
    
    def terminate_thread(self, thread):
        if not thread.is_alive():
            return
        tid = thread.ident
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(tid), ctypes.py_object(SystemExit))
        if res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(tid), 0)
            print("Exception raise failure")
        try:
            self.serial_connection.close()
        except Exception as e:
            print(f"{e}")
            input("按任意键继续...")

    def start_detection(self):
        if self.running:
            # 如果已经在运行，则重启程序
            button.config(text="开始测试")
            self.terminate_thread(self.thread)
            self.running = False
            print("\n停止测试...")
            
        else:
            # 启动新线程进行检测
            button.config(text="停止测试")
            self.thread = threading.Thread(target=self.detect_devices, daemon=True)
            self.thread.start()


def create_detector_button(parent_frame):
    detector = DeviceDetector()
    
    button = ttk.Button(
        parent_frame,
        text="开始测试",
        command=detector.start_detection,
    )
    button.pack()

    return button

button = create_detector_button(row3_fr)

# 运行主循环
root.mainloop()