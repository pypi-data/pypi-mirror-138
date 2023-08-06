import io

import pycparser
from cffi import FFI

if __name__ == '__main__':
    parser = pycparser.CParser()
    parsed = parser.parse("""
    int foo() {}
    
    int main() {
      foo();
      return 0;
    }""")

    ffi = FFI()
    cdecl = ffi.cdef("""
        typedef struct {
            unsigned char r, g, b, a;
            unsigned char x : 4;
            unsigned char y : 4;
            unsigned char z[];
        } a_struct;
    """)
    a_struck_size = ffi.sizeof('a_struct')
    struck = ffi.new("a_struct*")
    io.BytesIO()
    original = io.BytesIO(bytes.fromhex('41' * a_struck_size))
    ffi.buffer(struck)
    original_val = original.read(a_struck_size)
    print(f"{original_val.hex()=}")
    struck.r = 0xde
    struck.g = 0xad
    struck.b = 0xbe
    struck.a = 0xef
    struck.x = 2
    struck.y = 0xa
    try:
        struck.y = 1337
    except OverflowError as oe:
        print(oe)
    struck.z = bytes.fromhex('41414141414141414141414141')
    print(struck)
    buf = ffi.buffer(struck)
    new_val = io.BytesIO(buf).read()
    print(f"{new_val.hex()=}")
