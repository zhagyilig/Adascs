# coding=utf-8
# auth: zhangyiling
# time: 2019/1/17 下午6:07
# description:


from pyvim.connect import SmartConnect, Disconnect
import sys
from pyVmomi import vim
import atexit


class CenterManager:
    def __init__(self, host_url, username, password, port=80, context=None):
        """
           init v_center management
        """
        self.host = host_url
        self.user = username
        self.pwd = password
        self.port = port
        self.context = context
        if port == 443 and self.context is None:
            import ssl
            if getattr(ssl, '_create_unverified_context'):
                self.context = ssl._create_unverified_context()
        try:
            self.center = SmartConnect(host=self.host, user=self.user, pwd=self.pwd,
                                       port=self.port, sslContext=self.context)
        except Exception as e:
            print("Connect Error, please check username or password s%" % e)

        atexit.register(Disconnect, self.center)
        self.content = self.center.RetrieveContent()

    def get_obj(self, content, vimtype, name=None):
        """
          return: objects list
        """
        container = content.viewManager.CreateContainerView(content.rootFolder, vimtype, True)
        objs = [view for view in container.view]
        return objs

    def get_v_hosts(self):

        content = self.center.RetrieveContent()
        for child in content.rootFolder.childEntity:
            if hasattr(child, 'vmFolder'):
                vm_folder = child.vmFolder
                vm_list = vm_folder.childEntity
                for vm in vm_list:
                    print(vm.name)


if __name__ == '__main__':

    host = 'xxx.com'
    username = 'username'
    password = 'pass'
    port = 443

    center = CenterManager(host, username, password, port)
    esxi_objs = center.get_obj(content=center.content, vimtype=[vim.HostSystem])
    esxi_host = {}

    vm_hostname = []
    for esxi in esxi_objs:
        # print(esxi.name)  # 所有的物理机的ip地址
        # all physical host ip address is the key
        # esxi_host[esxi.name] = {'esxi_info': {}, 'datastore': {}, 'network': {}, 'vm': {}}
        # esxi_host[esxi.name] = {'esxi_info': {}, 'vm': {}}
        # esxi_host[esxi.name] = {'vm': {}}

        # add info
        # esxi_host[esxi.name]['esxi_info']['厂商'] = esxi.summary.hardware.vendor
        # esxi_host[esxi.name]['esxi_info']['型号'] = esxi.summary.hardware.model

        # Serial Number
        # for i in esxi.summary.hardware.otherIdentifyingInfo:
        #     if isinstance(i, vim.host.SystemIdentificationInfo):
        #         esxi_host[esxi.name]['esxi_info']['SN'] = i.identifierValue

        # CPU info
        # esxi_host[esxi.name]['esxi_info']['处理器'] = '数量:{} 核数：{} 线程数：{} 频率：{}({})'.format(
        #     esxi.summary.hardware.numCpuPkgs,
        #     esxi.summary.hardware.numCpuCores,
        #     esxi.summary.hardware.numCpuThreads,
        #     esxi.summary.hardware.cpuMhz,
        #     esxi.summary.hardware.cpuModel
        # )

        # esxi_host[esxi.name]['esxi_info']['处理器使用率'] = '{}'.format(
        #     esxi.summary.quickStats.overallCpuUsage /
        #     (esxi.summary.hardware.numCpuPkgs * esxi.summary.hardware.numCpuCores * esxi.summary.hardware.cpuMhz) * 100)

        # Memory info
        # esxi_host[esxi.name]['esxi_info']['内存(MB)'] = str(esxi.summary.hardware.memorySize / 1024 / 1024 / 1024)
        # esxi_host[esxi.name]['esxi_info']['可用内存(MB)'] = '{}'.format(
        #     str((esxi.summary.hardware.memorySize / 1024 / 1024) -
        #         esxi.summary.quickStats.overallMemoryUsage))
        # esxi_host[esxi.name]['esxi_info']['内存使用率'] = '{}'.format(str((esxi.summary.quickStats.overallMemoryUsage / (
        #         esxi.summary.hardware.memorySize / 1024 / 1024)) * 100))

        # Add vm info

        for vm in esxi.vm:
            print(vm.name)
            vm_hostname.append(vm.name)
        #     esxi_host[esxi.name]['vm'][vm.name] = {}
        # esxi_host[esxi.name]['vm'][vm.name]['电源状态'] = vm.runtime.powerState
        # esxi_host[esxi.name]['vm'][vm.name]['CPU(内核总数)'] = vm.config.hardware.numCPU
        # esxi_host[esxi.name]['vm'][vm.name]['内存(总数MB)'] = vm.config.hardware.memoryMB
        # esxi_host[esxi.name]['vm'][vm.name]['系统信息'] = vm.config.guestFullName

        # if vm.guest.ipAddress:
        #     esxi_host[esxi.name]['vm'][vm.name]['IP'] = vm.guest.ipAddress
        # else:
        #     esxi_host[esxi.name]['vm'][vm.name]['IP'] = 'NULL'

        # for d in vm.config.hardware.device:
        #     if isinstance(d, vim.vm.device.VirtualDisk):
        #         esxi_host[esxi.name]['vm'][vm.name][d.deviceInfo.label] = str(
        #             (d.capacityInKB) / 1024 / 1024) + ' GB'

    # print(esxi_host)

    print(vm_hostname)

print(len(vm_hostname))
