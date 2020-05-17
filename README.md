# Trusted-Boot-Emulation

模拟器的功能如下<br>
1 设备厂商进入 vendor 目录，可以编辑配置 uboot，并执行 python3 rsa-sig.py 生成相关文件<br>
把 vendor/uboot_signature 下的文件复制到 Flash/uboot/下面，模拟刷写固件的操作<br>
2 通过 CPU/cpu.config 来配置是否使能可信启动<br>
3 通过 python3 power.py On 来启动设备<br>
如果使能可信启动，在启动设备时，cpu 会按照**可信启动流程**执行，如果校验失败，则停止启动<br>
如果成功，则加载 uboot 执行
