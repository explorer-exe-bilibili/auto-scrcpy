import time
import subprocess
import sys
import random
import bluetooth  # 主要使用 PyBluez 进行设备检测

# ===== 配置区域 =====
TARGET_DEVICE_NAME = "vivo S9"  # 设备名称（可选）
TARGET_DEVICE_ADDR = "14:DD:9C:38:A7:E2"  # 蓝牙地址（带冒号格式）
SCREEN_MIRROR_CMD = r"scrcpy --tcpip=192.168.0.100"  # 替换为您的手机实际IP
CLOSE_MIRROR_CMD = "taskkill /im scrcpy.exe /f" 
POLL_INTERVAL = 5     # 检测间隔(秒)
DETECTION_TIMEOUT = 30  # 设备消失后等待多少秒关闭投屏
# ===================

def is_device_in_range():
    """检查目标设备是否在蓝牙范围内"""
    try:
        # 扫描附近所有蓝牙设备
        nearby_devices = bluetooth.discover_devices(duration=3, lookup_names=True, flush_cache=True)
        
        # 打印扫描到的设备列表（调试用）
        print(f"扫描到 {len(nearby_devices)} 个设备:")
        for addr, name in nearby_devices:
            print(f"  - {addr} ({name if name else '未知设备'})")
            
            # 检查是否为目标设备
            if addr == TARGET_DEVICE_ADDR or (TARGET_DEVICE_NAME and name == TARGET_DEVICE_NAME):
                return True
        
        return False
    except Exception as e:
        print(f"蓝牙扫描错误: {str(e)}")
        return False

def start_screen_mirroring():
    """启动投屏"""
    print(">>> 启动手机投屏")
    try:
        # 先尝试连接ADB
        subprocess.run("adb connect 192.168.0.100:5555", shell=True, check=False)
        
        # 启动scrcpy
        subprocess.Popen(SCREEN_MIRROR_CMD, shell=True)
        return True
    except Exception as e:
        print(f"启动投屏失败: {str(e)}")
        return False

def stop_screen_mirroring():
    """停止投屏"""
    print("<<< 停止手机投屏")
    try:
        # 关闭scrcpy
        subprocess.run(CLOSE_MIRROR_CMD, shell=True, check=False)
        
        # 断开ADB连接
        subprocess.run("adb disconnect", shell=True, check=False)
        return True
    except Exception as e:
        print(f"停止投屏失败: {str(e)}")
        return False

def check_bluetooth_adapter():
    """检查系统是否有可用的蓝牙适配器"""
    try:
        # 尝试获取本地蓝牙地址
        addr = bluetooth.read_local_bdaddr()
        if addr:
            print(f"找到蓝牙适配器: {addr}")
            return True
        return False
    except:
        return False

def main():
    # 检查蓝牙适配器
    if not check_bluetooth_adapter():
        print("错误: 未找到可用的蓝牙适配器")
        print("请确保:")
        print("1. 您的电脑有蓝牙功能")
        print("2. 蓝牙已启用")
        print("3. 蓝牙驱动程序已正确安装")
        input("按Enter键退出...")
        return
    
    mirroring_active = False
    last_detected = 0  # 上次检测到设备的时间戳
    detection_count = 0  # 连续检测到设备的次数
    
    print(f"开始检测设备: {TARGET_DEVICE_ADDR} ({TARGET_DEVICE_NAME})")
    
    while True:
        try:
            # 检测设备
            device_detected = is_device_in_range()
            
            if device_detected:
                last_detected = time.time()
                detection_count += 1
                
                # 首次检测到设备或重新连接
                if not mirroring_active:
                    print(f"设备在范围内 (检测次数: {detection_count})")
                    
                    # 需要连续检测到2次才启动投屏，避免误触发
                    if detection_count >= 2:
                        if start_screen_mirroring():
                            mirroring_active = True
                else:
                    print(f"设备仍在范围内 (检测次数: {detection_count})")
            else:
                detection_count = 0  # 重置检测计数
                print("未检测到设备")
                
                # 检查是否超时未检测到
                if mirroring_active and (time.time() - last_detected) > DETECTION_TIMEOUT:
                    if stop_screen_mirroring():
                        mirroring_active = False
                        print("设备离开，停止投屏")
            
            time.sleep(POLL_INTERVAL)
            
        except KeyboardInterrupt:
            print("\n程序终止")
            if mirroring_active:
                stop_screen_mirroring()
            sys.exit(0)
        except Exception as e:
            print(f"发生错误: {str(e)}")
            time.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    # 安装提示
    print("="*50)
    print("蓝牙自动投屏系统 v1.0")
    print("="*50)
    print("使用前请确保:")
    print("1. 电脑蓝牙已开启并正常工作")
    print("2. 手机蓝牙已开启")
    print("3. 手机已与电脑配对")
    print("4. 已设置好ADB无线调试")
    print("="*50)
    
    main()