import caesar_switch as caesar
import Noise


def serial_decrypt(code, decy_code):
    bin_command = bin(decy_code)[2:10]
    offset_str = bin_command[4:]
    offset = 3 + int(offset_str, 2)
    cmd = bin_command[3::-1]

    for i in range(4):
        if cmd[i] == '1':
            if int(i) % 2 == 0:
                code = Noise.de_swt(code, offset)
            else:
                code = caesar.dec(code, offset)

    return code


if __name__ == '__main__':
    print(serial_decrypt('x`i(9\\ NK/jqqaL\'3A\x0c9|gouaT-*<*kkC?fL\tbr#\\#0&=UcEjiYMvY\x16D:+P}.:8VzOz.rc_.\t!n^zdUp\\^SvN`sa~ DhsDQZAAU$a,i9c "N\r~iC@10\'>2$ {\'(p?@\x17ev+`wcbvHk|SK/M"\\D5E5zV/|81+YOb1\\89\x05([.OWn81`{`Ls#4)=D1w(0jV5d3\\uGn4[?H\x06l}>9SEp iY>^v/G.p\x19pH?tr{Ue%GW2CWlZ/\x0b7bODzj@HS~C|!OD=L', 191))
