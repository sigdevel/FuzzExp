




























from __future__ import print_function, absolute_import, division, unicode_literals

__version__          =  "0.17.10"
__ordering_version__ = b"0.6.4"  

import sys, argparse, itertools, string, re, multiprocessing, signal, os, cPickle, gc, \
       time, timeit, hashlib, collections, base64, struct, atexit, zlib, math, json, numbers





def full_version():
    from struct import calcsize
    return "btcrecover {} on Python {} {}-bit, {}-bit unicodes, {}-bit ints".format(
        __version__,
        ".".join(str(i) for i in sys.version_info[:3]),
        calcsize(b"P") * 8,
        sys.maxunicode.bit_length(),
        sys.maxint.bit_length() + 1
    )



def enable_unicode_mode():
    global io, tstr, tstr_from_stdin, tchr
    import locale, io
    tstr              = unicode
    preferredencoding = locale.getpreferredencoding()
    tstr_from_stdin   = lambda s: s if isinstance(s, unicode) else unicode(s, preferredencoding)
    tchr              = unichr

def enable_ascii_mode():
    global io, tstr, tstr_from_stdin, tchr
    io              = None
    tstr            = str
    tstr_from_stdin = str
    tchr            = chr









def init_wildcards():
    global wildcard_sets, wildcard_keys, wildcard_nocase_sets, wildcard_re, \
           custom_wildcard_cache, backreference_maps, backreference_maps_sha1
    
    
    wildcard_sets = {
        tstr("d") : tstr(string.digits),
        tstr("a") : tstr(string.lowercase),
        tstr("A") : tstr(string.uppercase),
        tstr("n") : tstr(string.lowercase + string.digits),
        tstr("N") : tstr(string.uppercase + string.digits),
        tstr("s") : tstr(" "),        
        tstr("l") : tstr("\n"),       
        tstr("r") : tstr("\r"),       
        tstr("R") : tstr("\n\r"),     
        tstr("t") : tstr("\t"),       
        tstr("T") : tstr(" \t"),      
        tstr("w") : tstr(" \r\n"),    
        tstr("W") : tstr(" \r\n\t"),  
        tstr("y") : tstr(string.punctuation),
        tstr("Y") : tstr(string.digits + string.punctuation),
        tstr("p") : tstr().join(map(tchr, xrange(33, 127))),  
        tstr("P") : tstr().join(map(tchr, xrange(33, 127))) + tstr(" \r\n\t"),  
        
        tstr("%") : tstr("%"),
        tstr("^") : tstr("^"),
        tstr("S") : tstr("$")  "S", the value is a dollar sign
    }
    wildcard_keys = tstr().join(wildcard_sets)
    
    
    wildcard_nocase_sets = {
        tstr("a") : tstr(string.lowercase + string.uppercase),
        tstr("A") : tstr(string.uppercase + string.lowercase),
        tstr("n") : tstr(string.lowercase + string.uppercase + string.digits),
        tstr("N") : tstr(string.uppercase + string.lowercase + string.digits)
    }
    
    wildcard_re = None
    custom_wildcard_cache   = dict()
    backreference_maps      = dict()
    backreference_maps_sha1 = None










def typo_repeat(p, i): return 2 * p[i],  
def typo_delete(p, i): return tstr(""),  
def typo_case(p, i):                     
    swapped = p[i].swapcase()            
    return (swapped,) if swapped != p[i] else ()

def typo_closecase(p, i):  
    cur_case_id = case_id_of(p[i])  
    if cur_case_id == UNCASED_ID: return ()
    if i==0 or i+1==len(p) or \
            case_id_changed(case_id_of(p[i-1]), cur_case_id) or \
            case_id_changed(case_id_of(p[i+1]), cur_case_id):
        return p[i].swapcase(),
    return ()

def typo_replace_wildcard(p, i): return [e for e in typos_replace_expanded if e != p[i]]
def typo_map(p, i):              return typos_map.get(p[i], ())



"typos-" + key_name; associated value is



simple_typos = collections.OrderedDict()
simple_typos["repeat"]    = typo_repeat
simple_typos["delete"]    = typo_delete
simple_typos["case"]      = typo_case
simple_typos["closecase"] = typo_closecase
simple_typos["replace"]   = typo_replace_wildcard
simple_typos["map"]       = typo_map



simple_typo_args = collections.OrderedDict()
simple_typo_args["repeat"]    = dict( action="store_true",       help="repeat (double) a character" )
simple_typo_args["delete"]    = dict( action="store_true",       help="delete a character" )
simple_typo_args["case"]      = dict( action="store_true",       help="change the case (upper/lower) of a letter" )
simple_typo_args["closecase"] = dict( action="store_true",       help="like --typos-case, but only change letters next to those with a different case")
simple_typo_args["map"]       = dict( metavar="FILE",            help="replace specific characters based on a map file" )
simple_typo_args["replace"]   = dict( metavar="WILDCARD-STRING", help="replace a character with another string or wildcard" )



wallet_types       = []
wallet_types_by_id = {}
def register_wallet_class(cls):
    global wallet_types, wallet_types_by_id
    wallet_types.append(cls)
    try:
        assert cls.data_extract_id not in wallet_types_by_id,\
            "register_wallet_class: registered wallet types must have unique data_extract_id's"
        wallet_types_by_id[cls.data_extract_id] = cls
    except AttributeError: pass
    return cls


def clear_registered_wallets():
    global wallet_types, wallet_types_by_id
    wallet_types       = []
    wallet_types_by_id = {}



MAX_WALLET_FILE_SIZE = 64 * 2**20  


def load_wallet(wallet_filename):
    
    
    uncertain_wallet_types = []
    with open(wallet_filename, "rb") as wallet_file:
        for wallet_type in wallet_types:
            found = wallet_type.is_wallet_file(wallet_file)
            if found:
                wallet_file.close()
                return wallet_type.load_from_filename(wallet_filename)
            elif found is None:  
                uncertain_wallet_types.append(wallet_type)

    
    
    uncertain_errors = []
    for wallet_type in uncertain_wallet_types:
        try:
            return wallet_type.load_from_filename(wallet_filename)
        except ValueError as e:
            uncertain_errors.append(wallet_type.__name__ + ": " + unicode(e))

    error_exit("unrecognized wallet format" +
        ("; heuristic parser(s) reported:\n    " + "\n    ".join(uncertain_errors) if uncertain_errors else "") )


def load_global_wallet(wallet_filename):
    global loaded_wallet
    loaded_wallet = load_wallet(wallet_filename)



def load_from_base64_key(key_crc_base64):
    global loaded_wallet

    try:   key_crc_data = base64.b64decode(key_crc_base64)
    except TypeError: error_exit("encrypted key data is corrupted (invalid base64)")

    
    if len(key_crc_data) < 8:
        error_exit("encrypted key data is corrupted (too short)")
    key_data = key_crc_data[:-4]
    (key_crc,) = struct.unpack(b"<I", key_crc_data[-4:])
    if zlib.crc32(key_data) & 0xffffffff != key_crc:
        error_exit("encrypted key data is corrupted (failed CRC check)")

    wallet_type = wallet_types_by_id.get(key_data[:2])
    if not wallet_type:
        error_exit("unrecognized encrypted key type '"+key_data[:3]+"'")

    loaded_wallet = wallet_type.load_from_data_extract(key_data[3:])
    return key_crc



cl_devices_avail = None
def get_opencl_devices():
    global pyopencl, numpy, cl_devices_avail
    if cl_devices_avail is None:
        try:
            import pyopencl, numpy
            cl_devices_avail = filter(lambda d: d.available==1 and d.profile=="FULL_PROFILE" and d.endian_little==1,
                itertools.chain(*[p.get_devices() for p in pyopencl.get_platforms()]))
        except ImportError as e:
            print(prog+": warning:", e, file=sys.stderr)
            cl_devices_avail = []
        except pyopencl.LogicError as e:
            if "platform not found" not in unicode(e): raise  
            cl_devices_avail = []  
    return cl_devices_avail



def est_entropy_bits(data):
    hist_bins = [0] * 256
    for byte in data:
        hist_bins[ord(byte)] += 1
    entropy_bits = 0.0
    for frequency in hist_bins:
        if frequency:
            prob = float(frequency) / len(data)
            entropy_bits += prob * math.log(prob, 2)
    return entropy_bits * -1


def prompt_unicode_password(prompt, error_msg):
    assert isinstance(prompt, str), "getpass() doesn't support Unicode on all platforms"
    from getpass import getpass
    encoding = sys.stdin.encoding or 'ASCII'
    if 'utf' not in encoding.lower():
        print(prog+": warning: terminal does not support UTF; passwords with non-ASCII chars might not work", file=sys.stderr)
    prompt = b"(note your password will not be displayed as you type)\n" + prompt
    password = getpass(prompt)
    if not password:
        error_exit(error_msg)
    if isinstance(password, str):
        password = password.decode(encoding)  
    return password





is_armory_path_added = False
def add_armory_library_path():
    global is_armory_path_added
    if is_armory_path_added: return
    if sys.platform == "win32":
        progfiles_path = os.environ.get("ProgramFiles",  r"C:\Program Files")  
        armory_path    = progfiles_path + r"\Armory"
        sys.path.extend((armory_path, armory_path + r"\library.zip"))
        
        if struct.calcsize(b"P") * 8 == 64:  
            assert not progfiles_path.endswith("(x86)"), "ProgramFiles doesn't end with '(x86)' on x64 Python"
            progfiles_path += " (x86)"
            armory_path     = progfiles_path + r"\Armory"
            sys.path.extend((armory_path, armory_path + r"\library.zip"))
    elif sys.platform.startswith("linux"):
        sys.path.extend(("/usr/local/lib/armory", "/usr/lib/armory"))
    elif sys.platform == "darwin":
        import glob
        sys.path.extend((
            "/Applications/Armory.app/Contents/MacOS/py/usr/local/lib/armory",
            "/Applications/Armory.app/Contents/MacOS/py/usr/lib/armory",
            "/Applications/Armory.app/Contents/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages"))
        sys.path.extend(glob.iglob(
            "/Applications/Armory.app/Contents/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/*.egg"))
    is_armory_path_added = True

is_armory_loaded = False
def load_armory_library():
    if tstr == unicode:
        error_exit("armory wallets do not support unicode; please remove the --utf8 option")
    global is_armory_loaded
    if is_armory_loaded: return

    
    
    old_argv = sys.argv[1:]
    sys.argv[1:] = ["--language", "es"]

    add_armory_library_path()
    try:
        
        
        import random
        for i in xrange(10):
            try:
                from armoryengine.ArmoryUtils import getVersionInt, readVersionString, BTCARMORY_VERSION
            except IOError as e:
                if i<9 and e.filename.endswith(r"\armorylog.txt"):
                    time.sleep(random.uniform(0.05, 0.15))
                else: raise  
            except SystemExit:
                if len(sys.argv) == 3:
                    del sys.argv[1:]  
                else: raise  
            except ImportError as e:
                if "not a valid Win32 application" in unicode(e):
                    print(prog+": error: can't load Armory, 32/64 bit mismatch between it and Python", file=sys.stderr)
                raise
            else: break  

        
        if getVersionInt(BTCARMORY_VERSION) < getVersionInt(readVersionString("0.92")):
            error_exit("Armory version 0.92 or greater is required")

        
        global PyBtcWallet, PyBtcAddress, SecureBinaryData, KdfRomix
        from armoryengine.PyBtcWallet import PyBtcWallet
        from armoryengine.PyBtcWallet import PyBtcAddress
        from CppBlockUtils import SecureBinaryData, KdfRomix
        is_armory_loaded = True

    finally:
        sys.argv[1:] = old_argv  

@register_wallet_class
class WalletArmory(object):

    class __metaclass__(type):
        @property
        def data_extract_id(cls): return b"ar"

    @staticmethod
    def passwords_per_seconds(seconds):
        return max(int(round(4 * seconds)), 1)

    @staticmethod
    def is_wallet_file(wallet_file):
        wallet_file.seek(0)
        return wallet_file.read(8) == b"\xbaWALLET\x00"  

    def __init__(self, loading = False):
        assert loading, 'use load_from_* to create a ' + self.__class__.__name__
        load_armory_library()

    def __getstate__(self):
        
        state = self.__dict__.copy()
        del state["_address"], state["_kdf"]
        state["addrStr20"]         = self._address.addrStr20
        state["binPrivKey32_Encr"] = self._address.binPrivKey32_Encr.toBinStr()
        state["binInitVect16"]     = self._address.binInitVect16.toBinStr()
        state["binPublicKey65"]    = self._address.binPublicKey65.toBinStr()
        state["memoryReqtBytes"]   = self._kdf.getMemoryReqtBytes()
        state["numIterations"]     = self._kdf.getNumIterations()
        state["salt"]              = self._kdf.getSalt().toBinStr()
        return state

    def __setstate__(self, state):
        
        global tstr
        try:
            assert tstr == str  
        except NameError:       
            tstr = str          
        load_armory_library()
        
        state["_address"] = PyBtcAddress().createFromEncryptedKeyData(
            state["addrStr20"],
            SecureBinaryData(state["binPrivKey32_Encr"]),
            SecureBinaryData(state["binInitVect16"]),
            pubKey=state["binPublicKey65"]  
        )
        del state["addrStr20"],     state["binPrivKey32_Encr"]
        del state["binInitVect16"], state["binPublicKey65"]
        
        state["_kdf"] = KdfRomix(
            state["memoryReqtBytes"],
            state["numIterations"],
            SecureBinaryData(state["salt"])
        )
        del state["memoryReqtBytes"], state["numIterations"], state["salt"]
        
        self.__dict__ = state

    
    @classmethod
    def load_from_filename(cls, wallet_filename):
        self = cls(loading=True)
        wallet = PyBtcWallet().readWalletFile(wallet_filename)
        self._address = wallet.addrMap['ROOT']
        self._kdf     = wallet.kdf
        if not self._address.hasPrivKey():
            error_exit("Armory wallet cannot be watching-only")
        if not self._address.useEncryption :
            error_exit("Armory wallet is not encrypted")
        return self

    
    @classmethod
    def load_from_data_extract(cls, privkey_data):
        self = cls(loading=True)
        self._address = PyBtcAddress().createFromEncryptedKeyData(
            privkey_data[:20],                      
            SecureBinaryData(privkey_data[20:52]),  
            SecureBinaryData(privkey_data[52:68])   
        )
        bytes_reqd, iter_count = struct.unpack(b"< I I", privkey_data[68:76])
        self._kdf = KdfRomix(bytes_reqd, iter_count, SecureBinaryData(privkey_data[76:]))  
        return self

    def difficulty_info(self):
        return "{:g} MiB, {} iterations + ECC".format(round(self._kdf.getMemoryReqtBytes() / 1024**2, 2), self._kdf.getNumIterations())

    
    def return_verified_password_or_false(self, passwords):
        return self._return_verified_password_or_false_opencl(passwords) if hasattr(self, "_cl_devices") \
          else self._return_verified_password_or_false_cpu(passwords)

    
    
    def _return_verified_password_or_false_cpu(self, passwords):
        for count, password in enumerate(passwords, 1):
            if self._address.verifyEncryptionKey(self._kdf.DeriveKey(SecureBinaryData(password))):
                return password, count
        else:
            return False, count

    
    
    
    
    
    
    
    
    def init_opencl_kernel(self, devices, global_ws, local_ws, int_rate, save_every = 1, calc_memory = False):
        
        assert devices, "WalletArmory.init_opencl_kernel: at least one device is selected"
        assert len(devices) == len(global_ws) == len(local_ws), "WalletArmory.init_opencl_kernel: one global_ws and one local_ws specified for each device"
        assert save_every > 0
        self._cl_devices   = devices
        self._cl_global_ws = global_ws
        self._cl_local_ws  = local_ws

        self._cl_V_buffer0s = self._cl_V_buffer1s = self._cl_V_buffer2s = self._cl_V_buffer3s = None  
        self._cl_kernel = self._cl_kernel_fill = self._cl_queues = self._cl_hashes_buffers = None     
        cl_context = pyopencl.Context(devices)
        
        
        assert  self._kdf.getMemoryReqtBytes() % 64 == 0
        v_len = self._kdf.getMemoryReqtBytes() // 64
        salt  = self._kdf.getSalt().toBinStr()
        assert len(salt) == 32
        with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "romix-ar-kernel.cl")) as opencl_file:
            cl_program = pyopencl.Program(cl_context, opencl_file.read()).build(
                b"-w -D SAVE_EVERY={}U -D V_LEN={}U -D SALT0=0x{:016x}UL -D SALT1=0x{:016x}UL -D SALT2=0x{:016x}UL -D SALT3=0x{:016x}UL" \
                .format(save_every, v_len, *struct.unpack(b">4Q", salt)))
        
        
        self._cl_kernel_fill = cl_program.kernel_fill_V    
        self._cl_kernel      = cl_program.kernel_lookup_V  
        self._cl_kernel_fill.set_scalar_arg_dtypes([None, None, None, None, numpy.uint32, numpy.uint32, None, numpy.uint8])
        self._cl_kernel     .set_scalar_arg_dtypes([None, None, None, None, numpy.uint32, None])
        
        
        for i, device in enumerate(devices):
            if local_ws[i] is None: continue
            max_local_ws = min(self._cl_kernel_fill.get_work_group_info(pyopencl.kernel_work_group_info.WORK_GROUP_SIZE, device),
                               self._cl_kernel     .get_work_group_info(pyopencl.kernel_work_group_info.WORK_GROUP_SIZE, device))
            if local_ws[i] > max_local_ws:
                error_exit("--local-ws of", local_ws[i], "exceeds max of", max_local_ws, "for GPU '"+device.name.strip()+"' with Armory wallets")

        if calc_memory:
            mem_per_worker = math.ceil(v_len / save_every) * 64 + 64
            print(    "Details for this wallet")
            print(    "  ROMix V-table length:  {:,}".format(v_len))
            print(    "  outer iteration count: {:,}".format(self._kdf.getNumIterations()))
            print(    "  with --mem-factor {},".format(save_every if save_every>1 else "1 (the default)"))
            print(    "    memory per global worker: {:,} KiB\n".format(int(round(mem_per_worker / 1024))))
            
            for i, device in enumerate(devices):
                print("Details for", device.name.strip())
                print("  global memory size:     {:,} MiB".format(int(round(device.global_mem_size / float(1024**2)))))
                print("  with --mem-factor {},".format(save_every if save_every>1 else "1 (the default)"))
                print("    est. max --global-ws: {}".format((int(device.global_mem_size // mem_per_worker) // 32 * 32)))
                print("    with --global-ws {},".format(global_ws[i] if global_ws[i]!=4096 else "4096 (the default)"))
                print("      est. memory usage:  {:,} MiB\n".format(int(round(global_ws[i] * mem_per_worker / float(1024**2)))))
            sys.exit(0)

        "V" buffers per device
        self._cl_queues         = []
        self._cl_hashes_buffers = []
        self._cl_V_buffer0s     = []
        self._cl_V_buffer1s     = []
        self._cl_V_buffer2s     = []
        self._cl_V_buffer3s     = []
        for i, device in enumerate(devices):
            self._cl_queues.append(pyopencl.CommandQueue(cl_context, device))
            
            self._cl_hashes_buffers.append(pyopencl.Buffer(cl_context, pyopencl.mem_flags.READ_WRITE, global_ws[i] * 64))
            
            "V" buffers total v_len * 64 * --global-ws bytes per device. There are four
            
            
            assert global_ws[i] % 4 == 0  
            V_buffer_len = int(math.ceil(v_len / save_every)) * 64 * global_ws[i] // 4
            self._cl_V_buffer0s.append(pyopencl.Buffer(cl_context, pyopencl.mem_flags.READ_WRITE, V_buffer_len))
            self._cl_V_buffer1s.append(pyopencl.Buffer(cl_context, pyopencl.mem_flags.READ_WRITE, V_buffer_len))
            self._cl_V_buffer2s.append(pyopencl.Buffer(cl_context, pyopencl.mem_flags.READ_WRITE, V_buffer_len))
            self._cl_V_buffer3s.append(pyopencl.Buffer(cl_context, pyopencl.mem_flags.READ_WRITE, V_buffer_len))

        
        
        
        
        int_rate = int(round(int_rate / self._kdf.getNumIterations())) or 1  
        self._v_len_chunksize = v_len // int_rate or 1
        if self._v_len_chunksize % int_rate != 0:  
            self._v_len_chunksize += 1             
        if self._v_len_chunksize % 2 != 0:         
            self._v_len_chunksize += 1             

    def _return_verified_password_or_false_opencl(self, passwords):
        assert len(passwords) <= sum(self._cl_global_ws), "WalletArmory.return_verified_password_or_false_opencl: at most --global-ws passwords"

        
        salt = self._kdf.getSalt().toBinStr()
        hashes = numpy.empty([sum(self._cl_global_ws), 64], numpy.uint8)
        for i, password in enumerate(passwords):
            hashes[i] = numpy.fromstring(hashlib.sha512(password + salt).digest(), numpy.uint8)

        
        done   = []  
        offset = 0
        for devnum, ws in enumerate(self._cl_global_ws):
            done.append(pyopencl.enqueue_copy(self._cl_queues[devnum], self._cl_hashes_buffers[devnum],
                                              hashes[offset : offset + ws], is_blocking=False))
            self._cl_queues[devnum].flush()  
            offset += ws
        pyopencl.wait_for_events(done)

        v_len = self._kdf.getMemoryReqtBytes() // 64
        for i in xrange(self._kdf.getNumIterations()):

            
            
            
            

            "V" lookup table.

            v_start = -self._v_len_chunksize  
            for v_start in xrange(0, v_len - self._v_len_chunksize, self._v_len_chunksize):
                done = []  
                
                for devnum in xrange(len(self._cl_devices)):
                    done.append(self._cl_kernel_fill(
                        self._cl_queues[devnum], (self._cl_global_ws[devnum],),
                        None if self._cl_local_ws[devnum] is None else (self._cl_local_ws[devnum],),
                        self._cl_V_buffer0s[devnum], self._cl_V_buffer1s[devnum], self._cl_V_buffer2s[devnum], self._cl_V_buffer3s[devnum],
                        v_start, self._v_len_chunksize, self._cl_hashes_buffers[devnum], 0 == v_start == i))
                    self._cl_queues[devnum].flush()  
                pyopencl.wait_for_events(done)

            
            done = []  
            for devnum in xrange(len(self._cl_devices)):
                done.append(self._cl_kernel_fill(
                    self._cl_queues[devnum], (self._cl_global_ws[devnum],),
                    None if self._cl_local_ws[devnum] is None else (self._cl_local_ws[devnum],),
                    self._cl_V_buffer0s[devnum], self._cl_V_buffer1s[devnum], self._cl_V_buffer2s[devnum], self._cl_V_buffer3s[devnum],
                    v_start + self._v_len_chunksize, v_len - self._v_len_chunksize - v_start, self._cl_hashes_buffers[devnum], v_start<0 and i==0))
                self._cl_queues[devnum].flush()  
            pyopencl.wait_for_events(done)

            "V" lookup table to complete
            

            assert self._v_len_chunksize % 2 == 0
            v_start = -self._v_len_chunksize//2  
            for v_start in xrange(0, v_len//2 - self._v_len_chunksize//2, self._v_len_chunksize//2):
                done = []  
                
                for devnum in xrange(len(self._cl_devices)):
                    done.append(self._cl_kernel(
                        self._cl_queues[devnum], (self._cl_global_ws[devnum],),
                        None if self._cl_local_ws[devnum] is None else (self._cl_local_ws[devnum],),
                        self._cl_V_buffer0s[devnum], self._cl_V_buffer1s[devnum], self._cl_V_buffer2s[devnum], self._cl_V_buffer3s[devnum],
                        self._v_len_chunksize//2, self._cl_hashes_buffers[devnum]))
                    self._cl_queues[devnum].flush()  
                pyopencl.wait_for_events(done)

            
            done = []  
            for devnum in xrange(len(self._cl_devices)):
                done.append(self._cl_kernel(
                    self._cl_queues[devnum], (self._cl_global_ws[devnum],),
                    None if self._cl_local_ws[devnum] is None else (self._cl_local_ws[devnum],),
                    self._cl_V_buffer0s[devnum], self._cl_V_buffer1s[devnum], self._cl_V_buffer2s[devnum], self._cl_V_buffer3s[devnum],
                    v_len//2 - self._v_len_chunksize//2 - v_start, self._cl_hashes_buffers[devnum]))
                self._cl_queues[devnum].flush()  
            pyopencl.wait_for_events(done)

        
        done   = []  
        offset = 0
        for devnum, ws in enumerate(self._cl_global_ws):
            done.append(pyopencl.enqueue_copy(self._cl_queues[devnum], hashes[offset : offset + ws],
                                              self._cl_hashes_buffers[devnum], is_blocking=False))
            offset += ws
            self._cl_queues[devnum].flush()  
        pyopencl.wait_for_events(done)

        
        for i, password in enumerate(passwords):
            if self._address.verifyEncryptionKey(hashes[i,:32].tostring()):
                return password, i + 1

        return False, i + 1




@register_wallet_class
class WalletBitcoinCore(object):

    class __metaclass__(type):
        @property
        def data_extract_id(cls): return b"bc"

    @staticmethod
    def passwords_per_seconds(seconds):
        return max(int(round(10 * seconds)), 1)

    @staticmethod
    def is_wallet_file(wallet_file):
        wallet_file.seek(12)
        return wallet_file.read(8) == b"\x62\x31\x05\x00\x09\x00\x00\x00"  

    def __init__(self, loading = False):
        assert loading, 'use load_from_* to create a ' + self.__class__.__name__
        load_aes256_library()

    def __setstate__(self, state):
        
        load_aes256_library(warnings=False)
        self.__dict__ = state

    
    @classmethod
    def load_from_filename(cls, wallet_filename, force_purepython = False):
        if not force_purepython:
            try:
                import bsddb.db
            except ImportError:
                force_purepython = True

        if not force_purepython:
            db_env = bsddb.db.DBEnv()
            wallet_filename = os.path.abspath(wallet_filename)
            try:
                db_env.open(os.path.dirname(wallet_filename), bsddb.db.DB_CREATE | bsddb.db.DB_INIT_MPOOL)
                db = bsddb.db.DB(db_env)
                db.open(wallet_filename, b"main", bsddb.db.DB_BTREE, bsddb.db.DB_RDONLY)
            except UnicodeEncodeError:
                error_exit("the entire path and filename of Bitcoin Core wallets must be entirely ASCII")
            mkey = db.get(b"\x04mkey\x01\x00\x00\x00")
            db.close()
            db_env.close()

        else:
            def align_32bits(i):  
                m = i % 4
                return i if m == 0 else i + 4 - m

            with open(wallet_filename, "rb") as wallet_file:
                wallet_file.seek(12)
                assert wallet_file.read(8) == b"\x62\x31\x05\x00\x09\x00\x00\x00", "is a Btree v9 file"
                mkey = None

                
                
                wallet_file.seek(20)
                page_size        = struct.unpack(b"<I", wallet_file.read(4))[0]
                wallet_file_size = os.path.getsize(wallet_filename)
                for page_base in xrange(page_size, wallet_file_size, page_size):  
                    wallet_file.seek(page_base + 20)
                    (item_count, first_item_pos, btree_level, page_type) = struct.unpack(b"< H H B B", wallet_file.read(6))
                    if page_type != 5 or btree_level != 1:
                        continue  
                    pos = align_32bits(page_base + first_item_pos)  
                    wallet_file.seek(pos)
                    for i in xrange(item_count):    
                        (item_len, item_type) = struct.unpack(b"< H B", wallet_file.read(3))
                        if item_type & ~0x80 == 1:  
                            if item_type == 1:      
                                if i % 2 == 0:      
                                    value_pos = pos + 3
                                    value_len = item_len
                                
                                elif item_len == 9 and wallet_file.read(item_len) == b"\x04mkey\x01\x00\x00\x00":
                                    wallet_file.seek(value_pos)
                                    mkey = wallet_file.read(value_len)  
                                    break
                            pos = align_32bits(pos + 3 + item_len)  
                        else:
                            pos += 12  
                        if i + 1 < item_count:  
                            assert pos < page_base + page_size, "next item is located in current page"
                            wallet_file.seek(pos)
                    else: continue  
                    break           

        if not mkey:
            if force_purepython:
                print(prog+": warning: bsddb (Berkeley DB) module not found; try installing it to resolve key-not-found errors (see INSTALL.md)", file=sys.stderr)
            raise ValueError("Encrypted master key "+
                             "(is this wallet encrypted? is this a standard Bitcoin Core wallet?)")
        
        
        
        self = cls(loading=True)
        encrypted_master_key, self._salt, method, self._iter_count = struct.unpack_from(b"< 49p 9p I I", mkey)
        if method != 0: raise NotImplementedError("Unsupported Bitcoin Core key derivation method " + unicode(method))

        
        self._part_encrypted_master_key = encrypted_master_key[-32:]
        return self

    
    @classmethod
    def load_from_data_extract(cls, mkey_data):
        
        self = cls(loading=True)
        self._part_encrypted_master_key, self._salt, self._iter_count = struct.unpack(b"< 32s 8s I", mkey_data)
        return self

    def difficulty_info(self):
        return "{:,} SHA-512 iterations".format(self._iter_count)

    
    def return_verified_password_or_false(self, passwords):
        return self._return_verified_password_or_false_opencl(passwords) if hasattr(self, "_cl_devices") \
          else self._return_verified_password_or_false_cpu(passwords)

    
    
    def _return_verified_password_or_false_cpu(self, passwords):
        
        l_sha512 = hashlib.sha512

        
        if tstr == unicode:
            passwords = itertools.imap(lambda p: p.encode("utf_8", "ignore"), passwords)

        for count, password in enumerate(passwords, 1):
            derived_key = password + self._salt
            for i in xrange(self._iter_count):
                derived_key = l_sha512(derived_key).digest()
            part_master_key = aes256_cbc_decrypt(derived_key[:32], self._part_encrypted_master_key[:16], self._part_encrypted_master_key[16:])
            
            
            if part_master_key == b"\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10":
                return password if tstr == str else password.decode("utf_8", "replace"), count

        return False, count

    
    
    
    
    
    
    def init_opencl_kernel(self, devices, global_ws, local_ws, int_rate):
        
        assert devices, "WalletBitcoinCore.init_opencl_kernel: at least one device is selected"
        assert len(devices) == len(global_ws) == len(local_ws), "WalletBitcoinCore.init_opencl_kernel: one global_ws and one local_ws specified for each device"
        self._cl_devices   = devices
        self._cl_global_ws = global_ws
        self._cl_local_ws  = local_ws

        self._cl_kernel = self._cl_queues = self._cl_hashes_buffers = None  
        cl_context = pyopencl.Context(devices)
        
        
        cl_program = pyopencl.Program(cl_context, open(
            os.path.join(os.path.dirname(os.path.realpath(__file__)), "sha512-bc-kernel.cl"))
            .read()).build(b"-w")
        
        
        self._cl_kernel = cl_program.kernel_sha512_bc
        self._cl_kernel.set_scalar_arg_dtypes([None, numpy.uint32])
        
        
        for i, device in enumerate(devices):
            if local_ws[i] is None: continue
            max_local_ws = self._cl_kernel.get_work_group_info(pyopencl.kernel_work_group_info.WORK_GROUP_SIZE, device)
            if local_ws[i] > max_local_ws:
                error_exit("--local-ws of", local_ws[i], "exceeds max of", max_local_ws, "for GPU '"+device.name.strip()+"' with Bitcoin Core wallets")

        
        self._cl_queues         = []
        self._cl_hashes_buffers = []
        for i, device in enumerate(devices):
            self._cl_queues.append(pyopencl.CommandQueue(cl_context, device))
            
            self._cl_hashes_buffers.append(pyopencl.Buffer(cl_context, pyopencl.mem_flags.READ_WRITE, global_ws[i] * 64))

        
        
        
        assert hasattr(self, "_iter_count") and self._iter_count, "WalletBitcoinCore.init_opencl_kernel: bitcoin core wallet or mkey has been loaded"
        self._iter_count_chunksize = self._iter_count // int_rate or 1
        if self._iter_count_chunksize % int_rate != 0:  
            self._iter_count_chunksize += 1             

    def _return_verified_password_or_false_opencl(self, passwords):
        assert len(passwords) <= sum(self._cl_global_ws), "WalletBitcoinCore.return_verified_password_or_false_opencl: at most --global-ws passwords"

        
        if tstr == unicode:
            passwords = map(lambda p: p.encode("utf_8", "ignore"), passwords)

        
        hashes = numpy.empty([sum(self._cl_global_ws), 64], numpy.uint8)
        for i, password in enumerate(passwords):
            hashes[i] = numpy.fromstring(hashlib.sha512(password + self._salt).digest(), numpy.uint8)

        
        done   = []  
        offset = 0
        for devnum, ws in enumerate(self._cl_global_ws):
            done.append(pyopencl.enqueue_copy(self._cl_queues[devnum], self._cl_hashes_buffers[devnum],
                                              hashes[offset : offset + ws], is_blocking=False))
            self._cl_queues[devnum].flush()  
            offset += ws
        pyopencl.wait_for_events(done)

        
        
        
        

        i = 1 - self._iter_count_chunksize  
        for i in xrange(1, self._iter_count - self._iter_count_chunksize, self._iter_count_chunksize):
            done = []  
            
            for devnum in xrange(len(self._cl_devices)):
                done.append(self._cl_kernel(self._cl_queues[devnum], (self._cl_global_ws[devnum],),
                                            None if self._cl_local_ws[devnum] is None else (self._cl_local_ws[devnum],),
                                            self._cl_hashes_buffers[devnum], self._iter_count_chunksize))
                self._cl_queues[devnum].flush()  
            pyopencl.wait_for_events(done)

        
        done = []  
        for devnum in xrange(len(self._cl_devices)):
            done.append(self._cl_kernel(self._cl_queues[devnum], (self._cl_global_ws[devnum],),
                                        None if self._cl_local_ws[devnum] is None else (self._cl_local_ws[devnum],),
                                        self._cl_hashes_buffers[devnum], self._iter_count - self._iter_count_chunksize - i))
            self._cl_queues[devnum].flush()  
        pyopencl.wait_for_events(done)

        
        done   = []  
        offset = 0
        for devnum, ws in enumerate(self._cl_global_ws):
            done.append(pyopencl.enqueue_copy(self._cl_queues[devnum], hashes[offset : offset + ws],
                                              self._cl_hashes_buffers[devnum], is_blocking=False))
            offset += ws
            self._cl_queues[devnum].flush()  
        pyopencl.wait_for_events(done)

        
        for i, password in enumerate(passwords):
            derived_key = hashes[i].tostring()
            part_master_key = aes256_cbc_decrypt(derived_key[:32], self._part_encrypted_master_key[:16], self._part_encrypted_master_key[16:])
            
            if part_master_key == b"\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10":
                return password if tstr == str else password.decode("utf_8", "replace"), i + 1
        return False, i + 1


@register_wallet_class
class WalletPywallet(WalletBitcoinCore):

    class __metaclass__(WalletBitcoinCore.__metaclass__):
        @property
        def data_extract_id(cls):    return False  

    @staticmethod
    def is_wallet_file(wallet_file): return None   

    
    @classmethod
    def load_from_filename(cls, wallet_filename):
        
        
        
        
        
        
        with open(wallet_filename) as wallet_file:
            last_block = b""
            cur_block  = wallet_file.read(16384)
            if sum(1 for c in cur_block if ord(c)>126 or ord(c)==0) > 512: 
                raise ValueError("Unrecognized pywallet format (does not look like ASCII text)")
            while cur_block:
                found_at = cur_block.find(b'"nDerivation')
                if found_at >= 0: break
                last_block = cur_block
                cur_block  = wallet_file.read(16384)
            else:
                raise ValueError("Unrecognized pywallet format (can't find mkey)")

            cur_block = last_block + cur_block + wallet_file.read(4096)
        found_at = cur_block.rfind(b"{", 0, found_at + len(last_block))
        if found_at < 0:
            raise ValueError("Unrecognized pywallet format (can't find mkey opening brace)")
        wallet = json.JSONDecoder().raw_decode(cur_block[found_at:])[0]

        if not all(name in wallet for name in ("nDerivationIterations", "nDerivationMethod", "nID", "salt")):
            raise ValueError("Unrecognized pywallet format (can't find all mkey attributes)")

        if wallet["nID"] != 1:
            raise NotImplementedError("Unsupported Bitcoin Core wallet ID " + wallet["nID"])
        if wallet["nDerivationMethod"] != 0:
            raise NotImplementedError("Unsupported Bitcoin Core key derivation method " + wallet["nDerivationMethod"])

        if "encrypted_key" in wallet:
            encrypted_master_key = wallet["encrypted_key"]
        elif "crypted_key" in wallet:
            encrypted_master_key = wallet["crypted_key"]
        else:
            raise ValueError("Unrecognized pywallet format (can't find [en]crypted_key attribute)")

        
        self = cls(loading=True)
        encrypted_master_key = base64.b16decode(encrypted_master_key, casefold=True)
        self._salt           = base64.b16decode(wallet["salt"], True)
        self._iter_count     = int(wallet["nDerivationIterations"])

        if len(encrypted_master_key) != 48: raise NotImplementedError("Unsupported encrypted master key length")
        if len(self._salt)           != 8:  raise NotImplementedError("Unsupported salt length")
        if self._iter_count          <= 0:  raise NotImplementedError("Unsupported iteration count")

        
        self._part_encrypted_master_key = encrypted_master_key[-32:]
        return self










@register_wallet_class
class WalletMultiBit(object):

    class __metaclass__(type):
        @property
        def data_extract_id(cls): return b"mb"

    
    @staticmethod
    def is_wallet_file(wallet_file):
        wallet_file.seek(0)
        try:   data = base64.b64decode(wallet_file.read(20).lstrip()[:12])
        except TypeError: return False
        return data.startswith(b"Salted__")

    def __init__(self, loading = False):
        assert loading, 'use load_from_* to create a ' + self.__class__.__name__
        aes_library_name = load_aes256_library().__name__
        self._passwords_per_second = 100000 if aes_library_name == "Crypto" else 5000

    def __setstate__(self, state):
        
        load_aes256_library(warnings=False)
        self.__dict__ = state

    def passwords_per_seconds(self, seconds):
        return max(int(round(self._passwords_per_second * seconds)), 1)

    
    @classmethod
    def load_from_filename(cls, privkey_filename):
        with open(privkey_filename) as privkey_file:
            
            
            data = b"".join(privkey_file.read(70).split())  
        if len(data) < 64: raise EOFError("Expected at least 64 bytes of text in the MultiBit private key file")
        data = base64.b64decode(data[:64])
        assert data.startswith(b"Salted__"), "WalletBitcoinCore.load_from_filename: file starts with base64 'Salted__'"
        if len(data) < 48:  raise EOFError("Expected at least 48 bytes of decoded data in the MultiBit private key file")
        self = cls(loading=True)
        self._encrypted_block = data[16:48]  
        self._salt            = data[8:16]
        return self

    
    @classmethod
    def load_from_data_extract(cls, privkey_data):
        assert len(privkey_data) == 24
        print(prog + ": WARNING: read the Usage for MultiBit Classic section of Extract_Scripts.md before proceeding", file=sys.stderr)
        self = cls(loading=True)
        self._encrypted_block = privkey_data[8:]  
        self._salt            = privkey_data[:8]
        return self

    def difficulty_info(self):
        return "3 MD5 iterations"

    
    
    assert b"1" < b"9" < b"A" < b"Z" < b"a" < b"z"  
    def return_verified_password_or_false(self, orig_passwords):
        
        l_md5                 = hashlib.md5
        l_aes256_cbc_decrypt  = aes256_cbc_decrypt
        encrypted_block       = self._encrypted_block
        salt                  = self._salt

        
        if tstr == unicode:
            passwords = itertools.imap(lambda p: p.encode("utf_16_le", "ignore")[::2], orig_passwords)
        else:
            passwords = orig_passwords

        for count, password in enumerate(passwords, 1):
            salted = password + salt
            key1   = l_md5(salted).digest()
            key2   = l_md5(key1 + salted).digest()
            iv     = l_md5(key2 + salted).digest()
            b58_privkey = l_aes256_cbc_decrypt(key1 + key2, iv, encrypted_block[:16])

            
            if b58_privkey[0] in b"LK5Q\x0a":
                
                
                if b58_privkey[0] in b"LK5Q":  
                    for c in b58_privkey[1:]:
                        
                        if c > b"z" or c < b"1" or b"9" < c < b"A" or b"Z" < c < b"a" or c in b"IOl":
                            break
                    
                    else:
                        
                        if len(encrypted_block) >= 32:
                            b58_privkey = l_aes256_cbc_decrypt(key1 + key2, encrypted_block[:16], encrypted_block[16:32])
                            for c in b58_privkey:
                                if c > b"z" or c < b"1" or b"9" < c < b"A" or b"Z" < c < b"a" or c in b"IOl":
                                    break  
                            
                            else:
                                return orig_passwords[count-1], count
                        else:
                            
                            return orig_passwords[count - 1], count
                
                
                elif b58_privkey[2:6] == b"org." and b58_privkey[0] == b"\x0a" and ord(b58_privkey[1]) < 128:
                    for c in b58_privkey[6:14]:
                        
                        if c > b"z" or (c < b"a" and c != b"."):
                            break
                    
                    else:
                        return orig_passwords[count - 1], count
                
                
                elif b58_privkey == b"":
                    return orig_passwords[count-1], count

        return False, count






EncryptionParams = collections.namedtuple("EncryptionParams", "salt n r p")

@register_wallet_class
class WalletBitcoinj(object):

    class __metaclass__(type):
        @property
        def data_extract_id(cls): return b"bj"

    def passwords_per_seconds(self, seconds):
        passwords_per_second = self._passwords_per_second
        if hasattr(self, "_scrypt_n"):
            passwords_per_second /= self._scrypt_n / 16384  
            passwords_per_second /= self._scrypt_r / 8      
            passwords_per_second /= self._scrypt_p / 1      
        return max(int(round(passwords_per_second * seconds)), 1)

    @staticmethod
    def is_wallet_file(wallet_file):
        wallet_file.seek(0)
        if wallet_file.read(1) == b"\x0a":  
            network_identifier_len = ord(wallet_file.read(1))
            if 1 <= network_identifier_len < 128:
                wallet_file.seek(2 + network_identifier_len)
                c = wallet_file.read(1)
                if c and c in b"\x12\x1a":   
                    return True
        return False

    def __init__(self, loading = False):
        assert loading, 'use load_from_* to create a ' + self.__class__.__name__
        global pylibscrypt
        import pylibscrypt
        
        if not pylibscrypt._done:
            print(prog+": warning: can't find an scrypt library, performance will be severely degraded", file=sys.stderr)
            self._passwords_per_second = 0.03
        else:
            self._passwords_per_second = 14
        load_aes256_library()

    def __setstate__(self, state):
        
        global pylibscrypt
        import pylibscrypt
        load_aes256_library(warnings=False)
        self.__dict__ = state

    
    @classmethod
    def load_from_filename(cls, wallet_filename):
        with open(wallet_filename, "rb") as wallet_file:
            filedata = wallet_file.read(MAX_WALLET_FILE_SIZE)  
        return cls._load_from_filedata(filedata)

    @classmethod
    def _load_from_filedata(cls, filedata):
        from . import wallet_pb2
        pb_wallet = wallet_pb2.Wallet()
        pb_wallet.ParseFromString(filedata)
        if pb_wallet.encryption_type == wallet_pb2.Wallet.UNENCRYPTED:
            raise ValueError("bitcoinj wallet is not encrypted")
        if pb_wallet.encryption_type != wallet_pb2.Wallet.ENCRYPTED_SCRYPT_AES:
            raise NotImplementedError("Unsupported bitcoinj encryption type "+unicode(pb_wallet.encryption_type))
        if not pb_wallet.HasField("encryption_parameters"):
            raise ValueError("bitcoinj wallet is missing its scrypt encryption parameters")

        for key in pb_wallet.key:
            if  key.type in (wallet_pb2.Key.ENCRYPTED_SCRYPT_AES, wallet_pb2.Key.DETERMINISTIC_KEY) and key.HasField("encrypted_data"):
                encrypted_len = len(key.encrypted_data.encrypted_private_key)
                if encrypted_len == 48:
                    
                    self = cls(loading=True)
                    self._part_encrypted_key = key.encrypted_data.encrypted_private_key[-32:]
                    self._scrypt_salt = pb_wallet.encryption_parameters.salt
                    self._scrypt_n    = pb_wallet.encryption_parameters.n
                    self._scrypt_r    = pb_wallet.encryption_parameters.r
                    self._scrypt_p    = pb_wallet.encryption_parameters.p
                    return self
                print(prog+": warning: ignoring encrypted key of unexpected length ("+unicode(encrypted_len)+")", file=sys.stderr)

        raise ValueError("No encrypted keys found in bitcoinj wallet")

    
    @classmethod
    def load_from_data_extract(cls, privkey_data):
        self = cls(loading=True)
        
        self._part_encrypted_key = privkey_data[:32]
        
        self._scrypt_salt = privkey_data[32:40]
        (self._scrypt_n, self._scrypt_r, self._scrypt_p) = struct.unpack(b"< I H H", privkey_data[40:])
        return self

    def difficulty_info(self):
        return "scrypt N, r, p = {}, {}, {}".format(self._scrypt_n, self._scrypt_r, self._scrypt_p)

    
    
    def return_verified_password_or_false(self, passwords):
        
        l_scrypt             = pylibscrypt.scrypt
        l_aes256_cbc_decrypt = aes256_cbc_decrypt
        part_encrypted_key   = self._part_encrypted_key
        scrypt_salt          = self._scrypt_salt
        scrypt_n             = self._scrypt_n
        scrypt_r             = self._scrypt_r
        scrypt_p             = self._scrypt_p

        
        passwords = itertools.imap(lambda p: p.encode("utf_16_be", "ignore"), passwords)

        for count, password in enumerate(passwords, 1):
            derived_key = l_scrypt(password, scrypt_salt, scrypt_n, scrypt_r, scrypt_p, 32)
            part_key    = l_aes256_cbc_decrypt(derived_key, part_encrypted_key[:16], part_encrypted_key[16:])
            
            
            if part_key == b"\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10":
                password = password.decode("utf_16_be", "replace")
                return password.encode("ascii", "replace") if tstr == str else password, count

        return False, count




@register_wallet_class
class WalletMultiBitHD(WalletBitcoinj):

    class __metaclass__(WalletBitcoinj.__metaclass__):
        @property
        def data_extract_id(cls): return b"m5"
        "m2", which *only* supported MultiBit HD prior to v0.5.0 ("m5" supports
        

    @staticmethod
    def is_wallet_file(wallet_file): return None  

    
    @classmethod
    def load_from_filename(cls, wallet_filename):
        
        "detect" it
        if os.path.basename(wallet_filename) != "mbhd.wallet.aes":
            raise ValueError("MultiBit HD wallet files must be named mbhd.wallet.aes")

        with open(wallet_filename, "rb") as wallet_file:
            encrypted_data = wallet_file.read(16384)  
            if len(encrypted_data) < 32:
                raise ValueError("MultiBit HD wallet files must be at least 32 bytes long")

        
        
        entropy_bits = est_entropy_bits(encrypted_data)
        if entropy_bits < 7.8:
            raise ValueError("Doesn't look random enough to be an encrypted MultiBit HD wallet (only {:.1f} bits of entropy per byte)".format(entropy_bits))

        self = cls(loading=True)
        self._iv                   = encrypted_data[:16]    
        self._encrypted_block_iv   = encrypted_data[16:32]  
        self._encrypted_block_noiv = encrypted_data[:16]    
        return self

    
    @classmethod
    def load_from_data_extract(cls, file_data):
        self = cls(loading=True)
        assert len(file_data) == 32
        self._iv                   = file_data[:16]  
        self._encrypted_block_iv   = file_data[16:]  
        self._encrypted_block_noiv = file_data[:16]  
        return self

    def difficulty_info(self):
        return "scrypt N, r, p = 16384, 8, 1"

    
    
    def return_verified_password_or_false(self, passwords):
        
        l_scrypt             = pylibscrypt.scrypt
        l_aes256_cbc_decrypt = aes256_cbc_decrypt
        iv                   = self._iv
        encrypted_block_iv   = self._encrypted_block_iv
        encrypted_block_noiv = self._encrypted_block_noiv

        
        passwords = itertools.imap(lambda p: p.encode("utf_16_be", "ignore"), passwords)

        for count, password in enumerate(passwords, 1):
            derived_key = l_scrypt(password, b'\x35\x51\x03\x80\x75\xa3\xb0\xc5', olen=32)  
            block_iv    = l_aes256_cbc_decrypt(derived_key, iv, encrypted_block_iv)         
            block_noiv  = l_aes256_cbc_decrypt(                                             
                derived_key,
                b'\xa3\x44\x39\x1f\x53\x83\x11\xb3\x29\x54\x86\x16\xc4\x89\x72\x3e',        
                encrypted_block_noiv)
            
            
            
            for block in (block_iv, block_noiv):
                if block[2:6] == b"org." and block[0] == b"\x0a" and ord(block[1]) < 128:
                    password = password.decode("utf_16_be", "replace")
                    return password.encode("ascii", "replace") if tstr == str else password, count

        return False, count





class WalletAndroidSpendingPIN(WalletBitcoinj):

    
    @classmethod
    def load_from_filename(cls, wallet_filename, password = None, force_purepython = False):
        with open(wallet_filename, "rb") as wallet_file:
            
            if WalletBitcoinj.is_wallet_file(wallet_file):
                wallet_file.close()
                return WalletBitcoinj.load_from_filename(wallet_filename)

            wallet_file.seek(0)
            data = wallet_file.read(MAX_WALLET_FILE_SIZE)  

        data = data.replace(b"\r", b"").replace(b"\n", b"")
        data = base64.b64decode(data)
        if not data.startswith(b"Salted__"):
            raise ValueError("Not a Bitcoin Wallet for Android/BlackBerry encrypted backup (missing 'Salted__')")
        if len(data) < 32:
            raise EOFError  ("Expected at least 32 bytes of decoded data in the encrypted backup file")
        if len(data) % 16 != 0:
            raise ValueError("Not a valid Bitcoin Wallet for Android/BlackBerry encrypted backup (size not divisible by 16)")
        salt = data[8:16]
        data = data[16:]

        if not password:
            password = prompt_unicode_password(
                b"Please enter the password for the Bitcoin Wallet for Android/BlackBerry backup: ",
                "encrypted Bitcoin Wallet for Android/BlackBerry backups must be decrypted before searching for the PIN")
        
        password = password.encode("utf_16_le", "ignore")[::2]

        
        load_aes256_library(force_purepython)
        salted = password + salt
        key1   = hashlib.md5(salted).digest()
        key2   = hashlib.md5(key1 + salted).digest()
        iv     = hashlib.md5(key2 + salted).digest()
        data   = aes256_cbc_decrypt(key1 + key2, iv, data)
        from cStringIO import StringIO
        if not WalletBitcoinj.is_wallet_file(StringIO(data[:100])):
            error_exit("can't decrypt wallet (wrong password?)")
        
        padding_len = ord(data[-1])
        if not (1 <= padding_len <= 16 and data.endswith(chr(padding_len) * padding_len)):
            error_exit("can't decrypt wallet, invalid padding (wrong password?)")

        return cls._load_from_filedata(data[:-padding_len])  




@register_wallet_class
class WalletMsigna(object):

    class __metaclass__(type):
        @property
        def data_extract_id(cls): return b"ms"

    @staticmethod
    def is_wallet_file(wallet_file):
        wallet_file.seek(0)
        "maybe yes" or "definitely no" (Bither wallets are also SQLite 3)
        return None if wallet_file.read(16) == b"SQLite format 3\0" else False

    def __init__(self, loading = False):
        assert loading, 'use load_from_* to create a ' + self.__class__.__name__
        aes_library_name = load_aes256_library().__name__
        self._passwords_per_second = 50000 if aes_library_name == "Crypto" else 5000

    def __setstate__(self, state):
        
        load_aes256_library(warnings=False)
        self.__dict__ = state

    def passwords_per_seconds(self, seconds):
        return max(int(round(self._passwords_per_second * seconds)), 1)

    
    @classmethod
    def load_from_filename(cls, wallet_filename):
        
        import sqlite3
        wallet_conn = sqlite3.connect(wallet_filename)
        wallet_conn.row_factory = sqlite3.Row
        select = b"SELECT * FROM Keychain"
        try:
            if "args" in globals() and args.msigna_keychain:  
                wallet_cur = wallet_conn.execute(select + b" WHERE name LIKE '%' || ? || '%'", (args.msigna_keychain,))
            else:
                wallet_cur = wallet_conn.execute(select)
        except sqlite3.OperationalError as e:
            if str(e).startswith(b"no such table"):
                raise ValueError("Not an mSIGNA wallet: " + unicode(e))  
            else:
                raise  
        keychain = wallet_cur.fetchone()
        if not keychain:
            error_exit("no such keychain found in the mSIGNA vault")
        keychain_extra = wallet_cur.fetchone()
        if keychain_extra:
            print("Multiple matching keychains found in the mSIGNA vault:", file=sys.stderr)
            print("  ", keychain[b"name"])
            print("  ", keychain_extra[b"name"])
            for keychain_extra in wallet_cur:
                print("  ", keychain_extra[b"name"])
            error_exit("use --msigna-keychain NAME to specify a specific keychain")
        wallet_conn.close()

        privkey_ciphertext = str(keychain[b"privkey_ciphertext"])
        if len(privkey_ciphertext) == 32:
            error_exit("mSIGNA keychain '"+keychain[b"name"]+"' is not encrypted")
        if len(privkey_ciphertext) != 48:
            error_exit("mSIGNA keychain '"+keychain[b"name"]+"' has an unexpected privkey length")

        
        self = cls(loading=True)
        self._part_encrypted_privkey = privkey_ciphertext[-32:]
        self._salt                   = struct.pack(b"< q", keychain[b"privkey_salt"])
        return self

    
    @classmethod
    def load_from_data_extract(cls, privkey_data):
        self = cls(loading=True)
        self._part_encrypted_privkey = privkey_data[:32]
        self._salt                   = privkey_data[32:]
        return self

    def difficulty_info(self):
        return "2 SHA-256 iterations"

    
    
    def return_verified_password_or_false(self, passwords):
        
        l_sha1                 = hashlib.sha1
        l_sha256               = hashlib.sha256
        part_encrypted_privkey = self._part_encrypted_privkey
        salt                   = self._salt

        
        if tstr == unicode:
            passwords = itertools.imap(lambda p: p.encode("utf_8", "ignore"), passwords)

        for count, password in enumerate(passwords, 1):
            password_hashed = l_sha256(l_sha256(password).digest()).digest()  
            
            
            
            
            derived_part1 = password_hashed + salt
            for i in xrange(5):  
                derived_part1 = l_sha1(derived_part1).digest()
            derived_part2 = derived_part1 + password_hashed + salt
            for i in xrange(5):
                derived_part2 = l_sha1(derived_part2).digest()
            
            part_privkey = aes256_cbc_decrypt(derived_part1 + derived_part2[:12], part_encrypted_privkey[:16], part_encrypted_privkey[16:])
            
            
            if part_privkey == b"\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10":
                return password if tstr == str else password.decode("utf_8", "replace"), count

        return False, count





class WalletElectrum(object):

    def __init__(self, loading = False):
        assert loading, 'use load_from_* to create a ' + self.__class__.__name__
        aes_library_name = load_aes256_library().__name__
        self._passwords_per_second = 100000 if aes_library_name == "Crypto" else 5000

    def __setstate__(self, state):
        
        load_aes256_library(warnings=False)
        self.__dict__ = state

    def passwords_per_seconds(self, seconds):
        return max(int(round(self._passwords_per_second * seconds)), 1)

    
    @classmethod
    def load_from_data_extract(cls, data):
        assert len(data) == 32
        self = cls(loading=True)
        self._iv                  = data[:16]  
        self._part_encrypted_data = data[16:]  
        return self

    def difficulty_info(self):
        return "2 SHA-256 iterations"

@register_wallet_class
class WalletElectrum1(WalletElectrum):

    class __metaclass__(type):
        @property
        def data_extract_id(cls): return b"el"

    @staticmethod
    def is_wallet_file(wallet_file):
        wallet_file.seek(0)
        "maybe yes" or "definitely no"
        return None if wallet_file.read(2) == b"{'" else False

    
    @classmethod
    def load_from_filename(cls, wallet_filename):
        from ast import literal_eval
        with open(wallet_filename) as wallet_file:
            try:
                wallet = literal_eval(wallet_file.read(MAX_WALLET_FILE_SIZE))  
            except SyntaxError as e:  
                raise ValueError(e)   
        return cls._load_from_dict(wallet)

    @classmethod
    def _load_from_dict(cls, wallet):
        seed_version = wallet.get("seed_version")
        if seed_version is None:             raise ValueError("Unrecognized wallet format (Electrum1 seed_version not found)")
        if seed_version != 4:                raise NotImplementedError("Unsupported Electrum1 seed version " + unicode(seed_version))
        if not wallet.get("use_encryption"): raise RuntimeError("Electrum1 wallet is not encrypted")
        seed_data = base64.b64decode(wallet["seed"])
        if len(seed_data) != 64:             raise RuntimeError("Electrum1 encrypted seed plus iv is not 64 bytes long")
        self = cls(loading=True)
        self._iv                  = seed_data[:16]    
        self._part_encrypted_data = seed_data[16:32]  
        return self

    
    
    assert b"0" < b"9" < b"a" < b"f"  
    def return_verified_password_or_false(self, passwords):
        
        l_sha256             = hashlib.sha256
        l_aes256_cbc_decrypt = aes256_cbc_decrypt
        part_encrypted_seed  = self._part_encrypted_data
        iv                   = self._iv

        
        if tstr == unicode:
            passwords = itertools.imap(lambda p: p.encode("utf_8", "ignore"), passwords)

        for count, password in enumerate(passwords, 1):
            key  = l_sha256( l_sha256( password ).digest() ).digest()
            seed = l_aes256_cbc_decrypt(key, iv, part_encrypted_seed)
            
            for c in seed:
                if c > b"f" or c < b"0" or b"9" < c < b"a": break  
            else:  
                return password if tstr == str else password.decode("utf_8", "replace"), count

        return False, count

@register_wallet_class
class WalletElectrum2(WalletElectrum):

    class __metaclass__(type):
        @property
        def data_extract_id(cls): return b"e2"

    @staticmethod
    def is_wallet_file(wallet_file):
        wallet_file.seek(0)
        "maybe yes" or "definitely no"
        return None if wallet_file.read(1) == b"{" else False

    
    @classmethod
    def load_from_filename(cls, wallet_filename):
        import json

        with open(wallet_filename) as wallet_file:
            wallet = json.load(wallet_file)
        wallet_type = wallet.get("wallet_type")
        if not wallet_type:
            raise ValueError("Unrecognized wallet format (Electrum2 wallet_type not found)")
        if wallet_type == "old":  
            return WalletElectrum1._load_from_dict(wallet)
        if not wallet.get("use_encryption"):
            raise ValueError("Electrum2 wallet is not encrypted")
        seed_version = wallet.get("seed_version", "(not found)")
        if wallet.get("seed_version") not in (11, 12, 13) and wallet_type != "imported":  
            raise NotImplementedError("Unsupported Electrum2 seed version " + unicode(seed_version))

        xprv = None
        while True:  "loops" exactly once; only here so we've something to break out of

            
            keystore = wallet.get("keystore")
            if keystore:
                keystore_type = keystore.get("type", "(not found)")

                
                if keystore_type == "bip32":
                    xprv = keystore.get("xprv")
                    if xprv: break

                
                elif keystore_type == "old":
                    seed_data = keystore.get("seed")
                    if seed_data:
                        
                        seed_data = base64.b64decode(seed_data)
                        if len(seed_data) != 64:
                            raise RuntimeError("Electrum1 encrypted seed plus iv is not 64 bytes long")
                        self = WalletElectrum1(loading=True)
                        self._iv                  = seed_data[:16]    
                        self._part_encrypted_data = seed_data[16:32]  
                        return self

                
                elif keystore_type == "imported":
                    for privkey in keystore["keypairs"].values():
                        if privkey:
                            
                            privkey = base64.b64decode(privkey)
                            if len(privkey) != 80:
                                raise RuntimeError("Electrum2 private key plus iv is not 80 bytes long")
                            self = WalletElectrumLooseKey(loading=True)
                            self._iv                  = privkey[-32:-16]  
                            self._part_encrypted_data = privkey[-16:]     
                            return self

                else:
                    print(prog+": warning: found unsupported keystore type " + keystore_type, file=sys.stderr)

            
            for i in itertools.count(1):
                x = wallet.get("x{}/".format(i))
                if not x: break
                x_type = x.get("type", "(not found)")
                if x_type == "bip32":
                    xprv = x.get("xprv")
                    if xprv: break
                else:
                    print(prog + ": warning: found unsupported key type " + x_type, file=sys.stderr)
            if xprv: break

            
            if wallet_type == "imported":
                for imported in wallet["accounts"]["/x"]["imported"].values():
                    privkey = imported[1] if len(imported) >= 2 else None
                    if privkey:
                        
                        privkey = base64.b64decode(privkey)
                        if len(privkey) != 80:
                            raise RuntimeError("Electrum2 private key plus iv is not 80 bytes long")
                        self = WalletElectrumLooseKey(loading=True)
                        self._iv                  = privkey[-32:-16]  
                        self._part_encrypted_data = privkey[-16:]     
                        return self

            
            else:
                mpks = wallet.get("master_private_keys")
                if mpks:
                    xprv = mpks.values()[0]
                    break

            raise RuntimeError("No master private keys or seeds found in Electrum2 wallet")

        xprv_data = base64.b64decode(xprv)
        if len(xprv_data) != 128:
            raise RuntimeError("Unexpected Electrum2 encrypted master private key length")
        self = cls(loading=True)
        self._iv                  = xprv_data[:16]    
        self._part_encrypted_data = xprv_data[16:32]  
        return self                                   

    
    
    assert b"1" < b"9" < b"A" < b"Z" < b"a" < b"z"  
    def return_verified_password_or_false(self, passwords):
        
        l_sha256             = hashlib.sha256
        l_aes256_cbc_decrypt = aes256_cbc_decrypt
        part_encrypted_xprv  = self._part_encrypted_data
        iv                   = self._iv

        
        if tstr == unicode:
            passwords = itertools.imap(lambda p: p.encode("utf_8", "ignore"), passwords)

        for count, password in enumerate(passwords, 1):
            key  = l_sha256( l_sha256( password ).digest() ).digest()
            xprv = l_aes256_cbc_decrypt(key, iv, part_encrypted_xprv)

            if xprv.startswith(b"xprv"):  
                for c in xprv[4:]:
                    
                    if c > b"z" or c < b"1" or b"9" < c < b"A" or b"Z" < c < b"a" or c in b"IOl": break  
                else:  
                    return password if tstr == str else password.decode("utf_8", "replace"), count

        return False, count

@register_wallet_class
class WalletElectrumLooseKey(WalletElectrum):

    class __metaclass__(type):
        @property
        def data_extract_id(cls):    return b"ek"

    @staticmethod
    def is_wallet_file(wallet_file): return False  

    
    
    assert b"1" < b"9" < b"A" < b"Z" < b"a" < b"z"  
    def return_verified_password_or_false(self, passwords):
        
        l_sha256              = hashlib.sha256
        l_aes256_cbc_decrypt  = aes256_cbc_decrypt
        encrypted_privkey_end = self._part_encrypted_data
        iv                    = self._iv

        
        if tstr == unicode:
            passwords = itertools.imap(lambda p: p.encode("utf_8", "ignore"), passwords)

        for count, password in enumerate(passwords, 1):
            key         = l_sha256( l_sha256( password ).digest() ).digest()
            privkey_end = l_aes256_cbc_decrypt(key, iv, encrypted_privkey_end)
            padding_len = ord(privkey_end[-1])
            "WIF" private key
            
            if (padding_len == 12 or padding_len == 13) and privkey_end.endswith(chr(padding_len) * padding_len):
                for c in privkey_end[:-padding_len]:
                    
                    if c > b"z" or c < b"1" or b"9" < c < b"A" or b"Z" < c < b"a" or c in b"IOl": break  
                else:  
                    return password if tstr == str else password.decode("utf_8", "replace"), count

        return False, count


@register_wallet_class
class WalletElectrum28(object):

    def passwords_per_seconds(self, seconds):
        return max(int(round(self._passwords_per_second * seconds)), 1)

    @staticmethod
    def is_wallet_file(wallet_file):
        wallet_file.seek(0)
        try:   data = base64.b64decode(wallet_file.read(8))
        except TypeError: return False
        return data[:4] == b"BIE1"  

    def __init__(self, loading = False):
        assert loading, 'use load_from_* to create a ' + self.__class__.__name__
        global hmac, coincurve
        import hmac, coincurve
        pbkdf2_library_name    = load_pbkdf2_library().__name__
        self._aes_library_name = load_aes256_library().__name__
        self._passwords_per_second = 800 if pbkdf2_library_name == "hashlib" else 140

    def __getstate__(self):
        
        state = self.__dict__.copy()
        state["_ephemeral_pubkey"] = self._ephemeral_pubkey.format(compressed=False)
        return state

    def __setstate__(self, state):
        
        global hmac, coincurve
        import hmac, coincurve
        load_pbkdf2_library(warnings=False)
        load_aes256_library(warnings=False)
        self.__dict__ = state
        self._ephemeral_pubkey = coincurve.PublicKey(self._ephemeral_pubkey)

    
    @classmethod
    def load_from_filename(cls, wallet_filename):
        with open(wallet_filename) as wallet_file:
            data = wallet_file.read(MAX_WALLET_FILE_SIZE)  
        if len(data) >= MAX_WALLET_FILE_SIZE:
            raise ValueError("Encrypted Electrum wallet file is too big")
        MIN_LEN = 37 + 32 + 32  
        if len(data) < MIN_LEN * 4 / 3:
            raise EOFError("Expected at least {} bytes of text in the Electrum wallet file".format(int(math.ceil(MIN_LEN * 4 / 3))))
        data = base64.b64decode(data)
        if len(data) < MIN_LEN:
            raise EOFError("Expected at least {} bytes of decoded data in the Electrum wallet file".format(MIN_LEN))
        assert data[:4] == b"BIE1", "wallet file has Electrum 2.8+ magic"

        self = cls(loading=True)
        self._ephemeral_pubkey = coincurve.PublicKey(data[4:37])
        self._ciphertext_beg   = data[37:37+16]  
        self._ciphertext_end   = data[-64:-32]   
        self._mac              = data[-32:]
        self._all_but_mac      = data[:-32]
        return self

    def difficulty_info(self):
        return "1024 PBKDF2-SHA512 iterations + ECC"

    
    
    def return_verified_password_or_false(self, passwords):
        cutils = coincurve.utils

        
        if tstr == unicode:
            passwords = itertools.imap(lambda p: p.encode("utf_8", "ignore"), passwords)

        for count, password in enumerate(passwords, 1):

            
            static_privkey = pbkdf2_hmac(b"sha512", password, b"", 1024, 64)
            
            static_privkey = cutils.int_to_bytes( cutils.bytes_to_int(static_privkey) % cutils.GROUP_ORDER_INT )
            shared_pubkey  = self._ephemeral_pubkey.multiply(static_privkey).format()
            keys           = hashlib.sha512(shared_pubkey).digest()

            
            if self._aes_library_name != 'aespython':
                
                plaintext_block = aes256_cbc_decrypt(keys[16:32], keys[:16], self._ciphertext_beg)  
                if not (plaintext_block.startswith(b"\x78\x9c") and ord(plaintext_block[2]) & 0x7 == 0x5):
                    continue

                
                plaintext_block = aes256_cbc_decrypt(keys[16:32], self._ciphertext_end[:16], self._ciphertext_end[16:])  
                padding_len = ord(plaintext_block[-1])
                if not (1 <= padding_len <= 16 and plaintext_block.endswith(chr(padding_len) * padding_len)):
                    continue

            
            computed_mac = hmac.new(keys[32:], self._all_but_mac, hashlib.sha256).digest()
            if computed_mac == self._mac:
                return password if tstr == str else password.decode("utf_8", "replace"), count

        return False, count




@register_wallet_class
class WalletBlockchain(object):

    class __metaclass__(type):
        @property
        def data_extract_id(cls):    return b"bk"

    @staticmethod
    def is_wallet_file(wallet_file): return None  

    def __init__(self, iter_count, loading = False):
        assert loading, 'use load_from_* to create a ' + self.__class__.__name__
        pbkdf2_library_name = load_pbkdf2_library().__name__
        aes_library_name    = load_aes256_library().__name__
        self._iter_count           = iter_count
        self._passwords_per_second = 400000 if pbkdf2_library_name == "hashlib" else 100000
        if iter_count == 0:  
            iter_count = 10
        self._passwords_per_second /= iter_count
        if aes_library_name != "Crypto" and self._passwords_per_second > 2000:
            self._passwords_per_second = 2000

    def __setstate__(self, state):
        
        load_pbkdf2_library(warnings=False)
        load_aes256_library(warnings=False)
        self.__dict__ = state

    def passwords_per_seconds(self, seconds):
        return max(int(round(self._passwords_per_second * seconds)), 1)

    
    @classmethod
    def load_from_filename(cls, wallet_filename):
        with open(wallet_filename) as wallet_file:
            data, iter_count = cls._parse_encrypted_blockchain_wallet(wallet_file.read(MAX_WALLET_FILE_SIZE))  
        self = cls(iter_count, loading=True)
        self._salt_and_iv     = data[:16]    
        self._encrypted_block = data[16:32]  
        return self

    
    
    @staticmethod
    def _parse_encrypted_blockchain_wallet(data):
        iter_count = 0

        while True:  "loops" exactly once; only here so we've something to break out of
            
            try:
                data = json.loads(data)
            except ValueError: break

            
            if "version" not in data:
                try:
                    data = data["payload"]  
                except KeyError:
                    raise ValueError("Can't find either version nor payload attributes in Blockchain file")
                try:
                    data = json.loads(data)  
                except ValueError: break

            
            if data["version"] > 3:
                raise NotImplementedError("Unsupported Blockchain wallet version " + unicode(data["version"]))
            iter_count = data["pbkdf2_iterations"]
            if not isinstance(iter_count, int) or iter_count < 1:
                raise ValueError("Invalid Blockchain pbkdf2_iterations " + unicode(iter_count))
            data = data["payload"]

            break

        "payload" field above, or
        
        try:
            data = base64.b64decode(data)
        except TypeError as e:
            raise ValueError("Can't base64-decode Blockchain wallet: "+unicode(e))
        if len(data) < 32:
            raise ValueError("Encrypted Blockchain data is too short")
        if len(data) % 16 != 0:
            raise ValueError("Encrypted Blockchain data length is not divisible by the encryption blocksize (16)")

        
        
        
        if not iter_count:  
            
            
            
            entropy_bits = est_entropy_bits(data)
            if entropy_bits < 7.2:
                raise ValueError("Doesn't look random enough to be an encrypted Blockchain wallet (only {:.1f} bits of entropy per byte)".format(entropy_bits))

        return data, iter_count  

    
    @classmethod
    def load_from_data_extract(cls, file_data):
        
        encrypted_block, salt_and_iv, iter_count = struct.unpack(b"< 16s 16s I", file_data)
        self = cls(iter_count, loading=True)
        self._encrypted_block = encrypted_block
        self._salt_and_iv     = salt_and_iv
        return self

    def difficulty_info(self):
        return "{:,} PBKDF2-SHA1 iterations".format(self._iter_count or 10)

    
    
    def return_verified_password_or_false(self, passwords):
        
        l_pbkdf2_hmac        = pbkdf2_hmac
        l_aes256_cbc_decrypt = aes256_cbc_decrypt
        l_aes256_ofb_decrypt = aes256_ofb_decrypt
        encrypted_block      = self._encrypted_block
        salt_and_iv          = self._salt_and_iv
        iter_count           = self._iter_count

        
        if tstr == unicode:
            passwords = map(lambda p: p.encode("utf_8", "ignore"), passwords)

        v0 = not iter_count     
        if v0: iter_count = 10  
        for count, password in enumerate(passwords, 1):
            key = l_pbkdf2_hmac(b"sha1", password, salt_and_iv, iter_count, 32)          
            unencrypted_block = l_aes256_cbc_decrypt(key, salt_and_iv, encrypted_block)  
            
            
            if unencrypted_block[0] == b"{" and b'"guid"' in unencrypted_block:
                return password if tstr == str else password.decode("utf_8", "replace"), count

        if v0:
            
            for count, password in enumerate(passwords, 1):
                key = l_pbkdf2_hmac(b"sha1", password, salt_and_iv, 1, 32)                   
                unencrypted_block = l_aes256_cbc_decrypt(key, salt_and_iv, encrypted_block)  
                if unencrypted_block[0] == b"{" and b'"guid"' in unencrypted_block:
                    return password if tstr == str else password.decode("utf_8", "replace"), count
                unencrypted_block = l_aes256_ofb_decrypt(key, salt_and_iv, encrypted_block)  
                if unencrypted_block[0] == b"{" and b'"guid"' in unencrypted_block:
                    return password if tstr == str else password.decode("utf_8", "replace"), count

        return False, count

@register_wallet_class
class WalletBlockchainSecondpass(WalletBlockchain):

    class __metaclass__(WalletBlockchain.__metaclass__):
        @property
        def data_extract_id(cls):    return b"bs"

    @staticmethod
    def is_wallet_file(wallet_file): return False  

    "Second Password" hash,
    
    @classmethod
    def load_from_filename(cls, wallet_filename, password = None, force_purepython = False):
        from uuid import UUID

        with open(wallet_filename) as wallet_file:
            data = wallet_file.read(MAX_WALLET_FILE_SIZE)  

        try:
            
            data, iter_count = cls._parse_encrypted_blockchain_wallet(data)
        except ValueError as e:
            
            if e.args[0] == "Can't find either version nor payload attributes in Blockchain file":
                pass
            else:
                raise
        except StandardError as e:
            error_exit(unicode(e))
        else:
            
            if not password:
                password = prompt_unicode_password(
                    b"Please enter the Blockchain wallet's main password: ",
                    "encrypted Blockchain files must be decrypted before searching for the second password")
            password = password.encode("utf_8")
            data, salt_and_iv = data[16:], data[:16]
            load_pbkdf2_library(force_purepython)
            load_aes256_library(force_purepython)
            
            
            
            
            
            def decrypt_current(iter_count):
                key = pbkdf2_hmac(b"sha1", password, salt_and_iv, iter_count, 32)
                decrypted = aes256_cbc_decrypt(key, salt_and_iv, data)    
                padding   = ord(decrypted[-1:])                           
                return decrypted[:-padding] if 1 <= padding <= 16 and re.match(b'{\s*"guid"', decrypted) else None
            
            
            def decrypt_old():
                key = pbkdf2_hmac(b"sha1", password, salt_and_iv, 1, 32)  
                decrypted  = aes256_ofb_decrypt(key, salt_and_iv, data)   
                
                last_block = tuple(itertools.dropwhile(lambda x: x==b"\0", decrypted[:15:-1]))
                padding    = 17 - len(last_block)                         
                return decrypted[:-padding] if 1 <= padding <= 16 and decrypted[-padding] == b"\x80" and re.match(b'{\s*"guid"', decrypted) else None
            
            if iter_count:  
                data = decrypt_current(iter_count)
            else:           
                data = decrypt_current(10) or decrypt_current(1) or decrypt_old()
            if not data:
                error_exit("can't decrypt wallet (wrong main password?)")

        
        data = json.loads(data)
        if not data.get("double_encryption"):
            error_exit("double encryption with a second password is not enabled for this wallet")

        
        try:
            iter_count = data["options"]["pbkdf2_iterations"]
            if not isinstance(iter_count, int) or iter_count < 1:
                raise ValueError("Invalid Blockchain second password pbkdf2_iterations " + unicode(iter_count))
        except KeyError:
            iter_count = 0
        self = cls(iter_count, loading=True)
        
        self._password_hash = base64.b16decode(data["dpasswordhash"], casefold=True)
        if len(self._password_hash) != 32:
            raise ValueError("Blockchain second password hash is not 32 bytes long")
        
        self._salt = data["sharedKey"].encode("ascii")
        if str(UUID(self._salt)) != self._salt:
            raise ValueError("Unrecognized Blockchain salt format")

        return self

    
    @classmethod
    def load_from_data_extract(cls, file_data):
        from uuid import UUID
        
        password_hash, uuid_salt, iter_count = struct.unpack(b"< 32s 16s I", file_data)
        self = cls(iter_count, loading=True)
        self._salt          = str(UUID(bytes=uuid_salt))
        self._password_hash = password_hash
        return self

    def difficulty_info(self):
        return ("{:,}".format(self._iter_count) if self._iter_count else "1-10") + " SHA-256 iterations"

    
    
    def return_verified_password_or_false(self, passwords):
        
        l_sha256 = hashlib.sha256
        password_hash = self._password_hash
        salt          = self._salt
        iter_count    = self._iter_count

        
        if tstr == unicode:
            passwords = itertools.imap(lambda p: p.encode("utf_8", "ignore"), passwords)

        
        if iter_count:
            for count, password in enumerate(passwords, 1):
                running_hash = salt + password
                for i in xrange(iter_count):
                    running_hash = l_sha256(running_hash).digest()
                if running_hash == password_hash:
                    return password if tstr == str else password.decode("utf_8", "replace"), count

        
        else:
            for count, password in enumerate(passwords, 1):
                running_hash = l_sha256(salt + password).digest()
                
                if running_hash == password_hash:
                    return password if tstr == str else password.decode("utf_8", "replace"), count
                
                for i in xrange(9):
                    running_hash = l_sha256(running_hash).digest()
                if running_hash == password_hash:
                    return password if tstr == str else password.decode("utf_8", "replace"), count
                
                if l_sha256(password).digest() == password_hash:
                    return password if tstr == str else password.decode("utf_8", "replace"), count

        return False, count




@register_wallet_class
class WalletBither(object):

    class __metaclass__(type):
        @property
        def data_extract_id(cls): return b"bt"

    def passwords_per_seconds(self, seconds):
        return max(int(round(self._passwords_per_second * seconds)), 1)

    @staticmethod
    def is_wallet_file(wallet_file):
        wallet_file.seek(0)
        "maybe yes" or "definitely no" (mSIGNA wallets are also SQLite 3)
        return None if wallet_file.read(16) == b"SQLite format 3\0" else False

    def __init__(self, loading = False):
        assert loading, 'use load_from_* to create a ' + self.__class__.__name__
        

    def __setstate__(self, state):
        
        global pylibscrypt, coincurve
        import pylibscrypt, coincurve
        load_aes256_library(warnings=False)
        self.__dict__ = state

    
    @classmethod
    def load_from_filename(cls, wallet_filename):
        import sqlite3
        wallet_conn = sqlite3.connect(wallet_filename)

        is_bitcoinj_compatible  = None
        
        try:
            wallet_cur = wallet_conn.execute(b"SELECT encrypt_private_key FROM addresses LIMIT 1")
            key_data   = wallet_cur.fetchone()
            if key_data:
                key_data = key_data[0]
                is_bitcoinj_compatible = True  
            else:
                e1 = "no encrypted keys present in addresses table"
        except sqlite3.OperationalError as e1:
            if str(e1).startswith(b"no such table"):
                key_data = None
            else: raise  

        if not key_data:
            
            try:
                wallet_cur = wallet_conn.execute(b"SELECT password_seed FROM password_seed LIMIT 1")
                key_data   = wallet_cur.fetchone()
            except sqlite3.OperationalError as e2:
                raise ValueError("Not a Bither wallet: {}, {}".format(e1, e2))  
            if not key_data:
                error_exit("can't find an encrypted key or password seed in the Bither wallet")
            key_data = key_data[0]

        
        bitcoinj_wallet = WalletBitcoinj(loading=True)

        
        key_data = key_data.split(b"/")
        if len(key_data) == 1:
            key_data = key_data.split(b":")  ":" as the delimiter
        pubkey_hash = key_data.pop(0) if len(key_data) == 4 else None
        if len(key_data) != 3:
            error_exit("unrecognized Bither encrypted key format (expected 3-4 slash-delimited elements, found {})"
                       .format(len(key_data)))
        (encrypted_key, iv, salt) = key_data
        encrypted_key = base64.b16decode(encrypted_key, casefold=True)

        
        salt = base64.b16decode(salt, casefold=True)
        if len(salt) == 9:
            flags = ord(salt[0])
            salt  = salt[1:]
        else:
            flags = 1  
            if len(salt) != 8:
                error_exit("unexpected salt length ({}) in Bither wallet".format(len(salt)))

        
        if is_bitcoinj_compatible:
            if len(encrypted_key) != 48:
                error_exit("unexpected encrypted key length in Bither wallet (expected 48, found {})"
                           .format(len(encrypted_key)))
            
            bitcoinj_wallet._part_encrypted_key = encrypted_key[-32:]
            bitcoinj_wallet._scrypt_salt = salt
            bitcoinj_wallet._scrypt_n    = 16384  
            bitcoinj_wallet._scrypt_r    = 8
            bitcoinj_wallet._scrypt_p    = 1
            return bitcoinj_wallet

        
        else:
            if not pubkey_hash:
                error_exit("pubkey hash160 not present in Bither password_seed")
            global coincurve
            import coincurve
            self = cls(loading=True)
            self._passwords_per_second = bitcoinj_wallet._passwords_per_second  
            self._iv_encrypted_key     = base64.b16decode(iv, casefold=True) + encrypted_key
            self._salt                 = salt  
            self._pubkey_hash160       = base64.b16decode(pubkey_hash, casefold=True)[1:]  
            self._is_compressed        = bool(flags & 1)  
            return self

    
    @classmethod
    def load_from_data_extract(cls, privkey_data):
        assert len(privkey_data) == 40, "extract-bither-privkey.py only extracts keys from bitcoinj compatible wallets"
        bitcoinj_wallet = WalletBitcoinj(loading=True)
        
        bitcoinj_wallet._part_encrypted_key = privkey_data[:32]
        
        bitcoinj_wallet._scrypt_salt = privkey_data[32:]
        bitcoinj_wallet._scrypt_n    = 16384
        bitcoinj_wallet._scrypt_r    = 8
        bitcoinj_wallet._scrypt_p    = 1
        return bitcoinj_wallet

    def difficulty_info(self):
        return "scrypt N, r, p = 16384, 8, 1 + ECC"

    
    
    def return_verified_password_or_false(self, passwords):
        
        l_scrypt             = pylibscrypt.scrypt
        l_aes256_cbc_decrypt = aes256_cbc_decrypt
        l_sha256             = hashlib.sha256
        hashlib_new          = hashlib.new
        iv_encrypted_key     = self._iv_encrypted_key  
        salt                 = self._salt
        pubkey_from_secret   = coincurve.PublicKey.from_valid_secret
        cutils               = coincurve.utils

        
        passwords = itertools.imap(lambda p: p.encode("utf_16_be", "ignore"), passwords)

        for count, password in enumerate(passwords, 1):
            derived_aeskey = l_scrypt(password, salt, 16384, 8, 1, 32)  

            
            privkey_end = l_aes256_cbc_decrypt(derived_aeskey, iv_encrypted_key[-32:-16], iv_encrypted_key[-16:])
            padding_len = ord(privkey_end[-1])
            if not (1 <= padding_len <= 16 and privkey_end.endswith(chr(padding_len) * padding_len)):
                continue
            privkey_end = privkey_end[:-padding_len]  

            
            privkey = l_aes256_cbc_decrypt(derived_aeskey, iv_encrypted_key[:16], iv_encrypted_key[16:-16]) + privkey_end
            
            privkey = cutils.int_to_bytes_padded( cutils.bytes_to_int(privkey) % cutils.GROUP_ORDER_INT )
            pubkey  = pubkey_from_secret(privkey).format(self._is_compressed)
            
            if hashlib_new("ripemd160", l_sha256(pubkey).digest()).digest() == self._pubkey_hash160:
                password = password.decode("utf_16_be", "replace")
                return password.encode("ascii", "replace") if tstr == str else password, count

        return False, count




"registered" wallet since there are no wallet files nor extracts
class WalletBIP39(object):

    def __init__(self, mpk = None, addresses = None, address_limit = None, addressdb_filename = None,
                 mnemonic = None, lang = None, path = None, wallet_type = "bitcoin", is_performance = False):
        from . import btcrseed
        if wallet_type == "bitcoin":
            btcrseed_cls = btcrseed.WalletBIP39
        elif wallet_type == "ethereum":
            if addressdb_filename:
                error_exit("can't use an address database with Ethereum wallets")
            btcrseed_cls = btcrseed.WalletEthereum
        else:
            error_exit("--wallet-type must be one of: bitcoin, ethereum")

        global normalize, hmac
        from unicodedata import normalize
        import hmac
        load_pbkdf2_library()

        
        
        if addressdb_filename:
            from .addressset import AddressSet
            print("Loading address database ...")
            hash160s = AddressSet.fromfile(open(addressdb_filename, "rb"))
        else:
            hash160s = None
        self.btcrseed_wallet = btcrseed_cls.create_from_params(
            mpk, addresses, address_limit, hash160s, path, is_performance)
        if is_performance and not mnemonic:
            mnemonic = "certain come keen collect slab gauge photo inside mechanic deny leader drop"
        self.btcrseed_wallet.config_mnemonic(mnemonic, lang)

        
        if not self.btcrseed_wallet.verify_mnemonic_syntax(btcrseed.mnemonic_ids_guess):
            error_exit("one or more words are missing from the mnemonic")
        if not self.btcrseed_wallet._verify_checksum(btcrseed.mnemonic_ids_guess):
            error_exit("invalid mnemonic (the checksum is wrong)")
        
        self.btcrseed_wallet._checksum_ratio = 1

        self._mnemonic = b" ".join(btcrseed.mnemonic_ids_guess)

    def __setstate__(self, state):
        
        global normalize, hmac
        from unicodedata import normalize
        import hmac
        load_pbkdf2_library(warnings=False)
        self.__dict__ = state

    def passwords_per_seconds(self, seconds):
        return self.btcrseed_wallet.passwords_per_seconds(seconds)

    def difficulty_info(self):
        return "2048 PBKDF2-SHA512 iterations + ECC"

    
    
    def return_verified_password_or_false(self, passwords):
        
        if tstr == unicode:
            passwords = itertools.imap(lambda p: normalize("NFKD", p).encode("utf_8", "ignore"), passwords)

        for count, password in enumerate(passwords, 1):
            seed_bytes = pbkdf2_hmac(b"sha512", self._mnemonic, b"mnemonic" + password, 2048)
            seed_bytes = hmac.new(b"Bitcoin seed", seed_bytes, hashlib.sha512).digest()
            if self.btcrseed_wallet._verify_seed(seed_bytes):
                return password if tstr == str else password.decode("utf_8", "replace"), count

        return False, count






class WalletNull(object):

    def passwords_per_seconds(self, seconds):
        return max(int(round(500000 * seconds)), 1)

    def return_verified_password_or_false(self, passwords):
        return False, len(passwords)






missing_pycrypto_warned = False
def load_aes256_library(force_purepython = False, warnings = True):
    global aes256_cbc_decrypt, aes256_ofb_decrypt, missing_pycrypto_warned
    if not force_purepython:
        try:
            import Crypto.Cipher.AES
            new_aes = Crypto.Cipher.AES.new
            aes256_cbc_decrypt = lambda key, iv, ciphertext: \
                new_aes(key, Crypto.Cipher.AES.MODE_CBC, iv).decrypt(ciphertext)
            aes256_ofb_decrypt = lambda key, iv, ciphertext: \
                new_aes(key, Crypto.Cipher.AES.MODE_OFB, iv).decrypt(ciphertext)
            return Crypto  
        except ImportError:
            if warnings and not missing_pycrypto_warned:
                print(prog+": warning: can't find PyCrypto, using aespython instead", file=sys.stderr)
                missing_pycrypto_warned = True

    
    
    "slowaes" package (although it's still 30x slower than the PyCrypto)
    
    import aespython
    expandKey = aespython.key_expander.expandKey
    AESCipher = aespython.aes_cipher.AESCipher
    def aes256_decrypt_factory(BlockMode):
        def aes256_decrypt(key, iv, ciphertext):
            block_cipher  = AESCipher( expandKey(bytearray(key)) )
            stream_cipher = BlockMode(block_cipher, 16)
            stream_cipher.set_iv(bytearray(iv))
            plaintext = bytearray()
            for i in xrange(0, len(ciphertext), 16):
                plaintext.extend( stream_cipher.decrypt_block(bytearray(ciphertext[i:i+16])) )  
            return str(plaintext)
        return aes256_decrypt
    aes256_cbc_decrypt = aes256_decrypt_factory(aespython.CBCMode)
    aes256_ofb_decrypt = aes256_decrypt_factory(aespython.OFBMode)
    return aespython  





"sha1"), password, salt, iter_count, key_len (the length of the returned key)
missing_pbkdf2_warned = False
def load_pbkdf2_library(force_purepython = False, warnings = True):
    global pbkdf2_hmac, missing_pbkdf2_warned
    if not force_purepython:
        try:
            pbkdf2_hmac = hashlib.pbkdf2_hmac
            return hashlib  
        except AttributeError:
            if warnings and not missing_pbkdf2_warned:
                print(prog+": warning: hashlib.pbkdf2_hmac requires Python 2.7.8+, using passlib instead", file=sys.stderr)
                missing_pbkdf2_warned = True
    
    import passlib.utils.pbkdf2
    passlib_pbkdf2 = passlib.utils.pbkdf2.pbkdf2
    pbkdf2_hmac = lambda hash_name, *args: passlib_pbkdf2(*args, prf= b"hmac-" + hash_name)
    return passlib  








builtin_print = print

def safe_print(*args, **kwargs):
    if kwargs.get("file") in (None, sys.stdout, sys.stderr):
        builtin_print(*_do_safe_print(*args, **kwargs), **kwargs)
    else:
        builtin_print(*args, **kwargs)

def _do_safe_print(*args, **kwargs):
    try:
        encoding = kwargs.get("file", sys.stdout).encoding or "ascii"
    except AttributeError:
        encoding = "ascii"
    converted_args = []
    for arg in args:
        if isinstance(arg, unicode):
            arg = arg.encode(encoding, errors="replace")
        converted_args.append(arg)
    return converted_args

print = safe_print


def error_exit(*messages):
    sys.exit(b" ".join(map(str, _do_safe_print(prog+": error:", *messages))))


def check_chars_range(s, error_msg, no_replacement_chars=False):
    assert isinstance(s, tstr), "check_chars_range: s is of " + unicode(tstr)
    if tstr == str:
        
        for c in s:
            if ord(c) > 127:  
                error_exit(error_msg, "has character with code point", ord(c), "> max (127 / ASCII)\n"
                                      "(see the Unicode Support section in the Tutorial and the --utf8 option)")
    else:
        
        if no_replacement_chars and "\uFFFD" in s:
            error_exit(error_msg, "contains an invalid UTF-8 byte sequence")
        "narrow" Python Unicode) builds, checks that the input unicode
        
        if sys.maxunicode < 65536:  
            for c in s:
                c = ord(c)
                if 0xD800 <= c <= 0xDBFF or 0xDC00 <= c <= 0xDFFF:
                    error_exit(error_msg, "has character with code point > max ("+unicode(sys.maxunicode)+" / Unicode BMP)")





def duplicates_removed(iterable):
    if args.no_dupchecks >= 4:
        if isinstance(iterable, basestring) or isinstance(iterable, list):
            return iterable
        return list(iterable)
    seen = set()
    unique = []
    for x in iterable:
        if x not in seen:
            unique.append(x)
            seen.add(x)
    if len(unique) == len(iterable) and (isinstance(iterable, basestring) or isinstance(iterable, list)):
        return iterable
    elif isinstance(iterable, basestring):
        return type(iterable)().join(unique)
    return unique


"hexa-fA-F" -> "hexabcdfABCDEF"
def build_wildcard_set(set_string):
    return duplicates_removed(re.sub(br"(.)-(.)", expand_single_range, set_string))

def expand_single_range(m):
    char_first, char_last = map(ord, m.groups())
    if char_first > char_last:
        raise ValueError("first character in wildcard range '"+unichr(char_first)+"' > last '"+unichr(char_last)+"'")
    return tstr().join(map(tchr, xrange(char_first, char_last+1)))




def count_valid_wildcards(str_with_wildcards, permit_contracting_wildcards = False):
    
    try:
        valid_wildcards_removed, count = \
            re.subn(br"%(?:(?:(\d+),)?(\d+))?(?:i?[{}]|i?\[.+?\]{}|(?:;.+?;(\d+)?|;(\d+))?b)"
                    .format(wildcard_keys, b"|[<>-]" if permit_contracting_wildcards else b""),
                    syntax_check_range, str_with_wildcards)
    except ValueError as e: return unicode(e)
    if tstr("%") in valid_wildcards_removed:
        invalid_wildcard_msg = "invalid wildcard (%) syntax (use %% to escape a %)"
        
        
        if not permit_contracting_wildcards and \
                count_valid_wildcards(str_with_wildcards, True) != invalid_wildcard_msg:
            return "contracting wildcards are not permitted here"
        else:
            return invalid_wildcard_msg
    if count == 0: return 0
    
    
    
    for wildcard_set in re.findall(br"%[\d,i]*\[(.+?)\]|%%", str_with_wildcards):
        if wildcard_set:
            try:   re.sub(br"(.)-(.)", expand_single_range, wildcard_set)
            except ValueError as e: return tstr(e)
    return count

def syntax_check_range(m):
    minlen, maxlen, bpos, bpos2 = m.groups()
    if minlen and maxlen and int(minlen) > int(maxlen):
        raise ValueError("max wildcard length ("+maxlen+") must be >= min length ("+minlen+")")
    if maxlen and int(maxlen) == 0:
        print(prog+": warning: %0 or %0,0 wildcards always expand to empty strings", file=sys.stderr)
    if bpos2: bpos = bpos2  
    if bpos and int(bpos) == 0:
        raise ValueError("backreference wildcard position must be > 0")
    return tstr("")



SAVESLOT_SIZE = 4096
def load_savestate(autosave_file):
    global savestate, autosave_nextslot
    savestate0 = savestate1 = first_error = None
    
    autosave_file.seek(0)
    try:
        savestate0 = cPickle.load(autosave_file)
    except Exception as e:
        first_error = e
    else:  assert autosave_file.tell() <= SAVESLOT_SIZE, "load_savestate: slot 0 data <= "+unicode(SAVESLOT_SIZE)+" bytes long"
    autosave_file.seek(0, os.SEEK_END)
    autosave_len = autosave_file.tell()
    if autosave_len > SAVESLOT_SIZE:  
        autosave_file.seek(SAVESLOT_SIZE)
        try:
            savestate1 = cPickle.load(autosave_file)
        except Exception: pass
        else:  assert autosave_file.tell() <= 2*SAVESLOT_SIZE, "load_savestate: slot 1 data <= "+unicode(SAVESLOT_SIZE)+" bytes long"
    else:
        
        autosave_file.write((SAVESLOT_SIZE - autosave_len) * b"\0")
    
    
    if savestate0 and savestate1:
        use_slot = 0 if savestate0[b"skip"] >= savestate1[b"skip"] else 1
    elif savestate0:
        if autosave_len > SAVESLOT_SIZE:
            print(prog+": warning: data in second autosave slot was corrupted, using first slot", file=sys.stderr)
        use_slot = 0
    elif savestate1:
        print(prog+": warning: data in first autosave slot was corrupted, using second slot", file=sys.stderr)
        use_slot = 1
    else:
        print(prog+": warning: data in both primary and backup autosave slots is corrupted", file=sys.stderr)
        raise first_error
    if use_slot == 0:
        savestate = savestate0
        autosave_nextslot =  1
    else:
        assert use_slot == 1
        savestate = savestate1
        autosave_nextslot =  0












class MakePeekable(object):
    def __new__(cls, file):
        if isinstance(file, MakePeekable):
            return file
        else:
            self         = object.__new__(cls)
            self._file   = file
            self._peeked = b""
            return self
    
    def peek(self):
        if not self._peeked:
            if hasattr(self._file, "peek"):
                real_peeked = self._file.peek(1)
                if len(real_peeked) >= 1:
                    return real_peeked[0]
            self._peeked = self._file.read(1)
        return self._peeked
    
    def read(self, size = -1):
        if size == 0: return tstr("")
        peeked = self._peeked
        self._peeked = b""
        return peeked + self._file.read(size - 1) if peeked else self._file.read(size)
    def readline(self, size = -1):
        if size == 0: return tstr("")
        peeked = self._peeked
        self._peeked = b""
        if peeked == b"\n": return peeked 
        if peeked == b"\r":               
            if size == 1:
                return peeked
            if self.peek() == b"\n":
                peeked = self._peeked
                self._peeked = b""
                return b"\r"+peeked       
            return peeked                 
        return peeked + self._file.readline(size - 1) if peeked else self._file.readline(size)
    def readlines(self, size = -1):
        lines = []
        while self._peeked:
            lines.append(self.readline())
        return lines + self._file.readlines(size)  
    
    def __iter__(self):
        return self
    def next(self):
        return self.readline() if self._peeked else self._file.next()
    
    reset_before_calling = {"seek", "tell", "truncate", "write", "writelines"}
    def __getattr__(self, name):
        if self._peeked and name in MakePeekable.reset_before_calling:
            self._file.seek(-1, os.SEEK_CUR)
            self._peeked = b""
        return getattr(self._file, name)
    
    def close(self):
        self._peeked = b""
        self._file.close()



"__funccall" and funccall_file is not None,



"no-exception" constraints and just return None if either fails.
"soft" fails which don't raise exceptions.)

"hard" fail) to pass up.

"b").

def open_or_use(filename, mode = "r",
        funccall_file    = None,   "__funccall"
        permit_stdin     = None,   "-" opens stdin
        default_filename = None,   
        require_data     = None,   
        new_or_empty     = None,   
        make_peekable    = None,   
        decoding_errors  = None):  
    assert not(permit_stdin and require_data), "open_or_use: stdin cannot require_data"
    assert not(permit_stdin and new_or_empty), "open_or_use: stdin is never new_or_empty"
    assert not(require_data and new_or_empty), "open_or_use: can either require_data or be new_or_empty"
    
    
    if funccall_file and filename == "__funccall":
        if require_data or new_or_empty:
            funccall_file.seek(0, os.SEEK_END)
            if funccall_file.tell() == 0:
                
                if require_data: return None
            else:
                funccall_file.seek(0)
                
                if new_or_empty: return None
        if tstr == unicode:
            if "b" in mode:
                assert not isinstance(funccall_file, io.TextIOBase), "already opened file not an io.TextIOBase; produces bytes"
            else:
                assert isinstance(funccall_file, io.TextIOBase), "already opened file isa io.TextIOBase producing unicode"
        return MakePeekable(funccall_file) if make_peekable else funccall_file;
    
    if permit_stdin and filename == "-":
        if tstr == unicode and "b" not in mode:
            sys.stdin = io.open(sys.stdin.fileno(), mode,
                                encoding= sys.stdin.encoding or "utf_8_sig", errors= decoding_errors)
        if make_peekable:
            sys.stdin = MakePeekable(sys.stdin)
        return sys.stdin
    
    
    if not filename and default_filename:
        if permit_stdin and default_filename == "-":
            if tstr == unicode and "b" not in mode:
                sys.stdin = io.open(sys.stdin.fileno(), mode,
                                    encoding= sys.stdin.encoding or "utf_8_sig", errors= decoding_errors)
            if make_peekable:
                sys.stdin = MakePeekable(sys.stdin)
            return sys.stdin
        if os.path.isfile(default_filename):
            filename = default_filename
        else:
            
            "two" extensions)
            default_filename, default_ext = os.path.splitext(default_filename)
            default_filename += default_ext + default_ext
            if os.path.isfile(default_filename):
                filename = default_filename
    if not filename:
        return None
    
    filename = tstr_from_stdin(filename)
    if require_data and (not os.path.isfile(filename) or os.path.getsize(filename) == 0):
        return None
    if new_or_empty and os.path.exists(filename) and (os.path.getsize(filename) > 0 or not os.path.isfile(filename)):
        return None
    
    if tstr == unicode and "b" not in mode:
        file = io.open(filename, mode, encoding="utf_8_sig", errors=decoding_errors)
    else:
        file = open(filename, mode)
    
    if "b" not in mode:
        if file.read(5) == br"{\rtf":
            error_exit(filename, "must be a plain text file (.txt), not a Rich Text File (.rtf)")
        file.seek(0)
    
    return MakePeekable(file) if make_peekable else file



pause_registered = None
def enable_pause():
    global pause_registered
    if pause_registered is None:
        if sys.stdin.isatty():
            atexit.register(lambda: not multiprocessing.current_process().name.startswith("PoolWorker-") and
                                    raw_input("Press Enter to exit ..."))
            pause_registered = True
        else:
            print(prog+": warning: ignoring --pause since stdin is not interactive (or was redirected)", file=sys.stderr)
            pause_registered = False


ADDRESSDB_DEF_FILENAME = "addresses.db"  


try:                  cpus = multiprocessing.cpu_count()
except StandardError: cpus = 1

parser_common = argparse.ArgumentParser(add_help=False)
prog          = unicode(parser_common.prog)
parser_common_initialized = False
def init_parser_common():
    global parser_common, parser_common_initialized, typo_types_group, bip39_group
    if not parser_common_initialized:
        
        parser_common.add_argument("--wallet",      metavar="FILE", help="the wallet file (this, --data-extract, or --listpass is required)")
        parser_common.add_argument("--typos",       type=int, metavar="COUNT", help="simulate up to this many typos; you must choose one or more typo types from the list below")
        parser_common.add_argument("--min-typos",   type=int, default=0, metavar="COUNT", help="enforce a min ")
        typo_types_group = parser_common.add_argument_group("typo types")
        typo_types_group.add_argument("--typos-capslock", action="store_true", help="try the password with caps lock turned on")
        typo_types_group.add_argument("--typos-swap",     action="store_true", help="swap two adjacent characters")
        for typo_name, typo_args in simple_typo_args.items():
            typo_types_group.add_argument("--typos-"+typo_name, **typo_args)
        typo_types_group.add_argument("--typos-insert",   metavar="WILDCARD-STRING", help="insert a string or wildcard")
        for typo_name in itertools.chain(("swap",), simple_typo_args.keys(), ("insert",)):
            typo_types_group.add_argument("--max-typos-"+typo_name, type=int, default=sys.maxint, metavar="", help="limit the number of --typos-"+typo_name+" typos")
        typo_types_group.add_argument("--max-adjacent-inserts", type=int, default=1, metavar="", help="max ")
        parser_common.add_argument("--custom-wild", metavar="STRING",    help="a custom set of characters for the %%c wildcard")
        parser_common.add_argument("--utf8",        action="store_true", help="enable Unicode mode; all input must be in UTF-8 format")
        parser_common.add_argument("--regex-only",  metavar="STRING",    help="only try passwords which match the given regular expr")
        parser_common.add_argument("--regex-never", metavar="STRING",    help="never try passwords which match the given regular expr")
        parser_common.add_argument("--delimiter",   metavar="STRING",    help="the delimiter between tokens in the tokenlist or columns in the typos-map (default: whitespace)")
        parser_common.add_argument("--skip",        type=int, default=0,    metavar="COUNT", help="skip this many initial passwords for continuing an interrupted search")
        parser_common.add_argument("--threads",     type=int, default=cpus, metavar="COUNT", help="number of worker threads (default: number of CPUs, %(default)s)")
        parser_common.add_argument("--worker",      metavar="ID",   help="divide the workload between TOTAL")
        parser_common.add_argument("--max-eta",     type=int, default=168,  metavar="HOURS", help="max estimated runtime before refusing to even start (default: %(default)s hours, i.e. 1 week)")
        parser_common.add_argument("--no-eta",      action="store_true",    help="disable calculating the estimated time to completion")
        parser_common.add_argument("--no-dupchecks", "-d", action="count", default=0, help="disable duplicate guess checking to save memory; specify up to four times for additional effect")
        parser_common.add_argument("--no-progress", action="store_true",   default=not sys.stdout.isatty(), help="disable the progress bar")
        parser_common.add_argument("--android-pin", action="store_true", help="search for the spending pin instead of the backup password in a Bitcoin Wallet for Android/BlackBerry")
        parser_common.add_argument("--blockchain-secondpass", action="store_true", help="search for the second password instead of the main password in a Blockchain wallet")
        parser_common.add_argument("--msigna-keychain", metavar="NAME",  help="keychain whose password to search for in an mSIGNA vault")
        parser_common.add_argument("--data-extract",action="store_true", help="prompt for data extracted by one of the extract-* scripts instead of using a wallet file")
        parser_common.add_argument("--mkey",        action="store_true", help=argparse.SUPPRESS)  
        parser_common.add_argument("--privkey",     action="store_true", help=argparse.SUPPRESS)  
        parser_common.add_argument("--exclude-passwordlist", metavar="FILE", nargs="?", const="-", help="never try passwords read (exactly one per line) from this file or from stdin")
        parser_common.add_argument("--listpass",    action="store_true", help="just list all password combinations to test and exit")
        parser_common.add_argument("--performance", action="store_true", help="run a continuous performance test (Ctrl-C to exit)")
        parser_common.add_argument("--pause",       action="store_true", help="pause before exiting")
        parser_common.add_argument("--version","-v",action="store_true", help="show full version information and exit")
        bip39_group = parser_common.add_argument_group("BIP-39 passwords")
        bip39_group.add_argument("--bip39",      action="store_true",   help="search for a BIP-39 password instead of from a wallet")
        bip39_group.add_argument("--mpk",        metavar="XPUB",        help="the master public key")
        bip39_group.add_argument("--addrs",      metavar="ADDRESS", nargs="+", help="if not using an mpk, address(es) in the wallet")
        bip39_group.add_argument("--addressdb",  metavar="FILE",    nargs="?", help="if not using addrs, use a full address database (default: %(const)s)", const=ADDRESSDB_DEF_FILENAME)
        bip39_group.add_argument("--addr-limit", type=int, metavar="COUNT",    help="if using addrs or addressdb, the generation limit")
        bip39_group.add_argument("--language",   metavar="LANG-CODE",   help="the wordlist language to use (see wordlists/README.md, default: auto)")
        bip39_group.add_argument("--bip32-path", metavar="PATH",        help="path (e.g. m/0'/0/) excluding the final index (default: BIP-44 account 0)")
        bip39_group.add_argument("--mnemonic-prompt", action="store_true", help="prompt for the mnemonic guess via the terminal (default: via the GUI)")
        bip39_group.add_argument("--wallet-type",     metavar="TYPE",      help="the wallet type, e.g. ethereum (default: bitcoin)")
        gpu_group = parser_common.add_argument_group("GPU acceleration")
        gpu_group.add_argument("--enable-gpu", action="store_true",     help="enable experimental OpenCL-based GPU acceleration (only supports Bitcoin Core wallets and extracts)")
        gpu_group.add_argument("--global-ws",  type=int, nargs="+",     default=[4096], metavar="PASSWORD-COUNT", help="OpenCL global work size (default: 4096)")
        gpu_group.add_argument("--local-ws",   type=int, nargs="+",     default=[None], metavar="PASSWORD-COUNT", help="OpenCL local work size; --global-ws must be evenly divisible by --local-ws (default: auto)")
        gpu_group.add_argument("--mem-factor", type=int,                default=1,      metavar="FACTOR", help="enable memory-saving space-time tradeoff for Armory")
        gpu_group.add_argument("--calc-memory",action="store_true",     help="list the memory requirements for an Armory wallet")
        gpu_group.add_argument("--gpu-names",  nargs="+",               metavar="NAME-OR-ID", help="choose GPU(s) on multi-GPU systems (default: auto)")
        gpu_group.add_argument("--list-gpus",  action="store_true",     help="list available GPU names and IDs, then exit")
        gpu_group.add_argument("--int-rate",   type=int, default=200,   metavar="RATE", help="interrupt rate: raise to improve PC's responsiveness at the expense of search performance (default: %(default)s)")
        parser_common_initialized = True




def register_simple_typo(name, help = None):
    assert name.isalpha() and name.islower(), "simple typo name must have only lowercase letters"
    assert name not in simple_typos,          "simple typo must not already exist"
    init_parser_common()  
    arg_params = dict(action="store_true")
    if help:
        args["help"] = help
    typo_types_group.add_argument("--typos-"+name, **arg_params)
    typo_types_group.add_argument("--max-typos-"+name, type=int, default=sys.maxint, metavar="", help="limit the number of --typos-"+name+" typos")
    def decorator(simple_typo_generator):
        simple_typos[name] = simple_typo_generator
        return simple_typo_generator  
    return decorator

















"--typos-insert items-to-insert", this can be







def parse_arguments(effective_argv, wallet = None, base_iterator = None,
                    perf_iterator = None, inserted_items = None, check_only = None, **kwds):

    
    
    
    
    

    
    
    if not effective_argv: enable_pause()

    
    global args
    init_parser_common()
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("-h", "--help",   action="store_true", help="show this help message and exit")
    parser.add_argument("--tokenlist",    metavar="FILE",      help="the list of tokens/partial passwords (required)")
    parser.add_argument("--max-tokens",   type=int, default=sys.maxint, metavar="COUNT", help="enforce a max ")
    parser.add_argument("--min-tokens",   type=int, default=1,          metavar="COUNT", help="enforce a min ")
    parser._add_container_actions(parser_common)
    parser.add_argument("--autosave",     metavar="FILE",      help="autosave (5 min) progress to or restore it from a file")
    parser.add_argument("--restore",      metavar="FILE",      help="restore progress and options from an autosave file (must be the only option on the command line)")
    parser.add_argument("--passwordlist", metavar="FILE", nargs="?", const="-", help="instead of using a tokenlist, read complete passwords (exactly one per line) from this file or from stdin")
    parser.add_argument("--has-wildcards",action="store_true", help="parse and expand wildcards inside passwordlists (default: wildcards are only parsed inside tokenlists)")
    
    
    try:
        import argcomplete
        argcomplete.autocomplete(parser)
    except ImportError:
        pass
    
    args = parser.parse_args(effective_argv)

    
    if args.pause: enable_pause()

    
    
    if args.utf8: enable_unicode_mode()
    else:         enable_ascii_mode()

    
    
    if args.passwordlist or base_iterator:
        parser = argparse.ArgumentParser(add_help=True)
        parser.add_argument("--passwordlist", required=not base_iterator, nargs="?", const="-", metavar="FILE", help="instead of using a tokenlist, read complete passwords (exactly one per line) from this file or from stdin")
        parser.add_argument("--has-wildcards",action="store_true", help="parse and expand wildcards inside passwordlists (default: disabled for passwordlists)")
        parser._add_container_actions(parser_common)
        
        parser.set_defaults(autosave=False, restore=False)
        args = parser.parse_args(effective_argv)

    
    elif args.help:
        parser.print_help()
        sys.exit(0)

    
    if args.version: sys.exit(0)


    if args.performance and (base_iterator or args.passwordlist or args.tokenlist):
        error_exit("--performance cannot be used with --tokenlist or --passwordlist")

    if args.list_gpus:
        devices_avail = get_opencl_devices()  
        if not devices_avail:
            error_exit("no supported GPUs found")
        for i, dev in enumerate(devices_avail, 1):
            print(""+unicode(i), dev.name.strip())
        sys.exit(0)

    
    
    TOKENS_AUTO_FILENAME = b"btcrecover-tokens-auto.txt"
    if not (args.restore or args.passwordlist or args.performance or base_iterator):
        tokenlist_file = open_or_use(args.tokenlist, "r", kwds.get("tokenlist"),
            default_filename=TOKENS_AUTO_FILENAME, permit_stdin=True, make_peekable=True)
        if hasattr(tokenlist_file, "name") and tokenlist_file.name.startswith(TOKENS_AUTO_FILENAME):
            enable_pause()  
    else:
        tokenlist_file = None

    "", parse it as additional arguments
    
    tokenlist_first_line_num = 1
    if tokenlist_file and tokenlist_file.peek() == b"": 
        first_line = tokenlist_file.readline()[1:].strip()
        tokenlist_first_line_num = 2                     
        if first_line.startswith(b"--"):                 
            print(b"Read additional options from tokenlist file: "+first_line, file=sys.stderr)
            tokenlist_args = first_line.split()          
            effective_argv = tokenlist_args + effective_argv  
            args = parser.parse_args(effective_argv)     
            
            if args.pause: enable_pause()
            for arg in tokenlist_args:
                if arg.startswith(b"--to"):              
                    error_exit("the --tokenlist option is not permitted inside a tokenlist file")
                elif arg.startswith(b"--pas"):           
                    error_exit("the --passwordlist option is not permitted inside a tokenlist file")
                elif arg.startswith(b"--pe"):            
                    error_exit("the --performance option is not permitted inside a tokenlist file")
                elif arg.startswith(b"--u"):             
                    error_exit("the --utf8 option is not permitted inside a tokenlist file")


    
    
    
    
    global savestate, restored, autosave_file
    savestate = None
    restored  = False
    
    autosave_file = open_or_use(args.restore, "r+b", kwds.get("restore"))
    if autosave_file:
        if len(effective_argv) > 2 or "=" in effective_argv[0] and len(effective_argv) > 1:
            error_exit("the --restore option must be the only option when used")
        load_savestate(autosave_file)
        effective_argv = savestate[b"argv"]  
        print("Restoring session:", " ".join(effective_argv))
        print("Last session ended having finished password ", savestate[b"skip"])
        restore_filename = args.restore      
        args = parser.parse_args(effective_argv)
        
        if args.pause: enable_pause()
        
        restored_ordering_version = savestate.get(b"ordering_version")
        if restored_ordering_version != __ordering_version__:
            if restored_ordering_version == __ordering_version__ + b"-Unicode":
                args.utf8 = True  
            else:
                error_exit("autosave was created with an incompatible version of "+prog)
        assert args.autosave,         "parse_arguments: autosave option enabled in restored autosave file"
        assert not args.passwordlist, "parse_arguments: passwordlist option not specified in restored autosave file"
        
        
        if args.utf8: enable_unicode_mode()
        
        
        tokenlist_file = open_or_use(args.tokenlist, "r", kwds.get("tokenlist"),
            default_filename=TOKENS_AUTO_FILENAME, permit_stdin=True, make_peekable=True)
        if hasattr(tokenlist_file, "name") and tokenlist_file.name.startswith(TOKENS_AUTO_FILENAME):
            enable_pause()  
        
        if tokenlist_file and tokenlist_file.peek() == b"": 
            first_line = tokenlist_file.readline()
            tokenlist_first_line_num = 2                     
            if re.match(b"", first_line, re.UNICODE):  
                print(prog+b": warning: all options loaded from restore file; ignoring options in tokenlist file '"+tokenlist_file.name+b"'", file=sys.stderr)
        print("Using autosave file '"+restore_filename+"'")
        args.skip = savestate[b"skip"]  
        restored = True  
    
    elif args.autosave:
        
        autosave_file = open_or_use(args.autosave, "r+b", kwds.get("autosave"), require_data=True)
        if autosave_file:
            
            load_savestate(autosave_file)
            restored_argv = savestate[b"argv"]
            print("Restoring session:", " ".join(restored_argv))
            print("Last session ended having finished password ", savestate[b"skip"])
            if restored_argv != effective_argv:  
                error_exit("can't restore previous session: the command line options have changed")
            
            if __ordering_version__ != savestate.get(b"ordering_version"):
                error_exit("autosave was created with an incompatible version of "+prog)
            print("Using autosave file '"+args.autosave+"'")
            args.skip = savestate[b"skip"]  
            restored = True  
        
        
        else:
            assert not (wallet or base_iterator or inserted_items), \
                        '--autosave is not supported with custom parse_arguments()'
            if args.listpass:
                print(prog+": warning: --autosave is ignored with --listpass", file=sys.stderr)
            elif args.performance:
                print(prog+": warning: --autosave is ignored with --performance", file=sys.stderr)
            else:
                
                savestate = dict(argv = effective_argv, ordering_version = __ordering_version__)


    
    init_wildcards()
    init_password_generator()

    

    
    
    
    if not (args.passwordlist or tokenlist_file or args.performance or base_iterator or args.calc_memory):
        error_exit("argument --tokenlist or --passwordlist is required (or file "+TOKENS_AUTO_FILENAME+" must be present)")

    if tokenlist_file and args.max_tokens < args.min_tokens:
        error_exit("--max-tokens must be greater than --min-tokens")

    assert not (inserted_items and args.typos_insert), "can't specify inserted_items with --typos-insert"
    if inserted_items:
        args.typos_insert = True

    
    for typo_name in itertools.chain(("swap",), simple_typos.keys(), ("insert",)):
        typo_max = args.__dict__["max_typos_"+typo_name]
        if typo_max < sys.maxint:
            
            
            if not args.__dict__["typos_"+typo_name]:
                print(prog+": warning: --max-typos-"+typo_name+" is ignored without --typos-"+typo_name, file=sys.stderr)
            
            
            elif typo_max <= 0:
                print(prog+": warning: --max-typos-"+typo_name, typo_max, "disables --typos-"+typo_name, file=sys.stderr)
                args.__dict__["typos_"+typo_name] = None
            
            
            elif args.typos and typo_max > args.typos:
                print(prog+": warning: --max-typos-"+typo_name+" ("+unicode(typo_max)+") is limited by the number of --typos ("+unicode(args.typos)+")", file=sys.stderr)

    
    if args.typos_closecase and args.typos_case:
        print(prog+": warning: specifying --typos-case disables --typos-closecase", file=sys.stderr)
        args.typos_closecase = None

    
    
    global enabled_simple_typos
    enabled_simple_typos = tuple(
        generator for name,generator in simple_typos.items() if args.__dict__["typos_"+name])

    
    any_typo_types_specified = enabled_simple_typos or \
        args.typos_capslock or args.typos_swap or args.typos_insert

    
    if not any_typo_types_specified:
        if args.min_typos > 0:
            error_exit("no passwords are produced when no type of typo is chosen, but --min-typos were required")
        if args.typos:
            print(prog+": warning: --typos has no effect because no type of typo was chosen", file=sys.stderr)
    
    else:
        if args.typos is None:
            if args.min_typos:
                print(prog+": warning: --typos COUNT not specified; assuming same as --min_typos ("+unicode(args.min_typos)+")", file=sys.stderr)
                args.typos = args.min_typos
            else:
                print(prog+": warning: --typos COUNT not specified; assuming 1", file=sys.stderr)
                args.typos = 1
        
        elif args.typos < args.min_typos:
            error_exit("--min_typos must be less than --typos")
        
        elif args.typos <= 0:
            print(prog+": warning: --typos", args.typos, " disables all typos", file=sys.stderr)
            enabled_simple_typos = args.typos_capslock = args.typos_swap = args.typos_insert = inserted_items = None

    
    global max_simple_typos, sum_max_simple_typos
    if enabled_simple_typos:
        max_simple_typos = \
            [args.__dict__["max_typos_"+name] for name in simple_typos.keys() if args.__dict__["typos_"+name]]
        if min(max_simple_typos) == sys.maxint:    
            max_simple_typos     = None
            sum_max_simple_typos = sys.maxint
        elif max(max_simple_typos) == sys.maxint:  
            sum_max_simple_typos = sys.maxint
        else:                                      
            sum_max_simple_typos = sum(max_simple_typos)

    "simple" typo)
    if args.max_adjacent_inserts != 1:
        if not args.typos_insert:
            print(prog+": warning: --max-adjacent-inserts has no effect unless --typos-insert is used", file=sys.stderr)
        elif args.max_adjacent_inserts < 1:
            print(prog+": warning: --max-adjacent-inserts", args.max_adjacent_inserts, " disables --typos-insert", file=sys.stderr)
            args.typos_insert = None
        elif args.max_adjacent_inserts > min(args.typos, args.max_typos_insert):
            if args.max_typos_insert < args.typos:
                print(prog+": warning: --max-adjacent-inserts ("+unicode(args.max_adjacent_inserts)+") is limited by --max-typos-insert ("+unicode(args.max_typos_insert)+")", file=sys.stderr)
            else:
                print(prog+": warning: --max-adjacent-inserts ("+unicode(args.max_adjacent_inserts)+") is limited by the number of --typos ("+unicode(args.typos)+")", file=sys.stderr)

    
    if inserted_items:
        args.typos_insert = False

    
    if args.custom_wild:
        global wildcard_keys
        if (args.passwordlist or base_iterator) and not \
                (args.has_wildcards or args.typos_insert or args.typos_replace):
            print(prog+": warning: ignoring unused --custom-wild", file=sys.stderr)
        else:
            args.custom_wild = tstr_from_stdin(args.custom_wild)
            check_chars_range(args.custom_wild, "--custom-wild")
            custom_set_built         = build_wildcard_set(args.custom_wild)
            wildcard_sets[tstr("c")] = custom_set_built  
            wildcard_sets[tstr("C")] = duplicates_removed(custom_set_built.upper())
            
            custom_set_caseswapped = custom_set_built.swapcase()
            if custom_set_caseswapped != custom_set_built:
                wildcard_nocase_sets[tstr("c")] = duplicates_removed(custom_set_built + custom_set_caseswapped)
                wildcard_nocase_sets[tstr("C")] = wildcard_nocase_sets[tstr("c")].swapcase()
            wildcard_keys += tstr("cC")  

    
    
    global typos_insert_expanded, typos_replace_expanded
    for arg_name, arg_val in ("--typos-insert", args.typos_insert), ("--typos-replace", args.typos_replace):
        if arg_val:
            arg_val = tstr_from_stdin(arg_val)
            check_chars_range(arg_val, arg_name)
            count_or_error_msg = count_valid_wildcards(arg_val)
            if isinstance(count_or_error_msg, basestring):
                error_exit(arg_name, arg_val, ":", count_or_error_msg)
            if count_or_error_msg:
                load_backreference_maps_from_token(arg_val)
    if args.typos_insert:
        typos_insert_expanded  = tuple(expand_wildcards_generator(args.typos_insert))
    if args.typos_replace:
        typos_replace_expanded = tuple(expand_wildcards_generator(args.typos_replace))

    if inserted_items:
        args.typos_insert     = True  
        typos_insert_expanded = tuple(inserted_items)

    if args.delimiter:
        args.delimiter = tstr_from_stdin(args.delimiter)

    
    global typos_map
    typos_map = None
    if args.typos_map:
        sha1 = hashlib.sha1() if savestate else None
        typos_map = parse_mapfile(open_or_use(args.typos_map, "r", kwds.get("typos_map")), sha1, b"--typos-map")
        
        
        
        
        if savestate:
            typos_map_hash = sha1.digest()
            del sha1
            if restored:
                if typos_map_hash != savestate[b"typos_map_hash"]:
                    error_exit("can't restore previous session: the typos-map file has changed")
            else:
                savestate[b"typos_map_hash"] = typos_map_hash
    
    
    elif (args.passwordlist or base_iterator) and args.delimiter:
        
        print(prog+": warning: ignoring unused --delimiter", file=sys.stderr)

    
    global regex_only, regex_never
    try:   regex_only  = re.compile(tstr_from_stdin(args.regex_only),  re.U) if args.regex_only  else None
    except re.error as e: error_exit("invalid --regex-only",  args.regex_only, ":", e)
    try:   regex_never = re.compile(tstr_from_stdin(args.regex_never), re.U) if args.regex_never else None
    except re.error as e: error_exit("invalid --regex-never", args.regex_only, ":", e)

    global custom_final_checker
    custom_final_checker = check_only

    if args.skip < 0:
        print(prog+": warning: --skip must be >= 0, assuming 0", file=sys.stderr)
        args.skip = 0

    if args.threads < 1:
        print(prog+": warning: --threads must be >= 1, assuming 1", file=sys.stderr)
        args.threads = 1

    if args.worker:  
        global worker_id, workers_total
        match = re.match(br"(\d+)/(\d+)$", args.worker)
        if not match:
            error_exit("--worker ID")
        worker_id     = int(match.group(1))
        workers_total = int(match.group(2))
        if workers_total < 2:
            error_exit("in --worker ID")
        if worker_id < 1:
            error_exit("in --worker ID")
        if worker_id > workers_total:
            error_exit("in --worker ID")
        worker_id -= 1  

    global have_progress, progressbar
    if args.no_progress:
        have_progress = False
    else:
        try:
            import progressbar
            have_progress = True
        except ImportError:
            have_progress = False

    
    for action in bip39_group._group_actions:
        if args.__dict__[action.dest]:
            args.bip39 = True
            break

    
    if args.mkey or args.privkey:
        args.data_extract = True

    required_args = 0
    if args.wallet:       required_args += 1
    if args.data_extract: required_args += 1
    if args.bip39:        required_args += 1
    if args.listpass:     required_args += 1
    if wallet:            required_args += 1
    if required_args != 1:
        assert not wallet, 'custom wallet object not permitted with --wallet, --data-extract, --bip39, or --listpass'
        error_exit("argument --wallet (or --data-extract, --bip39, or --listpass, exactly one) is required")

    
    global loaded_wallet
    if wallet:
        loaded_wallet = wallet

    
    if args.wallet:
        if args.android_pin:
            loaded_wallet = WalletAndroidSpendingPIN.load_from_filename(args.wallet)
        elif args.blockchain_secondpass:
            loaded_wallet = WalletBlockchainSecondpass.load_from_filename(args.wallet)
        elif args.wallet == "__null":
            loaded_wallet = WalletNull()
        else:
            load_global_wallet(args.wallet)
            if type(loaded_wallet) is WalletBitcoinj:
                print(prog+": notice: for MultiBit, use a .key file instead of a .wallet file if possible")
            if isinstance(loaded_wallet, WalletMultiBit) and not args.android_pin:
                print(prog+": notice: use --android-pin to recover the spending PIN of\n"
                           "    a Bitcoin Wallet for Android/BlackBerry backup (instead of the backup password)")
        if args.msigna_keychain and not isinstance(loaded_wallet, WalletMsigna):
            print(prog+": warning: ignoring --msigna-keychain (wallet file is not an mSIGNA vault)")


    
    
    if args.data_extract:
        key_crc_base64 = kwds.get("data_extract")  
        if not key_crc_base64:
            if tokenlist_file == sys.stdin:
                print(prog+": warning: order of data on stdin is: optional extra command-line arguments, key data, rest of tokenlist", file=sys.stderr)
            elif args.passwordlist == "-" and not sys.stdin.isatty():  
                print(prog+": warning: order of data on stdin is: key data, password list", file=sys.stderr)
            
            key_prompt = "Please enter the data from the extract script\n> "  
            try:
                if not sys.stdin.isatty() or sys.stdin.peeked:
                    key_prompt = "Reading extract data from stdin\n" 
            except AttributeError: pass
            key_crc_base64 = raw_input(key_prompt)
        
        
        
        key_crc = load_from_base64_key(key_crc_base64)
        
        
        if isinstance(loaded_wallet, WalletArmory):
            print("WARNING: an Armory private key, once decrypted, provides access to that key's Bitcoin", file=sys.stderr)
        
        if isinstance(loaded_wallet, WalletMsigna):
            if args.msigna_keychain:
                print(prog+": warning: ignoring --msigna-keychain (the extract script has already chosen the keychain)")
        elif args.msigna_keychain:
            print(prog+": warning: ignoring --msigna-keychain (--data-extract is not from an mSIGNA vault)")
        
        
        
        if savestate:
            if restored:
                if key_crc != savestate[b"key_crc"]:
                    error_exit("can't restore previous session: the encrypted key entered is not the same")
            else:
                savestate[b"key_crc"] = key_crc


    
    if args.bip39:
        if args.mnemonic_prompt:
            encoding = sys.stdin.encoding or "ASCII"
            if "utf" not in encoding.lower():
                print("terminal does not support UTF; mnemonics with non-ASCII chars might not work", file=sys.stderr)
            mnemonic = raw_input("Please enter your mnemonic (seed)\n> ")
            if not mnemonic:
                sys.exit("canceled")
            if isinstance(mnemonic, str):
                mnemonic = mnemonic.decode(encoding)  
        else:
            mnemonic = None

        args.wallet_type = args.wallet_type.strip().lower() if args.wallet_type else "bitcoin"
        loaded_wallet = WalletBIP39(args.mpk, args.addrs, args.addr_limit, args.addressdb, mnemonic,
                                    args.language, args.bip32_path, args.wallet_type, args.performance)


    
    if args.enable_gpu or args.calc_memory:
        if not hasattr(loaded_wallet, "init_opencl_kernel"):
            error_exit(loaded_wallet.__class__.__name__ + " does not support GPU acceleration")
        if isinstance(loaded_wallet, WalletBitcoinCore) and args.calc_memory:
            error_exit("--calc-memory is not supported for Bitcoin Core wallets")
        devices_avail = get_opencl_devices()  
        if not devices_avail:
            error_exit("no supported GPUs found")
        if args.int_rate <= 0:
            error_exit("--int-rate must be > 0")
        
        
        if args.gpu_names:
            
            avail_names = []  
            for i, dev in enumerate(devices_avail, 1):
                avail_names.append(""+unicode(i)+" "+dev.name.strip().lower())
            
            devices = []  
            for device_name in args.gpu_names:  
                if device_name == "":
                    error_exit("empty name in --gpus")
                device_name = device_name.lower()
                for i, avail_name in enumerate(avail_names):
                    if device_name in avail_name:  
                        devices.append(devices_avail[i])
                        avail_names[i] = ""  
                        break
                else:  
                    error_exit("can't find GPU whose name contains '"+device_name+"' (use --list-gpus to display available GPUs)")
        
        
        else:
            best_score_sofar = -1
            for dev in devices_avail:
                cur_score = 0
                if   dev.type & pyopencl.device_type.ACCELERATOR: cur_score += 8  
                elif dev.type & pyopencl.device_type.GPU:         cur_score += 4  
                if   "nvidia" in dev.vendor.lower():              cur_score += 2  
                elif "amd"    in dev.vendor.lower():              cur_score += 1  
                if cur_score >= best_score_sofar:                                 
                    if cur_score > best_score_sofar:
                        best_score_sofar = cur_score
                        devices = []
                    devices.append(dev)
            
            
            device_name = devices[0].name
            for dev in devices[1:]:
                if dev.name != device_name:
                    error_exit("can't automatically determine best GPU(s), please use the --gpu-names option")
        
        
        
        for argname, arglist in ("--global-ws", args.global_ws), ("--local-ws", args.local_ws):
            if len(arglist) == len(devices): continue
            if len(arglist) != 1:
                error_exit("number of", argname, "integers must be either one or be the number of GPUs utilized")
            arglist.extend(arglist * (len(devices) - 1))
        
        
        local_ws_warning = False
        if args.local_ws[0] is not None:  
            for i in xrange(len(args.local_ws)):
                if args.local_ws[i] < 1:
                    error_exit("each --local-ws must be a postive integer")
                if args.local_ws[i] > devices[i].max_work_group_size:
                    error_exit("--local-ws of", args.local_ws[i], "exceeds max of", devices[i].max_work_group_size, "for GPU '"+devices[i].name.strip()+"'")
                if args.global_ws[i] % args.local_ws[i] != 0:
                    error_exit("each --global-ws ("+unicode(args.global_ws[i])+") must be evenly divisible by its --local-ws ("+unicode(args.local_ws[i])+")")
                if args.local_ws[i] % 32 != 0 and not local_ws_warning:
                    print(prog+": warning: each --local-ws should probably be divisible by 32 for good performance", file=sys.stderr)
                    local_ws_warning = True
        for ws in args.global_ws:
            if ws < 1:
                error_exit("each --global-ws must be a postive integer")
            if isinstance(loaded_wallet, WalletArmory) and ws % 4 != 0:
                error_exit("each --global-ws must be divisible by 4 for Armory wallets")
            if ws % 32 != 0:
                print(prog+": warning: each --global-ws should probably be divisible by 32 for good performance", file=sys.stderr)
                break
        
        extra_opencl_args = ()
        if isinstance(loaded_wallet, WalletBitcoinCore):
            if args.mem_factor != 1:
                print(prog+": warning: --mem-factor is ignored for Bitcoin Core wallets", file=sys.stderr)
        elif isinstance(loaded_wallet, WalletArmory):
            if args.mem_factor < 1:
                error_exit("--mem-factor must be >= 1")
            extra_opencl_args = args.mem_factor, args.calc_memory
        loaded_wallet.init_opencl_kernel(devices, args.global_ws, args.local_ws, args.int_rate, *extra_opencl_args)
        if args.threads != parser.get_default("threads"):
            print(prog+": warning: --threads is ignored with --enable-gpu", file=sys.stderr)
        args.threads = 1
    
    
    else:
        for argkey in "gpu_names", "global_ws", "local_ws", "int_rate", "mem_factor":
            if args.__dict__[argkey] != parser.get_default(argkey):
                print(prog+": warning: --"+argkey.replace("_", "-"), "is ignored without --enable-gpu", file=sys.stderr)


    
    global base_password_generator, has_any_wildcards
    if base_iterator:
        assert not args.passwordlist, "can't specify --passwordlist with base_iterator"
        
        base_password_generator = base_iterator
        has_any_wildcards       = args.has_wildcards  

    
    global performance_base_password_generator
    performance_base_password_generator = perf_iterator if perf_iterator \
        else default_performance_base_password_generator

    if args.performance:
        base_password_generator = performance_base_password_generator
        has_any_wildcards       = args.has_wildcards  
        if args.listpass:
            error_exit("--performance tests require a wallet or data-extract")  

    
    if args.listpass or args.performance:
        args.no_eta = True


    
    
    
    global passwordlist_file, initial_passwordlist, passwordlist_allcached
    passwordlist_file = open_or_use(args.passwordlist, "r", kwds.get("passwordlist"),
                                    permit_stdin=True, decoding_errors="replace")
    if passwordlist_file:
        initial_passwordlist    = []
        passwordlist_allcached  = False
        has_any_wildcards       = False
        base_password_generator = passwordlist_base_password_generator
        
        if passwordlist_file == sys.stdin:
            passwordlist_isatty = sys.stdin.isatty()
            if passwordlist_isatty:  
                print("Please enter your password guesses, one per line (with no extra spaces)")
                print(exit)  "Use exit() or Ctrl-D (i.e. EOF) to exit"
            else:
                print("Reading passwordlist from stdin")
            
            for line_num in xrange(1, 1000000):
                line = passwordlist_file.readline()
                eof  = not line
                line = line.rstrip(tstr("\r\n"))
                if eof or passwordlist_isatty and line == "exit()":
                    passwordlist_allcached = True
                    break
                try:
                    check_chars_range(line, "line", no_replacement_chars=True)
                except SystemExit as e:
                    passwordlist_warn(None if passwordlist_isatty else line_num, e.code)
                    line = None  
                if args.has_wildcards and "%" in line:
                    count_or_error_msg = count_valid_wildcards(line, permit_contracting_wildcards=True)
                    if isinstance(count_or_error_msg, basestring):
                        passwordlist_warn(None if passwordlist_isatty else line_num, count_or_error_msg)
                        line = None  
                    else:
                        has_any_wildcards = True
                        try:
                            load_backreference_maps_from_token(line)
                        except IOError as e:
                            passwordlist_warn(None if passwordlist_isatty else line_num, e)
                            line = None  
                initial_passwordlist.append(line)
            
            if not passwordlist_allcached and not args.no_eta:
                
                print(prog+": warning: --no-eta has been enabled because --passwordlist is stdin and is large", file=sys.stderr)
                args.no_eta = True
        
        if not passwordlist_allcached and args.has_wildcards:
            has_any_wildcards = True  


    
    if args.no_eta:  
        if not args.no_dupchecks:
            if args.performance:
                print(prog+": warning: --performance without --no-dupchecks will eventually cause an out-of-memory error", file=sys.stderr)
            elif not args.listpass:
                print(prog+": warning: --no-eta without --no-dupchecks can cause out-of-memory failures while searching", file=sys.stderr)
        if args.max_eta != parser.get_default("max_eta"):
            print(prog+": warning: --max-eta is ignored with --no-eta, --listpass, or --performance", file=sys.stderr)


    
    if tokenlist_file:
        if tokenlist_file == sys.stdin:
            print("Reading tokenlist from stdin")
        parse_tokenlist(tokenlist_file, tokenlist_first_line_num)
        base_password_generator = tokenlist_base_password_generator


    
    
    if savestate and not restored:
        global autosave_nextslot
        autosave_file = open_or_use(args.autosave, "wb", kwds.get("autosave"), new_or_empty=True)
        if not autosave_file:
            error_exit("--autosave file '"+args.autosave+"' already exists, won't overwrite")
        autosave_nextslot = 0
        print("Using autosave file '"+args.autosave+"'")


    
    
    
    if args.exclude_passwordlist:
        exclude_file = open_or_use(args.exclude_passwordlist, "r", kwds.get("exclude_passwordlist"), permit_stdin=True)
        if exclude_file == tokenlist_file:
            error_exit("can't use stdin for both --tokenlist and --exclude-passwordlist")
        if exclude_file == passwordlist_file:
            error_exit("can't use stdin for both --passwordlist and --exclude-passwordlist")
        
        global password_dups
        password_dups = DuplicateChecker()
        sha1          = hashlib.sha1() if savestate else None
        try:
            for excluded_pw in exclude_file:
                excluded_pw = excluded_pw.rstrip(tstr("\r\n"))
                check_chars_range(excluded_pw, "--exclude-passwordlist file")
                password_dups.exclude(excluded_pw)  
                if sha1:
                    sha1.update(excluded_pw.encode("utf_8"))
        except MemoryError:
            error_exit("not enough memory to store entire --exclude-passwordlist file")
        finally:
            if exclude_file != sys.stdin:
                exclude_file.close()
        
        
        
        
        if savestate:
            exclude_passwordlist_hash = sha1.digest()
            del sha1
            if restored:
                if exclude_passwordlist_hash != savestate[b"exclude_passwordlist_hash"]:
                    error_exit("can't restore previous session: the exclude-passwordlist file has changed")
            else:
                savestate[b"exclude_passwordlist_hash"] = exclude_passwordlist_hash
        
        
        
        if args.no_dupchecks:
            password_dups.disable_duplicate_tracking()


    
    
    
    if (    not sys.stdin.closed and not sys.stdin.isatty() and (
                args.data_extract                or
                tokenlist_file    == sys.stdin   or
                passwordlist_file == sys.stdin   or
                args.exclude_passwordlist == '-' or
                args.android_pin                 or
                args.blockchain_secondpass       or
                args.mnemonic_prompt
            ) and (
                passwordlist_file != sys.stdin   or
                passwordlist_allcached
            ) and not pause_registered ):
        sys.stdin.close()   
        try:   os.close(0)  
        except StandardError: pass

    if tokenlist_file and not (pause_registered and tokenlist_file == sys.stdin):
        tokenlist_file.close()







def parse_mapfile(map_file, running_hash = None, feature_name = b"map", same_permitted = False):
    map_data = dict()
    try:
        for line_num, line in enumerate(map_file, 1):
            if line.startswith(b""): continue  
            
            
            
            split_line = line.rstrip(tstr("\r\n")).split(args.delimiter, 1)
            if split_line in ([], [tstr('')]): continue  
            if len(split_line) == 1:
                error_exit(feature_name, b"file '"+map_file.name+b"' has an empty replacement list on line", line_num)
            if args.delimiter is None: split_line[1] = split_line[1].rstrip()  

            check_chars_range(tstr().join(split_line), feature_name + b" file" + (b" '" + map_file.name + b"'" if hasattr(map_file, "name") else b""))
            for c in split_line[0]:  
                replacements = duplicates_removed(map_data.get(c, tstr()) + split_line[1])
                if not same_permitted and c in replacements:
                    map_data[c] = filter(lambda r: r != c, replacements)
                else:
                    map_data[c] = replacements
    finally:
        map_file.close()

    
    
    
    if running_hash:
        for k in sorted(map_data.keys()):  
            v = map_data[k]
            running_hash.update(k.encode("utf_8") + v.encode("utf_8"))

    return map_data







"+" (see example below).

































"$") ],











class AnchoredToken(object):
    
    POSITIONAL = 1  
    RELATIVE   = 2  
    MIDDLE     = 3  

    def __init__(self, token, line_num = "?"):
        if token.startswith(b"^"):
            
            match = re.match(br"\^(?:(?P<begin>\d+)?(?P<middle>,)(?P<end>\d+)?|(?P<rel>[rR])?(?P<pos>\d+))[\^$]", token)
            if match:
                
                if match.group(b"middle"):
                    begin = match.group(b"begin")
                    end   = match.group(b"end")
                    cached_str = tstr("^")  
                    if begin is None:
                        begin = 2
                    else:
                        begin = int(begin)
                        if begin > 2:
                            cached_str += tstr(begin)
                    cached_str += tstr(",")
                    if end is None:
                        end = sys.maxint
                    else:
                        end = int(end)
                        cached_str += tstr(end)
                    cached_str += tstr("^")
                    if begin > end:
                        error_exit("anchor range of token on line", line_num, "is invalid (begin > end)")
                    if begin < 2:
                        error_exit("anchor range of token on line", line_num, "must begin with 2 or greater")
                    self.type  = AnchoredToken.MIDDLE
                    self.begin = begin - 1
                    self.end   = end   - 1 if end != sys.maxint else end
                
                
                elif match.group(b"pos"):
                    pos = int(match.group(b"pos"))
                    cached_str = tstr("^")  
                    if match.group(b"rel"):
                        cached_str += tstr("r") + tstr(pos) + tstr("^")
                        self.type = AnchoredToken.RELATIVE
                        self.pos  = pos
                    else:
                        if pos < 1:
                            error_exit("anchor position of token on line", line_num, "must be 1 or greater")
                        if pos > 1:
                            cached_str += tstr(pos) + tstr("^")
                        self.type = AnchoredToken.POSITIONAL
                        self.pos  = pos - 1
                
                else:
                    assert False, "AnchoredToken.__init__: determined anchor type"

                self.text = token[match.end():]  
            
            
            else:
                if len(token) > 1 and token[1] in b"0123456789,":
                    print(prog+": warning: token on line", line_num, "looks like it might be a positional or middle anchor, " +
                          "but it can't be parsed correctly, so it's assumed to be a simple beginning anchor instead", file=sys.stderr)
                if len(token) > 2 and token[1].lower() == b"r" and token[2] in b"0123456789":
                    print(prog+": warning: token on line", line_num, "looks like it might be a relative anchor, " +
                          "but it can't be parsed correctly, so it's assumed to be a simple beginning anchor instead", file=sys.stderr)
                cached_str = tstr("^")  
                self.type  = AnchoredToken.POSITIONAL
                self.pos   = 0
                self.text  = token[1:]
            
            if self.text.endswith(b"$"):
                error_exit("token on line", line_num, "is anchored with both ^ at the beginning and $ at the end")
            
            cached_str += self.text  
        
        
        elif token.endswith(b"$"):
            cached_str = token
            self.type  = AnchoredToken.POSITIONAL
            self.pos   = b"$"
            self.text  = token[:-1]
        
        else: raise ValueError("token passed to AnchoredToken constructor is not an anchored token")
        
        self.cached_str  = intern(cached_str) if type(cached_str) is str else cached_str
        self.cached_hash = hash(self.cached_str)
        if self.text == "":
            print(prog+": warning: token on line", line_num, "contains only an anchor (and zero password characters)", file=sys.stderr)

    
    def __hash__(self):      return self.cached_hash
    def __eq__(self, other): return     isinstance(other, AnchoredToken) and self.cached_str == other.cached_str
    def __ne__(self, other): return not isinstance(other, AnchoredToken) or  self.cached_str != other.cached_str
    
    def __str__(self):       return     str(self.cached_str)
    def __unicode__(self):   return unicode(self.cached_str)
    
    def __repr__(self):      return self.__class__.__name__ + b"(" + repr(self.cached_str) + b")"

def parse_tokenlist(tokenlist_file, first_line_num = 1):
    global token_lists
    global has_any_duplicate_tokens, has_any_wildcards, has_any_anchors

    if args.no_dupchecks < 3:
        has_any_duplicate_tokens = False
        token_set_for_dupchecks  = set()
    has_any_wildcards   = False
    has_any_anchors     = False
    token_lists         = []

    for line_num, line in enumerate(tokenlist_file, first_line_num):

        
        if line.startswith(b""):
            if re.match(b"", line, re.UNICODE):
                print(prog+": warning: all options must be on the first line, ignoring options on line", unicode(line_num), file=sys.stderr)
            continue

        "+");
        "+", we'll remove this None later
        new_list = [None]

        
        
        new_list.extend( line.rstrip(tstr("\r\n")).split(args.delimiter) )

        
        if new_list in ([None], [None, tstr('')]): continue

        "+" is present at the beginning followed by at least one token,
        
        "+")
        if new_list[1] == b"+" and len(new_list) > 2:
            del new_list[0:2]

        
        for i, token in enumerate(new_list):
            if token is None: continue

            check_chars_range(token, "token on line " + unicode(line_num))

            
            count_or_error_msg = count_valid_wildcards(token, permit_contracting_wildcards=True)
            if isinstance(count_or_error_msg, basestring):
                error_exit("on line", unicode(line_num)+":", count_or_error_msg)
            elif count_or_error_msg:
                has_any_wildcards = True  
                load_backreference_maps_from_token(token)

            
            
            if token.startswith(b"--") and parser_common._get_option_tuples(token):
                if line_num == 1:
                    print(prog+": warning: token on line 1 looks like an option, "
                               "but line 1 did not start like this: ", file=sys.stderr)
                else:
                    print(prog+": warning: token on line", unicode(line_num), "looks like an option, "
                               " but all options must be on the first line", file=sys.stderr)

            
            if token.startswith(b"^") or token.endswith(b"$"):
                token = AnchoredToken(token, line_num)  
                new_list[i] = token
                has_any_anchors = True

            
            if args.no_dupchecks < 3 and not has_any_duplicate_tokens:
                if token in token_set_for_dupchecks:
                    has_any_duplicate_tokens = True
                    del token_set_for_dupchecks
                else:
                    token_set_for_dupchecks.add(token)

        
        token_lists.append(new_list)

    
    
    
    token_lists.reverse()

    
    
    
    if savestate:
        global backreference_maps_sha1
        token_lists_hash        = hashlib.sha1(repr(token_lists)).digest()
        backreference_maps_hash = backreference_maps_sha1.digest() if backreference_maps_sha1 else None
        if restored:
            if token_lists_hash != savestate[b"token_lists_hash"]:
                error_exit("can't restore previous session: the tokenlist file has changed")
            if backreference_maps_hash != savestate.get(b"backreference_maps_hash"):
                error_exit("can't restore previous session: one or more backreference maps have changed")
        else:
            savestate[b"token_lists_hash"] = token_lists_hash
            if backreference_maps_hash:
                savestate[b"backreference_maps_hash"] = backreference_maps_hash



def load_backreference_maps_from_token(token):
    global backreference_maps       
    global backreference_maps_sha1  
    
    
    for map_filename in re.findall(br"%[\d,]*;(.+?);\d*b|%%", token):
        if map_filename and map_filename not in backreference_maps:
            if savestate and not backreference_maps_sha1:
                backreference_maps_sha1 = hashlib.sha1()
            backreference_maps[map_filename] = \
                parse_mapfile(open(map_filename, "r"), backreference_maps_sha1, b"backreference map", same_permitted=True)







class DuplicateChecker(object):

    EXCLUDE = sys.maxint

    def __init__(self):
        self._seen_once  = dict()  
        self._duplicates = dict()  
        self._run_number = 0       
        self._tracking   = True    
                                   

    
    
    def is_duplicate(self, x):

        
        if self._run_number == 0:
            if x in self._duplicates:  
                return True
            if x in self._seen_once:   
                self._duplicates[x] = self._seen_once.pop(x)  
                return True
            
            if self._tracking:
                self._seen_once[x] = 1
            return False

        
        duplicate = self._duplicates.get(x)            
        if duplicate:
            if duplicate <= self._run_number:          
                self._duplicates[x] = self._run_number + 1  
                return False
            else:                                     
                return True
        return False                                  

    
    def exclude(self, x):
        self._seen_once[x] = self.EXCLUDE

    
    
    def disable_duplicate_tracking(self):
        self._tracking = False

    
    def run_finished(self):
        if self._run_number == 0:
            del self._seen_once  
        self._run_number += 1









def init_password_generator():
    global password_dups, token_combination_dups, passwordlist_warnings
    password_dups = token_combination_dups = None
    passwordlist_warnings = 0
    
    capslock_typos_generator.func_defaults = (0,)
    swap_typos_generator    .func_defaults = (0,)
    simple_typos_generator  .func_defaults = (0,)
    insert_typos_generator  .func_defaults = (0,)

def password_generator(chunksize = 1, only_yield_count = False):
    assert chunksize > 0, "password_generator: chunksize > 0"
    
    
    
    
    global typos_sofar
    typos_sofar = 0

    passwords_gathered = []
    passwords_count    = 0  
    worker_count = 0  
    new_args = None

    
    
    global password_dups
    if password_dups is None and args.no_dupchecks < 1:
        password_dups = DuplicateChecker()

    
    l_generator_product = generator_product
    l_regex_only        = regex_only
    l_regex_never       = regex_never
    l_password_dups     = password_dups
    l_args_worker       = args.worker
    if l_args_worker:
        l_workers_total = workers_total
        l_worker_id     = worker_id

    
    modification_generators = []
    if has_any_wildcards:    modification_generators.append( expand_wildcards_generator )
    if args.typos_capslock:  modification_generators.append( capslock_typos_generator   )
    if args.typos_swap:      modification_generators.append( swap_typos_generator       )
    if enabled_simple_typos: modification_generators.append( simple_typos_generator     )
    if args.typos_insert:    modification_generators.append( insert_typos_generator     )
    modification_generators_len = len(modification_generators)

    
    if args.min_typos:
        assert modification_generators[-1] != expand_wildcards_generator
        
        modification_generators[-1].func_defaults = (args.min_typos,)

    
    
    
    for password_base in base_password_generator() if callable(base_password_generator) else base_password_generator:

        
        
        

        
        
        
        
        
        
        
        if modification_generators_len:
            if modification_generators_len == 1:
                modification_iterator = modification_generators[0](password_base)
            else:
                modification_iterator = l_generator_product(password_base, *modification_generators)
        
        
        else:
            modification_iterator = (password_base,)

        for password in modification_iterator:

            
            if l_regex_only  and not l_regex_only .search(password): continue
            if l_regex_never and     l_regex_never.search(password): continue

            
            
            if custom_final_checker and not custom_final_checker(password): continue

            
            
            if l_password_dups and l_password_dups.is_duplicate(password):  continue

            
            if l_args_worker:
                if worker_count % l_workers_total != l_worker_id:
                    worker_count += 1
                    continue
                worker_count += 1

            
            passwords_count += 1
            if only_yield_count:
                if passwords_count >= chunksize:
                    new_args = yield passwords_count
                    passwords_count = 0
            else:
                passwords_gathered.append(password)
                if passwords_count >= chunksize:
                    new_args = yield passwords_gathered
                    passwords_gathered = []
                    passwords_count    = 0

            
            if new_args:
                chunksize, only_yield_count = new_args
                assert chunksize > 0, "password_generator.send: chunksize > 0"
                new_args = None
                yield

        assert typos_sofar == 0, "password_generator: typos_sofar == 0 after all typo generators have finished"

    if l_password_dups: l_password_dups.run_finished()

    
    if passwords_count > 0:
        yield passwords_count if only_yield_count else passwords_gathered
















def generator_product(initial_value, generator, *other_generators):
    if other_generators == ():
        for final_value in generator(initial_value):
            yield final_value
    else:
        for intermediate_value in generator(initial_value):
            for final_value in generator_product(intermediate_value, *other_generators):
                yield final_value





def tokenlist_base_password_generator():
    
    
    global token_combination_dups
    if token_combination_dups is None and args.no_dupchecks < 2 and has_any_duplicate_tokens:
        token_combination_dups = DuplicateChecker()

    
    l_len                    = len
    l_args_min_tokens        = args.min_tokens
    l_args_max_tokens        = args.max_tokens
    l_has_any_anchors        = has_any_anchors
    l_type                   = type
    l_token_combination_dups = token_combination_dups
    l_tuple                  = tuple
    l_sorted                 = sorted
    l_list                   = list
    l_tstr                   = tstr

    
    
    
    if args.no_dupchecks < 3 and has_any_duplicate_tokens:
        permutations_function = permutations_nodups
    else:
        permutations_function = itertools.permutations

    
    
    "+") have a None in their corresponding list; if this
    
    
    
    
    
    
    
    
    using_product_limitedlen = l_args_min_tokens > 5 or l_args_max_tokens < sys.maxint
    if using_product_limitedlen:
        product_generator = product_limitedlen(*token_lists, minlen=l_args_min_tokens, maxlen=l_args_max_tokens)
    else:
        product_generator = itertools.product(*token_lists)
    for tokens_combination in product_generator:

        
        
        if not using_product_limitedlen:
            tokens_combination = filter(lambda t: t is not None, tokens_combination)
            if not l_args_min_tokens <= l_len(tokens_combination) <= l_args_max_tokens: continue

        
        
        
        
        
        
        
        
        positional_anchors  = None  
        has_any_mid_anchors = False
        rel_anchors_count   = 0
        if l_has_any_anchors:
            tokens_combination_len   = l_len(tokens_combination)
            tokens_combination_nopos = []  
            invalid_anchors          = False
            for token in tokens_combination:
                if l_type(token) == AnchoredToken:
                    if token.type == AnchoredToken.POSITIONAL:  
                        pos = token.pos
                        if pos == b"$":
                            pos = tokens_combination_len - 1
                        elif pos >= tokens_combination_len:
                            invalid_anchors = True  
                            break
                        if not positional_anchors:  
                            positional_anchors = [None for i in xrange(tokens_combination_len)]
                        elif positional_anchors[pos] is not None:
                            invalid_anchors = True  
                            break
                        positional_anchors[pos] = token.text    
                    elif token.type == AnchoredToken.MIDDLE:    
                        if token.begin+1 >= tokens_combination_len:
                            invalid_anchors = True  
                            break
                        tokens_combination_nopos.append(token)  
                        has_any_mid_anchors = True
                    else:                                       
                        tokens_combination_nopos.append(token)  
                        rel_anchors_count += 1
                else:                                           
                    tokens_combination_nopos.append(token)      
            if invalid_anchors: continue
            
            if tokens_combination_nopos == []:              
                tokens_combination_nopos = ( l_tstr(""), )  
        else:
            tokens_combination_nopos = tokens_combination

        
        
        
        
        
        
        
        
        if l_token_combination_dups and \
           l_token_combination_dups.is_duplicate(l_tuple(l_sorted(tokens_combination, key=l_tstr))): continue

        
        
        
        
        for ordered_token_guess in permutations_function(tokens_combination_nopos):

            
            
            
            if rel_anchors_count:
                invalid_anchors   = False
                last_relative_pos = 0
                for i, token in enumerate(ordered_token_guess):
                    if l_type(token) == AnchoredToken and token.type == AnchoredToken.RELATIVE:
                        if token.pos < last_relative_pos:
                            invalid_anchors = True
                            break
                        if l_type(ordered_token_guess) != l_list:
                            ordered_token_guess = l_list(ordered_token_guess)
                        ordered_token_guess[i] = token.text  
                        if rel_anchors_count == 1:  
                            break
                        last_relative_pos = token.pos
                if invalid_anchors: continue

            
            if positional_anchors:
                ordered_token_guess = l_list(ordered_token_guess)
                for i, token in enumerate(positional_anchors):
                    if token is not None:
                        ordered_token_guess.insert(i, token)  

            
            
            
            
            if has_any_mid_anchors:
                if l_type(ordered_token_guess[0])  == AnchoredToken or \
                   l_type(ordered_token_guess[-1]) == AnchoredToken:
                    continue  
                invalid_anchors = False
                for i, token in enumerate(ordered_token_guess[1:-1], 1):
                    if l_type(token) == AnchoredToken:
                        assert token.type == AnchoredToken.MIDDLE, "only middle/range anchors left"
                        if token.begin <= i <= token.end:
                            if l_type(ordered_token_guess) != l_list:
                                ordered_token_guess = l_list(ordered_token_guess)
                            ordered_token_guess[i] = token.text  
                        else:
                            invalid_anchors = True
                            break
                if invalid_anchors: continue

            yield l_tstr().join(ordered_token_guess)

    if l_token_combination_dups: l_token_combination_dups.run_finished()






"repeat" argument.)




def product_limitedlen(*sequences, **kwds):
    minlen = max(kwds.get("minlen", 0), 0)  
    maxlen = kwds.get("maxlen", sys.maxint)

    if minlen > maxlen:  
        return xrange(0).__iter__()         

    if maxlen == 0:      
        
        
        for seq in sequences:
            if None not in seq: break
        else:  
            return itertools.repeat((), 1)  
        
        return xrange(0).__iter__()         

    sequences_len = len(sequences)
    if sequences_len == 0:
        if minlen == 0:  
            return itertools.repeat((), 1)  
        else:            
            return xrange(0).__iter__()     

    
    if minlen > sequences_len:
        return xrange(0).__iter__()         

    
    
    if sequences_len + 20 > sys.getrecursionlimit():
        sys.setrecursionlimit(sequences_len + 20)

    
    requireds_left_sofar = 0
    requireds_left = [None]  
    for seq in reversed(sequences[1:]):
        if None not in seq: requireds_left_sofar += 1
        requireds_left.append(requireds_left_sofar)

    return do_product_limitedlen(minlen, maxlen, requireds_left, sequences_len - 1, *sequences)


def do_product_limitedlen(minlen, maxlen, requireds_left, others_len, sequence, *other_sequences):
    
    if others_len == 0:
        
        
        if minlen == 1:
            for choice in sequence:
                if choice is not None: yield (choice,)
        
        else:
            for choice in sequence:
                yield () if choice is None else (choice,)
        return

    
    for choice in sequence:

        
        
        if choice is None:
            
            if others_len < minlen:
                continue
            new_minlen = minlen
            new_maxlen = maxlen

            
            for rest in do_product_limitedlen(new_minlen, new_maxlen, requireds_left, others_len - 1, *other_sequences):
                yield rest

        else:
            new_minlen = minlen - 1
            new_maxlen = maxlen - 1
            
            "required" and will definitely add to the length
            
            
            if requireds_left[others_len] > new_maxlen:
                continue
            
            
            if new_maxlen == 0:
                yield (choice,)
                continue

            
            for rest in do_product_limitedlen(new_minlen, new_maxlen, requireds_left, others_len - 1, *other_sequences):
                yield (choice,) + rest



"r" argument.)

def permutations_nodups(sequence):
    
    l_len = len

    sequence_len = l_len(sequence)

    
    if sequence_len == 2:
        
        yield sequence if type(sequence) == tuple else tuple(sequence)
        if sequence[0] != sequence[1]:
            yield (sequence[1], sequence[0])
        return

    
    seen = set(sequence)
    if l_len(seen) == 1:
        yield sequence if type(sequence) == tuple else tuple(sequence)
        return

    
    if l_len(seen) == sequence_len:
        for permutation in itertools.permutations(sequence):
            yield permutation
        return

    
    seen = set()
    for i, choice in enumerate(sequence):
        if i > 0 and choice in seen: continue          
        if i+1 < sequence_len:       seen.add(choice)  
        for rest in permutations_nodups(sequence[:i] + sequence[i+1:]):
            yield (choice,) + rest


MAX_PASSWORDLIST_WARNINGS = 100
def passwordlist_warn(line_num, *args):
    global passwordlist_warnings  
    if passwordlist_warnings is not None:
        passwordlist_warnings += 1
        if passwordlist_warnings <= MAX_PASSWORDLIST_WARNINGS:
            print(prog+": warning: ignoring",
                  "line "+unicode(line_num)+":" if line_num else "last line:",
                  *args, file=sys.stderr)




def passwordlist_base_password_generator():
    global initial_passwordlist, passwordlist_warnings

    line_num = 1
    for password_base in initial_passwordlist:  
        if password_base is not None:           
            yield password_base
        line_num += 1                           

    if not passwordlist_allcached:
        assert not passwordlist_file.closed
        for line_num, password_base in enumerate(passwordlist_file, line_num):  
            password_base = password_base.rstrip(tstr("\r\n"))
            try:
                check_chars_range(password_base, "line", no_replacement_chars=True)
            except SystemExit as e:
                passwordlist_warn(line_num, e.code)
                continue
            if args.has_wildcards and b"%" in password_base:
                count_or_error_msg = count_valid_wildcards(password_base, permit_contracting_wildcards=True)
                if isinstance(count_or_error_msg, basestring):
                    passwordlist_warn(line_num, count_or_error_msg)
                    continue
                try:
                    load_backreference_maps_from_token(password_base)
                except IOError as e:
                    passwordlist_warn(line_num, e)
                    continue
            yield password_base

    if passwordlist_warnings:
        if passwordlist_warnings > MAX_PASSWORDLIST_WARNINGS:
            print("\n"+prog+": warning:", passwordlist_warnings-MAX_PASSWORDLIST_WARNINGS,
                  "additional warnings were suppressed", file=sys.stderr)
        passwordlist_warnings = None  

    
    if passwordlist_file != sys.stdin:
        passwordlist_file.seek(0)

    
    elif not passwordlist_allcached:
        initial_passwordlist = ()
        passwordlist_file.close()




def default_performance_base_password_generator():
    for i in itertools.count(0):
        yield tstr("Measure Performance ") + tstr(i)








def expand_wildcards_generator(password_with_wildcards, prior_prefix = None):
    if prior_prefix is None: prior_prefix = tstr()

    
    if tstr("%") not in password_with_wildcards:
        
        yield prior_prefix + password_with_wildcards
        return

    
    l_xrange = xrange
    l_len    = len
    l_min    = min
    l_max    = max

    
    "i" if present and type is one of: wildcard_keys, "<", ">", or "-"
    "%d", "%-", "%2n", "%1,3ia", etc.), or type is of the form "[custom-wildcard-set]", or
    ";file;" [""] | ";" ] "b"  <--brackets denote options
    global wildcard_re
    if not wildcard_re:
        wildcard_re = re.compile(
            br"%(?:(?:(?P<min>\d+),)?(?P<max>\d+))?(?P<nocase>i)?(?:(?P<type>[{}<>-])|\[(?P<custom>.+?)\]|(?:;(?:(?P<bfile>.+?);)?(?P<bpos>\d+)?)?(?P<bref>b))" \
            .format(wildcard_keys))
    match = wildcard_re.search(password_with_wildcards)
    assert match, "expand_wildcards_generator: parsed valid wildcard spec"

    password_prefix      = password_with_wildcards[0:match.start()]          
    full_password_prefix = prior_prefix + password_prefix                    
    password_postfix_with_wildcards = password_with_wildcards[match.end():]  

    m_bref = match.group(b"bref")
    if m_bref:  "%b" or "%;2b" or "%;map.txt;2b"
        m_bfile, m_bpos = match.group(b"bfile", b"bpos")
        m_bpos = int(m_bpos) if m_bpos else 1
        bmap = backreference_maps[m_bfile] if m_bfile else None
    else:
        
        m_custom, m_nocase = match.group(b"custom", b"nocase")
        if m_custom:  
            is_expanding = True
            wildcard_set = custom_wildcard_cache.get((m_custom, m_nocase))
            if wildcard_set is None:
                wildcard_set = build_wildcard_set(m_custom)
                if m_nocase:
                    
                    wildcard_set_caseswapped = wildcard_set.swapcase()
                    if wildcard_set_caseswapped != wildcard_set:
                        wildcard_set = duplicates_removed(wildcard_set + wildcard_set_caseswapped)
                custom_wildcard_cache[(m_custom, m_nocase)] = wildcard_set
        else:  "normal" or a contracting wildcard
            m_type = match.group(b"type")
            is_expanding = m_type not in b"<>-"
            if is_expanding:
                if m_nocase and m_type in wildcard_nocase_sets:
                    wildcard_set = wildcard_nocase_sets[m_type]
                else:
                    wildcard_set = wildcard_sets[m_type]
        assert not is_expanding or wildcard_set, "expand_wildcards_generator: found expanding wildcard set"

    
    wildcard_maxlen = match.group(b"max")
    wildcard_maxlen = int(wildcard_maxlen) if wildcard_maxlen else 1
    wildcard_minlen = match.group(b"min")
    wildcard_minlen = int(wildcard_minlen) if wildcard_minlen else wildcard_maxlen

    
    if m_bref:
        first_pos = len(full_password_prefix) - m_bpos
        if first_pos < 0:  
            wildcard_minlen = l_max(wildcard_minlen + first_pos, 0)
            wildcard_maxlen = l_max(wildcard_maxlen + first_pos, 0)
            m_bpos += first_pos  
        m_bpos *= -1             

        if bmap:  
            
            if wildcard_minlen == 0:
                
                if password_postfix_with_wildcards == "":
                    yield full_password_prefix
                
                else:
                    for password_expanded in expand_wildcards_generator(password_postfix_with_wildcards, full_password_prefix):
                        yield password_expanded

            
            
            for password_prefix_expanded in expand_mapping_backreference_wildcard(full_password_prefix, wildcard_minlen, wildcard_maxlen, m_bpos, bmap):

                
                if password_postfix_with_wildcards == "":
                    yield password_prefix_expanded
                
                else:
                    for password_expanded in expand_wildcards_generator(password_postfix_with_wildcards, password_prefix_expanded):
                        yield password_expanded

        else:  "normal" backreference wildcard (without a map file)
            
            for i in xrange(0, wildcard_minlen):
                full_password_prefix += full_password_prefix[m_bpos]

            
            i = wildcard_minlen
            while True:

                
                if password_postfix_with_wildcards == "":
                    yield full_password_prefix
                
                else:
                    for password_expanded in expand_wildcards_generator(password_postfix_with_wildcards, full_password_prefix):
                        yield password_expanded

                i += 1
                if i > wildcard_maxlen: break

                
                full_password_prefix += full_password_prefix[m_bpos]

    
    elif is_expanding:
        
        for wildcard_len in l_xrange(wildcard_minlen, wildcard_maxlen+1):

            
            for wildcard_expanded_list in itertools.product(wildcard_set, repeat=wildcard_len):

                
                if password_postfix_with_wildcards == "":
                    yield full_password_prefix + tstr().join(wildcard_expanded_list)
                    continue
                
                for password_expanded in expand_wildcards_generator(password_postfix_with_wildcards, full_password_prefix + tstr().join(wildcard_expanded_list)):
                    yield password_expanded

    
    else:
        
        
        max_from_left  = l_len(password_prefix) if m_type in b"<-" else 0
        if m_type in b">-":
            max_from_right = password_postfix_with_wildcards.find("%")
            if max_from_right == -1: max_from_right = l_len(password_postfix_with_wildcards)
        else:
            max_from_right = 0

        
        for remove_total in l_xrange(wildcard_minlen, l_min(wildcard_maxlen, max_from_left+max_from_right) + 1):

            
            
            for remove_right in l_xrange(l_max(0, remove_total-max_from_left), l_min(remove_total, max_from_right) + 1):
                remove_left = remove_total-remove_right

                password_prefix_contracted = full_password_prefix[:-remove_left] if remove_left else full_password_prefix

                
                if l_len(password_postfix_with_wildcards) - remove_right == 0:
                    yield password_prefix_contracted
                    continue
                
                for password_expanded in expand_wildcards_generator(password_postfix_with_wildcards[remove_right:], password_prefix_contracted):
                    yield password_expanded








def expand_mapping_backreference_wildcard(password_prefix, minlen, maxlen, bpos, bmap):
    for wildcard_expanded in bmap.get(password_prefix[bpos], (password_prefix[bpos],)):
        password_prefix_expanded = password_prefix + wildcard_expanded
        if minlen <= 1:
            yield password_prefix_expanded
        if maxlen > 1:
            for password_expanded in expand_mapping_backreference_wildcard(password_prefix_expanded, minlen-1, maxlen-1, bpos, bmap):
                yield password_expanded





def capslock_typos_generator(password_base, min_typos = 0):
    global typos_sofar

    min_typos -= typos_sofar
    if min_typos > 1: return  

    
    if min_typos   <= 0:          yield password_base
    if typos_sofar >= args.typos: return

    password_swapped = password_base.swapcase()
    if password_swapped != password_base:
        typos_sofar += 1
        yield password_swapped
        typos_sofar -= 1






def swap_typos_generator(password_base, min_typos = 0):
    global typos_sofar
    
    l_xrange                 = xrange
    l_itertools_combinations = itertools.combinations
    l_args_nodupchecks       = args.no_dupchecks

    
    min_typos -= typos_sofar
    if min_typos <= 0: yield password_base

    
    
    
    password_base_len = len(password_base)
    max_swaps = min(args.max_typos_swap, args.typos - typos_sofar, password_base_len // 2)
    for swap_count in l_xrange(max(1, min_typos), max_swaps + 1):
        typos_sofar += swap_count

        
        
        
        for swap_indexes in l_itertools_combinations(l_xrange(password_base_len-1), swap_count):

            
            
            
            for i in l_xrange(1, swap_count):
                if swap_indexes[i] - swap_indexes[i-1] == 1:
                    break
            else:  

                
                password = password_base
                for i in swap_indexes:
                    if password[i] == password[i+1] and l_args_nodupchecks < 4:  "swapping" these would result in generating a duplicate guess
                        break
                    password = password[:i] + password[i+1:i+2] + password[i:i+1] + password[i+2:]
                else:  
                    yield password

        typos_sofar -= swap_count




UNCASED_ID   = 0
LOWERCASE_ID = 1
UPPERCASE_ID = 2
def case_id_of(letter):
    if   letter.islower(): return LOWERCASE_ID
    elif letter.isupper(): return UPPERCASE_ID
    else:                  return UNCASED_ID




def case_id_changed(case_id1, case_id2):
    if case_id1 != case_id2 and (case_id1 == UPPERCASE_ID or case_id2 == UPPERCASE_ID):
          return True
    else: return False






"simple" because the functions in the Configurables


def simple_typos_generator(password_base, min_typos = 0):
    global typos_sofar
    
    l_xrange               = xrange
    l_itertools_product    = itertools.product
    l_product_max_elements = product_max_elements
    l_enabled_simple_typos = enabled_simple_typos
    l_max_simple_typos     = max_simple_typos
    assert len(enabled_simple_typos) > 0, "simple_typos_generator: at least one simple typo enabled"

    
    min_typos -= typos_sofar
    if min_typos <= 0: yield password_base

    
    password_base_len = len(password_base)
    max_typos         = min(sum_max_simple_typos, args.typos - typos_sofar, password_base_len)
    for typos_count in l_xrange(max(1, min_typos), max_typos + 1):
        typos_sofar += typos_count

        
        
        if l_max_simple_typos:
            simple_typo_permutations = tuple(l_product_max_elements(l_enabled_simple_typos, typos_count, l_max_simple_typos))
        else:  
            simple_typo_permutations = tuple(l_itertools_product(l_enabled_simple_typos, repeat=typos_count))

        
        
        for typo_indexes in itertools.combinations(l_xrange(password_base_len), typos_count):
            
            
            typo_indexes_ = typo_indexes + (password_base_len,)

            
            
            for typo_generators_per_target in simple_typo_permutations:

                
                
                
                
                
                typo_replacements = [ generator(password_base, index) for index, generator in
                    zip(typo_indexes, typo_generators_per_target) ]

                
                
                
                
                
                
                
                for one_replacement_set in l_itertools_product(*typo_replacements):

                    
                    
                    password = password_base[0:typo_indexes_[0]]
                    for i, replacement in enumerate(one_replacement_set):
                        password += replacement + password_base[typo_indexes_[i]+1:typo_indexes_[i+1]]
                    yield password

        typos_sofar -= typos_count














def product_max_elements(sequence, repeat, max_elements):
    if repeat == 1:
        for choice in sequence:
            yield (choice,)
        return

    
    if min(max_elements) >= repeat:
        for product in itertools.product(sequence, repeat=repeat):
            yield product
        return

    
    for i, choice in enumerate(sequence):

        
        if max_elements[i] == 1:
            for rest in product_max_elements(sequence[:i] + sequence[i+1:], repeat - 1, max_elements[:i] + max_elements[i+1:]):
                yield (choice,) + rest

        
        else:
            max_elements[i] -= 1
            for rest in product_max_elements(sequence, repeat - 1, max_elements):
                yield (choice,) + rest
            max_elements[i] += 1





def insert_typos_generator(password_base, min_typos = 0):
    global typos_sofar
    
    l_max_adjacent_inserts = args.max_adjacent_inserts
    l_xrange               = xrange
    l_itertools_product    = itertools.product

    
    min_typos -= typos_sofar
    if min_typos <= 0: yield password_base

    password_base_len = len(password_base)
    assert l_max_adjacent_inserts > 0
    if l_max_adjacent_inserts > 1:
        
        combinations_function = itertools.combinations_with_replacement
        max_inserts = min(args.max_typos_insert, args.typos - typos_sofar)
    else:
        
        combinations_function = itertools.combinations
        max_inserts = min(args.max_typos_insert, args.typos - typos_sofar, password_base_len + 1)

    
    for inserts_count in l_xrange(max(1, min_typos), max_inserts + 1):
        typos_sofar += inserts_count

        
        
        for insert_indexes in combinations_function(l_xrange(password_base_len + 1), inserts_count):

            
            
            
            if l_max_adjacent_inserts > 1 and inserts_count > l_max_adjacent_inserts:
                too_many_adjacent = False
                last_index = -1
                for index in insert_indexes:
                    if index != last_index:
                        adjacent_count = 1
                        last_index = index
                    else:
                        adjacent_count += 1
                        too_many_adjacent = adjacent_count > l_max_adjacent_inserts
                        if too_many_adjacent: break
                if too_many_adjacent: continue

            
            
            insert_indexes_ = insert_indexes + (password_base_len,)

            
            
            for one_insertion_set in l_itertools_product(typos_insert_expanded, repeat = inserts_count):

                
                
                password = password_base[0:insert_indexes_[0]]
                for i, insertion in enumerate(one_insertion_set):
                    password += insertion + password_base[insert_indexes_[i]:insert_indexes_[i+1]]
                yield password

        typos_sofar -= inserts_count







def return_verified_password_or_false(passwords):
    return loaded_wallet.return_verified_password_or_false(passwords)





loaded_wallet = None  
def init_worker(wallet, char_mode):
    global loaded_wallet
    if not loaded_wallet:
        loaded_wallet = wallet
        if char_mode == str:
            enable_ascii_mode()
        elif char_mode == unicode:
            enable_unicode_mode()
        else:
            assert False
    set_process_priority_idle()
    signal.signal(signal.SIGINT, signal.SIG_IGN)

def set_process_priority_idle():
    try:
        if sys.platform == "win32":
            import ctypes, ctypes.wintypes
            GetCurrentProcess = ctypes.windll.kernel32.GetCurrentProcess
            GetCurrentProcess.argtypes = ()
            GetCurrentProcess.restype  = ctypes.wintypes.HANDLE
            SetPriorityClass = ctypes.windll.kernel32.SetPriorityClass
            SetPriorityClass.argtypes = ctypes.wintypes.HANDLE, ctypes.wintypes.DWORD
            SetPriorityClass.restype  = ctypes.wintypes.BOOL
            SetPriorityClass(GetCurrentProcess(), 0x00000040)  
        else:
            os.nice(19)
    except StandardError: pass




def handle_oom():
    global password_dups, token_combination_dups  
    if password_dups and password_dups._run_number == 0:
        del password_dups, token_combination_dups
        gc.collect()
        print()  
        print(prog+": error: out of memory", file=sys.stderr)
        print(prog+": notice: the --no-dupchecks option will reduce memory usage at the possible expense of speed", file=sys.stderr)
        return True
    elif token_combination_dups and token_combination_dups._run_number == 0:
        del token_combination_dups
        gc.collect()
        print()  
        print(prog+": error: out of memory", file=sys.stderr)
        print(prog+": notice: the --no-dupchecks option can be specified twice to further reduce memory usage", file=sys.stderr)
        return True
    return False




def do_autosave(skip, inside_interrupt_handler = False):
    global autosave_nextslot
    assert autosave_file and not autosave_file.closed,           "do_autosave: autosave_file is open"
    assert isinstance(savestate, dict) and b"argv" in savestate, "do_autosave: savestate is initialized"
    if not inside_interrupt_handler:
        sigint_handler  = signal.signal(signal.SIGINT,  signal.SIG_IGN)    
        sigterm_handler = signal.signal(signal.SIGTERM, signal.SIG_IGN)    
        if sys.platform != "win32":  
            sighup_handler = signal.signal(signal.SIGHUP, signal.SIG_IGN)  
    
    if autosave_nextslot == 0:
        start_pos = 0
        autosave_file.seek(start_pos)
        autosave_file.write(SAVESLOT_SIZE * b"\0")
        autosave_file.flush()
        try:   os.fsync(autosave_file.fileno())
        except StandardError: pass
        autosave_file.seek(start_pos)
    else:
        assert autosave_nextslot == 1
        start_pos = SAVESLOT_SIZE
        autosave_file.seek(start_pos)
        autosave_file.truncate()
        try:   os.fsync(autosave_file.fileno())
        except StandardError: pass
    savestate[b"skip"] = skip  
    cPickle.dump(savestate, autosave_file, cPickle.HIGHEST_PROTOCOL)
    assert autosave_file.tell() <= start_pos + SAVESLOT_SIZE, "do_autosave: data <= "+unicode(SAVESLOT_SIZE)+" bytes long"
    autosave_file.flush()
    try:   os.fsync(autosave_file.fileno())
    except StandardError: pass
    autosave_nextslot = 1 if autosave_nextslot==0 else 0
    if not inside_interrupt_handler:
        signal.signal(signal.SIGINT,  sigint_handler)
        signal.signal(signal.SIGTERM, sigterm_handler)
        if sys.platform != "win32":
            signal.signal(signal.SIGHUP, sighup_handler)





def count_and_check_eta(est):
    assert est > 0.0, "count_and_check_eta: est_secs_per_password > 0.0"
    return password_generator_factory(est_secs_per_password = est)[1]




SECONDS_BEFORE_DISPLAY    = 5.0
PASSWORDS_BETWEEN_UPDATES = 100000
def password_generator_factory(chunksize = 1, est_secs_per_password = 0):
    
    

    
    if not est_secs_per_password:
        
        if args.skip <= 0:
            return password_generator(chunksize), 0
        
        elif args.skip <= PASSWORDS_BETWEEN_UPDATES:
            passwords_count_iterator = password_generator(args.skip, only_yield_count=True)
            passwords_counted = 0
            try:
                
                passwords_counted = passwords_count_iterator.next()
                passwords_count_iterator.send( (chunksize, False) )  "normal" iterator
            except StopIteration: pass
            return passwords_count_iterator, passwords_counted

    assert args.skip >= 0
    sys_stderr_isatty = sys.stderr.isatty()
    max_seconds = args.max_eta * 3600  
    passwords_count_iterator = password_generator(PASSWORDS_BETWEEN_UPDATES, only_yield_count=True)
    passwords_counted = 0
    is_displayed = False
    start = time.clock() if sys_stderr_isatty else None
    try:
        
        for passwords_counted_last in passwords_count_iterator:
            passwords_counted += passwords_counted_last
            unskipped_passwords_counted = passwords_counted - args.skip

            

            if not is_displayed and sys_stderr_isatty and time.clock() - start > SECONDS_BEFORE_DISPLAY and (
                    est_secs_per_password or passwords_counted * 1.5 < args.skip):
                print("Counting passwords ..." if est_secs_per_password else "Skipping passwords ...", file=sys.stderr)
                is_displayed = True

            if is_displayed:
                
                if est_secs_per_password:
                    
                    if unskipped_passwords_counted > 0:
                        eta = unskipped_passwords_counted * est_secs_per_password / 60
                        if eta < 90:     eta = unicode(int(eta)+1) + " minutes"  
                        else:
                            eta /= 60
                            if eta < 48: eta = unicode(int(round(eta))) + " hours"
                            else:        eta = unicode(round(eta / 24, 1)) + " days"
                        msg = "\r  {:,}".format(passwords_counted)
                        if args.skip: msg += " (includes {:,} skipped)".format(args.skip)
                        msg += "  ETA: " + eta + " and counting   "
                        print(msg, end="", file=sys.stderr)
                    
                    else:
                        print("\r  {:,} (all skipped)".format(passwords_counted), end="", file=sys.stderr)
                
                "Skipping passwords ..." was already printed)
                else:
                    print("\r  {:,}".format(passwords_counted), end="", file=sys.stderr)

            
            if unskipped_passwords_counted * est_secs_per_password > max_seconds:
                error_exit("\rat least {:,} passwords to try, ETA > --max-eta option ({} hours), exiting" \
                    .format(passwords_counted - args.skip, args.max_eta))

            
            
            if not est_secs_per_password and passwords_counted >= args.skip - PASSWORDS_BETWEEN_UPDATES:
                break

        
        if is_displayed:
            print("\rDone" + " "*74, file=sys.stderr)

        
        if est_secs_per_password:
            return None, passwords_counted

        
        
        else:
            try:
                passwords_count_iterator.send( (args.skip - passwords_counted, True) )  
                passwords_counted += passwords_count_iterator.next()
                passwords_count_iterator.send( (chunksize, False) )  "normal" iterator
            except StopIteration: pass
            return passwords_count_iterator, passwords_counted

    except SystemExit: raise  
    except BaseException as e:
        handled = handle_oom() if isinstance(e, MemoryError) and passwords_counted > 0 else False
        if not handled: print(file=sys.stderr)  

        counting_or_skipping = "counting" if est_secs_per_password else "skipping"
        including_skipped    = "(including skipped ones)" if est_secs_per_password and args.skip else ""
        print("Interrupted after", counting_or_skipping, passwords_counted, "passwords", including_skipped, file=sys.stderr)

        if handled:                          sys.exit(1)
        if isinstance(e, KeyboardInterrupt): sys.exit(0)
        raise







def main():

    
    
    def windows_ctrl_handler(signal):
        if signal == 0:   
           return False   
        
        
        
        if savestate:
            do_autosave(args.skip + passwords_tried, inside_interrupt_handler=True)  
            autosave_file.close()
        print("\nInterrupted after finishing password ", args.skip + passwords_tried, file=sys.stderr)
        if sys.stdout.isatty() ^ sys.stderr.isatty():  
            print("\nInterrupted after finishing password ", args.skip + passwords_tried)
        os._exit(1)

    
    l_savestate = savestate

    
    passwords_count = 0
    if args.listpass:
        if tstr == unicode:
            stdout_encoding = sys.stdout.encoding if hasattr(sys.stdout, "encoding") else None  
            if not stdout_encoding:
                print(prog+": warning: output will be UTF-8 encoded", file=sys.stderr)
                stdout_encoding = "utf_8"
            elif "UTF" in stdout_encoding.upper():
                stdout_encoding = None  
            else:
                print(prog+": warning: stdout's encoding is not Unicode compatible; data loss may occur", file=sys.stderr)
        else:
            stdout_encoding = None
        password_iterator, skipped_count = password_generator_factory()
        plus_skipped = " (plus " + unicode(skipped_count) + " skipped)" if skipped_count else ""
        try:
            for password in password_iterator:
                passwords_count += 1
                builtin_print(password[0] if stdout_encoding is None else password[0].encode(stdout_encoding, "replace"))
        except BaseException as e:
            handled = handle_oom() if isinstance(e, MemoryError) and passwords_count > 0 else False
            if not handled: print()  
            print("Interrupted after generating", passwords_count, "passwords" + plus_skipped, file=sys.stderr)
            if handled:                          sys.exit(1)
            if isinstance(e, KeyboardInterrupt): sys.exit(0)
            raise
        return None, unicode(passwords_count) + " password combinations" + plus_skipped

    try:
        print("Wallet difficulty:", loaded_wallet.difficulty_info())
    except AttributeError: pass

    
    
    if args.performance and args.enable_gpu:  
        est_secs_per_password = 0.01          
    else:
        if args.enable_gpu:
            inner_iterations = sum(args.global_ws)
            outer_iterations = 1
        else:
            "chunks" to reduce call overhead. One chunk includes enough passwords to
            
            CHUNKSIZE_SECONDS = 1.0 / 100.0
            measure_performance_iterations = loaded_wallet.passwords_per_seconds(0.5)
            inner_iterations = int(round(2*measure_performance_iterations * CHUNKSIZE_SECONDS)) or 1  "2*" is due to the 0.5 seconds above
            outer_iterations = int(round(measure_performance_iterations / inner_iterations))
            assert outer_iterations > 0
        
        performance_generator = performance_base_password_generator()  
        start = timeit.default_timer()
        
        for o in xrange(outer_iterations):
            loaded_wallet.return_verified_password_or_false(list(
                itertools.islice(itertools.ifilter(custom_final_checker, performance_generator), inner_iterations)))
        est_secs_per_password = (timeit.default_timer() - start) / (outer_iterations * inner_iterations)
        del performance_generator
        assert isinstance(est_secs_per_password, float) and est_secs_per_password > 0.0

    if args.enable_gpu:
        chunksize = sum(args.global_ws)
    else:
        
        chunksize = int(round(CHUNKSIZE_SECONDS / est_secs_per_password)) or 1

    
    "worker" thread
    if est_secs_per_password < 1.0 / 75000.0:
        main_thread_is_worker = True
        spawned_threads   = args.threads - 1      
        verifying_threads = spawned_threads or 1
    else:
        main_thread_is_worker = False
        spawned_threads   = args.threads if args.threads > 1 else 0
        verifying_threads = args.threads

    
    est_secs_per_password /= min(verifying_threads, cpus)

    
    if not args.no_eta:

        assert args.skip >= 0
        if l_savestate and b"total_passwords" in l_savestate and args.no_dupchecks:
            passwords_count = l_savestate[b"total_passwords"]  
            iterate_time = 0
        else:
            start = time.clock()
            passwords_count = count_and_check_eta(est_secs_per_password)
            iterate_time = time.clock() - start
            if l_savestate:
                if b"total_passwords" in l_savestate:
                    assert l_savestate[b"total_passwords"] == passwords_count, "main: saved password count matches actual count"
                else:
                    l_savestate[b"total_passwords"] = passwords_count

        passwords_count -= args.skip
        if passwords_count <= 0:
            return False, "Skipped all "+unicode(passwords_count + args.skip)+" passwords, exiting"

        
        if l_savestate or not have_progress:
            eta_seconds = passwords_count * est_secs_per_password
            
            if spawned_threads == 0 and not args.enable_gpu or spawned_threads >= cpus:
                eta_seconds += iterate_time
            if l_savestate:
                est_passwords_per_5min = int(round(passwords_count / eta_seconds * 300.0))
                assert est_passwords_per_5min > 0
            eta_seconds = int(round(eta_seconds)) or 1

    
    elif l_savestate:
        est_passwords_per_5min = int(round(300.0 / est_secs_per_password))
        assert est_passwords_per_5min > 0

    
    
    if not args.no_eta and spawned_threads * chunksize > passwords_count:
        if spawned_threads > passwords_count:
            spawned_threads = passwords_count
        chunksize = (passwords_count-1) // spawned_threads + 1

    
    if args.skip > 0:
        print("Starting with password ", args.skip + 1)
    password_iterator, skipped_count = password_generator_factory(chunksize)
    if skipped_count < args.skip:
        assert args.no_eta, "discovering all passwords have been skipped this late only happens if --no-eta"
        return False, "Skipped all "+unicode(skipped_count)+" passwords, exiting"
    assert skipped_count == args.skip

    if args.enable_gpu:
        cl_devices = loaded_wallet._cl_devices
        if len(cl_devices) == 1:
            print("Using OpenCL", pyopencl.device_type.to_string(cl_devices[0].type), cl_devices[0].name.strip())
        else:
            print("Using", len(cl_devices), "OpenCL devices:")
            for dev in cl_devices:
                print(" ", pyopencl.device_type.to_string(dev.type), dev.name.strip())
    else:
        print("Using", args.threads, "worker", "threads" if args.threads > 1 else "thread")  

    if have_progress:
        if args.no_eta:
            progress = progressbar.ProgressBar(maxval=progressbar.UnknownLength, poll=0.1, widgets=[
                progressbar.AnimatedMarker(),
                progressbar.FormatLabel(b" %(value)d  elapsed: %(elapsed)s  rate: "),
                progressbar.FileTransferSpeed(unit=b"P")
            ])
            progress.update_interval = sys.maxint  
        else:
            progress = progressbar.ProgressBar(maxval=passwords_count, poll=0.1, widgets=[
                progressbar.SimpleProgress(), b" ",
                progressbar.Bar(left=b"[", fill=b"-", right=b"]"),
                progressbar.FormatLabel(b" %(elapsed)s, "),
                progressbar.ETA()
            ])
    else:
        progress = None
        if args.no_eta:
            print("Searching for password ...")
        else:
            
            print("Will try {:,} passwords, ETA ".format(passwords_count), end="")
            eta_hours    = eta_seconds // 3600
            eta_seconds -= 3600 * eta_hours
            eta_minutes  = eta_seconds // 60
            eta_seconds -= 60 * eta_minutes
            if eta_hours   > 0: print(eta_hours,   "hours ",   end="")
            if eta_minutes > 0: print(eta_minutes, "minutes ", end="")
            if eta_hours  == 0: print(eta_seconds, "seconds ", end="")
            print("...")

    
    if l_savestate: do_autosave(args.skip)

    
    
    gc.collect()

    
    
    if spawned_threads == 0:
        pool = None
        password_found_iterator = itertools.imap(return_verified_password_or_false, password_iterator)
        set_process_priority_idle()  
    else:
        pool = multiprocessing.Pool(spawned_threads, init_worker, (loaded_wallet, tstr))
        password_found_iterator = pool.imap(return_verified_password_or_false, password_iterator)
        if main_thread_is_worker: set_process_priority_idle()  

    
    
    windows_handler_routine = None
    try:
        sigint_handler = signal.getsignal(signal.SIGINT)
        signal.signal(signal.SIGTERM, sigint_handler)     
        if sys.platform != "win32":
            signal.signal(signal.SIGHUP, sigint_handler)  
        else:
            import ctypes, ctypes.wintypes
            HandlerRoutine = ctypes.WINFUNCTYPE(ctypes.wintypes.BOOL, ctypes.wintypes.DWORD)
            SetConsoleCtrlHandler = ctypes.windll.kernel32.SetConsoleCtrlHandler
            SetConsoleCtrlHandler.argtypes = HandlerRoutine, ctypes.wintypes.BOOL
            SetConsoleCtrlHandler.restype  = ctypes.wintypes.BOOL
            windows_handler_routine = HandlerRoutine(windows_ctrl_handler)  
            SetConsoleCtrlHandler(windows_handler_routine, True)
    except StandardError: pass

    
    
    if l_savestate:
        assert isinstance(est_passwords_per_5min, numbers.Integral)
        assert isinstance(chunksize,              numbers.Integral)
        est_passwords_per_5min = (est_passwords_per_5min // chunksize or 1) * chunksize

    
    password_found  = False
    passwords_tried = 0
    if progress: progress.start()
    try:
        for password_found, passwords_tried_last in password_found_iterator:
            if password_found:
                if pool:
                    
                    
                    
                    
                    pool.close()
                    global _pool
                    _pool = pool
                passwords_tried += passwords_tried_last - 1  
                if progress:
                    progress.next_update = 0  
                    progress.update(passwords_tried)
                    print()  
                break
            passwords_tried += passwords_tried_last
            if progress: progress.update(passwords_tried)
            if l_savestate and passwords_tried % est_passwords_per_5min == 0:
                do_autosave(args.skip + passwords_tried)
        else:  
            if pool: pool.close()
            if progress:
                if args.no_eta:
                    progress.maxval = passwords_tried
                else:
                    progress.widgets.pop()  
                progress.finish()
            if pool: pool.join()  

    
    
    
    
    except BaseException as e:
        handled = handle_oom() if isinstance(e, MemoryError) and passwords_tried > 0 else False
        if not handled: print()  
        if pool: pool.close()

        print("Interrupted after finishing password ", args.skip + passwords_tried, file=sys.stderr)
        if sys.stdout.isatty() ^ sys.stderr.isatty():  
            print("Interrupted after finishing password ", args.skip + passwords_tried)

        if not handled and not isinstance(e, KeyboardInterrupt): raise
        password_found = None  
    finally:
        if windows_handler_routine:
            SetConsoleCtrlHandler(windows_handler_routine, False)

    
    
    if l_savestate:
        do_autosave(args.skip + passwords_tried)
        autosave_file.close()

    return (password_found, "Password search exhausted" if password_found is False else None)
