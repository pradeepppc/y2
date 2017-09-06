from struct import *
packed_data = pack('iif',6,48,1.235)
print(packed_data)
print(calcsize('i'))
print(unpack('iif',packed_data))