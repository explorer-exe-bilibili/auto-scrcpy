# 蓝牙接近自动投屏系统

自动检测手机靠近并投屏到电脑

## 项目简介

这个Python脚本实现了当您的安卓手机靠近Windows电脑时自动投屏手机画面到电脑的功能。系统通过蓝牙检测手机接近状态，使用Scrcpy工具实现低延迟、高质量的投屏体验。

## 功能特点

- **自动检测手机靠近**：通过蓝牙信号检测手机是否在电脑附近
- **无缝投屏体验**：自动启动/停止Scrcpy投屏
- **低延迟高性能**：基于ADB无线调试的稳定连接
- **高度可配置**：可调整检测灵敏度、投屏参数等
- **详细日志输出**：实时显示检测状态和设备信息
- **智能防误触**：需要连续检测到设备才触发投屏

## 系统要求

### 硬件要求

- Windows 10或更高版本（支持蓝牙4.0+）
- 带蓝牙功能的安卓手机（Android 5.0+）
- 电脑和手机在同一WiFi网络下

### 软件要求

- Python 3.6
- [Scrcpy](https://github.com/Genymobile/scrcpy)
- [Android Platform Tools](https://developer.android.com/tools/releases/platform-tools)
- PyBluez库

## 安装步骤

### 1. 安装Python

从[Python官网](https://www.python.org/downloads/)下载并安装最新版Python，安装时勾选"Add Python to PATH"。

### 2. 安装依赖库

打开命令提示符(CMD)或PowerShell，执行以下命令：

```bash
pip install pybluez
```

### 3. 安装Scrcpy和ADB

1. 下载[Scrcpy](https://github.com/Genymobile/scrcpy/releases)并解压到任意目录
2. 下载[Android Platform Tools](https://developer.android.com/tools/releases/platform-tools)并解压
3. 将Scrcpy和Platform Tools目录添加到系统PATH环境变量

### 4. 配置手机ADB调试

1. 在手机上启用开发者选项（设置 > 关于手机 > 多次点击"版本号"）
2. 启用USB调试（设置 > 系统 > 开发者选项）
3. 使用USB线连接手机和电脑
4. 在电脑上运行：

   ```bash
   adb tcpip 5555
   adb connect <手机IP地址>:5555
   ```

5. 断开USB线，测试无线连接：

   ```bash
   adb devices
   ```

## 配置说明

编辑脚本中的以下配置参数：

```python
# ===== 配置区域 =====
TARGET_DEVICE_NAME = "phone"  # 设备名称（可选）
TARGET_DEVICE_ADDR = "XX:XX:XX:XX:XX:XX"  # 蓝牙地址（带冒号格式）
SCREEN_MIRROR_CMD = r"scrcpy --tcpip=192.168.1.100"  # 替换为您的手机实际IP
CLOSE_MIRROR_CMD = "taskkill /im scrcpy.exe /f" 
POLL_INTERVAL = 5     # 检测间隔(秒)
DETECTION_TIMEOUT = 30  # 设备消失后等待多少秒关闭投屏
# ===================
```

### 获取手机蓝牙地址

1. 在手机上：设置 > 关于手机 > 状态信息 > 蓝牙地址
2. 在电脑上：控制面板 > 设备和打印机 > 右键手机设备 > 属性 > 蓝牙

### 设置手机固定IP

在路由器设置中，根据手机MAC地址分配固定IP（推荐192.168.1.100）

## 使用方法

### 基本使用

1. 确保电脑和手机蓝牙已开启
2. 双击运行脚本`main.py`
3. 携带手机靠近电脑，观察投屏是否自动启动
4. 携带手机离开电脑，观察投屏是否自动停止

### 开机自启动

1. 创建脚本的快捷方式
2. 按`Win+R`输入`shell:startup`打开启动文件夹
3. 将快捷方式放入此文件夹

### 命令行参数

```bash
python main.py [选项]

选项:
  --debug     启用详细调试模式
  --test      测试模式（不实际启动投屏）
  --interval  设置检测间隔（秒）
```

## 常见问题

### 找不到蓝牙适配器

- 确保电脑有蓝牙功能并已启用
- 检查设备管理器中的蓝牙驱动程序
- 尝试重启蓝牙服务：
  
  ```bash
  net stop bthserv
  net start bthserv
  ```

### 扫描不到手机设备

- 确保手机蓝牙可见性设置为"对所有设备可见"
- 检查手机是否已与电脑配对
- 尝试重新配对设备

### ADB连接失败

- 确保手机和电脑在同一WiFi网络
- 检查手机IP地址是否正确
- 重新执行ADB设置步骤：
  
  ```bash
  adb tcpip 5555
  adb connect <手机IP地址>:5555
  ```

### 投屏启动失败

- 检查Scrcpy是否安装正确
- 确保PATH环境变量包含Scrcpy和ADB路径
- 手动测试投屏命令是否有效

## 注意事项

1. **隐私安全**：投屏会显示手机屏幕内容，请注意使用环境
2. **电池优化**：在手机设置中，为ADB和蓝牙相关服务禁用电池优化
3. **管理员权限**：某些操作可能需要管理员权限运行脚本
4. **防火墙设置**：允许Python和Scrcpy通过防火墙

## 贡献与支持

欢迎提交Issue或Pull Request改进项目：

- [GitHub仓库](https://github.com/explorer-exe-bilibili/auto-scrcpy)

如需进一步支持，请联系：<j13879066396@163.com>

---

**让科技简化您的生活，享受无缝投屏体验！**  
