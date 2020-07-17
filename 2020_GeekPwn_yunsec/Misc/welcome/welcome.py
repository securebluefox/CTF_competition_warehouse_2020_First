def decoder(string):
    len_str = len(string)
    if len_str % 16 != 0:
        return 0
    result = ''
    for x in range(0, len_str, 16):
        decode_char = string[x:x+16]
        temp_int = [ENSTRS.index(decode_char[y:y+2]) for y in range(0, 16, 2)]
        int_list = [temp_int[x]+temp_int[x+1] for x in range(0, 8, 2)]
        bin_temp = [bin(i).replace('0b', '') for i in int_list]
        binstr_list = []
        for b in bin_temp:            
            if len(b) < 4:                
                binstr_list.append(b.zfill(4))            
            else:                
                binstr_list.append(b)        
        binstr = ''.join(binstr_list)        
        result = result + chr(int(binstr, 2))    
    return result

def encoder(string):    
    result = ''    
    binstr_list = [b.replace('0b', '') for b in [bin(ord(c)) for c in string]]    
    for binstr in binstr_list:        
        len_binstr = len(binstr)        
        if len_binstr < 16:            
            binstr = binstr.zfill(16)        
        temp_list = [binstr[start:start+4] for start in range(0, 16, 4)]        
        int_list = []        
        for i in temp_list:            
            i = int(i, 2)        
            if i >= 11:                
                int_list.append(11)                
                int_list.append(i - 11)            
            else:                
                int_list.append(0)                
                int_list.append(i)        
        result = result + ''.join([ENSTRS[index] for index in int_list])    
    return result
    
ENSTRS = ("富强", "民主", "文明", "和谐", "自由", "平等","公正", "法治", "爱国", "敬业", "诚信", "友善")
while True:    
    input_str = input("1. 加密    2. 解密\n请选择：")    
    if input_str in ['eof', 'EOF', 'quit', 'QUIT', 'exit', 'EXIT']:        
        break    
    elif input_str in ['1', '加密']:        
        encode_str = input("请输入字符串：\n")        
        result = encoder(encode_str)        
        print("加密结果：\n{}".format(result))    
    elif input_str in ['2', '解密']:        
        decode_str = input("请输入加密字符串：\n")        
        result = decoder(decode_str)        
        print("解密结果:\n{}".format(result))    
    else:        
        print("输入有误！")