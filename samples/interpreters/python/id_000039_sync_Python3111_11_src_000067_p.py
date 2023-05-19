









from sys import version_info
if version_info >= (2,6,0):
    def swig_import_helper():
        from os.path import dirname
        import imp
        fp = None
        try:
            fp, pathname, description = imp.find_module('_x64dbgapi', [dirname(__file__)])
        except ImportError:
            import _x64dbgapi
            return _x64dbgapi
        if fp is not None:
            try:
                _mod = imp.load_module('_x64dbgapi', fp, pathname, description)
            finally:
                fp.close()
            return _mod
    _x64dbgapi = swig_import_helper()
    del swig_import_helper
else:
    import _x64dbgapi
del version_info
try:
    _swig_property = property
except NameError:
    pass 
def _swig_setattr_nondynamic(self,class_type,name,value,static=1):
    if (name == "thisown"): return self.this.own(value)
    if (name == "this"):
        if type(value).__name__ == 'SwigPyObject':
            self.__dict__[name] = value
            return
    method = class_type.__swig_setmethods__.get(name,None)
    if method: return method(self,value)
    if (not static):
        self.__dict__[name] = value
    else:
        raise AttributeError("You cannot add attributes to %s" % self)

def _swig_setattr(self,class_type,name,value):
    return _swig_setattr_nondynamic(self,class_type,name,value,0)

def _swig_getattr(self,class_type,name):
    if (name == "thisown"): return self.this.own()
    method = class_type.__swig_getmethods__.get(name,None)
    if method: return method(self)
    raise AttributeError(name)

def _swig_repr(self):
    try: strthis = "proxy of " + self.this.__repr__()
    except: strthis = ""
    return "<%s.%s; %s >" % (self.__class__.__module__, self.__class__.__name__, strthis,)

try:
    _object = object
    _newclass = 1
except AttributeError:
    class _object : pass
    _newclass = 0


def _swig_setattr_nondynamic_method(set):
    def set_attr(self,name,value):
        if (name == "thisown"): return self.this.own(value)
        if hasattr(self,name) or (name == "this"):
            set(self,name,value)
        else:
            raise AttributeError("You cannot add attributes to %s" % self)
    return set_attr



def cdata(*args):
  """cdata(void * ptr, size_t nelements=1) -> SWIGCDATA"""
  return _x64dbgapi.cdata(*args)

def memmove(*args):
  """memmove(void * data, void const * indata)"""
  return _x64dbgapi.memmove(*args)
class ListInfo(object):
    """Proxy of C++ ListInfo class"""
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    count = _swig_property(_x64dbgapi.ListInfo_count_get, _x64dbgapi.ListInfo_count_set)
    size = _swig_property(_x64dbgapi.ListInfo_size_get, _x64dbgapi.ListInfo_size_set)
    data = _swig_property(_x64dbgapi.ListInfo_data_get, _x64dbgapi.ListInfo_data_set)
    def __init__(self): 
        """__init__(ListInfo self) -> ListInfo"""
        this = _x64dbgapi.new_ListInfo()
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _x64dbgapi.delete_ListInfo
    __del__ = lambda self : None;
ListInfo_swigregister = _x64dbgapi.ListInfo_swigregister
ListInfo_swigregister(ListInfo)

MAX_SETTING_SIZE = _x64dbgapi.MAX_SETTING_SIZE
DBG_VERSION = _x64dbgapi.DBG_VERSION

def BridgeInit():
  """BridgeInit() -> wchar_t const *"""
  return _x64dbgapi.BridgeInit()

def BridgeStart():
  """BridgeStart() -> wchar_t const *"""
  return _x64dbgapi.BridgeStart()

def BridgeAlloc(*args):
  """BridgeAlloc(size_t size) -> void *"""
  return _x64dbgapi.BridgeAlloc(*args)

def BridgeFree(*args):
  """BridgeFree(void * ptr)"""
  return _x64dbgapi.BridgeFree(*args)

def BridgeSettingGet(*args):
  """BridgeSettingGet(char const * section, char const * key, char * value) -> bool"""
  return _x64dbgapi.BridgeSettingGet(*args)

def BridgeSettingGetUint(*args):
  """BridgeSettingGetUint(char const * section, char const * key, duint * value) -> bool"""
  return _x64dbgapi.BridgeSettingGetUint(*args)

def BridgeSettingSet(*args):
  """BridgeSettingSet(char const * section, char const * key, char const * value) -> bool"""
  return _x64dbgapi.BridgeSettingSet(*args)

def BridgeSettingSetUint(*args):
  """BridgeSettingSetUint(char const * section, char const * key, duint value) -> bool"""
  return _x64dbgapi.BridgeSettingSetUint(*args)

def BridgeSettingFlush():
  """BridgeSettingFlush() -> bool"""
  return _x64dbgapi.BridgeSettingFlush()

def BridgeSettingRead(*args):
  """BridgeSettingRead(int * errorLine) -> bool"""
  return _x64dbgapi.BridgeSettingRead(*args)

def BridgeGetDbgVersion():
  """BridgeGetDbgVersion() -> int"""
  return _x64dbgapi.BridgeGetDbgVersion()
MAX_LABEL_SIZE = _x64dbgapi.MAX_LABEL_SIZE
MAX_COMMENT_SIZE = _x64dbgapi.MAX_COMMENT_SIZE
MAX_MODULE_SIZE = _x64dbgapi.MAX_MODULE_SIZE
MAX_IMPORT_SIZE = _x64dbgapi.MAX_IMPORT_SIZE
MAX_BREAKPOINT_SIZE = _x64dbgapi.MAX_BREAKPOINT_SIZE
MAX_CONDITIONAL_EXPR_SIZE = _x64dbgapi.MAX_CONDITIONAL_EXPR_SIZE
MAX_CONDITIONAL_TEXT_SIZE = _x64dbgapi.MAX_CONDITIONAL_TEXT_SIZE
MAX_SCRIPT_LINE_SIZE = _x64dbgapi.MAX_SCRIPT_LINE_SIZE
MAX_THREAD_NAME_SIZE = _x64dbgapi.MAX_THREAD_NAME_SIZE
MAX_WATCH_NAME_SIZE = _x64dbgapi.MAX_WATCH_NAME_SIZE
MAX_STRING_SIZE = _x64dbgapi.MAX_STRING_SIZE
MAX_ERROR_SIZE = _x64dbgapi.MAX_ERROR_SIZE
MAX_SECTION_SIZE = _x64dbgapi.MAX_SECTION_SIZE
MAX_COMMAND_LINE_SIZE = _x64dbgapi.MAX_COMMAND_LINE_SIZE
MAX_MNEMONIC_SIZE = _x64dbgapi.MAX_MNEMONIC_SIZE
PAGE_SIZE = _x64dbgapi.PAGE_SIZE
initialized = _x64dbgapi.initialized
paused = _x64dbgapi.paused
running = _x64dbgapi.running
stopped = _x64dbgapi.stopped
SEG_DEFAULT = _x64dbgapi.SEG_DEFAULT
SEG_ES = _x64dbgapi.SEG_ES
SEG_DS = _x64dbgapi.SEG_DS
SEG_FS = _x64dbgapi.SEG_FS
SEG_GS = _x64dbgapi.SEG_GS
SEG_CS = _x64dbgapi.SEG_CS
SEG_SS = _x64dbgapi.SEG_SS
flagmodule = _x64dbgapi.flagmodule
flaglabel = _x64dbgapi.flaglabel
flagcomment = _x64dbgapi.flagcomment
flagbookmark = _x64dbgapi.flagbookmark
flagfunction = _x64dbgapi.flagfunction
flagloop = _x64dbgapi.flagloop
flagargs = _x64dbgapi.flagargs
flagNoFuncOffset = _x64dbgapi.flagNoFuncOffset
bp_none = _x64dbgapi.bp_none
bp_normal = _x64dbgapi.bp_normal
bp_hardware = _x64dbgapi.bp_hardware
bp_memory = _x64dbgapi.bp_memory
bp_dll = _x64dbgapi.bp_dll
bp_exception = _x64dbgapi.bp_exception
FUNC_NONE = _x64dbgapi.FUNC_NONE
FUNC_BEGIN = _x64dbgapi.FUNC_BEGIN
FUNC_MIDDLE = _x64dbgapi.FUNC_MIDDLE
FUNC_END = _x64dbgapi.FUNC_END
FUNC_SINGLE = _x64dbgapi.FUNC_SINGLE
LOOP_NONE = _x64dbgapi.LOOP_NONE
LOOP_BEGIN = _x64dbgapi.LOOP_BEGIN
LOOP_MIDDLE = _x64dbgapi.LOOP_MIDDLE
LOOP_ENTRY = _x64dbgapi.LOOP_ENTRY
LOOP_END = _x64dbgapi.LOOP_END
LOOP_SINGLE = _x64dbgapi.LOOP_SINGLE
XREF_NONE = _x64dbgapi.XREF_NONE
XREF_DATA = _x64dbgapi.XREF_DATA
XREF_JMP = _x64dbgapi.XREF_JMP
XREF_CALL = _x64dbgapi.XREF_CALL
ARG_NONE = _x64dbgapi.ARG_NONE
ARG_BEGIN = _x64dbgapi.ARG_BEGIN
ARG_MIDDLE = _x64dbgapi.ARG_MIDDLE
ARG_END = _x64dbgapi.ARG_END
ARG_SINGLE = _x64dbgapi.ARG_SINGLE
DBG_SCRIPT_LOAD = _x64dbgapi.DBG_SCRIPT_LOAD
DBG_SCRIPT_UNLOAD = _x64dbgapi.DBG_SCRIPT_UNLOAD
DBG_SCRIPT_RUN = _x64dbgapi.DBG_SCRIPT_RUN
DBG_SCRIPT_STEP = _x64dbgapi.DBG_SCRIPT_STEP
DBG_SCRIPT_BPTOGGLE = _x64dbgapi.DBG_SCRIPT_BPTOGGLE
DBG_SCRIPT_BPGET = _x64dbgapi.DBG_SCRIPT_BPGET
DBG_SCRIPT_CMDEXEC = _x64dbgapi.DBG_SCRIPT_CMDEXEC
DBG_SCRIPT_ABORT = _x64dbgapi.DBG_SCRIPT_ABORT
DBG_SCRIPT_GETLINETYPE = _x64dbgapi.DBG_SCRIPT_GETLINETYPE
DBG_SCRIPT_SETIP = _x64dbgapi.DBG_SCRIPT_SETIP
DBG_SCRIPT_GETBRANCHINFO = _x64dbgapi.DBG_SCRIPT_GETBRANCHINFO
DBG_SYMBOL_ENUM = _x64dbgapi.DBG_SYMBOL_ENUM
DBG_ASSEMBLE_AT = _x64dbgapi.DBG_ASSEMBLE_AT
DBG_MODBASE_FROM_NAME = _x64dbgapi.DBG_MODBASE_FROM_NAME
DBG_DISASM_AT = _x64dbgapi.DBG_DISASM_AT
DBG_STACK_COMMENT_GET = _x64dbgapi.DBG_STACK_COMMENT_GET
DBG_GET_THREAD_LIST = _x64dbgapi.DBG_GET_THREAD_LIST
DBG_SETTINGS_UPDATED = _x64dbgapi.DBG_SETTINGS_UPDATED
DBG_DISASM_FAST_AT = _x64dbgapi.DBG_DISASM_FAST_AT
DBG_MENU_ENTRY_CLICKED = _x64dbgapi.DBG_MENU_ENTRY_CLICKED
DBG_FUNCTION_GET = _x64dbgapi.DBG_FUNCTION_GET
DBG_FUNCTION_OVERLAPS = _x64dbgapi.DBG_FUNCTION_OVERLAPS
DBG_FUNCTION_ADD = _x64dbgapi.DBG_FUNCTION_ADD
DBG_FUNCTION_DEL = _x64dbgapi.DBG_FUNCTION_DEL
DBG_LOOP_GET = _x64dbgapi.DBG_LOOP_GET
DBG_LOOP_OVERLAPS = _x64dbgapi.DBG_LOOP_OVERLAPS
DBG_LOOP_ADD = _x64dbgapi.DBG_LOOP_ADD
DBG_LOOP_DEL = _x64dbgapi.DBG_LOOP_DEL
DBG_IS_RUN_LOCKED = _x64dbgapi.DBG_IS_RUN_LOCKED
DBG_IS_BP_DISABLED = _x64dbgapi.DBG_IS_BP_DISABLED
DBG_SET_AUTO_COMMENT_AT = _x64dbgapi.DBG_SET_AUTO_COMMENT_AT
DBG_DELETE_AUTO_COMMENT_RANGE = _x64dbgapi.DBG_DELETE_AUTO_COMMENT_RANGE
DBG_SET_AUTO_LABEL_AT = _x64dbgapi.DBG_SET_AUTO_LABEL_AT
DBG_DELETE_AUTO_LABEL_RANGE = _x64dbgapi.DBG_DELETE_AUTO_LABEL_RANGE
DBG_SET_AUTO_BOOKMARK_AT = _x64dbgapi.DBG_SET_AUTO_BOOKMARK_AT
DBG_DELETE_AUTO_BOOKMARK_RANGE = _x64dbgapi.DBG_DELETE_AUTO_BOOKMARK_RANGE
DBG_SET_AUTO_FUNCTION_AT = _x64dbgapi.DBG_SET_AUTO_FUNCTION_AT
DBG_DELETE_AUTO_FUNCTION_RANGE = _x64dbgapi.DBG_DELETE_AUTO_FUNCTION_RANGE
DBG_GET_STRING_AT = _x64dbgapi.DBG_GET_STRING_AT
DBG_GET_FUNCTIONS = _x64dbgapi.DBG_GET_FUNCTIONS
DBG_WIN_EVENT = _x64dbgapi.DBG_WIN_EVENT
DBG_WIN_EVENT_GLOBAL = _x64dbgapi.DBG_WIN_EVENT_GLOBAL
DBG_INITIALIZE_LOCKS = _x64dbgapi.DBG_INITIALIZE_LOCKS
DBG_DEINITIALIZE_LOCKS = _x64dbgapi.DBG_DEINITIALIZE_LOCKS
DBG_GET_TIME_WASTED_COUNTER = _x64dbgapi.DBG_GET_TIME_WASTED_COUNTER
DBG_SYMBOL_ENUM_FROMCACHE = _x64dbgapi.DBG_SYMBOL_ENUM_FROMCACHE
DBG_DELETE_COMMENT_RANGE = _x64dbgapi.DBG_DELETE_COMMENT_RANGE
DBG_DELETE_LABEL_RANGE = _x64dbgapi.DBG_DELETE_LABEL_RANGE
DBG_DELETE_BOOKMARK_RANGE = _x64dbgapi.DBG_DELETE_BOOKMARK_RANGE
DBG_GET_XREF_COUNT_AT = _x64dbgapi.DBG_GET_XREF_COUNT_AT
DBG_GET_XREF_TYPE_AT = _x64dbgapi.DBG_GET_XREF_TYPE_AT
DBG_XREF_ADD = _x64dbgapi.DBG_XREF_ADD
DBG_XREF_DEL_ALL = _x64dbgapi.DBG_XREF_DEL_ALL
DBG_XREF_GET = _x64dbgapi.DBG_XREF_GET
DBG_GET_ENCODE_TYPE_BUFFER = _x64dbgapi.DBG_GET_ENCODE_TYPE_BUFFER
DBG_ENCODE_TYPE_GET = _x64dbgapi.DBG_ENCODE_TYPE_GET
DBG_DELETE_ENCODE_TYPE_RANGE = _x64dbgapi.DBG_DELETE_ENCODE_TYPE_RANGE
DBG_ENCODE_SIZE_GET = _x64dbgapi.DBG_ENCODE_SIZE_GET
DBG_DELETE_ENCODE_TYPE_SEG = _x64dbgapi.DBG_DELETE_ENCODE_TYPE_SEG
DBG_RELEASE_ENCODE_TYPE_BUFFER = _x64dbgapi.DBG_RELEASE_ENCODE_TYPE_BUFFER
DBG_ARGUMENT_GET = _x64dbgapi.DBG_ARGUMENT_GET
DBG_ARGUMENT_OVERLAPS = _x64dbgapi.DBG_ARGUMENT_OVERLAPS
DBG_ARGUMENT_ADD = _x64dbgapi.DBG_ARGUMENT_ADD
DBG_ARGUMENT_DEL = _x64dbgapi.DBG_ARGUMENT_DEL
DBG_GET_WATCH_LIST = _x64dbgapi.DBG_GET_WATCH_LIST
DBG_SELCHANGED = _x64dbgapi.DBG_SELCHANGED
DBG_GET_PROCESS_HANDLE = _x64dbgapi.DBG_GET_PROCESS_HANDLE
DBG_GET_THREAD_HANDLE = _x64dbgapi.DBG_GET_THREAD_HANDLE
DBG_GET_PROCESS_ID = _x64dbgapi.DBG_GET_PROCESS_ID
DBG_GET_THREAD_ID = _x64dbgapi.DBG_GET_THREAD_ID
DBG_GET_PEB_ADDRESS = _x64dbgapi.DBG_GET_PEB_ADDRESS
DBG_GET_TEB_ADDRESS = _x64dbgapi.DBG_GET_TEB_ADDRESS
DBG_ANALYZE_FUNCTION = _x64dbgapi.DBG_ANALYZE_FUNCTION
DBG_MENU_PREPARE = _x64dbgapi.DBG_MENU_PREPARE
DBG_GET_SYMBOL_INFO = _x64dbgapi.DBG_GET_SYMBOL_INFO
linecommand = _x64dbgapi.linecommand
linebranch = _x64dbgapi.linebranch
linelabel = _x64dbgapi.linelabel
linecomment = _x64dbgapi.linecomment
lineempty = _x64dbgapi.lineempty
scriptnobranch = _x64dbgapi.scriptnobranch
scriptjmp = _x64dbgapi.scriptjmp
scriptjnejnz = _x64dbgapi.scriptjnejnz
scriptjejz = _x64dbgapi.scriptjejz
scriptjbjl = _x64dbgapi.scriptjbjl
scriptjajg = _x64dbgapi.scriptjajg
scriptjbejle = _x64dbgapi.scriptjbejle
scriptjaejge = _x64dbgapi.scriptjaejge
scriptcall = _x64dbgapi.scriptcall
instr_normal = _x64dbgapi.instr_normal
instr_branch = _x64dbgapi.instr_branch
instr_stack = _x64dbgapi.instr_stack
arg_normal = _x64dbgapi.arg_normal
arg_memory = _x64dbgapi.arg_memory
str_none = _x64dbgapi.str_none
str_ascii = _x64dbgapi.str_ascii
str_unicode = _x64dbgapi.str_unicode
_PriorityIdle = _x64dbgapi._PriorityIdle
_PriorityAboveNormal = _x64dbgapi._PriorityAboveNormal
_PriorityBelowNormal = _x64dbgapi._PriorityBelowNormal
_PriorityHighest = _x64dbgapi._PriorityHighest
_PriorityLowest = _x64dbgapi._PriorityLowest
_PriorityNormal = _x64dbgapi._PriorityNormal
_PriorityTimeCritical = _x64dbgapi._PriorityTimeCritical
_PriorityUnknown = _x64dbgapi._PriorityUnknown
_Executive = _x64dbgapi._Executive
_FreePage = _x64dbgapi._FreePage
_PageIn = _x64dbgapi._PageIn
_PoolAllocation = _x64dbgapi._PoolAllocation
_DelayExecution = _x64dbgapi._DelayExecution
_Suspended = _x64dbgapi._Suspended
_UserRequest = _x64dbgapi._UserRequest
_WrExecutive = _x64dbgapi._WrExecutive
_WrFreePage = _x64dbgapi._WrFreePage
_WrPageIn = _x64dbgapi._WrPageIn
_WrPoolAllocation = _x64dbgapi._WrPoolAllocation
_WrDelayExecution = _x64dbgapi._WrDelayExecution
_WrSuspended = _x64dbgapi._WrSuspended
_WrUserRequest = _x64dbgapi._WrUserRequest
_WrEventPair = _x64dbgapi._WrEventPair
_WrQueue = _x64dbgapi._WrQueue
_WrLpcReceive = _x64dbgapi._WrLpcReceive
_WrLpcReply = _x64dbgapi._WrLpcReply
_WrVirtualMemory = _x64dbgapi._WrVirtualMemory
_WrPageOut = _x64dbgapi._WrPageOut
_WrRendezvous = _x64dbgapi._WrRendezvous
_Spare2 = _x64dbgapi._Spare2
_Spare3 = _x64dbgapi._Spare3
_Spare4 = _x64dbgapi._Spare4
_Spare5 = _x64dbgapi._Spare5
_WrCalloutStack = _x64dbgapi._WrCalloutStack
_WrKernel = _x64dbgapi._WrKernel
_WrResource = _x64dbgapi._WrResource
_WrPushLock = _x64dbgapi._WrPushLock
_WrMutex = _x64dbgapi._WrMutex
_WrQuantumEnd = _x64dbgapi._WrQuantumEnd
_WrDispatchInt = _x64dbgapi._WrDispatchInt
_WrPreempted = _x64dbgapi._WrPreempted
_WrYieldExecution = _x64dbgapi._WrYieldExecution
_WrFastMutex = _x64dbgapi._WrFastMutex
_WrGuardedMutex = _x64dbgapi._WrGuardedMutex
_WrRundown = _x64dbgapi._WrRundown
size_byte = _x64dbgapi.size_byte
size_word = _x64dbgapi.size_word
size_dword = _x64dbgapi.size_dword
size_qword = _x64dbgapi.size_qword
enc_unknown = _x64dbgapi.enc_unknown
enc_byte = _x64dbgapi.enc_byte
enc_word = _x64dbgapi.enc_word
enc_dword = _x64dbgapi.enc_dword
enc_fword = _x64dbgapi.enc_fword
enc_qword = _x64dbgapi.enc_qword
enc_tbyte = _x64dbgapi.enc_tbyte
enc_oword = _x64dbgapi.enc_oword
enc_mmword = _x64dbgapi.enc_mmword
enc_xmmword = _x64dbgapi.enc_xmmword
enc_ymmword = _x64dbgapi.enc_ymmword
enc_zmmword = _x64dbgapi.enc_zmmword
enc_real4 = _x64dbgapi.enc_real4
enc_real8 = _x64dbgapi.enc_real8
enc_real10 = _x64dbgapi.enc_real10
enc_ascii = _x64dbgapi.enc_ascii
enc_unicode = _x64dbgapi.enc_unicode
enc_code = _x64dbgapi.enc_code
enc_junk = _x64dbgapi.enc_junk
enc_middle = _x64dbgapi.enc_middle
TYPE_UINT = _x64dbgapi.TYPE_UINT
TYPE_INT = _x64dbgapi.TYPE_INT
TYPE_FLOAT = _x64dbgapi.TYPE_FLOAT
TYPE_ASCII = _x64dbgapi.TYPE_ASCII
TYPE_UNICODE = _x64dbgapi.TYPE_UNICODE
TYPE_INVALID = _x64dbgapi.TYPE_INVALID
MODE_DISABLED = _x64dbgapi.MODE_DISABLED
MODE_ISTRUE = _x64dbgapi.MODE_ISTRUE
MODE_ISFALSE = _x64dbgapi.MODE_ISFALSE
MODE_CHANGED = _x64dbgapi.MODE_CHANGED
MODE_UNCHANGED = _x64dbgapi.MODE_UNCHANGED
hw_access = _x64dbgapi.hw_access
hw_write = _x64dbgapi.hw_write
hw_execute = _x64dbgapi.hw_execute
mem_access = _x64dbgapi.mem_access
mem_read = _x64dbgapi.mem_read
mem_write = _x64dbgapi.mem_write
mem_execute = _x64dbgapi.mem_execute
dll_load = _x64dbgapi.dll_load
dll_unload = _x64dbgapi.dll_unload
dll_all = _x64dbgapi.dll_all
ex_firstchance = _x64dbgapi.ex_firstchance
ex_secondchance = _x64dbgapi.ex_secondchance
ex_all = _x64dbgapi.ex_all
hw_byte = _x64dbgapi.hw_byte
hw_word = _x64dbgapi.hw_word
hw_dword = _x64dbgapi.hw_dword
hw_qword = _x64dbgapi.hw_qword
sym_import = _x64dbgapi.sym_import
sym_export = _x64dbgapi.sym_export
sym_symbol = _x64dbgapi.sym_symbol
class MEMORY_BASIC_INFORMATION(object):
    """Proxy of C++ _MEMORY_BASIC_INFORMATION class"""
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    BaseAddress = _swig_property(_x64dbgapi.MEMORY_BASIC_INFORMATION_BaseAddress_get, _x64dbgapi.MEMORY_BASIC_INFORMATION_BaseAddress_set)
    AllocationBase = _swig_property(_x64dbgapi.MEMORY_BASIC_INFORMATION_AllocationBase_get, _x64dbgapi.MEMORY_BASIC_INFORMATION_AllocationBase_set)
    AllocationProtect = _swig_property(_x64dbgapi.MEMORY_BASIC_INFORMATION_AllocationProtect_get, _x64dbgapi.MEMORY_BASIC_INFORMATION_AllocationProtect_set)
    RegionSize = _swig_property(_x64dbgapi.MEMORY_BASIC_INFORMATION_RegionSize_get, _x64dbgapi.MEMORY_BASIC_INFORMATION_RegionSize_set)
    State = _swig_property(_x64dbgapi.MEMORY_BASIC_INFORMATION_State_get, _x64dbgapi.MEMORY_BASIC_INFORMATION_State_set)
    Protect = _swig_property(_x64dbgapi.MEMORY_BASIC_INFORMATION_Protect_get, _x64dbgapi.MEMORY_BASIC_INFORMATION_Protect_set)
    Type = _swig_property(_x64dbgapi.MEMORY_BASIC_INFORMATION_Type_get, _x64dbgapi.MEMORY_BASIC_INFORMATION_Type_set)
    def __init__(self): 
        """__init__(_MEMORY_BASIC_INFORMATION self) -> MEMORY_BASIC_INFORMATION"""
        this = _x64dbgapi.new_MEMORY_BASIC_INFORMATION()
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _x64dbgapi.delete_MEMORY_BASIC_INFORMATION
    __del__ = lambda self : None;
MEMORY_BASIC_INFORMATION_swigregister = _x64dbgapi.MEMORY_BASIC_INFORMATION_swigregister
MEMORY_BASIC_INFORMATION_swigregister(MEMORY_BASIC_INFORMATION)

class MEMPAGE(object):
    """Proxy of C++ MEMPAGE class"""
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    mbi = _swig_property(_x64dbgapi.MEMPAGE_mbi_get, _x64dbgapi.MEMPAGE_mbi_set)
    info = _swig_property(_x64dbgapi.MEMPAGE_info_get, _x64dbgapi.MEMPAGE_info_set)
    def __init__(self): 
        """__init__(MEMPAGE self) -> MEMPAGE"""
        this = _x64dbgapi.new_MEMPAGE()
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _x64dbgapi.delete_MEMPAGE
    __del__ = lambda self : None;
MEMPAGE_swigregister = _x64dbgapi.MEMPAGE_swigregister
MEMPAGE_swigregister(MEMPAGE)

class MEMMAP(object):
    """Proxy of C++ MEMMAP class"""
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    count = _swig_property(_x64dbgapi.MEMMAP_count_get, _x64dbgapi.MEMMAP_count_set)
    page = _swig_property(_x64dbgapi.MEMMAP_page_get, _x64dbgapi.MEMMAP_page_set)
    def __init__(self): 
        """__init__(MEMMAP self) -> MEMMAP"""
        this = _x64dbgapi.new_MEMMAP()
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _x64dbgapi.delete_MEMMAP
    __del__ = lambda self : None;
MEMMAP_swigregister = _x64dbgapi.MEMMAP_swigregister
MEMMAP_swigregister(MEMMAP)

class BRIDGEBP(object):
    """Proxy of C++ BRIDGEBP class"""
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    type = _swig_property(_x64dbgapi.BRIDGEBP_type_get, _x64dbgapi.BRIDGEBP_type_set)
    addr = _swig_property(_x64dbgapi.BRIDGEBP_addr_get, _x64dbgapi.BRIDGEBP_addr_set)
    enabled = _swig_property(_x64dbgapi.BRIDGEBP_enabled_get, _x64dbgapi.BRIDGEBP_enabled_set)
    singleshoot = _swig_property(_x64dbgapi.BRIDGEBP_singleshoot_get, _x64dbgapi.BRIDGEBP_singleshoot_set)
    active = _swig_property(_x64dbgapi.BRIDGEBP_active_get, _x64dbgapi.BRIDGEBP_active_set)
    name = _swig_property(_x64dbgapi.BRIDGEBP_name_get, _x64dbgapi.BRIDGEBP_name_set)
    mod = _swig_property(_x64dbgapi.BRIDGEBP_mod_get, _x64dbgapi.BRIDGEBP_mod_set)
    slot = _swig_property(_x64dbgapi.BRIDGEBP_slot_get, _x64dbgapi.BRIDGEBP_slot_set)
    typeEx = _swig_property(_x64dbgapi.BRIDGEBP_typeEx_get, _x64dbgapi.BRIDGEBP_typeEx_set)
    hwSize = _swig_property(_x64dbgapi.BRIDGEBP_hwSize_get, _x64dbgapi.BRIDGEBP_hwSize_set)
    hitCount = _swig_property(_x64dbgapi.BRIDGEBP_hitCount_get, _x64dbgapi.BRIDGEBP_hitCount_set)
    fastResume = _swig_property(_x64dbgapi.BRIDGEBP_fastResume_get, _x64dbgapi.BRIDGEBP_fastResume_set)
    silent = _swig_property(_x64dbgapi.BRIDGEBP_silent_get, _x64dbgapi.BRIDGEBP_silent_set)
    breakCondition = _swig_property(_x64dbgapi.BRIDGEBP_breakCondition_get, _x64dbgapi.BRIDGEBP_breakCondition_set)
    logText = _swig_property(_x64dbgapi.BRIDGEBP_logText_get, _x64dbgapi.BRIDGEBP_logText_set)
    logCondition = _swig_property(_x64dbgapi.BRIDGEBP_logCondition_get, _x64dbgapi.BRIDGEBP_logCondition_set)
    commandText = _swig_property(_x64dbgapi.BRIDGEBP_commandText_get, _x64dbgapi.BRIDGEBP_commandText_set)
    commandCondition = _swig_property(_x64dbgapi.BRIDGEBP_commandCondition_get, _x64dbgapi.BRIDGEBP_commandCondition_set)
    def __init__(self): 
        """__init__(BRIDGEBP self) -> BRIDGEBP"""
        this = _x64dbgapi.new_BRIDGEBP()
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _x64dbgapi.delete_BRIDGEBP
    __del__ = lambda self : None;
BRIDGEBP_swigregister = _x64dbgapi.BRIDGEBP_swigregister
BRIDGEBP_swigregister(BRIDGEBP)

class BPMAP(object):
    """Proxy of C++ BPMAP class"""
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    count = _swig_property(_x64dbgapi.BPMAP_count_get, _x64dbgapi.BPMAP_count_set)
    bp = _swig_property(_x64dbgapi.BPMAP_bp_get, _x64dbgapi.BPMAP_bp_set)
    def __init__(self): 
        """__init__(BPMAP self) -> BPMAP"""
        this = _x64dbgapi.new_BPMAP()
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _x64dbgapi.delete_BPMAP
    __del__ = lambda self : None;
BPMAP_swigregister = _x64dbgapi.BPMAP_swigregister
BPMAP_swigregister(BPMAP)

class WATCHINFO(object):
    """Proxy of C++ WATCHINFO class"""
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    WatchName = _swig_property(_x64dbgapi.WATCHINFO_WatchName_get, _x64dbgapi.WATCHINFO_WatchName_set)
    Expression = _swig_property(_x64dbgapi.WATCHINFO_Expression_get, _x64dbgapi.WATCHINFO_Expression_set)
    window = _swig_property(_x64dbgapi.WATCHINFO_window_get, _x64dbgapi.WATCHINFO_window_set)
    id = _swig_property(_x64dbgapi.WATCHINFO_id_get, _x64dbgapi.WATCHINFO_id_set)
    varType = _swig_property(_x64dbgapi.WATCHINFO_varType_get, _x64dbgapi.WATCHINFO_varType_set)
    watchdogMode = _swig_property(_x64dbgapi.WATCHINFO_watchdogMode_get, _x64dbgapi.WATCHINFO_watchdogMode_set)
    value = _swig_property(_x64dbgapi.WATCHINFO_value_get, _x64dbgapi.WATCHINFO_value_set)
    watchdogTriggered = _swig_property(_x64dbgapi.WATCHINFO_watchdogTriggered_get, _x64dbgapi.WATCHINFO_watchdogTriggered_set)
    def __init__(self): 
        """__init__(WATCHINFO self) -> WATCHINFO"""
        this = _x64dbgapi.new_WATCHINFO()
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _x64dbgapi.delete_WATCHINFO
    __del__ = lambda self : None;
WATCHINFO_swigregister = _x64dbgapi.WATCHINFO_swigregister
WATCHINFO_swigregister(WATCHINFO)

class FUNCTION(object):
    """Proxy of C++ FUNCTION class"""
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    start = _swig_property(_x64dbgapi.FUNCTION_start_get, _x64dbgapi.FUNCTION_start_set)
    end = _swig_property(_x64dbgapi.FUNCTION_end_get, _x64dbgapi.FUNCTION_end_set)
    instrcount = _swig_property(_x64dbgapi.FUNCTION_instrcount_get, _x64dbgapi.FUNCTION_instrcount_set)
    def __init__(self): 
        """__init__(FUNCTION self) -> FUNCTION"""
        this = _x64dbgapi.new_FUNCTION()
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _x64dbgapi.delete_FUNCTION
    __del__ = lambda self : None;
FUNCTION_swigregister = _x64dbgapi.FUNCTION_swigregister
FUNCTION_swigregister(FUNCTION)

class LOOP(object):
    """Proxy of C++ LOOP class"""
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    depth = _swig_property(_x64dbgapi.LOOP_depth_get, _x64dbgapi.LOOP_depth_set)
    start = _swig_property(_x64dbgapi.LOOP_start_get, _x64dbgapi.LOOP_start_set)
    end = _swig_property(_x64dbgapi.LOOP_end_get, _x64dbgapi.LOOP_end_set)
    instrcount = _swig_property(_x64dbgapi.LOOP_instrcount_get, _x64dbgapi.LOOP_instrcount_set)
    def __init__(self): 
        """__init__(LOOP self) -> LOOP"""
        this = _x64dbgapi.new_LOOP()
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _x64dbgapi.delete_LOOP
    __del__ = lambda self : None;
LOOP_swigregister = _x64dbgapi.LOOP_swigregister
LOOP_swigregister(LOOP)

class BRIDGE_ADDRINFO(object):
    """Proxy of C++ BRIDGE_ADDRINFO class"""
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    flags = _swig_property(_x64dbgapi.BRIDGE_ADDRINFO_flags_get, _x64dbgapi.BRIDGE_ADDRINFO_flags_set)
    module = _swig_property(_x64dbgapi.BRIDGE_ADDRINFO_module_get, _x64dbgapi.BRIDGE_ADDRINFO_module_set)
    label = _swig_property(_x64dbgapi.BRIDGE_ADDRINFO_label_get, _x64dbgapi.BRIDGE_ADDRINFO_label_set)
    comment = _swig_property(_x64dbgapi.BRIDGE_ADDRINFO_comment_get, _x64dbgapi.BRIDGE_ADDRINFO_comment_set)
    isbookmark = _swig_property(_x64dbgapi.BRIDGE_ADDRINFO_isbookmark_get, _x64dbgapi.BRIDGE_ADDRINFO_isbookmark_set)
    function = _swig_property(_x64dbgapi.BRIDGE_ADDRINFO_function_get, _x64dbgapi.BRIDGE_ADDRINFO_function_set)
    loop = _swig_property(_x64dbgapi.BRIDGE_ADDRINFO_loop_get, _x64dbgapi.BRIDGE_ADDRINFO_loop_set)
    args = _swig_property(_x64dbgapi.BRIDGE_ADDRINFO_args_get, _x64dbgapi.BRIDGE_ADDRINFO_args_set)
    def __init__(self): 
        """__init__(BRIDGE_ADDRINFO self) -> BRIDGE_ADDRINFO"""
        this = _x64dbgapi.new_BRIDGE_ADDRINFO()
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _x64dbgapi.delete_BRIDGE_ADDRINFO
    __del__ = lambda self : None;
BRIDGE_ADDRINFO_swigregister = _x64dbgapi.BRIDGE_ADDRINFO_swigregister
BRIDGE_ADDRINFO_swigregister(BRIDGE_ADDRINFO)

class SYMBOLINFO(object):
    """Proxy of C++ SYMBOLINFO_ class"""
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    addr = _swig_property(_x64dbgapi.SYMBOLINFO_addr_get, _x64dbgapi.SYMBOLINFO_addr_set)
    decoratedSymbol = _swig_property(_x64dbgapi.SYMBOLINFO_decoratedSymbol_get, _x64dbgapi.SYMBOLINFO_decoratedSymbol_set)
    undecoratedSymbol = _swig_property(_x64dbgapi.SYMBOLINFO_undecoratedSymbol_get, _x64dbgapi.SYMBOLINFO_undecoratedSymbol_set)
    type = _swig_property(_x64dbgapi.SYMBOLINFO_type_get, _x64dbgapi.SYMBOLINFO_type_set)
    freeDecorated = _swig_property(_x64dbgapi.SYMBOLINFO_freeDecorated_get, _x64dbgapi.SYMBOLINFO_freeDecorated_set)
    freeUndecorated = _swig_property(_x64dbgapi.SYMBOLINFO_freeUndecorated_get, _x64dbgapi.SYMBOLINFO_freeUndecorated_set)
    def __init__(self): 
        """__init__(SYMBOLINFO_ self) -> SYMBOLINFO"""
        this = _x64dbgapi.new_SYMBOLINFO()
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _x64dbgapi.delete_SYMBOLINFO
    __del__ = lambda self : None;
SYMBOLINFO_swigregister = _x64dbgapi.SYMBOLINFO_swigregister
SYMBOLINFO_swigregister(SYMBOLINFO)

class SYMBOLMODULEINFO(object):
    """Proxy of C++ SYMBOLMODULEINFO class"""
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    base = _swig_property(_x64dbgapi.SYMBOLMODULEINFO_base_get, _x64dbgapi.SYMBOLMODULEINFO_base_set)
    name = _swig_property(_x64dbgapi.SYMBOLMODULEINFO_name_get, _x64dbgapi.SYMBOLMODULEINFO_name_set)
    def __init__(self): 
        """__init__(SYMBOLMODULEINFO self) -> SYMBOLMODULEINFO"""
        this = _x64dbgapi.new_SYMBOLMODULEINFO()
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _x64dbgapi.delete_SYMBOLMODULEINFO
    __del__ = lambda self : None;
SYMBOLMODULEINFO_swigregister = _x64dbgapi.SYMBOLMODULEINFO_swigregister
SYMBOLMODULEINFO_swigregister(SYMBOLMODULEINFO)

class SYMBOLCBINFO(object):
    """Proxy of C++ SYMBOLCBINFO class"""
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    base = _swig_property(_x64dbgapi.SYMBOLCBINFO_base_get, _x64dbgapi.SYMBOLCBINFO_base_set)
    cbSymbolEnum = _swig_property(_x64dbgapi.SYMBOLCBINFO_cbSymbolEnum_get, _x64dbgapi.SYMBOLCBINFO_cbSymbolEnum_set)
    user = _swig_property(_x64dbgapi.SYMBOLCBINFO_user_get, _x64dbgapi.SYMBOLCBINFO_user_set)
    def __init__(self): 
        """__init__(SYMBOLCBINFO self) -> SYMBOLCBINFO"""
        this = _x64dbgapi.new_SYMBOLCBINFO()
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _x64dbgapi.delete_SYMBOLCBINFO
    __del__ = lambda self : None;
SYMBOLCBINFO_swigregister = _x64dbgapi.SYMBOLCBINFO_swigregister
SYMBOLCBINFO_swigregister(SYMBOLCBINFO)

class FLAGS(object):
    """Proxy of C++ FLAGS class"""
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    c = _swig_property(_x64dbgapi.FLAGS_c_get, _x64dbgapi.FLAGS_c_set)
    p = _swig_property(_x64dbgapi.FLAGS_p_get, _x64dbgapi.FLAGS_p_set)
    a = _swig_property(_x64dbgapi.FLAGS_a_get, _x64dbgapi.FLAGS_a_set)
    z = _swig_property(_x64dbgapi.FLAGS_z_get, _x64dbgapi.FLAGS_z_set)
    s = _swig_property(_x64dbgapi.FLAGS_s_get, _x64dbgapi.FLAGS_s_set)
    t = _swig_property(_x64dbgapi.FLAGS_t_get, _x64dbgapi.FLAGS_t_set)
    i = _swig_property(_x64dbgapi.FLAGS_i_get, _x64dbgapi.FLAGS_i_set)
    d = _swig_property(_x64dbgapi.FLAGS_d_get, _x64dbgapi.FLAGS_d_set)
    o = _swig_property(_x64dbgapi.FLAGS_o_get, _x64dbgapi.FLAGS_o_set)
    def __init__(self): 
        """__init__(FLAGS self) -> FLAGS"""
        this = _x64dbgapi.new_FLAGS()
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _x64dbgapi.delete_FLAGS
    __del__ = lambda self : None;
FLAGS_swigregister = _x64dbgapi.FLAGS_swigregister
FLAGS_swigregister(FLAGS)

class MXCSRFIELDS(object):
    """Proxy of C++ MXCSRFIELDS class"""
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    FZ = _swig_property(_x64dbgapi.MXCSRFIELDS_FZ_get, _x64dbgapi.MXCSRFIELDS_FZ_set)
    PM = _swig_property(_x64dbgapi.MXCSRFIELDS_PM_get, _x64dbgapi.MXCSRFIELDS_PM_set)
    UM = _swig_property(_x64dbgapi.MXCSRFIELDS_UM_get, _x64dbgapi.MXCSRFIELDS_UM_set)
    OM = _swig_property(_x64dbgapi.MXCSRFIELDS_OM_get, _x64dbgapi.MXCSRFIELDS_OM_set)
    ZM = _swig_property(_x64dbgapi.MXCSRFIELDS_ZM_get, _x64dbgapi.MXCSRFIELDS_ZM_set)
    IM = _swig_property(_x64dbgapi.MXCSRFIELDS_IM_get, _x64dbgapi.MXCSRFIELDS_IM_set)
    DM = _swig_property(_x64dbgapi.MXCSRFIELDS_DM_get, _x64dbgapi.MXCSRFIELDS_DM_set)
    DAZ = _swig_property(_x64dbgapi.MXCSRFIELDS_DAZ_get, _x64dbgapi.MXCSRFIELDS_DAZ_set)
    PE = _swig_property(_x64dbgapi.MXCSRFIELDS_PE_get, _x64dbgapi.MXCSRFIELDS_PE_set)
    UE = _swig_property(_x64dbgapi.MXCSRFIELDS_UE_get, _x64dbgapi.MXCSRFIELDS_UE_set)
    OE = _swig_property(_x64dbgapi.MXCSRFIELDS_OE_get, _x64dbgapi.MXCSRFIELDS_OE_set)
    ZE = _swig_property(_x64dbgapi.MXCSRFIELDS_ZE_get, _x64dbgapi.MXCSRFIELDS_ZE_set)
    DE = _swig_property(_x64dbgapi.MXCSRFIELDS_DE_get, _x64dbgapi.MXCSRFIELDS_DE_set)
    IE = _swig_property(_x64dbgapi.MXCSRFIELDS_IE_get, _x64dbgapi.MXCSRFIELDS_IE_set)
    RC = _swig_property(_x64dbgapi.MXCSRFIELDS_RC_get, _x64dbgapi.MXCSRFIELDS_RC_set)
    def __init__(self): 
        """__init__(MXCSRFIELDS self) -> MXCSRFIELDS"""
        this = _x64dbgapi.new_MXCSRFIELDS()
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _x64dbgapi.delete_MXCSRFIELDS
    __del__ = lambda self : None;
MXCSRFIELDS_swigregister = _x64dbgapi.MXCSRFIELDS_swigregister
MXCSRFIELDS_swigregister(MXCSRFIELDS)

class X87STATUSWORDFIELDS(object):
    """Proxy of C++ X87STATUSWORDFIELDS class"""
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    B = _swig_property(_x64dbgapi.X87STATUSWORDFIELDS_B_get, _x64dbgapi.X87STATUSWORDFIELDS_B_set)
    C3 = _swig_property(_x64dbgapi.X87STATUSWORDFIELDS_C3_get, _x64dbgapi.X87STATUSWORDFIELDS_C3_set)
    C2 = _swig_property(_x64dbgapi.X87STATUSWORDFIELDS_C2_get, _x64dbgapi.X87STATUSWORDFIELDS_C2_set)
    C1 = _swig_property(_x64dbgapi.X87STATUSWORDFIELDS_C1_get, _x64dbgapi.X87STATUSWORDFIELDS_C1_set)
    C0 = _swig_property(_x64dbgapi.X87STATUSWORDFIELDS_C0_get, _x64dbgapi.X87STATUSWORDFIELDS_C0_set)
    ES = _swig_property(_x64dbgapi.X87STATUSWORDFIELDS_ES_get, _x64dbgapi.X87STATUSWORDFIELDS_ES_set)
    SF = _swig_property(_x64dbgapi.X87STATUSWORDFIELDS_SF_get, _x64dbgapi.X87STATUSWORDFIELDS_SF_set)
    P = _swig_property(_x64dbgapi.X87STATUSWORDFIELDS_P_get, _x64dbgapi.X87STATUSWORDFIELDS_P_set)
    U = _swig_property(_x64dbgapi.X87STATUSWORDFIELDS_U_get, _x64dbgapi.X87STATUSWORDFIELDS_U_set)
    O = _swig_property(_x64dbgapi.X87STATUSWORDFIELDS_O_get, _x64dbgapi.X87STATUSWORDFIELDS_O_set)
    Z = _swig_property(_x64dbgapi.X87STATUSWORDFIELDS_Z_get, _x64dbgapi.X87STATUSWORDFIELDS_Z_set)
    D = _swig_property(_x64dbgapi.X87STATUSWORDFIELDS_D_get, _x64dbgapi.X87STATUSWORDFIELDS_D_set)
    I = _swig_property(_x64dbgapi.X87STATUSWORDFIELDS_I_get, _x64dbgapi.X87STATUSWORDFIELDS_I_set)
    TOP = _swig_property(_x64dbgapi.X87STATUSWORDFIELDS_TOP_get, _x64dbgapi.X87STATUSWORDFIELDS_TOP_set)
    def __init__(self): 
        """__init__(X87STATUSWORDFIELDS self) -> X87STATUSWORDFIELDS"""
        this = _x64dbgapi.new_X87STATUSWORDFIELDS()
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _x64dbgapi.delete_X87STATUSWORDFIELDS
    __del__ = lambda self : None;
X87STATUSWORDFIELDS_swigregister = _x64dbgapi.X87STATUSWORDFIELDS_swigregister
X87STATUSWORDFIELDS_swigregister(X87STATUSWORDFIELDS)

class X87CONTROLWORDFIELDS(object):
    """Proxy of C++ X87CONTROLWORDFIELDS class"""
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    IC = _swig_property(_x64dbgapi.X87CONTROLWORDFIELDS_IC_get, _x64dbgapi.X87CONTROLWORDFIELDS_IC_set)
    IEM = _swig_property(_x64dbgapi.X87CONTROLWORDFIELDS_IEM_get, _x64dbgapi.X87CONTROLWORDFIELDS_IEM_set)
    PM = _swig_property(_x64dbgapi.X87CONTROLWORDFIELDS_PM_get, _x64dbgapi.X87CONTROLWORDFIELDS_PM_set)
    UM = _swig_property(_x64dbgapi.X87CONTROLWORDFIELDS_UM_get, _x64dbgapi.X87CONTROLWORDFIELDS_UM_set)
    OM = _swig_property(_x64dbgapi.X87CONTROLWORDFIELDS_OM_get, _x64dbgapi.X87CONTROLWORDFIELDS_OM_set)
    ZM = _swig_property(_x64dbgapi.X87CONTROLWORDFIELDS_ZM_get, _x64dbgapi.X87CONTROLWORDFIELDS_ZM_set)
    DM = _swig_property(_x64dbgapi.X87CONTROLWORDFIELDS_DM_get, _x64dbgapi.X87CONTROLWORDFIELDS_DM_set)
    IM = _swig_property(_x64dbgapi.X87CONTROLWORDFIELDS_IM_get, _x64dbgapi.X87CONTROLWORDFIELDS_IM_set)
    RC = _swig_property(_x64dbgapi.X87CONTROLWORDFIELDS_RC_get, _x64dbgapi.X87CONTROLWORDFIELDS_RC_set)
    PC = _swig_property(_x64dbgapi.X87CONTROLWORDFIELDS_PC_get, _x64dbgapi.X87CONTROLWORDFIELDS_PC_set)
    def __init__(self): 
        """__init__(X87CONTROLWORDFIELDS self) -> X87CONTROLWORDFIELDS"""
        this = _x64dbgapi.new_X87CONTROLWORDFIELDS()
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _x64dbgapi.delete_X87CONTROLWORDFIELDS
    __del__ = lambda self : None;
X87CONTROLWORDFIELDS_swigregister = _x64dbgapi.X87CONTROLWORDFIELDS_swigregister
X87CONTROLWORDFIELDS_swigregister(X87CONTROLWORDFIELDS)

class XMMREGISTER(object):
    """Proxy of C++ _XMMREGISTER class"""
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    Low = _swig_property(_x64dbgapi.XMMREGISTER_Low_get, _x64dbgapi.XMMREGISTER_Low_set)
    High = _swig_property(_x64dbgapi.XMMREGISTER_High_get, _x64dbgapi.XMMREGISTER_High_set)
    def __init__(self): 
        """__init__(_XMMREGISTER self) -> XMMREGISTER"""
        this = _x64dbgapi.new_XMMREGISTER()
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _x64dbgapi.delete_XMMREGISTER
    __del__ = lambda self : None;
XMMREGISTER_swigregister = _x64dbgapi.XMMREGISTER_swigregister
XMMREGISTER_swigregister(XMMREGISTER)

class YMMREGISTER(object):
    """Proxy of C++ YMMREGISTER class"""
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    Low = _swig_property(_x64dbgapi.YMMREGISTER_Low_get, _x64dbgapi.YMMREGISTER_Low_set)
    High = _swig_property(_x64dbgapi.YMMREGISTER_High_get, _x64dbgapi.YMMREGISTER_High_set)
    def __init__(self): 
        """__init__(YMMREGISTER self) -> YMMREGISTER"""
        this = _x64dbgapi.new_YMMREGISTER()
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _x64dbgapi.delete_YMMREGISTER
    __del__ = lambda self : None;
YMMREGISTER_swigregister = _x64dbgapi.YMMREGISTER_swigregister
YMMREGISTER_swigregister(YMMREGISTER)

class X87FPUREGISTER(object):
    """Proxy of C++ X87FPUREGISTER class"""
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    data = _swig_property(_x64dbgapi.X87FPUREGISTER_data_get, _x64dbgapi.X87FPUREGISTER_data_set)
    st_value = _swig_property(_x64dbgapi.X87FPUREGISTER_st_value_get, _x64dbgapi.X87FPUREGISTER_st_value_set)
    tag = _swig_property(_x64dbgapi.X87FPUREGISTER_tag_get, _x64dbgapi.X87FPUREGISTER_tag_set)
    def __init__(self): 
        """__init__(X87FPUREGISTER self) -> X87FPUREGISTER"""
        this = _x64dbgapi.new_X87FPUREGISTER()
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _x64dbgapi.delete_X87FPUREGISTER
    __del__ = lambda self : None;
X87FPUREGISTER_swigregister = _x64dbgapi.X87FPUREGISTER_swigregister
X87FPUREGISTER_swigregister(X87FPUREGISTER)

class X87FPU(object):
    """Proxy of C++ X87FPU class"""
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    ControlWord = _swig_property(_x64dbgapi.X87FPU_ControlWord_get, _x64dbgapi.X87FPU_ControlWord_set)
    StatusWord = _swig_property(_x64dbgapi.X87FPU_StatusWord_get, _x64dbgapi.X87FPU_StatusWord_set)
    TagWord = _swig_property(_x64dbgapi.X87FPU_TagWord_get, _x64dbgapi.X87FPU_TagWord_set)
    ErrorOffset = _swig_property(_x64dbgapi.X87FPU_ErrorOffset_get, _x64dbgapi.X87FPU_ErrorOffset_set)
    ErrorSelector = _swig_property(_x64dbgapi.X87FPU_ErrorSelector_get, _x64dbgapi.X87FPU_ErrorSelector_set)
    DataOffset = _swig_property(_x64dbgapi.X87FPU_DataOffset_get, _x64dbgapi.X87FPU_DataOffset_set)
    DataSelector = _swig_property(_x64dbgapi.X87FPU_DataSelector_get, _x64dbgapi.X87FPU_DataSelector_set)
    Cr0NpxState = _swig_property(_x64dbgapi.X87FPU_Cr0NpxState_get, _x64dbgapi.X87FPU_Cr0NpxState_set)
    def __init__(self): 
        """__init__(X87FPU self) -> X87FPU"""
        this = _x64dbgapi.new_X87FPU()
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _x64dbgapi.delete_X87FPU
    __del__ = lambda self : None;
X87FPU_swigregister = _x64dbgapi.X87FPU_swigregister
X87FPU_swigregister(X87FPU)

class REGISTERCONTEXT(object):
    """Proxy of C++ REGISTERCONTEXT class"""
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    cax = _swig_property(_x64dbgapi.REGISTERCONTEXT_cax_get, _x64dbgapi.REGISTERCONTEXT_cax_set)
    ccx = _swig_property(_x64dbgapi.REGISTERCONTEXT_ccx_get, _x64dbgapi.REGISTERCONTEXT_ccx_set)
    cdx = _swig_property(_x64dbgapi.REGISTERCONTEXT_cdx_get, _x64dbgapi.REGISTERCONTEXT_cdx_set)
    cbx = _swig_property(_x64dbgapi.REGISTERCONTEXT_cbx_get, _x64dbgapi.REGISTERCONTEXT_cbx_set)
    csp = _swig_property(_x64dbgapi.REGISTERCONTEXT_csp_get, _x64dbgapi.REGISTERCONTEXT_csp_set)
    cbp = _swig_property(_x64dbgapi.REGISTERCONTEXT_cbp_get, _x64dbgapi.REGISTERCONTEXT_cbp_set)
    csi = _swig_property(_x64dbgapi.REGISTERCONTEXT_csi_get, _x64dbgapi.REGISTERCONTEXT_csi_set)
    cdi = _swig_property(_x64dbgapi.REGISTERCONTEXT_cdi_get, _x64dbgapi.REGISTERCONTEXT_cdi_set)
    cip = _swig_property(_x64dbgapi.REGISTERCONTEXT_cip_get, _x64dbgapi.REGISTERCONTEXT_cip_set)
    eflags = _swig_property(_x64dbgapi.REGISTERCONTEXT_eflags_get, _x64dbgapi.REGISTERCONTEXT_eflags_set)
    gs = _swig_property(_x64dbgapi.REGISTERCONTEXT_gs_get, _x64dbgapi.REGISTERCONTEXT_gs_set)
    fs = _swig_property(_x64dbgapi.REGISTERCONTEXT_fs_get, _x64dbgapi.REGISTERCONTEXT_fs_set)
    es = _swig_property(_x64dbgapi.REGISTERCONTEXT_es_get, _x64dbgapi.REGISTERCONTEXT_es_set)
    ds = _swig_property(_x64dbgapi.REGISTERCONTEXT_ds_get, _x64dbgapi.REGISTERCONTEXT_ds_set)
    cs = _swig_property(_x64dbgapi.REGISTERCONTEXT_cs_get, _x64dbgapi.REGISTERCONTEXT_cs_set)
    ss = _swig_property(_x64dbgapi.REGISTERCONTEXT_ss_get, _x64dbgapi.REGISTERCONTEXT_ss_set)
    dr0 = _swig_property(_x64dbgapi.REGISTERCONTEXT_dr0_get, _x64dbgapi.REGISTERCONTEXT_dr0_set)
    dr1 = _swig_property(_x64dbgapi.REGISTERCONTEXT_dr1_get, _x64dbgapi.REGISTERCONTEXT_dr1_set)
    dr2 = _swig_property(_x64dbgapi.REGISTERCONTEXT_dr2_get, _x64dbgapi.REGISTERCONTEXT_dr2_set)
    dr3 = _swig_property(_x64dbgapi.REGISTERCONTEXT_dr3_get, _x64dbgapi.REGISTERCONTEXT_dr3_set)
    dr6 = _swig_property(_x64dbgapi.REGISTERCONTEXT_dr6_get, _x64dbgapi.REGISTERCONTEXT_dr6_set)
    dr7 = _swig_property(_x64dbgapi.REGISTERCONTEXT_dr7_get, _x64dbgapi.REGISTERCONTEXT_dr7_set)
    RegisterArea = _swig_property(_x64dbgapi.REGISTERCONTEXT_RegisterArea_get, _x64dbgapi.REGISTERCONTEXT_RegisterArea_set)
    x87fpu = _swig_property(_x64dbgapi.REGISTERCONTEXT_x87fpu_get, _x64dbgapi.REGISTERCONTEXT_x87fpu_set)
    MxCsr = _swig_property(_x64dbgapi.REGISTERCONTEXT_MxCsr_get, _x64dbgapi.REGISTERCONTEXT_MxCsr_set)
    XmmRegisters = _swig_property(_x64dbgapi.REGISTERCONTEXT_XmmRegisters_get, _x64dbgapi.REGISTERCONTEXT_XmmRegisters_set)
    YmmRegisters = _swig_property(_x64dbgapi.REGISTERCONTEXT_YmmRegisters_get, _x64dbgapi.REGISTERCONTEXT_YmmRegisters_set)
    def __init__(self): 
        """__init__(REGISTERCONTEXT self) -> REGISTERCONTEXT"""
        this = _x64dbgapi.new_REGISTERCONTEXT()
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _x64dbgapi.delete_REGISTERCONTEXT
    __del__ = lambda self : None;
REGISTERCONTEXT_swigregister = _x64dbgapi.REGISTERCONTEXT_swigregister
REGISTERCONTEXT_swigregister(REGISTERCONTEXT)

class LASTERROR(object):
    """Proxy of C++ LASTERROR class"""
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    code = _swig_property(_x64dbgapi.LASTERROR_code_get, _x64dbgapi.LASTERROR_code_set)
    name = _swig_property(_x64dbgapi.LASTERROR_name_get, _x64dbgapi.LASTERROR_name_set)
    def __init__(self): 
        """__init__(LASTERROR self) -> LASTERROR"""
        this = _x64dbgapi.new_LASTERROR()
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _x64dbgapi.delete_LASTERROR
    __del__ = lambda self : None;
LASTERROR_swigregister = _x64dbgapi.LASTERROR_swigregister
LASTERROR_swigregister(LASTERROR)

class LASTSTATUS(object):
    """Proxy of C++ LASTSTATUS class"""
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    code = _swig_property(_x64dbgapi.LASTSTATUS_code_get, _x64dbgapi.LASTSTATUS_code_set)
    name = _swig_property(_x64dbgapi.LASTSTATUS_name_get, _x64dbgapi.LASTSTATUS_name_set)
    def __init__(self): 
        """__init__(LASTSTATUS self) -> LASTSTATUS"""
        this = _x64dbgapi.new_LASTSTATUS()
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _x64dbgapi.delete_LASTSTATUS
    __del__ = lambda self : None;
LASTSTATUS_swigregister = _x64dbgapi.LASTSTATUS_swigregister
LASTSTATUS_swigregister(LASTSTATUS)

class REGDUMP(object):
    """Proxy of C++ REGDUMP class"""
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    regcontext = _swig_property(_x64dbgapi.REGDUMP_regcontext_get, _x64dbgapi.REGDUMP_regcontext_set)
    flags = _swig_property(_x64dbgapi.REGDUMP_flags_get, _x64dbgapi.REGDUMP_flags_set)
    x87FPURegisters = _swig_property(_x64dbgapi.REGDUMP_x87FPURegisters_get, _x64dbgapi.REGDUMP_x87FPURegisters_set)
    mmx = _swig_property(_x64dbgapi.REGDUMP_mmx_get, _x64dbgapi.REGDUMP_mmx_set)
    MxCsrFields = _swig_property(_x64dbgapi.REGDUMP_MxCsrFields_get, _x64dbgapi.REGDUMP_MxCsrFields_set)
    x87StatusWordFields = _swig_property(_x64dbgapi.REGDUMP_x87StatusWordFields_get, _x64dbgapi.REGDUMP_x87StatusWordFields_set)
    x87ControlWordFields = _swig_property(_x64dbgapi.REGDUMP_x87ControlWordFields_get, _x64dbgapi.REGDUMP_x87ControlWordFields_set)
    lastError = _swig_property(_x64dbgapi.REGDUMP_lastError_get, _x64dbgapi.REGDUMP_lastError_set)
    lastStatus = _swig_property(_x64dbgapi.REGDUMP_lastStatus_get, _x64dbgapi.REGDUMP_lastStatus_set)
    def __init__(self): 
        """__init__(REGDUMP self) -> REGDUMP"""
        this = _x64dbgapi.new_REGDUMP()
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _x64dbgapi.delete_REGDUMP
    __del__ = lambda self : None;
REGDUMP_swigregister = _x64dbgapi.REGDUMP_swigregister
REGDUMP_swigregister(REGDUMP)

class DISASM_ARG(object):
    """Proxy of C++ DISASM_ARG class"""
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    type = _swig_property(_x64dbgapi.DISASM_ARG_type_get, _x64dbgapi.DISASM_ARG_type_set)
    segment = _swig_property(_x64dbgapi.DISASM_ARG_segment_get, _x64dbgapi.DISASM_ARG_segment_set)
    mnemonic = _swig_property(_x64dbgapi.DISASM_ARG_mnemonic_get, _x64dbgapi.DISASM_ARG_mnemonic_set)
    constant = _swig_property(_x64dbgapi.DISASM_ARG_constant_get, _x64dbgapi.DISASM_ARG_constant_set)
    value = _swig_property(_x64dbgapi.DISASM_ARG_value_get, _x64dbgapi.DISASM_ARG_value_set)
    memvalue = _swig_property(_x64dbgapi.DISASM_ARG_memvalue_get, _x64dbgapi.DISASM_ARG_memvalue_set)
    def __init__(self): 
        """__init__(DISASM_ARG self) -> DISASM_ARG"""
        this = _x64dbgapi.new_DISASM_ARG()
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _x64dbgapi.delete_DISASM_ARG
    __del__ = lambda self : None;
DISASM_ARG_swigregister = _x64dbgapi.DISASM_ARG_swigregister
DISASM_ARG_swigregister(DISASM_ARG)

class DISASM_INSTR(object):
    """Proxy of C++ DISASM_INSTR class"""
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    instruction = _swig_property(_x64dbgapi.DISASM_INSTR_instruction_get, _x64dbgapi.DISASM_INSTR_instruction_set)
    type = _swig_property(_x64dbgapi.DISASM_INSTR_type_get, _x64dbgapi.DISASM_INSTR_type_set)
    argcount = _swig_property(_x64dbgapi.DISASM_INSTR_argcount_get, _x64dbgapi.DISASM_INSTR_argcount_set)
    instr_size = _swig_property(_x64dbgapi.DISASM_INSTR_instr_size_get, _x64dbgapi.DISASM_INSTR_instr_size_set)
    arg = _swig_property(_x64dbgapi.DISASM_INSTR_arg_get, _x64dbgapi.DISASM_INSTR_arg_set)
    def __init__(self): 
        """__init__(DISASM_INSTR self) -> DISASM_INSTR"""
        this = _x64dbgapi.new_DISASM_INSTR()
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _x64dbgapi.delete_DISASM_INSTR
    __del__ = lambda self : None;
DISASM_INSTR_swigregister = _x64dbgapi.DISASM_INSTR_swigregister
DISASM_INSTR_swigregister(DISASM_INSTR)

class STACK_COMMENT(object):
    """Proxy of C++ STACK_COMMENT class"""
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    color = _swig_property(_x64dbgapi.STACK_COMMENT_color_get, _x64dbgapi.STACK_COMMENT_color_set)
    comment = _swig_property(_x64dbgapi.STACK_COMMENT_comment_get, _x64dbgapi.STACK_COMMENT_comment_set)
    def __init__(self): 
        """__init__(STACK_COMMENT self) -> STACK_COMMENT"""
        this = _x64dbgapi.new_STACK_COMMENT()
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _x64dbgapi.delete_STACK_COMMENT
    __del__ = lambda self : None;
STACK_COMMENT_swigregister = _x64dbgapi.STACK_COMMENT_swigregister
STACK_COMMENT_swigregister(STACK_COMMENT)

class THREADINFO(object):
    """Proxy of C++ THREADINFO class"""
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    ThreadNumber = _swig_property(_x64dbgapi.THREADINFO_ThreadNumber_get, _x64dbgapi.THREADINFO_ThreadNumber_set)
    Handle = _swig_property(_x64dbgapi.THREADINFO_Handle_get, _x64dbgapi.THREADINFO_Handle_set)
    ThreadId = _swig_property(_x64dbgapi.THREADINFO_ThreadId_get, _x64dbgapi.THREADINFO_ThreadId_set)
    ThreadStartAddress = _swig_property(_x64dbgapi.THREADINFO_ThreadStartAddress_get, _x64dbgapi.THREADINFO_ThreadStartAddress_set)
    ThreadLocalBase = _swig_property(_x64dbgapi.THREADINFO_ThreadLocalBase_get, _x64dbgapi.THREADINFO_ThreadLocalBase_set)
    threadName = _swig_property(_x64dbgapi.THREADINFO_threadName_get, _x64dbgapi.THREADINFO_threadName_set)
    def __init__(self): 
        """__init__(THREADINFO self) -> THREADINFO"""
        this = _x64dbgapi.new_THREADINFO()
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _x64dbgapi.delete_THREADINFO
    __del__ = lambda self : None;
THREADINFO_swigregister = _x64dbgapi.THREADINFO_swigregister
THREADINFO_swigregister(THREADINFO)

class THREADALLINFO(object):
    """Proxy of C++ THREADALLINFO class"""
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    BasicInfo = _swig_property(_x64dbgapi.THREADALLINFO_BasicInfo_get, _x64dbgapi.THREADALLINFO_BasicInfo_set)
    ThreadCip = _swig_property(_x64dbgapi.THREADALLINFO_ThreadCip_get, _x64dbgapi.THREADALLINFO_ThreadCip_set)
    SuspendCount = _swig_property(_x64dbgapi.THREADALLINFO_SuspendCount_get, _x64dbgapi.THREADALLINFO_SuspendCount_set)
    Priority = _swig_property(_x64dbgapi.THREADALLINFO_Priority_get, _x64dbgapi.THREADALLINFO_Priority_set)
    WaitReason = _swig_property(_x64dbgapi.THREADALLINFO_WaitReason_get, _x64dbgapi.THREADALLINFO_WaitReason_set)
    LastError = _swig_property(_x64dbgapi.THREADALLINFO_LastError_get, _x64dbgapi.THREADALLINFO_LastError_set)
    UserTime = _swig_property(_x64dbgapi.THREADALLINFO_UserTime_get, _x64dbgapi.THREADALLINFO_UserTime_set)
    KernelTime = _swig_property(_x64dbgapi.THREADALLINFO_KernelTime_get, _x64dbgapi.THREADALLINFO_KernelTime_set)
    CreationTime = _swig_property(_x64dbgapi.THREADALLINFO_CreationTime_get, _x64dbgapi.THREADALLINFO_CreationTime_set)
    Cycles = _swig_property(_x64dbgapi.THREADALLINFO_Cycles_get, _x64dbgapi.THREADALLINFO_Cycles_set)
    def __init__(self): 
        """__init__(THREADALLINFO self) -> THREADALLINFO"""
        this = _x64dbgapi.new_THREADALLINFO()
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _x64dbgapi.delete_THREADALLINFO
    __del__ = lambda self : None;
THREADALLINFO_swigregister = _x64dbgapi.THREADALLINFO_swigregister
THREADALLINFO_swigregister(THREADALLINFO)

class THREADLIST(object):
    """Proxy of C++ THREADLIST class"""
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    count = _swig_property(_x64dbgapi.THREADLIST_count_get, _x64dbgapi.THREADLIST_count_set)
    list = _swig_property(_x64dbgapi.THREADLIST_list_get, _x64dbgapi.THREADLIST_list_set)
    CurrentThread = _swig_property(_x64dbgapi.THREADLIST_CurrentThread_get, _x64dbgapi.THREADLIST_CurrentThread_set)
    def __init__(self): 
        """__init__(THREADLIST self) -> THREADLIST"""
        this = _x64dbgapi.new_THREADLIST()
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _x64dbgapi.delete_THREADLIST
    __del__ = lambda self : None;
THREADLIST_swigregister = _x64dbgapi.THREADLIST_swigregister
THREADLIST_swigregister(THREADLIST)

class MEMORY_INFO(object):
    """Proxy of C++ MEMORY_INFO class"""
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    value = _swig_property(_x64dbgapi.MEMORY_INFO_value_get, _x64dbgapi.MEMORY_INFO_value_set)
    size = _swig_property(_x64dbgapi.MEMORY_INFO_size_get, _x64dbgapi.MEMORY_INFO_size_set)
    mnemonic = _swig_property(_x64dbgapi.MEMORY_INFO_mnemonic_get, _x64dbgapi.MEMORY_INFO_mnemonic_set)
    def __init__(self): 
        """__init__(MEMORY_INFO self) -> MEMORY_INFO"""
        this = _x64dbgapi.new_MEMORY_INFO()
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _x64dbgapi.delete_MEMORY_INFO
    __del__ = lambda self : None;
MEMORY_INFO_swigregister = _x64dbgapi.MEMORY_INFO_swigregister
MEMORY_INFO_swigregister(MEMORY_INFO)

class VALUE_INFO(object):
    """Proxy of C++ VALUE_INFO class"""
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    value = _swig_property(_x64dbgapi.VALUE_INFO_value_get, _x64dbgapi.VALUE_INFO_value_set)
    size = _swig_property(_x64dbgapi.VALUE_INFO_size_get, _x64dbgapi.VALUE_INFO_size_set)
    def __init__(self): 
        """__init__(VALUE_INFO self) -> VALUE_INFO"""
        this = _x64dbgapi.new_VALUE_INFO()
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _x64dbgapi.delete_VALUE_INFO
    __del__ = lambda self : None;
VALUE_INFO_swigregister = _x64dbgapi.VALUE_INFO_swigregister
VALUE_INFO_swigregister(VALUE_INFO)

TYPE_VALUE = _x64dbgapi.TYPE_VALUE
TYPE_MEMORY = _x64dbgapi.TYPE_MEMORY
TYPE_ADDR = _x64dbgapi.TYPE_ADDR
class BASIC_INSTRUCTION_INFO(object):
    """Proxy of C++ BASIC_INSTRUCTION_INFO class"""
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    type = _swig_property(_x64dbgapi.BASIC_INSTRUCTION_INFO_type_get, _x64dbgapi.BASIC_INSTRUCTION_INFO_type_set)
    value = _swig_property(_x64dbgapi.BASIC_INSTRUCTION_INFO_value_get, _x64dbgapi.BASIC_INSTRUCTION_INFO_value_set)
    memory = _swig_property(_x64dbgapi.BASIC_INSTRUCTION_INFO_memory_get, _x64dbgapi.BASIC_INSTRUCTION_INFO_memory_set)
    addr = _swig_property(_x64dbgapi.BASIC_INSTRUCTION_INFO_addr_get, _x64dbgapi.BASIC_INSTRUCTION_INFO_addr_set)
    branch = _swig_property(_x64dbgapi.BASIC_INSTRUCTION_INFO_branch_get, _x64dbgapi.BASIC_INSTRUCTION_INFO_branch_set)
    call = _swig_property(_x64dbgapi.BASIC_INSTRUCTION_INFO_call_get, _x64dbgapi.BASIC_INSTRUCTION_INFO_call_set)
    size = _swig_property(_x64dbgapi.BASIC_INSTRUCTION_INFO_size_get, _x64dbgapi.BASIC_INSTRUCTION_INFO_size_set)
    instruction = _swig_property(_x64dbgapi.BASIC_INSTRUCTION_INFO_instruction_get, _x64dbgapi.BASIC_INSTRUCTION_INFO_instruction_set)
    def __init__(self): 
        """__init__(BASIC_INSTRUCTION_INFO self) -> BASIC_INSTRUCTION_INFO"""
        this = _x64dbgapi.new_BASIC_INSTRUCTION_INFO()
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _x64dbgapi.delete_BASIC_INSTRUCTION_INFO
    __del__ = lambda self : None;
BASIC_INSTRUCTION_INFO_swigregister = _x64dbgapi.BASIC_INSTRUCTION_INFO_swigregister
BASIC_INSTRUCTION_INFO_swigregister(BASIC_INSTRUCTION_INFO)

class SCRIPTBRANCH(object):
    """Proxy of C++ SCRIPTBRANCH class"""
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    type = _swig_property(_x64dbgapi.SCRIPTBRANCH_type_get, _x64dbgapi.SCRIPTBRANCH_type_set)
    dest = _swig_property(_x64dbgapi.SCRIPTBRANCH_dest_get, _x64dbgapi.SCRIPTBRANCH_dest_set)
    branchlabel = _swig_property(_x64dbgapi.SCRIPTBRANCH_branchlabel_get, _x64dbgapi.SCRIPTBRANCH_branchlabel_set)
    def __init__(self): 
        """__init__(SCRIPTBRANCH self) -> SCRIPTBRANCH"""
        this = _x64dbgapi.new_SCRIPTBRANCH()
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _x64dbgapi.delete_SCRIPTBRANCH
    __del__ = lambda self : None;
SCRIPTBRANCH_swigregister = _x64dbgapi.SCRIPTBRANCH_swigregister
SCRIPTBRANCH_swigregister(SCRIPTBRANCH)

class FUNCTION_LOOP_INFO(object):
    """Proxy of C++ FUNCTION_LOOP_INFO class"""
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    addr = _swig_property(_x64dbgapi.FUNCTION_LOOP_INFO_addr_get, _x64dbgapi.FUNCTION_LOOP_INFO_addr_set)
    start = _swig_property(_x64dbgapi.FUNCTION_LOOP_INFO_start_get, _x64dbgapi.FUNCTION_LOOP_INFO_start_set)
    end = _swig_property(_x64dbgapi.FUNCTION_LOOP_INFO_end_get, _x64dbgapi.FUNCTION_LOOP_INFO_end_set)
    manual = _swig_property(_x64dbgapi.FUNCTION_LOOP_INFO_manual_get, _x64dbgapi.FUNCTION_LOOP_INFO_manual_set)
    depth = _swig_property(_x64dbgapi.FUNCTION_LOOP_INFO_depth_get, _x64dbgapi.FUNCTION_LOOP_INFO_depth_set)
    def __init__(self): 
        """__init__(FUNCTION_LOOP_INFO self) -> FUNCTION_LOOP_INFO"""
        this = _x64dbgapi.new_FUNCTION_LOOP_INFO()
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _x64dbgapi.delete_FUNCTION_LOOP_INFO
    __del__ = lambda self : None;
FUNCTION_LOOP_INFO_swigregister = _x64dbgapi.FUNCTION_LOOP_INFO_swigregister
FUNCTION_LOOP_INFO_swigregister(FUNCTION_LOOP_INFO)

class XREF_RECORD(object):
    """Proxy of C++ XREF_RECORD class"""
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    addr = _swig_property(_x64dbgapi.XREF_RECORD_addr_get, _x64dbgapi.XREF_RECORD_addr_set)
    type = _swig_property(_x64dbgapi.XREF_RECORD_type_get, _x64dbgapi.XREF_RECORD_type_set)
    def __init__(self): 
        """__init__(XREF_RECORD self) -> XREF_RECORD"""
        this = _x64dbgapi.new_XREF_RECORD()
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _x64dbgapi.delete_XREF_RECORD
    __del__ = lambda self : None;
XREF_RECORD_swigregister = _x64dbgapi.XREF_RECORD_swigregister
XREF_RECORD_swigregister(XREF_RECORD)

class XREF_INFO(object):
    """Proxy of C++ XREF_INFO class"""
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    refcount = _swig_property(_x64dbgapi.XREF_INFO_refcount_get, _x64dbgapi.XREF_INFO_refcount_set)
    references = _swig_property(_x64dbgapi.XREF_INFO_references_get, _x64dbgapi.XREF_INFO_references_set)
    def __init__(self): 
        """__init__(XREF_INFO self) -> XREF_INFO"""
        this = _x64dbgapi.new_XREF_INFO()
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _x64dbgapi.delete_XREF_INFO
    __del__ = lambda self : None;
XREF_INFO_swigregister = _x64dbgapi.XREF_INFO_swigregister
XREF_INFO_swigregister(XREF_INFO)

class SYMBOLPTR(object):
    """Proxy of C++ SYMBOLPTR_ class"""
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    modbase = _swig_property(_x64dbgapi.SYMBOLPTR_modbase_get, _x64dbgapi.SYMBOLPTR_modbase_set)
    symbol = _swig_property(_x64dbgapi.SYMBOLPTR_symbol_get, _x64dbgapi.SYMBOLPTR_symbol_set)
    def __init__(self): 
        """__init__(SYMBOLPTR_ self) -> SYMBOLPTR"""
        this = _x64dbgapi.new_SYMBOLPTR()
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _x64dbgapi.delete_SYMBOLPTR
    __del__ = lambda self : None;
SYMBOLPTR_swigregister = _x64dbgapi.SYMBOLPTR_swigregister
SYMBOLPTR_swigregister(SYMBOLPTR)


def DbgInit():
  """DbgInit() -> char const *"""
  return _x64dbgapi.DbgInit()

def DbgExit():
  """DbgExit()"""
  return _x64dbgapi.DbgExit()

def DbgMemRead(*args):
  """DbgMemRead(duint va, void * dest, duint size) -> bool"""
  return _x64dbgapi.DbgMemRead(*args)

def DbgMemWrite(*args):
  """DbgMemWrite(duint va, void const * src, duint size) -> bool"""
  return _x64dbgapi.DbgMemWrite(*args)

def DbgMemGetPageSize(*args):
  """DbgMemGetPageSize(duint base) -> duint"""
  return _x64dbgapi.DbgMemGetPageSize(*args)

def DbgMemFindBaseAddr(*args):
  """DbgMemFindBaseAddr(duint addr, duint * size) -> duint"""
  return _x64dbgapi.DbgMemFindBaseAddr(*args)

def DbgCmdExec(*args):
  """DbgCmdExec(char const * cmd) -> bool"""
  return _x64dbgapi.DbgCmdExec(*args)

def DbgCmdExecDirect(*args):
  """DbgCmdExecDirect(char const * cmd) -> bool"""
  return _x64dbgapi.DbgCmdExecDirect(*args)

def DbgMemMap(*args):
  """DbgMemMap(MEMMAP memmap) -> bool"""
  return _x64dbgapi.DbgMemMap(*args)

def DbgIsValidExpression(*args):
  """DbgIsValidExpression(char const * expression) -> bool"""
  return _x64dbgapi.DbgIsValidExpression(*args)

def DbgIsDebugging():
  """DbgIsDebugging() -> bool"""
  return _x64dbgapi.DbgIsDebugging()

def DbgIsJumpGoingToExecute(*args):
  """DbgIsJumpGoingToExecute(duint addr) -> bool"""
  return _x64dbgapi.DbgIsJumpGoingToExecute(*args)

def DbgGetLabelAt(*args):
  """DbgGetLabelAt(duint addr, SEGMENTREG segment, char * text) -> bool"""
  return _x64dbgapi.DbgGetLabelAt(*args)
def DbgGetLabelAt(addr, segment):
    import ctypes as C
    buff = C.create_string_buffer(_x64dbgapi.MAX_LABEL_SIZE)
    if not _x64dbgapi.DbgGetLabelAt(addr, segment, buff):
        return
    return buff.value.replace('\0', '')


def DbgSetLabelAt(*args):
  """DbgSetLabelAt(duint addr, char const * text) -> bool"""
  return _x64dbgapi.DbgSetLabelAt(*args)

def DbgClearLabelRange(*args):
  """DbgClearLabelRange(duint start, duint end)"""
  return _x64dbgapi.DbgClearLabelRange(*args)

def DbgGetCommentAt(*args):
  """DbgGetCommentAt(duint addr, char * text) -> bool"""
  return _x64dbgapi.DbgGetCommentAt(*args)

def DbgSetCommentAt(*args):
  """DbgSetCommentAt(duint addr, char const * text) -> bool"""
  return _x64dbgapi.DbgSetCommentAt(*args)

def DbgClearCommentRange(*args):
  """DbgClearCommentRange(duint start, duint end)"""
  return _x64dbgapi.DbgClearCommentRange(*args)

def DbgGetBookmarkAt(*args):
  """DbgGetBookmarkAt(duint addr) -> bool"""
  return _x64dbgapi.DbgGetBookmarkAt(*args)

def DbgSetBookmarkAt(*args):
  """DbgSetBookmarkAt(duint addr, bool isbookmark) -> bool"""
  return _x64dbgapi.DbgSetBookmarkAt(*args)

def DbgClearBookmarkRange(*args):
  """DbgClearBookmarkRange(duint start, duint end)"""
  return _x64dbgapi.DbgClearBookmarkRange(*args)

def DbgGetModuleAt(*args):
  """DbgGetModuleAt(duint addr, char * text) -> bool"""
  return _x64dbgapi.DbgGetModuleAt(*args)

def DbgGetBpxTypeAt(*args):
  """DbgGetBpxTypeAt(duint addr) -> BPXTYPE"""
  return _x64dbgapi.DbgGetBpxTypeAt(*args)

def DbgValFromString(*args):
  """DbgValFromString(char const * string) -> duint"""
  return _x64dbgapi.DbgValFromString(*args)

def DbgGetRegDumpEx(*args):
  """DbgGetRegDumpEx(REGDUMP regdump, size_t size) -> bool"""
  return _x64dbgapi.DbgGetRegDumpEx(*args)

def DbgValToString(*args):
  """DbgValToString(char const * string, duint value) -> bool"""
  return _x64dbgapi.DbgValToString(*args)

def DbgMemIsValidReadPtr(*args):
  """DbgMemIsValidReadPtr(duint addr) -> bool"""
  return _x64dbgapi.DbgMemIsValidReadPtr(*args)

def DbgGetBpList(*args):
  """DbgGetBpList(BPXTYPE type, BPMAP list) -> int"""
  return _x64dbgapi.DbgGetBpList(*args)

def DbgGetFunctionTypeAt(*args):
  """DbgGetFunctionTypeAt(duint addr) -> FUNCTYPE"""
  return _x64dbgapi.DbgGetFunctionTypeAt(*args)

def DbgGetLoopTypeAt(*args):
  """DbgGetLoopTypeAt(duint addr, int depth) -> LOOPTYPE"""
  return _x64dbgapi.DbgGetLoopTypeAt(*args)

def DbgGetBranchDestination(*args):
  """DbgGetBranchDestination(duint addr) -> duint"""
  return _x64dbgapi.DbgGetBranchDestination(*args)

def DbgScriptLoad(*args):
  """DbgScriptLoad(char const * filename)"""
  return _x64dbgapi.DbgScriptLoad(*args)

def DbgScriptUnload():
  """DbgScriptUnload()"""
  return _x64dbgapi.DbgScriptUnload()

def DbgScriptRun(*args):
  """DbgScriptRun(int destline)"""
  return _x64dbgapi.DbgScriptRun(*args)

def DbgScriptStep():
  """DbgScriptStep()"""
  return _x64dbgapi.DbgScriptStep()

def DbgScriptBpToggle(*args):
  """DbgScriptBpToggle(int line) -> bool"""
  return _x64dbgapi.DbgScriptBpToggle(*args)

def DbgScriptBpGet(*args):
  """DbgScriptBpGet(int line) -> bool"""
  return _x64dbgapi.DbgScriptBpGet(*args)

def DbgScriptCmdExec(*args):
  """DbgScriptCmdExec(char const * command) -> bool"""
  return _x64dbgapi.DbgScriptCmdExec(*args)

def DbgScriptAbort():
  """DbgScriptAbort()"""
  return _x64dbgapi.DbgScriptAbort()

def DbgScriptGetLineType(*args):
  """DbgScriptGetLineType(int line) -> SCRIPTLINETYPE"""
  return _x64dbgapi.DbgScriptGetLineType(*args)

def DbgScriptSetIp(*args):
  """DbgScriptSetIp(int line)"""
  return _x64dbgapi.DbgScriptSetIp(*args)

def DbgScriptGetBranchInfo(*args):
  """DbgScriptGetBranchInfo(int line, SCRIPTBRANCH info) -> bool"""
  return _x64dbgapi.DbgScriptGetBranchInfo(*args)

def DbgSymbolEnum(*args):
  """DbgSymbolEnum(duint base, CBSYMBOLENUM cbSymbolEnum, void * user)"""
  return _x64dbgapi.DbgSymbolEnum(*args)

def DbgSymbolEnumFromCache(*args):
  """DbgSymbolEnumFromCache(duint base, CBSYMBOLENUM cbSymbolEnum, void * user)"""
  return _x64dbgapi.DbgSymbolEnumFromCache(*args)

def DbgAssembleAt(*args):
  """DbgAssembleAt(duint addr, char const * instruction) -> bool"""
  return _x64dbgapi.DbgAssembleAt(*args)

def DbgModBaseFromName(*args):
  """DbgModBaseFromName(char const * name) -> duint"""
  return _x64dbgapi.DbgModBaseFromName(*args)

def DbgDisasmAt(*args):
  """DbgDisasmAt(duint addr, DISASM_INSTR instr)"""
  return _x64dbgapi.DbgDisasmAt(*args)

def DbgStackCommentGet(*args):
  """DbgStackCommentGet(duint addr, STACK_COMMENT comment) -> bool"""
  return _x64dbgapi.DbgStackCommentGet(*args)

def DbgGetThreadList(*args):
  """DbgGetThreadList(THREADLIST list)"""
  return _x64dbgapi.DbgGetThreadList(*args)

def DbgSettingsUpdated():
  """DbgSettingsUpdated()"""
  return _x64dbgapi.DbgSettingsUpdated()

def DbgDisasmFastAt(*args):
  """DbgDisasmFastAt(duint addr, BASIC_INSTRUCTION_INFO basicinfo)"""
  return _x64dbgapi.DbgDisasmFastAt(*args)

def DbgMenuEntryClicked(*args):
  """DbgMenuEntryClicked(int hEntry)"""
  return _x64dbgapi.DbgMenuEntryClicked(*args)

def DbgFunctionGet(*args):
  """DbgFunctionGet(duint addr, duint * start, duint * end) -> bool"""
  return _x64dbgapi.DbgFunctionGet(*args)

def DbgFunctionOverlaps(*args):
  """DbgFunctionOverlaps(duint start, duint end) -> bool"""
  return _x64dbgapi.DbgFunctionOverlaps(*args)

def DbgFunctionAdd(*args):
  """DbgFunctionAdd(duint start, duint end) -> bool"""
  return _x64dbgapi.DbgFunctionAdd(*args)

def DbgFunctionDel(*args):
  """DbgFunctionDel(duint addr) -> bool"""
  return _x64dbgapi.DbgFunctionDel(*args)

def DbgArgumentGet(*args):
  """DbgArgumentGet(duint addr, duint * start, duint * end) -> bool"""
  return _x64dbgapi.DbgArgumentGet(*args)

def DbgArgumentOverlaps(*args):
  """DbgArgumentOverlaps(duint start, duint end) -> bool"""
  return _x64dbgapi.DbgArgumentOverlaps(*args)

def DbgArgumentAdd(*args):
  """DbgArgumentAdd(duint start, duint end) -> bool"""
  return _x64dbgapi.DbgArgumentAdd(*args)

def DbgArgumentDel(*args):
  """DbgArgumentDel(duint addr) -> bool"""
  return _x64dbgapi.DbgArgumentDel(*args)

def DbgLoopGet(*args):
  """DbgLoopGet(int depth, duint addr, duint * start, duint * end) -> bool"""
  return _x64dbgapi.DbgLoopGet(*args)

def DbgLoopOverlaps(*args):
  """DbgLoopOverlaps(int depth, duint start, duint end) -> bool"""
  return _x64dbgapi.DbgLoopOverlaps(*args)

def DbgLoopAdd(*args):
  """DbgLoopAdd(duint start, duint end) -> bool"""
  return _x64dbgapi.DbgLoopAdd(*args)

def DbgLoopDel(*args):
  """DbgLoopDel(int depth, duint addr) -> bool"""
  return _x64dbgapi.DbgLoopDel(*args)

def DbgXrefAdd(*args):
  """DbgXrefAdd(duint addr, duint _from) -> bool"""
  return _x64dbgapi.DbgXrefAdd(*args)

def DbgXrefDelAll(*args):
  """DbgXrefDelAll(duint addr) -> bool"""
  return _x64dbgapi.DbgXrefDelAll(*args)

def DbgXrefGet(*args):
  """DbgXrefGet(duint addr, XREF_INFO info) -> bool"""
  return _x64dbgapi.DbgXrefGet(*args)

def DbgGetXrefCountAt(*args):
  """DbgGetXrefCountAt(duint addr) -> size_t"""
  return _x64dbgapi.DbgGetXrefCountAt(*args)

def DbgGetXrefTypeAt(*args):
  """DbgGetXrefTypeAt(duint addr) -> XREFTYPE"""
  return _x64dbgapi.DbgGetXrefTypeAt(*args)

def DbgIsRunLocked():
  """DbgIsRunLocked() -> bool"""
  return _x64dbgapi.DbgIsRunLocked()

def DbgIsBpDisabled(*args):
  """DbgIsBpDisabled(duint addr) -> bool"""
  return _x64dbgapi.DbgIsBpDisabled(*args)

def DbgSetAutoCommentAt(*args):
  """DbgSetAutoCommentAt(duint addr, char const * text) -> bool"""
  return _x64dbgapi.DbgSetAutoCommentAt(*args)

def DbgClearAutoCommentRange(*args):
  """DbgClearAutoCommentRange(duint start, duint end)"""
  return _x64dbgapi.DbgClearAutoCommentRange(*args)

def DbgSetAutoLabelAt(*args):
  """DbgSetAutoLabelAt(duint addr, char const * text) -> bool"""
  return _x64dbgapi.DbgSetAutoLabelAt(*args)

def DbgClearAutoLabelRange(*args):
  """DbgClearAutoLabelRange(duint start, duint end)"""
  return _x64dbgapi.DbgClearAutoLabelRange(*args)

def DbgSetAutoBookmarkAt(*args):
  """DbgSetAutoBookmarkAt(duint addr) -> bool"""
  return _x64dbgapi.DbgSetAutoBookmarkAt(*args)

def DbgClearAutoBookmarkRange(*args):
  """DbgClearAutoBookmarkRange(duint start, duint end)"""
  return _x64dbgapi.DbgClearAutoBookmarkRange(*args)

def DbgSetAutoFunctionAt(*args):
  """DbgSetAutoFunctionAt(duint start, duint end) -> bool"""
  return _x64dbgapi.DbgSetAutoFunctionAt(*args)

def DbgClearAutoFunctionRange(*args):
  """DbgClearAutoFunctionRange(duint start, duint end)"""
  return _x64dbgapi.DbgClearAutoFunctionRange(*args)

def DbgGetStringAt(*args):
  """DbgGetStringAt(duint addr, char * text) -> bool"""
  return _x64dbgapi.DbgGetStringAt(*args)

def DbgFunctions():
  """DbgFunctions() -> DBGFUNCTIONS"""
  return _x64dbgapi.DbgFunctions()

def DbgWinEvent(*args):
  """DbgWinEvent(MSG * message, long * result) -> bool"""
  return _x64dbgapi.DbgWinEvent(*args)

def DbgWinEventGlobal(*args):
  """DbgWinEventGlobal(MSG * message) -> bool"""
  return _x64dbgapi.DbgWinEventGlobal(*args)

def DbgIsRunning():
  """DbgIsRunning() -> bool"""
  return _x64dbgapi.DbgIsRunning()

def DbgGetTimeWastedCounter():
  """DbgGetTimeWastedCounter() -> duint"""
  return _x64dbgapi.DbgGetTimeWastedCounter()

def DbgGetArgTypeAt(*args):
  """DbgGetArgTypeAt(duint addr) -> ARGTYPE"""
  return _x64dbgapi.DbgGetArgTypeAt(*args)

def DbgGetEncodeTypeBuffer(*args):
  """DbgGetEncodeTypeBuffer(duint addr, duint * size) -> void *"""
  return _x64dbgapi.DbgGetEncodeTypeBuffer(*args)

def DbgReleaseEncodeTypeBuffer(*args):
  """DbgReleaseEncodeTypeBuffer(void * buffer)"""
  return _x64dbgapi.DbgReleaseEncodeTypeBuffer(*args)

def DbgGetEncodeTypeAt(*args):
  """DbgGetEncodeTypeAt(duint addr, duint size) -> ENCODETYPE"""
  return _x64dbgapi.DbgGetEncodeTypeAt(*args)

def DbgGetEncodeSizeAt(*args):
  """DbgGetEncodeSizeAt(duint addr, duint codesize) -> duint"""
  return _x64dbgapi.DbgGetEncodeSizeAt(*args)

def DbgSetEncodeType(*args):
  """DbgSetEncodeType(duint addr, duint size, ENCODETYPE type) -> bool"""
  return _x64dbgapi.DbgSetEncodeType(*args)

def DbgDelEncodeTypeRange(*args):
  """DbgDelEncodeTypeRange(duint start, duint end)"""
  return _x64dbgapi.DbgDelEncodeTypeRange(*args)

def DbgDelEncodeTypeSegment(*args):
  """DbgDelEncodeTypeSegment(duint start)"""
  return _x64dbgapi.DbgDelEncodeTypeSegment(*args)

def DbgGetWatchList(*args):
  """DbgGetWatchList(ListInfo list) -> bool"""
  return _x64dbgapi.DbgGetWatchList(*args)

def DbgSelChanged(*args):
  """DbgSelChanged(int hWindow, duint VA)"""
  return _x64dbgapi.DbgSelChanged(*args)

def DbgGetProcessHandle():
  """DbgGetProcessHandle() -> HANDLE"""
  return _x64dbgapi.DbgGetProcessHandle()

def DbgGetThreadHandle():
  """DbgGetThreadHandle() -> HANDLE"""
  return _x64dbgapi.DbgGetThreadHandle()

def DbgGetProcessId():
  """DbgGetProcessId() -> DWORD"""
  return _x64dbgapi.DbgGetProcessId()

def DbgGetThreadId():
  """DbgGetThreadId() -> DWORD"""
  return _x64dbgapi.DbgGetThreadId()

def DbgGetPebAddress(*args):
  """DbgGetPebAddress(DWORD ProcessId) -> duint"""
  return _x64dbgapi.DbgGetPebAddress(*args)

def DbgGetTebAddress(*args):
  """DbgGetTebAddress(DWORD ThreadId) -> duint"""
  return _x64dbgapi.DbgGetTebAddress(*args)

def DbgAnalyzeFunction(*args):
  """DbgAnalyzeFunction(duint entry, BridgeCFGraphList * graph) -> bool"""
  return _x64dbgapi.DbgAnalyzeFunction(*args)

def DbgEval(*args):
  """DbgEval(char const * expression, bool * success=None) -> duint"""
  return _x64dbgapi.DbgEval(*args)

def DbgMenuPrepare(*args):
  """DbgMenuPrepare(int hMenu)"""
  return _x64dbgapi.DbgMenuPrepare(*args)

def DbgGetSymbolInfo(*args):
  """DbgGetSymbolInfo(SYMBOLPTR symbolptr, SYMBOLINFO info)"""
  return _x64dbgapi.DbgGetSymbolInfo(*args)
GUI_PLUGIN_MENU = _x64dbgapi.GUI_PLUGIN_MENU
GUI_DISASM_MENU = _x64dbgapi.GUI_DISASM_MENU
GUI_DUMP_MENU = _x64dbgapi.GUI_DUMP_MENU
GUI_STACK_MENU = _x64dbgapi.GUI_STACK_MENU
GUI_DISASSEMBLY = _x64dbgapi.GUI_DISASSEMBLY
GUI_DUMP = _x64dbgapi.GUI_DUMP
GUI_STACK = _x64dbgapi.GUI_STACK
GUI_GRAPH = _x64dbgapi.GUI_GRAPH
GUI_MEMMAP = _x64dbgapi.GUI_MEMMAP
GUI_SYMMOD = _x64dbgapi.GUI_SYMMOD
GUI_MAX_LINE_SIZE = _x64dbgapi.GUI_MAX_LINE_SIZE
GUI_MAX_DISASSEMBLY_SIZE = _x64dbgapi.GUI_MAX_DISASSEMBLY_SIZE
GUI_DISASSEMBLE_AT = _x64dbgapi.GUI_DISASSEMBLE_AT
GUI_SET_DEBUG_STATE = _x64dbgapi.GUI_SET_DEBUG_STATE
GUI_ADD_MSG_TO_LOG = _x64dbgapi.GUI_ADD_MSG_TO_LOG
GUI_CLEAR_LOG = _x64dbgapi.GUI_CLEAR_LOG
GUI_UPDATE_REGISTER_VIEW = _x64dbgapi.GUI_UPDATE_REGISTER_VIEW
GUI_UPDATE_DISASSEMBLY_VIEW = _x64dbgapi.GUI_UPDATE_DISASSEMBLY_VIEW
GUI_UPDATE_BREAKPOINTS_VIEW = _x64dbgapi.GUI_UPDATE_BREAKPOINTS_VIEW
GUI_UPDATE_WINDOW_TITLE = _x64dbgapi.GUI_UPDATE_WINDOW_TITLE
GUI_GET_WINDOW_HANDLE = _x64dbgapi.GUI_GET_WINDOW_HANDLE
GUI_DUMP_AT = _x64dbgapi.GUI_DUMP_AT
GUI_SCRIPT_ADD = _x64dbgapi.GUI_SCRIPT_ADD
GUI_SCRIPT_CLEAR = _x64dbgapi.GUI_SCRIPT_CLEAR
GUI_SCRIPT_SETIP = _x64dbgapi.GUI_SCRIPT_SETIP
GUI_SCRIPT_ERROR = _x64dbgapi.GUI_SCRIPT_ERROR
GUI_SCRIPT_SETTITLE = _x64dbgapi.GUI_SCRIPT_SETTITLE
GUI_SCRIPT_SETINFOLINE = _x64dbgapi.GUI_SCRIPT_SETINFOLINE
GUI_SCRIPT_MESSAGE = _x64dbgapi.GUI_SCRIPT_MESSAGE
GUI_SCRIPT_MSGYN = _x64dbgapi.GUI_SCRIPT_MSGYN
GUI_SYMBOL_LOG_ADD = _x64dbgapi.GUI_SYMBOL_LOG_ADD
GUI_SYMBOL_LOG_CLEAR = _x64dbgapi.GUI_SYMBOL_LOG_CLEAR
GUI_SYMBOL_SET_PROGRESS = _x64dbgapi.GUI_SYMBOL_SET_PROGRESS
GUI_SYMBOL_UPDATE_MODULE_LIST = _x64dbgapi.GUI_SYMBOL_UPDATE_MODULE_LIST
GUI_REF_ADDCOLUMN = _x64dbgapi.GUI_REF_ADDCOLUMN
GUI_REF_SETROWCOUNT = _x64dbgapi.GUI_REF_SETROWCOUNT
GUI_REF_GETROWCOUNT = _x64dbgapi.GUI_REF_GETROWCOUNT
GUI_REF_DELETEALLCOLUMNS = _x64dbgapi.GUI_REF_DELETEALLCOLUMNS
GUI_REF_SETCELLCONTENT = _x64dbgapi.GUI_REF_SETCELLCONTENT
GUI_REF_GETCELLCONTENT = _x64dbgapi.GUI_REF_GETCELLCONTENT
GUI_REF_RELOADDATA = _x64dbgapi.GUI_REF_RELOADDATA
GUI_REF_SETSINGLESELECTION = _x64dbgapi.GUI_REF_SETSINGLESELECTION
GUI_REF_SETPROGRESS = _x64dbgapi.GUI_REF_SETPROGRESS
GUI_REF_SETCURRENTTASKPROGRESS = _x64dbgapi.GUI_REF_SETCURRENTTASKPROGRESS
GUI_REF_SETSEARCHSTARTCOL = _x64dbgapi.GUI_REF_SETSEARCHSTARTCOL
GUI_STACK_DUMP_AT = _x64dbgapi.GUI_STACK_DUMP_AT
GUI_UPDATE_DUMP_VIEW = _x64dbgapi.GUI_UPDATE_DUMP_VIEW
GUI_UPDATE_THREAD_VIEW = _x64dbgapi.GUI_UPDATE_THREAD_VIEW
GUI_ADD_RECENT_FILE = _x64dbgapi.GUI_ADD_RECENT_FILE
GUI_SET_LAST_EXCEPTION = _x64dbgapi.GUI_SET_LAST_EXCEPTION
GUI_GET_DISASSEMBLY = _x64dbgapi.GUI_GET_DISASSEMBLY
GUI_MENU_ADD = _x64dbgapi.GUI_MENU_ADD
GUI_MENU_ADD_ENTRY = _x64dbgapi.GUI_MENU_ADD_ENTRY
GUI_MENU_ADD_SEPARATOR = _x64dbgapi.GUI_MENU_ADD_SEPARATOR
GUI_MENU_CLEAR = _x64dbgapi.GUI_MENU_CLEAR
GUI_SELECTION_GET = _x64dbgapi.GUI_SELECTION_GET
GUI_SELECTION_SET = _x64dbgapi.GUI_SELECTION_SET
GUI_GETLINE_WINDOW = _x64dbgapi.GUI_GETLINE_WINDOW
GUI_AUTOCOMPLETE_ADDCMD = _x64dbgapi.GUI_AUTOCOMPLETE_ADDCMD
GUI_AUTOCOMPLETE_DELCMD = _x64dbgapi.GUI_AUTOCOMPLETE_DELCMD
GUI_AUTOCOMPLETE_CLEARALL = _x64dbgapi.GUI_AUTOCOMPLETE_CLEARALL
GUI_SCRIPT_ENABLEHIGHLIGHTING = _x64dbgapi.GUI_SCRIPT_ENABLEHIGHLIGHTING
GUI_ADD_MSG_TO_STATUSBAR = _x64dbgapi.GUI_ADD_MSG_TO_STATUSBAR
GUI_UPDATE_SIDEBAR = _x64dbgapi.GUI_UPDATE_SIDEBAR
GUI_REPAINT_TABLE_VIEW = _x64dbgapi.GUI_REPAINT_TABLE_VIEW
GUI_UPDATE_PATCHES = _x64dbgapi.GUI_UPDATE_PATCHES
GUI_UPDATE_CALLSTACK = _x64dbgapi.GUI_UPDATE_CALLSTACK
GUI_UPDATE_SEHCHAIN = _x64dbgapi.GUI_UPDATE_SEHCHAIN
GUI_SYMBOL_REFRESH_CURRENT = _x64dbgapi.GUI_SYMBOL_REFRESH_CURRENT
GUI_UPDATE_MEMORY_VIEW = _x64dbgapi.GUI_UPDATE_MEMORY_VIEW
GUI_REF_INITIALIZE = _x64dbgapi.GUI_REF_INITIALIZE
GUI_LOAD_SOURCE_FILE = _x64dbgapi.GUI_LOAD_SOURCE_FILE
GUI_MENU_SET_ICON = _x64dbgapi.GUI_MENU_SET_ICON
GUI_MENU_SET_ENTRY_ICON = _x64dbgapi.GUI_MENU_SET_ENTRY_ICON
GUI_SHOW_CPU = _x64dbgapi.GUI_SHOW_CPU
GUI_ADD_QWIDGET_TAB = _x64dbgapi.GUI_ADD_QWIDGET_TAB
GUI_SHOW_QWIDGET_TAB = _x64dbgapi.GUI_SHOW_QWIDGET_TAB
GUI_CLOSE_QWIDGET_TAB = _x64dbgapi.GUI_CLOSE_QWIDGET_TAB
GUI_EXECUTE_ON_GUI_THREAD = _x64dbgapi.GUI_EXECUTE_ON_GUI_THREAD
GUI_UPDATE_TIME_WASTED_COUNTER = _x64dbgapi.GUI_UPDATE_TIME_WASTED_COUNTER
GUI_SET_GLOBAL_NOTES = _x64dbgapi.GUI_SET_GLOBAL_NOTES
GUI_GET_GLOBAL_NOTES = _x64dbgapi.GUI_GET_GLOBAL_NOTES
GUI_SET_DEBUGGEE_NOTES = _x64dbgapi.GUI_SET_DEBUGGEE_NOTES
GUI_GET_DEBUGGEE_NOTES = _x64dbgapi.GUI_GET_DEBUGGEE_NOTES
GUI_DUMP_AT_N = _x64dbgapi.GUI_DUMP_AT_N
GUI_DISPLAY_WARNING = _x64dbgapi.GUI_DISPLAY_WARNING
GUI_REGISTER_SCRIPT_LANG = _x64dbgapi.GUI_REGISTER_SCRIPT_LANG
GUI_UNREGISTER_SCRIPT_LANG = _x64dbgapi.GUI_UNREGISTER_SCRIPT_LANG
GUI_UPDATE_ARGUMENT_VIEW = _x64dbgapi.GUI_UPDATE_ARGUMENT_VIEW
GUI_FOCUS_VIEW = _x64dbgapi.GUI_FOCUS_VIEW
GUI_UPDATE_WATCH_VIEW = _x64dbgapi.GUI_UPDATE_WATCH_VIEW
GUI_LOAD_GRAPH = _x64dbgapi.GUI_LOAD_GRAPH
GUI_GRAPH_AT = _x64dbgapi.GUI_GRAPH_AT
GUI_UPDATE_GRAPH_VIEW = _x64dbgapi.GUI_UPDATE_GRAPH_VIEW
GUI_SET_LOG_ENABLED = _x64dbgapi.GUI_SET_LOG_ENABLED
GUI_ADD_FAVOURITE_TOOL = _x64dbgapi.GUI_ADD_FAVOURITE_TOOL
GUI_ADD_FAVOURITE_COMMAND = _x64dbgapi.GUI_ADD_FAVOURITE_COMMAND
GUI_SET_FAVOURITE_TOOL_SHORTCUT = _x64dbgapi.GUI_SET_FAVOURITE_TOOL_SHORTCUT
GUI_FOLD_DISASSEMBLY = _x64dbgapi.GUI_FOLD_DISASSEMBLY
GUI_SELECT_IN_MEMORY_MAP = _x64dbgapi.GUI_SELECT_IN_MEMORY_MAP
GUI_GET_ACTIVE_VIEW = _x64dbgapi.GUI_GET_ACTIVE_VIEW
GUI_MENU_SET_ENTRY_CHECKED = _x64dbgapi.GUI_MENU_SET_ENTRY_CHECKED
GUI_ADD_INFO_LINE = _x64dbgapi.GUI_ADD_INFO_LINE
GUI_PROCESS_EVENTS = _x64dbgapi.GUI_PROCESS_EVENTS
GUI_TYPE_ADDNODE = _x64dbgapi.GUI_TYPE_ADDNODE
GUI_TYPE_CLEAR = _x64dbgapi.GUI_TYPE_CLEAR
GUI_UPDATE_TYPE_WIDGET = _x64dbgapi.GUI_UPDATE_TYPE_WIDGET
GUI_CLOSE_APPLICATION = _x64dbgapi.GUI_CLOSE_APPLICATION
GUI_MENU_SET_VISIBLE = _x64dbgapi.GUI_MENU_SET_VISIBLE
GUI_MENU_SET_ENTRY_VISIBLE = _x64dbgapi.GUI_MENU_SET_ENTRY_VISIBLE
GUI_MENU_SET_NAME = _x64dbgapi.GUI_MENU_SET_NAME
GUI_MENU_SET_ENTRY_NAME = _x64dbgapi.GUI_MENU_SET_ENTRY_NAME
GUI_FLUSH_LOG = _x64dbgapi.GUI_FLUSH_LOG
GUI_MENU_SET_ENTRY_HOTKEY = _x64dbgapi.GUI_MENU_SET_ENTRY_HOTKEY
GUI_REF_SEARCH_GETROWCOUNT = _x64dbgapi.GUI_REF_SEARCH_GETROWCOUNT
GUI_REF_SEARCH_GETCELLCONTENT = _x64dbgapi.GUI_REF_SEARCH_GETCELLCONTENT
GUI_MENU_REMOVE = _x64dbgapi.GUI_MENU_REMOVE
GUI_REF_ADDCOMMAND = _x64dbgapi.GUI_REF_ADDCOMMAND
GUI_OPEN_TRACE_FILE = _x64dbgapi.GUI_OPEN_TRACE_FILE
GUI_UPDATE_TRACE_BROWSER = _x64dbgapi.GUI_UPDATE_TRACE_BROWSER
GUI_INVALIDATE_SYMBOL_SOURCE = _x64dbgapi.GUI_INVALIDATE_SYMBOL_SOURCE
class CELLINFO(object):
    """Proxy of C++ CELLINFO class"""
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    row = _swig_property(_x64dbgapi.CELLINFO_row_get, _x64dbgapi.CELLINFO_row_set)
    col = _swig_property(_x64dbgapi.CELLINFO_col_get, _x64dbgapi.CELLINFO_col_set)
    str = _swig_property(_x64dbgapi.CELLINFO_str_get, _x64dbgapi.CELLINFO_str_set)
    def __init__(self): 
        """__init__(CELLINFO self) -> CELLINFO"""
        this = _x64dbgapi.new_CELLINFO()
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _x64dbgapi.delete_CELLINFO
    __del__ = lambda self : None;
CELLINFO_swigregister = _x64dbgapi.CELLINFO_swigregister
CELLINFO_swigregister(CELLINFO)

class SELECTIONDATA(object):
    """Proxy of C++ SELECTIONDATA class"""
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    start = _swig_property(_x64dbgapi.SELECTIONDATA_start_get, _x64dbgapi.SELECTIONDATA_start_set)
    end = _swig_property(_x64dbgapi.SELECTIONDATA_end_get, _x64dbgapi.SELECTIONDATA_end_set)
    def __init__(self): 
        """__init__(SELECTIONDATA self) -> SELECTIONDATA"""
        this = _x64dbgapi.new_SELECTIONDATA()
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _x64dbgapi.delete_SELECTIONDATA
    __del__ = lambda self : None;
SELECTIONDATA_swigregister = _x64dbgapi.SELECTIONDATA_swigregister
SELECTIONDATA_swigregister(SELECTIONDATA)

class ICONDATA(object):
    """Proxy of C++ ICONDATA class"""
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    data = _swig_property(_x64dbgapi.ICONDATA_data_get, _x64dbgapi.ICONDATA_data_set)
    size = _swig_property(_x64dbgapi.ICONDATA_size_get, _x64dbgapi.ICONDATA_size_set)
    def __init__(self): 
        """__init__(ICONDATA self) -> ICONDATA"""
        this = _x64dbgapi.new_ICONDATA()
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _x64dbgapi.delete_ICONDATA
    __del__ = lambda self : None;
ICONDATA_swigregister = _x64dbgapi.ICONDATA_swigregister
ICONDATA_swigregister(ICONDATA)

class SCRIPTTYPEINFO(object):
    """Proxy of C++ SCRIPTTYPEINFO class"""
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    name = _swig_property(_x64dbgapi.SCRIPTTYPEINFO_name_get, _x64dbgapi.SCRIPTTYPEINFO_name_set)
    id = _swig_property(_x64dbgapi.SCRIPTTYPEINFO_id_get, _x64dbgapi.SCRIPTTYPEINFO_id_set)
    execute = _swig_property(_x64dbgapi.SCRIPTTYPEINFO_execute_get, _x64dbgapi.SCRIPTTYPEINFO_execute_set)
    completeCommand = _swig_property(_x64dbgapi.SCRIPTTYPEINFO_completeCommand_get, _x64dbgapi.SCRIPTTYPEINFO_completeCommand_set)
    def __init__(self): 
        """__init__(SCRIPTTYPEINFO self) -> SCRIPTTYPEINFO"""
        this = _x64dbgapi.new_SCRIPTTYPEINFO()
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _x64dbgapi.delete_SCRIPTTYPEINFO
    __del__ = lambda self : None;
SCRIPTTYPEINFO_swigregister = _x64dbgapi.SCRIPTTYPEINFO_swigregister
SCRIPTTYPEINFO_swigregister(SCRIPTTYPEINFO)

class ACTIVEVIEW(object):
    """Proxy of C++ ACTIVEVIEW class"""
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    titleHwnd = _swig_property(_x64dbgapi.ACTIVEVIEW_titleHwnd_get, _x64dbgapi.ACTIVEVIEW_titleHwnd_set)
    classHwnd = _swig_property(_x64dbgapi.ACTIVEVIEW_classHwnd_get, _x64dbgapi.ACTIVEVIEW_classHwnd_set)
    title = _swig_property(_x64dbgapi.ACTIVEVIEW_title_get, _x64dbgapi.ACTIVEVIEW_title_set)
    className = _swig_property(_x64dbgapi.ACTIVEVIEW_className_get, _x64dbgapi.ACTIVEVIEW_className_set)
    def __init__(self): 
        """__init__(ACTIVEVIEW self) -> ACTIVEVIEW"""
        this = _x64dbgapi.new_ACTIVEVIEW()
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _x64dbgapi.delete_ACTIVEVIEW
    __del__ = lambda self : None;
ACTIVEVIEW_swigregister = _x64dbgapi.ACTIVEVIEW_swigregister
ACTIVEVIEW_swigregister(ACTIVEVIEW)

class TYPEDESCRIPTOR(object):
    """Proxy of C++ _TYPEDESCRIPTOR class"""
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    expanded = _swig_property(_x64dbgapi.TYPEDESCRIPTOR_expanded_get, _x64dbgapi.TYPEDESCRIPTOR_expanded_set)
    reverse = _swig_property(_x64dbgapi.TYPEDESCRIPTOR_reverse_get, _x64dbgapi.TYPEDESCRIPTOR_reverse_set)
    name = _swig_property(_x64dbgapi.TYPEDESCRIPTOR_name_get, _x64dbgapi.TYPEDESCRIPTOR_name_set)
    addr = _swig_property(_x64dbgapi.TYPEDESCRIPTOR_addr_get, _x64dbgapi.TYPEDESCRIPTOR_addr_set)
    offset = _swig_property(_x64dbgapi.TYPEDESCRIPTOR_offset_get, _x64dbgapi.TYPEDESCRIPTOR_offset_set)
    id = _swig_property(_x64dbgapi.TYPEDESCRIPTOR_id_get, _x64dbgapi.TYPEDESCRIPTOR_id_set)
    size = _swig_property(_x64dbgapi.TYPEDESCRIPTOR_size_get, _x64dbgapi.TYPEDESCRIPTOR_size_set)
    callback = _swig_property(_x64dbgapi.TYPEDESCRIPTOR_callback_get, _x64dbgapi.TYPEDESCRIPTOR_callback_set)
    userdata = _swig_property(_x64dbgapi.TYPEDESCRIPTOR_userdata_get, _x64dbgapi.TYPEDESCRIPTOR_userdata_set)
    def __init__(self): 
        """__init__(_TYPEDESCRIPTOR self) -> TYPEDESCRIPTOR"""
        this = _x64dbgapi.new_TYPEDESCRIPTOR()
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _x64dbgapi.delete_TYPEDESCRIPTOR
    __del__ = lambda self : None;
TYPEDESCRIPTOR_swigregister = _x64dbgapi.TYPEDESCRIPTOR_swigregister
TYPEDESCRIPTOR_swigregister(TYPEDESCRIPTOR)


def GuiTranslateText(*args):
  """GuiTranslateText(char const * Source) -> char const *"""
  return _x64dbgapi.GuiTranslateText(*args)

def GuiDisasmAt(*args):
  """GuiDisasmAt(duint addr, duint cip)"""
  return _x64dbgapi.GuiDisasmAt(*args)

def GuiSetDebugState(*args):
  """GuiSetDebugState(DBGSTATE state)"""
  return _x64dbgapi.GuiSetDebugState(*args)

def GuiSetDebugStateFast(*args):
  """GuiSetDebugStateFast(DBGSTATE state)"""
  return _x64dbgapi.GuiSetDebugStateFast(*args)

def GuiAddLogMessage(*args):
  """GuiAddLogMessage(char const * msg)"""
  return _x64dbgapi.GuiAddLogMessage(*args)

def GuiLogClear():
  """GuiLogClear()"""
  return _x64dbgapi.GuiLogClear()

def GuiUpdateAllViews():
  """GuiUpdateAllViews()"""
  return _x64dbgapi.GuiUpdateAllViews()

def GuiUpdateRegisterView():
  """GuiUpdateRegisterView()"""
  return _x64dbgapi.GuiUpdateRegisterView()

def GuiUpdateDisassemblyView():
  """GuiUpdateDisassemblyView()"""
  return _x64dbgapi.GuiUpdateDisassemblyView()

def GuiUpdateBreakpointsView():
  """GuiUpdateBreakpointsView()"""
  return _x64dbgapi.GuiUpdateBreakpointsView()

def GuiUpdateWindowTitle(*args):
  """GuiUpdateWindowTitle(char const * filename)"""
  return _x64dbgapi.GuiUpdateWindowTitle(*args)

def GuiGetWindowHandle():
  """GuiGetWindowHandle() -> HWND"""
  return _x64dbgapi.GuiGetWindowHandle()

def GuiDumpAt(*args):
  """GuiDumpAt(duint va)"""
  return _x64dbgapi.GuiDumpAt(*args)

def GuiScriptAdd(*args):
  """GuiScriptAdd(int count, char const ** lines)"""
  return _x64dbgapi.GuiScriptAdd(*args)

def GuiScriptClear():
  """GuiScriptClear()"""
  return _x64dbgapi.GuiScriptClear()

def GuiScriptSetIp(*args):
  """GuiScriptSetIp(int line)"""
  return _x64dbgapi.GuiScriptSetIp(*args)

def GuiScriptError(*args):
  """GuiScriptError(int line, char const * message)"""
  return _x64dbgapi.GuiScriptError(*args)

def GuiScriptSetTitle(*args):
  """GuiScriptSetTitle(char const * title)"""
  return _x64dbgapi.GuiScriptSetTitle(*args)

def GuiScriptSetInfoLine(*args):
  """GuiScriptSetInfoLine(int line, char const * info)"""
  return _x64dbgapi.GuiScriptSetInfoLine(*args)

def GuiScriptMessage(*args):
  """GuiScriptMessage(char const * message)"""
  return _x64dbgapi.GuiScriptMessage(*args)

def GuiScriptMsgyn(*args):
  """GuiScriptMsgyn(char const * message) -> int"""
  return _x64dbgapi.GuiScriptMsgyn(*args)

def GuiScriptEnableHighlighting(*args):
  """GuiScriptEnableHighlighting(bool enable)"""
  return _x64dbgapi.GuiScriptEnableHighlighting(*args)

def GuiSymbolLogAdd(*args):
  """GuiSymbolLogAdd(char const * message)"""
  return _x64dbgapi.GuiSymbolLogAdd(*args)

def GuiSymbolLogClear():
  """GuiSymbolLogClear()"""
  return _x64dbgapi.GuiSymbolLogClear()

def GuiSymbolSetProgress(*args):
  """GuiSymbolSetProgress(int percent)"""
  return _x64dbgapi.GuiSymbolSetProgress(*args)

def GuiSymbolUpdateModuleList(*args):
  """GuiSymbolUpdateModuleList(int count, SYMBOLMODULEINFO modules)"""
  return _x64dbgapi.GuiSymbolUpdateModuleList(*args)

def GuiSymbolRefreshCurrent():
  """GuiSymbolRefreshCurrent()"""
  return _x64dbgapi.GuiSymbolRefreshCurrent()

def GuiReferenceAddColumn(*args):
  """GuiReferenceAddColumn(int width, char const * title)"""
  return _x64dbgapi.GuiReferenceAddColumn(*args)

def GuiReferenceSetRowCount(*args):
  """GuiReferenceSetRowCount(int count)"""
  return _x64dbgapi.GuiReferenceSetRowCount(*args)

def GuiReferenceGetRowCount():
  """GuiReferenceGetRowCount() -> int"""
  return _x64dbgapi.GuiReferenceGetRowCount()

def GuiReferenceSearchGetRowCount():
  """GuiReferenceSearchGetRowCount() -> int"""
  return _x64dbgapi.GuiReferenceSearchGetRowCount()

def GuiReferenceDeleteAllColumns():
  """GuiReferenceDeleteAllColumns()"""
  return _x64dbgapi.GuiReferenceDeleteAllColumns()

def GuiReferenceInitialize(*args):
  """GuiReferenceInitialize(char const * name)"""
  return _x64dbgapi.GuiReferenceInitialize(*args)

def GuiReferenceSetCellContent(*args):
  """GuiReferenceSetCellContent(int row, int col, char const * str)"""
  return _x64dbgapi.GuiReferenceSetCellContent(*args)

def GuiReferenceGetCellContent(*args):
  """GuiReferenceGetCellContent(int row, int col) -> char const *"""
  return _x64dbgapi.GuiReferenceGetCellContent(*args)

def GuiReferenceSearchGetCellContent(*args):
  """GuiReferenceSearchGetCellContent(int row, int col) -> char const *"""
  return _x64dbgapi.GuiReferenceSearchGetCellContent(*args)

def GuiReferenceReloadData():
  """GuiReferenceReloadData()"""
  return _x64dbgapi.GuiReferenceReloadData()

def GuiReferenceSetSingleSelection(*args):
  """GuiReferenceSetSingleSelection(int index, bool scroll)"""
  return _x64dbgapi.GuiReferenceSetSingleSelection(*args)

def GuiReferenceSetProgress(*args):
  """GuiReferenceSetProgress(int progress)"""
  return _x64dbgapi.GuiReferenceSetProgress(*args)

def GuiReferenceSetCurrentTaskProgress(*args):
  """GuiReferenceSetCurrentTaskProgress(int progress, char const * taskTitle)"""
  return _x64dbgapi.GuiReferenceSetCurrentTaskProgress(*args)

def GuiReferenceSetSearchStartCol(*args):
  """GuiReferenceSetSearchStartCol(int col)"""
  return _x64dbgapi.GuiReferenceSetSearchStartCol(*args)

def GuiStackDumpAt(*args):
  """GuiStackDumpAt(duint addr, duint csp)"""
  return _x64dbgapi.GuiStackDumpAt(*args)

def GuiUpdateDumpView():
  """GuiUpdateDumpView()"""
  return _x64dbgapi.GuiUpdateDumpView()

def GuiUpdateWatchView():
  """GuiUpdateWatchView()"""
  return _x64dbgapi.GuiUpdateWatchView()

def GuiUpdateThreadView():
  """GuiUpdateThreadView()"""
  return _x64dbgapi.GuiUpdateThreadView()

def GuiUpdateMemoryView():
  """GuiUpdateMemoryView()"""
  return _x64dbgapi.GuiUpdateMemoryView()

def GuiAddRecentFile(*args):
  """GuiAddRecentFile(char const * file)"""
  return _x64dbgapi.GuiAddRecentFile(*args)

def GuiSetLastException(*args):
  """GuiSetLastException(unsigned int exception)"""
  return _x64dbgapi.GuiSetLastException(*args)

def GuiGetDisassembly(*args):
  """GuiGetDisassembly(duint addr, char * text) -> bool"""
  return _x64dbgapi.GuiGetDisassembly(*args)

def GuiMenuAdd(*args):
  """GuiMenuAdd(int hMenu, char const * title) -> int"""
  return _x64dbgapi.GuiMenuAdd(*args)

def GuiMenuAddEntry(*args):
  """GuiMenuAddEntry(int hMenu, char const * title) -> int"""
  return _x64dbgapi.GuiMenuAddEntry(*args)

def GuiMenuAddSeparator(*args):
  """GuiMenuAddSeparator(int hMenu)"""
  return _x64dbgapi.GuiMenuAddSeparator(*args)

def GuiMenuClear(*args):
  """GuiMenuClear(int hMenu)"""
  return _x64dbgapi.GuiMenuClear(*args)

def GuiMenuRemove(*args):
  """GuiMenuRemove(int hEntryMenu)"""
  return _x64dbgapi.GuiMenuRemove(*args)

def GuiSelectionGet(*args):
  """GuiSelectionGet(int hWindow, SELECTIONDATA selection) -> bool"""
  return _x64dbgapi.GuiSelectionGet(*args)

def GuiSelectionSet(*args):
  """GuiSelectionSet(int hWindow, SELECTIONDATA selection) -> bool"""
  return _x64dbgapi.GuiSelectionSet(*args)

def GuiGetLineWindow(*args):
  """GuiGetLineWindow(char const * title, char * text) -> bool"""
  return _x64dbgapi.GuiGetLineWindow(*args)

def GuiAutoCompleteAddCmd(*args):
  """GuiAutoCompleteAddCmd(char const * cmd)"""
  return _x64dbgapi.GuiAutoCompleteAddCmd(*args)

def GuiAutoCompleteDelCmd(*args):
  """GuiAutoCompleteDelCmd(char const * cmd)"""
  return _x64dbgapi.GuiAutoCompleteDelCmd(*args)

def GuiAutoCompleteClearAll():
  """GuiAutoCompleteClearAll()"""
  return _x64dbgapi.GuiAutoCompleteClearAll()

def GuiAddStatusBarMessage(*args):
  """GuiAddStatusBarMessage(char const * msg)"""
  return _x64dbgapi.GuiAddStatusBarMessage(*args)

def GuiUpdateSideBar():
  """GuiUpdateSideBar()"""
  return _x64dbgapi.GuiUpdateSideBar()

def GuiRepaintTableView():
  """GuiRepaintTableView()"""
  return _x64dbgapi.GuiRepaintTableView()

def GuiUpdatePatches():
  """GuiUpdatePatches()"""
  return _x64dbgapi.GuiUpdatePatches()

def GuiUpdateCallStack():
  """GuiUpdateCallStack()"""
  return _x64dbgapi.GuiUpdateCallStack()

def GuiUpdateSEHChain():
  """GuiUpdateSEHChain()"""
  return _x64dbgapi.GuiUpdateSEHChain()

def GuiLoadSourceFileEx(*args):
  """GuiLoadSourceFileEx(char const * path, duint addr)"""
  return _x64dbgapi.GuiLoadSourceFileEx(*args)

def GuiMenuSetIcon(*args):
  """GuiMenuSetIcon(int hMenu, ICONDATA icon)"""
  return _x64dbgapi.GuiMenuSetIcon(*args)

def GuiMenuSetEntryIcon(*args):
  """GuiMenuSetEntryIcon(int hEntry, ICONDATA icon)"""
  return _x64dbgapi.GuiMenuSetEntryIcon(*args)

def GuiMenuSetEntryChecked(*args):
  """GuiMenuSetEntryChecked(int hEntry, bool checked)"""
  return _x64dbgapi.GuiMenuSetEntryChecked(*args)

def GuiMenuSetVisible(*args):
  """GuiMenuSetVisible(int hMenu, bool visible)"""
  return _x64dbgapi.GuiMenuSetVisible(*args)

def GuiMenuSetEntryVisible(*args):
  """GuiMenuSetEntryVisible(int hEntry, bool visible)"""
  return _x64dbgapi.GuiMenuSetEntryVisible(*args)

def GuiMenuSetName(*args):
  """GuiMenuSetName(int hMenu, char const * name)"""
  return _x64dbgapi.GuiMenuSetName(*args)

def GuiMenuSetEntryName(*args):
  """GuiMenuSetEntryName(int hEntry, char const * name)"""
  return _x64dbgapi.GuiMenuSetEntryName(*args)

def GuiMenuSetEntryHotkey(*args):
  """GuiMenuSetEntryHotkey(int hEntry, char const * hack)"""
  return _x64dbgapi.GuiMenuSetEntryHotkey(*args)

def GuiShowCpu():
  """GuiShowCpu()"""
  return _x64dbgapi.GuiShowCpu()

def GuiAddQWidgetTab(*args):
  """GuiAddQWidgetTab(void * qWidget)"""
  return _x64dbgapi.GuiAddQWidgetTab(*args)

def GuiShowQWidgetTab(*args):
  """GuiShowQWidgetTab(void * qWidget)"""
  return _x64dbgapi.GuiShowQWidgetTab(*args)

def GuiCloseQWidgetTab(*args):
  """GuiCloseQWidgetTab(void * qWidget)"""
  return _x64dbgapi.GuiCloseQWidgetTab(*args)

def GuiExecuteOnGuiThread(*args):
  """GuiExecuteOnGuiThread(GUICALLBACK cbGuiThread)"""
  return _x64dbgapi.GuiExecuteOnGuiThread(*args)

def GuiUpdateTimeWastedCounter():
  """GuiUpdateTimeWastedCounter()"""
  return _x64dbgapi.GuiUpdateTimeWastedCounter()

def GuiSetGlobalNotes(*args):
  """GuiSetGlobalNotes(char const * text)"""
  return _x64dbgapi.GuiSetGlobalNotes(*args)

def GuiGetGlobalNotes(*args):
  """GuiGetGlobalNotes(char ** text)"""
  return _x64dbgapi.GuiGetGlobalNotes(*args)

def GuiSetDebuggeeNotes(*args):
  """GuiSetDebuggeeNotes(char const * text)"""
  return _x64dbgapi.GuiSetDebuggeeNotes(*args)

def GuiGetDebuggeeNotes(*args):
  """GuiGetDebuggeeNotes(char ** text)"""
  return _x64dbgapi.GuiGetDebuggeeNotes(*args)

def GuiDumpAtN(*args):
  """GuiDumpAtN(duint va, int index)"""
  return _x64dbgapi.GuiDumpAtN(*args)

def GuiDisplayWarning(*args):
  """GuiDisplayWarning(char const * title, char const * text)"""
  return _x64dbgapi.GuiDisplayWarning(*args)

def GuiRegisterScriptLanguage(*args):
  """GuiRegisterScriptLanguage(SCRIPTTYPEINFO info)"""
  return _x64dbgapi.GuiRegisterScriptLanguage(*args)

def GuiUnregisterScriptLanguage(*args):
  """GuiUnregisterScriptLanguage(int id)"""
  return _x64dbgapi.GuiUnregisterScriptLanguage(*args)

def GuiUpdateArgumentWidget():
  """GuiUpdateArgumentWidget()"""
  return _x64dbgapi.GuiUpdateArgumentWidget()

def GuiFocusView(*args):
  """GuiFocusView(int hWindow)"""
  return _x64dbgapi.GuiFocusView(*args)

def GuiIsUpdateDisabled():
  """GuiIsUpdateDisabled() -> bool"""
  return _x64dbgapi.GuiIsUpdateDisabled()

def GuiUpdateEnable(*args):
  """GuiUpdateEnable(bool updateNow)"""
  return _x64dbgapi.GuiUpdateEnable(*args)

def GuiUpdateDisable():
  """GuiUpdateDisable()"""
  return _x64dbgapi.GuiUpdateDisable()

def GuiLoadGraph(*args):
  """GuiLoadGraph(BridgeCFGraphList * graph, duint addr) -> bool"""
  return _x64dbgapi.GuiLoadGraph(*args)

def GuiGraphAt(*args):
  """GuiGraphAt(duint addr) -> duint"""
  return _x64dbgapi.GuiGraphAt(*args)

def GuiUpdateGraphView():
  """GuiUpdateGraphView()"""
  return _x64dbgapi.GuiUpdateGraphView()

def GuiDisableLog():
  """GuiDisableLog()"""
  return _x64dbgapi.GuiDisableLog()

def GuiEnableLog():
  """GuiEnableLog()"""
  return _x64dbgapi.GuiEnableLog()

def GuiAddFavouriteTool(*args):
  """GuiAddFavouriteTool(char const * name, char const * description)"""
  return _x64dbgapi.GuiAddFavouriteTool(*args)

def GuiAddFavouriteCommand(*args):
  """GuiAddFavouriteCommand(char const * name, char const * shortcut)"""
  return _x64dbgapi.GuiAddFavouriteCommand(*args)

def GuiSetFavouriteToolShortcut(*args):
  """GuiSetFavouriteToolShortcut(char const * name, char const * shortcut)"""
  return _x64dbgapi.GuiSetFavouriteToolShortcut(*args)

def GuiFoldDisassembly(*args):
  """GuiFoldDisassembly(duint startAddress, duint length)"""
  return _x64dbgapi.GuiFoldDisassembly(*args)

def GuiSelectInMemoryMap(*args):
  """GuiSelectInMemoryMap(duint addr)"""
  return _x64dbgapi.GuiSelectInMemoryMap(*args)

def GuiGetActiveView(*args):
  """GuiGetActiveView(ACTIVEVIEW activeView)"""
  return _x64dbgapi.GuiGetActiveView(*args)

def GuiAddInfoLine(*args):
  """GuiAddInfoLine(char const * infoLine)"""
  return _x64dbgapi.GuiAddInfoLine(*args)

def GuiProcessEvents():
  """GuiProcessEvents()"""
  return _x64dbgapi.GuiProcessEvents()

def GuiTypeAddNode(*args):
  """GuiTypeAddNode(void * parent, TYPEDESCRIPTOR type) -> void *"""
  return _x64dbgapi.GuiTypeAddNode(*args)

def GuiTypeClear():
  """GuiTypeClear() -> bool"""
  return _x64dbgapi.GuiTypeClear()

def GuiUpdateTypeWidget():
  """GuiUpdateTypeWidget()"""
  return _x64dbgapi.GuiUpdateTypeWidget()

def GuiCloseApplication():
  """GuiCloseApplication()"""
  return _x64dbgapi.GuiCloseApplication()

def GuiFlushLog():
  """GuiFlushLog()"""
  return _x64dbgapi.GuiFlushLog()

def GuiReferenceAddCommand(*args):
  """GuiReferenceAddCommand(char const * title, char const * command)"""
  return _x64dbgapi.GuiReferenceAddCommand(*args)

def GuiUpdateTraceBrowser():
  """GuiUpdateTraceBrowser()"""
  return _x64dbgapi.GuiUpdateTraceBrowser()

def GuiOpenTraceFile(*args):
  """GuiOpenTraceFile(char const * fileName)"""
  return _x64dbgapi.GuiOpenTraceFile(*args)

def GuiInvalidateSymbolSource(*args):
  """GuiInvalidateSymbolSource(duint base)"""
  return _x64dbgapi.GuiInvalidateSymbolSource(*args)
class MEMPAGEArray(object):
    """Proxy of C++ MEMPAGEArray class"""
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    def __init__(self, *args): 
        """__init__(MEMPAGEArray self, size_t nelements) -> MEMPAGEArray"""
        this = _x64dbgapi.new_MEMPAGEArray(*args)
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _x64dbgapi.delete_MEMPAGEArray
    __del__ = lambda self : None;
    def __getitem__(self, *args):
        """__getitem__(MEMPAGEArray self, size_t index) -> MEMPAGE"""
        return _x64dbgapi.MEMPAGEArray___getitem__(self, *args)

    def __setitem__(self, *args):
        """__setitem__(MEMPAGEArray self, size_t index, MEMPAGE value)"""
        return _x64dbgapi.MEMPAGEArray___setitem__(self, *args)

    def cast(self):
        """cast(MEMPAGEArray self) -> MEMPAGE"""
        return _x64dbgapi.MEMPAGEArray_cast(self)

    def frompointer(*args):
        """frompointer(MEMPAGE t) -> MEMPAGEArray"""
        return _x64dbgapi.MEMPAGEArray_frompointer(*args)

    frompointer = staticmethod(frompointer)
MEMPAGEArray_swigregister = _x64dbgapi.MEMPAGEArray_swigregister
MEMPAGEArray_swigregister(MEMPAGEArray)

def MEMPAGEArray_frompointer(*args):
  """MEMPAGEArray_frompointer(MEMPAGE t) -> MEMPAGEArray"""
  return _x64dbgapi.MEMPAGEArray_frompointer(*args)


def void_to_MEMPAGE(*args):
  """void_to_MEMPAGE(void * x) -> MEMPAGE"""
  return _x64dbgapi.void_to_MEMPAGE(*args)
class DBGPATCHINFO(object):
    """Proxy of C++ DBGPATCHINFO class"""
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    mod = _swig_property(_x64dbgapi.DBGPATCHINFO_mod_get, _x64dbgapi.DBGPATCHINFO_mod_set)
    addr = _swig_property(_x64dbgapi.DBGPATCHINFO_addr_get, _x64dbgapi.DBGPATCHINFO_addr_set)
    oldbyte = _swig_property(_x64dbgapi.DBGPATCHINFO_oldbyte_get, _x64dbgapi.DBGPATCHINFO_oldbyte_set)
    newbyte = _swig_property(_x64dbgapi.DBGPATCHINFO_newbyte_get, _x64dbgapi.DBGPATCHINFO_newbyte_set)
    def __init__(self): 
        """__init__(DBGPATCHINFO self) -> DBGPATCHINFO"""
        this = _x64dbgapi.new_DBGPATCHINFO()
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _x64dbgapi.delete_DBGPATCHINFO
    __del__ = lambda self : None;
DBGPATCHINFO_swigregister = _x64dbgapi.DBGPATCHINFO_swigregister
DBGPATCHINFO_swigregister(DBGPATCHINFO)

class DBGCALLSTACKENTRY(object):
    """Proxy of C++ DBGCALLSTACKENTRY class"""
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    addr = _swig_property(_x64dbgapi.DBGCALLSTACKENTRY_addr_get, _x64dbgapi.DBGCALLSTACKENTRY_addr_set)
    _from = _swig_property(_x64dbgapi.DBGCALLSTACKENTRY__from_get, _x64dbgapi.DBGCALLSTACKENTRY__from_set)
    to = _swig_property(_x64dbgapi.DBGCALLSTACKENTRY_to_get, _x64dbgapi.DBGCALLSTACKENTRY_to_set)
    comment = _swig_property(_x64dbgapi.DBGCALLSTACKENTRY_comment_get, _x64dbgapi.DBGCALLSTACKENTRY_comment_set)
    def __init__(self): 
        """__init__(DBGCALLSTACKENTRY self) -> DBGCALLSTACKENTRY"""
        this = _x64dbgapi.new_DBGCALLSTACKENTRY()
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _x64dbgapi.delete_DBGCALLSTACKENTRY
    __del__ = lambda self : None;
DBGCALLSTACKENTRY_swigregister = _x64dbgapi.DBGCALLSTACKENTRY_swigregister
DBGCALLSTACKENTRY_swigregister(DBGCALLSTACKENTRY)

class DBGCALLSTACK(object):
    """Proxy of C++ DBGCALLSTACK class"""
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    total = _swig_property(_x64dbgapi.DBGCALLSTACK_total_get, _x64dbgapi.DBGCALLSTACK_total_set)
    entries = _swig_property(_x64dbgapi.DBGCALLSTACK_entries_get, _x64dbgapi.DBGCALLSTACK_entries_set)
    def __init__(self): 
        """__init__(DBGCALLSTACK self) -> DBGCALLSTACK"""
        this = _x64dbgapi.new_DBGCALLSTACK()
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _x64dbgapi.delete_DBGCALLSTACK
    __del__ = lambda self : None;
DBGCALLSTACK_swigregister = _x64dbgapi.DBGCALLSTACK_swigregister
DBGCALLSTACK_swigregister(DBGCALLSTACK)

class DBGSEHRECORD(object):
    """Proxy of C++ DBGSEHRECORD class"""
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    addr = _swig_property(_x64dbgapi.DBGSEHRECORD_addr_get, _x64dbgapi.DBGSEHRECORD_addr_set)
    handler = _swig_property(_x64dbgapi.DBGSEHRECORD_handler_get, _x64dbgapi.DBGSEHRECORD_handler_set)
    def __init__(self): 
        """__init__(DBGSEHRECORD self) -> DBGSEHRECORD"""
        this = _x64dbgapi.new_DBGSEHRECORD()
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _x64dbgapi.delete_DBGSEHRECORD
    __del__ = lambda self : None;
DBGSEHRECORD_swigregister = _x64dbgapi.DBGSEHRECORD_swigregister
DBGSEHRECORD_swigregister(DBGSEHRECORD)

class DBGSEHCHAIN(object):
    """Proxy of C++ DBGSEHCHAIN class"""
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    total = _swig_property(_x64dbgapi.DBGSEHCHAIN_total_get, _x64dbgapi.DBGSEHCHAIN_total_set)
    records = _swig_property(_x64dbgapi.DBGSEHCHAIN_records_get, _x64dbgapi.DBGSEHCHAIN_records_set)
    def __init__(self): 
        """__init__(DBGSEHCHAIN self) -> DBGSEHCHAIN"""
        this = _x64dbgapi.new_DBGSEHCHAIN()
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _x64dbgapi.delete_DBGSEHCHAIN
    __del__ = lambda self : None;
DBGSEHCHAIN_swigregister = _x64dbgapi.DBGSEHCHAIN_swigregister
DBGSEHCHAIN_swigregister(DBGSEHCHAIN)

class DBGPROCESSINFO(object):
    """Proxy of C++ DBGPROCESSINFO class"""
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    dwProcessId = _swig_property(_x64dbgapi.DBGPROCESSINFO_dwProcessId_get, _x64dbgapi.DBGPROCESSINFO_dwProcessId_set)
    szExeFile = _swig_property(_x64dbgapi.DBGPROCESSINFO_szExeFile_get, _x64dbgapi.DBGPROCESSINFO_szExeFile_set)
    szExeMainWindowTitle = _swig_property(_x64dbgapi.DBGPROCESSINFO_szExeMainWindowTitle_get, _x64dbgapi.DBGPROCESSINFO_szExeMainWindowTitle_set)
    szExeArgs = _swig_property(_x64dbgapi.DBGPROCESSINFO_szExeArgs_get, _x64dbgapi.DBGPROCESSINFO_szExeArgs_set)
    def __init__(self): 
        """__init__(DBGPROCESSINFO self) -> DBGPROCESSINFO"""
        this = _x64dbgapi.new_DBGPROCESSINFO()
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _x64dbgapi.delete_DBGPROCESSINFO
    __del__ = lambda self : None;
DBGPROCESSINFO_swigregister = _x64dbgapi.DBGPROCESSINFO_swigregister
DBGPROCESSINFO_swigregister(DBGPROCESSINFO)

class DBGRELOCATIONINFO(object):
    """Proxy of C++ DBGRELOCATIONINFO class"""
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    rva = _swig_property(_x64dbgapi.DBGRELOCATIONINFO_rva_get, _x64dbgapi.DBGRELOCATIONINFO_rva_set)
    type = _swig_property(_x64dbgapi.DBGRELOCATIONINFO_type_get, _x64dbgapi.DBGRELOCATIONINFO_type_set)
    size = _swig_property(_x64dbgapi.DBGRELOCATIONINFO_size_get, _x64dbgapi.DBGRELOCATIONINFO_size_set)
    def __init__(self): 
        """__init__(DBGRELOCATIONINFO self) -> DBGRELOCATIONINFO"""
        this = _x64dbgapi.new_DBGRELOCATIONINFO()
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _x64dbgapi.delete_DBGRELOCATIONINFO
    __del__ = lambda self : None;
DBGRELOCATIONINFO_swigregister = _x64dbgapi.DBGRELOCATIONINFO_swigregister
DBGRELOCATIONINFO_swigregister(DBGRELOCATIONINFO)

InstructionBody = _x64dbgapi.InstructionBody
InstructionHeading = _x64dbgapi.InstructionHeading
InstructionTailing = _x64dbgapi.InstructionTailing
InstructionOverlapped = _x64dbgapi.InstructionOverlapped
DataByte = _x64dbgapi.DataByte
DataWord = _x64dbgapi.DataWord
DataDWord = _x64dbgapi.DataDWord
DataQWord = _x64dbgapi.DataQWord
DataFloat = _x64dbgapi.DataFloat
DataDouble = _x64dbgapi.DataDouble
DataLongDouble = _x64dbgapi.DataLongDouble
DataXMM = _x64dbgapi.DataXMM
DataYMM = _x64dbgapi.DataYMM
DataMMX = _x64dbgapi.DataMMX
DataMixed = _x64dbgapi.DataMixed
InstructionDataMixed = _x64dbgapi.InstructionDataMixed
TraceRecordNone = _x64dbgapi.TraceRecordNone
TraceRecordBitExec = _x64dbgapi.TraceRecordBitExec
TraceRecordByteWithExecTypeAndCounter = _x64dbgapi.TraceRecordByteWithExecTypeAndCounter
TraceRecordWordWithExecTypeAndCounter = _x64dbgapi.TraceRecordWordWithExecTypeAndCounter
class HANDLEINFO(object):
    """Proxy of C++ HANDLEINFO class"""
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    Handle = _swig_property(_x64dbgapi.HANDLEINFO_Handle_get, _x64dbgapi.HANDLEINFO_Handle_set)
    TypeNumber = _swig_property(_x64dbgapi.HANDLEINFO_TypeNumber_get, _x64dbgapi.HANDLEINFO_TypeNumber_set)
    GrantedAccess = _swig_property(_x64dbgapi.HANDLEINFO_GrantedAccess_get, _x64dbgapi.HANDLEINFO_GrantedAccess_set)
    def __init__(self): 
        """__init__(HANDLEINFO self) -> HANDLEINFO"""
        this = _x64dbgapi.new_HANDLEINFO()
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _x64dbgapi.delete_HANDLEINFO
    __del__ = lambda self : None;
HANDLEINFO_swigregister = _x64dbgapi.HANDLEINFO_swigregister
HANDLEINFO_swigregister(HANDLEINFO)

TCP_ADDR_SIZE = _x64dbgapi.TCP_ADDR_SIZE
class TCPCONNECTIONINFO(object):
    """Proxy of C++ TCPCONNECTIONINFO class"""
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    RemoteAddress = _swig_property(_x64dbgapi.TCPCONNECTIONINFO_RemoteAddress_get, _x64dbgapi.TCPCONNECTIONINFO_RemoteAddress_set)
    RemotePort = _swig_property(_x64dbgapi.TCPCONNECTIONINFO_RemotePort_get, _x64dbgapi.TCPCONNECTIONINFO_RemotePort_set)
    LocalAddress = _swig_property(_x64dbgapi.TCPCONNECTIONINFO_LocalAddress_get, _x64dbgapi.TCPCONNECTIONINFO_LocalAddress_set)
    LocalPort = _swig_property(_x64dbgapi.TCPCONNECTIONINFO_LocalPort_get, _x64dbgapi.TCPCONNECTIONINFO_LocalPort_set)
    StateText = _swig_property(_x64dbgapi.TCPCONNECTIONINFO_StateText_get, _x64dbgapi.TCPCONNECTIONINFO_StateText_set)
    State = _swig_property(_x64dbgapi.TCPCONNECTIONINFO_State_get, _x64dbgapi.TCPCONNECTIONINFO_State_set)
    def __init__(self): 
        """__init__(TCPCONNECTIONINFO self) -> TCPCONNECTIONINFO"""
        this = _x64dbgapi.new_TCPCONNECTIONINFO()
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _x64dbgapi.delete_TCPCONNECTIONINFO
    __del__ = lambda self : None;
TCPCONNECTIONINFO_swigregister = _x64dbgapi.TCPCONNECTIONINFO_swigregister
TCPCONNECTIONINFO_swigregister(TCPCONNECTIONINFO)

class WINDOW_INFO(object):
    """Proxy of C++ WINDOW_INFO class"""
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    handle = _swig_property(_x64dbgapi.WINDOW_INFO_handle_get, _x64dbgapi.WINDOW_INFO_handle_set)
    parent = _swig_property(_x64dbgapi.WINDOW_INFO_parent_get, _x64dbgapi.WINDOW_INFO_parent_set)
    threadId = _swig_property(_x64dbgapi.WINDOW_INFO_threadId_get, _x64dbgapi.WINDOW_INFO_threadId_set)
    style = _swig_property(_x64dbgapi.WINDOW_INFO_style_get, _x64dbgapi.WINDOW_INFO_style_set)
    styleEx = _swig_property(_x64dbgapi.WINDOW_INFO_styleEx_get, _x64dbgapi.WINDOW_INFO_styleEx_set)
    wndProc = _swig_property(_x64dbgapi.WINDOW_INFO_wndProc_get, _x64dbgapi.WINDOW_INFO_wndProc_set)
    enabled = _swig_property(_x64dbgapi.WINDOW_INFO_enabled_get, _x64dbgapi.WINDOW_INFO_enabled_set)
    position = _swig_property(_x64dbgapi.WINDOW_INFO_position_get, _x64dbgapi.WINDOW_INFO_position_set)
    windowTitle = _swig_property(_x64dbgapi.WINDOW_INFO_windowTitle_get, _x64dbgapi.WINDOW_INFO_windowTitle_set)
    windowClass = _swig_property(_x64dbgapi.WINDOW_INFO_windowClass_get, _x64dbgapi.WINDOW_INFO_windowClass_set)
    def __init__(self): 
        """__init__(WINDOW_INFO self) -> WINDOW_INFO"""
        this = _x64dbgapi.new_WINDOW_INFO()
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _x64dbgapi.delete_WINDOW_INFO
    __del__ = lambda self : None;
WINDOW_INFO_swigregister = _x64dbgapi.WINDOW_INFO_swigregister
WINDOW_INFO_swigregister(WINDOW_INFO)

class HEAPINFO(object):
    """Proxy of C++ HEAPINFO class"""
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    addr = _swig_property(_x64dbgapi.HEAPINFO_addr_get, _x64dbgapi.HEAPINFO_addr_set)
    size = _swig_property(_x64dbgapi.HEAPINFO_size_get, _x64dbgapi.HEAPINFO_size_set)
    flags = _swig_property(_x64dbgapi.HEAPINFO_flags_get, _x64dbgapi.HEAPINFO_flags_set)
    def __init__(self): 
        """__init__(HEAPINFO self) -> HEAPINFO"""
        this = _x64dbgapi.new_HEAPINFO()
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _x64dbgapi.delete_HEAPINFO
    __del__ = lambda self : None;
HEAPINFO_swigregister = _x64dbgapi.HEAPINFO_swigregister
HEAPINFO_swigregister(HEAPINFO)

class CONSTANTINFO(object):
    """Proxy of C++ CONSTANTINFO class"""
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    name = _swig_property(_x64dbgapi.CONSTANTINFO_name_get, _x64dbgapi.CONSTANTINFO_name_set)
    value = _swig_property(_x64dbgapi.CONSTANTINFO_value_get, _x64dbgapi.CONSTANTINFO_value_set)
    def __init__(self): 
        """__init__(CONSTANTINFO self) -> CONSTANTINFO"""
        this = _x64dbgapi.new_CONSTANTINFO()
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _x64dbgapi.delete_CONSTANTINFO
    __del__ = lambda self : None;
CONSTANTINFO_swigregister = _x64dbgapi.CONSTANTINFO_swigregister
CONSTANTINFO_swigregister(CONSTANTINFO)

class DBGFUNCTIONS(object):
    """Proxy of C++ DBGFUNCTIONS_ class"""
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    AssembleAtEx = _swig_property(_x64dbgapi.DBGFUNCTIONS_AssembleAtEx_get, _x64dbgapi.DBGFUNCTIONS_AssembleAtEx_set)
    SectionFromAddr = _swig_property(_x64dbgapi.DBGFUNCTIONS_SectionFromAddr_get, _x64dbgapi.DBGFUNCTIONS_SectionFromAddr_set)
    ModNameFromAddr = _swig_property(_x64dbgapi.DBGFUNCTIONS_ModNameFromAddr_get, _x64dbgapi.DBGFUNCTIONS_ModNameFromAddr_set)
    ModBaseFromAddr = _swig_property(_x64dbgapi.DBGFUNCTIONS_ModBaseFromAddr_get, _x64dbgapi.DBGFUNCTIONS_ModBaseFromAddr_set)
    ModBaseFromName = _swig_property(_x64dbgapi.DBGFUNCTIONS_ModBaseFromName_get, _x64dbgapi.DBGFUNCTIONS_ModBaseFromName_set)
    ModSizeFromAddr = _swig_property(_x64dbgapi.DBGFUNCTIONS_ModSizeFromAddr_get, _x64dbgapi.DBGFUNCTIONS_ModSizeFromAddr_set)
    Assemble = _swig_property(_x64dbgapi.DBGFUNCTIONS_Assemble_get, _x64dbgapi.DBGFUNCTIONS_Assemble_set)
    PatchGet = _swig_property(_x64dbgapi.DBGFUNCTIONS_PatchGet_get, _x64dbgapi.DBGFUNCTIONS_PatchGet_set)
    PatchInRange = _swig_property(_x64dbgapi.DBGFUNCTIONS_PatchInRange_get, _x64dbgapi.DBGFUNCTIONS_PatchInRange_set)
    MemPatch = _swig_property(_x64dbgapi.DBGFUNCTIONS_MemPatch_get, _x64dbgapi.DBGFUNCTIONS_MemPatch_set)
    PatchRestoreRange = _swig_property(_x64dbgapi.DBGFUNCTIONS_PatchRestoreRange_get, _x64dbgapi.DBGFUNCTIONS_PatchRestoreRange_set)
    PatchEnum = _swig_property(_x64dbgapi.DBGFUNCTIONS_PatchEnum_get, _x64dbgapi.DBGFUNCTIONS_PatchEnum_set)
    PatchRestore = _swig_property(_x64dbgapi.DBGFUNCTIONS_PatchRestore_get, _x64dbgapi.DBGFUNCTIONS_PatchRestore_set)
    PatchFile = _swig_property(_x64dbgapi.DBGFUNCTIONS_PatchFile_get, _x64dbgapi.DBGFUNCTIONS_PatchFile_set)
    ModPathFromAddr = _swig_property(_x64dbgapi.DBGFUNCTIONS_ModPathFromAddr_get, _x64dbgapi.DBGFUNCTIONS_ModPathFromAddr_set)
    ModPathFromName = _swig_property(_x64dbgapi.DBGFUNCTIONS_ModPathFromName_get, _x64dbgapi.DBGFUNCTIONS_ModPathFromName_set)
    DisasmFast = _swig_property(_x64dbgapi.DBGFUNCTIONS_DisasmFast_get, _x64dbgapi.DBGFUNCTIONS_DisasmFast_set)
    MemUpdateMap = _swig_property(_x64dbgapi.DBGFUNCTIONS_MemUpdateMap_get, _x64dbgapi.DBGFUNCTIONS_MemUpdateMap_set)
    GetCallStack = _swig_property(_x64dbgapi.DBGFUNCTIONS_GetCallStack_get, _x64dbgapi.DBGFUNCTIONS_GetCallStack_set)
    GetSEHChain = _swig_property(_x64dbgapi.DBGFUNCTIONS_GetSEHChain_get, _x64dbgapi.DBGFUNCTIONS_GetSEHChain_set)
    SymbolDownloadAllSymbols = _swig_property(_x64dbgapi.DBGFUNCTIONS_SymbolDownloadAllSymbols_get, _x64dbgapi.DBGFUNCTIONS_SymbolDownloadAllSymbols_set)
    GetJitAuto = _swig_property(_x64dbgapi.DBGFUNCTIONS_GetJitAuto_get, _x64dbgapi.DBGFUNCTIONS_GetJitAuto_set)
    GetJit = _swig_property(_x64dbgapi.DBGFUNCTIONS_GetJit_get, _x64dbgapi.DBGFUNCTIONS_GetJit_set)
    GetDefJit = _swig_property(_x64dbgapi.DBGFUNCTIONS_GetDefJit_get, _x64dbgapi.DBGFUNCTIONS_GetDefJit_set)
    GetProcessList = _swig_property(_x64dbgapi.DBGFUNCTIONS_GetProcessList_get, _x64dbgapi.DBGFUNCTIONS_GetProcessList_set)
    GetPageRights = _swig_property(_x64dbgapi.DBGFUNCTIONS_GetPageRights_get, _x64dbgapi.DBGFUNCTIONS_GetPageRights_set)
    SetPageRights = _swig_property(_x64dbgapi.DBGFUNCTIONS_SetPageRights_get, _x64dbgapi.DBGFUNCTIONS_SetPageRights_set)
    PageRightsToString = _swig_property(_x64dbgapi.DBGFUNCTIONS_PageRightsToString_get, _x64dbgapi.DBGFUNCTIONS_PageRightsToString_set)
    IsProcessElevated = _swig_property(_x64dbgapi.DBGFUNCTIONS_IsProcessElevated_get, _x64dbgapi.DBGFUNCTIONS_IsProcessElevated_set)
    GetCmdline = _swig_property(_x64dbgapi.DBGFUNCTIONS_GetCmdline_get, _x64dbgapi.DBGFUNCTIONS_GetCmdline_set)
    SetCmdline = _swig_property(_x64dbgapi.DBGFUNCTIONS_SetCmdline_get, _x64dbgapi.DBGFUNCTIONS_SetCmdline_set)
    FileOffsetToVa = _swig_property(_x64dbgapi.DBGFUNCTIONS_FileOffsetToVa_get, _x64dbgapi.DBGFUNCTIONS_FileOffsetToVa_set)
    VaToFileOffset = _swig_property(_x64dbgapi.DBGFUNCTIONS_VaToFileOffset_get, _x64dbgapi.DBGFUNCTIONS_VaToFileOffset_set)
    GetAddrFromLine = _swig_property(_x64dbgapi.DBGFUNCTIONS_GetAddrFromLine_get, _x64dbgapi.DBGFUNCTIONS_GetAddrFromLine_set)
    GetSourceFromAddr = _swig_property(_x64dbgapi.DBGFUNCTIONS_GetSourceFromAddr_get, _x64dbgapi.DBGFUNCTIONS_GetSourceFromAddr_set)
    ValFromString = _swig_property(_x64dbgapi.DBGFUNCTIONS_ValFromString_get, _x64dbgapi.DBGFUNCTIONS_ValFromString_set)
    PatchGetEx = _swig_property(_x64dbgapi.DBGFUNCTIONS_PatchGetEx_get, _x64dbgapi.DBGFUNCTIONS_PatchGetEx_set)
    GetBridgeBp = _swig_property(_x64dbgapi.DBGFUNCTIONS_GetBridgeBp_get, _x64dbgapi.DBGFUNCTIONS_GetBridgeBp_set)
    StringFormatInline = _swig_property(_x64dbgapi.DBGFUNCTIONS_StringFormatInline_get, _x64dbgapi.DBGFUNCTIONS_StringFormatInline_set)
    GetMnemonicBrief = _swig_property(_x64dbgapi.DBGFUNCTIONS_GetMnemonicBrief_get, _x64dbgapi.DBGFUNCTIONS_GetMnemonicBrief_set)
    GetTraceRecordHitCount = _swig_property(_x64dbgapi.DBGFUNCTIONS_GetTraceRecordHitCount_get, _x64dbgapi.DBGFUNCTIONS_GetTraceRecordHitCount_set)
    GetTraceRecordByteType = _swig_property(_x64dbgapi.DBGFUNCTIONS_GetTraceRecordByteType_get, _x64dbgapi.DBGFUNCTIONS_GetTraceRecordByteType_set)
    SetTraceRecordType = _swig_property(_x64dbgapi.DBGFUNCTIONS_SetTraceRecordType_get, _x64dbgapi.DBGFUNCTIONS_SetTraceRecordType_set)
    GetTraceRecordType = _swig_property(_x64dbgapi.DBGFUNCTIONS_GetTraceRecordType_get, _x64dbgapi.DBGFUNCTIONS_GetTraceRecordType_set)
    EnumHandles = _swig_property(_x64dbgapi.DBGFUNCTIONS_EnumHandles_get, _x64dbgapi.DBGFUNCTIONS_EnumHandles_set)
    GetHandleName = _swig_property(_x64dbgapi.DBGFUNCTIONS_GetHandleName_get, _x64dbgapi.DBGFUNCTIONS_GetHandleName_set)
    EnumTcpConnections = _swig_property(_x64dbgapi.DBGFUNCTIONS_EnumTcpConnections_get, _x64dbgapi.DBGFUNCTIONS_EnumTcpConnections_set)
    GetDbgEvents = _swig_property(_x64dbgapi.DBGFUNCTIONS_GetDbgEvents_get, _x64dbgapi.DBGFUNCTIONS_GetDbgEvents_set)
    ModGetParty = _swig_property(_x64dbgapi.DBGFUNCTIONS_ModGetParty_get, _x64dbgapi.DBGFUNCTIONS_ModGetParty_set)
    ModSetParty = _swig_property(_x64dbgapi.DBGFUNCTIONS_ModSetParty_get, _x64dbgapi.DBGFUNCTIONS_ModSetParty_set)
    WatchIsWatchdogTriggered = _swig_property(_x64dbgapi.DBGFUNCTIONS_WatchIsWatchdogTriggered_get, _x64dbgapi.DBGFUNCTIONS_WatchIsWatchdogTriggered_set)
    MemIsCodePage = _swig_property(_x64dbgapi.DBGFUNCTIONS_MemIsCodePage_get, _x64dbgapi.DBGFUNCTIONS_MemIsCodePage_set)
    AnimateCommand = _swig_property(_x64dbgapi.DBGFUNCTIONS_AnimateCommand_get, _x64dbgapi.DBGFUNCTIONS_AnimateCommand_set)
    DbgSetDebuggeeInitScript = _swig_property(_x64dbgapi.DBGFUNCTIONS_DbgSetDebuggeeInitScript_get, _x64dbgapi.DBGFUNCTIONS_DbgSetDebuggeeInitScript_set)
    DbgGetDebuggeeInitScript = _swig_property(_x64dbgapi.DBGFUNCTIONS_DbgGetDebuggeeInitScript_get, _x64dbgapi.DBGFUNCTIONS_DbgGetDebuggeeInitScript_set)
    EnumWindows = _swig_property(_x64dbgapi.DBGFUNCTIONS_EnumWindows_get, _x64dbgapi.DBGFUNCTIONS_EnumWindows_set)
    EnumHeaps = _swig_property(_x64dbgapi.DBGFUNCTIONS_EnumHeaps_get, _x64dbgapi.DBGFUNCTIONS_EnumHeaps_set)
    ThreadGetName = _swig_property(_x64dbgapi.DBGFUNCTIONS_ThreadGetName_get, _x64dbgapi.DBGFUNCTIONS_ThreadGetName_set)
    IsDepEnabled = _swig_property(_x64dbgapi.DBGFUNCTIONS_IsDepEnabled_get, _x64dbgapi.DBGFUNCTIONS_IsDepEnabled_set)
    GetCallStackEx = _swig_property(_x64dbgapi.DBGFUNCTIONS_GetCallStackEx_get, _x64dbgapi.DBGFUNCTIONS_GetCallStackEx_set)
    GetUserComment = _swig_property(_x64dbgapi.DBGFUNCTIONS_GetUserComment_get, _x64dbgapi.DBGFUNCTIONS_GetUserComment_set)
    EnumConstants = _swig_property(_x64dbgapi.DBGFUNCTIONS_EnumConstants_get, _x64dbgapi.DBGFUNCTIONS_EnumConstants_set)
    EnumErrorCodes = _swig_property(_x64dbgapi.DBGFUNCTIONS_EnumErrorCodes_get, _x64dbgapi.DBGFUNCTIONS_EnumErrorCodes_set)
    EnumExceptions = _swig_property(_x64dbgapi.DBGFUNCTIONS_EnumExceptions_get, _x64dbgapi.DBGFUNCTIONS_EnumExceptions_set)
    MemBpSize = _swig_property(_x64dbgapi.DBGFUNCTIONS_MemBpSize_get, _x64dbgapi.DBGFUNCTIONS_MemBpSize_set)
    ModRelocationsFromAddr = _swig_property(_x64dbgapi.DBGFUNCTIONS_ModRelocationsFromAddr_get, _x64dbgapi.DBGFUNCTIONS_ModRelocationsFromAddr_set)
    ModRelocationAtAddr = _swig_property(_x64dbgapi.DBGFUNCTIONS_ModRelocationAtAddr_get, _x64dbgapi.DBGFUNCTIONS_ModRelocationAtAddr_set)
    ModRelocationsInRange = _swig_property(_x64dbgapi.DBGFUNCTIONS_ModRelocationsInRange_get, _x64dbgapi.DBGFUNCTIONS_ModRelocationsInRange_set)
    DbGetHash = _swig_property(_x64dbgapi.DBGFUNCTIONS_DbGetHash_get, _x64dbgapi.DBGFUNCTIONS_DbGetHash_set)
    SymAutoComplete = _swig_property(_x64dbgapi.DBGFUNCTIONS_SymAutoComplete_get, _x64dbgapi.DBGFUNCTIONS_SymAutoComplete_set)
    RefreshModuleList = _swig_property(_x64dbgapi.DBGFUNCTIONS_RefreshModuleList_get, _x64dbgapi.DBGFUNCTIONS_RefreshModuleList_set)
    GetAddrFromLineEx = _swig_property(_x64dbgapi.DBGFUNCTIONS_GetAddrFromLineEx_get, _x64dbgapi.DBGFUNCTIONS_GetAddrFromLineEx_set)
    def AssembleAtEx_(self, *args):
        """AssembleAtEx_(DBGFUNCTIONS self, duint addr, char const * instruction, char * error, bool fillnop) -> bool"""
        return _x64dbgapi.DBGFUNCTIONS_AssembleAtEx_(self, *args)

    def SectionFromAddr_(self, *args):
        """SectionFromAddr_(DBGFUNCTIONS self, duint addr, char * section) -> bool"""
        return _x64dbgapi.DBGFUNCTIONS_SectionFromAddr_(self, *args)

    def ModNameFromAddr_(self, *args):
        """ModNameFromAddr_(DBGFUNCTIONS self, duint addr, char * modname, bool extension) -> bool"""
        return _x64dbgapi.DBGFUNCTIONS_ModNameFromAddr_(self, *args)

    def ModBaseFromAddr_(self, *args):
        """ModBaseFromAddr_(DBGFUNCTIONS self, duint addr) -> duint"""
        return _x64dbgapi.DBGFUNCTIONS_ModBaseFromAddr_(self, *args)

    def ModBaseFromName_(self, *args):
        """ModBaseFromName_(DBGFUNCTIONS self, char const * modname) -> duint"""
        return _x64dbgapi.DBGFUNCTIONS_ModBaseFromName_(self, *args)

    def ModSizeFromAddr_(self, *args):
        """ModSizeFromAddr_(DBGFUNCTIONS self, duint addr) -> duint"""
        return _x64dbgapi.DBGFUNCTIONS_ModSizeFromAddr_(self, *args)

    def Assemble_(self, *args):
        """Assemble_(DBGFUNCTIONS self, duint addr, unsigned char * dest, int * size, char const * instruction, char * error) -> bool"""
        return _x64dbgapi.DBGFUNCTIONS_Assemble_(self, *args)

    def PatchGet_(self, *args):
        """PatchGet_(DBGFUNCTIONS self, duint addr) -> bool"""
        return _x64dbgapi.DBGFUNCTIONS_PatchGet_(self, *args)

    def PatchInRange_(self, *args):
        """PatchInRange_(DBGFUNCTIONS self, duint start, duint end) -> bool"""
        return _x64dbgapi.DBGFUNCTIONS_PatchInRange_(self, *args)

    def MemPatch_(self, *args):
        """MemPatch_(DBGFUNCTIONS self, duint va, unsigned char const * src, duint size) -> bool"""
        return _x64dbgapi.DBGFUNCTIONS_MemPatch_(self, *args)

    def PatchRestoreRange_(self, *args):
        """PatchRestoreRange_(DBGFUNCTIONS self, duint start, duint end)"""
        return _x64dbgapi.DBGFUNCTIONS_PatchRestoreRange_(self, *args)

    def PatchEnum_(self, *args):
        """PatchEnum_(DBGFUNCTIONS self, DBGPATCHINFO patchlist, size_t * cbsize) -> bool"""
        return _x64dbgapi.DBGFUNCTIONS_PatchEnum_(self, *args)

    def PatchRestore_(self, *args):
        """PatchRestore_(DBGFUNCTIONS self, duint addr) -> bool"""
        return _x64dbgapi.DBGFUNCTIONS_PatchRestore_(self, *args)

    def PatchFile_(self, *args):
        """PatchFile_(DBGFUNCTIONS self, DBGPATCHINFO patchlist, int count, char const * szFileName, char * error) -> int"""
        return _x64dbgapi.DBGFUNCTIONS_PatchFile_(self, *args)

    def ModPathFromAddr_(self, *args):
        """ModPathFromAddr_(DBGFUNCTIONS self, duint addr, char * path, int size) -> int"""
        return _x64dbgapi.DBGFUNCTIONS_ModPathFromAddr_(self, *args)

    def ModPathFromName_(self, *args):
        """ModPathFromName_(DBGFUNCTIONS self, char const * modname, char * path, int size) -> int"""
        return _x64dbgapi.DBGFUNCTIONS_ModPathFromName_(self, *args)

    def DisasmFast_(self, *args):
        """DisasmFast_(DBGFUNCTIONS self, unsigned char const * data, duint addr, BASIC_INSTRUCTION_INFO basicinfo) -> bool"""
        return _x64dbgapi.DBGFUNCTIONS_DisasmFast_(self, *args)

    def MemUpdateMap_(self):
        """MemUpdateMap_(DBGFUNCTIONS self)"""
        return _x64dbgapi.DBGFUNCTIONS_MemUpdateMap_(self)

    def GetCallStack_(self, *args):
        """GetCallStack_(DBGFUNCTIONS self, DBGCALLSTACK callstack)"""
        return _x64dbgapi.DBGFUNCTIONS_GetCallStack_(self, *args)

    def SymbolDownloadAllSymbols_(self, *args):
        """SymbolDownloadAllSymbols_(DBGFUNCTIONS self, char const * szSymbolStore)"""
        return _x64dbgapi.DBGFUNCTIONS_SymbolDownloadAllSymbols_(self, *args)

    def GetJit_(self, *args):
        """GetJit_(DBGFUNCTIONS self, char * jit, bool x64) -> bool"""
        return _x64dbgapi.DBGFUNCTIONS_GetJit_(self, *args)

    def GetJitAuto_(self, *args):
        """GetJitAuto_(DBGFUNCTIONS self, bool * jitauto) -> bool"""
        return _x64dbgapi.DBGFUNCTIONS_GetJitAuto_(self, *args)

    def GetDefJit_(self, *args):
        """GetDefJit_(DBGFUNCTIONS self, char * defjit) -> bool"""
        return _x64dbgapi.DBGFUNCTIONS_GetDefJit_(self, *args)

    def GetProcessList_(self, *args):
        """GetProcessList_(DBGFUNCTIONS self, DBGPROCESSINFO ** entries, int * count) -> bool"""
        return _x64dbgapi.DBGFUNCTIONS_GetProcessList_(self, *args)

    def GetPageRights_(self, *args):
        """GetPageRights_(DBGFUNCTIONS self, duint addr, char * rights) -> bool"""
        return _x64dbgapi.DBGFUNCTIONS_GetPageRights_(self, *args)

    def SetPageRights_(self, *args):
        """SetPageRights_(DBGFUNCTIONS self, duint addr, char const * rights) -> bool"""
        return _x64dbgapi.DBGFUNCTIONS_SetPageRights_(self, *args)

    def PageRightsToString_(self, *args):
        """PageRightsToString_(DBGFUNCTIONS self, DWORD protect, char * rights) -> bool"""
        return _x64dbgapi.DBGFUNCTIONS_PageRightsToString_(self, *args)

    def IsProcessElevated_(self):
        """IsProcessElevated_(DBGFUNCTIONS self) -> bool"""
        return _x64dbgapi.DBGFUNCTIONS_IsProcessElevated_(self)

    def GetCmdline_(self, *args):
        """GetCmdline_(DBGFUNCTIONS self, char * cmdline, size_t * cbsize) -> bool"""
        return _x64dbgapi.DBGFUNCTIONS_GetCmdline_(self, *args)

    def SetCmdline_(self, *args):
        """SetCmdline_(DBGFUNCTIONS self, char const * cmdline) -> bool"""
        return _x64dbgapi.DBGFUNCTIONS_SetCmdline_(self, *args)

    def FileOffsetToVa_(self, *args):
        """FileOffsetToVa_(DBGFUNCTIONS self, char const * modname, duint offset) -> duint"""
        return _x64dbgapi.DBGFUNCTIONS_FileOffsetToVa_(self, *args)

    def VaToFileOffset_(self, *args):
        """VaToFileOffset_(DBGFUNCTIONS self, duint va) -> duint"""
        return _x64dbgapi.DBGFUNCTIONS_VaToFileOffset_(self, *args)

    def GetAddrFromLine_(self, *args):
        """GetAddrFromLine_(DBGFUNCTIONS self, char const * szSourceFile, int line, duint * displacement) -> duint"""
        return _x64dbgapi.DBGFUNCTIONS_GetAddrFromLine_(self, *args)

    def GetSourceFromAddr_(self, *args):
        """GetSourceFromAddr_(DBGFUNCTIONS self, duint addr, char * szSourceFile, int * line) -> bool"""
        return _x64dbgapi.DBGFUNCTIONS_GetSourceFromAddr_(self, *args)

    def ValFromString_(self, *args):
        """ValFromString_(DBGFUNCTIONS self, char const * string, duint * value) -> bool"""
        return _x64dbgapi.DBGFUNCTIONS_ValFromString_(self, *args)

    def PatchGetEx_(self, *args):
        """PatchGetEx_(DBGFUNCTIONS self, duint addr, DBGPATCHINFO info) -> bool"""
        return _x64dbgapi.DBGFUNCTIONS_PatchGetEx_(self, *args)

    def GetBridgeBp_(self, *args):
        """GetBridgeBp_(DBGFUNCTIONS self, BPXTYPE type, duint addr, BRIDGEBP bp) -> bool"""
        return _x64dbgapi.DBGFUNCTIONS_GetBridgeBp_(self, *args)

    def StringFormatInline_(self, *args):
        """StringFormatInline_(DBGFUNCTIONS self, char const * format, size_t resultSize, char * result) -> bool"""
        return _x64dbgapi.DBGFUNCTIONS_StringFormatInline_(self, *args)

    def GetMnemonicBrief_(self, *args):
        """GetMnemonicBrief_(DBGFUNCTIONS self, char const * mnem, size_t resultSize, char * result)"""
        return _x64dbgapi.DBGFUNCTIONS_GetMnemonicBrief_(self, *args)

    def GetTraceRecordHitCount_(self, *args):
        """GetTraceRecordHitCount_(DBGFUNCTIONS self, duint address) -> unsigned int"""
        return _x64dbgapi.DBGFUNCTIONS_GetTraceRecordHitCount_(self, *args)

    def GetTraceRecordByteType_(self, *args):
        """GetTraceRecordByteType_(DBGFUNCTIONS self, duint address) -> TRACERECORDBYTETYPE"""
        return _x64dbgapi.DBGFUNCTIONS_GetTraceRecordByteType_(self, *args)

    def SetTraceRecordType_(self, *args):
        """SetTraceRecordType_(DBGFUNCTIONS self, duint pageAddress, TRACERECORDTYPE type) -> bool"""
        return _x64dbgapi.DBGFUNCTIONS_SetTraceRecordType_(self, *args)

    def GetTraceRecordType_(self, *args):
        """GetTraceRecordType_(DBGFUNCTIONS self, duint pageAddress) -> TRACERECORDTYPE"""
        return _x64dbgapi.DBGFUNCTIONS_GetTraceRecordType_(self, *args)

    def EnumHandles_(self, *args):
        """EnumHandles_(DBGFUNCTIONS self, ListInfo handles) -> bool"""
        return _x64dbgapi.DBGFUNCTIONS_EnumHandles_(self, *args)

    def GetHandleName_(self, *args):
        """GetHandleName_(DBGFUNCTIONS self, duint handle, char * name, size_t nameSize, char * typeName, size_t typeNameSize) -> bool"""
        return _x64dbgapi.DBGFUNCTIONS_GetHandleName_(self, *args)

    def EnumTcpConnections_(self, *args):
        """EnumTcpConnections_(DBGFUNCTIONS self, ListInfo connections) -> bool"""
        return _x64dbgapi.DBGFUNCTIONS_EnumTcpConnections_(self, *args)

    def GetDbgEvents_(self):
        """GetDbgEvents_(DBGFUNCTIONS self) -> duint"""
        return _x64dbgapi.DBGFUNCTIONS_GetDbgEvents_(self)

    def ModGetParty_(self, *args):
        """ModGetParty_(DBGFUNCTIONS self, duint base) -> int"""
        return _x64dbgapi.DBGFUNCTIONS_ModGetParty_(self, *args)

    def ModSetParty_(self, *args):
        """ModSetParty_(DBGFUNCTIONS self, duint base, int party)"""
        return _x64dbgapi.DBGFUNCTIONS_ModSetParty_(self, *args)

    def WatchIsWatchdogTriggered_(self, *args):
        """WatchIsWatchdogTriggered_(DBGFUNCTIONS self, unsigned int id) -> bool"""
        return _x64dbgapi.DBGFUNCTIONS_WatchIsWatchdogTriggered_(self, *args)

    def MemIsCodePage_(self, *args):
        """MemIsCodePage_(DBGFUNCTIONS self, duint addr, bool refresh) -> bool"""
        return _x64dbgapi.DBGFUNCTIONS_MemIsCodePage_(self, *args)

    def AnimateCommand_(self, *args):
        """AnimateCommand_(DBGFUNCTIONS self, char const * command) -> bool"""
        return _x64dbgapi.DBGFUNCTIONS_AnimateCommand_(self, *args)

    def DbgSetDebuggeeInitScript_(self, *args):
        """DbgSetDebuggeeInitScript_(DBGFUNCTIONS self, char const * fileName)"""
        return _x64dbgapi.DBGFUNCTIONS_DbgSetDebuggeeInitScript_(self, *args)

    def DbgGetDebuggeeInitScript_(self):
        """DbgGetDebuggeeInitScript_(DBGFUNCTIONS self) -> char const *"""
        return _x64dbgapi.DBGFUNCTIONS_DbgGetDebuggeeInitScript_(self)

    def EnumWindows_(self, *args):
        """EnumWindows_(DBGFUNCTIONS self, ListInfo windows) -> bool"""
        return _x64dbgapi.DBGFUNCTIONS_EnumWindows_(self, *args)

    def EnumHeaps_(self, *args):
        """EnumHeaps_(DBGFUNCTIONS self, ListInfo heaps) -> bool"""
        return _x64dbgapi.DBGFUNCTIONS_EnumHeaps_(self, *args)

    def ThreadGetName_(self, *args):
        """ThreadGetName_(DBGFUNCTIONS self, DWORD tid, char * name) -> bool"""
        return _x64dbgapi.DBGFUNCTIONS_ThreadGetName_(self, *args)

    def IsDepEnabled_(self):
        """IsDepEnabled_(DBGFUNCTIONS self) -> bool"""
        return _x64dbgapi.DBGFUNCTIONS_IsDepEnabled_(self)

    def GetCallStackEx_(self, *args):
        """GetCallStackEx_(DBGFUNCTIONS self, DBGCALLSTACK callstack, bool cache)"""
        return _x64dbgapi.DBGFUNCTIONS_GetCallStackEx_(self, *args)

    def GetUserComment_(self, *args):
        """GetUserComment_(DBGFUNCTIONS self, duint addr, char * comment) -> bool"""
        return _x64dbgapi.DBGFUNCTIONS_GetUserComment_(self, *args)

    def EnumConstants_(self, *args):
        """EnumConstants_(DBGFUNCTIONS self, ListInfo constants)"""
        return _x64dbgapi.DBGFUNCTIONS_EnumConstants_(self, *args)

    def EnumErrorCodes_(self, *args):
        """EnumErrorCodes_(DBGFUNCTIONS self, ListInfo constants)"""
        return _x64dbgapi.DBGFUNCTIONS_EnumErrorCodes_(self, *args)

    def EnumExceptions_(self, *args):
        """EnumExceptions_(DBGFUNCTIONS self, ListInfo constants)"""
        return _x64dbgapi.DBGFUNCTIONS_EnumExceptions_(self, *args)

    def MemBpSize_(self, *args):
        """MemBpSize_(DBGFUNCTIONS self, duint addr) -> duint"""
        return _x64dbgapi.DBGFUNCTIONS_MemBpSize_(self, *args)

    def ModRelocationsFromAddr_(self, *args):
        """ModRelocationsFromAddr_(DBGFUNCTIONS self, duint addr, ListInfo relocations) -> bool"""
        return _x64dbgapi.DBGFUNCTIONS_ModRelocationsFromAddr_(self, *args)

    def ModRelocationAtAddr_(self, *args):
        """ModRelocationAtAddr_(DBGFUNCTIONS self, duint addr, DBGRELOCATIONINFO relocation) -> bool"""
        return _x64dbgapi.DBGFUNCTIONS_ModRelocationAtAddr_(self, *args)

    def ModRelocationsInRange_(self, *args):
        """ModRelocationsInRange_(DBGFUNCTIONS self, duint addr, duint size, ListInfo relocations) -> bool"""
        return _x64dbgapi.DBGFUNCTIONS_ModRelocationsInRange_(self, *args)

    def DbGetHash_(self):
        """DbGetHash_(DBGFUNCTIONS self) -> duint"""
        return _x64dbgapi.DBGFUNCTIONS_DbGetHash_(self)

    def SymAutoComplete_(self, *args):
        """SymAutoComplete_(DBGFUNCTIONS self, char const * Search, char ** Buffer, int MaxSymbols) -> int"""
        return _x64dbgapi.DBGFUNCTIONS_SymAutoComplete_(self, *args)

    def RefreshModuleList_(self):
        """RefreshModuleList_(DBGFUNCTIONS self)"""
        return _x64dbgapi.DBGFUNCTIONS_RefreshModuleList_(self)

    def GetAddrFromLineEx_(self, *args):
        """GetAddrFromLineEx_(DBGFUNCTIONS self, duint mod, char const * szSourceFile, int line) -> duint"""
        return _x64dbgapi.DBGFUNCTIONS_GetAddrFromLineEx_(self, *args)

    def __init__(self): 
        """__init__(DBGFUNCTIONS_ self) -> DBGFUNCTIONS"""
        this = _x64dbgapi.new_DBGFUNCTIONS()
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _x64dbgapi.delete_DBGFUNCTIONS
    __del__ = lambda self : None;
DBGFUNCTIONS_swigregister = _x64dbgapi.DBGFUNCTIONS_swigregister
DBGFUNCTIONS_swigregister(DBGFUNCTIONS)


def _plugin_logprintf(*args):
  """_plugin_logprintf(char const * format)"""
  return _x64dbgapi._plugin_logprintf(*args)
class ArgumentInfo(object):
    """Proxy of C++ Script::Argument::ArgumentInfo class"""
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    mod = _swig_property(_x64dbgapi.ArgumentInfo_mod_get, _x64dbgapi.ArgumentInfo_mod_set)
    rvaStart = _swig_property(_x64dbgapi.ArgumentInfo_rvaStart_get, _x64dbgapi.ArgumentInfo_rvaStart_set)
    rvaEnd = _swig_property(_x64dbgapi.ArgumentInfo_rvaEnd_get, _x64dbgapi.ArgumentInfo_rvaEnd_set)
    manual = _swig_property(_x64dbgapi.ArgumentInfo_manual_get, _x64dbgapi.ArgumentInfo_manual_set)
    instructioncount = _swig_property(_x64dbgapi.ArgumentInfo_instructioncount_get, _x64dbgapi.ArgumentInfo_instructioncount_set)
    def __init__(self): 
        """__init__(Script::Argument::ArgumentInfo self) -> ArgumentInfo"""
        this = _x64dbgapi.new_ArgumentInfo()
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _x64dbgapi.delete_ArgumentInfo
    __del__ = lambda self : None;
ArgumentInfo_swigregister = _x64dbgapi.ArgumentInfo_swigregister
ArgumentInfo_swigregister(ArgumentInfo)


def Argument_Add(*args):
  """
    Argument_Add(duint start, duint end, bool manual, duint instructionCount=0) -> bool
    Argument_Add(duint start, duint end, bool manual) -> bool
    """
  return _x64dbgapi.Argument_Add(*args)

def Argument_AddByArgumentInfo(*args):
  """Argument_AddByArgumentInfo(ArgumentInfo info) -> bool"""
  return _x64dbgapi.Argument_AddByArgumentInfo(*args)

def Argument_Get(*args):
  """
    Argument_Get(duint addr, duint * start=None, duint * end=None, duint * instructionCount=None) -> bool
    Argument_Get(duint addr, duint * start=None, duint * end=None) -> bool
    Argument_Get(duint addr, duint * start=None) -> bool
    Argument_Get(duint addr) -> bool
    """
  return _x64dbgapi.Argument_Get(*args)

def Argument_GetInfo(*args):
  """Argument_GetInfo(duint addr, ArgumentInfo info) -> bool"""
  return _x64dbgapi.Argument_GetInfo(*args)

def Argument_Overlaps(*args):
  """Argument_Overlaps(duint start, duint end) -> bool"""
  return _x64dbgapi.Argument_Overlaps(*args)

def Argument_Delete(*args):
  """Argument_Delete(duint address) -> bool"""
  return _x64dbgapi.Argument_Delete(*args)

def Argument_DeleteRange(*args):
  """
    Argument_DeleteRange(duint start, duint end, bool deleteManual=False)
    Argument_DeleteRange(duint start, duint end)
    """
  return _x64dbgapi.Argument_DeleteRange(*args)

def Argument_Clear():
  """Argument_Clear()"""
  return _x64dbgapi.Argument_Clear()

def Argument_GetList(*args):
  """Argument_GetList(ListInfo list) -> bool"""
  return _x64dbgapi.Argument_GetList(*args)

def Assembler_Assemble(*args):
  """Assembler_Assemble(duint addr, unsigned char * dest, int * size, char const * instruction) -> bool"""
  return _x64dbgapi.Assembler_Assemble(*args)

def Assembler_AssembleEx(*args):
  """Assembler_AssembleEx(duint addr, unsigned char * dest, int * size, char const * instruction, char * error) -> bool"""
  return _x64dbgapi.Assembler_AssembleEx(*args)

def Assembler_AssembleMem(*args):
  """Assembler_AssembleMem(duint addr, char const * instruction) -> bool"""
  return _x64dbgapi.Assembler_AssembleMem(*args)

def Assembler_AssembleMemEx(*args):
  """Assembler_AssembleMemEx(duint addr, char const * instruction, int * size, char * error, bool fillnop) -> bool"""
  return _x64dbgapi.Assembler_AssembleMemEx(*args)
class BookmarkInfo(object):
    """Proxy of C++ Script::Bookmark::BookmarkInfo class"""
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    mod = _swig_property(_x64dbgapi.BookmarkInfo_mod_get, _x64dbgapi.BookmarkInfo_mod_set)
    rva = _swig_property(_x64dbgapi.BookmarkInfo_rva_get, _x64dbgapi.BookmarkInfo_rva_set)
    manual = _swig_property(_x64dbgapi.BookmarkInfo_manual_get, _x64dbgapi.BookmarkInfo_manual_set)
    def __init__(self): 
        """__init__(Script::Bookmark::BookmarkInfo self) -> BookmarkInfo"""
        this = _x64dbgapi.new_BookmarkInfo()
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _x64dbgapi.delete_BookmarkInfo
    __del__ = lambda self : None;
BookmarkInfo_swigregister = _x64dbgapi.BookmarkInfo_swigregister
BookmarkInfo_swigregister(BookmarkInfo)


def Bookmark_Set(*args):
  """
    Bookmark_Set(duint addr, bool manual=False) -> bool
    Bookmark_Set(duint addr) -> bool
    """
  return _x64dbgapi.Bookmark_Set(*args)

def Bookmark_SetByBookmarkInfo(*args):
  """Bookmark_SetByBookmarkInfo(BookmarkInfo info) -> bool"""
  return _x64dbgapi.Bookmark_SetByBookmarkInfo(*args)

def Bookmark_Get(*args):
  """Bookmark_Get(duint addr) -> bool"""
  return _x64dbgapi.Bookmark_Get(*args)

def Bookmark_GetInfo(*args):
  """Bookmark_GetInfo(duint addr, BookmarkInfo info) -> bool"""
  return _x64dbgapi.Bookmark_GetInfo(*args)

def Bookmark_Delete(*args):
  """Bookmark_Delete(duint addr) -> bool"""
  return _x64dbgapi.Bookmark_Delete(*args)

def Bookmark_DeleteRange(*args):
  """Bookmark_DeleteRange(duint start, duint end)"""
  return _x64dbgapi.Bookmark_DeleteRange(*args)

def Bookmark_Clear():
  """Bookmark_Clear()"""
  return _x64dbgapi.Bookmark_Clear()

def Bookmark_GetList(*args):
  """Bookmark_GetList(ListInfo list) -> bool"""
  return _x64dbgapi.Bookmark_GetList(*args)
class CommentInfo(object):
    """Proxy of C++ Script::Comment::CommentInfo class"""
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    mod = _swig_property(_x64dbgapi.CommentInfo_mod_get, _x64dbgapi.CommentInfo_mod_set)
    rva = _swig_property(_x64dbgapi.CommentInfo_rva_get, _x64dbgapi.CommentInfo_rva_set)
    text = _swig_property(_x64dbgapi.CommentInfo_text_get, _x64dbgapi.CommentInfo_text_set)
    manual = _swig_property(_x64dbgapi.CommentInfo_manual_get, _x64dbgapi.CommentInfo_manual_set)
    def __init__(self): 
        """__init__(Script::Comment::CommentInfo self) -> CommentInfo"""
        this = _x64dbgapi.new_CommentInfo()
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _x64dbgapi.delete_CommentInfo
    __del__ = lambda self : None;
CommentInfo_swigregister = _x64dbgapi.CommentInfo_swigregister
CommentInfo_swigregister(CommentInfo)


def Comment_Set(*args):
  """
    Comment_Set(duint addr, char const * text, bool manual=False) -> bool
    Comment_Set(duint addr, char const * text) -> bool
    """
  return _x64dbgapi.Comment_Set(*args)

def Comment_ByCommentInfo(*args):
  """Comment_ByCommentInfo(CommentInfo info) -> bool"""
  return _x64dbgapi.Comment_ByCommentInfo(*args)

def Comment_Get(*args):
  """Comment_Get(duint addr, char * text) -> bool"""
  return _x64dbgapi.Comment_Get(*args)

def Comment_GetInfo(*args):
  """Comment_GetInfo(duint addr, CommentInfo info) -> bool"""
  return _x64dbgapi.Comment_GetInfo(*args)

def Comment_Delete(*args):
  """Comment_Delete(duint addr) -> bool"""
  return _x64dbgapi.Comment_Delete(*args)

def Comment_DeleteRange(*args):
  """Comment_DeleteRange(duint start, duint end)"""
  return _x64dbgapi.Comment_DeleteRange(*args)

def Comment_Clear():
  """Comment_Clear()"""
  return _x64dbgapi.Comment_Clear()

def Comment_GetList(*args):
  """Comment_GetList(ListInfo list) -> bool"""
  return _x64dbgapi.Comment_GetList(*args)
HardwareAccess = _x64dbgapi.HardwareAccess
HardwareWrite = _x64dbgapi.HardwareWrite
HardwareExecute = _x64dbgapi.HardwareExecute

def Debug_Wait():
  """Debug_Wait()"""
  return _x64dbgapi.Debug_Wait()

def Debug_Run():
  """Debug_Run()"""
  return _x64dbgapi.Debug_Run()

def Debug_Pause():
  """Debug_Pause()"""
  return _x64dbgapi.Debug_Pause()

def Debug_Stop():
  """Debug_Stop()"""
  return _x64dbgapi.Debug_Stop()

def Debug_StepIn():
  """Debug_StepIn()"""
  return _x64dbgapi.Debug_StepIn()

def Debug_StepOver():
  """Debug_StepOver()"""
  return _x64dbgapi.Debug_StepOver()

def Debug_StepOut():
  """Debug_StepOut()"""
  return _x64dbgapi.Debug_StepOut()

def Debug_SetBreakpoint(*args):
  """Debug_SetBreakpoint(duint address) -> bool"""
  return _x64dbgapi.Debug_SetBreakpoint(*args)

def Debug_DeleteBreakpoint(*args):
  """Debug_DeleteBreakpoint(duint address) -> bool"""
  return _x64dbgapi.Debug_DeleteBreakpoint(*args)

def Debug_DisableBreakpoint(*args):
  """Debug_DisableBreakpoint(duint address) -> bool"""
  return _x64dbgapi.Debug_DisableBreakpoint(*args)

def Debug_SetHardwareBreakpoint(*args):
  """
    Debug_SetHardwareBreakpoint(duint address, Script::Debug::HardwareType type=HardwareExecute) -> bool
    Debug_SetHardwareBreakpoint(duint address) -> bool
    """
  return _x64dbgapi.Debug_SetHardwareBreakpoint(*args)

def Debug_DeleteHardwareBreakpoint(*args):
  """Debug_DeleteHardwareBreakpoint(duint address) -> bool"""
  return _x64dbgapi.Debug_DeleteHardwareBreakpoint(*args)
ZF = _x64dbgapi.ZF
OF = _x64dbgapi.OF
CF = _x64dbgapi.CF
PF = _x64dbgapi.PF
SF = _x64dbgapi.SF
TF = _x64dbgapi.TF
AF = _x64dbgapi.AF
DF = _x64dbgapi.DF
IF = _x64dbgapi.IF

def Flag_Get(*args):
  """Flag_Get(Script::Flag::FlagEnum flag) -> bool"""
  return _x64dbgapi.Flag_Get(*args)

def Flag_Set(*args):
  """Flag_Set(Script::Flag::FlagEnum flag, bool value) -> bool"""
  return _x64dbgapi.Flag_Set(*args)

def Flag_GetZF():
  """Flag_GetZF() -> bool"""
  return _x64dbgapi.Flag_GetZF()

def Flag_SetZF(*args):
  """Flag_SetZF(bool value) -> bool"""
  return _x64dbgapi.Flag_SetZF(*args)

def Flag_GetOF():
  """Flag_GetOF() -> bool"""
  return _x64dbgapi.Flag_GetOF()

def Flag_SetOF(*args):
  """Flag_SetOF(bool value) -> bool"""
  return _x64dbgapi.Flag_SetOF(*args)

def Flag_GetCF():
  """Flag_GetCF() -> bool"""
  return _x64dbgapi.Flag_GetCF()

def Flag_SetCF(*args):
  """Flag_SetCF(bool value) -> bool"""
  return _x64dbgapi.Flag_SetCF(*args)

def Flag_GetPF():
  """Flag_GetPF() -> bool"""
  return _x64dbgapi.Flag_GetPF()

def Flag_SetPF(*args):
  """Flag_SetPF(bool value) -> bool"""
  return _x64dbgapi.Flag_SetPF(*args)

def Flag_GetSF():
  """Flag_GetSF() -> bool"""
  return _x64dbgapi.Flag_GetSF()

def Flag_SetSF(*args):
  """Flag_SetSF(bool value) -> bool"""
  return _x64dbgapi.Flag_SetSF(*args)

def Flag_GetTF():
  """Flag_GetTF() -> bool"""
  return _x64dbgapi.Flag_GetTF()

def Flag_SetTF(*args):
  """Flag_SetTF(bool value) -> bool"""
  return _x64dbgapi.Flag_SetTF(*args)

def Flag_GetAF():
  """Flag_GetAF() -> bool"""
  return _x64dbgapi.Flag_GetAF()

def Flag_SetAF(*args):
  """Flag_SetAF(bool value) -> bool"""
  return _x64dbgapi.Flag_SetAF(*args)

def Flag_GetDF():
  """Flag_GetDF() -> bool"""
  return _x64dbgapi.Flag_GetDF()

def Flag_SetDF(*args):
  """Flag_SetDF(bool value) -> bool"""
  return _x64dbgapi.Flag_SetDF(*args)

def Flag_GetIF():
  """Flag_GetIF() -> bool"""
  return _x64dbgapi.Flag_GetIF()

def Flag_SetIF(*args):
  """Flag_SetIF(bool value) -> bool"""
  return _x64dbgapi.Flag_SetIF(*args)
class FunctionInfo(object):
    """Proxy of C++ Script::Function::FunctionInfo class"""
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    mod = _swig_property(_x64dbgapi.FunctionInfo_mod_get, _x64dbgapi.FunctionInfo_mod_set)
    rvaStart = _swig_property(_x64dbgapi.FunctionInfo_rvaStart_get, _x64dbgapi.FunctionInfo_rvaStart_set)
    rvaEnd = _swig_property(_x64dbgapi.FunctionInfo_rvaEnd_get, _x64dbgapi.FunctionInfo_rvaEnd_set)
    manual = _swig_property(_x64dbgapi.FunctionInfo_manual_get, _x64dbgapi.FunctionInfo_manual_set)
    instructioncount = _swig_property(_x64dbgapi.FunctionInfo_instructioncount_get, _x64dbgapi.FunctionInfo_instructioncount_set)
    def __init__(self): 
        """__init__(Script::Function::FunctionInfo self) -> FunctionInfo"""
        this = _x64dbgapi.new_FunctionInfo()
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _x64dbgapi.delete_FunctionInfo
    __del__ = lambda self : None;
FunctionInfo_swigregister = _x64dbgapi.FunctionInfo_swigregister
FunctionInfo_swigregister(FunctionInfo)


def Function_Add(*args):
  """
    Function_Add(duint start, duint end, bool manual, duint instructionCount=0) -> bool
    Function_Add(duint start, duint end, bool manual) -> bool
    """
  return _x64dbgapi.Function_Add(*args)

def Function_AddByFuncInfo(*args):
  """Function_AddByFuncInfo(FunctionInfo info) -> bool"""
  return _x64dbgapi.Function_AddByFuncInfo(*args)

def Function_Get(*args):
  """
    Function_Get(duint addr, duint * start=None, duint * end=None, duint * instructionCount=None) -> bool
    Function_Get(duint addr, duint * start=None, duint * end=None) -> bool
    Function_Get(duint addr, duint * start=None) -> bool
    Function_Get(duint addr) -> bool
    """
  return _x64dbgapi.Function_Get(*args)

def Function_GetInfo(*args):
  """Function_GetInfo(duint addr, FunctionInfo info) -> bool"""
  return _x64dbgapi.Function_GetInfo(*args)

def Function_Overlaps(*args):
  """Function_Overlaps(duint start, duint end) -> bool"""
  return _x64dbgapi.Function_Overlaps(*args)

def Function_Delete(*args):
  """Function_Delete(duint address) -> bool"""
  return _x64dbgapi.Function_Delete(*args)

def Function_DeleteRange(*args):
  """Function_DeleteRange(duint start, duint end, bool deleteManual)"""
  return _x64dbgapi.Function_DeleteRange(*args)

def Function_DeleteRangeAuto(*args):
  """Function_DeleteRangeAuto(duint start, duint end)"""
  return _x64dbgapi.Function_DeleteRangeAuto(*args)

def Function_Clear():
  """Function_Clear()"""
  return _x64dbgapi.Function_Clear()

def Function_GetList(*args):
  """Function_GetList(ListInfo list) -> bool"""
  return _x64dbgapi.Function_GetList(*args)

def Gui_Disassembly_SelectionGet(*args):
  """Gui_Disassembly_SelectionGet(duint * start, duint * end) -> bool"""
  return _x64dbgapi.Gui_Disassembly_SelectionGet(*args)

def Gui_Disassembly_SelectionSet(*args):
  """Gui_Disassembly_SelectionSet(duint start, duint end) -> bool"""
  return _x64dbgapi.Gui_Disassembly_SelectionSet(*args)

def Gui_Disassembly_SelectionGetStart():
  """Gui_Disassembly_SelectionGetStart() -> duint"""
  return _x64dbgapi.Gui_Disassembly_SelectionGetStart()

def Gui_Disassembly_SelectionGetEnd():
  """Gui_Disassembly_SelectionGetEnd() -> duint"""
  return _x64dbgapi.Gui_Disassembly_SelectionGetEnd()

def Gui_Dump_SelectionGet(*args):
  """Gui_Dump_SelectionGet(duint * start, duint * end) -> bool"""
  return _x64dbgapi.Gui_Dump_SelectionGet(*args)

def Gui_Dump_SelectionSet(*args):
  """Gui_Dump_SelectionSet(duint start, duint end) -> bool"""
  return _x64dbgapi.Gui_Dump_SelectionSet(*args)

def Gui_Dump_SelectionGetStart():
  """Gui_Dump_SelectionGetStart() -> duint"""
  return _x64dbgapi.Gui_Dump_SelectionGetStart()

def Gui_Dump_SelectionGetEnd():
  """Gui_Dump_SelectionGetEnd() -> duint"""
  return _x64dbgapi.Gui_Dump_SelectionGetEnd()

def Gui_Stack_SelectionGet(*args):
  """Gui_Stack_SelectionGet(duint * start, duint * end) -> bool"""
  return _x64dbgapi.Gui_Stack_SelectionGet(*args)

def Gui_Stack_SelectionSet(*args):
  """Gui_Stack_SelectionSet(duint start, duint end) -> bool"""
  return _x64dbgapi.Gui_Stack_SelectionSet(*args)

def Gui_Stack_SelectionGetStart():
  """Gui_Stack_SelectionGetStart() -> duint"""
  return _x64dbgapi.Gui_Stack_SelectionGetStart()

def Gui_Stack_SelectionGetEnd():
  """Gui_Stack_SelectionGetEnd() -> duint"""
  return _x64dbgapi.Gui_Stack_SelectionGetEnd()

def Gui_Graph_SelectionGetStart():
  """Gui_Graph_SelectionGetStart() -> duint"""
  return _x64dbgapi.Gui_Graph_SelectionGetStart()

def Gui_MemMap_SelectionGetStart():
  """Gui_MemMap_SelectionGetStart() -> duint"""
  return _x64dbgapi.Gui_MemMap_SelectionGetStart()

def Gui_SymMod_SelectionGetStart():
  """Gui_SymMod_SelectionGetStart() -> duint"""
  return _x64dbgapi.Gui_SymMod_SelectionGetStart()
DisassemblyWindow = _x64dbgapi.DisassemblyWindow
DumpWindow = _x64dbgapi.DumpWindow
StackWindow = _x64dbgapi.StackWindow
GraphWindow = _x64dbgapi.GraphWindow
MemMapWindow = _x64dbgapi.MemMapWindow
SymModWindow = _x64dbgapi.SymModWindow

def Gui_SelectionGet(*args):
  """Gui_SelectionGet(Script::Gui::Window window, duint * start, duint * end) -> bool"""
  return _x64dbgapi.Gui_SelectionGet(*args)

def Gui_SelectionSet(*args):
  """Gui_SelectionSet(Script::Gui::Window window, duint start, duint end) -> bool"""
  return _x64dbgapi.Gui_SelectionSet(*args)

def Gui_SelectionGetStart(*args):
  """Gui_SelectionGetStart(Script::Gui::Window window) -> duint"""
  return _x64dbgapi.Gui_SelectionGetStart(*args)

def Gui_SelectionGetEnd(*args):
  """Gui_SelectionGetEnd(Script::Gui::Window window) -> duint"""
  return _x64dbgapi.Gui_SelectionGetEnd(*args)

def Gui_Message(*args):
  """Gui_Message(char const * message)"""
  return _x64dbgapi.Gui_Message(*args)

def Gui_MessageYesNo(*args):
  """Gui_MessageYesNo(char const * message) -> bool"""
  return _x64dbgapi.Gui_MessageYesNo(*args)

def Gui_InputLine(*args):
  """Gui_InputLine(char const * title, char * text) -> bool"""
  return _x64dbgapi.Gui_InputLine(*args)

def Gui_InputValue(*args):
  """Gui_InputValue(char const * title, duint * value) -> bool"""
  return _x64dbgapi.Gui_InputValue(*args)

def Gui_Refresh():
  """Gui_Refresh()"""
  return _x64dbgapi.Gui_Refresh()

def Gui_AddQWidgetTab(*args):
  """Gui_AddQWidgetTab(void * qWidget)"""
  return _x64dbgapi.Gui_AddQWidgetTab(*args)

def Gui_ShowQWidgetTab(*args):
  """Gui_ShowQWidgetTab(void * qWidget)"""
  return _x64dbgapi.Gui_ShowQWidgetTab(*args)

def Gui_CloseQWidgetTab(*args):
  """Gui_CloseQWidgetTab(void * qWidget)"""
  return _x64dbgapi.Gui_CloseQWidgetTab(*args)
class LabelInfo(object):
    """Proxy of C++ Script::Label::LabelInfo class"""
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    mod = _swig_property(_x64dbgapi.LabelInfo_mod_get, _x64dbgapi.LabelInfo_mod_set)
    rva = _swig_property(_x64dbgapi.LabelInfo_rva_get, _x64dbgapi.LabelInfo_rva_set)
    text = _swig_property(_x64dbgapi.LabelInfo_text_get, _x64dbgapi.LabelInfo_text_set)
    manual = _swig_property(_x64dbgapi.LabelInfo_manual_get, _x64dbgapi.LabelInfo_manual_set)
    def __init__(self): 
        """__init__(Script::Label::LabelInfo self) -> LabelInfo"""
        this = _x64dbgapi.new_LabelInfo()
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _x64dbgapi.delete_LabelInfo
    __del__ = lambda self : None;
LabelInfo_swigregister = _x64dbgapi.LabelInfo_swigregister
LabelInfo_swigregister(LabelInfo)


def Label_Set(*args):
  """
    Label_Set(duint addr, char const * text, bool manual=False) -> bool
    Label_Set(duint addr, char const * text) -> bool
    """
  return _x64dbgapi.Label_Set(*args)

def Label_SetByLabelInfo(*args):
  """Label_SetByLabelInfo(LabelInfo info) -> bool"""
  return _x64dbgapi.Label_SetByLabelInfo(*args)

def Label_FromString(*args):
  """Label_FromString(char const * label, duint * addr) -> bool"""
  return _x64dbgapi.Label_FromString(*args)

def Label_Get(*args):
  """Label_Get(duint addr, char * text) -> bool"""
  return _x64dbgapi.Label_Get(*args)

def Label_GetInfo(*args):
  """Label_GetInfo(duint addr, LabelInfo info) -> bool"""
  return _x64dbgapi.Label_GetInfo(*args)

def Label_Delete(*args):
  """Label_Delete(duint addr) -> bool"""
  return _x64dbgapi.Label_Delete(*args)

def Label_DeleteRange(*args):
  """Label_DeleteRange(duint start, duint end)"""
  return _x64dbgapi.Label_DeleteRange(*args)

def Label_Clear():
  """Label_Clear()"""
  return _x64dbgapi.Label_Clear()

def Label_GetList(*args):
  """Label_GetList(ListInfo list) -> bool"""
  return _x64dbgapi.Label_GetList(*args)

def Memory_Read(*args):
  """Memory_Read(duint addr, void * data, duint size, duint * sizeRead) -> bool"""
  return _x64dbgapi.Memory_Read(*args)

def Memory_Write(*args):
  """Memory_Write(duint addr, void const * data, duint size, duint * sizeWritten) -> bool"""
  return _x64dbgapi.Memory_Write(*args)

def Memory_IsValidPtr(*args):
  """Memory_IsValidPtr(duint addr) -> bool"""
  return _x64dbgapi.Memory_IsValidPtr(*args)

def Memory_RemoteAlloc(*args):
  """Memory_RemoteAlloc(duint addr, duint size) -> duint"""
  return _x64dbgapi.Memory_RemoteAlloc(*args)

def Memory_RemoteFree(*args):
  """Memory_RemoteFree(duint addr) -> bool"""
  return _x64dbgapi.Memory_RemoteFree(*args)

def Memory_GetProtect(*args):
  """
    Memory_GetProtect(duint addr, bool reserved=False, bool cache=True) -> unsigned int
    Memory_GetProtect(duint addr, bool reserved=False) -> unsigned int
    Memory_GetProtect(duint addr) -> unsigned int
    """
  return _x64dbgapi.Memory_GetProtect(*args)

def Memory_GetBase(*args):
  """
    Memory_GetBase(duint addr, bool reserved=False, bool cache=True) -> duint
    Memory_GetBase(duint addr, bool reserved=False) -> duint
    Memory_GetBase(duint addr) -> duint
    """
  return _x64dbgapi.Memory_GetBase(*args)

def Memory_GetSize(*args):
  """
    Memory_GetSize(duint addr, bool reserved=False, bool cache=True) -> duint
    Memory_GetSize(duint addr, bool reserved=False) -> duint
    Memory_GetSize(duint addr) -> duint
    """
  return _x64dbgapi.Memory_GetSize(*args)

def Memory_ReadByte(*args):
  """Memory_ReadByte(duint addr) -> unsigned char"""
  return _x64dbgapi.Memory_ReadByte(*args)

def Memory_WriteByte(*args):
  """Memory_WriteByte(duint addr, unsigned char data) -> bool"""
  return _x64dbgapi.Memory_WriteByte(*args)

def Memory_ReadWord(*args):
  """Memory_ReadWord(duint addr) -> unsigned short"""
  return _x64dbgapi.Memory_ReadWord(*args)

def Memory_WriteWord(*args):
  """Memory_WriteWord(duint addr, unsigned short data) -> bool"""
  return _x64dbgapi.Memory_WriteWord(*args)

def Memory_ReadDword(*args):
  """Memory_ReadDword(duint addr) -> unsigned int"""
  return _x64dbgapi.Memory_ReadDword(*args)

def Memory_WriteDword(*args):
  """Memory_WriteDword(duint addr, unsigned int data) -> bool"""
  return _x64dbgapi.Memory_WriteDword(*args)

def Memory_ReadQword(*args):
  """Memory_ReadQword(duint addr) -> unsigned long long"""
  return _x64dbgapi.Memory_ReadQword(*args)

def Memory_WriteQword(*args):
  """Memory_WriteQword(duint addr, unsigned long long data) -> bool"""
  return _x64dbgapi.Memory_WriteQword(*args)

def Memory_ReadPtr(*args):
  """Memory_ReadPtr(duint addr) -> duint"""
  return _x64dbgapi.Memory_ReadPtr(*args)

def Memory_WritePtr(*args):
  """Memory_WritePtr(duint addr, duint data) -> bool"""
  return _x64dbgapi.Memory_WritePtr(*args)

def Misc_ParseExpression(*args):
  """Misc_ParseExpression(char const * expression, duint * value) -> bool"""
  return _x64dbgapi.Misc_ParseExpression(*args)

def Misc_RemoteGetProcAddress(*args):
  """Misc_RemoteGetProcAddress(char const * module, char const * api) -> duint"""
  return _x64dbgapi.Misc_RemoteGetProcAddress(*args)

def Misc_ResolveLabel(*args):
  """Misc_ResolveLabel(char const * label) -> duint"""
  return _x64dbgapi.Misc_ResolveLabel(*args)

def Misc_Alloc(*args):
  """Misc_Alloc(duint size) -> void *"""
  return _x64dbgapi.Misc_Alloc(*args)

def Misc_Free(*args):
  """Misc_Free(void * ptr)"""
  return _x64dbgapi.Misc_Free(*args)
class ModuleInfo(object):
    """Proxy of C++ Script::Module::ModuleInfo class"""
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    base = _swig_property(_x64dbgapi.ModuleInfo_base_get, _x64dbgapi.ModuleInfo_base_set)
    size = _swig_property(_x64dbgapi.ModuleInfo_size_get, _x64dbgapi.ModuleInfo_size_set)
    entry = _swig_property(_x64dbgapi.ModuleInfo_entry_get, _x64dbgapi.ModuleInfo_entry_set)
    sectionCount = _swig_property(_x64dbgapi.ModuleInfo_sectionCount_get, _x64dbgapi.ModuleInfo_sectionCount_set)
    name = _swig_property(_x64dbgapi.ModuleInfo_name_get, _x64dbgapi.ModuleInfo_name_set)
    path = _swig_property(_x64dbgapi.ModuleInfo_path_get, _x64dbgapi.ModuleInfo_path_set)
    def __init__(self): 
        """__init__(Script::Module::ModuleInfo self) -> ModuleInfo"""
        this = _x64dbgapi.new_ModuleInfo()
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _x64dbgapi.delete_ModuleInfo
    __del__ = lambda self : None;
ModuleInfo_swigregister = _x64dbgapi.ModuleInfo_swigregister
ModuleInfo_swigregister(ModuleInfo)

class ModuleSectionInfo(object):
    """Proxy of C++ Script::Module::ModuleSectionInfo class"""
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    addr = _swig_property(_x64dbgapi.ModuleSectionInfo_addr_get, _x64dbgapi.ModuleSectionInfo_addr_set)
    size = _swig_property(_x64dbgapi.ModuleSectionInfo_size_get, _x64dbgapi.ModuleSectionInfo_size_set)
    name = _swig_property(_x64dbgapi.ModuleSectionInfo_name_get, _x64dbgapi.ModuleSectionInfo_name_set)
    def __init__(self): 
        """__init__(Script::Module::ModuleSectionInfo self) -> ModuleSectionInfo"""
        this = _x64dbgapi.new_ModuleSectionInfo()
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _x64dbgapi.delete_ModuleSectionInfo
    __del__ = lambda self : None;
ModuleSectionInfo_swigregister = _x64dbgapi.ModuleSectionInfo_swigregister
ModuleSectionInfo_swigregister(ModuleSectionInfo)


def Module_InfoFromAddr(*args):
  """Module_InfoFromAddr(duint addr, ModuleInfo info) -> bool"""
  return _x64dbgapi.Module_InfoFromAddr(*args)

def Module_InfoFromName(*args):
  """Module_InfoFromName(char const * name, ModuleInfo info) -> bool"""
  return _x64dbgapi.Module_InfoFromName(*args)

def Module_BaseFromAddr(*args):
  """Module_BaseFromAddr(duint addr) -> duint"""
  return _x64dbgapi.Module_BaseFromAddr(*args)

def Module_BaseFromName(*args):
  """Module_BaseFromName(char const * name) -> duint"""
  return _x64dbgapi.Module_BaseFromName(*args)

def Module_SizeFromAddr(*args):
  """Module_SizeFromAddr(duint addr) -> duint"""
  return _x64dbgapi.Module_SizeFromAddr(*args)

def Module_SizeFromName(*args):
  """Module_SizeFromName(char const * name) -> duint"""
  return _x64dbgapi.Module_SizeFromName(*args)

def Module_NameFromAddr(*args):
  """Module_NameFromAddr(duint addr, char * name) -> bool"""
  return _x64dbgapi.Module_NameFromAddr(*args)

def Module_PathFromAddr(*args):
  """Module_PathFromAddr(duint addr, char * path) -> bool"""
  return _x64dbgapi.Module_PathFromAddr(*args)

def Module_PathFromName(*args):
  """Module_PathFromName(char const * name, char * path) -> bool"""
  return _x64dbgapi.Module_PathFromName(*args)

def Module_EntryFromAddr(*args):
  """Module_EntryFromAddr(duint addr) -> duint"""
  return _x64dbgapi.Module_EntryFromAddr(*args)

def Module_EntryFromName(*args):
  """Module_EntryFromName(char const * name) -> duint"""
  return _x64dbgapi.Module_EntryFromName(*args)

def Module_SectionCountFromAddr(*args):
  """Module_SectionCountFromAddr(duint addr) -> int"""
  return _x64dbgapi.Module_SectionCountFromAddr(*args)

def Module_SectionCountFromName(*args):
  """Module_SectionCountFromName(char const * name) -> int"""
  return _x64dbgapi.Module_SectionCountFromName(*args)

def Module_SectionFromAddr(*args):
  """Module_SectionFromAddr(duint addr, int number, ModuleSectionInfo section) -> bool"""
  return _x64dbgapi.Module_SectionFromAddr(*args)

def Module_SectionFromName(*args):
  """Module_SectionFromName(char const * name, int number, ModuleSectionInfo section) -> bool"""
  return _x64dbgapi.Module_SectionFromName(*args)

def Module_SectionListFromAddr(*args):
  """Module_SectionListFromAddr(duint addr, ListInfo list) -> bool"""
  return _x64dbgapi.Module_SectionListFromAddr(*args)

def Module_SectionListFromName(*args):
  """Module_SectionListFromName(char const * name, ListInfo list) -> bool"""
  return _x64dbgapi.Module_SectionListFromName(*args)

def Module_GetMainModuleInfo(*args):
  """Module_GetMainModuleInfo(ModuleInfo info) -> bool"""
  return _x64dbgapi.Module_GetMainModuleInfo(*args)

def Module_GetMainModuleBase():
  """Module_GetMainModuleBase() -> duint"""
  return _x64dbgapi.Module_GetMainModuleBase()

def Module_GetMainModuleSize():
  """Module_GetMainModuleSize() -> duint"""
  return _x64dbgapi.Module_GetMainModuleSize()

def Module_GetMainModuleEntry():
  """Module_GetMainModuleEntry() -> duint"""
  return _x64dbgapi.Module_GetMainModuleEntry()

def Module_GetMainModuleSectionCount():
  """Module_GetMainModuleSectionCount() -> int"""
  return _x64dbgapi.Module_GetMainModuleSectionCount()

def Module_GetMainModuleName(*args):
  """Module_GetMainModuleName(char * name) -> bool"""
  return _x64dbgapi.Module_GetMainModuleName(*args)

def Module_GetMainModulePath(*args):
  """Module_GetMainModulePath(char * path) -> bool"""
  return _x64dbgapi.Module_GetMainModulePath(*args)

def Module_GetMainModuleSectionList(*args):
  """Module_GetMainModuleSectionList(ListInfo list) -> bool"""
  return _x64dbgapi.Module_GetMainModuleSectionList(*args)

def Module_GetList(*args):
  """Module_GetList(ListInfo list) -> bool"""
  return _x64dbgapi.Module_GetList(*args)

def Pattern_Find(*args):
  """Pattern_Find(unsigned char * data, duint datasize, char const * pattern) -> duint"""
  return _x64dbgapi.Pattern_Find(*args)

def Pattern_FindMem(*args):
  """Pattern_FindMem(duint start, duint size, char const * pattern) -> duint"""
  return _x64dbgapi.Pattern_FindMem(*args)

def Pattern_Write(*args):
  """Pattern_Write(unsigned char * data, duint datasize, char const * pattern)"""
  return _x64dbgapi.Pattern_Write(*args)

def Pattern_WriteMem(*args):
  """Pattern_WriteMem(duint start, duint size, char const * pattern)"""
  return _x64dbgapi.Pattern_WriteMem(*args)

def Pattern_SearchAndReplace(*args):
  """Pattern_SearchAndReplace(unsigned char * data, duint datasize, char const * searchpattern, char const * replacepattern) -> bool"""
  return _x64dbgapi.Pattern_SearchAndReplace(*args)

def Pattern_SearchAndReplaceMem(*args):
  """Pattern_SearchAndReplaceMem(duint start, duint size, char const * searchpattern, char const * replacepattern) -> bool"""
  return _x64dbgapi.Pattern_SearchAndReplaceMem(*args)
DR0 = _x64dbgapi.DR0
DR1 = _x64dbgapi.DR1
DR2 = _x64dbgapi.DR2
DR3 = _x64dbgapi.DR3
DR6 = _x64dbgapi.DR6
DR7 = _x64dbgapi.DR7
EAX = _x64dbgapi.EAX
AX = _x64dbgapi.AX
AH = _x64dbgapi.AH
AL = _x64dbgapi.AL
EBX = _x64dbgapi.EBX
BX = _x64dbgapi.BX
BH = _x64dbgapi.BH
BL = _x64dbgapi.BL
ECX = _x64dbgapi.ECX
CX = _x64dbgapi.CX
CH = _x64dbgapi.CH
CL = _x64dbgapi.CL
EDX = _x64dbgapi.EDX
DX = _x64dbgapi.DX
DH = _x64dbgapi.DH
DL = _x64dbgapi.DL
EDI = _x64dbgapi.EDI
DI = _x64dbgapi.DI
ESI = _x64dbgapi.ESI
SI = _x64dbgapi.SI
EBP = _x64dbgapi.EBP
BP = _x64dbgapi.BP
ESP = _x64dbgapi.ESP
SP = _x64dbgapi.SP
EIP = _x64dbgapi.EIP
CIP = _x64dbgapi.CIP
CSP = _x64dbgapi.CSP
CAX = _x64dbgapi.CAX
CBX = _x64dbgapi.CBX
CCX = _x64dbgapi.CCX
CDX = _x64dbgapi.CDX
CDI = _x64dbgapi.CDI
CSI = _x64dbgapi.CSI
CBP = _x64dbgapi.CBP
CFLAGS = _x64dbgapi.CFLAGS

def Register_Get(*args):
  """Register_Get(Script::Register::RegisterEnum reg) -> duint"""
  return _x64dbgapi.Register_Get(*args)

def Register_Set(*args):
  """Register_Set(Script::Register::RegisterEnum reg, duint value) -> bool"""
  return _x64dbgapi.Register_Set(*args)

def Register_Size():
  """Register_Size() -> int"""
  return _x64dbgapi.Register_Size()

def Register_GetDR0():
  """Register_GetDR0() -> duint"""
  return _x64dbgapi.Register_GetDR0()

def Register_SetDR0(*args):
  """Register_SetDR0(duint value) -> bool"""
  return _x64dbgapi.Register_SetDR0(*args)

def Register_GetDR1():
  """Register_GetDR1() -> duint"""
  return _x64dbgapi.Register_GetDR1()

def Register_SetDR1(*args):
  """Register_SetDR1(duint value) -> bool"""
  return _x64dbgapi.Register_SetDR1(*args)

def Register_GetDR2():
  """Register_GetDR2() -> duint"""
  return _x64dbgapi.Register_GetDR2()

def Register_SetDR2(*args):
  """Register_SetDR2(duint value) -> bool"""
  return _x64dbgapi.Register_SetDR2(*args)

def Register_GetDR3():
  """Register_GetDR3() -> duint"""
  return _x64dbgapi.Register_GetDR3()

def Register_SetDR3(*args):
  """Register_SetDR3(duint value) -> bool"""
  return _x64dbgapi.Register_SetDR3(*args)

def Register_GetDR6():
  """Register_GetDR6() -> duint"""
  return _x64dbgapi.Register_GetDR6()

def Register_SetDR6(*args):
  """Register_SetDR6(duint value) -> bool"""
  return _x64dbgapi.Register_SetDR6(*args)

def Register_GetDR7():
  """Register_GetDR7() -> duint"""
  return _x64dbgapi.Register_GetDR7()

def Register_SetDR7(*args):
  """Register_SetDR7(duint value) -> bool"""
  return _x64dbgapi.Register_SetDR7(*args)

def Register_GetEAX():
  """Register_GetEAX() -> unsigned int"""
  return _x64dbgapi.Register_GetEAX()

def Register_SetEAX(*args):
  """Register_SetEAX(unsigned int value) -> bool"""
  return _x64dbgapi.Register_SetEAX(*args)

def Register_GetAX():
  """Register_GetAX() -> unsigned short"""
  return _x64dbgapi.Register_GetAX()

def Register_SetAX(*args):
  """Register_SetAX(unsigned short value) -> bool"""
  return _x64dbgapi.Register_SetAX(*args)

def Register_GetAH():
  """Register_GetAH() -> unsigned char"""
  return _x64dbgapi.Register_GetAH()

def Register_SetAH(*args):
  """Register_SetAH(unsigned char value) -> bool"""
  return _x64dbgapi.Register_SetAH(*args)

def Register_GetAL():
  """Register_GetAL() -> unsigned char"""
  return _x64dbgapi.Register_GetAL()

def Register_SetAL(*args):
  """Register_SetAL(unsigned char value) -> bool"""
  return _x64dbgapi.Register_SetAL(*args)

def Register_GetEBX():
  """Register_GetEBX() -> unsigned int"""
  return _x64dbgapi.Register_GetEBX()

def Register_SetEBX(*args):
  """Register_SetEBX(unsigned int value) -> bool"""
  return _x64dbgapi.Register_SetEBX(*args)

def Register_GetBX():
  """Register_GetBX() -> unsigned short"""
  return _x64dbgapi.Register_GetBX()

def Register_SetBX(*args):
  """Register_SetBX(unsigned short value) -> bool"""
  return _x64dbgapi.Register_SetBX(*args)

def Register_GetBH():
  """Register_GetBH() -> unsigned char"""
  return _x64dbgapi.Register_GetBH()

def Register_SetBH(*args):
  """Register_SetBH(unsigned char value) -> bool"""
  return _x64dbgapi.Register_SetBH(*args)

def Register_GetBL():
  """Register_GetBL() -> unsigned char"""
  return _x64dbgapi.Register_GetBL()

def Register_SetBL(*args):
  """Register_SetBL(unsigned char value) -> bool"""
  return _x64dbgapi.Register_SetBL(*args)

def Register_GetECX():
  """Register_GetECX() -> unsigned int"""
  return _x64dbgapi.Register_GetECX()

def Register_SetECX(*args):
  """Register_SetECX(unsigned int value) -> bool"""
  return _x64dbgapi.Register_SetECX(*args)

def Register_GetCX():
  """Register_GetCX() -> unsigned short"""
  return _x64dbgapi.Register_GetCX()

def Register_SetCX(*args):
  """Register_SetCX(unsigned short value) -> bool"""
  return _x64dbgapi.Register_SetCX(*args)

def Register_GetCH():
  """Register_GetCH() -> unsigned char"""
  return _x64dbgapi.Register_GetCH()

def Register_SetCH(*args):
  """Register_SetCH(unsigned char value) -> bool"""
  return _x64dbgapi.Register_SetCH(*args)

def Register_GetCL():
  """Register_GetCL() -> unsigned char"""
  return _x64dbgapi.Register_GetCL()

def Register_SetCL(*args):
  """Register_SetCL(unsigned char value) -> bool"""
  return _x64dbgapi.Register_SetCL(*args)

def Register_GetEDX():
  """Register_GetEDX() -> unsigned int"""
  return _x64dbgapi.Register_GetEDX()

def Register_SetEDX(*args):
  """Register_SetEDX(unsigned int value) -> bool"""
  return _x64dbgapi.Register_SetEDX(*args)

def Register_GetDX():
  """Register_GetDX() -> unsigned short"""
  return _x64dbgapi.Register_GetDX()

def Register_SetDX(*args):
  """Register_SetDX(unsigned short value) -> bool"""
  return _x64dbgapi.Register_SetDX(*args)

def Register_GetDH():
  """Register_GetDH() -> unsigned char"""
  return _x64dbgapi.Register_GetDH()

def Register_SetDH(*args):
  """Register_SetDH(unsigned char value) -> bool"""
  return _x64dbgapi.Register_SetDH(*args)

def Register_GetDL():
  """Register_GetDL() -> unsigned char"""
  return _x64dbgapi.Register_GetDL()

def Register_SetDL(*args):
  """Register_SetDL(unsigned char value) -> bool"""
  return _x64dbgapi.Register_SetDL(*args)

def Register_GetEDI():
  """Register_GetEDI() -> unsigned int"""
  return _x64dbgapi.Register_GetEDI()

def Register_SetEDI(*args):
  """Register_SetEDI(unsigned int value) -> bool"""
  return _x64dbgapi.Register_SetEDI(*args)

def Register_GetDI():
  """Register_GetDI() -> unsigned short"""
  return _x64dbgapi.Register_GetDI()

def Register_SetDI(*args):
  """Register_SetDI(unsigned short value) -> bool"""
  return _x64dbgapi.Register_SetDI(*args)

def Register_GetESI():
  """Register_GetESI() -> unsigned int"""
  return _x64dbgapi.Register_GetESI()

def Register_SetESI(*args):
  """Register_SetESI(unsigned int value) -> bool"""
  return _x64dbgapi.Register_SetESI(*args)

def Register_GetSI():
  """Register_GetSI() -> unsigned short"""
  return _x64dbgapi.Register_GetSI()

def Register_SetSI(*args):
  """Register_SetSI(unsigned short value) -> bool"""
  return _x64dbgapi.Register_SetSI(*args)

def Register_GetEBP():
  """Register_GetEBP() -> unsigned int"""
  return _x64dbgapi.Register_GetEBP()

def Register_SetEBP(*args):
  """Register_SetEBP(unsigned int value) -> bool"""
  return _x64dbgapi.Register_SetEBP(*args)

def Register_GetBP():
  """Register_GetBP() -> unsigned short"""
  return _x64dbgapi.Register_GetBP()

def Register_SetBP(*args):
  """Register_SetBP(unsigned short value) -> bool"""
  return _x64dbgapi.Register_SetBP(*args)

def Register_GetESP():
  """Register_GetESP() -> unsigned int"""
  return _x64dbgapi.Register_GetESP()

def Register_SetESP(*args):
  """Register_SetESP(unsigned int value) -> bool"""
  return _x64dbgapi.Register_SetESP(*args)

def Register_GetSP():
  """Register_GetSP() -> unsigned short"""
  return _x64dbgapi.Register_GetSP()

def Register_SetSP(*args):
  """Register_SetSP(unsigned short value) -> bool"""
  return _x64dbgapi.Register_SetSP(*args)

def Register_GetEIP():
  """Register_GetEIP() -> unsigned int"""
  return _x64dbgapi.Register_GetEIP()

def Register_SetEIP(*args):
  """Register_SetEIP(unsigned int value) -> bool"""
  return _x64dbgapi.Register_SetEIP(*args)

def Register_GetCAX():
  """Register_GetCAX() -> duint"""
  return _x64dbgapi.Register_GetCAX()

def Register_SetCAX(*args):
  """Register_SetCAX(duint value) -> bool"""
  return _x64dbgapi.Register_SetCAX(*args)

def Register_GetCBX():
  """Register_GetCBX() -> duint"""
  return _x64dbgapi.Register_GetCBX()

def Register_SetCBX(*args):
  """Register_SetCBX(duint value) -> bool"""
  return _x64dbgapi.Register_SetCBX(*args)

def Register_GetCCX():
  """Register_GetCCX() -> duint"""
  return _x64dbgapi.Register_GetCCX()

def Register_SetCCX(*args):
  """Register_SetCCX(duint value) -> bool"""
  return _x64dbgapi.Register_SetCCX(*args)

def Register_GetCDX():
  """Register_GetCDX() -> duint"""
  return _x64dbgapi.Register_GetCDX()

def Register_SetCDX(*args):
  """Register_SetCDX(duint value) -> bool"""
  return _x64dbgapi.Register_SetCDX(*args)

def Register_GetCDI():
  """Register_GetCDI() -> duint"""
  return _x64dbgapi.Register_GetCDI()

def Register_SetCDI(*args):
  """Register_SetCDI(duint value) -> bool"""
  return _x64dbgapi.Register_SetCDI(*args)

def Register_GetCSI():
  """Register_GetCSI() -> duint"""
  return _x64dbgapi.Register_GetCSI()

def Register_SetCSI(*args):
  """Register_SetCSI(duint value) -> bool"""
  return _x64dbgapi.Register_SetCSI(*args)

def Register_GetCBP():
  """Register_GetCBP() -> duint"""
  return _x64dbgapi.Register_GetCBP()

def Register_SetCBP(*args):
  """Register_SetCBP(duint value) -> bool"""
  return _x64dbgapi.Register_SetCBP(*args)

def Register_GetCSP():
  """Register_GetCSP() -> duint"""
  return _x64dbgapi.Register_GetCSP()

def Register_SetCSP(*args):
  """Register_SetCSP(duint value) -> bool"""
  return _x64dbgapi.Register_SetCSP(*args)

def Register_GetCIP():
  """Register_GetCIP() -> duint"""
  return _x64dbgapi.Register_GetCIP()

def Register_SetCIP(*args):
  """Register_SetCIP(duint value) -> bool"""
  return _x64dbgapi.Register_SetCIP(*args)

def Register_GetCFLAGS():
  """Register_GetCFLAGS() -> duint"""
  return _x64dbgapi.Register_GetCFLAGS()

def Register_SetCFLAGS(*args):
  """Register_SetCFLAGS(duint value) -> bool"""
  return _x64dbgapi.Register_SetCFLAGS(*args)

def Stack_Pop():
  """Stack_Pop() -> duint"""
  return _x64dbgapi.Stack_Pop()

def Stack_Push(*args):
  """Stack_Push(duint value) -> duint"""
  return _x64dbgapi.Stack_Push(*args)

def Stack_Peek(offset=0):
  """
    Stack_Peek(int offset=0) -> duint
    Stack_Peek() -> duint
    """
  return _x64dbgapi.Stack_Peek(offset)
Function = _x64dbgapi.Function
Import = _x64dbgapi.Import
Export = _x64dbgapi.Export
class SymbolInfo(object):
    """Proxy of C++ Script::Symbol::SymbolInfo class"""
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    mod = _swig_property(_x64dbgapi.SymbolInfo_mod_get, _x64dbgapi.SymbolInfo_mod_set)
    rva = _swig_property(_x64dbgapi.SymbolInfo_rva_get, _x64dbgapi.SymbolInfo_rva_set)
    name = _swig_property(_x64dbgapi.SymbolInfo_name_get, _x64dbgapi.SymbolInfo_name_set)
    manual = _swig_property(_x64dbgapi.SymbolInfo_manual_get, _x64dbgapi.SymbolInfo_manual_set)
    type = _swig_property(_x64dbgapi.SymbolInfo_type_get, _x64dbgapi.SymbolInfo_type_set)
    def __init__(self): 
        """__init__(Script::Symbol::SymbolInfo self) -> SymbolInfo"""
        this = _x64dbgapi.new_SymbolInfo()
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _x64dbgapi.delete_SymbolInfo
    __del__ = lambda self : None;
SymbolInfo_swigregister = _x64dbgapi.SymbolInfo_swigregister
SymbolInfo_swigregister(SymbolInfo)


def Symbol_GetList(*args):
  """Symbol_GetList(ListInfo list) -> bool"""
  return _x64dbgapi.Symbol_GetList(*args)
class ArgumentInfoArray(object):
    """Proxy of C++ ArgumentInfoArray class"""
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    def __init__(self, *args): 
        """__init__(ArgumentInfoArray self, size_t nelements) -> ArgumentInfoArray"""
        this = _x64dbgapi.new_ArgumentInfoArray(*args)
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _x64dbgapi.delete_ArgumentInfoArray
    __del__ = lambda self : None;
    def __getitem__(self, *args):
        """__getitem__(ArgumentInfoArray self, size_t index) -> ArgumentInfo"""
        return _x64dbgapi.ArgumentInfoArray___getitem__(self, *args)

    def __setitem__(self, *args):
        """__setitem__(ArgumentInfoArray self, size_t index, ArgumentInfo value)"""
        return _x64dbgapi.ArgumentInfoArray___setitem__(self, *args)

    def cast(self):
        """cast(ArgumentInfoArray self) -> ArgumentInfo"""
        return _x64dbgapi.ArgumentInfoArray_cast(self)

    def frompointer(*args):
        """frompointer(ArgumentInfo t) -> ArgumentInfoArray"""
        return _x64dbgapi.ArgumentInfoArray_frompointer(*args)

    frompointer = staticmethod(frompointer)
ArgumentInfoArray_swigregister = _x64dbgapi.ArgumentInfoArray_swigregister
ArgumentInfoArray_swigregister(ArgumentInfoArray)

def ArgumentInfoArray_frompointer(*args):
  """ArgumentInfoArray_frompointer(ArgumentInfo t) -> ArgumentInfoArray"""
  return _x64dbgapi.ArgumentInfoArray_frompointer(*args)

class BookmarkInfoArray(object):
    """Proxy of C++ BookmarkInfoArray class"""
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    def __init__(self, *args): 
        """__init__(BookmarkInfoArray self, size_t nelements) -> BookmarkInfoArray"""
        this = _x64dbgapi.new_BookmarkInfoArray(*args)
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _x64dbgapi.delete_BookmarkInfoArray
    __del__ = lambda self : None;
    def __getitem__(self, *args):
        """__getitem__(BookmarkInfoArray self, size_t index) -> BookmarkInfo"""
        return _x64dbgapi.BookmarkInfoArray___getitem__(self, *args)

    def __setitem__(self, *args):
        """__setitem__(BookmarkInfoArray self, size_t index, BookmarkInfo value)"""
        return _x64dbgapi.BookmarkInfoArray___setitem__(self, *args)

    def cast(self):
        """cast(BookmarkInfoArray self) -> BookmarkInfo"""
        return _x64dbgapi.BookmarkInfoArray_cast(self)

    def frompointer(*args):
        """frompointer(BookmarkInfo t) -> BookmarkInfoArray"""
        return _x64dbgapi.BookmarkInfoArray_frompointer(*args)

    frompointer = staticmethod(frompointer)
BookmarkInfoArray_swigregister = _x64dbgapi.BookmarkInfoArray_swigregister
BookmarkInfoArray_swigregister(BookmarkInfoArray)

def BookmarkInfoArray_frompointer(*args):
  """BookmarkInfoArray_frompointer(BookmarkInfo t) -> BookmarkInfoArray"""
  return _x64dbgapi.BookmarkInfoArray_frompointer(*args)

class CommentInfoArray(object):
    """Proxy of C++ CommentInfoArray class"""
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    def __init__(self, *args): 
        """__init__(CommentInfoArray self, size_t nelements) -> CommentInfoArray"""
        this = _x64dbgapi.new_CommentInfoArray(*args)
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _x64dbgapi.delete_CommentInfoArray
    __del__ = lambda self : None;
    def __getitem__(self, *args):
        """__getitem__(CommentInfoArray self, size_t index) -> CommentInfo"""
        return _x64dbgapi.CommentInfoArray___getitem__(self, *args)

    def __setitem__(self, *args):
        """__setitem__(CommentInfoArray self, size_t index, CommentInfo value)"""
        return _x64dbgapi.CommentInfoArray___setitem__(self, *args)

    def cast(self):
        """cast(CommentInfoArray self) -> CommentInfo"""
        return _x64dbgapi.CommentInfoArray_cast(self)

    def frompointer(*args):
        """frompointer(CommentInfo t) -> CommentInfoArray"""
        return _x64dbgapi.CommentInfoArray_frompointer(*args)

    frompointer = staticmethod(frompointer)
CommentInfoArray_swigregister = _x64dbgapi.CommentInfoArray_swigregister
CommentInfoArray_swigregister(CommentInfoArray)

def CommentInfoArray_frompointer(*args):
  """CommentInfoArray_frompointer(CommentInfo t) -> CommentInfoArray"""
  return _x64dbgapi.CommentInfoArray_frompointer(*args)

class FunctionInfoArray(object):
    """Proxy of C++ FunctionInfoArray class"""
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    def __init__(self, *args): 
        """__init__(FunctionInfoArray self, size_t nelements) -> FunctionInfoArray"""
        this = _x64dbgapi.new_FunctionInfoArray(*args)
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _x64dbgapi.delete_FunctionInfoArray
    __del__ = lambda self : None;
    def __getitem__(self, *args):
        """__getitem__(FunctionInfoArray self, size_t index) -> FunctionInfo"""
        return _x64dbgapi.FunctionInfoArray___getitem__(self, *args)

    def __setitem__(self, *args):
        """__setitem__(FunctionInfoArray self, size_t index, FunctionInfo value)"""
        return _x64dbgapi.FunctionInfoArray___setitem__(self, *args)

    def cast(self):
        """cast(FunctionInfoArray self) -> FunctionInfo"""
        return _x64dbgapi.FunctionInfoArray_cast(self)

    def frompointer(*args):
        """frompointer(FunctionInfo t) -> FunctionInfoArray"""
        return _x64dbgapi.FunctionInfoArray_frompointer(*args)

    frompointer = staticmethod(frompointer)
FunctionInfoArray_swigregister = _x64dbgapi.FunctionInfoArray_swigregister
FunctionInfoArray_swigregister(FunctionInfoArray)

def FunctionInfoArray_frompointer(*args):
  """FunctionInfoArray_frompointer(FunctionInfo t) -> FunctionInfoArray"""
  return _x64dbgapi.FunctionInfoArray_frompointer(*args)

class LabelInfoArray(object):
    """Proxy of C++ LabelInfoArray class"""
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    def __init__(self, *args): 
        """__init__(LabelInfoArray self, size_t nelements) -> LabelInfoArray"""
        this = _x64dbgapi.new_LabelInfoArray(*args)
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _x64dbgapi.delete_LabelInfoArray
    __del__ = lambda self : None;
    def __getitem__(self, *args):
        """__getitem__(LabelInfoArray self, size_t index) -> LabelInfo"""
        return _x64dbgapi.LabelInfoArray___getitem__(self, *args)

    def __setitem__(self, *args):
        """__setitem__(LabelInfoArray self, size_t index, LabelInfo value)"""
        return _x64dbgapi.LabelInfoArray___setitem__(self, *args)

    def cast(self):
        """cast(LabelInfoArray self) -> LabelInfo"""
        return _x64dbgapi.LabelInfoArray_cast(self)

    def frompointer(*args):
        """frompointer(LabelInfo t) -> LabelInfoArray"""
        return _x64dbgapi.LabelInfoArray_frompointer(*args)

    frompointer = staticmethod(frompointer)
LabelInfoArray_swigregister = _x64dbgapi.LabelInfoArray_swigregister
LabelInfoArray_swigregister(LabelInfoArray)

def LabelInfoArray_frompointer(*args):
  """LabelInfoArray_frompointer(LabelInfo t) -> LabelInfoArray"""
  return _x64dbgapi.LabelInfoArray_frompointer(*args)

class ModuleInfoArray(object):
    """Proxy of C++ ModuleInfoArray class"""
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    def __init__(self, *args): 
        """__init__(ModuleInfoArray self, size_t nelements) -> ModuleInfoArray"""
        this = _x64dbgapi.new_ModuleInfoArray(*args)
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _x64dbgapi.delete_ModuleInfoArray
    __del__ = lambda self : None;
    def __getitem__(self, *args):
        """__getitem__(ModuleInfoArray self, size_t index) -> ModuleInfo"""
        return _x64dbgapi.ModuleInfoArray___getitem__(self, *args)

    def __setitem__(self, *args):
        """__setitem__(ModuleInfoArray self, size_t index, ModuleInfo value)"""
        return _x64dbgapi.ModuleInfoArray___setitem__(self, *args)

    def cast(self):
        """cast(ModuleInfoArray self) -> ModuleInfo"""
        return _x64dbgapi.ModuleInfoArray_cast(self)

    def frompointer(*args):
        """frompointer(ModuleInfo t) -> ModuleInfoArray"""
        return _x64dbgapi.ModuleInfoArray_frompointer(*args)

    frompointer = staticmethod(frompointer)
ModuleInfoArray_swigregister = _x64dbgapi.ModuleInfoArray_swigregister
ModuleInfoArray_swigregister(ModuleInfoArray)

def ModuleInfoArray_frompointer(*args):
  """ModuleInfoArray_frompointer(ModuleInfo t) -> ModuleInfoArray"""
  return _x64dbgapi.ModuleInfoArray_frompointer(*args)

class ModuleSectionInfoArray(object):
    """Proxy of C++ ModuleSectionInfoArray class"""
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    def __init__(self, *args): 
        """__init__(ModuleSectionInfoArray self, size_t nelements) -> ModuleSectionInfoArray"""
        this = _x64dbgapi.new_ModuleSectionInfoArray(*args)
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _x64dbgapi.delete_ModuleSectionInfoArray
    __del__ = lambda self : None;
    def __getitem__(self, *args):
        """__getitem__(ModuleSectionInfoArray self, size_t index) -> ModuleSectionInfo"""
        return _x64dbgapi.ModuleSectionInfoArray___getitem__(self, *args)

    def __setitem__(self, *args):
        """__setitem__(ModuleSectionInfoArray self, size_t index, ModuleSectionInfo value)"""
        return _x64dbgapi.ModuleSectionInfoArray___setitem__(self, *args)

    def cast(self):
        """cast(ModuleSectionInfoArray self) -> ModuleSectionInfo"""
        return _x64dbgapi.ModuleSectionInfoArray_cast(self)

    def frompointer(*args):
        """frompointer(ModuleSectionInfo t) -> ModuleSectionInfoArray"""
        return _x64dbgapi.ModuleSectionInfoArray_frompointer(*args)

    frompointer = staticmethod(frompointer)
ModuleSectionInfoArray_swigregister = _x64dbgapi.ModuleSectionInfoArray_swigregister
ModuleSectionInfoArray_swigregister(ModuleSectionInfoArray)

def ModuleSectionInfoArray_frompointer(*args):
  """ModuleSectionInfoArray_frompointer(ModuleSectionInfo t) -> ModuleSectionInfoArray"""
  return _x64dbgapi.ModuleSectionInfoArray_frompointer(*args)

class SymbolInfoArray(object):
    """Proxy of C++ SymbolInfoArray class"""
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    def __init__(self, *args): 
        """__init__(SymbolInfoArray self, size_t nelements) -> SymbolInfoArray"""
        this = _x64dbgapi.new_SymbolInfoArray(*args)
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _x64dbgapi.delete_SymbolInfoArray
    __del__ = lambda self : None;
    def __getitem__(self, *args):
        """__getitem__(SymbolInfoArray self, size_t index) -> SymbolInfo"""
        return _x64dbgapi.SymbolInfoArray___getitem__(self, *args)

    def __setitem__(self, *args):
        """__setitem__(SymbolInfoArray self, size_t index, SymbolInfo value)"""
        return _x64dbgapi.SymbolInfoArray___setitem__(self, *args)

    def cast(self):
        """cast(SymbolInfoArray self) -> SymbolInfo"""
        return _x64dbgapi.SymbolInfoArray_cast(self)

    def frompointer(*args):
        """frompointer(SymbolInfo t) -> SymbolInfoArray"""
        return _x64dbgapi.SymbolInfoArray_frompointer(*args)

    frompointer = staticmethod(frompointer)
SymbolInfoArray_swigregister = _x64dbgapi.SymbolInfoArray_swigregister
SymbolInfoArray_swigregister(SymbolInfoArray)

def SymbolInfoArray_frompointer(*args):
  """SymbolInfoArray_frompointer(SymbolInfo t) -> SymbolInfoArray"""
  return _x64dbgapi.SymbolInfoArray_frompointer(*args)


def new_intp():
  """new_intp() -> int *"""
  return _x64dbgapi.new_intp()

def copy_intp(*args):
  """copy_intp(int value) -> int *"""
  return _x64dbgapi.copy_intp(*args)

def delete_intp(*args):
  """delete_intp(int * obj)"""
  return _x64dbgapi.delete_intp(*args)

def intp_assign(*args):
  """intp_assign(int * obj, int value)"""
  return _x64dbgapi.intp_assign(*args)

def intp_value(*args):
  """intp_value(int * obj) -> int"""
  return _x64dbgapi.intp_value(*args)

def new_uintp():
  """new_uintp() -> unsigned int *"""
  return _x64dbgapi.new_uintp()

def copy_uintp(*args):
  """copy_uintp(unsigned int value) -> unsigned int *"""
  return _x64dbgapi.copy_uintp(*args)

def delete_uintp(*args):
  """delete_uintp(unsigned int * obj)"""
  return _x64dbgapi.delete_uintp(*args)

def uintp_assign(*args):
  """uintp_assign(unsigned int * obj, unsigned int value)"""
  return _x64dbgapi.uintp_assign(*args)

def uintp_value(*args):
  """uintp_value(unsigned int * obj) -> unsigned int"""
  return _x64dbgapi.uintp_value(*args)

def new_duintp():
  """new_duintp() -> duint *"""
  return _x64dbgapi.new_duintp()

def copy_duintp(*args):
  """copy_duintp(duint value) -> duint *"""
  return _x64dbgapi.copy_duintp(*args)

def delete_duintp(*args):
  """delete_duintp(duint * obj)"""
  return _x64dbgapi.delete_duintp(*args)

def duintp_assign(*args):
  """duintp_assign(duint * obj, duint value)"""
  return _x64dbgapi.duintp_assign(*args)

def duintp_value(*args):
  """duintp_value(duint * obj) -> duint"""
  return _x64dbgapi.duintp_value(*args)


