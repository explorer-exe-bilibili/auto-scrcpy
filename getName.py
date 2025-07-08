import bluetooth

try:
    # 执行蓝牙设备扫描
    devices = bluetooth.discover_devices(duration=8, lookup_names=True)

    # 打印扫描结果
    print("发现的蓝牙设备:")
    for addr, name in devices:
        try:
            print(f"地址: {addr}, 名称: {name}")
        except UnicodeEncodeError:
            print(f"地址: {addr}, 名称: (名称无法显示)")
except Exception as e:
    print(f"扫描过程中发生错误: {e}")