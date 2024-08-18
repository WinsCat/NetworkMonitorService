# NetworkMonitorService

**<h2>融汇图灵小组开发的网关热备服务，根据网络情况自动获取、切换本机网络参数</h2>**
**应用场景：Windows**

**<h3>脚本功能说明</h3>**

	自动检测网络适配器名称：脚本会自动检测当前连接的网络适配器名称，而不需要手动指定。
	检查DHCP状态：在更改网关之前，脚本会检查该网络适配器是否启用了DHCP。
	DHCP操作：
    如果网络适配器启用了DHCP，脚本会释放当前DHCP配置，并重新获取新的IP配置（包括网关）。
    如果网络适配器没有启用DHCP，脚本将直接更改默认网关。
	定时检查：服务将在后台每隔一定时间（默认为60秒）检查网络连接状态，并根据ping的结果调整网关设置。

**<h3>Python 安装运行服务</h3>**

#1.安装服务

<pre><code>python NetworkMonitorService.py install</code></pre>

#2.让服务自动启动

<pre><code>python NetworkMonitorService.py --startup auto install</code></pre>

#3.启动服务

<pre><code>python NetworkMonitorService.py start</code></pre>

#4.重启服务

<pre><code>python NetworkMonitorService.py restart</code></pre>

#5.停止服务

<pre><code>python NetworkMonitorService.py stop</code></pre>

#6.删除/卸载服务

<pre><code>python NetworkMonitorService.py remove</code></pre>

**<h3>打包为可执行文件</h3>**

您可以使用之前提到的PyInstaller来将此脚本打包为一个Windows可执行文件：
<pre><code>pyinstaller --onefile --hidden-import=win32timezone NetworkMonitorService.py</code></pre>

**<h3>可执行文件安装和运行服务</h3>**
安装服务
<pre><code>NetworkMonitorService.exe install</code></pre>
启动服务
<pre><code>NetworkMonitorService.exe start</code></pre>
