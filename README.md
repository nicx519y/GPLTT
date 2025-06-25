# GPLTT 树莓派Pico开发环境使用说明

## 🎯 环境配置完成状态

✅ **Arduino CLI 已安装** - 位于 `.\tools\arduino-cli.exe`  
✅ **Cursor IDE 任务配置完成** - `.vscode\tasks.json` 已配置  
✅ **项目结构已创建** - 包含所有必要的配置文件

## 🚀 开始使用

### 在 Cursor IDE 中编译

1. **打开任务面板**：
   - 按 `Ctrl + Shift + P`
   - 输入 `Tasks: Run Task`
   - 回车

2. **选择编译任务**：
   - 🔨 **编译 Pico 固件** - 编译当前项目
   - 📤 **上传到 Pico** - 上传固件到Pico
   - 🔗 **编译并上传** - 一键编译并上传
   - 📋 **列出可用串口** - 查看可用的串口
   - 📺 **串口监视器** - 打开串口监视器

3. **首次编译说明**：
   - 第一次编译会自动下载 Pico 核心包
   - 可能需要等待几分钟
   - 如果网络不好，可能会失败，重试即可

### 手动命令行操作

如果喜欢使用命令行，可以直接运行：

```powershell
# 编译固件
.\tools\arduino-cli.exe compile --fqbn rp2040:rp2040:rpipico GPLTT_fw.ino

# 查看可用串口
.\tools\arduino-cli.exe board list

# 上传固件 (替换COM3为实际串口)
.\tools\arduino-cli.exe upload --fqbn rp2040:rp2040:rpipico --port COM3 GPLTT_fw.ino

# 串口监视
.\tools\arduino-cli.exe monitor --port COM3 --config baudrate=115200
```

## 🔌 Pico 连接步骤

### 上传固件时：
1. **按住** Pico 上的 `BOOTSEL` 按钮
2. **插入** USB 线连接到电脑
3. **松开** `BOOTSEL` 按钮
4. Pico 会显示为 USB 存储设备
5. 在 Cursor 中运行上传任务

### 正常运行时：
- 直接插入 USB 即可
- 固件会自动开始运行
- 可以通过串口监视器查看输出

## 🏗️ 硬件连接

```
树莓派 Pico 引脚分配：
├── GPIO5  - 触发检测输入 (INPUT_PULLUP)
├── GPIO25 - 内置LED指示灯 (LED_BUILTIN)  
└── USB    - 串口通信 (115200 波特率)
```

## 🛠️ 故障排除

### 编译失败
- **现象**：提示找不到 rp2040 平台
- **解决**：首次编译会自动下载，耐心等待

### 上传失败
- **检查** Pico 是否进入 BOOTSEL 模式
- **确认** USB 连接正常
- **查看** 设备管理器中的串口号

### 串口连接问题
- 运行 `📋 列出可用串口` 任务查看可用端口
- 确保没有其他程序占用串口
- 尝试不同的 USB 端口

## 📁 项目文件说明

```
gpltt-v1.01/
├── GPLTT_fw.ino              # Arduino 固件源码 ⭐
├── GPLTT.py                  # Python GUI 应用
├── tools/                    # 本地工具目录
│   └── arduino-cli.exe       # Arduino CLI 工具
├── .vscode/                  # Cursor 配置
│   ├── tasks.json           # 编译任务配置
│   ├── c_cpp_properties.json # C++ 智能提示
│   └── settings.json        # 工作区设置
└── build/                   # 编译输出 (自动生成)
```

## 💡 开发技巧

1. **代码补全**：`.ino` 文件会被识别为 C++，支持智能提示
2. **快速编译**：`Ctrl + Shift + B` 快速运行默认编译任务
3. **串口调试**：使用 `Serial.println()` 输出调试信息
4. **LED 指示**：内置 LED 可用于状态指示

## 🎉 完成！

现在您可以开始在 Cursor IDE 中开发 GPLTT 项目了！

**下一步**：
- 在 Cursor 中打开 `GPLTT_fw.ino` 开始编写代码
- 使用 `Ctrl + Shift + P` → `Tasks: Run Task` 编译测试
- 连接 Pico 硬件进行实际测试 

## 项目简介
GPLTT (Game Pad Latency Test Tool) 是一个游戏手柄延迟测试工具，包含：
- **Python GUI应用** (`GPLTT.py`) - 提供测试界面
- **Arduino固件** (`gpltt-v1.01.ino`) - 运行在树莓派Pico上的固件

## 快速开始

### 1. 编译固件
```bash
# 方法1：使用快捷键
Ctrl + Shift + B

# 方法2：使用任务面板
Ctrl + Shift + P → Tasks: Run Task → 🔨 编译Pico固件
```

### 2. 上传固件到Pico
1. 按住Pico上的BOOTSEL按钮
2. 连接USB线到电脑
3. 松开BOOTSEL按钮（Pico会显示为USB存储设备）
4. 在Cursor中运行：
   ```bash
   Ctrl + Shift + P → Tasks: Run Task → 📤 上传到Pico
   ```

## 网络问题解决方案

如果遇到"dial tcp"或"connectex"网络连接错误，说明无法下载rp2040核心包。请使用以下解决方案：

### 方案A：手动下载（推荐）

1. **下载预编译的核心包**：
   - 访问：https://github.com/earlephilhower/arduino-pico/releases
   - 下载最新版本的压缩包

2. **手动安装**：
   ```bash
   # 创建核心包目录
   mkdir -p .\.arduino15\packages\rp2040\hardware\rp2040
   
   # 解压下载的文件到上述目录
   ```

### 方案B：使用预配置的离线环境

如果网络问题持续，可以：

1. 使用传统的Arduino IDE进行初次设置
2. 下载完成后，复制配置到本项目
3. 或者使用我提供的离线工具包

### 方案C：修改网络设置

1. **使用代理**：
   ```bash
   # 在PowerShell中设置代理（如果有）
   $env:HTTP_PROXY="http://proxy:port"
   $env:HTTPS_PROXY="http://proxy:port"
   ```

2. **修改hosts文件**（管理员权限）：
   ```
   # 添加到 C:\Windows\System32\drivers\etc\hosts
   140.82.112.3 github.com
   185.199.108.153 github.com
   ```

## 可用任务

在Cursor中按 `Ctrl + Shift + P`，然后输入 "Tasks: Run Task" 可以看到以下任务：

- 🔨 **编译Pico固件** - 编译Arduino代码
- 📤 **上传到Pico** - 上传固件到设备
- 🔗 **编译并上传** - 一键完成编译和上传
- 📋 **列出可用串口** - 查看连接的设备
- 📺 **串口监视器** - 查看设备调试输出
- 🧹 **清理构建文件** - 清理编译产生的临时文件
- ⚙️ **安装Pico核心包** - 更新索引
- 📦 **安装Pico平台** - 安装rp2040支持

## 硬件连接

### GPIO分配
- **GPIO5**: 触发信号检测输入
- **GPIO25**: LED指示灯输出（Pico内置LED）
- **USB**: 串口通信 (115200波特率)

### 连接方式
1. **上传模式**: 按住BOOTSEL + 连接USB
2. **运行模式**: 直接USB连接

## 手动命令行操作

如果任务面板不工作，可以使用以下命令：

```bash
# 编译
.\tools\arduino-cli.exe --config-file arduino-cli.yaml compile --fqbn rp2040:rp2040:rpipico --output-dir ./build --verbose .

# 列出串口
.\tools\arduino-cli.exe --config-file arduino-cli.yaml board list

# 上传（替换COM3为实际端口）
.\tools\arduino-cli.exe --config-file arduino-cli.yaml upload --fqbn rp2040:rp2040:rpipico --port COM3 --input-dir ./build .

# 串口监视器
.\tools\arduino-cli.exe --config-file arduino-cli.yaml monitor --port COM3 --config baudrate=115200
```

## 故障排除

### 1. 找不到主文件错误
确保Arduino文件名为 `gpltt-v1.01.ino`（与项目目录同名）

### 2. 平台未安装错误
运行任务：📦 **安装Pico平台**

### 3. 串口连接问题
- 检查USB线连接
- 确认驱动程序已安装
- 使用任务：📋 **列出可用串口** 查看设备

### 4. 编译错误
- 运行任务：🧹 **清理构建文件**
- 重新编译

### 5. 网络连接问题
- 参考上方的"网络问题解决方案"
- 考虑使用离线安装方式

## 开发提示

- 使用 `Ctrl + Shift + B` 快速编译
- 代码自动补全已配置好
- 错误会在问题面板中显示
- 支持调试和语法高亮

## Python GUI使用

编译上传固件后，运行Python应用：
```bash
python GPLTT.py
```

应用支持测试：
- 游戏手柄按键延迟
- 摇杆响应时间
- 键盘按键延迟
- 鼠标点击延迟 