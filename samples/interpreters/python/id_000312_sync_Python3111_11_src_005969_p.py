








































"... initcall_debug log_buf_len=16M ..."


import sys
import time
import os
import string
import re
import platform
from datetime import datetime
import struct





class SystemValues:
	version = 3.0
	verbose = False
	testdir = '.'
	tpath = '/sys/kernel/debug/tracing/'
	fpdtpath = '/sys/firmware/acpi/tables/FPDT'
	epath = '/sys/kernel/debug/tracing/events/power/'
	traceevents = [
		'suspend_resume',
		'device_pm_callback_end',
		'device_pm_callback_start'
	]
	modename = {
		'freeze': 'Suspend-To-Idle (S0)',
		'standby': 'Power-On Suspend (S1)',
		'mem': 'Suspend-to-RAM (S3)',
		'disk': 'Suspend-to-disk (S4)'
	}
	mempath = '/dev/mem'
	powerfile = '/sys/power/state'
	suspendmode = 'mem'
	hostname = 'localhost'
	prefix = 'test'
	teststamp = ''
	dmesgfile = ''
	ftracefile = ''
	htmlfile = ''
	rtcwake = False
	rtcwaketime = 10
	rtcpath = ''
	android = False
	adb = 'adb'
	devicefilter = []
	stamp = 0
	execcount = 1
	x2delay = 0
	usecallgraph = False
	usetraceevents = False
	usetraceeventsonly = False
	notestrun = False
	altdevname = dict()
	postresumetime = 0
	tracertypefmt = '
	firmwarefmt = '
	postresumefmt = '
	stampfmt = '
				'(?P<H>[0-9]{2})(?P<M>[0-9]{2})(?P<S>[0-9]{2})'+\
				' (?P<host>.*) (?P<mode>.*) (?P<kernel>.*)$'
	def __init__(self):
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
	def setOutputFile(self):
		if((self.htmlfile == '') and (self.dmesgfile != '')):
			m = re.match('(?P<name>.*)_dmesg\.txt$', self.dmesgfile)
			if(m):
				self.htmlfile = m.group('name')+'.html'
		if((self.htmlfile == '') and (self.ftracefile != '')):
			m = re.match('(?P<name>.*)_ftrace\.txt$', self.ftracefile)
			if(m):
				self.htmlfile = m.group('name')+'.html'
		if(self.htmlfile == ''):
			self.htmlfile = 'output.html'
	def initTestOutput(self, subdir):
		if(not self.android):
			self.prefix = self.hostname
			v = open('/proc/version', 'r').read().strip()
			kver = string.split(v)[2]
		else:
			self.prefix = 'android'
			v = os.popen(self.adb+' shell cat /proc/version').read().strip()
			kver = string.split(v)[2]
		testtime = datetime.now().strftime('suspend-%m%d%y-%H%M%S')
		if(subdir != "."):
			self.testdir = subdir+"/"+testtime
		else:
			self.testdir = testtime
		self.teststamp = \
			'
		self.dmesgfile = \
			self.testdir+'/'+self.prefix+'_'+self.suspendmode+'_dmesg.txt'
		self.ftracefile = \
			self.testdir+'/'+self.prefix+'_'+self.suspendmode+'_ftrace.txt'
		self.htmlfile = \
			self.testdir+'/'+self.prefix+'_'+self.suspendmode+'.html'
		os.mkdir(self.testdir)
	def setDeviceFilter(self, devnames):
		self.devicefilter = string.split(devnames)
	def rtcWakeAlarm(self):
		os.system('echo 0 > '+self.rtcpath+'/wakealarm')
		outD = open(self.rtcpath+'/date', 'r').read().strip()
		outT = open(self.rtcpath+'/time', 'r').read().strip()
		mD = re.match('^(?P<y>[0-9]*)-(?P<m>[0-9]*)-(?P<d>[0-9]*)', outD)
		mT = re.match('^(?P<h>[0-9]*):(?P<m>[0-9]*):(?P<s>[0-9]*)', outT)
		if(mD and mT):
			
			utcoffset = int((datetime.now() - datetime.utcnow()).total_seconds())
			dt = datetime(\
				int(mD.group('y')), int(mD.group('m')), int(mD.group('d')),
				int(mT.group('h')), int(mT.group('m')), int(mT.group('s')))
			nowtime = int(dt.strftime('%s')) + utcoffset
		else:
			
			nowtime = int(datetime.now().strftime('%s'))
		alarm = nowtime + self.rtcwaketime
		os.system('echo %d > %s/wakealarm' % (alarm, self.rtcpath))
sysvals = SystemValues()




class DeviceNode:
	name = ''
	children = 0
	depth = 0
	def __init__(self, nodename, nodedepth):
		self.name = nodename
		self.children = []
		self.depth = nodedepth























class Data:
	dmesg = {}  
	phases = [] 
	start = 0.0 
	end = 0.0   
	tSuspended = 0.0 
	tResumed = 0.0   
	tLow = 0.0       
	fwValid = False  
	fwSuspend = 0    
	fwResume = 0     
	dmesgtext = []   
	testnumber = 0
	idstr = ''
	html_device_id = 0
	stamp = 0
	outfile = ''
	def __init__(self, num):
		idchar = 'abcdefghijklmnopqrstuvwxyz'
		self.testnumber = num
		self.idstr = idchar[num]
		self.dmesgtext = []
		self.phases = []
		self.dmesg = { 
			'suspend_prepare': {'list': dict(), 'start': -1.0, 'end': -1.0,
								'row': 0, 'color': '
			        'suspend': {'list': dict(), 'start': -1.0, 'end': -1.0,
								'row': 0, 'color': '
			   'suspend_late': {'list': dict(), 'start': -1.0, 'end': -1.0,
								'row': 0, 'color': '
			  'suspend_noirq': {'list': dict(), 'start': -1.0, 'end': -1.0,
								'row': 0, 'color': '
		    'suspend_machine': {'list': dict(), 'start': -1.0, 'end': -1.0,
								'row': 0, 'color': '
			 'resume_machine': {'list': dict(), 'start': -1.0, 'end': -1.0,
								'row': 0, 'color': '
			   'resume_noirq': {'list': dict(), 'start': -1.0, 'end': -1.0,
								'row': 0, 'color': '
			   'resume_early': {'list': dict(), 'start': -1.0, 'end': -1.0,
								'row': 0, 'color': '
			         'resume': {'list': dict(), 'start': -1.0, 'end': -1.0,
								'row': 0, 'color': '
			'resume_complete': {'list': dict(), 'start': -1.0, 'end': -1.0,
								'row': 0, 'color': '
		}
		self.phases = self.sortedPhases()
	def getStart(self):
		return self.dmesg[self.phases[0]]['start']
	def setStart(self, time):
		self.start = time
		self.dmesg[self.phases[0]]['start'] = time
	def getEnd(self):
		return self.dmesg[self.phases[-1]]['end']
	def setEnd(self, time):
		self.end = time
		self.dmesg[self.phases[-1]]['end'] = time
	def isTraceEventOutsideDeviceCalls(self, pid, time):
		for phase in self.phases:
			list = self.dmesg[phase]['list']
			for dev in list:
				d = list[dev]
				if(d['pid'] == pid and time >= d['start'] and
					time <= d['end']):
					return False
		return True
	def addIntraDevTraceEvent(self, action, name, pid, time):
		if(action == 'mutex_lock_try'):
			color = 'red'
		elif(action == 'mutex_lock_pass'):
			color = 'green'
		elif(action == 'mutex_unlock'):
			color = 'blue'
		else:
			
			v1 = len(name)*10 % 256
			v2 = string.count(name, 'e')*100 % 256
			v3 = ord(name[0])*20 % 256
			color = '
		for phase in self.phases:
			list = self.dmesg[phase]['list']
			for dev in list:
				d = list[dev]
				if(d['pid'] == pid and time >= d['start'] and
					time <= d['end']):
					e = TraceEvent(action, name, color, time)
					if('traceevents' not in d):
						d['traceevents'] = []
					d['traceevents'].append(e)
					return d
					break
		return 0
	def capIntraDevTraceEvent(self, action, name, pid, time):
		for phase in self.phases:
			list = self.dmesg[phase]['list']
			for dev in list:
				d = list[dev]
				if(d['pid'] == pid and time >= d['start'] and
					time <= d['end']):
					if('traceevents' not in d):
						return
					for e in d['traceevents']:
						if(e.action == action and
							e.name == name and not e.ready):
							e.length = time - e.time
							e.ready = True
							break
					return
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
		self.end = self.trimTimeVal(self.end, t0, dT, left)
		for phase in self.phases:
			p = self.dmesg[phase]
			p['start'] = self.trimTimeVal(p['start'], t0, dT, left)
			p['end'] = self.trimTimeVal(p['end'], t0, dT, left)
			list = p['list']
			for name in list:
				d = list[name]
				d['start'] = self.trimTimeVal(d['start'], t0, dT, left)
				d['end'] = self.trimTimeVal(d['end'], t0, dT, left)
				if('ftrace' in d):
					cg = d['ftrace']
					cg.start = self.trimTimeVal(cg.start, t0, dT, left)
					cg.end = self.trimTimeVal(cg.end, t0, dT, left)
					for line in cg.list:
						line.time = self.trimTimeVal(line.time, t0, dT, left)
				if('traceevents' in d):
					for e in d['traceevents']:
						e.time = self.trimTimeVal(e.time, t0, dT, left)
	def normalizeTime(self, tZero):
		
		if(self.tSuspended != self.tResumed):
			if(self.tResumed > tZero):
				self.trimTime(self.tSuspended, \
					self.tResumed-self.tSuspended, True)
			else:
				self.trimTime(self.tSuspended, \
					self.tResumed-self.tSuspended, False)
		
		self.tSuspended -= tZero
		self.tResumed -= tZero
		self.start -= tZero
		self.end -= tZero
		for phase in self.phases:
			p = self.dmesg[phase]
			p['start'] -= tZero
			p['end'] -= tZero
			list = p['list']
			for name in list:
				d = list[name]
				d['start'] -= tZero
				d['end'] -= tZero
				if('ftrace' in d):
					cg = d['ftrace']
					cg.start -= tZero
					cg.end -= tZero
					for line in cg.list:
						line.time -= tZero
				if('traceevents' in d):
					for e in d['traceevents']:
						e.time -= tZero
	def newPhaseWithSingleAction(self, phasename, devname, start, end, color):
		for phase in self.phases:
			self.dmesg[phase]['order'] += 1
		self.html_device_id += 1
		devid = '%s%d' % (self.idstr, self.html_device_id)
		list = dict()
		list[devname] = \
			{'start': start, 'end': end, 'pid': 0, 'par': '',
			'length': (end-start), 'row': 0, 'id': devid, 'drv': '' };
		self.dmesg[phasename] = \
			{'list': list, 'start': start, 'end': end,
			'row': 0, 'color': color, 'order': 0}
		self.phases = self.sortedPhases()
	def newPhase(self, phasename, start, end, color, order):
		if(order < 0):
			order = len(self.phases)
		for phase in self.phases[order:]:
			self.dmesg[phase]['order'] += 1
		if(order > 0):
			p = self.phases[order-1]
			self.dmesg[p]['end'] = start
		if(order < len(self.phases)):
			p = self.phases[order]
			self.dmesg[p]['start'] = end
		list = dict()
		self.dmesg[phasename] = \
			{'list': list, 'start': start, 'end': end,
			'row': 0, 'color': color, 'order': order}
		self.phases = self.sortedPhases()
	def setPhase(self, phase, ktime, isbegin):
		if(isbegin):
			self.dmesg[phase]['start'] = ktime
		else:
			self.dmesg[phase]['end'] = ktime
	def dmesgSortVal(self, phase):
		return self.dmesg[phase]['order']
	def sortedPhases(self):
		return sorted(self.dmesg, key=self.dmesgSortVal)
	def sortedDevices(self, phase):
		list = self.dmesg[phase]['list']
		slist = []
		tmp = dict()
		for devname in list:
			dev = list[devname]
			tmp[dev['start']] = devname
		for t in sorted(tmp):
			slist.append(tmp[t])
		return slist
	def fixupInitcalls(self, phase, end):
		
		phaselist = self.dmesg[phase]['list']
		for devname in phaselist:
			dev = phaselist[devname]
			if(dev['end'] < 0):
				dev['end'] = end
				vprint('%s (%s): callback didnt return' % (devname, phase))
	def deviceFilter(self, devicefilter):
		
		filter = []
		for phase in self.phases:
			list = self.dmesg[phase]['list']
			for name in devicefilter:
				dev = name
				while(dev in list):
					if(dev not in filter):
						filter.append(dev)
					dev = list[dev]['par']
				children = self.deviceDescendants(name, phase)
				for dev in children:
					if(dev not in filter):
						filter.append(dev)
		for phase in self.phases:
			list = self.dmesg[phase]['list']
			rmlist = []
			for name in list:
				pid = list[name]['pid']
				if(name not in filter and pid >= 0):
					rmlist.append(name)
			for name in rmlist:
				del list[name]
	def fixupInitcallsThatDidntReturn(self):
		
		for phase in self.phases:
			self.fixupInitcalls(phase, self.getEnd())
	def newActionGlobal(self, name, start, end):
		"in"
		targetphase = "none"
		overlap = 0.0
		for phase in self.phases:
			pstart = self.dmesg[phase]['start']
			pend = self.dmesg[phase]['end']
			o = max(0, min(end, pend) - max(start, pstart))
			if(o > overlap):
				targetphase = phase
				overlap = o
		if targetphase in self.phases:
			self.newAction(targetphase, name, -1, '', start, end, '')
			return True
		return False
	def newAction(self, phase, name, pid, parent, start, end, drv):
		
		self.html_device_id += 1
		devid = '%s%d' % (self.idstr, self.html_device_id)
		list = self.dmesg[phase]['list']
		length = -1.0
		if(start >= 0 and end >= 0):
			length = end - start
		list[name] = {'start': start, 'end': end, 'pid': pid, 'par': parent,
					  'length': length, 'row': 0, 'id': devid, 'drv': drv }
	def deviceIDs(self, devlist, phase):
		idlist = []
		list = self.dmesg[phase]['list']
		for devname in list:
			if devname in devlist:
				idlist.append(list[devname]['id'])
		return idlist
	def deviceParentID(self, devname, phase):
		pdev = ''
		pdevid = ''
		list = self.dmesg[phase]['list']
		if devname in list:
			pdev = list[devname]['par']
		if pdev in list:
			return list[pdev]['id']
		return pdev
	def deviceChildren(self, devname, phase):
		devlist = []
		list = self.dmesg[phase]['list']
		for child in list:
			if(list[child]['par'] == devname):
				devlist.append(child)
		return devlist
	def deviceDescendants(self, devname, phase):
		children = self.deviceChildren(devname, phase)
		family = children
		for child in children:
			family += self.deviceDescendants(child, phase)
		return family
	def deviceChildrenIDs(self, devname, phase):
		devlist = self.deviceChildren(devname, phase)
		return self.deviceIDs(devlist, phase)
	def printDetails(self):
		vprint('          test start: %f' % self.start)
		for phase in self.phases:
			dc = len(self.dmesg[phase]['list'])
			vprint('    %16s: %f - %f (%d devices)' % (phase, \
				self.dmesg[phase]['start'], self.dmesg[phase]['end'], dc))
		vprint('            test end: %f' % self.end)
	def masterTopology(self, name, list, depth):
		node = DeviceNode(name, depth)
		for cname in list:
			clist = self.deviceChildren(cname, 'resume')
			cnode = self.masterTopology(cname, clist, depth+1)
			node.children.append(cnode)
		return node
	def printTopology(self, node):
		html = ''
		if node.name:
			info = ''
			drv = ''
			for phase in self.phases:
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
		for phase in self.dmesg:
			list = self.dmesg[phase]['list']
			for dev in list:
				if list[dev]['pid'] >= 0 and dev not in real:
					real.append(dev)
		
		rootlist = []
		for phase in self.dmesg:
			list = self.dmesg[phase]['list']
			for dev in list:
				pdev = list[dev]['par']
				if(re.match('[0-9]*-[0-9]*\.[0-9]*[\.0-9]*\:[\.0-9]*$', pdev)):
					continue
				if pdev and pdev not in real and pdev not in rootlist:
					rootlist.append(pdev)
		return rootlist
	def deviceTopology(self):
		rootlist = self.rootDeviceList()
		master = self.masterTopology('', rootlist, 0)
		return self.printTopology(master)



class TraceEvent:
	ready = False
	name = ''
	time = 0.0
	color = '
	length = 0.0
	action = ''
	def __init__(self, a, n, c, t):
		self.action = a
		self.name = n
		self.color = c
		self.time = t




"  dpm_run_callback() {"
"  }"
" dpm_run_callback();"




class FTraceLine:
	time = 0.0
	length = 0.0
	fcall = False
	freturn = False
	fevent = False
	depth = 0
	name = ''
	type = ''
	def __init__(self, t, m, d):
		self.time = float(t)
		
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
					self.name = match.group('n')
		
		else:
			self.fcall = True
			
			if(m[-1] == '{'):
				match = re.match('^(?P<n>.*) *\(.*', m)
				if(match):
					self.name = match.group('n')
			
			elif(m[-1] == ';'):
				self.freturn = True
				match = re.match('^(?P<n>.*) *\(.*', m)
				if(match):
					self.name = match.group('n')
			
			else:
				self.name = m
	def getDepth(self, str):
		return len(str)/2
	def debugPrint(self, dev):
		if(self.freturn and self.fcall):
			print('%s -- %f (%02d): %s(); (%.3f us)' % (dev, self.time, \
				self.depth, self.name, self.length*1000000))
		elif(self.freturn):
			print('%s -- %f (%02d): %s} (%.3f us)' % (dev, self.time, \
				self.depth, self.name, self.length*1000000))
		else:
			print('%s -- %f (%02d): %s() { (%.3f us)' % (dev, self.time, \
				self.depth, self.name, self.length*1000000))






class FTraceCallGraph:
	start = -1.0
	end = -1.0
	list = []
	invalid = False
	depth = 0
	def __init__(self):
		self.start = -1.0
		self.end = -1.0
		self.list = []
		self.depth = 0
	def setDepth(self, line):
		if(line.fcall and not line.freturn):
			line.depth = self.depth
			self.depth += 1
		elif(line.freturn and not line.fcall):
			self.depth -= 1
			line.depth = self.depth
		else:
			line.depth = self.depth
	def addLine(self, line, match):
		if(not self.invalid):
			self.setDepth(line)
		if(line.depth == 0 and line.freturn):
			if(self.start < 0):
				self.start = line.time
			self.end = line.time
			self.list.append(line)
			return True
		if(self.invalid):
			return False
		if(len(self.list) >= 1000000 or self.depth < 0):
			if(len(self.list) > 0):
				first = self.list[0]
				self.list = []
				self.list.append(first)
			self.invalid = True
			if(not match):
				return False
			id = 'task %s cpu %s' % (match.group('pid'), match.group('cpu'))
			window = '(%f - %f)' % (self.start, line.time)
			if(self.depth < 0):
				print('Too much data for '+id+\
					' (buffer overflow), ignoring this callback')
			else:
				print('Too much data for '+id+\
					' '+window+', ignoring this callback')
			return False
		self.list.append(line)
		if(self.start < 0):
			self.start = line.time
		return False
	def slice(self, t0, tN):
		minicg = FTraceCallGraph()
		count = -1
		firstdepth = 0
		for l in self.list:
			if(l.time < t0 or l.time > tN):
				continue
			if(count < 0):
				if(not l.fcall or l.name == 'dev_driver_string'):
					continue
				firstdepth = l.depth
				count = 0
			l.depth -= firstdepth
			minicg.addLine(l, 0)
			if((count == 0 and l.freturn and l.fcall) or
				(count > 0 and l.depth <= 0)):
				break
			count += 1
		return minicg
	def sanityCheck(self):
		stack = dict()
		cnt = 0
		for l in self.list:
			if(l.fcall and not l.freturn):
				stack[l.depth] = l
				cnt += 1
			elif(l.freturn and not l.fcall):
				if(l.depth not in stack):
					return False
				stack[l.depth].length = l.length
				stack[l.depth] = 0
				l.length = 0
				cnt -= 1
		if(cnt == 0):
			return True
		return False
	def debugPrint(self, filename):
		if(filename == 'stdout'):
			print('[%f - %f]') % (self.start, self.end)
			for l in self.list:
				if(l.freturn and l.fcall):
					print('%f (%02d): %s(); (%.3f us)' % (l.time, \
						l.depth, l.name, l.length*1000000))
				elif(l.freturn):
					print('%f (%02d): %s} (%.3f us)' % (l.time, \
						l.depth, l.name, l.length*1000000))
				else:
					print('%f (%02d): %s() { (%.3f us)' % (l.time, \
						l.depth, l.name, l.length*1000000))
			print(' ')
		else:
			fp = open(filename, 'w')
			print(filename)
			for l in self.list:
				if(l.freturn and l.fcall):
					fp.write('%f (%02d): %s(); (%.3f us)\n' % (l.time, \
						l.depth, l.name, l.length*1000000))
				elif(l.freturn):
					fp.write('%f (%02d): %s} (%.3f us)\n' % (l.time, \
						l.depth, l.name, l.length*1000000))
				else:
					fp.write('%f (%02d): %s() { (%.3f us)\n' % (l.time, \
						l.depth, l.name, l.length*1000000))
			fp.close()





class Timeline:
	html = {}
	scaleH = 0.0 
	rowH = 0.0 
	row_height_pixels = 30
	maxrows = 0
	height = 0
	def __init__(self):
		self.html = {
			'timeline': '',
			'legend': '',
			'scale': ''
		}
	def setRows(self, rows):
		self.maxrows = int(rows)
		self.scaleH = 100.0/float(self.maxrows)
		self.height = self.maxrows*self.row_height_pixels
		r = float(self.maxrows - 1)
		if(r < 1.0):
			r = 1.0
		self.rowH = (100.0 - self.scaleH)/r




class TestRun:
	ftrace_line_fmt_fg = \
		'^ *(?P<time>[0-9\.]*) *\| *(?P<cpu>[0-9]*)\)'+\
		' *(?P<proc>.*)-(?P<pid>[0-9]*) *\|'+\
		'[ +!]*(?P<dur>[0-9\.]*) .*\|  (?P<msg>.*)'
	ftrace_line_fmt_nop = \
		' *(?P<proc>.*)-(?P<pid>[0-9]*) *\[(?P<cpu>[0-9]*)\] *'+\
		'(?P<flags>.{4}) *(?P<time>[0-9\.]*): *'+\
		'(?P<msg>.*)'
	ftrace_line_fmt = ftrace_line_fmt_nop
	cgformat = False
	ftemp = dict()
	ttemp = dict()
	inthepipe = False
	tracertype = ''
	data = 0
	def __init__(self, dataobj):
		self.data = dataobj
		self.ftemp = dict()
		self.ttemp = dict()
	def isReady(self):
		if(tracertype == '' or not data):
			return False
		return True
	def setTracerType(self, tracer):
		self.tracertype = tracer
		if(tracer == 'function_graph'):
			self.cgformat = True
			self.ftrace_line_fmt = self.ftrace_line_fmt_fg
		elif(tracer == 'nop'):
			self.ftrace_line_fmt = self.ftrace_line_fmt_nop
		else:
			doError('Invalid tracer format: [%s]' % tracer, False)






def vprint(msg):
	global sysvals
	if(sysvals.verbose):
		print(msg)



def initFtrace():
	global sysvals
	tp = sysvals.tpath
	cf = 'dpm_run_callback'
	if(sysvals.usetraceeventsonly):
		cf = '-e dpm_prepare -e dpm_complete -e dpm_run_callback'
	if(sysvals.usecallgraph or sysvals.usetraceevents):
		print('INITIALIZING FTRACE...')
		
		os.system('echo 0 > '+tp+'tracing_on')
		
		os.system('echo global > '+tp+'trace_clock')
		
		os.system('echo nop > '+tp+'current_tracer')
		os.system('echo 100000 > '+tp+'buffer_size_kb')
		
		if(sysvals.usecallgraph and sysvals.execcount == 1):
			
			os.system('echo function_graph > '+tp+'current_tracer')
			os.system('echo "" > '+tp+'set_ftrace_filter')
			
			os.system('echo funcgraph-abstime > '+tp+'trace_options')
			os.system('echo funcgraph-proc > '+tp+'trace_options')
			
			os.system('cat '+tp+'available_filter_functions | grep '+\
				cf+' > '+tp+'set_graph_function')
		if(sysvals.usetraceevents):
			
			events = iter(sysvals.traceevents)
			for e in events:
				os.system('echo 1 > '+sysvals.epath+e+'/enable')
		
		os.system('echo "" > '+tp+'trace')



def initFtraceAndroid():
	global sysvals
	tp = sysvals.tpath
	if(sysvals.usetraceevents):
		print('INITIALIZING FTRACE...')
		
		os.system(sysvals.adb+" shell 'echo 0 > "+tp+"tracing_on'")
		
		os.system(sysvals.adb+" shell 'echo global > "+tp+"trace_clock'")
		
		os.system(sysvals.adb+" shell 'echo nop > "+tp+"current_tracer'")
		os.system(sysvals.adb+" shell 'echo 10000 > "+tp+"buffer_size_kb'")
		
		events = iter(sysvals.traceevents)
		for e in events:
			os.system(sysvals.adb+" shell 'echo 1 > "+\
				sysvals.epath+e+"/enable'")
		
		os.system(sysvals.adb+" shell 'echo \"\" > "+tp+"trace'")





def verifyFtrace():
	global sysvals
	
	files = ['buffer_size_kb', 'current_tracer', 'trace', 'trace_clock',
			 'trace_marker', 'trace_options', 'tracing_on']
	
	tp = sysvals.tpath
	if(sysvals.usecallgraph):
		files += [
			'available_filter_functions',
			'set_ftrace_filter',
			'set_graph_function'
		]
	for f in files:
		if(sysvals.android):
			out = os.popen(sysvals.adb+' shell ls '+tp+f).read().strip()
			if(out != tp+f):
				return False
		else:
			if(os.path.exists(tp+f) == False):
				return False
	return True






def parseStamp(m, data):
	global sysvals
	data.stamp = {'time': '', 'host': '', 'mode': ''}
	dt = datetime(int(m.group('y'))+2000, int(m.group('m')),
		int(m.group('d')), int(m.group('H')), int(m.group('M')),
		int(m.group('S')))
	data.stamp['time'] = dt.strftime('%B %d %Y, %I:%M:%S %p')
	data.stamp['host'] = m.group('host')
	data.stamp['mode'] = m.group('mode')
	data.stamp['kernel'] = m.group('kernel')
	sysvals.suspendmode = data.stamp['mode']
	if not sysvals.stamp:
		sysvals.stamp = data.stamp








def diffStamp(stamp1, stamp2):
	if 'host' in stamp1 and 'host' in stamp2:
		if stamp1['host'] != stamp2['host']:
			return True
	if 'kernel' in stamp1 and 'kernel' in stamp2:
		if stamp1['kernel'] != stamp2['kernel']:
			return True
	if 'mode' in stamp1 and 'mode' in stamp2:
		if stamp1['mode'] != stamp2['mode']:
			return True
	return False





def doesTraceLogHaveTraceEvents():
	global sysvals
	sysvals.usetraceeventsonly = True
	sysvals.usetraceevents = False
	for e in sysvals.traceevents:
		out = os.popen('cat '+sysvals.ftracefile+' | grep "'+e+': "').read()
		if(not out):
			sysvals.usetraceeventsonly = False
		if(e == 'suspend_resume' and out):
			sysvals.usetraceevents = True










def appendIncompleteTraceLog(testruns):
	global sysvals
	
	testcnt = len(testruns)
	testidx = -1
	testrun = []
	for data in testruns:
		testrun.append(TestRun(data))
	
	vprint('Analyzing the ftrace data...')
	tf = open(sysvals.ftracefile, 'r')
	for line in tf:
		
		line = line.replace('\r\n', '')
		
		m = re.match(sysvals.stampfmt, line)
		if(m):
			testidx += 1
			parseStamp(m, testrun[testidx].data)
			continue
		
		if(re.match(sysvals.firmwarefmt, line)):
			continue
		
		if(testidx < 0):
			continue
		
		m = re.match(sysvals.tracertypefmt, line)
		if(m):
			tracer = m.group('t')
			testrun[testidx].setTracerType(tracer)
			continue
		
		m = re.match(testrun[testidx].ftrace_line_fmt, line)
		if(not m):
			continue
		
		m_time = m.group('time')
		m_pid = m.group('pid')
		m_msg = m.group('msg')
		if(testrun[testidx].cgformat):
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
		
		data = testrun[testidx].data
		if(not testrun[testidx].inthepipe):
			
			if(t.fevent):
				if(t.name == 'SUSPEND START'):
					testrun[testidx].inthepipe = True
					data.setStart(t.time)
				continue
		else:
			
			if(t.fevent):
				if(t.name == 'RESUME COMPLETE'):
					testrun[testidx].inthepipe = False
					data.setEnd(t.time)
					if(testidx == testcnt - 1):
						break
					continue
				
				if(re.match('(?P<name>.*) begin$', t.name)):
					isbegin = True
				elif(re.match('(?P<name>.*) end$', t.name)):
					isbegin = False
				else:
					continue
				m = re.match('(?P<name>.*)\[(?P<val>[0-9]*)\] .*', t.name)
				if(m):
					val = m.group('val')
					if val == '0':
						name = m.group('name')
					else:
						name = m.group('name')+'['+val+']'
				else:
					m = re.match('(?P<name>.*) .*', t.name)
					name = m.group('name')
				
				if re.match('dpm_prepare\[.*', name):
					continue
				elif re.match('machine_suspend.*', name):
					continue
				elif re.match('suspend_enter\[.*', name):
					if(not isbegin):
						data.dmesg['suspend_prepare']['end'] = t.time
					continue
				elif re.match('dpm_suspend\[.*', name):
					if(not isbegin):
						data.dmesg['suspend']['end'] = t.time
					continue
				elif re.match('dpm_suspend_late\[.*', name):
					if(isbegin):
						data.dmesg['suspend_late']['start'] = t.time
					else:
						data.dmesg['suspend_late']['end'] = t.time
					continue
				elif re.match('dpm_suspend_noirq\[.*', name):
					if(isbegin):
						data.dmesg['suspend_noirq']['start'] = t.time
					else:
						data.dmesg['suspend_noirq']['end'] = t.time
					continue
				elif re.match('dpm_resume_noirq\[.*', name):
					if(isbegin):
						data.dmesg['resume_machine']['end'] = t.time
						data.dmesg['resume_noirq']['start'] = t.time
					else:
						data.dmesg['resume_noirq']['end'] = t.time
					continue
				elif re.match('dpm_resume_early\[.*', name):
					if(isbegin):
						data.dmesg['resume_early']['start'] = t.time
					else:
						data.dmesg['resume_early']['end'] = t.time
					continue
				elif re.match('dpm_resume\[.*', name):
					if(isbegin):
						data.dmesg['resume']['start'] = t.time
					else:
						data.dmesg['resume']['end'] = t.time
					continue
				elif re.match('dpm_complete\[.*', name):
					if(isbegin):
						data.dmesg['resume_complete']['start'] = t.time
					else:
						data.dmesg['resume_complete']['end'] = t.time
					continue
				
				if(data.isTraceEventOutsideDeviceCalls(pid, t.time)):
					
					if(isbegin):
						
						if(name not in testrun[testidx].ttemp):
							testrun[testidx].ttemp[name] = []
						testrun[testidx].ttemp[name].append(\
							{'begin': t.time, 'end': t.time})
					else:
						
						if(name in testrun[testidx].ttemp):
							testrun[testidx].ttemp[name][-1]['end'] = t.time
				else:
					if(isbegin):
						data.addIntraDevTraceEvent('', name, pid, t.time)
					else:
						data.capIntraDevTraceEvent('', name, pid, t.time)
			
			elif sysvals.usecallgraph:
				
				if(pid not in testrun[testidx].ftemp):
					testrun[testidx].ftemp[pid] = []
					testrun[testidx].ftemp[pid].append(FTraceCallGraph())
				
				cg = testrun[testidx].ftemp[pid][-1]
				if(cg.addLine(t, m)):
					testrun[testidx].ftemp[pid].append(FTraceCallGraph())
	tf.close()
	for test in testrun:
		
		if(sysvals.usetraceevents):
			for name in test.ttemp:
				for event in test.ttemp[name]:
					begin = event['begin']
					end = event['end']
					
					if(begin < test.data.start):
						test.data.setStart(begin)
					
					if(end > test.data.end):
						test.data.setEnd(end)
					test.data.newActionGlobal(name, begin, end)
		
		for pid in test.ftemp:
			for cg in test.ftemp[pid]:
				if(not cg.sanityCheck()):
					id = 'task %s cpu %s' % (pid, m.group('cpu'))
					vprint('Sanity check failed for '+\
						id+', ignoring this callback')
					continue
				callstart = cg.start
				callend = cg.end
				for p in test.data.phases:
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
		if(sysvals.verbose):
			test.data.printDetails()
	
	if(len(testruns) > 1):
		t1e = testruns[0].getEnd()
		t2s = testruns[-1].getStart()
		testruns[-1].newPhaseWithSingleAction('user mode', \
			'user mode', t1e, t2s, '








def parseTraceLog():
	global sysvals
	vprint('Analyzing the ftrace data...')
	if(os.path.exists(sysvals.ftracefile) == False):
		doError('%s doesnt exist' % sysvals.ftracefile, False)
	
	testruns = []
	testdata = []
	testrun = 0
	data = 0
	tf = open(sysvals.ftracefile, 'r')
	phase = 'suspend_prepare'
	for line in tf:
		
		line = line.replace('\r\n', '')
		
		m = re.match(sysvals.stampfmt, line)
		if(m):
			data = Data(len(testdata))
			testdata.append(data)
			testrun = TestRun(data)
			testruns.append(testrun)
			parseStamp(m, data)
			continue
		if(not data):
			continue
		
		m = re.match(sysvals.firmwarefmt, line)
		if(m):
			data.fwSuspend = int(m.group('s'))
			data.fwResume = int(m.group('r'))
			if(data.fwSuspend > 0 or data.fwResume > 0):
				data.fwValid = True
			continue
		
		m = re.match(sysvals.tracertypefmt, line)
		if(m):
			tracer = m.group('t')
			testrun.setTracerType(tracer)
			continue
		
		m = re.match(sysvals.postresumefmt, line)
		if(m):
			t = int(m.group('t'))
			if(t > 0):
				sysvals.postresumetime = t
			continue
		
		m = re.match(testrun.ftrace_line_fmt, line)
		if(not m):
			continue
		
		m_time = m.group('time')
		m_pid = m.group('pid')
		m_msg = m.group('msg')
		if(testrun.cgformat):
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
		
		if(not testrun.inthepipe):
			
			if(t.fevent):
				if(t.name == 'SUSPEND START'):
					testrun.inthepipe = True
					data.setStart(t.time)
			continue
		
		if(t.fevent):
			if(t.name == 'RESUME COMPLETE'):
				if(sysvals.postresumetime > 0):
					phase = 'post_resume'
					data.newPhase(phase, t.time, t.time, '
				else:
					testrun.inthepipe = False
				data.setEnd(t.time)
				continue
			if(phase == 'post_resume'):
				data.setEnd(t.time)
			if(t.type == 'suspend_resume'):
				
				if(re.match('(?P<name>.*) begin$', t.name)):
					isbegin = True
				elif(re.match('(?P<name>.*) end$', t.name)):
					isbegin = False
				else:
					continue
				m = re.match('(?P<name>.*)\[(?P<val>[0-9]*)\] .*', t.name)
				if(m):
					val = m.group('val')
					if val == '0':
						name = m.group('name')
					else:
						name = m.group('name')+'['+val+']'
				else:
					m = re.match('(?P<name>.*) .*', t.name)
					name = m.group('name')
				
				if(re.match('acpi_suspend\[.*', t.name) or
					re.match('suspend_enter\[.*', name)):
					continue
				
				
				if(re.match('dpm_prepare\[.*', t.name)):
					phase = 'suspend_prepare'
					if(not isbegin):
						data.dmesg[phase]['end'] = t.time
					continue
				
				elif(re.match('dpm_suspend\[.*', t.name)):
					phase = 'suspend'
					data.setPhase(phase, t.time, isbegin)
					continue
				
				elif(re.match('dpm_suspend_late\[.*', t.name)):
					phase = 'suspend_late'
					data.setPhase(phase, t.time, isbegin)
					continue
				
				elif(re.match('dpm_suspend_noirq\[.*', t.name)):
					phase = 'suspend_noirq'
					data.setPhase(phase, t.time, isbegin)
					if(not isbegin):
						phase = 'suspend_machine'
						data.dmesg[phase]['start'] = t.time
					continue
				
				elif(re.match('machine_suspend\[.*', t.name)):
					if(isbegin):
						phase = 'suspend_machine'
						data.dmesg[phase]['end'] = t.time
						data.tSuspended = t.time
					else:
						if(sysvals.suspendmode in ['mem', 'disk']):
							data.dmesg['suspend_machine']['end'] = t.time
							data.tSuspended = t.time
						phase = 'resume_machine'
						data.dmesg[phase]['start'] = t.time
						data.tResumed = t.time
						data.tLow = data.tResumed - data.tSuspended
					continue
				
				elif(re.match('dpm_resume_noirq\[.*', t.name)):
					phase = 'resume_noirq'
					data.setPhase(phase, t.time, isbegin)
					if(isbegin):
						data.dmesg['resume_machine']['end'] = t.time
					continue
				
				elif(re.match('dpm_resume_early\[.*', t.name)):
					phase = 'resume_early'
					data.setPhase(phase, t.time, isbegin)
					continue
				
				elif(re.match('dpm_resume\[.*', t.name)):
					phase = 'resume'
					data.setPhase(phase, t.time, isbegin)
					continue
				
				elif(re.match('dpm_complete\[.*', t.name)):
					phase = 'resume_complete'
					if(isbegin):
						data.dmesg[phase]['start'] = t.time
					continue
				
				if(data.isTraceEventOutsideDeviceCalls(pid, t.time)):
					
					if(name not in testrun.ttemp):
						testrun.ttemp[name] = []
					if(isbegin):
						
						testrun.ttemp[name].append(\
							{'begin': t.time, 'end': t.time})
					else:
						if(len(testrun.ttemp[name]) > 0):
							
							testrun.ttemp[name][-1]['end'] = t.time
						elif(phase == 'post_resume'):
							
							testrun.ttemp[name].append({
								'begin': data.dmesg[phase]['start'],
								'end': t.time})
				else:
					if(isbegin):
						data.addIntraDevTraceEvent('', name, pid, t.time)
					else:
						data.capIntraDevTraceEvent('', name, pid, t.time)
			
			elif(t.type == 'device_pm_callback_start'):
				m = re.match('(?P<drv>.*) (?P<d>.*), parent: *(?P<p>.*), .*',\
					t.name);
				if(not m):
					continue
				drv = m.group('drv')
				n = m.group('d')
				p = m.group('p')
				if(n and p):
					data.newAction(phase, n, pid, p, t.time, -1, drv)
			
			elif(t.type == 'device_pm_callback_end'):
				m = re.match('(?P<drv>.*) (?P<d>.*), err.*', t.name);
				if(not m):
					continue
				n = m.group('d')
				list = data.dmesg[phase]['list']
				if(n in list):
					dev = list[n]
					dev['length'] = t.time - dev['start']
					dev['end'] = t.time
		
		elif sysvals.usecallgraph:
			
			if(phase == 'post_resume'):
				continue
			
			if(pid not in testrun.ftemp):
				testrun.ftemp[pid] = []
				testrun.ftemp[pid].append(FTraceCallGraph())
			
			cg = testrun.ftemp[pid][-1]
			if(cg.addLine(t, m)):
				testrun.ftemp[pid].append(FTraceCallGraph())
	tf.close()
	for test in testruns:
		
		if(sysvals.usetraceevents):
			for name in test.ttemp:
				for event in test.ttemp[name]:
					begin = event['begin']
					end = event['end']
					
					if(begin < test.data.start):
						test.data.setStart(begin)
					
					if(end > test.data.end):
						test.data.setEnd(end)
					test.data.newActionGlobal(name, begin, end)
		
		borderphase = {
			'dpm_prepare': 'suspend_prepare',
			'dpm_complete': 'resume_complete'
		}
		for pid in test.ftemp:
			for cg in test.ftemp[pid]:
				if len(cg.list) < 2:
					continue
				if(not cg.sanityCheck()):
					id = 'task %s cpu %s' % (pid, m.group('cpu'))
					vprint('Sanity check failed for '+\
						id+', ignoring this callback')
					continue
				callstart = cg.start
				callend = cg.end
				if(cg.list[0].name in borderphase):
					p = borderphase[cg.list[0].name]
					list = test.data.dmesg[p]['list']
					for devname in list:
						dev = list[devname]
						if(pid == dev['pid'] and
							callstart <= dev['start'] and
							callend >= dev['end']):
							dev['ftrace'] = cg.slice(dev['start'], dev['end'])
					continue
				if(cg.list[0].name != 'dpm_run_callback'):
					continue
				for p in test.data.phases:
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
	
	for data in testdata:
		lp = data.phases[0]
		for p in data.phases:
			if(data.dmesg[p]['start'] < 0 and data.dmesg[p]['end'] < 0):
				print('WARNING: phase "%s" is missing!' % p)
			if(data.dmesg[p]['start'] < 0):
				data.dmesg[p]['start'] = data.dmesg[lp]['end']
				if(p == 'resume_machine'):
					data.tSuspended = data.dmesg[lp]['end']
					data.tResumed = data.dmesg[lp]['end']
					data.tLow = 0
			if(data.dmesg[p]['end'] < 0):
				data.dmesg[p]['end'] = data.dmesg[p]['start']
			lp = p
		if(len(sysvals.devicefilter) > 0):
			data.deviceFilter(sysvals.devicefilter)
		data.fixupInitcallsThatDidntReturn()
		if(sysvals.verbose):
			data.printDetails()
	
	if(len(testdata) > 1):
		t1e = testdata[0].getEnd()
		t2s = testdata[-1].getStart()
		testdata[-1].newPhaseWithSingleAction('user mode', \
			'user mode', t1e, t2s, '
	return testdata







def loadKernelLog():
	global sysvals
	vprint('Analyzing the dmesg data...')
	if(os.path.exists(sysvals.dmesgfile) == False):
		doError('%s doesnt exist' % sysvals.dmesgfile, False)
	
	testruns = []
	data = 0
	lf = open(sysvals.dmesgfile, 'r')
	for line in lf:
		line = line.replace('\r\n', '')
		idx = line.find('[')
		if idx > 1:
			line = line[idx:]
		m = re.match(sysvals.stampfmt, line)
		if(m):
			if(data):
				testruns.append(data)
			data = Data(len(testruns))
			parseStamp(m, data)
			continue
		if(not data):
			continue
		m = re.match(sysvals.firmwarefmt, line)
		if(m):
			data.fwSuspend = int(m.group('s'))
			data.fwResume = int(m.group('r'))
			if(data.fwSuspend > 0 or data.fwResume > 0):
				data.fwValid = True
			continue
		m = re.match('[ \t]*(\[ *)(?P<ktime>[0-9\.]*)(\]) (?P<msg>.*)', line)
		if(m):
			data.dmesgtext.append(line)
			if(re.match('ACPI: resume from mwait', m.group('msg'))):
				print('NOTE: This suspend appears to be freeze rather than'+\
					' %s, it will be treated as such' % sysvals.suspendmode)
				sysvals.suspendmode = 'freeze'
		else:
			vprint('ignoring dmesg line: %s' % line.replace('\n', ''))
	testruns.append(data)
	lf.close()
	if(not data):
		print('ERROR: analyze_suspend header missing from dmesg log')
		sys.exit()
	
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
	global sysvals
	phase = 'suspend_runtime'
	if(data.fwValid):
		vprint('Firmware Suspend = %u ns, Firmware Resume = %u ns' % \
			(data.fwSuspend, data.fwResume))
	
	dm = {
		'suspend_prepare': 'PM: Syncing filesystems.*',
		        'suspend': 'PM: Entering [a-z]* sleep.*',
		   'suspend_late': 'PM: suspend of devices complete after.*',
		  'suspend_noirq': 'PM: late suspend of devices complete after.*',
		'suspend_machine': 'PM: noirq suspend of devices complete after.*',
		 'resume_machine': 'ACPI: Low-level resume complete.*',
		   'resume_noirq': 'ACPI: Waking up from system sleep state.*',
		   'resume_early': 'PM: noirq resume of devices complete after.*',
		         'resume': 'PM: early resume of devices complete after.*',
		'resume_complete': 'PM: resume of devices complete after.*',
		    'post_resume': '.*Restarting tasks \.\.\..*',
	}
	if(sysvals.suspendmode == 'standby'):
		dm['resume_machine'] = 'PM: Restoring platform NVS memory'
	elif(sysvals.suspendmode == 'disk'):
		dm['suspend_late'] = 'PM: freeze of devices complete after.*'
		dm['suspend_noirq'] = 'PM: late freeze of devices complete after.*'
		dm['suspend_machine'] = 'PM: noirq freeze of devices complete after.*'
		dm['resume_machine'] = 'PM: Restoring platform NVS memory'
		dm['resume_early'] = 'PM: noirq restore of devices complete after.*'
		dm['resume'] = 'PM: early restore of devices complete after.*'
		dm['resume_complete'] = 'PM: restore of devices complete after.*'
	elif(sysvals.suspendmode == 'freeze'):
		dm['resume_machine'] = 'ACPI: resume from mwait'
	
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
				doWarning('INVALID DMESG LINE: '+\
					line.replace('\n', ''), 'dmesg')
				continue
			msg = m.group('msg')
			
			if t0 < 0:
				data.setStart(ktime)
				t0 = ktime
		else:
			continue
		
		if(not sysvals.usetraceevents and sysvals.suspendmode == 'freeze' \
			and phase == 'resume_machine' and \
			re.match('calling  (?P<f>.*)\+ @ .*, parent: .*', msg)):
			data.dmesg['resume_machine']['end'] = ktime
			phase = 'resume_noirq'
			data.dmesg[phase]['start'] = ktime
		
		
		if(re.match(dm['suspend_prepare'], msg)):
			phase = 'suspend_prepare'
			data.dmesg[phase]['start'] = ktime
			data.setStart(ktime)
		
		elif(re.match(dm['suspend'], msg)):
			data.dmesg['suspend_prepare']['end'] = ktime
			phase = 'suspend'
			data.dmesg[phase]['start'] = ktime
		
		elif(re.match(dm['suspend_late'], msg)):
			data.dmesg['suspend']['end'] = ktime
			phase = 'suspend_late'
			data.dmesg[phase]['start'] = ktime
		
		elif(re.match(dm['suspend_noirq'], msg)):
			data.dmesg['suspend_late']['end'] = ktime
			phase = 'suspend_noirq'
			data.dmesg[phase]['start'] = ktime
		
		elif(re.match(dm['suspend_machine'], msg)):
			data.dmesg['suspend_noirq']['end'] = ktime
			phase = 'suspend_machine'
			data.dmesg[phase]['start'] = ktime
		
		elif(re.match(dm['resume_machine'], msg)):
			if(sysvals.suspendmode in ['freeze', 'standby']):
				data.tSuspended = prevktime
				data.dmesg['suspend_machine']['end'] = prevktime
			else:
				data.tSuspended = ktime
				data.dmesg['suspend_machine']['end'] = ktime
			phase = 'resume_machine'
			data.tResumed = ktime
			data.tLow = data.tResumed - data.tSuspended
			data.dmesg[phase]['start'] = ktime
		
		elif(re.match(dm['resume_noirq'], msg)):
			data.dmesg['resume_machine']['end'] = ktime
			phase = 'resume_noirq'
			data.dmesg[phase]['start'] = ktime
		
		elif(re.match(dm['resume_early'], msg)):
			data.dmesg['resume_noirq']['end'] = ktime
			phase = 'resume_early'
			data.dmesg[phase]['start'] = ktime
		
		elif(re.match(dm['resume'], msg)):
			data.dmesg['resume_early']['end'] = ktime
			phase = 'resume'
			data.dmesg[phase]['start'] = ktime
		
		elif(re.match(dm['resume_complete'], msg)):
			data.dmesg['resume']['end'] = ktime
			phase = 'resume_complete'
			data.dmesg[phase]['start'] = ktime
		
		elif(re.match(dm['post_resume'], msg)):
			data.dmesg['resume_complete']['end'] = ktime
			data.setEnd(ktime)
			phase = 'post_resume'
			break
		
		if(phase in data.phases):
			
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
			
			for a in at:
				if(re.match(at[a]['smsg'], msg)):
					if(a not in actions):
						actions[a] = []
					actions[a].append({'begin': ktime, 'end': ktime})
				if(re.match(at[a]['emsg'], msg)):
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
	
	lp = data.phases[0]
	for p in data.phases:
		if(data.dmesg[p]['start'] < 0 and data.dmesg[p]['end'] < 0):
			print('WARNING: phase "%s" is missing, something went wrong!' % p)
			print('    In %s, this dmesg line denotes the start of %s:' % \
				(sysvals.suspendmode, p))
			print('        "%s"' % dm[p])
		if(data.dmesg[p]['start'] < 0):
			data.dmesg[p]['start'] = data.dmesg[lp]['end']
			if(p == 'resume_machine'):
				data.tSuspended = data.dmesg[lp]['end']
				data.tResumed = data.dmesg[lp]['end']
				data.tLow = 0
		if(data.dmesg[p]['end'] < 0):
			data.dmesg[p]['end'] = data.dmesg[p]['start']
		lp = p
	
	for name in actions:
		for event in actions[name]:
			begin = event['begin']
			end = event['end']
			
			if(begin < data.start):
				data.setStart(begin)
			
			if(end > data.end):
				data.setEnd(end)
			data.newActionGlobal(name, begin, end)
	if(sysvals.verbose):
		data.printDetails()
	if(len(sysvals.devicefilter) > 0):
		data.deviceFilter(sysvals.devicefilter)
	data.fixupInitcallsThatDidntReturn()
	return True









def setTimelineRows(list, sortedkeys):
	
	remaining = len(list)
	rowdata = dict()
	row = 0
	for item in list:
		list[item]['row'] = -1
	
	while(remaining > 0):
		if(row not in rowdata):
			rowdata[row] = []
		for item in sortedkeys:
			if(list[item]['row'] < 0):
				s = list[item]['start']
				e = list[item]['end']
				valid = True
				for ritem in rowdata[row]:
					rs = ritem['start']
					re = ritem['end']
					if(not (((s <= rs) and (e <= rs)) or
						((s >= re) and (e >= re)))):
						valid = False
						break
				if(valid):
					rowdata[row].append(list[item])
					list[item]['row'] = row
					remaining -= 1
		row += 1
	return row









def createTimeScale(t0, tMax, tSuspended):
	timescale = '<div class="t" style="right:{0}%">{1}</div>\n'
	output = '<div id="timescale">\n'
	
	tTotal = tMax - t0
	tS = 0.1
	if(tTotal <= 0):
		return output
	if(tTotal > 4):
		tS = 1
	if(tSuspended < 0):
		for i in range(int(tTotal/tS)+1):
			pos = '%0.3f' % (100 - ((float(i)*tS*100)/tTotal))
			if(i > 0):
				val = '%0.fms' % (float(i)*tS*1000)
			else:
				val = ''
			output += timescale.format(pos, val)
	else:
		tSuspend = tSuspended - t0
		divTotal = int(tTotal/tS) + 1
		divSuspend = int(tSuspend/tS)
		s0 = (tSuspend - tS*divSuspend)*100/tTotal
		for i in range(divTotal):
			pos = '%0.3f' % (100 - ((float(i)*tS*100)/tTotal) - s0)
			if((i == 0) and (s0 < 3)):
				val = ''
			elif(i == divSuspend):
				val = 'S/R'
			else:
				val = '%0.fms' % (float(i-divSuspend)*tS*1000)
			output += timescale.format(pos, val)
	output += '</div>\n'
	return output





def createHTMLSummarySimple(testruns, htmlfile):
	global sysvals
	
	hf = open(htmlfile, 'w')
	
	html = '<!DOCTYPE html>\n<html>\n<head>\n\
	<meta http-equiv="content-type" content="text/html; charset=UTF-8">\n\
	<title>AnalyzeSuspend Summary</title>\n\
	<style type=\'text/css\'>\n\
		body {overflow-y: scroll;}\n\
		.stamp {width: 100%;text-align:center;background-color:
		table {width:100%;border-collapse: collapse;}\n\
		.summary {font: 22px Arial;border:1px solid;}\n\
		th {border: 1px solid black;background-color:
		td {text-align: center;}\n\
		tr.alt td {background-color:
		tr.avg td {background-color:
		a:link {color: 
		a:visited {color: 
		a:hover {color: 
		a:active {color: 
	</style>\n</head>\n<body>\n'
	
	count = len(testruns)
	headline_stamp = '<div class="stamp">{0} {1} {2} {3} ({4} tests)</div>\n'
	html += headline_stamp.format(sysvals.stamp['host'],
		sysvals.stamp['kernel'], sysvals.stamp['mode'],
		sysvals.stamp['time'], count)
	
	stampcolumns = False
	for data in testruns:
		if diffStamp(sysvals.stamp, data.stamp):
			stampcolumns = True
			break
	th = '\t<th>{0}</th>\n'
	td = '\t<td>{0}</td>\n'
	tdlink = '\t<td><a href="{0}">Click Here</a></td>\n'
	
	html += '<table class="summary">\n<tr>\n'
	html += th.format("Test ")
	if stampcolumns:
		html += th.format("Hostname")
		html += th.format("Kernel Version")
		html += th.format("Suspend Mode")
	html += th.format("Test Time")
	html += th.format("Suspend Time")
	html += th.format("Resume Time")
	html += th.format("Detail")
	html += '</tr>\n'
	
	sTimeAvg = 0.0
	rTimeAvg = 0.0
	num = 1
	for data in testruns:
		
		resumeEnd = data.dmesg['resume_complete']['end']
		if num % 2 == 1:
			html += '<tr class="alt">\n'
		else:
			html += '<tr>\n'
		
		html += td.format("test %d" % num)
		num += 1
		if stampcolumns:
			
			val = "unknown"
			if('host' in data.stamp):
				val = data.stamp['host']
			html += td.format(val)
			
			val = "unknown"
			if('kernel' in data.stamp):
				val = data.stamp['kernel']
			html += td.format(val)
			
			val = "unknown"
			if('mode' in data.stamp):
				val = data.stamp['mode']
			html += td.format(val)
		
		val = "unknown"
		if('time' in data.stamp):
			val = data.stamp['time']
		html += td.format(val)
		
		sTime = (data.tSuspended - data.start)*1000
		sTimeAvg += sTime
		html += td.format("%3.3f ms" % sTime)
		
		rTime = (resumeEnd - data.tResumed)*1000
		rTimeAvg += rTime
		html += td.format("%3.3f ms" % rTime)
		
		html += tdlink.format(data.outfile)
		html += '</tr>\n'
	
	if(count > 0):
		sTimeAvg /= count
		rTimeAvg /= count
	html += '<tr class="avg">\n'
	html += td.format('Average') 	
	if stampcolumns:
		html += td.format('')			
		html += td.format('')			
		html += td.format('')			
	html += td.format('')			
	html += td.format("%3.3f ms" % sTimeAvg)	
	html += td.format("%3.3f ms" % rTimeAvg)	
	html += td.format('')			
	html += '</tr>\n'
	
	hf.write(html+'</table>\n')
	hf.write('</body>\n</html>\n')
	hf.close()







def createHTML(testruns):
	global sysvals
	for data in testruns:
		data.normalizeTime(testruns[-1].tSuspended)
	x2changes = ['', 'absolute']
	if len(testruns) > 1:
		x2changes = ['1', 'relative']
	
	headline_stamp = '<div class="stamp">{0} {1} {2} {3}</div>\n'
	html_devlist1 = '<button id="devlist1" class="devlist" style="float:left;">Device Detail%s</button>' % x2changes[0]
	html_zoombox = '<center><button id="zoomin">ZOOM IN</button><button id="zoomout">ZOOM OUT</button><button id="zoomdef">ZOOM 1:1</button></center>\n'
	html_devlist2 = '<button id="devlist2" class="devlist" style="float:right;">Device Detail2</button>\n'
	html_timeline = '<div id="dmesgzoombox" class="zoombox">\n<div id="{0}" class="timeline" style="height:{1}px">\n'
	html_device = '<div id="{0}" title="{1}" class="thread" style="left:{2}%;top:{3}%;height:{4}%;width:{5}%;">{6}</div>\n'
	html_traceevent = '<div title="{0}" class="traceevent" style="left:{1}%;top:{2}%;height:{3}%;width:{4}%;border:1px solid {5};background-color:{5}">{6}</div>\n'
	html_phase = '<div class="phase" style="left:{0}%;width:{1}%;top:{2}%;height:{3}%;background-color:{4}">{5}</div>\n'
	html_phaselet = '<div id="{0}" class="phaselet" style="left:{1}%;width:{2}%;background-color:{3}"></div>\n'
	html_legend = '<div class="square" style="left:{0}%;background-color:{1}">&nbsp;{2}</div>\n'
	html_timetotal = '<table class="time1">\n<tr>'\
		'<td class="green">{2} Suspend Time: <b>{0} ms</b></td>'\
		'<td class="yellow">{2} Resume Time: <b>{1} ms</b></td>'\
		'</tr>\n</table>\n'
	html_timetotal2 = '<table class="time1">\n<tr>'\
		'<td class="green">{3} Suspend Time: <b>{0} ms</b></td>'\
		'<td class="gray">'+sysvals.suspendmode+' time: <b>{1} ms</b></td>'\
		'<td class="yellow">{3} Resume Time: <b>{2} ms</b></td>'\
		'</tr>\n</table>\n'
	html_timegroups = '<table class="time2">\n<tr>'\
		'<td class="green">{4}Kernel Suspend: {0} ms</td>'\
		'<td class="purple">{4}Firmware Suspend: {1} ms</td>'\
		'<td class="purple">{4}Firmware Resume: {2} ms</td>'\
		'<td class="yellow">{4}Kernel Resume: {3} ms</td>'\
		'</tr>\n</table>\n'
	
	vprint('Creating Device Timeline...')
	devtl = Timeline()
	
	textnum = ['First', 'Second']
	for data in testruns:
		tTotal = data.end - data.start
		tEnd = data.dmesg['resume_complete']['end']
		if(tTotal == 0):
			print('ERROR: No timeline data')
			sys.exit()
		if(data.tLow > 0):
			low_time = '%.0f'%(data.tLow*1000)
		if data.fwValid:
			suspend_time = '%.0f'%((data.tSuspended-data.start)*1000 + \
				(data.fwSuspend/1000000.0))
			resume_time = '%.0f'%((tEnd-data.tSuspended)*1000 + \
				(data.fwResume/1000000.0))
			testdesc1 = 'Total'
			testdesc2 = ''
			if(len(testruns) > 1):
				testdesc1 = testdesc2 = textnum[data.testnumber]
				testdesc2 += ' '
			if(data.tLow == 0):
				thtml = html_timetotal.format(suspend_time, \
					resume_time, testdesc1)
			else:
				thtml = html_timetotal2.format(suspend_time, low_time, \
					resume_time, testdesc1)
			devtl.html['timeline'] += thtml
			sktime = '%.3f'%((data.dmesg['suspend_machine']['end'] - \
				data.getStart())*1000)
			sftime = '%.3f'%(data.fwSuspend / 1000000.0)
			rftime = '%.3f'%(data.fwResume / 1000000.0)
			rktime = '%.3f'%((data.getEnd() - \
				data.dmesg['resume_machine']['start'])*1000)
			devtl.html['timeline'] += html_timegroups.format(sktime, \
				sftime, rftime, rktime, testdesc2)
		else:
			suspend_time = '%.0f'%((data.tSuspended-data.start)*1000)
			resume_time = '%.0f'%((tEnd-data.tSuspended)*1000)
			testdesc = 'Kernel'
			if(len(testruns) > 1):
				testdesc = textnum[data.testnumber]+' '+testdesc
			if(data.tLow == 0):
				thtml = html_timetotal.format(suspend_time, \
					resume_time, testdesc)
			else:
				thtml = html_timetotal2.format(suspend_time, low_time, \
					resume_time, testdesc)
			devtl.html['timeline'] += thtml
	
	t0 = testruns[0].start
	tMax = testruns[-1].end
	tSuspended = testruns[-1].tSuspended
	tTotal = tMax - t0
	
	timelinerows = 0
	for data in testruns:
		for phase in data.dmesg:
			list = data.dmesg[phase]['list']
			rows = setTimelineRows(list, list)
			data.dmesg[phase]['row'] = rows
			if(rows > timelinerows):
				timelinerows = rows
	
	devtl.setRows(timelinerows + 1)
	devtl.html['timeline'] += html_devlist1
	if len(testruns) > 1:
		devtl.html['timeline'] += html_devlist2
	devtl.html['timeline'] += html_zoombox
	devtl.html['timeline'] += html_timeline.format('dmesg', devtl.height)
	
	for data in testruns:
		for b in data.dmesg:
			phase = data.dmesg[b]
			length = phase['end']-phase['start']
			left = '%.3f' % (((phase['start']-t0)*100.0)/tTotal)
			width = '%.3f' % ((length*100.0)/tTotal)
			devtl.html['timeline'] += html_phase.format(left, width, \
				'%.3f'%devtl.scaleH, '%.3f'%(100-devtl.scaleH), \
				data.dmesg[b]['color'], '')
	
	devtl.html['scale'] = createTimeScale(t0, tMax, tSuspended)
	devtl.html['timeline'] += devtl.html['scale']
	for data in testruns:
		for b in data.dmesg:
			phaselist = data.dmesg[b]['list']
			for d in phaselist:
				name = d
				drv = ''
				dev = phaselist[d]
				if(d in sysvals.altdevname):
					name = sysvals.altdevname[d]
				if('drv' in dev and dev['drv']):
					drv = ' {%s}' % dev['drv']
				height = (100.0 - devtl.scaleH)/data.dmesg[b]['row']
				top = '%.3f' % ((dev['row']*height) + devtl.scaleH)
				left = '%.3f' % (((dev['start']-t0)*100)/tTotal)
				width = '%.3f' % (((dev['end']-dev['start'])*100)/tTotal)
				length = ' (%0.3f ms) ' % ((dev['end']-dev['start'])*1000)
				color = 'rgba(204,204,204,0.5)'
				devtl.html['timeline'] += html_device.format(dev['id'], \
					d+drv+length+b, left, top, '%.3f'%height, width, name+drv)
	
	for data in testruns:
		for b in data.dmesg:
			phaselist = data.dmesg[b]['list']
			for name in phaselist:
				dev = phaselist[name]
				if('traceevents' in dev):
					vprint('Debug trace events found for device %s' % name)
					vprint('%20s %20s %10s %8s' % ('action', \
						'name', 'time(ms)', 'length(ms)'))
					for e in dev['traceevents']:
						vprint('%20s %20s %10.3f %8.3f' % (e.action, \
							e.name, e.time*1000, e.length*1000))
						height = (100.0 - devtl.scaleH)/data.dmesg[b]['row']
						top = '%.3f' % ((dev['row']*height) + devtl.scaleH)
						left = '%.3f' % (((e.time-t0)*100)/tTotal)
						width = '%.3f' % (e.length*100/tTotal)
						color = 'rgba(204,204,204,0.5)'
						devtl.html['timeline'] += \
							html_traceevent.format(e.action+' '+e.name, \
								left, top, '%.3f'%height, \
								width, e.color, '')
	
	devtl.html['timeline'] += '</div>\n</div>\n'
	
	data = testruns[-1]
	devtl.html['legend'] = '<div class="legend">\n'
	pdelta = 100.0/len(data.phases)
	pmargin = pdelta / 4.0
	for phase in data.phases:
		order = '%.2f' % ((data.dmesg[phase]['order'] * pdelta) + pmargin)
		name = string.replace(phase, '_', ' &nbsp;')
		devtl.html['legend'] += html_legend.format(order, \
			data.dmesg[phase]['color'], name)
	devtl.html['legend'] += '</div>\n'
	hf = open(sysvals.htmlfile, 'w')
	thread_height = 0
	
	html_header = '<!DOCTYPE html>\n<html>\n<head>\n\
	<meta http-equiv="content-type" content="text/html; charset=UTF-8">\n\
	<title>AnalyzeSuspend</title>\n\
	<style type=\'text/css\'>\n\
		body {overflow-y: scroll;}\n\
		.stamp {width: 100%;text-align:center;background-color:gray;line-height:30px;color:white;font: 25px Arial;}\n\
		.callgraph {margin-top: 30px;box-shadow: 5px 5px 20px black;}\n\
		.callgraph article * {padding-left: 28px;}\n\
		h1 {color:black;font: bold 30px Times;}\n\
		t0 {color:black;font: bold 30px Times;}\n\
		t1 {color:black;font: 30px Times;}\n\
		t2 {color:black;font: 25px Times;}\n\
		t3 {color:black;font: 20px Times;white-space:nowrap;}\n\
		t4 {color:black;font: bold 30px Times;line-height:60px;white-space:nowrap;}\n\
		table {width:100%;}\n\
		.gray {background-color:rgba(80,80,80,0.1);}\n\
		.green {background-color:rgba(204,255,204,0.4);}\n\
		.purple {background-color:rgba(128,0,128,0.2);}\n\
		.yellow {background-color:rgba(255,255,204,0.4);}\n\
		.time1 {font: 22px Arial;border:1px solid;}\n\
		.time2 {font: 15px Arial;border-bottom:1px solid;border-left:1px solid;border-right:1px solid;}\n\
		td {text-align: center;}\n\
		r {color:
		n {color:
		.tdhl {color: red;}\n\
		.hide {display: none;}\n\
		.pf {display: none;}\n\
		.pf:checked + label {background: url(\'data:image/svg+xml;utf,<?xml version="1.0" standalone="no"?><svg xmlns="http://www.w3.org/2000/svg" height="18" width="18" version="1.1"><circle cx="9" cy="9" r="8" stroke="black" stroke-width="1" fill="white"/><rect x="4" y="8" width="10" height="2" style="fill:black;stroke-width:0"/><rect x="8" y="4" width="2" height="10" style="fill:black;stroke-width:0"/></svg>\') no-repeat left center;}\n\
		.pf:not(:checked) ~ label {background: url(\'data:image/svg+xml;utf,<?xml version="1.0" standalone="no"?><svg xmlns="http://www.w3.org/2000/svg" height="18" width="18" version="1.1"><circle cx="9" cy="9" r="8" stroke="black" stroke-width="1" fill="white"/><rect x="4" y="8" width="10" height="2" style="fill:black;stroke-width:0"/></svg>\') no-repeat left center;}\n\
		.pf:checked ~ *:not(:nth-child(2)) {display: none;}\n\
		.zoombox {position: relative; width: 100%; overflow-x: scroll;}\n\
		.timeline {position: relative; font-size: 14px;cursor: pointer;width: 100%; overflow: hidden; background-color:
		.thread {position: absolute; height: '+'%.3f'%thread_height+'%; overflow: hidden; line-height: 30px; border:1px solid;text-align:center;white-space:nowrap;background-color:rgba(204,204,204,0.5);}\n\
		.thread:hover {background-color:white;border:1px solid red;z-index:10;}\n\
		.hover {background-color:white;border:1px solid red;z-index:10;}\n\
		.traceevent {position: absolute;opacity: 0.3;height: '+'%.3f'%thread_height+'%;width:0;overflow:hidden;line-height:30px;text-align:center;white-space:nowrap;}\n\
		.phase {position: absolute;overflow: hidden;border:0px;text-align:center;}\n\
		.phaselet {position:absolute;overflow:hidden;border:0px;text-align:center;height:100px;font-size:24px;}\n\
		.t {position:absolute;top:0%;height:100%;border-right:1px solid black;}\n\
		.legend {position: relative; width: 100%; height: 40px; text-align: center;margin-bottom:20px}\n\
		.legend .square {position:absolute;top:10px; width: 0px;height: 20px;border:1px solid;padding-left:20px;}\n\
		button {height:40px;width:200px;margin-bottom:20px;margin-top:20px;font-size:24px;}\n\
		.devlist {position:'+x2changes[1]+';width:190px;}\n\
		
	</style>\n</head>\n<body>\n'
	hf.write(html_header)
	
	if(sysvals.stamp['time'] != ""):
		hf.write(headline_stamp.format(sysvals.stamp['host'],
			sysvals.stamp['kernel'], sysvals.stamp['mode'], \
				sysvals.stamp['time']))
	
	hf.write(devtl.html['timeline'])
	hf.write(devtl.html['legend'])
	hf.write('<div id="devicedetailtitle"></div>\n')
	hf.write('<div id="devicedetail" style="display:none;">\n')
	
	for data in testruns:
		hf.write('<div id="devicedetail%d">\n' % data.testnumber)
		for b in data.phases:
			phase = data.dmesg[b]
			length = phase['end']-phase['start']
			left = '%.3f' % (((phase['start']-t0)*100.0)/tTotal)
			width = '%.3f' % ((length*100.0)/tTotal)
			hf.write(html_phaselet.format(b, left, width, \
				data.dmesg[b]['color']))
		hf.write('</div>\n')
	hf.write('</div>\n')
	
	data = testruns[-1]
	if(sysvals.usecallgraph):
		hf.write('<section id="callgraphs" class="callgraph">\n')
		
		html_func_top = '<article id="{0}" class="atop" style="background-color:{1}">\n<input type="checkbox" class="pf" id="f{2}" checked/><label for="f{2}">{3} {4}</label>\n'
		html_func_start = '<article>\n<input type="checkbox" class="pf" id="f{0}" checked/><label for="f{0}">{1} {2}</label>\n'
		html_func_end = '</article>\n'
		html_func_leaf = '<article>{0} {1}</article>\n'
		num = 0
		for p in data.phases:
			list = data.dmesg[p]['list']
			for devname in data.sortedDevices(p):
				if('ftrace' not in list[devname]):
					continue
				name = devname
				if(devname in sysvals.altdevname):
					name = sysvals.altdevname[devname]
				devid = list[devname]['id']
				cg = list[devname]['ftrace']
				flen = '<r>(%.3f ms @ %.3f to %.3f)</r>' % \
					((cg.end - cg.start)*1000, cg.start*1000, cg.end*1000)
				hf.write(html_func_top.format(devid, data.dmesg[p]['color'], \
					num, name+' '+p, flen))
				num += 1
				for line in cg.list:
					if(line.length < 0.000000001):
						flen = ''
					else:
						flen = '<n>(%.3f ms @ %.3f)</n>' % (line.length*1000, \
							line.time*1000)
					if(line.freturn and line.fcall):
						hf.write(html_func_leaf.format(line.name, flen))
					elif(line.freturn):
						hf.write(html_func_end)
					else:
						hf.write(html_func_start.format(num, line.name, flen))
						num += 1
				hf.write(html_func_end)
		hf.write('\n\n    </section>\n')
	
	addScriptCode(hf, testruns)
	hf.write('</body>\n</html>\n')
	hf.close()
	return True






def addScriptCode(hf, testruns):
	t0 = (testruns[0].start - testruns[-1].tSuspended) * 1000
	tMax = (testruns[-1].end - testruns[-1].tSuspended) * 1000
	
	detail = '	var devtable = [];\n'
	for data in testruns:
		topo = data.deviceTopology()
		detail += '	devtable[%d] = "%s";\n' % (data.testnumber, topo)
	detail += '	var bounds = [%f,%f];\n' % (t0, tMax)
	
	script_code = \
	'<script type="text/javascript">\n'+detail+\
	'	function zoomTimeline() {\n'\
	'		var timescale = document.getElementById("timescale");\n'\
	'		var dmesg = document.getElementById("dmesg");\n'\
	'		var zoombox = document.getElementById("dmesgzoombox");\n'\
	'		var val = parseFloat(dmesg.style.width);\n'\
	'		var newval = 100;\n'\
	'		var sh = window.outerWidth / 2;\n'\
	'		if(this.id == "zoomin") {\n'\
	'			newval = val * 1.2;\n'\
	'			if(newval > 40000) newval = 40000;\n'\
	'			dmesg.style.width = newval+"%";\n'\
	'			zoombox.scrollLeft = ((zoombox.scrollLeft + sh) * newval / val) - sh;\n'\
	'		} else if (this.id == "zoomout") {\n'\
	'			newval = val / 1.2;\n'\
	'			if(newval < 100) newval = 100;\n'\
	'			dmesg.style.width = newval+"%";\n'\
	'			zoombox.scrollLeft = ((zoombox.scrollLeft + sh) * newval / val) - sh;\n'\
	'		} else {\n'\
	'			zoombox.scrollLeft = 0;\n'\
	'			dmesg.style.width = "100%";\n'\
	'		}\n'\
	'		var html = "";\n'\
	'		var t0 = bounds[0];\n'\
	'		var tMax = bounds[1];\n'\
	'		var tTotal = tMax - t0;\n'\
	'		var wTotal = tTotal * 100.0 / newval;\n'\
	'		for(var tS = 1000; (wTotal / tS) < 3; tS /= 10);\n'\
	'		if(tS < 1) tS = 1;\n'\
	'		for(var s = ((t0 / tS)|0) * tS; s < tMax; s += tS) {\n'\
	'			var pos = (tMax - s) * 100.0 / tTotal;\n'\
	'			var name = (s == 0)?"S/R":(s+"ms");\n'\
	'			html += "<div class=\\"t\\" style=\\"right:"+pos+"%\\">"+name+"</div>";\n'\
	'		}\n'\
	'		timescale.innerHTML = html;\n'\
	'	}\n'\
	'	function deviceHover() {\n'\
	'		var name = this.title.slice(0, this.title.indexOf(" ("));\n'\
	'		var dmesg = document.getElementById("dmesg");\n'\
	'		var dev = dmesg.getElementsByClassName("thread");\n'\
	'		var cpu = -1;\n'\
	'		if(name.match("CPU_ON\[[0-9]*\]"))\n'\
	'			cpu = parseInt(name.slice(7));\n'\
	'		else if(name.match("CPU_OFF\[[0-9]*\]"))\n'\
	'			cpu = parseInt(name.slice(8));\n'\
	'		for (var i = 0; i < dev.length; i++) {\n'\
	'			dname = dev[i].title.slice(0, dev[i].title.indexOf(" ("));\n'\
	'			if((cpu >= 0 && dname.match("CPU_O[NF]*\\\[*"+cpu+"\\\]")) ||\n'\
	'				(name == dname))\n'\
	'			{\n'\
	'				dev[i].className = "thread hover";\n'\
	'			} else {\n'\
	'				dev[i].className = "thread";\n'\
	'			}\n'\
	'		}\n'\
	'	}\n'\
	'	function deviceUnhover() {\n'\
	'		var dmesg = document.getElementById("dmesg");\n'\
	'		var dev = dmesg.getElementsByClassName("thread");\n'\
	'		for (var i = 0; i < dev.length; i++) {\n'\
	'			dev[i].className = "thread";\n'\
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
	'		var name = title.slice(0, title.indexOf(" "));\n'\
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
	'		var name = this.title.slice(0, this.title.indexOf(" ("));\n'\
	'		var cpu = -1;\n'\
	'		if(name.match("CPU_ON\[[0-9]*\]"))\n'\
	'			cpu = parseInt(name.slice(7));\n'\
	'		else if(name.match("CPU_OFF\[[0-9]*\]"))\n'\
	'			cpu = parseInt(name.slice(8));\n'\
	'		var dmesg = document.getElementById("dmesg");\n'\
	'		var dev = dmesg.getElementsByClassName("thread");\n'\
	'		var idlist = [];\n'\
	'		var pdata = [[]];\n'\
	'		var pd = pdata[0];\n'\
	'		var total = [0.0, 0.0, 0.0];\n'\
	'		for (var i = 0; i < dev.length; i++) {\n'\
	'			dname = dev[i].title.slice(0, dev[i].title.indexOf(" ("));\n'\
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
	'					var pname = "<t3 style=\\"font-size:"+fs2+"px\\">"+phases[i].id.replace("_", " ")+"</t3>";\n'\
	'					phases[i].innerHTML = time+pname;\n'\
	'				} else {\n'\
	'					phases[i].style.width = "0%";\n'\
	'					phases[i].style.left = left+"%";\n'\
	'				}\n'\
	'			}\n'\
	'		}\n'\
	'		var cglist = document.getElementById("callgraphs");\n'\
	'		if(!cglist) return;\n'\
	'		var cg = cglist.getElementsByClassName("atop");\n'\
	'		for (var i = 0; i < cg.length; i++) {\n'\
	'			if(idlist.indexOf(cg[i].id) >= 0) {\n'\
	'				cg[i].style.display = "block";\n'\
	'			} else {\n'\
	'				cg[i].style.display = "none";\n'\
	'			}\n'\
	'		}\n'\
	'	}\n'\
	'	function devListWindow(e) {\n'\
	'		var sx = e.clientX;\n'\
	'		if(sx > window.innerWidth - 440)\n'\
	'			sx = window.innerWidth - 440;\n'\
	'		var cfg="top="+e.screenY+", left="+sx+", width=440, height=720, scrollbars=yes";\n'\
	'		var win = window.open("", "_blank", cfg);\n'\
	'		if(window.chrome) win.moveBy(sx, 0);\n'\
	'		var html = "<title>"+e.target.innerHTML+"</title>"+\n'\
	'			"<style type=\\"text/css\\">"+\n'\
	'			"   ul {list-style-type:circle;padding-left:10px;margin-left:10px;}"+\n'\
	'			"</style>"\n'\
	'		var dt = devtable[0];\n'\
	'		if(e.target.id != "devlist1")\n'\
	'			dt = devtable[1];\n'\
	'		win.document.write(html+dt);\n'\
	'	}\n'\
	'	window.addEventListener("load", function () {\n'\
	'		var dmesg = document.getElementById("dmesg");\n'\
	'		dmesg.style.width = "100%"\n'\
	'		document.getElementById("zoomin").onclick = zoomTimeline;\n'\
	'		document.getElementById("zoomout").onclick = zoomTimeline;\n'\
	'		document.getElementById("zoomdef").onclick = zoomTimeline;\n'\
	'		var devlist = document.getElementsByClassName("devlist");\n'\
	'		for (var i = 0; i < devlist.length; i++)\n'\
	'			devlist[i].onclick = devListWindow;\n'\
	'		var dev = dmesg.getElementsByClassName("thread");\n'\
	'		for (var i = 0; i < dev.length; i++) {\n'\
	'			dev[i].onclick = deviceDetail;\n'\
	'			dev[i].onmouseover = deviceHover;\n'\
	'			dev[i].onmouseout = deviceUnhover;\n'\
	'		}\n'\
	'		zoomTimeline();\n'\
	'	});\n'\
	'</script>\n'
	hf.write(script_code);




def executeSuspend():
	global sysvals
	detectUSB(False)
	t0 = time.time()*1000
	tp = sysvals.tpath
	
	for count in range(1,sysvals.execcount+1):
		
		os.system('dmesg -C')
		
		if(sysvals.usecallgraph and count == 2):
			
			os.system('echo function_graph > '+tp+'current_tracer')
			os.system('echo "" > '+tp+'set_ftrace_filter')
			
			os.system('echo funcgraph-abstime > '+tp+'trace_options')
			os.system('echo funcgraph-proc > '+tp+'trace_options')
			
			os.system('cat '+tp+'available_filter_functions | '+\
				'grep dpm_run_callback > '+tp+'set_graph_function')
		
		if(count > 1 and sysvals.x2delay > 0):
			tN = time.time()*1000
			while (tN - t0) < sysvals.x2delay:
				tN = time.time()*1000
				time.sleep(0.001)
		
		if(sysvals.usecallgraph or sysvals.usetraceevents):
			print('START TRACING')
			os.system('echo 1 > '+tp+'tracing_on')
		
		if(sysvals.usecallgraph or sysvals.usetraceevents):
			os.system('echo SUSPEND START > '+tp+'trace_marker')
		if(sysvals.rtcwake):
			print('SUSPEND START')
			print('will autoresume in %d seconds' % sysvals.rtcwaketime)
			sysvals.rtcWakeAlarm()
		else:
			print('SUSPEND START (press a key to resume)')
		pf = open(sysvals.powerfile, 'w')
		pf.write(sysvals.suspendmode)
		
		pf.close()
		t0 = time.time()*1000
		
		print('RESUME COMPLETE')
		if(sysvals.usecallgraph or sysvals.usetraceevents):
			os.system('echo RESUME COMPLETE > '+tp+'trace_marker')
		
		t = sysvals.postresumetime
		if(t > 0):
			print('Waiting %d seconds for POST-RESUME trace events...' % t)
			time.sleep(t)
		
		if(sysvals.usecallgraph or sysvals.usetraceevents):
			os.system('echo 0 > '+tp+'tracing_on')
			print('CAPTURING TRACE')
			writeDatafileHeader(sysvals.ftracefile)
			os.system('cat '+tp+'trace >> '+sysvals.ftracefile)
			os.system('echo "" > '+tp+'trace')
		
		print('CAPTURING DMESG')
		writeDatafileHeader(sysvals.dmesgfile)
		os.system('dmesg -c >> '+sysvals.dmesgfile)
def writeDatafileHeader(filename):
	global sysvals
	fw = getFPDT(False)
	prt = sysvals.postresumetime
	fp = open(filename, 'a')
	fp.write(sysvals.teststamp+'\n')
	if(fw):
		fp.write('
	if(prt > 0):
		fp.write('
	fp.close()





def executeAndroidSuspend():
	global sysvals
	
	tp = sysvals.tpath
	out = os.popen(sysvals.adb+\
		' shell dumpsys power | grep mScreenOn').read().strip()
	
	if(out.endswith('false')):
		print('Waking the device up for the test...')
		
		os.system(sysvals.adb+' shell input keyevent 26')
		
		time.sleep(3)
	
	for count in range(1,sysvals.execcount+1):
		
		os.system(sysvals.adb+' shell dmesg -c > /dev/null 2>&1')
		
		if(sysvals.usetraceevents):
			print('START TRACING')
			os.system(sysvals.adb+" shell 'echo 1 > "+tp+"tracing_on'")
		
		for count in range(1,sysvals.execcount+1):
			if(sysvals.usetraceevents):
				os.system(sysvals.adb+\
					" shell 'echo SUSPEND START > "+tp+"trace_marker'")
			print('SUSPEND START (press a key on the device to resume)')
			os.system(sysvals.adb+" shell 'echo "+sysvals.suspendmode+\
				" > "+sysvals.powerfile+"'")
			
			while(True):
				check = os.popen(sysvals.adb+\
					' shell pwd 2>/dev/null').read().strip()
				if(len(check) > 0):
					break
				time.sleep(1)
			if(sysvals.usetraceevents):
				os.system(sysvals.adb+" shell 'echo RESUME COMPLETE > "+tp+\
					"trace_marker'")
		
		print('RESUME COMPLETE')
		
		if(sysvals.usetraceevents):
			os.system(sysvals.adb+" shell 'echo 0 > "+tp+"tracing_on'")
			print('CAPTURING TRACE')
			os.system('echo "'+sysvals.teststamp+'" > '+sysvals.ftracefile)
			os.system(sysvals.adb+' shell cat '+tp+\
				'trace >> '+sysvals.ftracefile)
		
		print('CAPTURING DMESG')
		os.system('echo "'+sysvals.teststamp+'" > '+sysvals.dmesgfile)
		os.system(sysvals.adb+' shell dmesg >> '+sysvals.dmesgfile)






def setUSBDevicesAuto():
	global sysvals
	rootCheck()
	for dirname, dirnames, filenames in os.walk('/sys/devices'):
		if(re.match('.*/usb[0-9]*.*', dirname) and
			'idVendor' in filenames and 'idProduct' in filenames):
			os.system('echo auto > %s/power/control' % dirname)
			name = dirname.split('/')[-1]
			desc = os.popen('cat %s/product 2>/dev/null' % \
				dirname).read().replace('\n', '')
			ctrl = os.popen('cat %s/power/control 2>/dev/null' % \
				dirname).read().replace('\n', '')
			print('control is %s for %6s: %s' % (ctrl, name, desc))





def yesno(val):
	yesvals = ['auto', 'enabled', 'active', '1']
	novals = ['on', 'disabled', 'suspended', 'forbidden', 'unsupported']
	if val in yesvals:
		return 'Y'
	elif val in novals:
		return 'N'
	return ' '




"1901m16s"
def ms2nice(val):
	ms = 0
	try:
		ms = int(val)
	except:
		return 0.0
	m = ms / 60000
	s = (ms / 1000) - (m * 60)
	return '%3dm%2ds' % (m, s)






def detectUSB(output):
	global sysvals
	field = {'idVendor':'', 'idProduct':'', 'product':'', 'speed':''}
	power = {'async':'', 'autosuspend':'', 'autosuspend_delay_ms':'',
			 'control':'', 'persist':'', 'runtime_enabled':'',
			 'runtime_status':'', 'runtime_usage':'',
			'runtime_active_time':'',
			'runtime_suspended_time':'',
			'active_duration':'',
			'connected_duration':''}
	if(output):
		print('LEGEND')
		print('---------------------------------------------------------------------------------------------')
		print('  A = async/sync PM queue Y/N                       D = autosuspend delay (seconds)')
		print('  S = autosuspend Y/N                         rACTIVE = runtime active (min/sec)')
		print('  P = persist across suspend Y/N              rSUSPEN = runtime suspend (min/sec)')
		print('  E = runtime suspend enabled/forbidden Y/N    ACTIVE = active duration (min/sec)')
		print('  R = runtime status active/suspended Y/N     CONNECT = connected duration (min/sec)')
		print('  U = runtime usage count')
		print('---------------------------------------------------------------------------------------------')
		print('  NAME       ID      DESCRIPTION         SPEED A S P E R U D rACTIVE rSUSPEN  ACTIVE CONNECT')
		print('---------------------------------------------------------------------------------------------')
	for dirname, dirnames, filenames in os.walk('/sys/devices'):
		if(re.match('.*/usb[0-9]*.*', dirname) and
			'idVendor' in filenames and 'idProduct' in filenames):
			for i in field:
				field[i] = os.popen('cat %s/%s 2>/dev/null' % \
					(dirname, i)).read().replace('\n', '')
			name = dirname.split('/')[-1]
			if(len(field['product']) > 0):
				sysvals.altdevname[name] = \
					'%s [%s]' % (field['product'], name)
			else:
				sysvals.altdevname[name] = \
					'%s:%s [%s]' % (field['idVendor'], \
						field['idProduct'], name)
			if(output):
				for i in power:
					power[i] = os.popen('cat %s/power/%s 2>/dev/null' % \
						(dirname, i)).read().replace('\n', '')
				if(re.match('usb[0-9]*', name)):
					first = '%-8s' % name
				else:
					first = '%8s' % name
				print('%s [%s:%s] %-20s %-4s %1s %1s %1s %1s %1s %1s %1s %s %s %s %s' % \
					(first, field['idVendor'], field['idProduct'], \
					field['product'][0:20], field['speed'], \
					yesno(power['async']), \
					yesno(power['control']), \
					yesno(power['persist']), \
					yesno(power['runtime_enabled']), \
					yesno(power['runtime_status']), \
					power['runtime_usage'], \
					power['autosuspend'], \
					ms2nice(power['runtime_active_time']), \
					ms2nice(power['runtime_suspended_time']), \
					ms2nice(power['active_duration']), \
					ms2nice(power['connected_duration'])))





def getModes():
	global sysvals
	modes = ''
	if(not sysvals.android):
		if(os.path.exists(sysvals.powerfile)):
			fp = open(sysvals.powerfile, 'r')
			modes = string.split(fp.read())
			fp.close()
	else:
		line = os.popen(sysvals.adb+' shell cat '+\
			sysvals.powerfile).read().strip()
		modes = string.split(line)
	return modes





def getFPDT(output):
	global sysvals
	rectype = {}
	rectype[0] = 'Firmware Basic Boot Performance Record'
	rectype[1] = 'S3 Performance Table Record'
	prectype = {}
	prectype[0] = 'Basic S3 Resume Performance Record'
	prectype[1] = 'Basic S3 Suspend Performance Record'
	rootCheck()
	if(not os.path.exists(sysvals.fpdtpath)):
		if(output):
			doError('file doesnt exist: %s' % sysvals.fpdtpath, False)
		return False
	if(not os.access(sysvals.fpdtpath, os.R_OK)):
		if(output):
			doError('file isnt readable: %s' % sysvals.fpdtpath, False)
		return False
	if(not os.path.exists(sysvals.mempath)):
		if(output):
			doError('file doesnt exist: %s' % sysvals.mempath, False)
		return False
	if(not os.access(sysvals.mempath, os.R_OK)):
		if(output):
			doError('file isnt readable: %s' % sysvals.mempath, False)
		return False
	fp = open(sysvals.fpdtpath, 'rb')
	buf = fp.read()
	fp.close()
	if(len(buf) < 36):
		if(output):
			doError('Invalid FPDT table data, should '+\
				'be at least 36 bytes', False)
		return False
	table = struct.unpack('4sIBB6s8sI4sI', buf[0:36])
	if(output):
		print('')
		print('Firmware Performance Data Table (%s)' % table[0])
		print('                  Signature : %s' % table[0])
		print('               Table Length : %u' % table[1])
		print('                   Revision : %u' % table[2])
		print('                   Checksum : 0x%x' % table[3])
		print('                     OEM ID : %s' % table[4])
		print('               OEM Table ID : %s' % table[5])
		print('               OEM Revision : %u' % table[6])
		print('                 Creator ID : %s' % table[7])
		print('           Creator Revision : 0x%x' % table[8])
		print('')
	if(table[0] != 'FPDT'):
		if(output):
			doError('Invalid FPDT table')
		return False
	if(len(buf) <= 36):
		return False
	i = 0
	fwData = [0, 0]
	records = buf[36:]
	fp = open(sysvals.mempath, 'rb')
	while(i < len(records)):
		header = struct.unpack('HBB', records[i:i+4])
		if(header[0] not in rectype):
			continue
		if(header[1] != 16):
			continue
		addr = struct.unpack('Q', records[i+8:i+16])[0]
		try:
			fp.seek(addr)
			first = fp.read(8)
		except:
			doError('Bad address 0x%x in %s' % (addr, sysvals.mempath), False)
		rechead = struct.unpack('4sI', first)
		recdata = fp.read(rechead[1]-8)
		if(rechead[0] == 'FBPT'):
			record = struct.unpack('HBBIQQQQQ', recdata)
			if(output):
				print('%s (%s)' % (rectype[header[0]], rechead[0]))
				print('                  Reset END : %u ns' % record[4])
				print('  OS Loader LoadImage Start : %u ns' % record[5])
				print(' OS Loader StartImage Start : %u ns' % record[6])
				print('     ExitBootServices Entry : %u ns' % record[7])
				print('      ExitBootServices Exit : %u ns' % record[8])
		elif(rechead[0] == 'S3PT'):
			if(output):
				print('%s (%s)' % (rectype[header[0]], rechead[0]))
			j = 0
			while(j < len(recdata)):
				prechead = struct.unpack('HBB', recdata[j:j+4])
				if(prechead[0] not in prectype):
					continue
				if(prechead[0] == 0):
					record = struct.unpack('IIQQ', recdata[j:j+prechead[1]])
					fwData[1] = record[2]
					if(output):
						print('    %s' % prectype[prechead[0]])
						print('               Resume Count : %u' % \
							record[1])
						print('                 FullResume : %u ns' % \
							record[2])
						print('              AverageResume : %u ns' % \
							record[3])
				elif(prechead[0] == 1):
					record = struct.unpack('QQ', recdata[j+4:j+prechead[1]])
					fwData[0] = record[1] - record[0]
					if(output):
						print('    %s' % prectype[prechead[0]])
						print('               SuspendStart : %u ns' % \
							record[0])
						print('                 SuspendEnd : %u ns' % \
							record[1])
						print('                SuspendTime : %u ns' % \
							fwData[0])
				j += prechead[1]
		if(output):
			print('')
		i += header[1]
	fp.close()
	return fwData






def statusCheck():
	global sysvals
	status = True
	if(sysvals.android):
		print('Checking the android system ...')
	else:
		print('Checking this system (%s)...' % platform.node())
	
	if(sysvals.android):
		res = 'NO'
		out = os.popen(sysvals.adb+' get-state').read().strip()
		if(out == 'device'):
			res = 'YES'
		print('    is android device connected: %s' % res)
		if(res != 'YES'):
			print('    Please connect the device before using this tool')
			return False
	
	res = 'NO (No features of this tool will work!)'
	if(sysvals.android):
		out = os.popen(sysvals.adb+' shell id').read().strip()
		if('root' in out):
			res = 'YES'
	else:
		if(os.environ['USER'] == 'root'):
			res = 'YES'
	print('    have root access: %s' % res)
	if(res != 'YES'):
		if(sysvals.android):
			print('    Try running "adb root" to restart the daemon as root')
		else:
			print('    Try running this script with sudo')
		return False
	
	res = 'NO (No features of this tool will work!)'
	if(sysvals.android):
		out = os.popen(sysvals.adb+' shell ls '+\
			sysvals.powerfile).read().strip()
		if(out == sysvals.powerfile):
			res = 'YES'
	else:
		if(os.path.exists(sysvals.powerfile)):
			res = 'YES'
	print('    is sysfs mounted: %s' % res)
	if(res != 'YES'):
		return False
	
	res = 'NO'
	modes = getModes()
	if(sysvals.suspendmode in modes):
		res = 'YES'
	else:
		status = False
	print('    is "%s" a valid power mode: %s' % (sysvals.suspendmode, res))
	if(res == 'NO'):
		print('      valid power modes are: %s' % modes)
		print('      please choose one with -m')
	
	if(sysvals.android):
		res = 'YES'
		out1 = os.popen(sysvals.adb+\
			' shell dumpsys power | grep mScreenOn').read().strip()
		out2 = os.popen(sysvals.adb+\
			' shell input').read().strip()
		if(not out1.startswith('mScreenOn') or not out2.startswith('usage')):
			res = 'NO (wake the android device up before running the test)'
		print('    can I unlock the screen: %s' % res)
	
	res = 'NO'
	ftgood = verifyFtrace()
	if(ftgood):
		res = 'YES'
	elif(sysvals.usecallgraph):
		status = False
	print('    is ftrace supported: %s' % res)
	
	res = 'DMESG'
	if(ftgood):
		sysvals.usetraceeventsonly = True
		sysvals.usetraceevents = False
		for e in sysvals.traceevents:
			check = False
			if(sysvals.android):
				out = os.popen(sysvals.adb+' shell ls -d '+\
					sysvals.epath+e).read().strip()
				if(out == sysvals.epath+e):
					check = True
			else:
				if(os.path.exists(sysvals.epath+e)):
					check = True
			if(not check):
				sysvals.usetraceeventsonly = False
			if(e == 'suspend_resume' and check):
				sysvals.usetraceevents = True
		if(sysvals.usetraceevents and sysvals.usetraceeventsonly):
			res = 'FTRACE (all trace events found)'
		elif(sysvals.usetraceevents):
			res = 'DMESG and FTRACE (suspend_resume trace event found)'
	print('    timeline data source: %s' % res)
	
	res = 'NO'
	if(sysvals.rtcpath != ''):
		res = 'YES'
	elif(sysvals.rtcwake):
		status = False
	print('    is rtcwake supported: %s' % res)
	return status






def doError(msg, help):
	if(help == True):
		printHelp()
	print('ERROR: %s\n') % msg
	sys.exit()






def doWarning(msg, file):
	print('/* %s */') % msg
	if(file):
		print('/* For a fix, please send this'+\
			' %s file to <todd.e.brandt@intel.com> */' % file)



def rootCheck():
	if(os.environ['USER'] != 'root'):
		doError('This script must be run as root', False)



def getArgInt(name, args, min, max):
	try:
		arg = args.next()
	except:
		doError(name+': no argument supplied', True)
	try:
		val = int(arg)
	except:
		doError(name+': non-integer value given', True)
	if(val < min or val > max):
		doError(name+': value should be between %d and %d' % (min, max), True)
	return val



def rerunTest():
	global sysvals
	if(sysvals.ftracefile != ''):
		doesTraceLogHaveTraceEvents()
	if(sysvals.dmesgfile == '' and not sysvals.usetraceeventsonly):
		doError('recreating this html output '+\
			'requires a dmesg file', False)
	sysvals.setOutputFile()
	vprint('Output file: %s' % sysvals.htmlfile)
	print('PROCESSING DATA')
	if(sysvals.usetraceeventsonly):
		testruns = parseTraceLog()
	else:
		testruns = loadKernelLog()
		for data in testruns:
			parseKernelLog(data)
		if(sysvals.ftracefile != ''):
			appendIncompleteTraceLog(testruns)
	createHTML(testruns)



def runTest(subdir):
	global sysvals
	
	if(not sysvals.android):
		initFtrace()
	else:
		initFtraceAndroid()
	sysvals.initTestOutput(subdir)
	vprint('Output files:\n    %s' % sysvals.dmesgfile)
	if(sysvals.usecallgraph or
		sysvals.usetraceevents or
		sysvals.usetraceeventsonly):
		vprint('    %s' % sysvals.ftracefile)
	vprint('    %s' % sysvals.htmlfile)
	
	if(not sysvals.android):
		executeSuspend()
	else:
		executeAndroidSuspend()
	
	print('PROCESSING DATA')
	if(sysvals.usetraceeventsonly):
		
		testruns = parseTraceLog()
	else:
		
		testruns = loadKernelLog()
		for data in testruns:
			parseKernelLog(data)
		if(sysvals.usecallgraph or sysvals.usetraceevents):
			appendIncompleteTraceLog(testruns)
	createHTML(testruns)



def runSummary(subdir, output):
	global sysvals
	
	files = []
	for dirname, dirnames, filenames in os.walk(subdir):
		for filename in filenames:
			if(re.match('.*_ftrace.txt', filename)):
				files.append("%s/%s" % (dirname, filename))
	
	testruns = []
	for file in sorted(files):
		if output:
			print("Test found in %s" % os.path.dirname(file))
		sysvals.ftracefile = file
		sysvals.dmesgfile = file.replace('_ftrace.txt', '_dmesg.txt')
		doesTraceLogHaveTraceEvents()
		sysvals.usecallgraph = False
		if not sysvals.usetraceeventsonly:
			if(not os.path.exists(sysvals.dmesgfile)):
				print("Skipping %s: not a valid test input" % file)
				continue
			else:
				if output:
					f = os.path.basename(sysvals.ftracefile)
					d = os.path.basename(sysvals.dmesgfile)
					print("\tInput files: %s and %s" % (f, d))
				testdata = loadKernelLog()
				data = testdata[0]
				parseKernelLog(data)
				testdata = [data]
				appendIncompleteTraceLog(testdata)
		else:
			if output:
				print("\tInput file: %s" % os.path.basename(sysvals.ftracefile))
			testdata = parseTraceLog()
			data = testdata[0]
		data.normalizeTime(data.tSuspended)
		link = file.replace(subdir+'/', '').replace('_ftrace.txt', '.html')
		data.outfile = link
		testruns.append(data)
	createHTMLSummarySimple(testruns, subdir+'/summary.html')



def printHelp():
	global sysvals
	modes = getModes()
	print('')
	print('AnalyzeSuspend v%.1f' % sysvals.version)
	print('Usage: sudo analyze_suspend.py <options>')
	print('')
	print('Description:')
	print('  This tool is designed to assist kernel and OS developers in optimizing')
	print('  their linux stack\'s suspend/resume time. Using a kernel image built')
	print('  with a few extra options enabled, the tool will execute a suspend and')
	print('  capture dmesg and ftrace data until resume is complete. This data is')
	print('  transformed into a device timeline and an optional callgraph to give')
	print('  a detailed view of which devices/subsystems are taking the most')
	print('  time in suspend/resume.')
	print('')
	print('  Generates output files in subdirectory: suspend-mmddyy-HHMMSS')
	print('   HTML output:                    <hostname>_<mode>.html')
	print('   raw dmesg output:               <hostname>_<mode>_dmesg.txt')
	print('   raw ftrace output:              <hostname>_<mode>_ftrace.txt')
	print('')
	print('Options:')
	print('  [general]')
	print('    -h          Print this help text')
	print('    -v          Print the current tool version')
	print('    -verbose    Print extra information during execution and analysis')
	print('    -status     Test to see if the system is enabled to run this tool')
	print('    -modes      List available suspend modes')
	print('    -m mode     Mode to initiate for suspend %s (default: %s)') % (modes, sysvals.suspendmode)
	print('    -rtcwake t  Use rtcwake to autoresume after <t> seconds (default: disabled)')
	print('  [advanced]')
	print('    -f          Use ftrace to create device callgraphs (default: disabled)')
	print('    -filter "d1 d2 ..." Filter out all but this list of dev names')
	print('    -x2         Run two suspend/resumes back to back (default: disabled)')
	print('    -x2delay t  Minimum millisecond delay <t> between the two test runs (default: 0 ms)')
	print('    -postres t  Time after resume completion to wait for post-resume events (default: 0 S)')
	print('    -multi n d  Execute <n> consecutive tests at <d> seconds intervals. The outputs will')
	print('                be created in a new subdirectory with a summary page.')
	print('  [utilities]')
	print('    -fpdt       Print out the contents of the ACPI Firmware Performance Data Table')
	print('    -usbtopo    Print out the current USB topology with power info')
	print('    -usbauto    Enable autosuspend for all connected USB devices')
	print('  [android testing]')
	print('    -adb binary Use the given adb binary to run the test on an android device.')
	print('                The device should already be connected and with root access.')
	print('                Commands will be executed on the device using "adb shell"')
	print('  [re-analyze data from previous runs]')
	print('    -ftrace ftracefile  Create HTML output using ftrace input')
	print('    -dmesg dmesgfile    Create HTML output using dmesg (not needed for kernel >= 3.15)')
	print('    -summary directory  Create a summary of all test in this dir')
	print('')
	return True


if __name__ == '__main__':
	cmd = ''
	cmdarg = ''
	multitest = {'run': False, 'count': 0, 'delay': 0}
	
	args = iter(sys.argv[1:])
	for arg in args:
		if(arg == '-m'):
			try:
				val = args.next()
			except:
				doError('No mode supplied', True)
			sysvals.suspendmode = val
		elif(arg == '-adb'):
			try:
				val = args.next()
			except:
				doError('No adb binary supplied', True)
			if(not os.path.exists(val)):
				doError('file doesnt exist: %s' % val, False)
			if(not os.access(val, os.X_OK)):
				doError('file isnt executable: %s' % val, False)
			try:
				check = os.popen(val+' version').read().strip()
			except:
				doError('adb version failed to execute', False)
			if(not re.match('Android Debug Bridge .*', check)):
				doError('adb version failed to execute', False)
			sysvals.adb = val
			sysvals.android = True
		elif(arg == '-x2'):
			if(sysvals.postresumetime > 0):
				doError('-x2 is not compatible with -postres', False)
			sysvals.execcount = 2
		elif(arg == '-x2delay'):
			sysvals.x2delay = getArgInt('-x2delay', args, 0, 60000)
		elif(arg == '-postres'):
			if(sysvals.execcount != 1):
				doError('-x2 is not compatible with -postres', False)
			sysvals.postresumetime = getArgInt('-postres', args, 0, 3600)
		elif(arg == '-f'):
			sysvals.usecallgraph = True
		elif(arg == '-modes'):
			cmd = 'modes'
		elif(arg == '-fpdt'):
			cmd = 'fpdt'
		elif(arg == '-usbtopo'):
			cmd = 'usbtopo'
		elif(arg == '-usbauto'):
			cmd = 'usbauto'
		elif(arg == '-status'):
			cmd = 'status'
		elif(arg == '-verbose'):
			sysvals.verbose = True
		elif(arg == '-v'):
			print("Version %.1f" % sysvals.version)
			sys.exit()
		elif(arg == '-rtcwake'):
			sysvals.rtcwake = True
			sysvals.rtcwaketime = getArgInt('-rtcwake', args, 0, 3600)
		elif(arg == '-multi'):
			multitest['run'] = True
			multitest['count'] = getArgInt('-multi n (exec count)', args, 2, 1000000)
			multitest['delay'] = getArgInt('-multi d (delay between tests)', args, 0, 3600)
		elif(arg == '-dmesg'):
			try:
				val = args.next()
			except:
				doError('No dmesg file supplied', True)
			sysvals.notestrun = True
			sysvals.dmesgfile = val
			if(os.path.exists(sysvals.dmesgfile) == False):
				doError('%s doesnt exist' % sysvals.dmesgfile, False)
		elif(arg == '-ftrace'):
			try:
				val = args.next()
			except:
				doError('No ftrace file supplied', True)
			sysvals.notestrun = True
			sysvals.usecallgraph = True
			sysvals.ftracefile = val
			if(os.path.exists(sysvals.ftracefile) == False):
				doError('%s doesnt exist' % sysvals.ftracefile, False)
		elif(arg == '-summary'):
			try:
				val = args.next()
			except:
				doError('No directory supplied', True)
			cmd = 'summary'
			cmdarg = val
			sysvals.notestrun = True
			if(os.path.isdir(val) == False):
				doError('%s isnt accesible' % val, False)
		elif(arg == '-filter'):
			try:
				val = args.next()
			except:
				doError('No devnames supplied', True)
			sysvals.setDeviceFilter(val)
		elif(arg == '-h'):
			printHelp()
			sys.exit()
		else:
			doError('Invalid argument: '+arg, True)
	
	if(cmd != ''):
		if(cmd == 'status'):
			statusCheck()
		elif(cmd == 'fpdt'):
			if(sysvals.android):
				doError('cannot read FPDT on android device', False)
			getFPDT(True)
		elif(cmd == 'usbtopo'):
			if(sysvals.android):
				doError('cannot read USB topology '+\
					'on an android device', False)
			detectUSB(True)
		elif(cmd == 'modes'):
			modes = getModes()
			print modes
		elif(cmd == 'usbauto'):
			setUSBDevicesAuto()
		elif(cmd == 'summary'):
			print("Generating a summary of folder \"%s\"" % cmdarg)
			runSummary(cmdarg, True)
		sys.exit()
	
	if(sysvals.android):
		if(sysvals.usecallgraph):
			doError('ftrace (-f) is not yet supported '+\
				'in the android kernel', False)
		if(sysvals.notestrun):
			doError('cannot analyze test files on the '+\
				'android device', False)
	
	if(sysvals.notestrun):
		rerunTest()
		sys.exit()
	
	if(not statusCheck()):
		print('Check FAILED, aborting the test run!')
		sys.exit()
	if multitest['run']:
		
		s = 'x%d' % multitest['count']
		subdir = datetime.now().strftime('suspend-'+s+'-%m%d%y-%H%M%S')
		os.mkdir(subdir)
		for i in range(multitest['count']):
			if(i != 0):
				print('Waiting %d seconds...' % (multitest['delay']))
				time.sleep(multitest['delay'])
			print('TEST (%d/%d) START' % (i+1, multitest['count']))
			runTest(subdir)
			print('TEST (%d/%d) COMPLETE' % (i+1, multitest['count']))
		runSummary(subdir, False)
	else:
		
		runTest(".")
