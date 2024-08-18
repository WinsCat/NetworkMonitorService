# Copyright (C) 2023 iSeeNEw Studio, Inc. All Rights Reserved
#
# @Time    : 18/8/24 PM9:27
# @Author  : Wins
# @Email   : cn.lazycat@gmail.com
# @File    : NetworkMonitorService.py
# @Software: PyCharm

import os
import sys
import time
import socket
import subprocess
import win32serviceutil
import win32service
import win32event
import servicemanager
import re


class NetworkMonitorService(win32serviceutil.ServiceFramework):
    _svc_name_ = "NetworkMonitorService"
    _svc_display_name_ = "Network Monitor Service"
    _svc_description_ = "融汇图灵小组开发的网关热备服务，根据网络情况自动获取、切换本机网络参数"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.running = True

        # Configuration
        self.target = "8.8.8.8"
        self.default_gateway = "192.168.1.1"
        self.backup_gateway = "192.168.1.2"
        self.interval = 60  # seconds
        self.adapter_name = self.get_adapter_name()

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        self.running = False
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        servicemanager.LogMsg(
            servicemanager.EVENTLOG_INFORMATION_TYPE,
            servicemanager.PYS_SERVICE_STARTED,
            (self._svc_name_, "")
        )
        self.main()

    def main(self):
        while self.running:
            if self.ping_target(self.target):
                self.set_gateway(self.default_gateway)
            else:
                self.set_gateway(self.backup_gateway)
            time.sleep(self.interval)

    def ping_target(self, target):
        try:
            socket.setdefaulttimeout(2)
            host = socket.gethostbyname(target)
            s = socket.create_connection((host, 80), 2)
            s.close()
            return True
        except Exception as e:
            return False

    def set_gateway(self, gateway):
        if self.is_dhcp_enabled(self.adapter_name):
            self.release_renew_dhcp(self.adapter_name)
        else:
            subprocess.call(
                f'netsh interface ip set address name="{self.adapter_name}" gateway={gateway}',
                shell=True)

    def get_adapter_name(self):
        # 自动检测活动的网络适配器名称
        result = subprocess.run(
            'netsh interface show interface',
            shell=True,
            capture_output=True,
            text=True)
        for line in result.stdout.splitlines():
            if "Connected" in line:
                return line.split()[-1]  # 返回连接状态的适配器名称
        return None

    # DHCP判断
    def is_dhcp_enabled(self, adapter_name):
        result = subprocess.run(
            f'netsh interface ip show config name="{adapter_name}"',
            shell=True,
            capture_output=True,
            text=True)
        return "DHCP enabled: Yes" in result.stdout

        # 获取新网络信息    def release_renew_dhcp(self, adapter_name):
        # 释放并更新DHCP
        subprocess.call(f'ipconfig /release "{adapter_name}"', shell=True)
        time.sleep(5)  # 等待一段时间以确保释放
        subprocess.call(f'ipconfig /renew "{adapter_name}"', shell=True)
        time.sleep(5)  # 等待一段时间以确保续订
        servicemanager.LogInfoMsg(
            f"DHCP settings refreshed for adapter {adapter_name}")


if __name__ == '__main__':
    import servicemanager

    if len(sys.argv) == 1:
        try:
            evtsrc_dll = os.path.abspath(servicemanager.__file__)
            # 如果修改过名字，名字要统一
            servicemanager.PrepareToHostSingle(NetworkMonitorService)
            # 如果修改过名字，名字要统一
            servicemanager.Initialize('NetworkMonitorService', evtsrc_dll)
            servicemanager.StartServiceCtrlDispatcher()
        except win32service.error as details:
            import winerror

            if details == winerror.ERROR_FAILED_SERVICE_CONTROLLER_CONNECT:
                win32serviceutil.usage()
    else:
        # 如果修改过名字，名字要统一
        win32serviceutil.HandleCommandLine(NetworkMonitorService)
