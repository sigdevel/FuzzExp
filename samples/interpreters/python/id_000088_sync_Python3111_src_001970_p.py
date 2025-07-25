














































"... initcall_debug log_buf_len=16M ..."




import sys
import time
import os
import string
import re
import platform
import signal
import codecs
from datetime import datetime, timedelta
import struct
import configparser
import gzip
from threading import Thread
from subprocess import call, Popen, PIPE
import base64

def pprint(msg):
	print(msg)
	sys.stdout.flush()

def ascii(text):
	return text.decode('ascii', 'ignore')







class SystemValues:
	title = 'SleepGraph'
	version = '5.6'
	ansi = False
	rs = 0
	display = ''
	gzip = False
	sync = False
	wifi = False
	verbose = False
	testlog = True
	dmesglog = True
	ftracelog = False
	tstat = True
	mindevlen = 0.0
	mincglen = 0.0
	cgphase = ''
	cgtest = -1
	cgskip = ''
	maxfail = 0
	multitest = {'run': False, 'count': 1000000, 'delay': 0}
	max_graph_depth = 0
	callloopmaxgap = 0.0001
	callloopmaxlen = 0.005
	bufsize = 0
	cpucount = 0
	memtotal = 204800
	memfree = 204800
	srgap = 0
	cgexp = False
	testdir = ''
	outdir = ''
	tpath = '/sys/kernel/debug/tracing/'
	fpdtpath = '/sys/firmware/acpi/tables/FPDT'
	epath = '/sys/kernel/debug/tracing/events/power/'
	pmdpath = '/sys/power/pm_debug_messages'
	traceevents = [
		'suspend_resume',
		'wakeup_source_activate',
		'wakeup_source_deactivate',
		'device_pm_callback_end',
		'device_pm_callback_start'
	]
	logmsg = ''
	testcommand = ''
	mempath = '/dev/mem'
	powerfile = '/sys/power/state'
	mempowerfile = '/sys/power/mem_sleep'
	diskpowerfile = '/sys/power/disk'
	suspendmode = 'mem'
	memmode = ''
	diskmode = ''
	hostname = 'localhost'
	prefix = 'test'
	teststamp = ''
	sysstamp = ''
	dmesgstart = 0.0
	dmesgfile = ''
	ftracefile = ''
	htmlfile = 'output.html'
	result = ''
	rtcwake = True
	rtcwaketime = 15
	rtcpath = ''
	devicefilter = []
	cgfilter = []
	stamp = 0
	execcount = 1
	x2delay = 0
	skiphtml = False
	usecallgraph = False
	ftopfunc = 'pm_suspend'
	ftop = False
	usetraceevents = False
	usetracemarkers = True
	usekprobes = True
	usedevsrc = False
	useprocmon = False
	notestrun = False
	cgdump = False
	devdump = False
	mixedphaseheight = True
	devprops = dict()
	platinfo = []
	predelay = 0
	postdelay = 0
	pmdebug = ''
	tmstart = 'SUSPEND START %Y%m%d-%H:%M:%S.%f'
	tmend = 'RESUME COMPLETE %Y%m%d-%H:%M:%S.%f'
	tracefuncs = {
		'sys_sync': {},
		'ksys_sync': {},
		'__pm_notifier_call_chain': {},
		'pm_prepare_console': {},
		'pm_notifier_call_chain': {},
		'freeze_processes': {},
		'freeze_kernel_threads': {},
		'pm_restrict_gfp_mask': {},
		'acpi_suspend_begin': {},
		'acpi_hibernation_begin': {},
		'acpi_hibernation_enter': {},
		'acpi_hibernation_leave': {},
		'acpi_pm_freeze': {},
		'acpi_pm_thaw': {},
		'acpi_s2idle_end': {},
		'acpi_s2idle_sync': {},
		'acpi_s2idle_begin': {},
		'acpi_s2idle_prepare': {},
		'acpi_s2idle_prepare_late': {},
		'acpi_s2idle_wake': {},
		'acpi_s2idle_wakeup': {},
		'acpi_s2idle_restore': {},
		'acpi_s2idle_restore_early': {},
		'hibernate_preallocate_memory': {},
		'create_basic_memory_bitmaps': {},
		'swsusp_write': {},
		'suspend_console': {},
		'acpi_pm_prepare': {},
		'syscore_suspend': {},
		'arch_thaw_secondary_cpus_end': {},
		'syscore_resume': {},
		'acpi_pm_finish': {},
		'resume_console': {},
		'acpi_pm_end': {},
		'pm_restore_gfp_mask': {},
		'thaw_processes': {},
		'pm_restore_console': {},
		'CPU_OFF': {
			'func':'_cpu_down',
			'args_x86_64': {'cpu':'%di:s32'},
			'format': 'CPU_OFF[{cpu}]'
		},
		'CPU_ON': {
			'func':'_cpu_up',
			'args_x86_64': {'cpu':'%di:s32'},
			'format': 'CPU_ON[{cpu}]'
		},
	}
	dev_tracefuncs = {
		
		'msleep': { 'args_x86_64': {'time':'%di:s32'}, 'ub': 1 },
		'schedule_timeout': { 'args_x86_64': {'timeout':'%di:s32'}, 'ub': 1 },
		'udelay': { 'func':'__const_udelay', 'args_x86_64': {'loops':'%di:s32'}, 'ub': 1 },
		'usleep_range': { 'args_x86_64': {'min':'%di:s32', 'max':'%si:s32'}, 'ub': 1 },
		'mutex_lock_slowpath': { 'func':'__mutex_lock_slowpath', 'ub': 1 },
		'acpi_os_stall': {'ub': 1},
		'rt_mutex_slowlock': {'ub': 1},
		
		'acpi_resume_power_resources': {},
		'acpi_ps_execute_method': { 'args_x86_64': {
			'fullpath':'+0(+40(%di)):string',
		}},
		
		'mei_reset': {},
		
		'ext4_sync_fs': {},
		
		'ath10k_bmi_read_memory': { 'args_x86_64': {'length':'%cx:s32'} },
		'ath10k_bmi_write_memory': { 'args_x86_64': {'length':'%cx:s32'} },
		'ath10k_bmi_fast_download': { 'args_x86_64': {'length':'%cx:s32'} },
		'iwlagn_mac_start': {},
		'iwlagn_alloc_bcast_station': {},
		'iwl_trans_pcie_start_hw': {},
		'iwl_trans_pcie_start_fw': {},
		'iwl_run_init_ucode': {},
		'iwl_load_ucode_wait_alive': {},
		'iwl_alive_start': {},
		'iwlagn_mac_stop': {},
		'iwlagn_mac_suspend': {},
		'iwlagn_mac_resume': {},
		'iwlagn_mac_add_interface': {},
		'iwlagn_mac_remove_interface': {},
		'iwlagn_mac_change_interface': {},
		'iwlagn_mac_config': {},
		'iwlagn_configure_filter': {},
		'iwlagn_mac_hw_scan': {},
		'iwlagn_bss_info_changed': {},
		'iwlagn_mac_channel_switch': {},
		'iwlagn_mac_flush': {},
		
		'ata_eh_recover': { 'args_x86_64': {'port':'+36(%di):s32'} },
		
		'i915_gem_resume': {},
		'i915_restore_state': {},
		'intel_opregion_setup': {},
		'g4x_pre_enable_dp': {},
		'vlv_pre_enable_dp': {},
		'chv_pre_enable_dp': {},
		'g4x_enable_dp': {},
		'vlv_enable_dp': {},
		'intel_hpd_init': {},
		'intel_opregion_register': {},
		'intel_dp_detect': {},
		'intel_hdmi_detect': {},
		'intel_opregion_init': {},
		'intel_fbdev_set_suspend': {},
	}
	infocmds = [
		[0, 'kparams', 'cat', '/proc/cmdline'],
		[0, 'mcelog', 'mcelog'],
		[0, 'pcidevices', 'lspci', '-tv'],
		[0, 'usbdevices', 'lsusb', '-t'],
		[1, 'interrupts', 'cat', '/proc/interrupts'],
		[1, 'wakeups', 'cat', '/sys/kernel/debug/wakeup_sources'],
		[2, 'gpecounts', 'sh', '-c', 'grep -v invalid /sys/firmware/acpi/interrupts/*'],
		[2, 'suspendstats', 'sh', '-c', 'grep -v invalid /sys/power/suspend_stats/*'],
		[2, 'cpuidle', 'sh', '-c', 'grep -v invalid /sys/devices/system/cpu/cpu*/cpuidle/state*/s2idle/*'],
		[2, 'battery', 'sh', '-c', 'grep -v invalid /sys/class/power_supply/*/*'],
	]
	cgblacklist = []
	kprobes = dict()
	timeformat = '%.3f'
	cmdline = '%s %s' % \
			(os.path.basename(sys.argv[0]), ' '.join(sys.argv[1:]))
	sudouser = ''
	def __init__(self):
		self.archargs = 'args_'+platform.machine()
		self.hostname = platform.node()
		if(self.hostname == ''):
			self.hostname = 'localhost'
		rtc = "rtc0"
		if os.path.exists('/dev/rtc'):
			rtc = os.readlink('/dev/rtc')
		rtc = '/sys/class/rtc/'+rtc
		if os.path.exists(rtc) and os.path.exists(rtc+'/date') and \
			os.path.exists(rtc+'/time') and os.path.exists(rtc+'/wakealarm'):
			self.rtcpath = rtc
		if (hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()):
			self.ansi = True
		self.testdir = datetime.now().strftime('suspend-%y%m%d-%H%M%S')
		if os.getuid() == 0 and 'SUDO_USER' in os.environ and \
			os.environ['SUDO_USER']:
			self.sudouser = os.environ['SUDO_USER']
	def resetlog(self):
		self.logmsg = ''
		self.platinfo = []
	def vprint(self, msg):
		self.logmsg += msg+'\n'
		if self.verbose or msg.startswith('WARNING:'):
			pprint(msg)
	def signalHandler(self, signum, frame):
		if not self.result:
			return
		signame = self.signames[signum] if signum in self.signames else 'UNKNOWN'
		msg = 'Signal %s caused a tool exit, line %d' % (signame, frame.f_lineno)
		self.outputResult({'error':msg})
		sys.exit(3)
	def signalHandlerInit(self):
		capture = ['BUS', 'SYS', 'XCPU', 'XFSZ', 'PWR', 'HUP', 'INT', 'QUIT',
			'ILL', 'ABRT', 'FPE', 'SEGV', 'TERM']
		self.signames = dict()
		for i in capture:
			s = 'SIG'+i
			try:
				signum = getattr(signal, s)
				signal.signal(signum, self.signalHandler)
			except:
				continue
			self.signames[signum] = s
	def rootCheck(self, fatal=True):
		if(os.access(self.powerfile, os.W_OK)):
			return True
		if fatal:
			msg = 'This command requires sysfs mount and root access'
			pprint('ERROR: %s\n' % msg)
			self.outputResult({'error':msg})
			sys.exit(1)
		return False
	def rootUser(self, fatal=False):
		if 'USER' in os.environ and os.environ['USER'] == 'root':
			return True
		if fatal:
			msg = 'This command must be run as root'
			pprint('ERROR: %s\n' % msg)
			self.outputResult({'error':msg})
			sys.exit(1)
		return False
	def usable(self, file):
		return (os.path.exists(file) and os.path.getsize(file) > 0)
	def getExec(self, cmd):
		try:
			fp = Popen(['which', cmd], stdout=PIPE, stderr=PIPE).stdout
			out = ascii(fp.read()).strip()
			fp.close()
		except:
			out = ''
		if out:
			return out
		for path in ['/sbin', '/bin', '/usr/sbin', '/usr/bin',
			'/usr/local/sbin', '/usr/local/bin']:
			cmdfull = os.path.join(path, cmd)
			if os.path.exists(cmdfull):
				return cmdfull
		return out
	def setPrecision(self, num):
		if num < 0 or num > 6:
			return
		self.timeformat = '%.{0}f'.format(num)
	def setOutputFolder(self, value):
		args = dict()
		n = datetime.now()
		args['date'] = n.strftime('%y%m%d')
		args['time'] = n.strftime('%H%M%S')
		args['hostname'] = args['host'] = self.hostname
		args['mode'] = self.suspendmode
		return value.format(**args)
	def setOutputFile(self):
		if self.dmesgfile != '':
			m = re.match('(?P<name>.*)_dmesg\.txt.*', self.dmesgfile)
			if(m):
				self.htmlfile = m.group('name')+'.html'
		if self.ftracefile != '':
			m = re.match('(?P<name>.*)_ftrace\.txt.*', self.ftracefile)
			if(m):
				self.htmlfile = m.group('name')+'.html'
	def systemInfo(self, info):
		p = m = ''
		if 'baseboard-manufacturer' in info:
			m = info['baseboard-manufacturer']
		elif 'system-manufacturer' in info:
			m = info['system-manufacturer']
		if 'system-product-name' in info:
			p = info['system-product-name']
		elif 'baseboard-product-name' in info:
			p = info['baseboard-product-name']
		if m[:5].lower() == 'intel' and 'baseboard-product-name' in info:
			p = info['baseboard-product-name']
		c = info['processor-version'] if 'processor-version' in info else ''
		b = info['bios-version'] if 'bios-version' in info else ''
		r = info['bios-release-date'] if 'bios-release-date' in info else ''
		self.sysstamp = '
			(m, p, c, b, r, self.cpucount, self.memtotal, self.memfree)
	def printSystemInfo(self, fatal=False):
		self.rootCheck(True)
		out = dmidecode(self.mempath, fatal)
		if len(out) < 1:
			return
		fmt = '%-24s: %s'
		for name in sorted(out):
			print(fmt % (name, out[name]))
		print(fmt % ('cpucount', ('%d' % self.cpucount)))
		print(fmt % ('memtotal', ('%d kB' % self.memtotal)))
		print(fmt % ('memfree', ('%d kB' % self.memfree)))
	def cpuInfo(self):
		self.cpucount = 0
		fp = open('/proc/cpuinfo', 'r')
		for line in fp:
			if re.match('^processor[ \t]*:[ \t]*[0-9]*', line):
				self.cpucount += 1
		fp.close()
		fp = open('/proc/meminfo', 'r')
		for line in fp:
			m = re.match('^MemTotal:[ \t]*(?P<sz>[0-9]*) *kB', line)
			if m:
				self.memtotal = int(m.group('sz'))
			m = re.match('^MemFree:[ \t]*(?P<sz>[0-9]*) *kB', line)
			if m:
				self.memfree = int(m.group('sz'))
		fp.close()
	def initTestOutput(self, name):
		self.prefix = self.hostname
		v = open('/proc/version', 'r').read().strip()
		kver = v.split()[2]
		fmt = name+'-%m%d%y-%H%M%S'
		testtime = datetime.now().strftime(fmt)
		self.teststamp = \
			'
		ext = ''
		if self.gzip:
			ext = '.gz'
		self.dmesgfile = \
			self.testdir+'/'+self.prefix+'_'+self.suspendmode+'_dmesg.txt'+ext
		self.ftracefile = \
			self.testdir+'/'+self.prefix+'_'+self.suspendmode+'_ftrace.txt'+ext
		self.htmlfile = \
			self.testdir+'/'+self.prefix+'_'+self.suspendmode+'.html'
		if not os.path.isdir(self.testdir):
			os.makedirs(self.testdir)
		self.sudoUserchown(self.testdir)
	def getValueList(self, value):
		out = []
		for i in value.split(','):
			if i.strip():
				out.append(i.strip())
		return out
	def setDeviceFilter(self, value):
		self.devicefilter = self.getValueList(value)
	def setCallgraphFilter(self, value):
		self.cgfilter = self.getValueList(value)
	def skipKprobes(self, value):
		for k in self.getValueList(value):
			if k in self.tracefuncs:
				del self.tracefuncs[k]
			if k in self.dev_tracefuncs:
				del self.dev_tracefuncs[k]
	def setCallgraphBlacklist(self, file):
		self.cgblacklist = self.listFromFile(file)
	def rtcWakeAlarmOn(self):
		call('echo 0 > '+self.rtcpath+'/wakealarm', shell=True)
		nowtime = open(self.rtcpath+'/since_epoch', 'r').read().strip()
		if nowtime:
			nowtime = int(nowtime)
		else:
			
			nowtime = int(datetime.now().strftime('%s'))
		alarm = nowtime + self.rtcwaketime
		call('echo %d > %s/wakealarm' % (alarm, self.rtcpath), shell=True)
	def rtcWakeAlarmOff(self):
		call('echo 0 > %s/wakealarm' % self.rtcpath, shell=True)
	def initdmesg(self):
		
		fp = Popen('dmesg', stdout=PIPE).stdout
		ktime = '0'
		for line in fp:
			line = ascii(line).replace('\r\n', '')
			idx = line.find('[')
			if idx > 1:
				line = line[idx:]
			m = re.match('[ \t]*(\[ *)(?P<ktime>[0-9\.]*)(\]) (?P<msg>.*)', line)
			if(m):
				ktime = m.group('ktime')
		fp.close()
		self.dmesgstart = float(ktime)
	def getdmesg(self, testdata):
		op = self.writeDatafileHeader(self.dmesgfile, testdata)
		
		fp = Popen('dmesg', stdout=PIPE).stdout
		for line in fp:
			line = ascii(line).replace('\r\n', '')
			idx = line.find('[')
			if idx > 1:
				line = line[idx:]
			m = re.match('[ \t]*(\[ *)(?P<ktime>[0-9\.]*)(\]) (?P<msg>.*)', line)
			if(not m):
				continue
			ktime = float(m.group('ktime'))
			if ktime > self.dmesgstart:
				op.write(line)
		fp.close()
		op.close()
	def listFromFile(self, file):
		list = []
		fp = open(file)
		for i in fp.read().split('\n'):
			i = i.strip()
			if i and i[0] != '
				list.append(i)
		fp.close()
		return list
	def addFtraceFilterFunctions(self, file):
		for i in self.listFromFile(file):
			if len(i) < 2:
				continue
			self.tracefuncs[i] = dict()
	def getFtraceFilterFunctions(self, current):
		self.rootCheck(True)
		if not current:
			call('cat '+self.tpath+'available_filter_functions', shell=True)
			return
		master = self.listFromFile(self.tpath+'available_filter_functions')
		for i in sorted(self.tracefuncs):
			if 'func' in self.tracefuncs[i]:
				i = self.tracefuncs[i]['func']
			if i in master:
				print(i)
			else:
				print(self.colorText(i))
	def setFtraceFilterFunctions(self, list):
		master = self.listFromFile(self.tpath+'available_filter_functions')
		flist = ''
		for i in list:
			if i not in master:
				continue
			if ' [' in i:
				flist += i.split(' ')[0]+'\n'
			else:
				flist += i+'\n'
		fp = open(self.tpath+'set_graph_function', 'w')
		fp.write(flist)
		fp.close()
	def basicKprobe(self, name):
		self.kprobes[name] = {'name': name,'func': name,'args': dict(),'format': name}
	def defaultKprobe(self, name, kdata):
		k = kdata
		for field in ['name', 'format', 'func']:
			if field not in k:
				k[field] = name
		if self.archargs in k:
			k['args'] = k[self.archargs]
		else:
			k['args'] = dict()
			k['format'] = name
		self.kprobes[name] = k
	def kprobeColor(self, name):
		if name not in self.kprobes or 'color' not in self.kprobes[name]:
			return ''
		return self.kprobes[name]['color']
	def kprobeDisplayName(self, name, dataraw):
		if name not in self.kprobes:
			self.basicKprobe(name)
		data = ''
		quote=0
		
		for c in dataraw:
			if c == '"':
				quote = (quote + 1) % 2
			if quote and c == ' ':
				data += '_'
			elif c != '"':
				data += c
		fmt, args = self.kprobes[name]['format'], self.kprobes[name]['args']
		arglist = dict()
		
		for arg in sorted(args):
			arglist[arg] = ''
			m = re.match('.* '+arg+'=(?P<arg>.*) ', data);
			if m:
				arglist[arg] = m.group('arg')
			else:
				m = re.match('.* '+arg+'=(?P<arg>.*)', data);
				if m:
					arglist[arg] = m.group('arg')
		out = fmt.format(**arglist)
		out = out.replace(' ', '_').replace('"', '')
		return out
	def kprobeText(self, kname, kprobe):
		name = fmt = func = kname
		args = dict()
		if 'name' in kprobe:
			name = kprobe['name']
		if 'format' in kprobe:
			fmt = kprobe['format']
		if 'func' in kprobe:
			func = kprobe['func']
		if self.archargs in kprobe:
			args = kprobe[self.archargs]
		if 'args' in kprobe:
			args = kprobe['args']
		if re.findall('{(?P<n>[a-z,A-Z,0-9]*)}', func):
			doError('Kprobe "%s" has format info in the function name "%s"' % (name, func))
		for arg in re.findall('{(?P<n>[a-z,A-Z,0-9]*)}', fmt):
			if arg not in args:
				doError('Kprobe "%s" is missing argument "%s"' % (name, arg))
		val = 'p:%s_cal %s' % (name, func)
		for i in sorted(args):
			val += ' %s=%s' % (i, args[i])
		val += '\nr:%s_ret %s $retval\n' % (name, func)
		return val
	def addKprobes(self, output=False):
		if len(self.kprobes) < 1:
			return
		if output:
			pprint('    kprobe functions in this kernel:')
		
		rejects = []
		
		kpl = [[], [], [], []]
		linesout = len(self.kprobes)
		for name in sorted(self.kprobes):
			res = self.colorText('YES', 32)
			if not self.testKprobe(name, self.kprobes[name]):
				res = self.colorText('NO')
				rejects.append(name)
			else:
				if name in self.tracefuncs:
					kpl[0].append(name)
				elif name in self.dev_tracefuncs:
					if 'ub' in self.dev_tracefuncs[name]:
						kpl[1].append(name)
					else:
						kpl[3].append(name)
				else:
					kpl[2].append(name)
			if output:
				pprint('         %s: %s' % (name, res))
		kplist = kpl[0] + kpl[1] + kpl[2] + kpl[3]
		
		for name in rejects:
			self.kprobes.pop(name)
		
		self.fsetVal('', 'kprobe_events')
		kprobeevents = ''
		for kp in kplist:
			kprobeevents += self.kprobeText(kp, self.kprobes[kp])
		self.fsetVal(kprobeevents, 'kprobe_events')
		if output:
			check = self.fgetVal('kprobe_events')
			linesack = (len(check.split('\n')) - 1) // 2
			pprint('    kprobe functions enabled: %d/%d' % (linesack, linesout))
		self.fsetVal('1', 'events/kprobes/enable')
	def testKprobe(self, kname, kprobe):
		self.fsetVal('0', 'events/kprobes/enable')
		kprobeevents = self.kprobeText(kname, kprobe)
		if not kprobeevents:
			return False
		try:
			self.fsetVal(kprobeevents, 'kprobe_events')
			check = self.fgetVal('kprobe_events')
		except:
			return False
		linesout = len(kprobeevents.split('\n'))
		linesack = len(check.split('\n'))
		if linesack < linesout:
			return False
		return True
	def setVal(self, val, file):
		if not os.path.exists(file):
			return False
		try:
			fp = open(file, 'wb', 0)
			fp.write(val.encode())
			fp.flush()
			fp.close()
		except:
			return False
		return True
	def fsetVal(self, val, path):
		return self.setVal(val, self.tpath+path)
	def getVal(self, file):
		res = ''
		if not os.path.exists(file):
			return res
		try:
			fp = open(file, 'r')
			res = fp.read()
			fp.close()
		except:
			pass
		return res
	def fgetVal(self, path):
		return self.getVal(self.tpath+path)
	def cleanupFtrace(self):
		if(self.usecallgraph or self.usetraceevents or self.usedevsrc):
			self.fsetVal('0', 'events/kprobes/enable')
			self.fsetVal('', 'kprobe_events')
			self.fsetVal('1024', 'buffer_size_kb')
		if self.pmdebug:
			self.setVal(self.pmdebug, self.pmdpath)
	def setupAllKprobes(self):
		for name in self.tracefuncs:
			self.defaultKprobe(name, self.tracefuncs[name])
		for name in self.dev_tracefuncs:
			self.defaultKprobe(name, self.dev_tracefuncs[name])
	def isCallgraphFunc(self, name):
		if len(self.tracefuncs) < 1 and self.suspendmode == 'command':
			return True
		for i in self.tracefuncs:
			if 'func' in self.tracefuncs[i]:
				f = self.tracefuncs[i]['func']
			else:
				f = i
			if name == f:
				return True
		return False
	def initFtrace(self, quiet=False):
		if not quiet:
			sysvals.printSystemInfo(False)
			pprint('INITIALIZING FTRACE...')
		
		self.fsetVal('0', 'tracing_on')
		self.cleanupFtrace()
		
		pv = self.getVal(self.pmdpath)
		if pv != '1':
			self.setVal('1', self.pmdpath)
			self.pmdebug = pv
		
		self.fsetVal('global', 'trace_clock')
		self.fsetVal('nop', 'current_tracer')
		
		cpus = max(1, self.cpucount)
		if self.bufsize > 0:
			tgtsize = self.bufsize
		elif self.usecallgraph or self.usedevsrc:
			bmax = (1*1024*1024) if self.suspendmode in ['disk', 'command'] \
				else (3*1024*1024)
			tgtsize = min(self.memfree, bmax)
		else:
			tgtsize = 65536
		while not self.fsetVal('%d' % (tgtsize // cpus), 'buffer_size_kb'):
			
			tgtsize -= 65536
			if tgtsize < 65536:
				tgtsize = int(self.fgetVal('buffer_size_kb')) * cpus
				break
		self.vprint('Setting trace buffers to %d kB (%d kB per cpu)' % (tgtsize, tgtsize/cpus))
		
		if(self.usecallgraph):
			
			self.fsetVal('function_graph', 'current_tracer')
			self.fsetVal('', 'set_ftrace_filter')
			
			self.fsetVal('print-parent', 'trace_options')
			self.fsetVal('funcgraph-abstime', 'trace_options')
			self.fsetVal('funcgraph-cpu', 'trace_options')
			self.fsetVal('funcgraph-duration', 'trace_options')
			self.fsetVal('funcgraph-proc', 'trace_options')
			self.fsetVal('funcgraph-tail', 'trace_options')
			self.fsetVal('nofuncgraph-overhead', 'trace_options')
			self.fsetVal('context-info', 'trace_options')
			self.fsetVal('graph-time', 'trace_options')
			self.fsetVal('%d' % self.max_graph_depth, 'max_graph_depth')
			cf = ['dpm_run_callback']
			if(self.usetraceevents):
				cf += ['dpm_prepare', 'dpm_complete']
			for fn in self.tracefuncs:
				if 'func' in self.tracefuncs[fn]:
					cf.append(self.tracefuncs[fn]['func'])
				else:
					cf.append(fn)
			if self.ftop:
				self.setFtraceFilterFunctions([self.ftopfunc])
			else:
				self.setFtraceFilterFunctions(cf)
		
		elif self.usekprobes:
			for name in self.tracefuncs:
				self.defaultKprobe(name, self.tracefuncs[name])
			if self.usedevsrc:
				for name in self.dev_tracefuncs:
					self.defaultKprobe(name, self.dev_tracefuncs[name])
			if not quiet:
				pprint('INITIALIZING KPROBES...')
			self.addKprobes(self.verbose)
		if(self.usetraceevents):
			
			events = iter(self.traceevents)
			for e in events:
				self.fsetVal('1', 'events/power/'+e+'/enable')
		
		self.fsetVal('', 'trace')
	def verifyFtrace(self):
		
		files = ['buffer_size_kb', 'current_tracer', 'trace', 'trace_clock',
				 'trace_marker', 'trace_options', 'tracing_on']
		
		tp = self.tpath
		if(self.usecallgraph):
			files += [
				'available_filter_functions',
				'set_ftrace_filter',
				'set_graph_function'
			]
		for f in files:
			if(os.path.exists(tp+f) == False):
				return False
		return True
	def verifyKprobes(self):
		
		files = ['kprobe_events', 'events']
		tp = self.tpath
		for f in files:
			if(os.path.exists(tp+f) == False):
				return False
		return True
	def colorText(self, str, color=31):
		if not self.ansi:
			return str
		return '\x1B[%d;40m%s\x1B[m' % (color, str)
	def writeDatafileHeader(self, filename, testdata):
		fp = self.openlog(filename, 'w')
		fp.write('%s\n%s\n
		for test in testdata:
			if 'fw' in test:
				fw = test['fw']
				if(fw):
					fp.write('
			if 'turbo' in test:
				fp.write('
			if 'wifi' in test:
				fp.write('
			if test['error'] or len(testdata) > 1:
				fp.write('
		return fp
	def sudoUserchown(self, dir):
		if os.path.exists(dir) and self.sudouser:
			cmd = 'chown -R {0}:{0} {1} > /dev/null 2>&1'
			call(cmd.format(self.sudouser, dir), shell=True)
	def outputResult(self, testdata, num=0):
		if not self.result:
			return
		n = ''
		if num > 0:
			n = '%d' % num
		fp = open(self.result, 'a')
		if 'error' in testdata:
			fp.write('result%s: fail\n' % n)
			fp.write('error%s: %s\n' % (n, testdata['error']))
		else:
			fp.write('result%s: pass\n' % n)
		for v in ['suspend', 'resume', 'boot', 'lastinit']:
			if v in testdata:
				fp.write('%s%s: %.3f\n' % (v, n, testdata[v]))
		for v in ['fwsuspend', 'fwresume']:
			if v in testdata:
				fp.write('%s%s: %.3f\n' % (v, n, testdata[v] / 1000000.0))
		if 'bugurl' in testdata:
			fp.write('url%s: %s\n' % (n, testdata['bugurl']))
		fp.close()
		self.sudoUserchown(self.result)
	def configFile(self, file):
		dir = os.path.dirname(os.path.realpath(__file__))
		if os.path.exists(file):
			return file
		elif os.path.exists(dir+'/'+file):
			return dir+'/'+file
		elif os.path.exists(dir+'/config/'+file):
			return dir+'/config/'+file
		return ''
	def openlog(self, filename, mode):
		isgz = self.gzip
		if mode == 'r':
			try:
				with gzip.open(filename, mode+'t') as fp:
					test = fp.read(64)
				isgz = True
			except:
				isgz = False
		if isgz:
			return gzip.open(filename, mode+'t')
		return open(filename, mode)
	def b64unzip(self, data):
		try:
			out = codecs.decode(base64.b64decode(data), 'zlib').decode()
		except:
			out = data
		return out
	def b64zip(self, data):
		out = base64.b64encode(codecs.encode(data.encode(), 'zlib')).decode()
		return out
	def platforminfo(self, cmdafter):
		
		if not os.path.exists(self.ftracefile):
			return False
		footer = '

		
		if self.suspendmode == 'command' and self.testcommand:
			footer += '

		
		props = dict()
		tp = TestProps()
		tf = self.openlog(self.ftracefile, 'r')
		for line in tf:
			
			m = re.match(tp.tracertypefmt, line)
			if(m):
				tp.setTracerType(m.group('t'))
				continue
			
			m = re.match(tp.ftrace_line_fmt, line)
			if(not m or 'device_pm_callback_start' not in line):
				continue
			m = re.match('.*: (?P<drv>.*) (?P<d>.*), parent: *(?P<p>.*), .*', m.group('msg'));
			if(not m):
				continue
			dev = m.group('d')
			if dev not in props:
				props[dev] = DevProps()
		tf.close()

		
		for dirname, dirnames, filenames in os.walk('/sys/devices'):
			if(re.match('.*/power', dirname) and 'async' in filenames):
				dev = dirname.split('/')[-2]
				if dev in props and (not props[dev].syspath or len(dirname) < len(props[dev].syspath)):
					props[dev].syspath = dirname[:-6]

		
		for dev in sorted(props):
			dirname = props[dev].syspath
			if not dirname or not os.path.exists(dirname):
				continue
			with open(dirname+'/power/async') as fp:
				text = fp.read()
				props[dev].isasync = False
				if 'enabled' in text:
					props[dev].isasync = True
			fields = os.listdir(dirname)
			if 'product' in fields:
				with open(dirname+'/product', 'rb') as fp:
					props[dev].altname = ascii(fp.read())
			elif 'name' in fields:
				with open(dirname+'/name', 'rb') as fp:
					props[dev].altname = ascii(fp.read())
			elif 'model' in fields:
				with open(dirname+'/model', 'rb') as fp:
					props[dev].altname = ascii(fp.read())
			elif 'description' in fields:
				with open(dirname+'/description', 'rb') as fp:
					props[dev].altname = ascii(fp.read())
			elif 'id' in fields:
				with open(dirname+'/id', 'rb') as fp:
					props[dev].altname = ascii(fp.read())
			elif 'idVendor' in fields and 'idProduct' in fields:
				idv, idp = '', ''
				with open(dirname+'/idVendor', 'rb') as fp:
					idv = ascii(fp.read()).strip()
				with open(dirname+'/idProduct', 'rb') as fp:
					idp = ascii(fp.read()).strip()
				props[dev].altname = '%s:%s' % (idv, idp)
			if props[dev].altname:
				out = props[dev].altname.strip().replace('\n', ' ')\
					.replace(',', ' ').replace(';', ' ')
				props[dev].altname = out

		
		out = ''
		for dev in sorted(props):
			out += props[dev].out(dev)
		footer += '

		
		for name, cmdline, info in cmdafter:
			footer += '

		with self.openlog(self.ftracefile, 'a') as fp:
			fp.write(footer)
		return True
	def commonPrefix(self, list):
		if len(list) < 2:
			return ''
		prefix = list[0]
		for s in list[1:]:
			while s[:len(prefix)] != prefix and prefix:
				prefix = prefix[:len(prefix)-1]
			if not prefix:
				break
		if '/' in prefix and prefix[-1] != '/':
			prefix = prefix[0:prefix.rfind('/')+1]
		return prefix
	def dictify(self, text, format):
		out = dict()
		header = True if format == 1 else False
		delim = ' ' if format == 1 else ':'
		for line in text.split('\n'):
			if header:
				header, out['@'] = False, line
				continue
			line = line.strip()
			if delim in line:
				data = line.split(delim, 1)
				num = re.search(r'[\d]+', data[1])
				if format == 2 and num:
					out[data[0].strip()] = num.group()
				else:
					out[data[0].strip()] = data[1]
		return out
	def cmdinfo(self, begin, debug=False):
		out = []
		if begin:
			self.cmd1 = dict()
		for cargs in self.infocmds:
			delta, name = cargs[0], cargs[1]
			cmdline, cmdpath = ' '.join(cargs[2:]), self.getExec(cargs[2])
			if not cmdpath or (begin and not delta):
				continue
			try:
				fp = Popen([cmdpath]+cargs[3:], stdout=PIPE, stderr=PIPE).stdout
				info = ascii(fp.read()).strip()
				fp.close()
			except:
				continue
			if not debug and begin:
				self.cmd1[name] = self.dictify(info, delta)
			elif not debug and delta and name in self.cmd1:
				before, after = self.cmd1[name], self.dictify(info, delta)
				dinfo = ('\t%s\n' % before['@']) if '@' in before else ''
				prefix = self.commonPrefix(list(before.keys()))
				for key in sorted(before):
					if key in after and before[key] != after[key]:
						title = key.replace(prefix, '')
						if delta == 2:
							dinfo += '\t%s : %s -> %s\n' % \
								(title, before[key].strip(), after[key].strip())
						else:
							dinfo += '%10s (start) : %s\n%10s (after) : %s\n' % \
								(title, before[key], title, after[key])
				dinfo = '\tnothing changed' if not dinfo else dinfo.rstrip()
				out.append((name, cmdline, dinfo))
			else:
				out.append((name, cmdline, '\tnothing' if not info else info))
		return out
	def haveTurbostat(self):
		if not self.tstat:
			return False
		cmd = self.getExec('turbostat')
		if not cmd:
			return False
		fp = Popen([cmd, '-v'], stdout=PIPE, stderr=PIPE).stderr
		out = ascii(fp.read()).strip()
		fp.close()
		if re.match('turbostat version .*', out):
			self.vprint(out)
			return True
		return False
	def turbostat(self):
		cmd = self.getExec('turbostat')
		rawout = keyline = valline = ''
		fullcmd = '%s -q -S echo freeze > %s' % (cmd, self.powerfile)
		fp = Popen(['sh', '-c', fullcmd], stdout=PIPE, stderr=PIPE).stderr
		for line in fp:
			line = ascii(line)
			rawout += line
			if keyline and valline:
				continue
			if re.match('(?i)Avg_MHz.*', line):
				keyline = line.strip().split()
			elif keyline:
				valline = line.strip().split()
		fp.close()
		if not keyline or not valline or len(keyline) != len(valline):
			errmsg = 'unrecognized turbostat output:\n'+rawout.strip()
			self.vprint(errmsg)
			if not self.verbose:
				pprint(errmsg)
			return ''
		if self.verbose:
			pprint(rawout.strip())
		out = []
		for key in keyline:
			idx = keyline.index(key)
			val = valline[idx]
			out.append('%s=%s' % (key, val))
		return '|'.join(out)
	def wifiDetails(self, dev):
		try:
			info = open('/sys/class/net/%s/device/uevent' % dev, 'r').read().strip()
		except:
			return dev
		vals = [dev]
		for prop in info.split('\n'):
			if prop.startswith('DRIVER=') or prop.startswith('PCI_ID='):
				vals.append(prop.split('=')[-1])
		return ':'.join(vals)
	def checkWifi(self, dev=''):
		try:
			w = open('/proc/net/wireless', 'r').read().strip()
		except:
			return ''
		for line in reversed(w.split('\n')):
			m = re.match(' *(?P<dev>.*): (?P<stat>[0-9a-f]*) .*', w.split('\n')[-1])
			if not m or (dev and dev != m.group('dev')):
				continue
			return m.group('dev')
		return ''
	def pollWifi(self, dev, timeout=60):
		start = time.time()
		while (time.time() - start) < timeout:
			w = self.checkWifi(dev)
			if w:
				return '%s reconnected %.2f' % \
					(self.wifiDetails(dev), max(0, time.time() - start))
			time.sleep(0.01)
		return '%s timeout %d' % (self.wifiDetails(dev), timeout)
	def errorSummary(self, errinfo, msg):
		found = False
		for entry in errinfo:
			if re.match(entry['match'], msg):
				entry['count'] += 1
				if self.hostname not in entry['urls']:
					entry['urls'][self.hostname] = [self.htmlfile]
				elif self.htmlfile not in entry['urls'][self.hostname]:
					entry['urls'][self.hostname].append(self.htmlfile)
				found = True
				break
		if found:
			return
		arr = msg.split()
		for j in range(len(arr)):
			if re.match('^[0-9,\-\.]*$', arr[j]):
				arr[j] = '[0-9,\-\.]*'
			else:
				arr[j] = arr[j]\
					.replace('\\', '\\\\').replace(']', '\]').replace('[', '\[')\
					.replace('.', '\.').replace('+', '\+').replace('*', '\*')\
					.replace('(', '\(').replace(')', '\)').replace('}', '\}')\
					.replace('{', '\{')
		mstr = ' *'.join(arr)
		entry = {
			'line': msg,
			'match': mstr,
			'count': 1,
			'urls': {self.hostname: [self.htmlfile]}
		}
		errinfo.append(entry)
	def multistat(self, start, idx, finish):
		if 'time' in self.multitest:
			id = '%d Duration=%dmin' % (idx+1, self.multitest['time'])
		else:
			id = '%d/%d' % (idx+1, self.multitest['count'])
		t = time.time()
		if 'start' not in self.multitest:
			self.multitest['start'] = self.multitest['last'] = t
			self.multitest['total'] = 0.0
			pprint('TEST (%s) START' % id)
			return
		dt = t - self.multitest['last']
		if not start:
			if idx == 0 and self.multitest['delay'] > 0:
				self.multitest['total'] += self.multitest['delay']
			pprint('TEST (%s) COMPLETE -- Duration %.1fs' % (id, dt))
			return
		self.multitest['total'] += dt
		self.multitest['last'] = t
		avg = self.multitest['total'] / idx
		if 'time' in self.multitest:
			left = finish - datetime.now()
			left -= timedelta(microseconds=left.microseconds)
		else:
			left = timedelta(seconds=((self.multitest['count'] - idx) * int(avg)))
		pprint('TEST (%s) START - Avg Duration %.1fs, Time left %s' % \
			(id, avg, str(left)))
	def multiinit(self, c, d):
		sz, unit = 'count', 'm'
		if c.endswith('d') or c.endswith('h') or c.endswith('m'):
			sz, unit, c = 'time', c[-1], c[:-1]
		self.multitest['run'] = True
		self.multitest[sz] = getArgInt('multi: n d (exec count)', c, 1, 1000000, False)
		self.multitest['delay'] = getArgInt('multi: n d (delay between tests)', d, 0, 3600, False)
		if unit == 'd':
			self.multitest[sz] *= 1440
		elif unit == 'h':
			self.multitest[sz] *= 60

sysvals = SystemValues()
switchvalues = ['enable', 'disable', 'on', 'off', 'true', 'false', '1', '0']
switchoff = ['disable', 'off', 'false', '0']
suspendmodename = {
	'freeze': 'Freeze (S0)',
	'standby': 'Standby (S1)',
	'mem': 'Suspend (S3)',
	'disk': 'Hibernate (S4)'
}





class DevProps:
	def __init__(self):
		self.syspath = ''
		self.altname = ''
		self.isasync = True
		self.xtraclass = ''
		self.xtrainfo = ''
	def out(self, dev):
		return '%s,%s,%d;' % (dev, self.altname, self.isasync)
	def debug(self, dev):
		pprint('%s:\n\taltname = %s\n\t  async = %s' % (dev, self.altname, self.isasync))
	def altName(self, dev):
		if not self.altname or self.altname == dev:
			return dev
		return '%s [%s]' % (self.altname, dev)
	def xtraClass(self):
		if self.xtraclass:
			return ' '+self.xtraclass
		if not self.isasync:
			return ' sync'
		return ''
	def xtraInfo(self):
		if self.xtraclass:
			return ' '+self.xtraclass
		if self.isasync:
			return ' async_device'
		return ' sync_device'





class DeviceNode:
	def __init__(self, nodename, nodedepth):
		self.name = nodename
		self.children = []
		self.depth = nodedepth






















class Data:
	phasedef = {
		'suspend_prepare': {'order': 0, 'color': '
		        'suspend': {'order': 1, 'color': '
		   'suspend_late': {'order': 2, 'color': '
		  'suspend_noirq': {'order': 3, 'color': '
		'suspend_machine': {'order': 4, 'color': '
		 'resume_machine': {'order': 5, 'color': '
		   'resume_noirq': {'order': 6, 'color': '
		   'resume_early': {'order': 7, 'color': '
		         'resume': {'order': 8, 'color': '
		'resume_complete': {'order': 9, 'color': '
	}
	errlist = {
		'HWERROR' : r'.*\[ *Hardware Error *\].*',
		'FWBUG'   : r'.*\[ *Firmware Bug *\].*',
		'BUG'     : r'(?i).*\bBUG\b.*',
		'ERROR'   : r'(?i).*\bERROR\b.*',
		'WARNING' : r'(?i).*\bWARNING\b.*',
		'FAULT'   : r'(?i).*\bFAULT\b.*',
		'FAIL'    : r'(?i).*\bFAILED\b.*',
		'INVALID' : r'(?i).*\bINVALID\b.*',
		'CRASH'   : r'(?i).*\bCRASHED\b.*',
		'IRQ'     : r'.*\bgenirq: .*',
		'TASKFAIL': r'.*Freezing of tasks *.*',
		'ACPI'    : r'.*\bACPI *(?P<b>[A-Za-z]*) *Error[: ].*',
		'DISKFULL': r'.*\bNo space left on device.*',
		'USBERR'  : r'.*usb .*device .*, error [0-9-]*',
		'ATAERR'  : r' *ata[0-9\.]*: .*failed.*',
		'MEIERR'  : r' *mei.*: .*failed.*',
		'TPMERR'  : r'(?i) *tpm *tpm[0-9]*: .*error.*',
	}
	def __init__(self, num):
		idchar = 'abcdefghij'
		self.start = 0.0 
		self.end = 0.0   
		self.hwstart = 0 
		self.hwend = 0   
		self.tSuspended = 0.0 
		self.tResumed = 0.0   
		self.tKernSus = 0.0   
		self.tKernRes = 0.0   
		self.fwValid = False  
		self.fwSuspend = 0    
		self.fwResume = 0     
		self.html_device_id = 0
		self.stamp = 0
		self.outfile = ''
		self.kerror = False
		self.wifi = dict()
		self.turbostat = 0
		self.enterfail = ''
		self.currphase = ''
		self.pstl = dict()    
		self.testnumber = num
		self.idstr = idchar[num]
		self.dmesgtext = []   
		self.dmesg = dict()   
		self.errorinfo = {'suspend':[],'resume':[]}
		self.tLow = []        
		self.devpids = []
		self.devicegroups = 0
	def sortedPhases(self):
		return sorted(self.dmesg, key=lambda k:self.dmesg[k]['order'])
	def initDevicegroups(self):
		
		for phase in sorted(self.dmesg.keys()):
			if '*' in phase:
				p = phase.split('*')
				pnew = '%s%d' % (p[0], len(p))
				self.dmesg[pnew] = self.dmesg.pop(phase)
		self.devicegroups = []
		for phase in self.sortedPhases():
			self.devicegroups.append([phase])
	def nextPhase(self, phase, offset):
		order = self.dmesg[phase]['order'] + offset
		for p in self.dmesg:
			if self.dmesg[p]['order'] == order:
				return p
		return ''
	def lastPhase(self):
		plist = self.sortedPhases()
		if len(plist) < 1:
			return ''
		return plist[-1]
	def turbostatInfo(self):
		tp = TestProps()
		out = {'syslpi':'N/A','pkgpc10':'N/A'}
		for line in self.dmesgtext:
			m = re.match(tp.tstatfmt, line)
			if not m:
				continue
			for i in m.group('t').split('|'):
				if 'SYS%LPI' in i:
					out['syslpi'] = i.split('=')[-1]+'%'
				elif 'pc10' in i:
					out['pkgpc10'] = i.split('=')[-1]+'%'
			break
		return out
	def extractErrorInfo(self):
		lf = self.dmesgtext
		if len(self.dmesgtext) < 1 and sysvals.dmesgfile:
			lf = sysvals.openlog(sysvals.dmesgfile, 'r')
		i = 0
		list = []
		for line in lf:
			i += 1
			m = re.match('[ \t]*(\[ *)(?P<ktime>[0-9\.]*)(\]) (?P<msg>.*)', line)
			if not m:
				continue
			t = float(m.group('ktime'))
			if t < self.start or t > self.end:
				continue
			dir = 'suspend' if t < self.tSuspended else 'resume'
			msg = m.group('msg')
			if re.match('capability: warning: .*', msg):
				continue
			for err in self.errlist:
				if re.match(self.errlist[err], msg):
					list.append((msg, err, dir, t, i, i))
					self.kerror = True
					break
		msglist = []
		for msg, type, dir, t, idx1, idx2 in list:
			msglist.append(msg)
			self.errorinfo[dir].append((type, t, idx1, idx2))
		if self.kerror:
			sysvals.dmesglog = True
		if len(self.dmesgtext) < 1 and sysvals.dmesgfile:
			lf.close()
		return msglist
	def setStart(self, time, msg=''):
		self.start = time
		if msg:
			try:
				self.hwstart = datetime.strptime(msg, sysvals.tmstart)
			except:
				self.hwstart = 0
	def setEnd(self, time, msg=''):
		self.end = time
		if msg:
			try:
				self.hwend = datetime.strptime(msg, sysvals.tmend)
			except:
				self.hwend = 0
	def isTraceEventOutsideDeviceCalls(self, pid, time):
		for phase in self.sortedPhases():
			list = self.dmesg[phase]['list']
			for dev in list:
				d = list[dev]
				if(d['pid'] == pid and time >= d['start'] and
					time < d['end']):
					return False
		return True
	def sourcePhase(self, start):
		for phase in self.sortedPhases():
			if 'machine' in phase:
				continue
			pend = self.dmesg[phase]['end']
			if start <= pend:
				return phase
		return 'resume_complete'
	def sourceDevice(self, phaselist, start, end, pid, type):
		tgtdev = ''
		for phase in phaselist:
			list = self.dmesg[phase]['list']
			for devname in list:
				dev = list[devname]
				
				if dev['pid'] != pid:
					continue
				devS = dev['start']
				devE = dev['end']
				if type == 'device':
					
					if(start < devS or start >= devE or end <= devS or end > devE):
						continue
				elif type == 'thread':
					
					if start < devS:
						dev['start'] = start
					if end > devE:
						dev['end'] = end
				tgtdev = dev
				break
		return tgtdev
	def addDeviceFunctionCall(self, displayname, kprobename, proc, pid, start, end, cdata, rdata):
		
		phases = self.sortedPhases()
		tgtdev = self.sourceDevice(phases, start, end, pid, 'device')
		
		
		if not tgtdev and pid in self.devpids:
			return False
		
		if not tgtdev:
			tgtdev = self.sourceDevice(phases, start, end, pid, 'thread')
		
		if not tgtdev:
			if proc == '<...>':
				threadname = 'kthread-%d' % (pid)
			else:
				threadname = '%s-%d' % (proc, pid)
			tgtphase = self.sourcePhase(start)
			self.newAction(tgtphase, threadname, pid, '', start, end, '', ' kth', '')
			return self.addDeviceFunctionCall(displayname, kprobename, proc, pid, start, end, cdata, rdata)
		
		if not tgtdev:
			sysvals.vprint('[%f - %f] %s-%d %s %s %s' % \
				(start, end, proc, pid, kprobename, cdata, rdata))
			return False
		
		if('src' not in tgtdev):
			tgtdev['src'] = []
		dtf = sysvals.dev_tracefuncs
		ubiquitous = False
		if kprobename in dtf and 'ub' in dtf[kprobename]:
			ubiquitous = True
		title = cdata+' '+rdata
		mstr = '\(.*\) *(?P<args>.*) *\((?P<caller>.*)\+.* arg1=(?P<ret>.*)'
		m = re.match(mstr, title)
		if m:
			c = m.group('caller')
			a = m.group('args').strip()
			r = m.group('ret')
			if len(r) > 6:
				r = ''
			else:
				r = 'ret=%s ' % r
			if ubiquitous and c in dtf and 'ub' in dtf[c]:
				return False
		color = sysvals.kprobeColor(kprobename)
		e = DevFunction(displayname, a, c, r, start, end, ubiquitous, proc, pid, color)
		tgtdev['src'].append(e)
		return True
	def overflowDevices(self):
		
		devlist = []
		for phase in self.sortedPhases():
			list = self.dmesg[phase]['list']
			for devname in list:
				dev = list[devname]
				if dev['end'] > self.end:
					devlist.append(dev)
		return devlist
	def mergeOverlapDevices(self, devlist):
		
		for dev in devlist:
			devname = dev['name']
			for phase in self.sortedPhases():
				list = self.dmesg[phase]['list']
				if devname not in list:
					continue
				tdev = list[devname]
				o = min(dev['end'], tdev['end']) - max(dev['start'], tdev['start'])
				if o <= 0:
					continue
				dev['end'] = tdev['end']
				if 'src' not in dev or 'src' not in tdev:
					continue
				dev['src'] += tdev['src']
				del list[devname]
	def usurpTouchingThread(self, name, dev):
		
		for phase in self.sortedPhases():
			list = self.dmesg[phase]['list']
			if name in list:
				tdev = list[name]
				if tdev['start'] - dev['end'] < 0.1:
					dev['end'] = tdev['end']
					if 'src' not in dev:
						dev['src'] = []
					if 'src' in tdev:
						dev['src'] += tdev['src']
					del list[name]
				break
	def stitchTouchingThreads(self, testlist):
		
		for phase in self.sortedPhases():
			list = self.dmesg[phase]['list']
			for devname in list:
				dev = list[devname]
				if 'htmlclass' not in dev or 'kth' not in dev['htmlclass']:
					continue
				for data in testlist:
					data.usurpTouchingThread(devname, dev)
	def optimizeDevSrc(self):
		
		for phase in self.sortedPhases():
			list = self.dmesg[phase]['list']
			for dev in list:
				if 'src' not in list[dev]:
					continue
				src = list[dev]['src']
				p = 0
				for e in sorted(src, key=lambda event: event.time):
					if not p or not e.repeat(p):
						p = e
						continue
					
					p.end = e.end
					p.length = p.end - p.time
					p.count += 1
					src.remove(e)
	def trimTimeVal(self, t, t0, dT, left):
		if left:
			if(t > t0):
				if(t - dT < t0):
					return t0
				return t - dT
			else:
				return t
		else:
			if(t < t0 + dT):
				if(t > t0):
					return t0 + dT
				return t + dT
			else:
				return t
	def trimTime(self, t0, dT, left):
		self.tSuspended = self.trimTimeVal(self.tSuspended, t0, dT, left)
		self.tResumed = self.trimTimeVal(self.tResumed, t0, dT, left)
		self.start = self.trimTimeVal(self.start, t0, dT, left)
		self.tKernSus = self.trimTimeVal(self.tKernSus, t0, dT, left)
		self.tKernRes = self.trimTimeVal(self.tKernRes, t0, dT, left)
		self.end = self.trimTimeVal(self.end, t0, dT, left)
		for phase in self.sortedPhases():
			p = self.dmesg[phase]
			p['start'] = self.trimTimeVal(p['start'], t0, dT, left)
			p['end'] = self.trimTimeVal(p['end'], t0, dT, left)
			list = p['list']
			for name in list:
				d = list[name]
				d['start'] = self.trimTimeVal(d['start'], t0, dT, left)
				d['end'] = self.trimTimeVal(d['end'], t0, dT, left)
				d['length'] = d['end'] - d['start']
				if('ftrace' in d):
					cg = d['ftrace']
					cg.start = self.trimTimeVal(cg.start, t0, dT, left)
					cg.end = self.trimTimeVal(cg.end, t0, dT, left)
					for line in cg.list:
						line.time = self.trimTimeVal(line.time, t0, dT, left)
				if('src' in d):
					for e in d['src']:
						e.time = self.trimTimeVal(e.time, t0, dT, left)
		for dir in ['suspend', 'resume']:
			list = []
			for e in self.errorinfo[dir]:
				type, tm, idx1, idx2 = e
				tm = self.trimTimeVal(tm, t0, dT, left)
				list.append((type, tm, idx1, idx2))
			self.errorinfo[dir] = list
	def trimFreezeTime(self, tZero):
		
		lp = ''
		for phase in self.sortedPhases():
			if 'resume_machine' in phase and 'suspend_machine' in lp:
				tS, tR = self.dmesg[lp]['end'], self.dmesg[phase]['start']
				tL = tR - tS
				if tL > 0:
					left = True if tR > tZero else False
					self.trimTime(tS, tL, left)
					self.tLow.append('%.0f'%(tL*1000))
			lp = phase
	def getMemTime(self):
		if not self.hwstart or not self.hwend:
			return
		stime = (self.tSuspended - self.start) * 1000000
		rtime = (self.end - self.tResumed) * 1000000
		hws = self.hwstart + timedelta(microseconds=stime)
		hwr = self.hwend - timedelta(microseconds=rtime)
		self.tLow.append('%.0f'%((hwr - hws).total_seconds() * 1000))
	def getTimeValues(self):
		sktime = (self.tSuspended - self.tKernSus) * 1000
		rktime = (self.tKernRes - self.tResumed) * 1000
		return (sktime, rktime)
	def setPhase(self, phase, ktime, isbegin, order=-1):
		if(isbegin):
			
			if self.currphase:
				if 'resume_machine' not in self.currphase:
					sysvals.vprint('WARNING: phase %s failed to end' % self.currphase)
				self.dmesg[self.currphase]['end'] = ktime
			phases = self.dmesg.keys()
			color = self.phasedef[phase]['color']
			count = len(phases) if order < 0 else order
			
			while phase in phases:
				phase += '*'
			self.dmesg[phase] = {'list': dict(), 'start': -1.0, 'end': -1.0,
				'row': 0, 'color': color, 'order': count}
			self.dmesg[phase]['start'] = ktime
			self.currphase = phase
		else:
			
			if phase not in self.currphase:
				if self.currphase:
					sysvals.vprint('WARNING: %s ended instead of %s, ftrace corruption?' % (phase, self.currphase))
				else:
					sysvals.vprint('WARNING: %s ended without a start, ftrace corruption?' % phase)
					return phase
			phase = self.currphase
			self.dmesg[phase]['end'] = ktime
			self.currphase = ''
		return phase
	def sortedDevices(self, phase):
		list = self.dmesg[phase]['list']
		return sorted(list, key=lambda k:list[k]['start'])
	def fixupInitcalls(self, phase):
		
		phaselist = self.dmesg[phase]['list']
		for devname in phaselist:
			dev = phaselist[devname]
			if(dev['end'] < 0):
				for p in self.sortedPhases():
					if self.dmesg[p]['end'] > dev['start']:
						dev['end'] = self.dmesg[p]['end']
						break
				sysvals.vprint('%s (%s): callback didnt return' % (devname, phase))
	def deviceFilter(self, devicefilter):
		for phase in self.sortedPhases():
			list = self.dmesg[phase]['list']
			rmlist = []
			for name in list:
				keep = False
				for filter in devicefilter:
					if filter in name or \
						('drv' in list[name] and filter in list[name]['drv']):
						keep = True
				if not keep:
					rmlist.append(name)
			for name in rmlist:
				del list[name]
	def fixupInitcallsThatDidntReturn(self):
		
		for phase in self.sortedPhases():
			self.fixupInitcalls(phase)
	def phaseOverlap(self, phases):
		rmgroups = []
		newgroup = []
		for group in self.devicegroups:
			for phase in phases:
				if phase not in group:
					continue
				for p in group:
					if p not in newgroup:
						newgroup.append(p)
				if group not in rmgroups:
					rmgroups.append(group)
		for group in rmgroups:
			self.devicegroups.remove(group)
		self.devicegroups.append(newgroup)
	def newActionGlobal(self, name, start, end, pid=-1, color=''):
		
		phases = self.sortedPhases()
		targetphase = 'none'
		htmlclass = ''
		overlap = 0.0
		myphases = []
		for phase in phases:
			pstart = self.dmesg[phase]['start']
			pend = self.dmesg[phase]['end']
			
			o = max(0, min(end, pend) - max(start, pstart))
			if o > 0:
				myphases.append(phase)
			
			if o > overlap:
				if overlap > 0 and phase == 'post_resume':
					continue
				targetphase = phase
				overlap = o
		
		if targetphase == 'none':
			p0start = self.dmesg[phases[0]]['start']
			if start <= p0start:
				targetphase = phases[0]
			else:
				targetphase = phases[-1]
		if pid == -2:
			htmlclass = ' bg'
		elif pid == -3:
			htmlclass = ' ps'
		if len(myphases) > 1:
			htmlclass = ' bg'
			self.phaseOverlap(myphases)
		if targetphase in phases:
			newname = self.newAction(targetphase, name, pid, '', start, end, '', htmlclass, color)
			return (targetphase, newname)
		return False
	def newAction(self, phase, name, pid, parent, start, end, drv, htmlclass='', color=''):
		
		self.html_device_id += 1
		devid = '%s%d' % (self.idstr, self.html_device_id)
		list = self.dmesg[phase]['list']
		length = -1.0
		if(start >= 0 and end >= 0):
			length = end - start
		if pid == -2:
			i = 2
			origname = name
			while(name in list):
				name = '%s[%d]' % (origname, i)
				i += 1
		list[name] = {'name': name, 'start': start, 'end': end, 'pid': pid,
			'par': parent, 'length': length, 'row': 0, 'id': devid, 'drv': drv }
		if htmlclass:
			list[name]['htmlclass'] = htmlclass
		if color:
			list[name]['color'] = color
		return name
	def deviceChildren(self, devname, phase):
		devlist = []
		list = self.dmesg[phase]['list']
		for child in list:
			if(list[child]['par'] == devname):
				devlist.append(child)
		return devlist
	def maxDeviceNameSize(self, phase):
		size = 0
		for name in self.dmesg[phase]['list']:
			if len(name) > size:
				size = len(name)
		return size
	def printDetails(self):
		sysvals.vprint('Timeline Details:')
		sysvals.vprint('          test start: %f' % self.start)
		sysvals.vprint('kernel suspend start: %f' % self.tKernSus)
		tS = tR = False
		for phase in self.sortedPhases():
			devlist = self.dmesg[phase]['list']
			dc, ps, pe = len(devlist), self.dmesg[phase]['start'], self.dmesg[phase]['end']
			if not tS and ps >= self.tSuspended:
				sysvals.vprint('   machine suspended: %f' % self.tSuspended)
				tS = True
			if not tR and ps >= self.tResumed:
				sysvals.vprint('     machine resumed: %f' % self.tResumed)
				tR = True
			sysvals.vprint('%20s: %f - %f (%d devices)' % (phase, ps, pe, dc))
			if sysvals.devdump:
				sysvals.vprint(''.join('-' for i in range(80)))
				maxname = '%d' % self.maxDeviceNameSize(phase)
				fmt = '%3d) %'+maxname+'s - %f - %f'
				c = 1
				for name in sorted(devlist):
					s = devlist[name]['start']
					e = devlist[name]['end']
					sysvals.vprint(fmt % (c, name, s, e))
					c += 1
				sysvals.vprint(''.join('-' for i in range(80)))
		sysvals.vprint('   kernel resume end: %f' % self.tKernRes)
		sysvals.vprint('            test end: %f' % self.end)
	def deviceChildrenAllPhases(self, devname):
		devlist = []
		for phase in self.sortedPhases():
			list = self.deviceChildren(devname, phase)
			for dev in sorted(list):
				if dev not in devlist:
					devlist.append(dev)
		return devlist
	def masterTopology(self, name, list, depth):
		node = DeviceNode(name, depth)
		for cname in list:
			
			if name == cname:
				continue
			clist = self.deviceChildrenAllPhases(cname)
			cnode = self.masterTopology(cname, clist, depth+1)
			node.children.append(cnode)
		return node
	def printTopology(self, node):
		html = ''
		if node.name:
			info = ''
			drv = ''
			for phase in self.sortedPhases():
				list = self.dmesg[phase]['list']
				if node.name in list:
					s = list[node.name]['start']
					e = list[node.name]['end']
					if list[node.name]['drv']:
						drv = ' {'+list[node.name]['drv']+'}'
					info += ('<li>%s: %.3fms</li>' % (phase, (e-s)*1000))
			html += '<li><b>'+node.name+drv+'</b>'
			if info:
				html += '<ul>'+info+'</ul>'
			html += '</li>'
		if len(node.children) > 0:
			html += '<ul>'
			for cnode in node.children:
				html += self.printTopology(cnode)
			html += '</ul>'
		return html
	def rootDeviceList(self):
		
		real = []
		for phase in self.sortedPhases():
			list = self.dmesg[phase]['list']
			for dev in sorted(list):
				if list[dev]['pid'] >= 0 and dev not in real:
					real.append(dev)
		
		rootlist = []
		for phase in self.sortedPhases():
			list = self.dmesg[phase]['list']
			for dev in sorted(list):
				pdev = list[dev]['par']
				pid = list[dev]['pid']
				if(pid < 0 or re.match('[0-9]*-[0-9]*\.[0-9]*[\.0-9]*\:[\.0-9]*$', pdev)):
					continue
				if pdev and pdev not in real and pdev not in rootlist:
					rootlist.append(pdev)
		return rootlist
	def deviceTopology(self):
		rootlist = self.rootDeviceList()
		master = self.masterTopology('', rootlist, 0)
		return self.printTopology(master)
	def selectTimelineDevices(self, widfmt, tTotal, mindevlen):
		
		self.tdevlist = dict()
		for phase in self.dmesg:
			devlist = []
			list = self.dmesg[phase]['list']
			for dev in list:
				length = (list[dev]['end'] - list[dev]['start']) * 1000
				width = widfmt % (((list[dev]['end']-list[dev]['start'])*100)/tTotal)
				if width != '0.000000' and length >= mindevlen:
					devlist.append(dev)
			self.tdevlist[phase] = devlist
	def addHorizontalDivider(self, devname, devend):
		phase = 'suspend_prepare'
		self.newAction(phase, devname, -2, '', \
			self.start, devend, '', ' sec', '')
		if phase not in self.tdevlist:
			self.tdevlist[phase] = []
		self.tdevlist[phase].append(devname)
		d = DevItem(0, phase, self.dmesg[phase]['list'][devname])
		return d
	def addProcessUsageEvent(self, name, times):
		
		maxC = 0
		tlast = 0
		start = -1
		end = -1
		for t in sorted(times):
			if tlast == 0:
				tlast = t
				continue
			if name in self.pstl[t]:
				if start == -1 or tlast < start:
					start = tlast
				if end == -1 or t > end:
					end = t
			tlast = t
		if start == -1 or end == -1:
			return 0
		
		out = self.newActionGlobal(name, start, end, -3)
		if not out:
			return 0
		phase, devname = out
		dev = self.dmesg[phase]['list'][devname]
		
		tlast = 0
		clast = 0
		cpuexec = dict()
		for t in sorted(times):
			if tlast == 0 or t <= start or t > end:
				tlast = t
				continue
			list = self.pstl[t]
			c = 0
			if name in list:
				c = list[name]
			if c > maxC:
				maxC = c
			if c != clast:
				key = (tlast, t)
				cpuexec[key] = c
				tlast = t
				clast = c
		dev['cpuexec'] = cpuexec
		return maxC
	def createProcessUsageEvents(self):
		
		proclist = []
		for t in sorted(self.pstl):
			pslist = self.pstl[t]
			for ps in sorted(pslist):
				if ps not in proclist:
					proclist.append(ps)
		
		tsus = []
		tres = []
		for t in sorted(self.pstl):
			if t < self.tSuspended:
				tsus.append(t)
			else:
				tres.append(t)
		
		if len(proclist) > 0:
			sysvals.vprint('Process Execution:')
		for ps in proclist:
			c = self.addProcessUsageEvent(ps, tsus)
			if c > 0:
				sysvals.vprint('%25s (sus): %d' % (ps, c))
			c = self.addProcessUsageEvent(ps, tres)
			if c > 0:
				sysvals.vprint('%25s (res): %d' % (ps, c))
	def handleEndMarker(self, time, msg=''):
		dm = self.dmesg
		self.setEnd(time, msg)
		self.initDevicegroups()
		
		if 'suspend_prepare' in dm and dm['suspend_prepare']['end'] < 0:
			dm['suspend_prepare']['end'] = time
		
		if 'resume_machine' in dm and dm['resume_machine']['end'] < 0:
			np = self.nextPhase('resume_machine', 1)
			if np:
				dm['resume_machine']['end'] = dm[np]['start']
		
		if self.tKernRes == 0.0:
			self.tKernRes = time
		
		if self.tKernSus == 0.0:
			self.tKernSus = time
		
		if 'resume_complete' in dm:
			dm['resume_complete']['end'] = time
	def debugPrint(self):
		for p in self.sortedPhases():
			list = self.dmesg[p]['list']
			for devname in sorted(list):
				dev = list[devname]
				if 'ftrace' in dev:
					dev['ftrace'].debugPrint(' [%s]' % devname)




class DevFunction:
	def __init__(self, name, args, caller, ret, start, end, u, proc, pid, color):
		self.row = 0
		self.count = 1
		self.name = name
		self.args = args
		self.caller = caller
		self.ret = ret
		self.time = start
		self.length = end - start
		self.end = end
		self.ubiquitous = u
		self.proc = proc
		self.pid = pid
		self.color = color
	def title(self):
		cnt = ''
		if self.count > 1:
			cnt = '(x%d)' % self.count
		l = '%0.3fms' % (self.length * 1000)
		if self.ubiquitous:
			title = '%s(%s)%s <- %s, %s(%s)' % \
				(self.name, self.args, cnt, self.caller, self.ret, l)
		else:
			title = '%s(%s) %s%s(%s)' % (self.name, self.args, self.ret, cnt, l)
		return title.replace('"', '')
	def text(self):
		if self.count > 1:
			text = '%s(x%d)' % (self.name, self.count)
		else:
			text = self.name
		return text
	def repeat(self, tgt):
		
		dt = self.time - tgt.end
		
		if tgt.caller == self.caller and \
			tgt.name == self.name and tgt.args == self.args and \
			tgt.proc == self.proc and tgt.pid == self.pid and \
			tgt.ret == self.ret and dt >= 0 and \
			dt <= sysvals.callloopmaxgap and \
			self.length < sysvals.callloopmaxlen:
			return True
		return False





"  dpm_run_callback() {"
"  }"
" dpm_run_callback();"




class FTraceLine:
	def __init__(self, t, m='', d=''):
		self.length = 0.0
		self.fcall = False
		self.freturn = False
		self.fevent = False
		self.fkprobe = False
		self.depth = 0
		self.name = ''
		self.type = ''
		self.time = float(t)
		if not m and not d:
			return
		
		if(d == 'traceevent' or re.match('^ *\/\* *(?P<msg>.*) \*\/ *$', m)):
			if(d == 'traceevent'):
				
				msg = m
			else:
				
				em = re.match('^ *\/\* *(?P<msg>.*) \*\/ *$', m)
				msg = em.group('msg')

			emm = re.match('^(?P<call>.*?): (?P<msg>.*)', msg)
			if(emm):
				self.name = emm.group('msg')
				self.type = emm.group('call')
			else:
				self.name = msg
			km = re.match('^(?P<n>.*)_cal$', self.type)
			if km:
				self.fcall = True
				self.fkprobe = True
				self.type = km.group('n')
				return
			km = re.match('^(?P<n>.*)_ret$', self.type)
			if km:
				self.freturn = True
				self.fkprobe = True
				self.type = km.group('n')
				return
			self.fevent = True
			return
		
		if(d):
			self.length = float(d)/1000000
		
		match = re.match('^(?P<d> *)(?P<o>.*)$', m)
		if(not match):
			return
		self.depth = self.getDepth(match.group('d'))
		m = match.group('o')
		
		if(m[0] == '}'):
			self.freturn = True
			if(len(m) > 1):
				
				match = re.match('^} *\/\* *(?P<n>.*) *\*\/$', m)
				if(match):
					self.name = match.group('n').strip()
		
		else:
			self.fcall = True
			
			if(m[-1] == '{'):
				match = re.match('^(?P<n>.*) *\(.*', m)
				if(match):
					self.name = match.group('n').strip()
			
			elif(m[-1] == ';'):
				self.freturn = True
				match = re.match('^(?P<n>.*) *\(.*', m)
				if(match):
					self.name = match.group('n').strip()
			
			else:
				self.name = m
	def isCall(self):
		return self.fcall and not self.freturn
	def isReturn(self):
		return self.freturn and not self.fcall
	def isLeaf(self):
		return self.fcall and self.freturn
	def getDepth(self, str):
		return len(str)/2
	def debugPrint(self, info=''):
		if self.isLeaf():
			pprint(' -- %12.6f (depth=%02d): %s(); (%.3f us) %s' % (self.time, \
				self.depth, self.name, self.length*1000000, info))
		elif self.freturn:
			pprint(' -- %12.6f (depth=%02d): %s} (%.3f us) %s' % (self.time, \
				self.depth, self.name, self.length*1000000, info))
		else:
			pprint(' -- %12.6f (depth=%02d): %s() { (%.3f us) %s' % (self.time, \
				self.depth, self.name, self.length*1000000, info))
	def startMarker(self):
		
		if not self.fevent:
			return False
		if sysvals.usetracemarkers:
			if(self.name.startswith('SUSPEND START')):
				return True
			return False
		else:
			if(self.type == 'suspend_resume' and
				re.match('suspend_enter\[.*\] begin', self.name)):
				return True
			return False
	def endMarker(self):
		
		if not self.fevent:
			return False
		if sysvals.usetracemarkers:
			if(self.name.startswith('RESUME COMPLETE')):
				return True
			return False
		else:
			if(self.type == 'suspend_resume' and
				re.match('thaw_processes\[.*\] end', self.name)):
				return True
			return False







class FTraceCallGraph:
	vfname = 'missing_function_name'
	def __init__(self, pid, sv):
		self.id = ''
		self.invalid = False
		self.name = ''
		self.partial = False
		self.ignore = False
		self.start = -1.0
		self.end = -1.0
		self.list = []
		self.depth = 0
		self.pid = pid
		self.sv = sv
	def addLine(self, line):
		
		if(self.invalid):
			if(line.depth == 0 and line.freturn):
				return 1
			return 0
		
		if(self.depth < 0):
			self.invalidate(line)
			return 0
		
		if self.ignore:
			if line.depth > self.depth:
				return 0
			else:
				self.list[-1].freturn = True
				self.list[-1].length = line.time - self.list[-1].time
				self.ignore = False
				
				if line.depth == self.depth and line.isReturn():
					if line.depth == 0:
						self.end = line.time
						return 1
					return 0
		
		prelinedep = line.depth
		if line.isReturn():
			prelinedep += 1
		last = 0
		lasttime = line.time
		if len(self.list) > 0:
			last = self.list[-1]
			lasttime = last.time
			if last.isLeaf():
				lasttime += last.length
		
		mismatch = prelinedep - self.depth
		warning = self.sv.verbose and abs(mismatch) > 1
		info = []
		if mismatch < 0:
			idx = 0
			
			while prelinedep < self.depth:
				self.depth -= 1
				if idx == 0 and last and last.isCall():
					
					last.depth = self.depth
					last.freturn = True
					last.length = line.time - last.time
					if warning:
						info.append(('[make leaf]', last))
				else:
					vline = FTraceLine(lasttime)
					vline.depth = self.depth
					vline.name = self.vfname
					vline.freturn = True
					self.list.append(vline)
					if warning:
						if idx == 0:
							info.append(('', last))
						info.append(('[add return]', vline))
				idx += 1
			if warning:
				info.append(('', line))
		
		elif mismatch > 0:
			idx = 0
			if warning:
				info.append(('', last))
			
			while prelinedep > self.depth:
				if idx == 0 and line.isReturn():
					
					line.fcall = True
					prelinedep -= 1
					if warning:
						info.append(('[make leaf]', line))
				else:
					vline = FTraceLine(lasttime)
					vline.depth = self.depth
					vline.name = self.vfname
					vline.fcall = True
					self.list.append(vline)
					self.depth += 1
					if not last:
						self.start = vline.time
					if warning:
						info.append(('[add call]', vline))
				idx += 1
			if warning and ('[make leaf]', line) not in info:
				info.append(('', line))
		if warning:
			pprint('WARNING: ftrace data missing, corrections made:')
			for i in info:
				t, obj = i
				if obj:
					obj.debugPrint(t)
		
		skipadd = False
		md = self.sv.max_graph_depth
		if line.isCall():
			
			if (md and self.depth >= md - 1) or (line.name in self.sv.cgblacklist):
				self.ignore = True
			else:
				self.depth += 1
		elif line.isReturn():
			self.depth -= 1
			
			if (last and last.isCall() and last.depth == line.depth) or \
				(md and last and last.depth >= md) or \
				(line.name in self.sv.cgblacklist):
				while len(self.list) > 0 and self.list[-1].depth > line.depth:
					self.list.pop(-1)
				if len(self.list) == 0:
					self.invalid = True
					return 1
				self.list[-1].freturn = True
				self.list[-1].length = line.time - self.list[-1].time
				self.list[-1].name = line.name
				skipadd = True
		if len(self.list) < 1:
			self.start = line.time
		
		res = 1
		if mismatch < 0 and self.list[-1].depth == 0 and self.list[-1].freturn:
			line = self.list[-1]
			skipadd = True
			res = -1
		if not skipadd:
			self.list.append(line)
		if(line.depth == 0 and line.freturn):
			if(self.start < 0):
				self.start = line.time
			self.end = line.time
			if line.fcall:
				self.end += line.length
			if self.list[0].name == self.vfname:
				self.invalid = True
			if res == -1:
				self.partial = True
			return res
		return 0
	def invalidate(self, line):
		if(len(self.list) > 0):
			first = self.list[0]
			self.list = []
			self.list.append(first)
		self.invalid = True
		id = 'task %s' % (self.pid)
		window = '(%f - %f)' % (self.start, line.time)
		if(self.depth < 0):
			pprint('Data misalignment for '+id+\
				' (buffer overflow), ignoring this callback')
		else:
			pprint('Too much data for '+id+\
				' '+window+', ignoring this callback')
	def slice(self, dev):
		minicg = FTraceCallGraph(dev['pid'], self.sv)
		minicg.name = self.name
		mydepth = -1
		good = False
		for l in self.list:
			if(l.time < dev['start'] or l.time > dev['end']):
				continue
			if mydepth < 0:
				if l.name == 'mutex_lock' and l.freturn:
					mydepth = l.depth
				continue
			elif l.depth == mydepth and l.name == 'mutex_unlock' and l.fcall:
				good = True
				break
			l.depth -= mydepth
			minicg.addLine(l)
		if not good or len(minicg.list) < 1:
			return 0
		return minicg
	def repair(self, enddepth):
		
		fixed = False
		last = self.list[-1]
		for i in reversed(range(enddepth)):
			t = FTraceLine(last.time)
			t.depth = i
			t.freturn = True
			fixed = self.addLine(t)
			if fixed != 0:
				self.end = last.time
				return True
		return False
	def postProcess(self):
		if len(self.list) > 0:
			self.name = self.list[0].name
		stack = dict()
		cnt = 0
		last = 0
		for l in self.list:
			
			
			if last and last.isLeaf():
				if last.length > l.time - last.time:
					last.length = l.time - last.time
			if l.isCall():
				stack[l.depth] = l
				cnt += 1
			elif l.isReturn():
				if(l.depth not in stack):
					if self.sv.verbose:
						pprint('Post Process Error: Depth missing')
						l.debugPrint()
					return False
				
				cl = stack[l.depth]
				cl.length = l.time - cl.time
				if cl.name == self.vfname:
					cl.name = l.name
				stack.pop(l.depth)
				l.length = 0
				cnt -= 1
			last = l
		if(cnt == 0):
			
			return True
		elif(cnt < 0):
			if self.sv.verbose:
				pprint('Post Process Error: Depth is less than 0')
			return False
		
		return self.repair(cnt)
	def deviceMatch(self, pid, data):
		found = ''
		
		borderphase = {
			'dpm_prepare': 'suspend_prepare',
			'dpm_complete': 'resume_complete'
		}
		if(self.name in borderphase):
			p = borderphase[self.name]
			list = data.dmesg[p]['list']
			for devname in list:
				dev = list[devname]
				if(pid == dev['pid'] and
					self.start <= dev['start'] and
					self.end >= dev['end']):
					cg = self.slice(dev)
					if cg:
						dev['ftrace'] = cg
					found = devname
			return found
		for p in data.sortedPhases():
			if(data.dmesg[p]['start'] <= self.start and
				self.start <= data.dmesg[p]['end']):
				list = data.dmesg[p]['list']
				for devname in sorted(list, key=lambda k:list[k]['start']):
					dev = list[devname]
					if(pid == dev['pid'] and
						self.start <= dev['start'] and
						self.end >= dev['end']):
						dev['ftrace'] = self
						found = devname
						break
				break
		return found
	def newActionFromFunction(self, data):
		name = self.name
		if name in ['dpm_run_callback', 'dpm_prepare', 'dpm_complete']:
			return
		fs = self.start
		fe = self.end
		if fs < data.start or fe > data.end:
			return
		phase = ''
		for p in data.sortedPhases():
			if(data.dmesg[p]['start'] <= self.start and
				self.start < data.dmesg[p]['end']):
				phase = p
				break
		if not phase:
			return
		out = data.newActionGlobal(name, fs, fe, -2)
		if out:
			phase, myname = out
			data.dmesg[phase]['list'][myname]['ftrace'] = self
	def debugPrint(self, info=''):
		pprint('%s pid=%d [%f - %f] %.3f us' % \
			(self.name, self.pid, self.start, self.end,
			(self.end - self.start)*1000000))
		for l in self.list:
			if l.isLeaf():
				pprint('%f (%02d): %s(); (%.3f us)%s' % (l.time, \
					l.depth, l.name, l.length*1000000, info))
			elif l.freturn:
				pprint('%f (%02d): %s} (%.3f us)%s' % (l.time, \
					l.depth, l.name, l.length*1000000, info))
			else:
				pprint('%f (%02d): %s() { (%.3f us)%s' % (l.time, \
					l.depth, l.name, l.length*1000000, info))
		pprint(' ')

class DevItem:
	def __init__(self, test, phase, dev):
		self.test = test
		self.phase = phase
		self.dev = dev
	def isa(self, cls):
		if 'htmlclass' in self.dev and cls in self.dev['htmlclass']:
			return True
		return False





class Timeline:
	html_tblock = '<div id="block{0}" class="tblock" style="left:{1}%;width:{2}%;"><div class="tback" style="height:{3}px"></div>\n'
	html_device = '<div id="{0}" title="{1}" class="thread{7}" style="left:{2}%;top:{3}px;height:{4}px;width:{5}%;{8}">{6}</div>\n'
	html_phase = '<div class="phase" style="left:{0}%;width:{1}%;top:{2}px;height:{3}px;background:{4}">{5}</div>\n'
	html_phaselet = '<div id="{0}" class="phaselet" style="left:{1}%;width:{2}%;background:{3}"></div>\n'
	html_legend = '<div id="p{3}" class="square" style="left:{0}%;background:{1}">&nbsp;{2}</div>\n'
	def __init__(self, rowheight, scaleheight):
		self.html = ''
		self.height = 0  
		self.scaleH = scaleheight 
		self.rowH = rowheight     
		self.bodyH = 0   
		self.rows = 0    
		self.rowlines = dict()
		self.rowheight = dict()
	def createHeader(self, sv, stamp):
		if(not stamp['time']):
			return
		self.html += '<div class="version"><a href="https://01.org/pm-graph">%s v%s</a></div>' \
			% (sv.title, sv.version)
		if sv.logmsg and sv.testlog:
			self.html += '<button id="showtest" class="logbtn btnfmt">log</button>'
		if sv.dmesglog:
			self.html += '<button id="showdmesg" class="logbtn btnfmt">dmesg</button>'
		if sv.ftracelog:
			self.html += '<button id="showftrace" class="logbtn btnfmt">ftrace</button>'
		headline_stamp = '<div class="stamp">{0} {1} {2} {3}</div>\n'
		self.html += headline_stamp.format(stamp['host'], stamp['kernel'],
			stamp['mode'], stamp['time'])
		if 'man' in stamp and 'plat' in stamp and 'cpu' in stamp and \
			stamp['man'] and stamp['plat'] and stamp['cpu']:
			headline_sysinfo = '<div class="stamp sysinfo">{0} {1} <i>with</i> {2}</div>\n'
			self.html += headline_sysinfo.format(stamp['man'], stamp['plat'], stamp['cpu'])

	
	
	
	
	
	
	
	def getDeviceRows(self, rawlist):
		
		sortdict = dict()
		for item in rawlist:
			item.row = -1
			sortdict[item] = item.length
		sortlist = sorted(sortdict, key=sortdict.get, reverse=True)
		remaining = len(sortlist)
		rowdata = dict()
		row = 1
		
		while(remaining > 0):
			if(row not in rowdata):
				rowdata[row] = []
			for i in sortlist:
				if(i.row >= 0):
					continue
				s = i.time
				e = i.time + i.length
				valid = True
				for ritem in rowdata[row]:
					rs = ritem.time
					re = ritem.time + ritem.length
					if(not (((s <= rs) and (e <= rs)) or
						((s >= re) and (e >= re)))):
						valid = False
						break
				if(valid):
					rowdata[row].append(i)
					i.row = row
					remaining -= 1
			row += 1
		return row
	
	
	
	
	
	
	
	
	def getPhaseRows(self, devlist, row=0, sortby='length'):
		
		remaining = len(devlist)
		rowdata = dict()
		sortdict = dict()
		myphases = []
		
		for item in devlist:
			dev = item.dev
			tp = (item.test, item.phase)
			if tp not in myphases:
				myphases.append(tp)
			dev['row'] = -1
			if sortby == 'start':
				
				sortdict[item] = (-1*float(dev['start']), float(dev['end']) - float(dev['start']))
			else:
				
				sortdict[item] = (float(dev['end']) - float(dev['start']), item.dev['name'])
			if 'src' in dev:
				dev['devrows'] = self.getDeviceRows(dev['src'])
		
		sortlist = sorted(sortdict, key=sortdict.get, reverse=True)
		orderedlist = []
		for item in sortlist:
			if item.dev['pid'] == -2:
				orderedlist.append(item)
		for item in sortlist:
			if item not in orderedlist:
				orderedlist.append(item)
		
		while(remaining > 0):
			rowheight = 1
			if(row not in rowdata):
				rowdata[row] = []
			for item in orderedlist:
				dev = item.dev
				if(dev['row'] < 0):
					s = dev['start']
					e = dev['end']
					valid = True
					for ritem in rowdata[row]:
						rs = ritem.dev['start']
						re = ritem.dev['end']
						if(not (((s <= rs) and (e <= rs)) or
							((s >= re) and (e >= re)))):
							valid = False
							break
					if(valid):
						rowdata[row].append(item)
						dev['row'] = row
						remaining -= 1
						if 'devrows' in dev and dev['devrows'] > rowheight:
							rowheight = dev['devrows']
			for t, p in myphases:
				if t not in self.rowlines or t not in self.rowheight:
					self.rowlines[t] = dict()
					self.rowheight[t] = dict()
				if p not in self.rowlines[t] or p not in self.rowheight[t]:
					self.rowlines[t][p] = dict()
					self.rowheight[t][p] = dict()
				rh = self.rowH
				
				if len(rowdata[row]) == 1 and \
					'htmlclass' in rowdata[row][0].dev and \
					'sec' in rowdata[row][0].dev['htmlclass']:
					rh = 15
				self.rowlines[t][p][row] = rowheight
				self.rowheight[t][p][row] = rowheight * rh
			row += 1
		if(row > self.rows):
			self.rows = int(row)
		return row
	def phaseRowHeight(self, test, phase, row):
		return self.rowheight[test][phase][row]
	def phaseRowTop(self, test, phase, row):
		top = 0
		for i in sorted(self.rowheight[test][phase]):
			if i >= row:
				break
			top += self.rowheight[test][phase][i]
		return top
	def calcTotalRows(self):
		
		maxrows = 0
		standardphases = []
		for t in self.rowlines:
			for p in self.rowlines[t]:
				total = 0
				for i in sorted(self.rowlines[t][p]):
					total += self.rowlines[t][p][i]
				if total > maxrows:
					maxrows = total
				if total == len(self.rowlines[t][p]):
					standardphases.append((t, p))
		self.height = self.scaleH + (maxrows*self.rowH)
		self.bodyH = self.height - self.scaleH
		
		for t, p in standardphases:
			for i in sorted(self.rowheight[t][p]):
				self.rowheight[t][p][i] = float(self.bodyH)/len(self.rowlines[t][p])
	def createZoomBox(self, mode='command', testcount=1):
		
		html_zoombox = '<center><button id="zoomin">ZOOM IN +</button><button id="zoomout">ZOOM OUT -</button><button id="zoomdef">ZOOM 1:1</button></center>\n'
		html_timeline = '<div id="dmesgzoombox" class="zoombox">\n<div id="{0}" class="timeline" style="height:{1}px">\n'
		html_devlist1 = '<button id="devlist1" class="devlist" style="float:left;">Device Detail{0}</button>'
		html_devlist2 = '<button id="devlist2" class="devlist" style="float:right;">Device Detail2</button>\n'
		if mode != 'command':
			if testcount > 1:
				self.html += html_devlist2
				self.html += html_devlist1.format('1')
			else:
				self.html += html_devlist1.format('')
		self.html += html_zoombox
		self.html += html_timeline.format('dmesg', self.height)
	
	
	
	
	
	
	
	
	
	
	def createTimeScale(self, m0, mMax, tTotal, mode):
		timescale = '<div class="t" style="right:{0}%">{1}</div>\n'
		rline = '<div class="t" style="left:0;border-left:1px solid black;border-right:0;">{0}</div>\n'
		output = '<div class="timescale">\n'
		
		mTotal = mMax - m0
		tS = 0.1
		if(tTotal <= 0):
			return output+'</div>\n'
		if(tTotal > 4):
			tS = 1
		divTotal = int(mTotal/tS) + 1
		divEdge = (mTotal - tS*(divTotal-1))*100/mTotal
		for i in range(divTotal):
			htmlline = ''
			if(mode == 'suspend'):
				pos = '%0.3f' % (100 - ((float(i)*tS*100)/mTotal) - divEdge)
				val = '%0.fms' % (float(i-divTotal+1)*tS*1000)
				if(i == divTotal - 1):
					val = mode
				htmlline = timescale.format(pos, val)
			else:
				pos = '%0.3f' % (100 - ((float(i)*tS*100)/mTotal))
				val = '%0.fms' % (float(i)*tS*1000)
				htmlline = timescale.format(pos, val)
				if(i == 0):
					htmlline = rline.format(mode)
			output += htmlline
		self.html += output+'</div>\n'




class TestProps:
	stampfmt = '
				'(?P<H>[0-9]{2})(?P<M>[0-9]{2})(?P<S>[0-9]{2})'+\
				' (?P<host>.*) (?P<mode>.*) (?P<kernel>.*)$'
	wififmt    = '^
	tstatfmt   = '^
	testerrfmt = '^
	sysinfofmt = '^
	cmdlinefmt = '^
	devpropfmt = '
	pinfofmt   = '
	tracertypefmt = '
	firmwarefmt = '
	procexecfmt = 'ps - (?P<ps>.*)$'
	ftrace_line_fmt_fg = \
		'^ *(?P<time>[0-9\.]*) *\| *(?P<cpu>[0-9]*)\)'+\
		' *(?P<proc>.*)-(?P<pid>[0-9]*) *\|'+\
		'[ +!
	ftrace_line_fmt_nop = \
		' *(?P<proc>.*)-(?P<pid>[0-9]*) *\[(?P<cpu>[0-9]*)\] *'+\
		'(?P<flags>.{4}) *(?P<time>[0-9\.]*): *'+\
		'(?P<msg>.*)'
	def __init__(self):
		self.stamp = ''
		self.sysinfo = ''
		self.cmdline = ''
		self.testerror = []
		self.turbostat = []
		self.wifi = []
		self.fwdata = []
		self.ftrace_line_fmt = self.ftrace_line_fmt_nop
		self.cgformat = False
		self.data = 0
		self.ktemp = dict()
	def setTracerType(self, tracer):
		if(tracer == 'function_graph'):
			self.cgformat = True
			self.ftrace_line_fmt = self.ftrace_line_fmt_fg
		elif(tracer == 'nop'):
			self.ftrace_line_fmt = self.ftrace_line_fmt_nop
		else:
			doError('Invalid tracer format: [%s]' % tracer)
	def stampInfo(self, line):
		if re.match(self.stampfmt, line):
			self.stamp = line
			return True
		elif re.match(self.sysinfofmt, line):
			self.sysinfo = line
			return True
		elif re.match(self.cmdlinefmt, line):
			self.cmdline = line
			return True
		elif re.match(self.tstatfmt, line):
			self.turbostat.append(line)
			return True
		elif re.match(self.wififmt, line):
			self.wifi.append(line)
			return True
		elif re.match(self.testerrfmt, line):
			self.testerror.append(line)
			return True
		elif re.match(self.firmwarefmt, line):
			self.fwdata.append(line)
			return True
		return False
	def parseStamp(self, data, sv):
		
		m = re.match(self.stampfmt, self.stamp)
		if not self.stamp or not m:
			doError('data does not include the expected stamp')
		data.stamp = {'time': '', 'host': '', 'mode': ''}
		dt = datetime(int(m.group('y'))+2000, int(m.group('m')),
			int(m.group('d')), int(m.group('H')), int(m.group('M')),
			int(m.group('S')))
		data.stamp['time'] = dt.strftime('%B %d %Y, %I:%M:%S %p')
		data.stamp['host'] = m.group('host')
		data.stamp['mode'] = m.group('mode')
		data.stamp['kernel'] = m.group('kernel')
		if re.match(self.sysinfofmt, self.sysinfo):
			for f in self.sysinfo.split('|'):
				if '
					continue
				tmp = f.strip().split(':', 1)
				key = tmp[0]
				val = tmp[1]
				data.stamp[key] = val
		sv.hostname = data.stamp['host']
		sv.suspendmode = data.stamp['mode']
		if sv.suspendmode == 'command' and sv.ftracefile != '':
			modes = ['on', 'freeze', 'standby', 'mem', 'disk']
			fp = sysvals.openlog(sv.ftracefile, 'r')
			for line in fp:
				m = re.match('.* machine_suspend\[(?P<mode>.*)\]', line)
				if m and m.group('mode') in ['1', '2', '3', '4']:
					sv.suspendmode = modes[int(m.group('mode'))]
					data.stamp['mode'] = sv.suspendmode
					break
			fp.close()
		m = re.match(self.cmdlinefmt, self.cmdline)
		if m:
			sv.cmdline = m.group('cmd')
		if not sv.stamp:
			sv.stamp = data.stamp
		
		if sv.suspendmode == 'mem' and len(self.fwdata) > data.testnumber:
			m = re.match(self.firmwarefmt, self.fwdata[data.testnumber])
			if m:
				data.fwSuspend, data.fwResume = int(m.group('s')), int(m.group('r'))
				if(data.fwSuspend > 0 or data.fwResume > 0):
					data.fwValid = True
		
		if len(self.turbostat) > data.testnumber:
			m = re.match(self.tstatfmt, self.turbostat[data.testnumber])
			if m:
				data.turbostat = m.group('t')
		
		if len(self.wifi) > data.testnumber:
			m = re.match(self.wififmt, self.wifi[data.testnumber])
			if m:
				data.wifi = {'dev': m.group('d'), 'stat': m.group('s'),
					'time': float(m.group('t'))}
				data.stamp['wifi'] = m.group('d')
		
		if len(self.testerror) > data.testnumber:
			m = re.match(self.testerrfmt, self.testerror[data.testnumber])
			if m:
				data.enterfail = m.group('e')
	def devprops(self, data):
		props = dict()
		devlist = data.split(';')
		for dev in devlist:
			f = dev.split(',')
			if len(f) < 3:
				continue
			dev = f[0]
			props[dev] = DevProps()
			props[dev].altname = f[1]
			if int(f[2]):
				props[dev].isasync = True
			else:
				props[dev].isasync = False
		return props
	def parseDevprops(self, line, sv):
		idx = line.index(': ') + 2
		if idx >= len(line):
			return
		props = self.devprops(line[idx:])
		if sv.suspendmode == 'command' and 'testcommandstring' in props:
			sv.testcommand = props['testcommandstring'].altname
		sv.devprops = props
	def parsePlatformInfo(self, line, sv):
		m = re.match(self.pinfofmt, line)
		if not m:
			return
		name, info = m.group('val'), m.group('info')
		if name == 'devinfo':
			sv.devprops = self.devprops(sv.b64unzip(info))
			return
		elif name == 'testcmd':
			sv.testcommand = info
			return
		field = info.split('|')
		if len(field) < 2:
			return
		cmdline = field[0].strip()
		output = sv.b64unzip(field[1].strip())
		sv.platinfo.append([name, cmdline, output])





class TestRun:
	def __init__(self, dataobj):
		self.data = dataobj
		self.ftemp = dict()
		self.ttemp = dict()

class ProcessMonitor:
	def __init__(self):
		self.proclist = dict()
		self.running = False
	def procstat(self):
		c = ['cat /proc/[1-9]*/stat 2>/dev/null']
		process = Popen(c, shell=True, stdout=PIPE)
		running = dict()
		for line in process.stdout:
			data = ascii(line).split()
			pid = data[0]
			name = re.sub('[()]', '', data[1])
			user = int(data[13])
			kern = int(data[14])
			kjiff = ujiff = 0
			if pid not in self.proclist:
				self.proclist[pid] = {'name' : name, 'user' : user, 'kern' : kern}
			else:
				val = self.proclist[pid]
				ujiff = user - val['user']
				kjiff = kern - val['kern']
				val['user'] = user
				val['kern'] = kern
			if ujiff > 0 or kjiff > 0:
				running[pid] = ujiff + kjiff
		process.wait()
		out = ''
		for pid in running:
			jiffies = running[pid]
			val = self.proclist[pid]
			if out:
				out += ','
			out += '%s-%s %d' % (val['name'], pid, jiffies)
		return 'ps - '+out
	def processMonitor(self, tid):
		while self.running:
			out = self.procstat()
			if out:
				sysvals.fsetVal(out, 'trace_marker')
	def start(self):
		self.thread = Thread(target=self.processMonitor, args=(0,))
		self.running = True
		self.thread.start()
	def stop(self):
		self.running = False







def doesTraceLogHaveTraceEvents():
	kpcheck = ['_cal: (', '_ret: (']
	techeck = ['suspend_resume', 'device_pm_callback']
	tmcheck = ['SUSPEND START', 'RESUME COMPLETE']
	sysvals.usekprobes = False
	fp = sysvals.openlog(sysvals.ftracefile, 'r')
	for line in fp:
		
		if not sysvals.usekprobes:
			for i in kpcheck:
				if i in line:
					sysvals.usekprobes = True
		
		check = techeck[:]
		for i in techeck:
			if i in line:
				check.remove(i)
		techeck = check
		
		check = tmcheck[:]
		for i in tmcheck:
			if i in line:
				check.remove(i)
		tmcheck = check
	fp.close()
	sysvals.usetraceevents = True if len(techeck) < 2 else False
	sysvals.usetracemarkers = True if len(tmcheck) == 0 else False








def appendIncompleteTraceLog(testruns):
	
	testcnt = len(testruns)
	testidx = 0
	testrun = []
	for data in testruns:
		testrun.append(TestRun(data))

	
	sysvals.vprint('Analyzing the ftrace data (%s)...' % \
		os.path.basename(sysvals.ftracefile))
	tp = TestProps()
	tf = sysvals.openlog(sysvals.ftracefile, 'r')
	data = 0
	for line in tf:
		
		line = line.replace('\r\n', '')
		if tp.stampInfo(line):
			continue
		
		m = re.match(tp.tracertypefmt, line)
		if(m):
			tp.setTracerType(m.group('t'))
			continue
		
		if(re.match(tp.devpropfmt, line)):
			tp.parseDevprops(line, sysvals)
			continue
		
		if(re.match(tp.pinfofmt, line)):
			tp.parsePlatformInfo(line, sysvals)
			continue
		
		m = re.match(tp.ftrace_line_fmt, line)
		if(not m):
			continue
		
		m_time = m.group('time')
		m_pid = m.group('pid')
		m_msg = m.group('msg')
		if(tp.cgformat):
			m_param3 = m.group('dur')
		else:
			m_param3 = 'traceevent'
		if(m_time and m_pid and m_msg):
			t = FTraceLine(m_time, m_msg, m_param3)
			pid = int(m_pid)
		else:
			continue
		
		if(not t.fcall and not t.freturn and not t.fevent):
			continue
		
		if(t.startMarker()):
			data = testrun[testidx].data
			tp.parseStamp(data, sysvals)
			data.setStart(t.time, t.name)
			continue
		if(not data):
			continue
		
		if(t.endMarker()):
			data.setEnd(t.time, t.name)
			testidx += 1
			if(testidx >= testcnt):
				break
			continue
		
		if(t.fevent):
			continue
		
		elif sysvals.usecallgraph:
			
			if(pid not in testrun[testidx].ftemp):
				testrun[testidx].ftemp[pid] = []
				testrun[testidx].ftemp[pid].append(FTraceCallGraph(pid, sysvals))
			
			cg = testrun[testidx].ftemp[pid][-1]
			res = cg.addLine(t)
			if(res != 0):
				testrun[testidx].ftemp[pid].append(FTraceCallGraph(pid, sysvals))
			if(res == -1):
				testrun[testidx].ftemp[pid][-1].addLine(t)
	tf.close()

	for test in testrun:
		
		for pid in test.ftemp:
			for cg in test.ftemp[pid]:
				if len(cg.list) < 1 or cg.invalid or (cg.end - cg.start == 0):
					continue
				if(not cg.postProcess()):
					id = 'task %s cpu %s' % (pid, m.group('cpu'))
					sysvals.vprint('Sanity check failed for '+\
						id+', ignoring this callback')
					continue
				callstart = cg.start
				callend = cg.end
				for p in test.data.sortedPhases():
					if(test.data.dmesg[p]['start'] <= callstart and
						callstart <= test.data.dmesg[p]['end']):
						list = test.data.dmesg[p]['list']
						for devname in list:
							dev = list[devname]
							if(pid == dev['pid'] and
								callstart <= dev['start'] and
								callend >= dev['end']):
								dev['ftrace'] = cg
						break









def parseTraceLog(live=False):
	sysvals.vprint('Analyzing the ftrace data (%s)...' % \
		os.path.basename(sysvals.ftracefile))
	if(os.path.exists(sysvals.ftracefile) == False):
		doError('%s does not exist' % sysvals.ftracefile)
	if not live:
		sysvals.setupAllKprobes()
	ksuscalls = ['ksys_sync', 'pm_prepare_console']
	krescalls = ['pm_restore_console']
	tracewatch = ['irq_wakeup']
	if sysvals.usekprobes:
		tracewatch += ['sync_filesystems', 'freeze_processes', 'syscore_suspend',
			'syscore_resume', 'resume_console', 'thaw_processes', 'CPU_ON',
			'CPU_OFF', 'timekeeping_freeze', 'acpi_suspend']

	
	tp = TestProps()
	testruns = []
	testdata = []
	testrun = 0
	data, limbo = 0, True
	tf = sysvals.openlog(sysvals.ftracefile, 'r')
	phase = 'suspend_prepare'
	for line in tf:
		
		line = line.replace('\r\n', '')
		if tp.stampInfo(line):
			continue
		
		m = re.match(tp.tracertypefmt, line)
		if(m):
			tp.setTracerType(m.group('t'))
			continue
		
		if(re.match(tp.devpropfmt, line)):
			tp.parseDevprops(line, sysvals)
			continue
		
		if(re.match(tp.pinfofmt, line)):
			tp.parsePlatformInfo(line, sysvals)
			continue
		
		if line[0] == '
			continue
		
		m = re.match(tp.ftrace_line_fmt, line)
		if(not m):
			continue
		
		m_time = m.group('time')
		m_proc = m.group('proc')
		m_pid = m.group('pid')
		m_msg = m.group('msg')
		if(tp.cgformat):
			m_param3 = m.group('dur')
		else:
			m_param3 = 'traceevent'
		if(m_time and m_pid and m_msg):
			t = FTraceLine(m_time, m_msg, m_param3)
			pid = int(m_pid)
		else:
			continue
		
		if(not t.fcall and not t.freturn and not t.fevent):
			continue
		
		if(t.startMarker()):
			data, limbo = Data(len(testdata)), False
			testdata.append(data)
			testrun = TestRun(data)
			testruns.append(testrun)
			tp.parseStamp(data, sysvals)
			data.setStart(t.time, t.name)
			data.first_suspend_prepare = True
			phase = data.setPhase('suspend_prepare', t.time, True)
			continue
		if(not data or limbo):
			continue
		
		if t.type == 'tracing_mark_write':
			m = re.match(tp.procexecfmt, t.name)
			if(m):
				proclist = dict()
				for ps in m.group('ps').split(','):
					val = ps.split()
					if not val:
						continue
					name = val[0].replace('--', '-')
					proclist[name] = int(val[1])
				data.pstl[t.time] = proclist
				continue
		
		if(t.endMarker()):
			if data.tKernRes == 0:
				data.tKernRes = t.time
			data.handleEndMarker(t.time, t.name)
			if(not sysvals.usetracemarkers):
				
				
				if('thaw_processes' in testrun.ttemp and len(testrun.ttemp['thaw_processes']) > 0):
					
					testrun.ttemp['thaw_processes'][-1]['end'] = t.time
			limbo = True
			continue
		
		if(t.fevent):
			if(t.type == 'suspend_resume'):
				
				if(re.match('(?P<name>.*) begin$', t.name)):
					isbegin = True
				elif(re.match('(?P<name>.*) end$', t.name)):
					isbegin = False
				else:
					continue
				if '[' in t.name:
					m = re.match('(?P<name>.*)\[.*', t.name)
				else:
					m = re.match('(?P<name>.*) .*', t.name)
				name = m.group('name')
				
				if(name.split('[')[0] in tracewatch):
					continue
				
				
				if(re.match('suspend_enter\[.*', t.name)):
					if(isbegin and data.tKernSus == 0):
						data.tKernSus = t.time
					continue
				
				elif(re.match('dpm_prepare\[.*', t.name)):
					if isbegin and data.first_suspend_prepare:
						data.first_suspend_prepare = False
						if data.tKernSus == 0:
							data.tKernSus = t.time
						continue
					phase = data.setPhase('suspend_prepare', t.time, isbegin)
					continue
				
				elif(re.match('dpm_suspend\[.*', t.name)):
					phase = data.setPhase('suspend', t.time, isbegin)
					continue
				
				elif(re.match('dpm_suspend_late\[.*', t.name)):
					phase = data.setPhase('suspend_late', t.time, isbegin)
					continue
				
				elif(re.match('dpm_suspend_noirq\[.*', t.name)):
					phase = data.setPhase('suspend_noirq', t.time, isbegin)
					continue
				
				elif(re.match('machine_suspend\[.*', t.name)):
					if(isbegin):
						lp = data.lastPhase()
						if lp.startswith('resume_machine'):
							data.dmesg[lp]['end'] = t.time
						phase = data.setPhase('suspend_machine', data.dmesg[lp]['end'], True)
						data.setPhase(phase, t.time, False)
						if data.tSuspended == 0:
							data.tSuspended = t.time
					else:
						phase = data.setPhase('resume_machine', t.time, True)
						if(sysvals.suspendmode in ['mem', 'disk']):
							susp = phase.replace('resume', 'suspend')
							if susp in data.dmesg:
								data.dmesg[susp]['end'] = t.time
							data.tSuspended = t.time
						data.tResumed = t.time
					continue
				
				elif(re.match('dpm_resume_noirq\[.*', t.name)):
					phase = data.setPhase('resume_noirq', t.time, isbegin)
					continue
				
				elif(re.match('dpm_resume_early\[.*', t.name)):
					phase = data.setPhase('resume_early', t.time, isbegin)
					continue
				
				elif(re.match('dpm_resume\[.*', t.name)):
					phase = data.setPhase('resume', t.time, isbegin)
					continue
				
				elif(re.match('dpm_complete\[.*', t.name)):
					phase = data.setPhase('resume_complete', t.time, isbegin)
					continue
				
				if(not data.isTraceEventOutsideDeviceCalls(pid, t.time)):
					continue
				
				if(name not in testrun.ttemp):
					testrun.ttemp[name] = []
				if(isbegin):
					
					testrun.ttemp[name].append(\
						{'begin': t.time, 'end': t.time, 'pid': pid})
				else:
					if(len(testrun.ttemp[name]) > 0):
						
						testrun.ttemp[name][-1]['end'] = t.time
			
			elif(t.type == 'device_pm_callback_start'):
				if phase not in data.dmesg:
					continue
				m = re.match('(?P<drv>.*) (?P<d>.*), parent: *(?P<p>.*), .*',\
					t.name);
				if(not m):
					continue
				drv = m.group('drv')
				n = m.group('d')
				p = m.group('p')
				if(n and p):
					data.newAction(phase, n, pid, p, t.time, -1, drv)
					if pid not in data.devpids:
						data.devpids.append(pid)
			
			elif(t.type == 'device_pm_callback_end'):
				if phase not in data.dmesg:
					continue
				m = re.match('(?P<drv>.*) (?P<d>.*), err.*', t.name);
				if(not m):
					continue
				n = m.group('d')
				list = data.dmesg[phase]['list']
				if(n in list):
					dev = list[n]
					dev['length'] = t.time - dev['start']
					dev['end'] = t.time
		
		elif(t.fkprobe):
			kprobename = t.type
			kprobedata = t.name
			key = (kprobename, pid)
			
			displayname = ''
			if(t.fcall):
				displayname = sysvals.kprobeDisplayName(kprobename, kprobedata)
				if not displayname:
					continue
				if(key not in tp.ktemp):
					tp.ktemp[key] = []
				tp.ktemp[key].append({
					'pid': pid,
					'begin': t.time,
					'end': -1,
					'name': displayname,
					'cdata': kprobedata,
					'proc': m_proc,
				})
				
				if(data.tKernSus == 0 and phase == 'suspend_prepare' \
					and kprobename in ksuscalls):
					data.tKernSus = t.time
			elif(t.freturn):
				if(key not in tp.ktemp) or len(tp.ktemp[key]) < 1:
					continue
				e = next((x for x in reversed(tp.ktemp[key]) if x['end'] < 0), 0)
				if not e:
					continue
				e['end'] = t.time
				e['rdata'] = kprobedata
				
				if(phase != 'suspend_prepare' and kprobename in krescalls):
					if phase in data.dmesg:
						data.dmesg[phase]['end'] = t.time
					data.tKernRes = t.time

		
		elif sysvals.usecallgraph:
			
			key = (m_proc, pid)
			if(key not in testrun.ftemp):
				testrun.ftemp[key] = []
				testrun.ftemp[key].append(FTraceCallGraph(pid, sysvals))
			
			cg = testrun.ftemp[key][-1]
			res = cg.addLine(t)
			if(res != 0):
				testrun.ftemp[key].append(FTraceCallGraph(pid, sysvals))
			if(res == -1):
				testrun.ftemp[key][-1].addLine(t)
	tf.close()
	if len(testdata) < 1:
		sysvals.vprint('WARNING: ftrace start marker is missing')
	if data and not data.devicegroups:
		sysvals.vprint('WARNING: ftrace end marker is missing')
		data.handleEndMarker(t.time, t.name)

	if sysvals.suspendmode == 'command':
		for test in testruns:
			for p in test.data.sortedPhases():
				if p == 'suspend_prepare':
					test.data.dmesg[p]['start'] = test.data.start
					test.data.dmesg[p]['end'] = test.data.end
				else:
					test.data.dmesg[p]['start'] = test.data.end
					test.data.dmesg[p]['end'] = test.data.end
			test.data.tSuspended = test.data.end
			test.data.tResumed = test.data.end
			test.data.fwValid = False

	
	if sysvals.usedevsrc or sysvals.useprocmon:
		sysvals.mixedphaseheight = False

	
	for data in testdata:
		lp = data.sortedPhases()[0]
		for p in data.sortedPhases():
			if(p != lp and not ('machine' in p and 'machine' in lp)):
				data.dmesg[lp]['end'] = data.dmesg[p]['start']
			lp = p

	for i in range(len(testruns)):
		test = testruns[i]
		data = test.data
		
		tlb, tle = data.start, data.end
		if i < len(testruns) - 1:
			tle = testruns[i+1].data.start
		
		if sysvals.useprocmon:
			data.createProcessUsageEvents()
		
		if(sysvals.usetraceevents):
			
			for name in sorted(test.ttemp):
				for event in test.ttemp[name]:
					data.newActionGlobal(name, event['begin'], event['end'], event['pid'])
			
			for key in sorted(tp.ktemp):
				name, pid = key
				if name not in sysvals.tracefuncs:
					continue
				if pid not in data.devpids:
					data.devpids.append(pid)
				for e in tp.ktemp[key]:
					kb, ke = e['begin'], e['end']
					if ke - kb < 0.000001 or tlb > kb or tle <= kb:
						continue
					color = sysvals.kprobeColor(name)
					data.newActionGlobal(e['name'], kb, ke, pid, color)
			
			if sysvals.usedevsrc:
				for key in sorted(tp.ktemp):
					name, pid = key
					if name in sysvals.tracefuncs or name not in sysvals.dev_tracefuncs:
						continue
					for e in tp.ktemp[key]:
						kb, ke = e['begin'], e['end']
						if ke - kb < 0.000001 or tlb > kb or tle <= kb:
							continue
						data.addDeviceFunctionCall(e['name'], name, e['proc'], pid, kb,
							ke, e['cdata'], e['rdata'])
		if sysvals.usecallgraph:
			
			sortlist = dict()
			for key in sorted(test.ftemp):
				proc, pid = key
				for cg in test.ftemp[key]:
					if len(cg.list) < 1 or cg.invalid or (cg.end - cg.start == 0):
						continue
					if(not cg.postProcess()):
						id = 'task %s' % (pid)
						sysvals.vprint('Sanity check failed for '+\
							id+', ignoring this callback')
						continue
					
					devname = ''
					if sysvals.suspendmode != 'command':
						devname = cg.deviceMatch(pid, data)
					if not devname:
						sortkey = '%f%f%d' % (cg.start, cg.end, pid)
						sortlist[sortkey] = cg
					elif len(cg.list) > 1000000 and cg.name != sysvals.ftopfunc:
						sysvals.vprint('WARNING: the callgraph for %s is massive (%d lines)' %\
							(devname, len(cg.list)))
			
			for sortkey in sorted(sortlist):
				cg = sortlist[sortkey]
				name = cg.name
				if sysvals.isCallgraphFunc(name):
					sysvals.vprint('Callgraph found for task %d: %.3fms, %s' % (cg.pid, (cg.end - cg.start)*1000, name))
					cg.newActionFromFunction(data)
	if sysvals.suspendmode == 'command':
		return (testdata, '')

	
	error = []
	for data in testdata:
		tn = '' if len(testdata) == 1 else ('%d' % (data.testnumber + 1))
		terr = ''
		phasedef = data.phasedef
		lp = 'suspend_prepare'
		for p in sorted(phasedef, key=lambda k:phasedef[k]['order']):
			if p not in data.dmesg:
				if not terr:
					pprint('TEST%s FAILED: %s failed in %s phase' % (tn, sysvals.suspendmode, lp))
					terr = '%s%s failed in %s phase' % (sysvals.suspendmode, tn, lp)
					error.append(terr)
					if data.tSuspended == 0:
						data.tSuspended = data.dmesg[lp]['end']
					if data.tResumed == 0:
						data.tResumed = data.dmesg[lp]['end']
					data.fwValid = False
				sysvals.vprint('WARNING: phase "%s" is missing!' % p)
			lp = p
		if not terr and 'dev' in data.wifi and data.wifi['stat'] == 'timeout':
			terr = '%s%s failed in wifi_resume <i>(%s %.0fs timeout)</i>' % \
				(sysvals.suspendmode, tn, data.wifi['dev'], data.wifi['time'])
			error.append(terr)
		if not terr and data.enterfail:
			pprint('test%s FAILED: enter %s failed with %s' % (tn, sysvals.suspendmode, data.enterfail))
			terr = 'test%s failed to enter %s mode' % (tn, sysvals.suspendmode)
			error.append(terr)
		if data.tSuspended == 0:
			data.tSuspended = data.tKernRes
		if data.tResumed == 0:
			data.tResumed = data.tSuspended

		if(len(sysvals.devicefilter) > 0):
			data.deviceFilter(sysvals.devicefilter)
		data.fixupInitcallsThatDidntReturn()
		if sysvals.usedevsrc:
			data.optimizeDevSrc()

	
	if sysvals.usedevsrc and len(testdata) > 1:
		tc = len(testdata)
		for i in range(tc - 1):
			devlist = testdata[i].overflowDevices()
			for j in range(i + 1, tc):
				testdata[j].mergeOverlapDevices(devlist)
		testdata[0].stitchTouchingThreads(testdata[1:])
	return (testdata, ', '.join(error))








def loadKernelLog():
	sysvals.vprint('Analyzing the dmesg data (%s)...' % \
		os.path.basename(sysvals.dmesgfile))
	if(os.path.exists(sysvals.dmesgfile) == False):
		doError('%s does not exist' % sysvals.dmesgfile)

	
	tp = TestProps()
	tp.stamp = datetime.now().strftime('
	testruns = []
	data = 0
	lf = sysvals.openlog(sysvals.dmesgfile, 'r')
	for line in lf:
		line = line.replace('\r\n', '')
		idx = line.find('[')
		if idx > 1:
			line = line[idx:]
		if tp.stampInfo(line):
			continue
		m = re.match('[ \t]*(\[ *)(?P<ktime>[0-9\.]*)(\]) (?P<msg>.*)', line)
		if(not m):
			continue
		msg = m.group("msg")
		if(re.match('PM: Syncing filesystems.*', msg)):
			if(data):
				testruns.append(data)
			data = Data(len(testruns))
			tp.parseStamp(data, sysvals)
		if(not data):
			continue
		m = re.match('.* *(?P<k>[0-9]\.[0-9]{2}\.[0-9]-.*) .*', msg)
		if(m):
			sysvals.stamp['kernel'] = m.group('k')
		m = re.match('PM: Preparing system for (?P<m>.*) sleep', msg)
		if(m):
			sysvals.stamp['mode'] = sysvals.suspendmode = m.group('m')
		data.dmesgtext.append(line)
	lf.close()

	if data:
		testruns.append(data)
	if len(testruns) < 1:
		doError('dmesg log has no suspend/resume data: %s' \
			% sysvals.dmesgfile)

	
	for data in testruns:
		last = ''
		for line in data.dmesgtext:
			mc = re.match('.*(\[ *)(?P<t>[0-9\.]*)(\]) calling  '+\
				'(?P<f>.*)\+ @ .*, parent: .*', line)
			mr = re.match('.*(\[ *)(?P<t>[0-9\.]*)(\]) call '+\
				'(?P<f>.*)\+ returned .* after (?P<dt>.*) usecs', last)
			if(mc and mr and (mc.group('t') == mr.group('t')) and
				(mc.group('f') == mr.group('f'))):
				i = data.dmesgtext.index(last)
				j = data.dmesgtext.index(line)
				data.dmesgtext[i] = line
				data.dmesgtext[j] = last
			last = line
	return testruns













def parseKernelLog(data):
	phase = 'suspend_runtime'

	if(data.fwValid):
		sysvals.vprint('Firmware Suspend = %u ns, Firmware Resume = %u ns' % \
			(data.fwSuspend, data.fwResume))

	
	dm = {
		'suspend_prepare': ['PM: Syncing filesystems.*'],
		        'suspend': ['PM: Entering [a-z]* sleep.*', 'Suspending console.*'],
		   'suspend_late': ['PM: suspend of devices complete after.*'],
		  'suspend_noirq': ['PM: late suspend of devices complete after.*'],
		'suspend_machine': ['PM: noirq suspend of devices complete after.*'],
		 'resume_machine': ['ACPI: Low-level resume complete.*'],
		   'resume_noirq': ['ACPI: Waking up from system sleep state.*'],
		   'resume_early': ['PM: noirq resume of devices complete after.*'],
		         'resume': ['PM: early resume of devices complete after.*'],
		'resume_complete': ['PM: resume of devices complete after.*'],
		    'post_resume': ['.*Restarting tasks \.\.\..*'],
	}
	if(sysvals.suspendmode == 'standby'):
		dm['resume_machine'] = ['PM: Restoring platform NVS memory']
	elif(sysvals.suspendmode == 'disk'):
		dm['suspend_late'] = ['PM: freeze of devices complete after.*']
		dm['suspend_noirq'] = ['PM: late freeze of devices complete after.*']
		dm['suspend_machine'] = ['PM: noirq freeze of devices complete after.*']
		dm['resume_machine'] = ['PM: Restoring platform NVS memory']
		dm['resume_early'] = ['PM: noirq restore of devices complete after.*']
		dm['resume'] = ['PM: early restore of devices complete after.*']
		dm['resume_complete'] = ['PM: restore of devices complete after.*']
	elif(sysvals.suspendmode == 'freeze'):
		dm['resume_machine'] = ['ACPI: resume from mwait']

	
	at = {
		'sync_filesystems': {
			'smsg': 'PM: Syncing filesystems.*',
			'emsg': 'PM: Preparing system for mem sleep.*' },
		'freeze_user_processes': {
			'smsg': 'Freezing user space processes .*',
			'emsg': 'Freezing remaining freezable tasks.*' },
		'freeze_tasks': {
			'smsg': 'Freezing remaining freezable tasks.*',
			'emsg': 'PM: Entering (?P<mode>[a-z,A-Z]*) sleep.*' },
		'ACPI prepare': {
			'smsg': 'ACPI: Preparing to enter system sleep state.*',
			'emsg': 'PM: Saving platform NVS memory.*' },
		'PM vns': {
			'smsg': 'PM: Saving platform NVS memory.*',
			'emsg': 'Disabling non-boot CPUs .*' },
	}

	t0 = -1.0
	cpu_start = -1.0
	prevktime = -1.0
	actions = dict()
	for line in data.dmesgtext:
		
		m = re.match('[ \t]*(\[ *)(?P<ktime>[0-9\.]*)(\]) (?P<msg>.*)', line)
		if(m):
			val = m.group('ktime')
			try:
				ktime = float(val)
			except:
				continue
			msg = m.group('msg')
			
			if t0 < 0:
				data.setStart(ktime)
				t0 = ktime
		else:
			continue

		
		phasechange = False
		for p in dm:
			for s in dm[p]:
				if(re.match(s, msg)):
					phasechange, phase = True, p
					break

		
		if(not sysvals.usetraceevents and sysvals.suspendmode == 'freeze' \
			and phase == 'resume_machine' and \
			re.match('calling  (?P<f>.*)\+ @ .*, parent: .*', msg)):
			data.setPhase(phase, ktime, False)
			phase = 'resume_noirq'
			data.setPhase(phase, ktime, True)

		if phasechange:
			if phase == 'suspend_prepare':
				data.setPhase(phase, ktime, True)
				data.setStart(ktime)
				data.tKernSus = ktime
			elif phase == 'suspend':
				lp = data.lastPhase()
				if lp:
					data.setPhase(lp, ktime, False)
				data.setPhase(phase, ktime, True)
			elif phase == 'suspend_late':
				lp = data.lastPhase()
				if lp:
					data.setPhase(lp, ktime, False)
				data.setPhase(phase, ktime, True)
			elif phase == 'suspend_noirq':
				lp = data.lastPhase()
				if lp:
					data.setPhase(lp, ktime, False)
				data.setPhase(phase, ktime, True)
			elif phase == 'suspend_machine':
				lp = data.lastPhase()
				if lp:
					data.setPhase(lp, ktime, False)
				data.setPhase(phase, ktime, True)
			elif phase == 'resume_machine':
				lp = data.lastPhase()
				if(sysvals.suspendmode in ['freeze', 'standby']):
					data.tSuspended = prevktime
					if lp:
						data.setPhase(lp, prevktime, False)
				else:
					data.tSuspended = ktime
					if lp:
						data.setPhase(lp, prevktime, False)
				data.tResumed = ktime
				data.setPhase(phase, ktime, True)
			elif phase == 'resume_noirq':
				lp = data.lastPhase()
				if lp:
					data.setPhase(lp, ktime, False)
				data.setPhase(phase, ktime, True)
			elif phase == 'resume_early':
				lp = data.lastPhase()
				if lp:
					data.setPhase(lp, ktime, False)
				data.setPhase(phase, ktime, True)
			elif phase == 'resume':
				lp = data.lastPhase()
				if lp:
					data.setPhase(lp, ktime, False)
				data.setPhase(phase, ktime, True)
			elif phase == 'resume_complete':
				lp = data.lastPhase()
				if lp:
					data.setPhase(lp, ktime, False)
				data.setPhase(phase, ktime, True)
			elif phase == 'post_resume':
				lp = data.lastPhase()
				if lp:
					data.setPhase(lp, ktime, False)
				data.setEnd(ktime)
				data.tKernRes = ktime
				break

		
		if(phase in data.sortedPhases()):
			
			if(re.match('calling  (?P<f>.*)\+ @ .*, parent: .*', msg)):
				sm = re.match('calling  (?P<f>.*)\+ @ '+\
					'(?P<n>.*), parent: (?P<p>.*)', msg);
				f = sm.group('f')
				n = sm.group('n')
				p = sm.group('p')
				if(f and n and p):
					data.newAction(phase, f, int(n), p, ktime, -1, '')
			
			elif(re.match('call (?P<f>.*)\+ returned .* after '+\
				'(?P<t>.*) usecs', msg)):
				sm = re.match('call (?P<f>.*)\+ returned .* after '+\
					'(?P<t>.*) usecs(?P<a>.*)', msg);
				f = sm.group('f')
				t = sm.group('t')
				list = data.dmesg[phase]['list']
				if(f in list):
					dev = list[f]
					dev['length'] = int(t)
					dev['end'] = ktime

		
		if(not sysvals.usetraceevents):
			
			for a in sorted(at):
				if(re.match(at[a]['smsg'], msg)):
					if(a not in actions):
						actions[a] = []
					actions[a].append({'begin': ktime, 'end': ktime})
				if(re.match(at[a]['emsg'], msg)):
					if(a in actions):
						actions[a][-1]['end'] = ktime
			
			if(re.match('Disabling non-boot CPUs .*', msg)):
				
				cpu_start = ktime
			elif(re.match('Enabling non-boot CPUs .*', msg)):
				
				cpu_start = ktime
			elif(re.match('smpboot: CPU (?P<cpu>[0-9]*) is now offline', msg)):
				
				m = re.match('smpboot: CPU (?P<cpu>[0-9]*) is now offline', msg)
				cpu = 'CPU'+m.group('cpu')
				if(cpu not in actions):
					actions[cpu] = []
				actions[cpu].append({'begin': cpu_start, 'end': ktime})
				cpu_start = ktime
			elif(re.match('CPU(?P<cpu>[0-9]*) is up', msg)):
				
				m = re.match('CPU(?P<cpu>[0-9]*) is up', msg)
				cpu = 'CPU'+m.group('cpu')
				if(cpu not in actions):
					actions[cpu] = []
				actions[cpu].append({'begin': cpu_start, 'end': ktime})
				cpu_start = ktime
		prevktime = ktime
	data.initDevicegroups()

	
	phasedef = data.phasedef
	terr, lp = '', 'suspend_prepare'
	for p in sorted(phasedef, key=lambda k:phasedef[k]['order']):
		if p not in data.dmesg:
			if not terr:
				pprint('TEST FAILED: %s failed in %s phase' % (sysvals.suspendmode, lp))
				terr = '%s failed in %s phase' % (sysvals.suspendmode, lp)
				if data.tSuspended == 0:
					data.tSuspended = data.dmesg[lp]['end']
				if data.tResumed == 0:
					data.tResumed = data.dmesg[lp]['end']
			sysvals.vprint('WARNING: phase "%s" is missing!' % p)
		lp = p
	lp = data.sortedPhases()[0]
	for p in data.sortedPhases():
		if(p != lp and not ('machine' in p and 'machine' in lp)):
			data.dmesg[lp]['end'] = data.dmesg[p]['start']
		lp = p
	if data.tSuspended == 0:
		data.tSuspended = data.tKernRes
	if data.tResumed == 0:
		data.tResumed = data.tSuspended

	
	for name in sorted(actions):
		for event in actions[name]:
			data.newActionGlobal(name, event['begin'], event['end'])

	if(len(sysvals.devicefilter) > 0):
		data.deviceFilter(sysvals.devicefilter)
	data.fixupInitcallsThatDidntReturn()
	return True

def callgraphHTML(sv, hf, num, cg, title, color, devid):
	html_func_top = '<article id="{0}" class="atop" style="background:{1}">\n<input type="checkbox" class="pf" id="f{2}" checked/><label for="f{2}">{3} {4}</label>\n'
	html_func_start = '<article>\n<input type="checkbox" class="pf" id="f{0}" checked/><label for="f{0}">{1} {2}</label>\n'
	html_func_end = '</article>\n'
	html_func_leaf = '<article>{0} {1}</article>\n'

	cgid = devid
	if cg.id:
		cgid += cg.id
	cglen = (cg.end - cg.start) * 1000
	if cglen < sv.mincglen:
		return num

	fmt = '<r>(%.3f ms @ '+sv.timeformat+' to '+sv.timeformat+')</r>'
	flen = fmt % (cglen, cg.start, cg.end)
	hf.write(html_func_top.format(cgid, color, num, title, flen))
	num += 1
	for line in cg.list:
		if(line.length < 0.000000001):
			flen = ''
		else:
			fmt = '<n>(%.3f ms @ '+sv.timeformat+')</n>'
			flen = fmt % (line.length*1000, line.time)
		if line.isLeaf():
			hf.write(html_func_leaf.format(line.name, flen))
		elif line.freturn:
			hf.write(html_func_end)
		else:
			hf.write(html_func_start.format(num, line.name, flen))
			num += 1
	hf.write(html_func_end)
	return num

def addCallgraphs(sv, hf, data):
	hf.write('<section id="callgraphs" class="callgraph">\n')
	
	num = 0
	for p in data.sortedPhases():
		if sv.cgphase and p != sv.cgphase:
			continue
		list = data.dmesg[p]['list']
		for devname in data.sortedDevices(p):
			if len(sv.cgfilter) > 0 and devname not in sv.cgfilter:
				continue
			dev = list[devname]
			color = 'white'
			if 'color' in data.dmesg[p]:
				color = data.dmesg[p]['color']
			if 'color' in dev:
				color = dev['color']
			name = devname
			if(devname in sv.devprops):
				name = sv.devprops[devname].altName(devname)
			if sv.suspendmode in suspendmodename:
				name += ' '+p
			if('ftrace' in dev):
				cg = dev['ftrace']
				if cg.name == sv.ftopfunc:
					name = 'top level suspend/resume call'
				num = callgraphHTML(sv, hf, num, cg,
					name, color, dev['id'])
			if('ftraces' in dev):
				for cg in dev['ftraces']:
					num = callgraphHTML(sv, hf, num, cg,
						name+' &rarr; '+cg.name, color, dev['id'])
	hf.write('\n\n    </section>\n')

def summaryCSS(title, center=True):
	tdcenter = 'text-align:center;' if center else ''
	out = '<!DOCTYPE html>\n<html>\n<head>\n\
	<meta http-equiv="content-type" content="text/html; charset=UTF-8">\n\
	<title>'+title+'</title>\n\
	<style type=\'text/css\'>\n\
		.stamp {width: 100%;text-align:center;background:
		table {width:100%;border-collapse: collapse;border:1px solid;}\n\
		th {border: 1px solid black;background:
		td {font: 14px "Times New Roman";'+tdcenter+'}\n\
		tr.head td {border: 1px solid black;background:
		tr.alt {background-color:
		tr.notice {color:red;}\n\
		.minval {background-color:
		.medval {background-color:
		.maxval {background-color:
		.head a {color:
	</style>\n</head>\n<body>\n'
	return out






def createHTMLSummarySimple(testruns, htmlfile, title):
	
	html = summaryCSS('Summary - SleepGraph')

	
	list = dict()
	tAvg, tMin, tMax, tMed = [0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [dict(), dict()]
	iMin, iMed, iMax = [0, 0], [0, 0], [0, 0]
	num = 0
	useturbo = usewifi = False
	lastmode = ''
	cnt = dict()
	for data in sorted(testruns, key=lambda v:(v['mode'], v['host'], v['kernel'], v['time'])):
		mode = data['mode']
		if mode not in list:
			list[mode] = {'data': [], 'avg': [0,0], 'min': [0,0], 'max': [0,0], 'med': [0,0]}
		if lastmode and lastmode != mode and num > 0:
			for i in range(2):
				s = sorted(tMed[i])
				list[lastmode]['med'][i] = s[int(len(s)//2)]
				iMed[i] = tMed[i][list[lastmode]['med'][i]]
			list[lastmode]['avg'] = [tAvg[0] / num, tAvg[1] / num]
			list[lastmode]['min'] = tMin
			list[lastmode]['max'] = tMax
			list[lastmode]['idx'] = (iMin, iMed, iMax)
			tAvg, tMin, tMax, tMed = [0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [dict(), dict()]
			iMin, iMed, iMax = [0, 0], [0, 0], [0, 0]
			num = 0
		pkgpc10 = syslpi = wifi = ''
		if 'pkgpc10' in data and 'syslpi' in data:
			pkgpc10, syslpi, useturbo = data['pkgpc10'], data['syslpi'], True
		if 'wifi' in data:
			wifi, usewifi = data['wifi'], True
		res = data['result']
		tVal = [float(data['suspend']), float(data['resume'])]
		list[mode]['data'].append([data['host'], data['kernel'],
			data['time'], tVal[0], tVal[1], data['url'], res,
			data['issues'], data['sus_worst'], data['sus_worsttime'],
			data['res_worst'], data['res_worsttime'], pkgpc10, syslpi, wifi])
		idx = len(list[mode]['data']) - 1
		if res.startswith('fail in'):
			res = 'fail'
		if res not in cnt:
			cnt[res] = 1
		else:
			cnt[res] += 1
		if res == 'pass':
			for i in range(2):
				tMed[i][tVal[i]] = idx
				tAvg[i] += tVal[i]
				if tMin[i] == 0 or tVal[i] < tMin[i]:
					iMin[i] = idx
					tMin[i] = tVal[i]
				if tMax[i] == 0 or tVal[i] > tMax[i]:
					iMax[i] = idx
					tMax[i] = tVal[i]
			num += 1
		lastmode = mode
	if lastmode and num > 0:
		for i in range(2):
			s = sorted(tMed[i])
			list[lastmode]['med'][i] = s[int(len(s)//2)]
			iMed[i] = tMed[i][list[lastmode]['med'][i]]
		list[lastmode]['avg'] = [tAvg[0] / num, tAvg[1] / num]
		list[lastmode]['min'] = tMin
		list[lastmode]['max'] = tMax
		list[lastmode]['idx'] = (iMin, iMed, iMax)

	
	desc = []
	for ilk in sorted(cnt, reverse=True):
		if cnt[ilk] > 0:
			desc.append('%d %s' % (cnt[ilk], ilk))
	html += '<div class="stamp">%s (%d tests: %s)</div>\n' % (title, len(testruns), ', '.join(desc))
	th = '\t<th>{0}</th>\n'
	td = '\t<td>{0}</td>\n'
	tdh = '\t<td{1}>{0}</td>\n'
	tdlink = '\t<td><a href="{0}">html</a></td>\n'
	cols = 12
	if useturbo:
		cols += 2
	if usewifi:
		cols += 1
	colspan = '%d' % cols

	
	html += '<table>\n<tr>\n' + th.format('
		th.format('Mode') + th.format('Host') + th.format('Kernel') +\
		th.format('Test Time') + th.format('Result') + th.format('Issues') +\
		th.format('Suspend') + th.format('Resume') +\
		th.format('Worst Suspend Device') + th.format('SD Time') +\
		th.format('Worst Resume Device') + th.format('RD Time')
	if useturbo:
		html += th.format('PkgPC10') + th.format('SysLPI')
	if usewifi:
		html += th.format('Wifi')
	html += th.format('Detail')+'</tr>\n'
	
	head = '<tr class="head"><td>{0}</td><td>{1}</td>'+\
		'<td colspan='+colspan+' class="sus">Suspend Avg={2} '+\
		'<span class=minval><a href="">Min={3}</a></span> '+\
		'<span class=medval><a href="">Med={4}</a></span> '+\
		'<span class=maxval><a href="">Max={5}</a></span> '+\
		'Resume Avg={6} '+\
		'<span class=minval><a href="">Min={7}</a></span> '+\
		'<span class=medval><a href="">Med={8}</a></span> '+\
		'<span class=maxval><a href="">Max={9}</a></span></td>'+\
		'</tr>\n'
	headnone = '<tr class="head"><td>{0}</td><td>{1}</td><td colspan='+\
		colspan+'></td></tr>\n'
	for mode in sorted(list):
		
		num = 0
		tAvg, tMin, tMax, tMed = list[mode]['avg'], list[mode]['min'],\
			list[mode]['max'], list[mode]['med']
		count = len(list[mode]['data'])
		if 'idx' in list[mode]:
			iMin, iMed, iMax = list[mode]['idx']
			html += head.format('%d' % count, mode.upper(),
				'%.3f' % tAvg[0], '%.3f' % tMin[0], '%.3f' % tMed[0], '%.3f' % tMax[0],
				'%.3f' % tAvg[1], '%.3f' % tMin[1], '%.3f' % tMed[1], '%.3f' % tMax[1],
				mode.lower()
			)
		else:
			iMin = iMed = iMax = [-1, -1, -1]
			html += headnone.format('%d' % count, mode.upper())
		for d in list[mode]['data']:
			
			rcls = ['alt'] if num % 2 == 1 else []
			if d[6] != 'pass':
				rcls.append('notice')
			html += '<tr class="'+(' '.join(rcls))+'">\n' if len(rcls) > 0 else '<tr>\n'
			
			idx = list[mode]['data'].index(d)
			tHigh = ['', '']
			for i in range(2):
				tag = 's%s' % mode if i == 0 else 'r%s' % mode
				if idx == iMin[i]:
					tHigh[i] = ' id="%smin" class=minval title="Minimum"' % tag
				elif idx == iMax[i]:
					tHigh[i] = ' id="%smax" class=maxval title="Maximum"' % tag
				elif idx == iMed[i]:
					tHigh[i] = ' id="%smed" class=medval title="Median"' % tag
			html += td.format("%d" % (list[mode]['data'].index(d) + 1)) 
			html += td.format(mode)										
			html += td.format(d[0])										
			html += td.format(d[1])										
			html += td.format(d[2])										
			html += td.format(d[6])										
			html += td.format(d[7])										
			html += tdh.format('%.3f ms' % d[3], tHigh[0]) if d[3] else td.format('')	
			html += tdh.format('%.3f ms' % d[4], tHigh[1]) if d[4] else td.format('')	
			html += td.format(d[8])										
			html += td.format('%.3f ms' % d[9])	if d[9] else td.format('')		
			html += td.format(d[10])									
			html += td.format('%.3f ms' % d[11]) if d[11] else td.format('')	
			if useturbo:
				html += td.format(d[12])								
				html += td.format(d[13])								
			if usewifi:
				html += td.format(d[14])								
			html += tdlink.format(d[5]) if d[5] else td.format('')		
			html += '</tr>\n'
			num += 1

	
	hf = open(htmlfile, 'w')
	hf.write(html+'</table>\n</body>\n</html>\n')
	hf.close()

def createHTMLDeviceSummary(testruns, htmlfile, title):
	html = summaryCSS('Device Summary - SleepGraph', False)

	
	devall = dict()
	for data in testruns:
		host, url, devlist = data['host'], data['url'], data['devlist']
		for type in devlist:
			if type not in devall:
				devall[type] = dict()
			mdevlist, devlist = devall[type], data['devlist'][type]
			for name in devlist:
				length = devlist[name]
				if name not in mdevlist:
					mdevlist[name] = {'name': name, 'host': host,
						'worst': length, 'total': length, 'count': 1,
						'url': url}
				else:
					if length > mdevlist[name]['worst']:
						mdevlist[name]['worst'] = length
						mdevlist[name]['url'] = url
						mdevlist[name]['host'] = host
					mdevlist[name]['total'] += length
					mdevlist[name]['count'] += 1

	
	th = '\t<th>{0}</th>\n'
	td = '\t<td align=center>{0}</td>\n'
	tdr = '\t<td align=right>{0}</td>\n'
	tdlink = '\t<td align=center><a href="{0}">html</a></td>\n'
	limit = 1
	for type in sorted(devall, reverse=True):
		num = 0
		devlist = devall[type]
		
		html += '<div class="stamp">%s (%s devices > %d ms)</div><table>\n' % \
			(title, type.upper(), limit)
		html += '<tr>\n' + '<th align=right>Device Name</th>' +\
			th.format('Average Time') + th.format('Count') +\
			th.format('Worst Time') + th.format('Host (worst time)') +\
			th.format('Link (worst time)') + '</tr>\n'
		for name in sorted(devlist, key=lambda k:(devlist[k]['worst'], \
			devlist[k]['total'], devlist[k]['name']), reverse=True):
			data = devall[type][name]
			data['average'] = data['total'] / data['count']
			if data['average'] < limit:
				continue
			
			rcls = ['alt'] if num % 2 == 1 else []
			html += '<tr class="'+(' '.join(rcls))+'">\n' if len(rcls) > 0 else '<tr>\n'
			html += tdr.format(data['name'])				
			html += td.format('%.3f ms' % data['average'])	
			html += td.format(data['count'])				
			html += td.format('%.3f ms' % data['worst'])	
			html += td.format(data['host'])					
			html += tdlink.format(data['url'])				
			html += '</tr>\n'
			num += 1
		html += '</table>\n'

	
	hf = open(htmlfile, 'w')
	hf.write(html+'</body>\n</html>\n')
	hf.close()
	return devall

def createHTMLIssuesSummary(testruns, issues, htmlfile, title, extra=''):
	multihost = len([e for e in issues if len(e['urls']) > 1]) > 0
	html = summaryCSS('Issues Summary - SleepGraph', False)
	total = len(testruns)

	
	th = '\t<th>{0}</th>\n'
	td = '\t<td align={0}>{1}</td>\n'
	tdlink = '<a href="{1}">{0}</a>'
	subtitle = '%d issues' % len(issues) if len(issues) > 0 else 'no issues'
	html += '<div class="stamp">%s (%s)</div><table>\n' % (title, subtitle)
	html += '<tr>\n' + th.format('Issue') + th.format('Count')
	if multihost:
		html += th.format('Hosts')
	html += th.format('Tests') + th.format('Fail Rate') +\
		th.format('First Instance') + '</tr>\n'

	num = 0
	for e in sorted(issues, key=lambda v:v['count'], reverse=True):
		testtotal = 0
		links = []
		for host in sorted(e['urls']):
			links.append(tdlink.format(host, e['urls'][host][0]))
			testtotal += len(e['urls'][host])
		rate = '%d/%d (%.2f%%)' % (testtotal, total, 100*float(testtotal)/float(total))
		
		rcls = ['alt'] if num % 2 == 1 else []
		html += '<tr class="'+(' '.join(rcls))+'">\n' if len(rcls) > 0 else '<tr>\n'
		html += td.format('left', e['line'])		
		html += td.format('center', e['count'])		
		if multihost:
			html += td.format('center', len(e['urls']))	
		html += td.format('center', testtotal)		
		html += td.format('center', rate)			
		html += td.format('center nowrap', '<br>'.join(links))	
		html += '</tr>\n'
		num += 1

	
	hf = open(htmlfile, 'w')
	hf.write(html+'</table>\n'+extra+'</body>\n</html>\n')
	hf.close()
	return issues

def ordinal(value):
	suffix = 'th'
	if value < 10 or value > 19:
		if value % 10 == 1:
			suffix = 'st'
		elif value % 10 == 2:
			suffix = 'nd'
		elif value % 10 == 3:
			suffix = 'rd'
	return '%d%s' % (value, suffix)








def createHTML(testruns, testfail):
	if len(testruns) < 1:
		pprint('ERROR: Not enough test data to build a timeline')
		return

	kerror = False
	for data in testruns:
		if data.kerror:
			kerror = True
		if(sysvals.suspendmode in ['freeze', 'standby']):
			data.trimFreezeTime(testruns[-1].tSuspended)
		else:
			data.getMemTime()

	
	html_error = '<div id="{1}" title="kernel error/warning" class="err" style="right:{0}%">{2}&rarr;</div>\n'
	html_traceevent = '<div title="{0}" class="traceevent{6}" style="left:{1}%;top:{2}px;height:{3}px;width:{4}%;line-height:{3}px;{7}">{5}</div>\n'
	html_cpuexec = '<div class="jiffie" style="left:{0}%;top:{1}px;height:{2}px;width:{3}%;background:{4};"></div>\n'
	html_timetotal = '<table class="time1">\n<tr>'\
		'<td class="green" title="{3}">{2} Suspend Time: <b>{0} ms</b></td>'\
		'<td class="yellow" title="{4}">{2} Resume Time: <b>{1} ms</b></td>'\
		'</tr>\n</table>\n'
	html_timetotal2 = '<table class="time1">\n<tr>'\
		'<td class="green" title="{4}">{3} Suspend Time: <b>{0} ms</b></td>'\
		'<td class="gray" title="time spent in low-power mode with clock running">'+sysvals.suspendmode+' time: <b>{1} ms</b></td>'\
		'<td class="yellow" title="{5}">{3} Resume Time: <b>{2} ms</b></td>'\
		'</tr>\n</table>\n'
	html_timetotal3 = '<table class="time1">\n<tr>'\
		'<td class="green">Execution Time: <b>{0} ms</b></td>'\
		'<td class="yellow">Command: <b>{1}</b></td>'\
		'</tr>\n</table>\n'
	html_fail = '<table class="testfail"><tr><td>{0}</td></tr></table>\n'
	html_kdesc = '<td class="{3}" title="time spent in kernel execution">{0}Kernel {2}: {1} ms</td>'
	html_fwdesc = '<td class="{3}" title="time spent in firmware">{0}Firmware {2}: {1} ms</td>'
	html_wifdesc = '<td class="yellow" title="time for wifi to reconnect after resume complete ({2})">{0}Wifi Resume: {1}</td>'

	
	scaleH = 20
	if kerror:
		scaleH = 40

	
	devtl = Timeline(30, scaleH)

	
	devtl.createHeader(sysvals, testruns[0].stamp)

	
	for data in testruns:
		tTotal = data.end - data.start
		if(tTotal == 0):
			doError('No timeline data')
		if sysvals.suspendmode == 'command':
			run_time = '%.0f' % (tTotal * 1000)
			if sysvals.testcommand:
				testdesc = sysvals.testcommand
			else:
				testdesc = 'unknown'
			if(len(testruns) > 1):
				testdesc = ordinal(data.testnumber+1)+' '+testdesc
			thtml = html_timetotal3.format(run_time, testdesc)
			devtl.html += thtml
			continue
		
		stot, rtot = sktime, rktime = data.getTimeValues()
		ssrc, rsrc, testdesc, testdesc2 = ['kernel'], ['kernel'], 'Kernel', ''
		if data.fwValid:
			stot += (data.fwSuspend/1000000.0)
			rtot += (data.fwResume/1000000.0)
			ssrc.append('firmware')
			rsrc.append('firmware')
			testdesc = 'Total'
		if 'time' in data.wifi and data.wifi['stat'] != 'timeout':
			rtot += data.end - data.tKernRes + (data.wifi['time'] * 1000.0)
			rsrc.append('wifi')
			testdesc = 'Total'
		suspend_time, resume_time = '%.3f' % stot, '%.3f' % rtot
		stitle = 'time from kernel suspend start to %s mode [%s time]' % \
			(sysvals.suspendmode, ' & '.join(ssrc))
		rtitle = 'time from %s mode to kernel resume complete [%s time]' % \
			(sysvals.suspendmode, ' & '.join(rsrc))
		if(len(testruns) > 1):
			testdesc = testdesc2 = ordinal(data.testnumber+1)
			testdesc2 += ' '
		if(len(data.tLow) == 0):
			thtml = html_timetotal.format(suspend_time, \
				resume_time, testdesc, stitle, rtitle)
		else:
			low_time = '+'.join(data.tLow)
			thtml = html_timetotal2.format(suspend_time, low_time, \
				resume_time, testdesc, stitle, rtitle)
		devtl.html += thtml
		if not data.fwValid and 'dev' not in data.wifi:
			continue
		
		thtml = '<table class="time2">\n<tr>'
		thtml += html_kdesc.format(testdesc2, '%.3f'%sktime, 'Suspend', 'green')
		if data.fwValid:
			sftime = '%.3f'%(data.fwSuspend / 1000000.0)
			rftime = '%.3f'%(data.fwResume / 1000000.0)
			thtml += html_fwdesc.format(testdesc2, sftime, 'Suspend', 'green')
			thtml += html_fwdesc.format(testdesc2, rftime, 'Resume', 'yellow')
		thtml += html_kdesc.format(testdesc2, '%.3f'%rktime, 'Resume', 'yellow')
		if 'time' in data.wifi:
			if data.wifi['stat'] != 'timeout':
				wtime = '%.0f ms'%(data.end - data.tKernRes + (data.wifi['time'] * 1000.0))
			else:
				wtime = 'TIMEOUT'
			thtml += html_wifdesc.format(testdesc2, wtime, data.wifi['dev'])
		thtml += '</tr>\n</table>\n'
		devtl.html += thtml
	if testfail:
		devtl.html += html_fail.format(testfail)

	
	t0 = testruns[0].start
	tMax = testruns[-1].end
	tTotal = tMax - t0

	
	fulllist = []
	threadlist = []
	pscnt = 0
	devcnt = 0
	for data in testruns:
		data.selectTimelineDevices('%f', tTotal, sysvals.mindevlen)
		for group in data.devicegroups:
			devlist = []
			for phase in group:
				for devname in sorted(data.tdevlist[phase]):
					d = DevItem(data.testnumber, phase, data.dmesg[phase]['list'][devname])
					devlist.append(d)
					if d.isa('kth'):
						threadlist.append(d)
					else:
						if d.isa('ps'):
							pscnt += 1
						else:
							devcnt += 1
						fulllist.append(d)
			if sysvals.mixedphaseheight:
				devtl.getPhaseRows(devlist)
	if not sysvals.mixedphaseheight:
		if len(threadlist) > 0 and len(fulllist) > 0:
			if pscnt > 0 and devcnt > 0:
				msg = 'user processes & device pm callbacks'
			elif pscnt > 0:
				msg = 'user processes'
			else:
				msg = 'device pm callbacks'
			d = testruns[0].addHorizontalDivider(msg, testruns[-1].end)
			fulllist.insert(0, d)
		devtl.getPhaseRows(fulllist)
		if len(threadlist) > 0:
			d = testruns[0].addHorizontalDivider('asynchronous kernel threads', testruns[-1].end)
			threadlist.insert(0, d)
			devtl.getPhaseRows(threadlist, devtl.rows)
	devtl.calcTotalRows()

	
	devtl.createZoomBox(sysvals.suspendmode, len(testruns))
	for data in testruns:
		
		phases = {'suspend':[],'resume':[]}
		for phase in data.sortedPhases():
			if data.dmesg[phase]['start'] >= data.tSuspended:
				phases['resume'].append(phase)
			else:
				phases['suspend'].append(phase)
		
		for dir in phases:
			
			bname = '%s%d' % (dir[0], data.testnumber)
			if dir == 'suspend':
				m0 = data.start
				mMax = data.tSuspended
				left = '%f' % (((m0-t0)*100.0)/tTotal)
			else:
				m0 = data.tSuspended
				mMax = data.end
				
				if len(testruns) > 1 and data.testnumber == 0:
					mMax = testruns[1].start
				left = '%f' % ((((m0-t0)*100.0)+sysvals.srgap/2)/tTotal)
			mTotal = mMax - m0
			
			if mTotal == 0:
				continue
			width = '%f' % (((mTotal*100.0)-sysvals.srgap/2)/tTotal)
			devtl.html += devtl.html_tblock.format(bname, left, width, devtl.scaleH)
			for b in phases[dir]:
				
				phase = data.dmesg[b]
				length = phase['end']-phase['start']
				left = '%f' % (((phase['start']-m0)*100.0)/mTotal)
				width = '%f' % ((length*100.0)/mTotal)
				devtl.html += devtl.html_phase.format(left, width, \
					'%.3f'%devtl.scaleH, '%.3f'%devtl.bodyH, \
					data.dmesg[b]['color'], '')
			for e in data.errorinfo[dir]:
				
				type, t, idx1, idx2 = e
				id = '%d_%d' % (idx1, idx2)
				right = '%f' % (((mMax-t)*100.0)/mTotal)
				devtl.html += html_error.format(right, id, type)
			for b in phases[dir]:
				
				phaselist = data.dmesg[b]['list']
				for d in sorted(data.tdevlist[b]):
					name = d
					drv = ''
					dev = phaselist[d]
					xtraclass = ''
					xtrainfo = ''
					xtrastyle = ''
					if 'htmlclass' in dev:
						xtraclass = dev['htmlclass']
					if 'color' in dev:
						xtrastyle = 'background:%s;' % dev['color']
					if(d in sysvals.devprops):
						name = sysvals.devprops[d].altName(d)
						xtraclass = sysvals.devprops[d].xtraClass()
						xtrainfo = sysvals.devprops[d].xtraInfo()
					elif xtraclass == ' kth':
						xtrainfo = ' kernel_thread'
					if('drv' in dev and dev['drv']):
						drv = ' {%s}' % dev['drv']
					rowheight = devtl.phaseRowHeight(data.testnumber, b, dev['row'])
					rowtop = devtl.phaseRowTop(data.testnumber, b, dev['row'])
					top = '%.3f' % (rowtop + devtl.scaleH)
					left = '%f' % (((dev['start']-m0)*100)/mTotal)
					width = '%f' % (((dev['end']-dev['start'])*100)/mTotal)
					length = ' (%0.3f ms) ' % ((dev['end']-dev['start'])*1000)
					title = name+drv+xtrainfo+length
					if sysvals.suspendmode == 'command':
						title += sysvals.testcommand
					elif xtraclass == ' ps':
						if 'suspend' in b:
							title += 'pre_suspend_process'
						else:
							title += 'post_resume_process'
					else:
						title += b
					devtl.html += devtl.html_device.format(dev['id'], \
						title, left, top, '%.3f'%rowheight, width, \
						d+drv, xtraclass, xtrastyle)
					if('cpuexec' in dev):
						for t in sorted(dev['cpuexec']):
							start, end = t
							j = float(dev['cpuexec'][t]) / 5
							if j > 1.0:
								j = 1.0
							height = '%.3f' % (rowheight/3)
							top = '%.3f' % (rowtop + devtl.scaleH + 2*rowheight/3)
							left = '%f' % (((start-m0)*100)/mTotal)
							width = '%f' % ((end-start)*100/mTotal)
							color = 'rgba(255, 0, 0, %f)' % j
							devtl.html += \
								html_cpuexec.format(left, top, height, width, color)
					if('src' not in dev):
						continue
					
					for e in dev['src']:
						height = '%.3f' % devtl.rowH
						top = '%.3f' % (rowtop + devtl.scaleH + (e.row*devtl.rowH))
						left = '%f' % (((e.time-m0)*100)/mTotal)
						width = '%f' % (e.length*100/mTotal)
						xtrastyle = ''
						if e.color:
							xtrastyle = 'background:%s;' % e.color
						devtl.html += \
							html_traceevent.format(e.title(), \
								left, top, height, width, e.text(), '', xtrastyle)
			
			devtl.createTimeScale(m0, mMax, tTotal, dir)
			devtl.html += '</div>\n'

	
	devtl.html += '</div>\n</div>\n'

	
	if sysvals.suspendmode != 'command':
		phasedef = testruns[-1].phasedef
		devtl.html += '<div class="legend">\n'
		pdelta = 100.0/len(phasedef.keys())
		pmargin = pdelta / 4.0
		for phase in sorted(phasedef, key=lambda k:phasedef[k]['order']):
			id, p = '', phasedef[phase]
			for word in phase.split('_'):
				id += word[0]
			order = '%.2f' % ((p['order'] * pdelta) + pmargin)
			name = phase.replace('_', ' &nbsp;')
			devtl.html += devtl.html_legend.format(order, p['color'], name, id)
		devtl.html += '</div>\n'

	hf = open(sysvals.htmlfile, 'w')
	addCSS(hf, sysvals, len(testruns), kerror)

	
	hf.write(devtl.html)
	hf.write('<div id="devicedetailtitle"></div>\n')
	hf.write('<div id="devicedetail" style="display:none;">\n')
	
	for data in testruns:
		hf.write('<div id="devicedetail%d">\n' % data.testnumber)
		pscolor = 'linear-gradient(to top left, 
		hf.write(devtl.html_phaselet.format('pre_suspend_process', \
			'0', '0', pscolor))
		for b in data.sortedPhases():
			phase = data.dmesg[b]
			length = phase['end']-phase['start']
			left = '%.3f' % (((phase['start']-t0)*100.0)/tTotal)
			width = '%.3f' % ((length*100.0)/tTotal)
			hf.write(devtl.html_phaselet.format(b, left, width, \
				data.dmesg[b]['color']))
		hf.write(devtl.html_phaselet.format('post_resume_process', \
			'0', '0', pscolor))
		if sysvals.suspendmode == 'command':
			hf.write(devtl.html_phaselet.format('cmdexec', '0', '0', pscolor))
		hf.write('</div>\n')
	hf.write('</div>\n')

	
	if sysvals.cgtest >= 0 and len(testruns) > sysvals.cgtest:
		data = testruns[sysvals.cgtest]
	else:
		data = testruns[-1]
	if sysvals.usecallgraph:
		addCallgraphs(sysvals, hf, data)

	
	if sysvals.testlog and sysvals.logmsg:
		hf.write('<div id="testlog" style="display:none;">\n'+sysvals.logmsg+'</div>\n')
	
	if sysvals.dmesglog and sysvals.dmesgfile:
		hf.write('<div id="dmesglog" style="display:none;">\n')
		lf = sysvals.openlog(sysvals.dmesgfile, 'r')
		for line in lf:
			line = line.replace('<', '&lt').replace('>', '&gt')
			hf.write(line)
		lf.close()
		hf.write('</div>\n')
	
	if sysvals.ftracelog and sysvals.ftracefile:
		hf.write('<div id="ftracelog" style="display:none;">\n')
		lf = sysvals.openlog(sysvals.ftracefile, 'r')
		for line in lf:
			hf.write(line)
		lf.close()
		hf.write('</div>\n')

	
	addScriptCode(hf, testruns)
	hf.write('</body>\n</html>\n')
	hf.close()
	return True

def addCSS(hf, sv, testcount=1, kerror=False, extra=''):
	kernel = sv.stamp['kernel']
	host = sv.hostname[0].upper()+sv.hostname[1:]
	mode = sv.suspendmode
	if sv.suspendmode in suspendmodename:
		mode = suspendmodename[sv.suspendmode]
	title = host+' '+mode+' '+kernel

	
	cgchk = 'checked'
	cgnchk = 'not(:checked)'
	if sv.cgexp:
		cgchk = 'not(:checked)'
		cgnchk = 'checked'

	hoverZ = 'z-index:8;'
	if sv.usedevsrc:
		hoverZ = ''

	devlistpos = 'absolute'
	if testcount > 1:
		devlistpos = 'relative'

	scaleTH = 20
	if kerror:
		scaleTH = 60

	
	html_header = '<!DOCTYPE html>\n<html>\n<head>\n\
	<meta http-equiv="content-type" content="text/html; charset=UTF-8">\n\
	<title>'+title+'</title>\n\
	<style type=\'text/css\'>\n\
		body {overflow-y:scroll;}\n\
		.stamp {width:100%;text-align:center;background:gray;line-height:30px;color:white;font:25px Arial;}\n\
		.stamp.sysinfo {font:10px Arial;}\n\
		.callgraph {margin-top:30px;box-shadow:5px 5px 20px black;}\n\
		.callgraph article * {padding-left:28px;}\n\
		h1 {color:black;font:bold 30px Times;}\n\
		t0 {color:black;font:bold 30px Times;}\n\
		t1 {color:black;font:30px Times;}\n\
		t2 {color:black;font:25px Times;}\n\
		t3 {color:black;font:20px Times;white-space:nowrap;}\n\
		t4 {color:black;font:bold 30px Times;line-height:60px;white-space:nowrap;}\n\
		cS {font:bold 13px Times;}\n\
		table {width:100%;}\n\
		.gray {background:rgba(80,80,80,0.1);}\n\
		.green {background:rgba(204,255,204,0.4);}\n\
		.purple {background:rgba(128,0,128,0.2);}\n\
		.yellow {background:rgba(255,255,204,0.4);}\n\
		.blue {background:rgba(169,208,245,0.4);}\n\
		.time1 {font:22px Arial;border:1px solid;}\n\
		.time2 {font:15px Arial;border-bottom:1px solid;border-left:1px solid;border-right:1px solid;}\n\
		.testfail {font:bold 22px Arial;color:red;border:1px dashed;}\n\
		td {text-align:center;}\n\
		r {color:
		n {color:
		.tdhl {color:red;}\n\
		.hide {display:none;}\n\
		.pf {display:none;}\n\
		.pf:'+cgchk+' + label {background:url(\'data:image/svg+xml;utf,<?xml version="1.0" standalone="no"?><svg xmlns="http://www.w3.org/2000/svg" height="18" width="18" version="1.1"><circle cx="9" cy="9" r="8" stroke="black" stroke-width="1" fill="white"/><rect x="4" y="8" width="10" height="2" style="fill:black;stroke-width:0"/><rect x="8" y="4" width="2" height="10" style="fill:black;stroke-width:0"/></svg>\') no-repeat left center;}\n\
		.pf:'+cgnchk+' ~ label {background:url(\'data:image/svg+xml;utf,<?xml version="1.0" standalone="no"?><svg xmlns="http://www.w3.org/2000/svg" height="18" width="18" version="1.1"><circle cx="9" cy="9" r="8" stroke="black" stroke-width="1" fill="white"/><rect x="4" y="8" width="10" height="2" style="fill:black;stroke-width:0"/></svg>\') no-repeat left center;}\n\
		.pf:'+cgchk+' ~ *:not(:nth-child(2)) {display:none;}\n\
		.zoombox {position:relative;width:100%;overflow-x:scroll;-webkit-user-select:none;-moz-user-select:none;user-select:none;}\n\
		.timeline {position:relative;font-size:14px;cursor:pointer;width:100%; overflow:hidden;background:linear-gradient(
		.thread {position:absolute;height:0%;overflow:hidden;z-index:7;line-height:30px;font-size:14px;border:1px solid;text-align:center;white-space:nowrap;}\n\
		.thread.ps {border-radius:3px;background:linear-gradient(to top, 
		.thread:hover {background:white;border:1px solid red;'+hoverZ+'}\n\
		.thread.sec,.thread.sec:hover {background:black;border:0;color:white;line-height:15px;font-size:10px;}\n\
		.hover {background:white;border:1px solid red;'+hoverZ+'}\n\
		.hover.sync {background:white;}\n\
		.hover.bg,.hover.kth,.hover.sync,.hover.ps {background:white;}\n\
		.jiffie {position:absolute;pointer-events: none;z-index:8;}\n\
		.traceevent {position:absolute;font-size:10px;z-index:7;overflow:hidden;color:black;text-align:center;white-space:nowrap;border-radius:5px;border:1px solid black;background:linear-gradient(to bottom right,
		.traceevent:hover {color:white;font-weight:bold;border:1px solid white;}\n\
		.phase {position:absolute;overflow:hidden;border:0px;text-align:center;}\n\
		.phaselet {float:left;overflow:hidden;border:0px;text-align:center;min-height:100px;font-size:24px;}\n\
		.t {position:absolute;line-height:'+('%d'%scaleTH)+'px;pointer-events:none;top:0;height:100%;border-right:1px solid black;z-index:6;}\n\
		.err {position:absolute;top:0%;height:100%;border-right:3px solid red;color:red;font:bold 14px Times;line-height:18px;}\n\
		.legend {position:relative; width:100%; height:40px; text-align:center;margin-bottom:20px}\n\
		.legend .square {position:absolute;cursor:pointer;top:10px; width:0px;height:20px;border:1px solid;padding-left:20px;}\n\
		button {height:40px;width:200px;margin-bottom:20px;margin-top:20px;font-size:24px;}\n\
		.btnfmt {position:relative;float:right;height:25px;width:auto;margin-top:3px;margin-bottom:0;font-size:10px;text-align:center;}\n\
		.devlist {position:'+devlistpos+';width:190px;}\n\
		a:link {color:white;text-decoration:none;}\n\
		a:visited {color:white;}\n\
		a:hover {color:white;}\n\
		a:active {color:white;}\n\
		.version {position:relative;float:left;color:white;font-size:10px;line-height:30px;margin-left:10px;}\n\
		
		.tblock {position:absolute;height:100%;background:
		.tback {position:absolute;width:100%;background:linear-gradient(
		.bg {z-index:1;}\n\
'+extra+'\
	</style>\n</head>\n<body>\n'
	hf.write(html_header)







def addScriptCode(hf, testruns):
	t0 = testruns[0].start * 1000
	tMax = testruns[-1].end * 1000
	
	detail = '	var devtable = [];\n'
	for data in testruns:
		topo = data.deviceTopology()
		detail += '	devtable[%d] = "%s";\n' % (data.testnumber, topo)
	detail += '	var bounds = [%f,%f];\n' % (t0, tMax)
	
	script_code = \
	'<script type="text/javascript">\n'+detail+\
	'	var resolution = -1;\n'\
	'	var dragval = [0, 0];\n'\
	'	function redrawTimescale(t0, tMax, tS) {\n'\
	'		var rline = \'<div class="t" style="left:0;border-left:1px solid black;border-right:0;">\';\n'\
	'		var tTotal = tMax - t0;\n'\
	'		var list = document.getElementsByClassName("tblock");\n'\
	'		for (var i = 0; i < list.length; i++) {\n'\
	'			var timescale = list[i].getElementsByClassName("timescale")[0];\n'\
	'			var m0 = t0 + (tTotal*parseFloat(list[i].style.left)/100);\n'\
	'			var mTotal = tTotal*parseFloat(list[i].style.width)/100;\n'\
	'			var mMax = m0 + mTotal;\n'\
	'			var html = "";\n'\
	'			var divTotal = Math.floor(mTotal/tS) + 1;\n'\
	'			if(divTotal > 1000) continue;\n'\
	'			var divEdge = (mTotal - tS*(divTotal-1))*100/mTotal;\n'\
	'			var pos = 0.0, val = 0.0;\n'\
	'			for (var j = 0; j < divTotal; j++) {\n'\
	'				var htmlline = "";\n'\
	'				var mode = list[i].id[5];\n'\
	'				if(mode == "s") {\n'\
	'					pos = 100 - (((j)*tS*100)/mTotal) - divEdge;\n'\
	'					val = (j-divTotal+1)*tS;\n'\
	'					if(j == divTotal - 1)\n'\
	'						htmlline = \'<div class="t" style="right:\'+pos+\'%"><cS>S&rarr;</cS></div>\';\n'\
	'					else\n'\
	'						htmlline = \'<div class="t" style="right:\'+pos+\'%">\'+val+\'ms</div>\';\n'\
	'				} else {\n'\
	'					pos = 100 - (((j)*tS*100)/mTotal);\n'\
	'					val = (j)*tS;\n'\
	'					htmlline = \'<div class="t" style="right:\'+pos+\'%">\'+val+\'ms</div>\';\n'\
	'					if(j == 0)\n'\
	'						if(mode == "r")\n'\
	'							htmlline = rline+"<cS>&larr;R</cS></div>";\n'\
	'						else\n'\
	'							htmlline = rline+"<cS>0ms</div>";\n'\
	'				}\n'\
	'				html += htmlline;\n'\
	'			}\n'\
	'			timescale.innerHTML = html;\n'\
	'		}\n'\
	'	}\n'\
	'	function zoomTimeline() {\n'\
	'		var dmesg = document.getElementById("dmesg");\n'\
	'		var zoombox = document.getElementById("dmesgzoombox");\n'\
	'		var left = zoombox.scrollLeft;\n'\
	'		var val = parseFloat(dmesg.style.width);\n'\
	'		var newval = 100;\n'\
	'		var sh = window.outerWidth / 2;\n'\
	'		if(this.id == "zoomin") {\n'\
	'			newval = val * 1.2;\n'\
	'			if(newval > 910034) newval = 910034;\n'\
	'			dmesg.style.width = newval+"%";\n'\
	'			zoombox.scrollLeft = ((left + sh) * newval / val) - sh;\n'\
	'		} else if (this.id == "zoomout") {\n'\
	'			newval = val / 1.2;\n'\
	'			if(newval < 100) newval = 100;\n'\
	'			dmesg.style.width = newval+"%";\n'\
	'			zoombox.scrollLeft = ((left + sh) * newval / val) - sh;\n'\
	'		} else {\n'\
	'			zoombox.scrollLeft = 0;\n'\
	'			dmesg.style.width = "100%";\n'\
	'		}\n'\
	'		var tS = [10000, 5000, 2000, 1000, 500, 200, 100, 50, 20, 10, 5, 2, 1];\n'\
	'		var t0 = bounds[0];\n'\
	'		var tMax = bounds[1];\n'\
	'		var tTotal = tMax - t0;\n'\
	'		var wTotal = tTotal * 100.0 / newval;\n'\
	'		var idx = 7*window.innerWidth/1100;\n'\
	'		for(var i = 0; (i < tS.length)&&((wTotal / tS[i]) < idx); i++);\n'\
	'		if(i >= tS.length) i = tS.length - 1;\n'\
	'		if(tS[i] == resolution) return;\n'\
	'		resolution = tS[i];\n'\
	'		redrawTimescale(t0, tMax, tS[i]);\n'\
	'	}\n'\
	'	function deviceName(title) {\n'\
	'		var name = title.slice(0, title.indexOf(" ("));\n'\
	'		return name;\n'\
	'	}\n'\
	'	function deviceHover() {\n'\
	'		var name = deviceName(this.title);\n'\
	'		var dmesg = document.getElementById("dmesg");\n'\
	'		var dev = dmesg.getElementsByClassName("thread");\n'\
	'		var cpu = -1;\n'\
	'		if(name.match("CPU_ON\[[0-9]*\]"))\n'\
	'			cpu = parseInt(name.slice(7));\n'\
	'		else if(name.match("CPU_OFF\[[0-9]*\]"))\n'\
	'			cpu = parseInt(name.slice(8));\n'\
	'		for (var i = 0; i < dev.length; i++) {\n'\
	'			dname = deviceName(dev[i].title);\n'\
	'			var cname = dev[i].className.slice(dev[i].className.indexOf("thread"));\n'\
	'			if((cpu >= 0 && dname.match("CPU_O[NF]*\\\[*"+cpu+"\\\]")) ||\n'\
	'				(name == dname))\n'\
	'			{\n'\
	'				dev[i].className = "hover "+cname;\n'\
	'			} else {\n'\
	'				dev[i].className = cname;\n'\
	'			}\n'\
	'		}\n'\
	'	}\n'\
	'	function deviceUnhover() {\n'\
	'		var dmesg = document.getElementById("dmesg");\n'\
	'		var dev = dmesg.getElementsByClassName("thread");\n'\
	'		for (var i = 0; i < dev.length; i++) {\n'\
	'			dev[i].className = dev[i].className.slice(dev[i].className.indexOf("thread"));\n'\
	'		}\n'\
	'	}\n'\
	'	function deviceTitle(title, total, cpu) {\n'\
	'		var prefix = "Total";\n'\
	'		if(total.length > 3) {\n'\
	'			prefix = "Average";\n'\
	'			total[1] = (total[1]+total[3])/2;\n'\
	'			total[2] = (total[2]+total[4])/2;\n'\
	'		}\n'\
	'		var devtitle = document.getElementById("devicedetailtitle");\n'\
	'		var name = deviceName(title);\n'\
	'		if(cpu >= 0) name = "CPU"+cpu;\n'\
	'		var driver = "";\n'\
	'		var tS = "<t2>(</t2>";\n'\
	'		var tR = "<t2>)</t2>";\n'\
	'		if(total[1] > 0)\n'\
	'			tS = "<t2>("+prefix+" Suspend:</t2><t0> "+total[1].toFixed(3)+" ms</t0> ";\n'\
	'		if(total[2] > 0)\n'\
	'			tR = " <t2>"+prefix+" Resume:</t2><t0> "+total[2].toFixed(3)+" ms<t2>)</t2></t0>";\n'\
	'		var s = title.indexOf("{");\n'\
	'		var e = title.indexOf("}");\n'\
	'		if((s >= 0) && (e >= 0))\n'\
	'			driver = title.slice(s+1, e) + " <t1>@</t1> ";\n'\
	'		if(total[1] > 0 && total[2] > 0)\n'\
	'			devtitle.innerHTML = "<t0>"+driver+name+"</t0> "+tS+tR;\n'\
	'		else\n'\
	'			devtitle.innerHTML = "<t0>"+title+"</t0>";\n'\
	'		return name;\n'\
	'	}\n'\
	'	function deviceDetail() {\n'\
	'		var devinfo = document.getElementById("devicedetail");\n'\
	'		devinfo.style.display = "block";\n'\
	'		var name = deviceName(this.title);\n'\
	'		var cpu = -1;\n'\
	'		if(name.match("CPU_ON\[[0-9]*\]"))\n'\
	'			cpu = parseInt(name.slice(7));\n'\
	'		else if(name.match("CPU_OFF\[[0-9]*\]"))\n'\
	'			cpu = parseInt(name.slice(8));\n'\
	'		var dmesg = document.getElementById("dmesg");\n'\
	'		var dev = dmesg.getElementsByClassName("thread");\n'\
	'		var idlist = [];\n'\
	'		var pdata = [[]];\n'\
	'		if(document.getElementById("devicedetail1"))\n'\
	'			pdata = [[], []];\n'\
	'		var pd = pdata[0];\n'\
	'		var total = [0.0, 0.0, 0.0];\n'\
	'		for (var i = 0; i < dev.length; i++) {\n'\
	'			dname = deviceName(dev[i].title);\n'\
	'			if((cpu >= 0 && dname.match("CPU_O[NF]*\\\[*"+cpu+"\\\]")) ||\n'\
	'				(name == dname))\n'\
	'			{\n'\
	'				idlist[idlist.length] = dev[i].id;\n'\
	'				var tidx = 1;\n'\
	'				if(dev[i].id[0] == "a") {\n'\
	'					pd = pdata[0];\n'\
	'				} else {\n'\
	'					if(pdata.length == 1) pdata[1] = [];\n'\
	'					if(total.length == 3) total[3]=total[4]=0.0;\n'\
	'					pd = pdata[1];\n'\
	'					tidx = 3;\n'\
	'				}\n'\
	'				var info = dev[i].title.split(" ");\n'\
	'				var pname = info[info.length-1];\n'\
	'				pd[pname] = parseFloat(info[info.length-3].slice(1));\n'\
	'				total[0] += pd[pname];\n'\
	'				if(pname.indexOf("suspend") >= 0)\n'\
	'					total[tidx] += pd[pname];\n'\
	'				else\n'\
	'					total[tidx+1] += pd[pname];\n'\
	'			}\n'\
	'		}\n'\
	'		var devname = deviceTitle(this.title, total, cpu);\n'\
	'		var left = 0.0;\n'\
	'		for (var t = 0; t < pdata.length; t++) {\n'\
	'			pd = pdata[t];\n'\
	'			devinfo = document.getElementById("devicedetail"+t);\n'\
	'			var phases = devinfo.getElementsByClassName("phaselet");\n'\
	'			for (var i = 0; i < phases.length; i++) {\n'\
	'				if(phases[i].id in pd) {\n'\
	'					var w = 100.0*pd[phases[i].id]/total[0];\n'\
	'					var fs = 32;\n'\
	'					if(w < 8) fs = 4*w | 0;\n'\
	'					var fs2 = fs*3/4;\n'\
	'					phases[i].style.width = w+"%";\n'\
	'					phases[i].style.left = left+"%";\n'\
	'					phases[i].title = phases[i].id+" "+pd[phases[i].id]+" ms";\n'\
	'					left += w;\n'\
	'					var time = "<t4 style=\\"font-size:"+fs+"px\\">"+pd[phases[i].id]+" ms<br></t4>";\n'\
	'					var pname = "<t3 style=\\"font-size:"+fs2+"px\\">"+phases[i].id.replace(new RegExp("_", "g"), " ")+"</t3>";\n'\
	'					phases[i].innerHTML = time+pname;\n'\
	'				} else {\n'\
	'					phases[i].style.width = "0%";\n'\
	'					phases[i].style.left = left+"%";\n'\
	'				}\n'\
	'			}\n'\
	'		}\n'\
	'		if(typeof devstats !== \'undefined\')\n'\
	'			callDetail(this.id, this.title);\n'\
	'		var cglist = document.getElementById("callgraphs");\n'\
	'		if(!cglist) return;\n'\
	'		var cg = cglist.getElementsByClassName("atop");\n'\
	'		if(cg.length < 10) return;\n'\
	'		for (var i = 0; i < cg.length; i++) {\n'\
	'			cgid = cg[i].id.split("x")[0]\n'\
	'			if(idlist.indexOf(cgid) >= 0) {\n'\
	'				cg[i].style.display = "block";\n'\
	'			} else {\n'\
	'				cg[i].style.display = "none";\n'\
	'			}\n'\
	'		}\n'\
	'	}\n'\
	'	function callDetail(devid, devtitle) {\n'\
	'		if(!(devid in devstats) || devstats[devid].length < 1)\n'\
	'			return;\n'\
	'		var list = devstats[devid];\n'\
	'		var tmp = devtitle.split(" ");\n'\
	'		var name = tmp[0], phase = tmp[tmp.length-1];\n'\
	'		var dd = document.getElementById(phase);\n'\
	'		var total = parseFloat(tmp[1].slice(1));\n'\
	'		var mlist = [];\n'\
	'		var maxlen = 0;\n'\
	'		var info = []\n'\
	'		for(var i in list) {\n'\
	'			if(list[i][0] == "@") {\n'\
	'				info = list[i].split("|");\n'\
	'				continue;\n'\
	'			}\n'\
	'			var tmp = list[i].split("|");\n'\
	'			var t = parseFloat(tmp[0]), f = tmp[1], c = parseInt(tmp[2]);\n'\
	'			var p = (t*100.0/total).toFixed(2);\n'\
	'			mlist[mlist.length] = [f, c, t.toFixed(2), p+"%"];\n'\
	'			if(f.length > maxlen)\n'\
	'				maxlen = f.length;\n'\
	'		}\n'\
	'		var pad = 5;\n'\
	'		if(mlist.length == 0) pad = 30;\n'\
	'		var html = \'<div style="padding-top:\'+pad+\'px"><t3> <b>\'+name+\':</b>\';\n'\
	'		if(info.length > 2)\n'\
	'			html += " start=<b>"+info[1]+"</b>, end=<b>"+info[2]+"</b>";\n'\
	'		if(info.length > 3)\n'\
	'			html += ", length<i>(w/o overhead)</i>=<b>"+info[3]+" ms</b>";\n'\
	'		if(info.length > 4)\n'\
	'			html += ", return=<b>"+info[4]+"</b>";\n'\
	'		html += "</t3></div>";\n'\
	'		if(mlist.length > 0) {\n'\
	'			html += \'<table class=fstat style="padding-top:\'+(maxlen*5)+\'px;"><tr><th>Function</th>\';\n'\
	'			for(var i in mlist)\n'\
	'				html += "<td class=vt>"+mlist[i][0]+"</td>";\n'\
	'			html += "</tr><tr><th>Calls</th>";\n'\
	'			for(var i in mlist)\n'\
	'				html += "<td>"+mlist[i][1]+"</td>";\n'\
	'			html += "</tr><tr><th>Time(ms)</th>";\n'\
	'			for(var i in mlist)\n'\
	'				html += "<td>"+mlist[i][2]+"</td>";\n'\
	'			html += "</tr><tr><th>Percent</th>";\n'\
	'			for(var i in mlist)\n'\
	'				html += "<td>"+mlist[i][3]+"</td>";\n'\
	'			html += "</tr></table>";\n'\
	'		}\n'\
	'		dd.innerHTML = html;\n'\
	'		var height = (maxlen*5)+100;\n'\
	'		dd.style.height = height+"px";\n'\
	'		document.getElementById("devicedetail").style.height = height+"px";\n'\
	'	}\n'\
	'	function callSelect() {\n'\
	'		var cglist = document.getElementById("callgraphs");\n'\
	'		if(!cglist) return;\n'\
	'		var cg = cglist.getElementsByClassName("atop");\n'\
	'		for (var i = 0; i < cg.length; i++) {\n'\
	'			if(this.id == cg[i].id) {\n'\
	'				cg[i].style.display = "block";\n'\
	'			} else {\n'\
	'				cg[i].style.display = "none";\n'\
	'			}\n'\
	'		}\n'\
	'	}\n'\
	'	function devListWindow(e) {\n'\
	'		var win = window.open();\n'\
	'		var html = "<title>"+e.target.innerHTML+"</title>"+\n'\
	'			"<style type=\\"text/css\\">"+\n'\
	'			"   ul {list-style-type:circle;padding-left:10px;margin-left:10px;}"+\n'\
	'			"</style>"\n'\
	'		var dt = devtable[0];\n'\
	'		if(e.target.id != "devlist1")\n'\
	'			dt = devtable[1];\n'\
	'		win.document.write(html+dt);\n'\
	'	}\n'\
	'	function errWindow() {\n'\
	'		var range = this.id.split("_");\n'\
	'		var idx1 = parseInt(range[0]);\n'\
	'		var idx2 = parseInt(range[1]);\n'\
	'		var win = window.open();\n'\
	'		var log = document.getElementById("dmesglog");\n'\
	'		var title = "<title>dmesg log</title>";\n'\
	'		var text = log.innerHTML.split("\\n");\n'\
	'		var html = "";\n'\
	'		for(var i = 0; i < text.length; i++) {\n'\
	'			if(i == idx1) {\n'\
	'				html += "<e id=target>"+text[i]+"</e>\\n";\n'\
	'			} else if(i > idx1 && i <= idx2) {\n'\
	'				html += "<e>"+text[i]+"</e>\\n";\n'\
	'			} else {\n'\
	'				html += text[i]+"\\n";\n'\
	'			}\n'\
	'		}\n'\
	'		win.document.write("<style>e{color:red}</style>"+title+"<pre>"+html+"</pre>");\n'\
	'		win.location.hash = "";\n'\
	'		win.document.close();\n'\
	'	}\n'\
	'	function logWindow(e) {\n'\
	'		var name = e.target.id.slice(4);\n'\
	'		var win = window.open();\n'\
	'		var log = document.getElementById(name+"log");\n'\
	'		var title = "<title>"+document.title.split(" ")[0]+" "+name+" log</title>";\n'\
	'		win.document.write(title+"<pre>"+log.innerHTML+"</pre>");\n'\
	'		win.document.close();\n'\
	'	}\n'\
	'	function onMouseDown(e) {\n'\
	'		dragval[0] = e.clientX;\n'\
	'		dragval[1] = document.getElementById("dmesgzoombox").scrollLeft;\n'\
	'		document.onmousemove = onMouseMove;\n'\
	'	}\n'\
	'	function onMouseMove(e) {\n'\
	'		var zoombox = document.getElementById("dmesgzoombox");\n'\
	'		zoombox.scrollLeft = dragval[1] + dragval[0] - e.clientX;\n'\
	'	}\n'\
	'	function onMouseUp(e) {\n'\
	'		document.onmousemove = null;\n'\
	'	}\n'\
	'	function onKeyPress(e) {\n'\
	'		var c = e.charCode;\n'\
	'		if(c != 42 && c != 43 && c != 45) return;\n'\
	'		var click = document.createEvent("Events");\n'\
	'		click.initEvent("click", true, false);\n'\
	'		if(c == 43)  \n'\
	'			document.getElementById("zoomin").dispatchEvent(click);\n'\
	'		else if(c == 45)\n'\
	'			document.getElementById("zoomout").dispatchEvent(click);\n'\
	'		else if(c == 42)\n'\
	'			document.getElementById("zoomdef").dispatchEvent(click);\n'\
	'	}\n'\
	'	window.addEventListener("resize", function () {zoomTimeline();});\n'\
	'	window.addEventListener("load", function () {\n'\
	'		var dmesg = document.getElementById("dmesg");\n'\
	'		dmesg.style.width = "100%"\n'\
	'		dmesg.onmousedown = onMouseDown;\n'\
	'		document.onmouseup = onMouseUp;\n'\
	'		document.onkeypress = onKeyPress;\n'\
	'		document.getElementById("zoomin").onclick = zoomTimeline;\n'\
	'		document.getElementById("zoomout").onclick = zoomTimeline;\n'\
	'		document.getElementById("zoomdef").onclick = zoomTimeline;\n'\
	'		var list = document.getElementsByClassName("err");\n'\
	'		for (var i = 0; i < list.length; i++)\n'\
	'			list[i].onclick = errWindow;\n'\
	'		var list = document.getElementsByClassName("logbtn");\n'\
	'		for (var i = 0; i < list.length; i++)\n'\
	'			list[i].onclick = logWindow;\n'\
	'		list = document.getElementsByClassName("devlist");\n'\
	'		for (var i = 0; i < list.length; i++)\n'\
	'			list[i].onclick = devListWindow;\n'\
	'		var dev = dmesg.getElementsByClassName("thread");\n'\
	'		for (var i = 0; i < dev.length; i++) {\n'\
	'			dev[i].onclick = deviceDetail;\n'\
	'			dev[i].onmouseover = deviceHover;\n'\
	'			dev[i].onmouseout = deviceUnhover;\n'\
	'		}\n'\
	'		var dev = dmesg.getElementsByClassName("srccall");\n'\
	'		for (var i = 0; i < dev.length; i++)\n'\
	'			dev[i].onclick = callSelect;\n'\
	'		zoomTimeline();\n'\
	'	});\n'\
	'</script>\n'
	hf.write(script_code);

def setRuntimeSuspend(before=True):
	global sysvals
	sv = sysvals
	if sv.rs == 0:
		return
	if before:
		
		if sv.rs > 0:
			sv.rstgt, sv.rsval, sv.rsdir = 'on', 'auto', 'enabled'
		else:
			sv.rstgt, sv.rsval, sv.rsdir = 'auto', 'on', 'disabled'
		pprint('CONFIGURING RUNTIME SUSPEND...')
		sv.rslist = deviceInfo(sv.rstgt)
		for i in sv.rslist:
			sv.setVal(sv.rsval, i)
		pprint('runtime suspend %s on all devices (%d changed)' % (sv.rsdir, len(sv.rslist)))
		pprint('waiting 5 seconds...')
		time.sleep(5)
	else:
		
		for i in sv.rslist:
			sv.setVal(sv.rstgt, i)
		pprint('runtime suspend settings restored on %d devices' % len(sv.rslist))





def executeSuspend(quiet=False):
	pm = ProcessMonitor()
	tp = sysvals.tpath
	if sysvals.wifi:
		wifi = sysvals.checkWifi()
	testdata = []
	
	if sysvals.display:
		if not quiet:
			pprint('SET DISPLAY TO %s' % sysvals.display.upper())
		displayControl(sysvals.display)
		time.sleep(1)
	if sysvals.sync:
		if not quiet:
			pprint('SYNCING FILESYSTEMS')
		call('sync', shell=True)
	
	sysvals.initdmesg()
	
	if(sysvals.usecallgraph or sysvals.usetraceevents):
		if not quiet:
			pprint('START TRACING')
		sysvals.fsetVal('1', 'tracing_on')
		if sysvals.useprocmon:
			pm.start()
	sysvals.cmdinfo(True)
	
	for count in range(1,sysvals.execcount+1):
		
		if(count > 1 and sysvals.x2delay > 0):
			sysvals.fsetVal('WAIT %d' % sysvals.x2delay, 'trace_marker')
			time.sleep(sysvals.x2delay/1000.0)
			sysvals.fsetVal('WAIT END', 'trace_marker')
		
		if sysvals.testcommand != '':
			pprint('COMMAND START')
		else:
			if(sysvals.rtcwake):
				pprint('SUSPEND START')
			else:
				pprint('SUSPEND START (press a key to resume)')
		
		if(sysvals.rtcwake):
			if not quiet:
				pprint('will issue an rtcwake in %d seconds' % sysvals.rtcwaketime)
			sysvals.rtcWakeAlarmOn()
		
		if(sysvals.usecallgraph or sysvals.usetraceevents):
			sysvals.fsetVal(datetime.now().strftime(sysvals.tmstart), 'trace_marker')
		
		if(count == 1 and sysvals.predelay > 0):
			sysvals.fsetVal('WAIT %d' % sysvals.predelay, 'trace_marker')
			time.sleep(sysvals.predelay/1000.0)
			sysvals.fsetVal('WAIT END', 'trace_marker')
		
		tdata = {'error': ''}
		if sysvals.testcommand != '':
			res = call(sysvals.testcommand+' 2>&1', shell=True);
			if res != 0:
				tdata['error'] = 'cmd returned %d' % res
		else:
			mode = sysvals.suspendmode
			if sysvals.memmode and os.path.exists(sysvals.mempowerfile):
				mode = 'mem'
				pf = open(sysvals.mempowerfile, 'w')
				pf.write(sysvals.memmode)
				pf.close()
			if sysvals.diskmode and os.path.exists(sysvals.diskpowerfile):
				mode = 'disk'
				pf = open(sysvals.diskpowerfile, 'w')
				pf.write(sysvals.diskmode)
				pf.close()
			if mode == 'freeze' and sysvals.haveTurbostat():
				
				turbo = sysvals.turbostat()
				if turbo:
					tdata['turbo'] = turbo
			else:
				pf = open(sysvals.powerfile, 'w')
				pf.write(mode)
				
				try:
					pf.close()
				except Exception as e:
					tdata['error'] = str(e)
		if(sysvals.rtcwake):
			sysvals.rtcWakeAlarmOff()
		
		if(count == sysvals.execcount and sysvals.postdelay > 0):
			sysvals.fsetVal('WAIT %d' % sysvals.postdelay, 'trace_marker')
			time.sleep(sysvals.postdelay/1000.0)
			sysvals.fsetVal('WAIT END', 'trace_marker')
		
		pprint('RESUME COMPLETE')
		if(sysvals.usecallgraph or sysvals.usetraceevents):
			sysvals.fsetVal(datetime.now().strftime(sysvals.tmend), 'trace_marker')
		if sysvals.wifi and wifi:
			tdata['wifi'] = sysvals.pollWifi(wifi)
		if(sysvals.suspendmode == 'mem' or sysvals.suspendmode == 'command'):
			tdata['fw'] = getFPDT(False)
		testdata.append(tdata)
	cmdafter = sysvals.cmdinfo(False)
	
	if(sysvals.usecallgraph or sysvals.usetraceevents):
		if sysvals.useprocmon:
			pm.stop()
		sysvals.fsetVal('0', 'tracing_on')
	
	if not quiet:
		pprint('CAPTURING DMESG')
	sysvals.getdmesg(testdata)
	
	if(sysvals.usecallgraph or sysvals.usetraceevents):
		if not quiet:
			pprint('CAPTURING TRACE')
		op = sysvals.writeDatafileHeader(sysvals.ftracefile, testdata)
		fp = open(tp+'trace', 'r')
		for line in fp:
			op.write(line)
		op.close()
		sysvals.fsetVal('', 'trace')
		sysvals.platforminfo(cmdafter)

def readFile(file):
	if os.path.islink(file):
		return os.readlink(file).split('/')[-1]
	else:
		return sysvals.getVal(file).strip()





"1901m16s"
def ms2nice(val):
	val = int(val)
	h = val // 3600000
	m = (val // 60000) % 60
	s = (val // 1000) % 60
	if h > 0:
		return '%d:%02d:%02d' % (h, m, s)
	if m > 0:
		return '%02d:%02d' % (m, s)
	return '%ds' % s

def yesno(val):
	list = {'enabled':'A', 'disabled':'S', 'auto':'E', 'on':'D',
		'active':'A', 'suspended':'S', 'suspending':'S'}
	if val not in list:
		return ' '
	return list[val]





def deviceInfo(output=''):
	if not output:
		pprint('LEGEND\n'\
		'---------------------------------------------------------------------------------------------\n'\
		'  A = async/sync PM queue (A/S)               C = runtime active children\n'\
		'  R = runtime suspend enabled/disabled (E/D)  rACTIVE = runtime active (min/sec)\n'\
		'  S = runtime status active/suspended (A/S)   rSUSPEND = runtime suspend (min/sec)\n'\
		'  U = runtime usage count\n'\
		'---------------------------------------------------------------------------------------------\n'\
		'DEVICE                     NAME                       A R S U C    rACTIVE   rSUSPEND\n'\
		'---------------------------------------------------------------------------------------------')

	res = []
	tgtval = 'runtime_status'
	lines = dict()
	for dirname, dirnames, filenames in os.walk('/sys/devices'):
		if(not re.match('.*/power', dirname) or
			'control' not in filenames or
			tgtval not in filenames):
			continue
		name = ''
		dirname = dirname[:-6]
		device = dirname.split('/')[-1]
		power = dict()
		power[tgtval] = readFile('%s/power/%s' % (dirname, tgtval))
		
		if power[tgtval] not in ['active', 'suspended', 'suspending']:
			continue
		for i in ['product', 'driver', 'subsystem']:
			file = '%s/%s' % (dirname, i)
			if os.path.exists(file):
				name = readFile(file)
				break
		for i in ['async', 'control', 'runtime_status', 'runtime_usage',
			'runtime_active_kids', 'runtime_active_time',
			'runtime_suspended_time']:
			if i in filenames:
				power[i] = readFile('%s/power/%s' % (dirname, i))
		if output:
			if power['control'] == output:
				res.append('%s/power/control' % dirname)
			continue
		lines[dirname] = '%-26s %-26s %1s %1s %1s %1s %1s %10s %10s' % \
			(device[:26], name[:26],
			yesno(power['async']), \
			yesno(power['control']), \
			yesno(power['runtime_status']), \
			power['runtime_usage'], \
			power['runtime_active_kids'], \
			ms2nice(power['runtime_active_time']), \
			ms2nice(power['runtime_suspended_time']))
	for i in sorted(lines):
		print(lines[i])
	return res






def getModes():
	modes = []
	if(os.path.exists(sysvals.powerfile)):
		fp = open(sysvals.powerfile, 'r')
		modes = fp.read().split()
		fp.close()
	if(os.path.exists(sysvals.mempowerfile)):
		deep = False
		fp = open(sysvals.mempowerfile, 'r')
		for m in fp.read().split():
			memmode = m.strip('[]')
			if memmode == 'deep':
				deep = True
			else:
				modes.append('mem-%s' % memmode)
		fp.close()
		if 'mem' in modes and not deep:
			modes.remove('mem')
	if('disk' in modes and os.path.exists(sysvals.diskpowerfile)):
		fp = open(sysvals.diskpowerfile, 'r')
		for m in fp.read().split():
			modes.append('disk-%s' % m.strip('[]'))
		fp.close()
	return modes









def dmidecode(mempath, fatal=False):
	out = dict()

	
	info = {
		'bios-vendor': (0, 4),
		'bios-version': (0, 5),
		'bios-release-date': (0, 8),
		'system-manufacturer': (1, 4),
		'system-product-name': (1, 5),
		'system-version': (1, 6),
		'system-serial-number': (1, 7),
		'baseboard-manufacturer': (2, 4),
		'baseboard-product-name': (2, 5),
		'baseboard-version': (2, 6),
		'baseboard-serial-number': (2, 7),
		'chassis-manufacturer': (3, 4),
		'chassis-type': (3, 5),
		'chassis-version': (3, 6),
		'chassis-serial-number': (3, 7),
		'processor-manufacturer': (4, 7),
		'processor-version': (4, 16),
	}
	if(not os.path.exists(mempath)):
		if(fatal):
			doError('file does not exist: %s' % mempath)
		return out
	if(not os.access(mempath, os.R_OK)):
		if(fatal):
			doError('file is not readable: %s' % mempath)
		return out

	
	memaddr = 0xf0000
	memsize = 0x10000
	for ep in ['/sys/firmware/efi/systab', '/proc/efi/systab']:
		if not os.path.exists(ep) or not os.access(ep, os.R_OK):
			continue
		fp = open(ep, 'r')
		buf = fp.read()
		fp.close()
		i = buf.find('SMBIOS=')
		if i >= 0:
			try:
				memaddr = int(buf[i+7:], 16)
				memsize = 0x20
			except:
				continue

	
	try:
		fp = open(mempath, 'rb')
		fp.seek(memaddr)
		buf = fp.read(memsize)
	except:
		if(fatal):
			doError('DMI table is unreachable, sorry')
		else:
			pprint('WARNING: /dev/mem is not readable, ignoring DMI data')
			return out
	fp.close()

	
	i = base = length = num = 0
	while(i < memsize):
		if buf[i:i+4] == b'_SM_' and i < memsize - 16:
			length = struct.unpack('H', buf[i+22:i+24])[0]
			base, num = struct.unpack('IH', buf[i+24:i+30])
			break
		elif buf[i:i+5] == b'_DMI_':
			length = struct.unpack('H', buf[i+6:i+8])[0]
			base, num = struct.unpack('IH', buf[i+8:i+14])
			break
		i += 16
	if base == 0 and length == 0 and num == 0:
		if(fatal):
			doError('Neither SMBIOS nor DMI were found')
		else:
			return out

	
	try:
		fp = open(mempath, 'rb')
		fp.seek(base)
		buf = fp.read(length)
	except:
		if(fatal):
			doError('DMI table is unreachable, sorry')
		else:
			pprint('WARNING: /dev/mem is not readable, ignoring DMI data')
			return out
	fp.close()

	
	count = i = 0
	while(count < num and i <= len(buf) - 4):
		type, size, handle = struct.unpack('BBH', buf[i:i+4])
		n = i + size
		while n < len(buf) - 1:
			if 0 == struct.unpack('H', buf[n:n+2])[0]:
				break
			n += 1
		data = buf[i+size:n+2].split(b'\0')
		for name in info:
			itype, idxadr = info[name]
			if itype == type:
				idx = struct.unpack('B', buf[i+idxadr:i+idxadr+1])[0]
				if idx > 0 and idx < len(data) - 1:
					s = data[idx-1].decode('utf-8')
					if s.strip() and s.strip().lower() != 'to be filled by o.e.m.':
						out[name] = s
		i = n + 2
		count += 1
	return out

def displayControl(cmd):
	xset, ret = 'timeout 10 xset -d :0.0 {0}', 0
	if sysvals.sudouser:
		xset = 'sudo -u %s %s' % (sysvals.sudouser, xset)
	if cmd == 'init':
		ret = call(xset.format('dpms 0 0 0'), shell=True)
		if not ret:
			ret = call(xset.format('s off'), shell=True)
	elif cmd == 'reset':
		ret = call(xset.format('s reset'), shell=True)
	elif cmd in ['on', 'off', 'standby', 'suspend']:
		b4 = displayControl('stat')
		ret = call(xset.format('dpms force %s' % cmd), shell=True)
		if not ret:
			curr = displayControl('stat')
			sysvals.vprint('Display Switched: %s -> %s' % (b4, curr))
			if curr != cmd:
				sysvals.vprint('WARNING: Display failed to change to %s' % cmd)
		if ret:
			sysvals.vprint('WARNING: Display failed to change to %s with xset' % cmd)
			return ret
	elif cmd == 'stat':
		fp = Popen(xset.format('q').split(' '), stdout=PIPE).stdout
		ret = 'unknown'
		for line in fp:
			m = re.match('[\s]*Monitor is (?P<m>.*)', ascii(line))
			if(m and len(m.group('m')) >= 2):
				out = m.group('m').lower()
				ret = out[3:] if out[0:2] == 'in' else out
				break
		fp.close()
	return ret






def getFPDT(output):
	rectype = {}
	rectype[0] = 'Firmware Basic Boot Performance Record'
	rectype[1] = 'S3 Performance Table Record'
	prectype = {}
	prectype[0] = 'Basic S3 Resume Performance Record'
	prectype[1] = 'Basic S3 Suspend Performance Record'

	sysvals.rootCheck(True)
	if(not os.path.exists(sysvals.fpdtpath)):
		if(output):
			doError('file does not exist: %s' % sysvals.fpdtpath)
		return False
	if(not os.access(sysvals.fpdtpath, os.R_OK)):
		if(output):
			doError('file is not readable: %s' % sysvals.fpdtpath)
		return False
	if(not os.path.exists(sysvals.mempath)):
		if(output):
			doError('file does not exist: %s' % sysvals.mempath)
		return False
	if(not os.access(sysvals.mempath, os.R_OK)):
		if(output):
			doError('file is not readable: %s' % sysvals.mempath)
		return False

	fp = open(sysvals.fpdtpath, 'rb')
	buf = fp.read()
	fp.close()

	if(len(buf) < 36):
		if(output):
			doError('Invalid FPDT table data, should '+\
				'be at least 36 bytes')
		return False

	table = struct.unpack('4sIBB6s8sI4sI', buf[0:36])
	if(output):
		pprint('\n'\
		'Firmware Performance Data Table (%s)\n'\
		'                  Signature : %s\n'\
		'               Table Length : %u\n'\
		'                   Revision : %u\n'\
		'                   Checksum : 0x%x\n'\
		'                     OEM ID : %s\n'\
		'               OEM Table ID : %s\n'\
		'               OEM Revision : %u\n'\
		'                 Creator ID : %s\n'\
		'           Creator Revision : 0x%x\n'\
		'' % (ascii(table[0]), ascii(table[0]), table[1], table[2],
			table[3], ascii(table[4]), ascii(table[5]), table[6],
			ascii(table[7]), table[8]))

	if(table[0] != b'FPDT'):
		if(output):
			doError('Invalid FPDT table')
		return False
	if(len(buf) <= 36):
		return False
	i = 0
	fwData = [0, 0]
	records = buf[36:]
	try:
		fp = open(sysvals.mempath, 'rb')
	except:
		pprint('WARNING: /dev/mem is not readable, ignoring the FPDT data')
		return False
	while(i < len(records)):
		header = struct.unpack('HBB', records[i:i+4])
		if(header[0] not in rectype):
			i += header[1]
			continue
		if(header[1] != 16):
			i += header[1]
			continue
		addr = struct.unpack('Q', records[i+8:i+16])[0]
		try:
			fp.seek(addr)
			first = fp.read(8)
		except:
			if(output):
				pprint('Bad address 0x%x in %s' % (addr, sysvals.mempath))
			return [0, 0]
		rechead = struct.unpack('4sI', first)
		recdata = fp.read(rechead[1]-8)
		if(rechead[0] == b'FBPT'):
			record = struct.unpack('HBBIQQQQQ', recdata[:48])
			if(output):
				pprint('%s (%s)\n'\
				'                  Reset END : %u ns\n'\
				'  OS Loader LoadImage Start : %u ns\n'\
				' OS Loader StartImage Start : %u ns\n'\
				'     ExitBootServices Entry : %u ns\n'\
				'      ExitBootServices Exit : %u ns'\
				'' % (rectype[header[0]], ascii(rechead[0]), record[4], record[5],
					record[6], record[7], record[8]))
		elif(rechead[0] == b'S3PT'):
			if(output):
				pprint('%s (%s)' % (rectype[header[0]], ascii(rechead[0])))
			j = 0
			while(j < len(recdata)):
				prechead = struct.unpack('HBB', recdata[j:j+4])
				if(prechead[0] not in prectype):
					continue
				if(prechead[0] == 0):
					record = struct.unpack('IIQQ', recdata[j:j+prechead[1]])
					fwData[1] = record[2]
					if(output):
						pprint('    %s\n'\
						'               Resume Count : %u\n'\
						'                 FullResume : %u ns\n'\
						'              AverageResume : %u ns'\
						'' % (prectype[prechead[0]], record[1],
								record[2], record[3]))
				elif(prechead[0] == 1):
					record = struct.unpack('QQ', recdata[j+4:j+prechead[1]])
					fwData[0] = record[1] - record[0]
					if(output):
						pprint('    %s\n'\
						'               SuspendStart : %u ns\n'\
						'                 SuspendEnd : %u ns\n'\
						'                SuspendTime : %u ns'\
						'' % (prectype[prechead[0]], record[0],
								record[1], fwData[0]))

				j += prechead[1]
		if(output):
			pprint('')
		i += header[1]
	fp.close()
	return fwData







def statusCheck(probecheck=False):
	status = ''

	pprint('Checking this system (%s)...' % platform.node())

	
	res = sysvals.colorText('NO (No features of this tool will work!)')
	if(sysvals.rootCheck(False)):
		res = 'YES'
	pprint('    have root access: %s' % res)
	if(res != 'YES'):
		pprint('    Try running this script with sudo')
		return 'missing root access'

	
	res = sysvals.colorText('NO (No features of this tool will work!)')
	if(os.path.exists(sysvals.powerfile)):
		res = 'YES'
	pprint('    is sysfs mounted: %s' % res)
	if(res != 'YES'):
		return 'sysfs is missing'

	
	if sysvals.suspendmode != 'command':
		res = sysvals.colorText('NO')
		modes = getModes()
		if(sysvals.suspendmode in modes):
			res = 'YES'
		else:
			status = '%s mode is not supported' % sysvals.suspendmode
		pprint('    is "%s" a valid power mode: %s' % (sysvals.suspendmode, res))
		if(res == 'NO'):
			pprint('      valid power modes are: %s' % modes)
			pprint('      please choose one with -m')

	
	res = sysvals.colorText('NO')
	ftgood = sysvals.verifyFtrace()
	if(ftgood):
		res = 'YES'
	elif(sysvals.usecallgraph):
		status = 'ftrace is not properly supported'
	pprint('    is ftrace supported: %s' % res)

	
	if sysvals.usekprobes:
		res = sysvals.colorText('NO')
		sysvals.usekprobes = sysvals.verifyKprobes()
		if(sysvals.usekprobes):
			res = 'YES'
		else:
			sysvals.usedevsrc = False
		pprint('    are kprobes supported: %s' % res)

	
	res = 'DMESG'
	if(ftgood):
		sysvals.usetraceevents = True
		for e in sysvals.traceevents:
			if not os.path.exists(sysvals.epath+e):
				sysvals.usetraceevents = False
		if(sysvals.usetraceevents):
			res = 'FTRACE (all trace events found)'
	pprint('    timeline data source: %s' % res)

	
	res = sysvals.colorText('NO')
	if(sysvals.rtcpath != ''):
		res = 'YES'
	elif(sysvals.rtcwake):
		status = 'rtcwake is not properly supported'
	pprint('    is rtcwake supported: %s' % res)

	
	pprint('    optional commands this tool may use for info:')
	no = sysvals.colorText('MISSING')
	yes = sysvals.colorText('FOUND', 32)
	for c in ['turbostat', 'mcelog', 'lspci', 'lsusb']:
		if c == 'turbostat':
			res = yes if sysvals.haveTurbostat() else no
		else:
			res = yes if sysvals.getExec(c) else no
		pprint('        %s: %s' % (c, res))

	if not probecheck:
		return status

	
	if sysvals.usekprobes:
		for name in sysvals.tracefuncs:
			sysvals.defaultKprobe(name, sysvals.tracefuncs[name])
		if sysvals.usedevsrc:
			for name in sysvals.dev_tracefuncs:
				sysvals.defaultKprobe(name, sysvals.dev_tracefuncs[name])
		sysvals.addKprobes(True)

	return status







def doError(msg, help=False):
	if(help == True):
		printHelp()
	pprint('ERROR: %s\n' % msg)
	sysvals.outputResult({'error':msg})
	sys.exit(1)




def getArgInt(name, args, min, max, main=True):
	if main:
		try:
			arg = next(args)
		except:
			doError(name+': no argument supplied', True)
	else:
		arg = args
	try:
		val = int(arg)
	except:
		doError(name+': non-integer value given', True)
	if(val < min or val > max):
		doError(name+': value should be between %d and %d' % (min, max), True)
	return val




def getArgFloat(name, args, min, max, main=True):
	if main:
		try:
			arg = next(args)
		except:
			doError(name+': no argument supplied', True)
	else:
		arg = args
	try:
		val = float(arg)
	except:
		doError(name+': non-numerical value given', True)
	if(val < min or val > max):
		doError(name+': value should be between %f and %f' % (min, max), True)
	return val

def processData(live=False, quiet=False):
	if not quiet:
		pprint('PROCESSING DATA')
	sysvals.vprint('usetraceevents=%s, usetracemarkers=%s, usekprobes=%s' % \
		(sysvals.usetraceevents, sysvals.usetracemarkers, sysvals.usekprobes))
	error = ''
	if(sysvals.usetraceevents):
		testruns, error = parseTraceLog(live)
		if sysvals.dmesgfile:
			for data in testruns:
				data.extractErrorInfo()
	else:
		testruns = loadKernelLog()
		for data in testruns:
			parseKernelLog(data)
		if(sysvals.ftracefile and (sysvals.usecallgraph or sysvals.usetraceevents)):
			appendIncompleteTraceLog(testruns)
	if not sysvals.stamp:
		pprint('ERROR: data does not include the expected stamp')
		return (testruns, {'error': 'timeline generation failed'})
	shown = ['bios', 'biosdate', 'cpu', 'host', 'kernel', 'man', 'memfr',
			'memsz', 'mode', 'numcpu', 'plat', 'time', 'wifi']
	sysvals.vprint('System Info:')
	for key in sorted(sysvals.stamp):
		if key in shown:
			sysvals.vprint('    %-8s : %s' % (key.upper(), sysvals.stamp[key]))
	sysvals.vprint('Command:\n    %s' % sysvals.cmdline)
	for data in testruns:
		if data.turbostat:
			idx, s = 0, 'Turbostat:\n    '
			for val in data.turbostat.split('|'):
				idx += len(val) + 1
				if idx >= 80:
					idx = 0
					s += '\n    '
				s += val + ' '
			sysvals.vprint(s)
		data.printDetails()
	if len(sysvals.platinfo) > 0:
		sysvals.vprint('\nPlatform Info:')
		for info in sysvals.platinfo:
			sysvals.vprint('[%s - %s]' % (info[0], info[1]))
			sysvals.vprint(info[2])
		sysvals.vprint('')
	if sysvals.cgdump:
		for data in testruns:
			data.debugPrint()
		sys.exit(0)
	if len(testruns) < 1:
		pprint('ERROR: Not enough test data to build a timeline')
		return (testruns, {'error': 'timeline generation failed'})
	sysvals.vprint('Creating the html timeline (%s)...' % sysvals.htmlfile)
	createHTML(testruns, error)
	if not quiet:
		pprint('DONE')
	data = testruns[0]
	stamp = data.stamp
	stamp['suspend'], stamp['resume'] = data.getTimeValues()
	if data.fwValid:
		stamp['fwsuspend'], stamp['fwresume'] = data.fwSuspend, data.fwResume
	if error:
		stamp['error'] = error
	return (testruns, stamp)




def rerunTest(htmlfile=''):
	if sysvals.ftracefile:
		doesTraceLogHaveTraceEvents()
	if not sysvals.dmesgfile and not sysvals.usetraceevents:
		doError('recreating this html output requires a dmesg file')
	if htmlfile:
		sysvals.htmlfile = htmlfile
	else:
		sysvals.setOutputFile()
	if os.path.exists(sysvals.htmlfile):
		if not os.path.isfile(sysvals.htmlfile):
			doError('a directory already exists with this name: %s' % sysvals.htmlfile)
		elif not os.access(sysvals.htmlfile, os.W_OK):
			doError('missing permission to write to %s' % sysvals.htmlfile)
	testruns, stamp = processData()
	sysvals.resetlog()
	return stamp




def runTest(n=0, quiet=False):
	
	sysvals.initFtrace(quiet)
	sysvals.initTestOutput('suspend')

	
	executeSuspend(quiet)
	sysvals.cleanupFtrace()
	if sysvals.skiphtml:
		sysvals.outputResult({}, n)
		sysvals.sudoUserchown(sysvals.testdir)
		return
	testruns, stamp = processData(True, quiet)
	for data in testruns:
		del data
	sysvals.sudoUserchown(sysvals.testdir)
	sysvals.outputResult(stamp, n)
	if 'error' in stamp:
		return 2
	return 0

def find_in_html(html, start, end, firstonly=True):
	n, cnt, out = 0, len(html), []
	while n < cnt:
		e = cnt if (n + 10000 > cnt or n == 0) else n + 10000
		m = re.search(start, html[n:e])
		if not m:
			break
		i = m.end()
		m = re.search(end, html[n+i:e])
		if not m:
			break
		j = m.start()
		str = html[n+i:n+i+j]
		if end == 'ms':
			num = re.search(r'[-+]?\d*\.\d+|\d+', str)
			str = num.group() if num else 'NaN'
		if firstonly:
			return str
		out.append(str)
		n += i+j
	if firstonly:
		return ''
	return out

def data_from_html(file, outpath, issues, fulldetail=False):
	html = open(file, 'r').read()
	sysvals.htmlfile = os.path.relpath(file, outpath)
	
	suspend = find_in_html(html, 'Kernel Suspend', 'ms')
	resume = find_in_html(html, 'Kernel Resume', 'ms')
	sysinfo = find_in_html(html, '<div class="stamp sysinfo">', '</div>')
	line = find_in_html(html, '<div class="stamp">', '</div>')
	stmp = line.split()
	if not suspend or not resume or len(stmp) != 8:
		return False
	try:
		dt = datetime.strptime(' '.join(stmp[3:]), '%B %d %Y, %I:%M:%S %p')
	except:
		return False
	sysvals.hostname = stmp[0]
	tstr = dt.strftime('%Y/%m/%d %H:%M:%S')
	error = find_in_html(html, '<table class="testfail"><tr><td>', '</td>')
	if error:
		m = re.match('[a-z0-9]* failed in (?P<p>\S*).*', error)
		if m:
			result = 'fail in %s' % m.group('p')
		else:
			result = 'fail'
	else:
		result = 'pass'
	
	ilist = []
	extra = dict()
	log = find_in_html(html, '<div id="dmesglog" style="display:none;">',
		'</div>').strip()
	if log:
		d = Data(0)
		d.end = 999999999
		d.dmesgtext = log.split('\n')
		msglist = d.extractErrorInfo()
		for msg in msglist:
			sysvals.errorSummary(issues, msg)
		if stmp[2] == 'freeze':
			extra = d.turbostatInfo()
		elist = dict()
		for dir in d.errorinfo:
			for err in d.errorinfo[dir]:
				if err[0] not in elist:
					elist[err[0]] = 0
				elist[err[0]] += 1
		for i in elist:
			ilist.append('%sx%d' % (i, elist[i]) if elist[i] > 1 else i)
	wifi = find_in_html(html, 'Wifi Resume: ', '</td>')
	if wifi:
		extra['wifi'] = wifi
	low = find_in_html(html, 'freeze time: <b>', ' ms</b>')
	if low and '|' in low:
		issue = 'FREEZEx%d' % len(low.split('|'))
		match = [i for i in issues if i['match'] == issue]
		if len(match) > 0:
			match[0]['count'] += 1
			if sysvals.hostname not in match[0]['urls']:
				match[0]['urls'][sysvals.hostname] = [sysvals.htmlfile]
			elif sysvals.htmlfile not in match[0]['urls'][sysvals.hostname]:
				match[0]['urls'][sysvals.hostname].append(sysvals.htmlfile)
		else:
			issues.append({
				'match': issue, 'count': 1, 'line': issue,
				'urls': {sysvals.hostname: [sysvals.htmlfile]},
			})
		ilist.append(issue)
	
	devices = dict()
	for line in html.split('\n'):
		m = re.match(' *<div id=\"[a,0-9]*\" *title=\"(?P<title>.*)\" class=\"thread.*', line)
		if not m or 'thread kth' in line or 'thread sec' in line:
			continue
		m = re.match('(?P<n>.*) \((?P<t>[0-9,\.]*) ms\) (?P<p>.*)', m.group('title'))
		if not m:
			continue
		name, time, phase = m.group('n'), m.group('t'), m.group('p')
		if ' async' in name or ' sync' in name:
			name = ' '.join(name.split(' ')[:-1])
		if phase.startswith('suspend'):
			d = 'suspend'
		elif phase.startswith('resume'):
			d = 'resume'
		else:
			continue
		if d not in devices:
			devices[d] = dict()
		if name not in devices[d]:
			devices[d][name] = 0.0
		devices[d][name] += float(time)
	
	worst = dict()
	for d in ['suspend', 'resume']:
		worst[d] = {'name':'', 'time': 0.0}
		dev = devices[d] if d in devices else 0
		if dev and len(dev.keys()) > 0:
			n = sorted(dev, key=lambda k:(dev[k], k), reverse=True)[0]
			worst[d]['name'], worst[d]['time'] = n, dev[n]
	data = {
		'mode': stmp[2],
		'host': stmp[0],
		'kernel': stmp[1],
		'sysinfo': sysinfo,
		'time': tstr,
		'result': result,
		'issues': ' '.join(ilist),
		'suspend': suspend,
		'resume': resume,
		'devlist': devices,
		'sus_worst': worst['suspend']['name'],
		'sus_worsttime': worst['suspend']['time'],
		'res_worst': worst['resume']['name'],
		'res_worsttime': worst['resume']['time'],
		'url': sysvals.htmlfile,
	}
	for key in extra:
		data[key] = extra[key]
	if fulldetail:
		data['funclist'] = find_in_html(html, '<div title="', '" class="traceevent"', False)
	return data

def genHtml(subdir, force=False):
	for dirname, dirnames, filenames in os.walk(subdir):
		sysvals.dmesgfile = sysvals.ftracefile = sysvals.htmlfile = ''
		for filename in filenames:
			file = os.path.join(dirname, filename)
			if sysvals.usable(file):
				if(re.match('.*_dmesg.txt', filename)):
					sysvals.dmesgfile = file
				elif(re.match('.*_ftrace.txt', filename)):
					sysvals.ftracefile = file
		sysvals.setOutputFile()
		if (sysvals.dmesgfile or sysvals.ftracefile) and sysvals.htmlfile and \
			(force or not sysvals.usable(sysvals.htmlfile)):
			pprint('FTRACE: %s' % sysvals.ftracefile)
			if sysvals.dmesgfile:
				pprint('DMESG : %s' % sysvals.dmesgfile)
			rerunTest()




def runSummary(subdir, local=True, genhtml=False):
	inpath = os.path.abspath(subdir)
	outpath = os.path.abspath('.') if local else inpath
	pprint('Generating a summary of folder:\n   %s' % inpath)
	if genhtml:
		genHtml(subdir)
	issues = []
	testruns = []
	desc = {'host':[],'mode':[],'kernel':[]}
	for dirname, dirnames, filenames in os.walk(subdir):
		for filename in filenames:
			if(not re.match('.*.html', filename)):
				continue
			data = data_from_html(os.path.join(dirname, filename), outpath, issues)
			if(not data):
				continue
			testruns.append(data)
			for key in desc:
				if data[key] not in desc[key]:
					desc[key].append(data[key])
	pprint('Summary files:')
	if len(desc['host']) == len(desc['mode']) == len(desc['kernel']) == 1:
		title = '%s %s %s' % (desc['host'][0], desc['kernel'][0], desc['mode'][0])
	else:
		title = inpath
	createHTMLSummarySimple(testruns, os.path.join(outpath, 'summary.html'), title)
	pprint('   summary.html         - tabular list of test data found')
	createHTMLDeviceSummary(testruns, os.path.join(outpath, 'summary-devices.html'), title)
	pprint('   summary-devices.html - kernel device list sorted by total execution time')
	createHTMLIssuesSummary(testruns, issues, os.path.join(outpath, 'summary-issues.html'), title)
	pprint('   summary-issues.html  - kernel issues found sorted by frequency')




def checkArgBool(name, value):
	if value in switchvalues:
		if value in switchoff:
			return False
		return True
	doError('invalid boolean --> (%s: %s), use "true/false" or "1/0"' % (name, value), True)
	return False




def configFromFile(file):
	Config = configparser.ConfigParser()

	Config.read(file)
	sections = Config.sections()
	overridekprobes = False
	overridedevkprobes = False
	if 'Settings' in sections:
		for opt in Config.options('Settings'):
			value = Config.get('Settings', opt).lower()
			option = opt.lower()
			if(option == 'verbose'):
				sysvals.verbose = checkArgBool(option, value)
			elif(option == 'addlogs'):
				sysvals.dmesglog = sysvals.ftracelog = checkArgBool(option, value)
			elif(option == 'dev'):
				sysvals.usedevsrc = checkArgBool(option, value)
			elif(option == 'proc'):
				sysvals.useprocmon = checkArgBool(option, value)
			elif(option == 'x2'):
				if checkArgBool(option, value):
					sysvals.execcount = 2
			elif(option == 'callgraph'):
				sysvals.usecallgraph = checkArgBool(option, value)
			elif(option == 'override-timeline-functions'):
				overridekprobes = checkArgBool(option, value)
			elif(option == 'override-dev-timeline-functions'):
				overridedevkprobes = checkArgBool(option, value)
			elif(option == 'skiphtml'):
				sysvals.skiphtml = checkArgBool(option, value)
			elif(option == 'sync'):
				sysvals.sync = checkArgBool(option, value)
			elif(option == 'rs' or option == 'runtimesuspend'):
				if value in switchvalues:
					if value in switchoff:
						sysvals.rs = -1
					else:
						sysvals.rs = 1
				else:
					doError('invalid value --> (%s: %s), use "enable/disable"' % (option, value), True)
			elif(option == 'display'):
				disopt = ['on', 'off', 'standby', 'suspend']
				if value not in disopt:
					doError('invalid value --> (%s: %s), use %s' % (option, value, disopt), True)
				sysvals.display = value
			elif(option == 'gzip'):
				sysvals.gzip = checkArgBool(option, value)
			elif(option == 'cgfilter'):
				sysvals.setCallgraphFilter(value)
			elif(option == 'cgskip'):
				if value in switchoff:
					sysvals.cgskip = ''
				else:
					sysvals.cgskip = sysvals.configFile(val)
					if(not sysvals.cgskip):
						doError('%s does not exist' % sysvals.cgskip)
			elif(option == 'cgtest'):
				sysvals.cgtest = getArgInt('cgtest', value, 0, 1, False)
			elif(option == 'cgphase'):
				d = Data(0)
				if value not in d.phasedef:
					doError('invalid phase --> (%s: %s), valid phases are %s'\
						% (option, value, d.phasedef.keys()), True)
				sysvals.cgphase = value
			elif(option == 'fadd'):
				file = sysvals.configFile(value)
				if(not file):
					doError('%s does not exist' % value)
				sysvals.addFtraceFilterFunctions(file)
			elif(option == 'result'):
				sysvals.result = value
			elif(option == 'multi'):
				nums = value.split()
				if len(nums) != 2:
					doError('multi requires 2 integers (exec_count and delay)', True)
				sysvals.multiinit(nums[0], nums[1])
			elif(option == 'devicefilter'):
				sysvals.setDeviceFilter(value)
			elif(option == 'expandcg'):
				sysvals.cgexp = checkArgBool(option, value)
			elif(option == 'srgap'):
				if checkArgBool(option, value):
					sysvals.srgap = 5
			elif(option == 'mode'):
				sysvals.suspendmode = value
			elif(option == 'command' or option == 'cmd'):
				sysvals.testcommand = value
			elif(option == 'x2delay'):
				sysvals.x2delay = getArgInt('x2delay', value, 0, 60000, False)
			elif(option == 'predelay'):
				sysvals.predelay = getArgInt('predelay', value, 0, 60000, False)
			elif(option == 'postdelay'):
				sysvals.postdelay = getArgInt('postdelay', value, 0, 60000, False)
			elif(option == 'maxdepth'):
				sysvals.max_graph_depth = getArgInt('maxdepth', value, 0, 1000, False)
			elif(option == 'rtcwake'):
				if value in switchoff:
					sysvals.rtcwake = False
				else:
					sysvals.rtcwake = True
					sysvals.rtcwaketime = getArgInt('rtcwake', value, 0, 3600, False)
			elif(option == 'timeprec'):
				sysvals.setPrecision(getArgInt('timeprec', value, 0, 6, False))
			elif(option == 'mindev'):
				sysvals.mindevlen = getArgFloat('mindev', value, 0.0, 10000.0, False)
			elif(option == 'callloop-maxgap'):
				sysvals.callloopmaxgap = getArgFloat('callloop-maxgap', value, 0.0, 1.0, False)
			elif(option == 'callloop-maxlen'):
				sysvals.callloopmaxgap = getArgFloat('callloop-maxlen', value, 0.0, 1.0, False)
			elif(option == 'mincg'):
				sysvals.mincglen = getArgFloat('mincg', value, 0.0, 10000.0, False)
			elif(option == 'bufsize'):
				sysvals.bufsize = getArgInt('bufsize', value, 1, 1024*1024*8, False)
			elif(option == 'output-dir'):
				sysvals.outdir = sysvals.setOutputFolder(value)

	if sysvals.suspendmode == 'command' and not sysvals.testcommand:
		doError('No command supplied for mode "command"')

	
	if sysvals.usedevsrc and sysvals.usecallgraph:
		doError('-dev is not compatible with -f')
	if sysvals.usecallgraph and sysvals.useprocmon:
		doError('-proc is not compatible with -f')

	if overridekprobes:
		sysvals.tracefuncs = dict()
	if overridedevkprobes:
		sysvals.dev_tracefuncs = dict()

	kprobes = dict()
	kprobesec = 'dev_timeline_functions_'+platform.machine()
	if kprobesec in sections:
		for name in Config.options(kprobesec):
			text = Config.get(kprobesec, name)
			kprobes[name] = (text, True)
	kprobesec = 'timeline_functions_'+platform.machine()
	if kprobesec in sections:
		for name in Config.options(kprobesec):
			if name in kprobes:
				doError('Duplicate timeline function found "%s"' % (name))
			text = Config.get(kprobesec, name)
			kprobes[name] = (text, False)

	for name in kprobes:
		function = name
		format = name
		color = ''
		args = dict()
		text, dev = kprobes[name]
		data = text.split()
		i = 0
		for val in data:
			
			if val[0] == '[' and val[-1] == ']':
				for prop in val[1:-1].split(','):
					p = prop.split('=')
					if p[0] == 'color':
						try:
							color = int(p[1], 16)
							color = '
						except:
							color = p[1]
				continue
			
			if i == 0:
				format = val
			
			else:
				d = val.split('=')
				args[d[0]] = d[1]
			i += 1
		if not function or not format:
			doError('Invalid kprobe: %s' % name)
		for arg in re.findall('{(?P<n>[a-z,A-Z,0-9]*)}', format):
			if arg not in args:
				doError('Kprobe "%s" is missing argument "%s"' % (name, arg))
		if (dev and name in sysvals.dev_tracefuncs) or (not dev and name in sysvals.tracefuncs):
			doError('Duplicate timeline function found "%s"' % (name))

		kp = {
			'name': name,
			'func': function,
			'format': format,
			sysvals.archargs: args
		}
		if color:
			kp['color'] = color
		if dev:
			sysvals.dev_tracefuncs[name] = kp
		else:
			sysvals.tracefuncs[name] = kp




def printHelp():
	pprint('\n%s v%s\n'\
	'Usage: sudo sleepgraph <options> <commands>\n'\
	'\n'\
	'Description:\n'\
	'  This tool is designed to assist kernel and OS developers in optimizing\n'\
	'  their linux stack\'s suspend/resume time. Using a kernel image built\n'\
	'  with a few extra options enabled, the tool will execute a suspend and\n'\
	'  capture dmesg and ftrace data until resume is complete. This data is\n'\
	'  transformed into a device timeline and an optional callgraph to give\n'\
	'  a detailed view of which devices/subsystems are taking the most\n'\
	'  time in suspend/resume.\n'\
	'\n'\
	'  If no specific command is given, the default behavior is to initiate\n'\
	'  a suspend/resume and capture the dmesg/ftrace output as an html timeline.\n'\
	'\n'\
	'  Generates output files in subdirectory: suspend-yymmdd-HHMMSS\n'\
	'   HTML output:                    <hostname>_<mode>.html\n'\
	'   raw dmesg output:               <hostname>_<mode>_dmesg.txt\n'\
	'   raw ftrace output:              <hostname>_<mode>_ftrace.txt\n'\
	'\n'\
	'Options:\n'\
	'   -h           Print this help text\n'\
	'   -v           Print the current tool version\n'\
	'   -config fn   Pull arguments and config options from file fn\n'\
	'   -verbose     Print extra information during execution and analysis\n'\
	'   -m mode      Mode to initiate for suspend (default: %s)\n'\
	'   -o name      Overrides the output subdirectory name when running a new test\n'\
	'                default: suspend-{date}-{time}\n'\
	'   -rtcwake t   Wakeup t seconds after suspend, set t to "off" to disable (default: 15)\n'\
	'   -addlogs     Add the dmesg and ftrace logs to the html output\n'\
	'   -noturbostat Dont use turbostat in freeze mode (default: disabled)\n'\
	'   -srgap       Add a visible gap in the timeline between sus/res (default: disabled)\n'\
	'   -skiphtml    Run the test and capture the trace logs, but skip the timeline (default: disabled)\n'\
	'   -result fn   Export a results table to a text file for parsing.\n'\
	'   -wifi        If a wifi connection is available, check that it reconnects after resume.\n'\
	'  [testprep]\n'\
	'   -sync        Sync the filesystems before starting the test\n'\
	'   -rs on/off   Enable/disable runtime suspend for all devices, restore all after test\n'\
	'   -display m   Change the display mode to m for the test (on/off/standby/suspend)\n'\
	'  [advanced]\n'\
	'   -gzip        Gzip the trace and dmesg logs to save space\n'\
	'   -cmd {s}     Run the timeline over a custom command, e.g. "sync -d"\n'\
	'   -proc        Add usermode process info into the timeline (default: disabled)\n'\
	'   -dev         Add kernel function calls and threads to the timeline (default: disabled)\n'\
	'   -x2          Run two suspend/resumes back to back (default: disabled)\n'\
	'   -x2delay t   Include t ms delay between multiple test runs (default: 0 ms)\n'\
	'   -predelay t  Include t ms delay before 1st suspend (default: 0 ms)\n'\
	'   -postdelay t Include t ms delay after last resume (default: 0 ms)\n'\
	'   -mindev ms   Discard all device blocks shorter than ms milliseconds (e.g. 0.001 for us)\n'\
	'   -multi n d   Execute <n> consecutive tests at <d> seconds intervals. If <n> is followed\n'\
	'                by a "d", "h", or "m" execute for <n> days, hours, or mins instead.\n'\
	'                The outputs will be created in a new subdirectory with a summary page.\n'\
	'   -maxfail n   Abort a -multi run after n consecutive fails (default is 0 = never abort)\n'\
	'  [debug]\n'\
	'   -f           Use ftrace to create device callgraphs (default: disabled)\n'\
	'   -ftop        Use ftrace on the top level call: "%s" (default: disabled)\n'\
	'   -maxdepth N  limit the callgraph data to N call levels (default: 0=all)\n'\
	'   -expandcg    pre-expand the callgraph data in the html output (default: disabled)\n'\
	'   -fadd file   Add functions to be graphed in the timeline from a list in a text file\n'\
	'   -filter "d1,d2,..." Filter out all but this comma-delimited list of device names\n'\
	'   -mincg  ms   Discard all callgraphs shorter than ms milliseconds (e.g. 0.001 for us)\n'\
	'   -cgphase P   Only show callgraph data for phase P (e.g. suspend_late)\n'\
	'   -cgtest N    Only show callgraph data for test N (e.g. 0 or 1 in an x2 run)\n'\
	'   -timeprec N  Number of significant digits in timestamps (0:S, [3:ms], 6:us)\n'\
	'   -cgfilter S  Filter the callgraph output in the timeline\n'\
	'   -cgskip file Callgraph functions to skip, off to disable (default: cgskip.txt)\n'\
	'   -bufsize N   Set trace buffer size to N kilo-bytes (default: all of free memory)\n'\
	'   -devdump     Print out all the raw device data for each phase\n'\
	'   -cgdump      Print out all the raw callgraph data\n'\
	'\n'\
	'Other commands:\n'\
	'   -modes       List available suspend modes\n'\
	'   -status      Test to see if the system is enabled to run this tool\n'\
	'   -fpdt        Print out the contents of the ACPI Firmware Performance Data Table\n'\
	'   -wificheck   Print out wifi connection info\n'\
	'   -x<mode>     Test xset by toggling the given mode (on/off/standby/suspend)\n'\
	'   -sysinfo     Print out system info extracted from BIOS\n'\
	'   -devinfo     Print out the pm settings of all devices which support runtime suspend\n'\
	'   -cmdinfo     Print out all the platform info collected before and after suspend/resume\n'\
	'   -flist       Print the list of functions currently being captured in ftrace\n'\
	'   -flistall    Print all functions capable of being captured in ftrace\n'\
	'   -summary dir Create a summary of tests in this dir [-genhtml builds missing html]\n'\
	'  [redo]\n'\
	'   -ftrace ftracefile  Create HTML output using ftrace input (used with -dmesg)\n'\
	'   -dmesg dmesgfile    Create HTML output using dmesg (used with -ftrace)\n'\
	'' % (sysvals.title, sysvals.version, sysvals.suspendmode, sysvals.ftopfunc))
	return True



if __name__ == '__main__':
	genhtml = False
	cmd = ''
	simplecmds = ['-sysinfo', '-modes', '-fpdt', '-flist', '-flistall',
		'-devinfo', '-status', '-xon', '-xoff', '-xstandby', '-xsuspend',
		'-xinit', '-xreset', '-xstat', '-wificheck', '-cmdinfo']
	if '-f' in sys.argv:
		sysvals.cgskip = sysvals.configFile('cgskip.txt')
	
	args = iter(sys.argv[1:])
	for arg in args:
		if(arg == '-m'):
			try:
				val = next(args)
			except:
				doError('No mode supplied', True)
			if val == 'command' and not sysvals.testcommand:
				doError('No command supplied for mode "command"', True)
			sysvals.suspendmode = val
		elif(arg in simplecmds):
			cmd = arg[1:]
		elif(arg == '-h'):
			printHelp()
			sys.exit(0)
		elif(arg == '-v'):
			pprint("Version %s" % sysvals.version)
			sys.exit(0)
		elif(arg == '-x2'):
			sysvals.execcount = 2
		elif(arg == '-x2delay'):
			sysvals.x2delay = getArgInt('-x2delay', args, 0, 60000)
		elif(arg == '-predelay'):
			sysvals.predelay = getArgInt('-predelay', args, 0, 60000)
		elif(arg == '-postdelay'):
			sysvals.postdelay = getArgInt('-postdelay', args, 0, 60000)
		elif(arg == '-f'):
			sysvals.usecallgraph = True
		elif(arg == '-ftop'):
			sysvals.usecallgraph = True
			sysvals.ftop = True
			sysvals.usekprobes = False
		elif(arg == '-skiphtml'):
			sysvals.skiphtml = True
		elif(arg == '-cgdump'):
			sysvals.cgdump = True
		elif(arg == '-devdump'):
			sysvals.devdump = True
		elif(arg == '-genhtml'):
			genhtml = True
		elif(arg == '-addlogs'):
			sysvals.dmesglog = sysvals.ftracelog = True
		elif(arg == '-nologs'):
			sysvals.dmesglog = sysvals.ftracelog = False
		elif(arg == '-addlogdmesg'):
			sysvals.dmesglog = True
		elif(arg == '-addlogftrace'):
			sysvals.ftracelog = True
		elif(arg == '-noturbostat'):
			sysvals.tstat = False
		elif(arg == '-verbose'):
			sysvals.verbose = True
		elif(arg == '-proc'):
			sysvals.useprocmon = True
		elif(arg == '-dev'):
			sysvals.usedevsrc = True
		elif(arg == '-sync'):
			sysvals.sync = True
		elif(arg == '-wifi'):
			sysvals.wifi = True
		elif(arg == '-gzip'):
			sysvals.gzip = True
		elif(arg == '-info'):
			try:
				val = next(args)
			except:
				doError('-info requires one string argument', True)
		elif(arg == '-rs'):
			try:
				val = next(args)
			except:
				doError('-rs requires "enable" or "disable"', True)
			if val.lower() in switchvalues:
				if val.lower() in switchoff:
					sysvals.rs = -1
				else:
					sysvals.rs = 1
			else:
				doError('invalid option: %s, use "enable/disable" or "on/off"' % val, True)
		elif(arg == '-display'):
			try:
				val = next(args)
			except:
				doError('-display requires an mode value', True)
			disopt = ['on', 'off', 'standby', 'suspend']
			if val.lower() not in disopt:
				doError('valid display mode values are %s' % disopt, True)
			sysvals.display = val.lower()
		elif(arg == '-maxdepth'):
			sysvals.max_graph_depth = getArgInt('-maxdepth', args, 0, 1000)
		elif(arg == '-rtcwake'):
			try:
				val = next(args)
			except:
				doError('No rtcwake time supplied', True)
			if val.lower() in switchoff:
				sysvals.rtcwake = False
			else:
				sysvals.rtcwake = True
				sysvals.rtcwaketime = getArgInt('-rtcwake', val, 0, 3600, False)
		elif(arg == '-timeprec'):
			sysvals.setPrecision(getArgInt('-timeprec', args, 0, 6))
		elif(arg == '-mindev'):
			sysvals.mindevlen = getArgFloat('-mindev', args, 0.0, 10000.0)
		elif(arg == '-mincg'):
			sysvals.mincglen = getArgFloat('-mincg', args, 0.0, 10000.0)
		elif(arg == '-bufsize'):
			sysvals.bufsize = getArgInt('-bufsize', args, 1, 1024*1024*8)
		elif(arg == '-cgtest'):
			sysvals.cgtest = getArgInt('-cgtest', args, 0, 1)
		elif(arg == '-cgphase'):
			try:
				val = next(args)
			except:
				doError('No phase name supplied', True)
			d = Data(0)
			if val not in d.phasedef:
				doError('invalid phase --> (%s: %s), valid phases are %s'\
					% (arg, val, d.phasedef.keys()), True)
			sysvals.cgphase = val
		elif(arg == '-cgfilter'):
			try:
				val = next(args)
			except:
				doError('No callgraph functions supplied', True)
			sysvals.setCallgraphFilter(val)
		elif(arg == '-skipkprobe'):
			try:
				val = next(args)
			except:
				doError('No kprobe functions supplied', True)
			sysvals.skipKprobes(val)
		elif(arg == '-cgskip'):
			try:
				val = next(args)
			except:
				doError('No file supplied', True)
			if val.lower() in switchoff:
				sysvals.cgskip = ''
			else:
				sysvals.cgskip = sysvals.configFile(val)
				if(not sysvals.cgskip):
					doError('%s does not exist' % sysvals.cgskip)
		elif(arg == '-callloop-maxgap'):
			sysvals.callloopmaxgap = getArgFloat('-callloop-maxgap', args, 0.0, 1.0)
		elif(arg == '-callloop-maxlen'):
			sysvals.callloopmaxlen = getArgFloat('-callloop-maxlen', args, 0.0, 1.0)
		elif(arg == '-cmd'):
			try:
				val = next(args)
			except:
				doError('No command string supplied', True)
			sysvals.testcommand = val
			sysvals.suspendmode = 'command'
		elif(arg == '-expandcg'):
			sysvals.cgexp = True
		elif(arg == '-srgap'):
			sysvals.srgap = 5
		elif(arg == '-maxfail'):
			sysvals.maxfail = getArgInt('-maxfail', args, 0, 1000000)
		elif(arg == '-multi'):
			try:
				c, d = next(args), next(args)
			except:
				doError('-multi requires two values', True)
			sysvals.multiinit(c, d)
		elif(arg == '-o'):
			try:
				val = next(args)
			except:
				doError('No subdirectory name supplied', True)
			sysvals.outdir = sysvals.setOutputFolder(val)
		elif(arg == '-config'):
			try:
				val = next(args)
			except:
				doError('No text file supplied', True)
			file = sysvals.configFile(val)
			if(not file):
				doError('%s does not exist' % val)
			configFromFile(file)
		elif(arg == '-fadd'):
			try:
				val = next(args)
			except:
				doError('No text file supplied', True)
			file = sysvals.configFile(val)
			if(not file):
				doError('%s does not exist' % val)
			sysvals.addFtraceFilterFunctions(file)
		elif(arg == '-dmesg'):
			try:
				val = next(args)
			except:
				doError('No dmesg file supplied', True)
			sysvals.notestrun = True
			sysvals.dmesgfile = val
			if(os.path.exists(sysvals.dmesgfile) == False):
				doError('%s does not exist' % sysvals.dmesgfile)
		elif(arg == '-ftrace'):
			try:
				val = next(args)
			except:
				doError('No ftrace file supplied', True)
			sysvals.notestrun = True
			sysvals.ftracefile = val
			if(os.path.exists(sysvals.ftracefile) == False):
				doError('%s does not exist' % sysvals.ftracefile)
		elif(arg == '-summary'):
			try:
				val = next(args)
			except:
				doError('No directory supplied', True)
			cmd = 'summary'
			sysvals.outdir = val
			sysvals.notestrun = True
			if(os.path.isdir(val) == False):
				doError('%s is not accesible' % val)
		elif(arg == '-filter'):
			try:
				val = next(args)
			except:
				doError('No devnames supplied', True)
			sysvals.setDeviceFilter(val)
		elif(arg == '-result'):
			try:
				val = next(args)
			except:
				doError('No result file supplied', True)
			sysvals.result = val
			sysvals.signalHandlerInit()
		else:
			doError('Invalid argument: '+arg, True)

	
	if(sysvals.usecallgraph and sysvals.usedevsrc):
		doError('-dev is not compatible with -f')
	if(sysvals.usecallgraph and sysvals.useprocmon):
		doError('-proc is not compatible with -f')

	if sysvals.usecallgraph and sysvals.cgskip:
		sysvals.vprint('Using cgskip file: %s' % sysvals.cgskip)
		sysvals.setCallgraphBlacklist(sysvals.cgskip)

	
	if sysvals.mincglen < sysvals.mindevlen:
		sysvals.mincglen = sysvals.mindevlen

	
	if(sysvals.usecallgraph or sysvals.usedevsrc):
		sysvals.fsetVal('16', 'buffer_size_kb')
	sysvals.cpuInfo()

	
	if(cmd != ''):
		ret = 0
		if(cmd == 'status'):
			if not statusCheck(True):
				ret = 1
		elif(cmd == 'fpdt'):
			if not getFPDT(True):
				ret = 1
		elif(cmd == 'sysinfo'):
			sysvals.printSystemInfo(True)
		elif(cmd == 'devinfo'):
			deviceInfo()
		elif(cmd == 'modes'):
			pprint(getModes())
		elif(cmd == 'flist'):
			sysvals.getFtraceFilterFunctions(True)
		elif(cmd == 'flistall'):
			sysvals.getFtraceFilterFunctions(False)
		elif(cmd == 'summary'):
			runSummary(sysvals.outdir, True, genhtml)
		elif(cmd in ['xon', 'xoff', 'xstandby', 'xsuspend', 'xinit', 'xreset']):
			sysvals.verbose = True
			ret = displayControl(cmd[1:])
		elif(cmd == 'xstat'):
			pprint('Display Status: %s' % displayControl('stat').upper())
		elif(cmd == 'wificheck'):
			dev = sysvals.checkWifi()
			if dev:
				print('%s is connected' % sysvals.wifiDetails(dev))
			else:
				print('No wifi connection found')
		elif(cmd == 'cmdinfo'):
			for out in sysvals.cmdinfo(False, True):
				print('[%s - %s]\n%s\n' % out)
		sys.exit(ret)

	
	if(sysvals.notestrun):
		stamp = rerunTest(sysvals.outdir)
		sysvals.outputResult(stamp)
		sys.exit(0)

	
	error = statusCheck()
	if(error):
		doError(error)

	
	mode = sysvals.suspendmode
	if mode.startswith('mem'):
		memmode = mode.split('-', 1)[-1] if '-' in mode else 'deep'
		if memmode == 'shallow':
			mode = 'standby'
		elif memmode ==  's2idle':
			mode = 'freeze'
		else:
			mode = 'mem'
		sysvals.memmode = memmode
		sysvals.suspendmode = mode
	if mode.startswith('disk-'):
		sysvals.diskmode = mode.split('-', 1)[-1]
		sysvals.suspendmode = 'disk'

	sysvals.systemInfo(dmidecode(sysvals.mempath))

	setRuntimeSuspend(True)
	if sysvals.display:
		displayControl('init')
	failcnt, ret = 0, 0
	if sysvals.multitest['run']:
		
		if not sysvals.outdir:
			if 'time' in sysvals.multitest:
				s = '-%dm' % sysvals.multitest['time']
			else:
				s = '-x%d' % sysvals.multitest['count']
			sysvals.outdir = datetime.now().strftime('suspend-%y%m%d-%H%M%S'+s)
		if not os.path.isdir(sysvals.outdir):
			os.makedirs(sysvals.outdir)
		sysvals.sudoUserchown(sysvals.outdir)
		finish = datetime.now()
		if 'time' in sysvals.multitest:
			finish += timedelta(minutes=sysvals.multitest['time'])
		for i in range(sysvals.multitest['count']):
			sysvals.multistat(True, i, finish)
			if i != 0 and sysvals.multitest['delay'] > 0:
				pprint('Waiting %d seconds...' % (sysvals.multitest['delay']))
				time.sleep(sysvals.multitest['delay'])
			fmt = 'suspend-%y%m%d-%H%M%S'
			sysvals.testdir = os.path.join(sysvals.outdir, datetime.now().strftime(fmt))
			ret = runTest(i+1, True)
			failcnt = 0 if not ret else failcnt + 1
			if sysvals.maxfail > 0 and failcnt >= sysvals.maxfail:
				pprint('Maximum fail count of %d reached, aborting multitest' % (sysvals.maxfail))
				break
			time.sleep(5)
			sysvals.resetlog()
			sysvals.multistat(False, i, finish)
			if 'time' in sysvals.multitest and datetime.now() >= finish:
				break
		if not sysvals.skiphtml:
			runSummary(sysvals.outdir, False, False)
		sysvals.sudoUserchown(sysvals.outdir)
	else:
		if sysvals.outdir:
			sysvals.testdir = sysvals.outdir
		
		ret = runTest()
	if sysvals.display:
		displayControl('reset')
	setRuntimeSuspend(False)
	sys.exit(ret)
