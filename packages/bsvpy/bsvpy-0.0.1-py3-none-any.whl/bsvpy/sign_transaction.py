from bsvpy.ec_point_operation import curve, scalar_multiply
from bsvpy.meta import int_to_varint, address_to_public_key_hash, build_locking_script, deserialize_signature, serialize_signature, serialize_public_key, public_key_to_address, private_key_to_wif
from bsvpy.crypto import double_sha256
from bsvpy.sign import verify_signature, sign
from collections import namedtuple
from binascii import unhexlify, hexlify
from urllib import request
import json
import requests

VERSION = 0x01.to_bytes(4, 'little')
SEQUENCE = 0xffffffff.to_bytes(4, byteorder='little')
LOCK_TIME = 0x00.to_bytes(4, byteorder='little')

SH_ALL = 0x01
SH_FORKID = 0x40
SIGHASH_ALL = SH_ALL | SH_FORKID
P_0 = b'\x00'
OP_FALSE = b'\00'
OP_CHECKLOCKTIMEVERIFY = b'\xb1'
OP_CHECKSIG = b'\xac'
OP_DUP = b'v'
OP_EQUALVERIFY = b'\x88'
OP_HASH160 = b'\xa9'
OP_PUSH_20 = b'\x14'
OP_RETURN = b'\x6a'
OP_PUSHDATA1 = b'\x4c'
OP_PUSHDATA2 = b'\x4d'
OP_PUSHDATA4 = b'\x4e'




OP_DUP = b'\x76'
OP_HASH160 = b'\xa9'
OP_PUSH_20 = b'\x14'
OP_EQUALVERIFY = b'\x88'
OP_CHECKSIG = b'\xac'


class TxIn:
    def __init__(self, satoshi: int, txid: str, index: int, locking_script: str, sequence: bytes = SEQUENCE) -> None:
        self.satoshi = satoshi.to_bytes(8, byteorder='little')
        self.txid = unhexlify(txid)[::-1]
        self.index = index.to_bytes(4, byteorder='little')
        self.locking_script = unhexlify(locking_script)
        self.locking_script_len = int_to_varint(len(self.locking_script))
        self.unlocking_script = b''
        self.unlocking_script_len = b''
        self.sequence = sequence


#TxOut = namedtuple('TxOut', 'address satoshi')

def get_op_pushdata_code(dest):
    length_data = len(dest)
    if length_data <= 0x4c:  # (https://en.bitcoin.it/wiki/Script)
        return length_data.to_bytes(1, byteorder='little')
    elif length_data <= 0xff:
        return OP_PUSHDATA1 + length_data.to_bytes(1, byteorder='little')  # OP_PUSHDATA1 format
    elif length_data <= 0xffff:
        return OP_PUSHDATA2 + length_data.to_bytes(2, byteorder='little')  # OP_PUSHDATA2 format
    else:
        return OP_PUSHDATA4 + length_data.to_bytes(4, byteorder='little')  # OP_PUSHDATA4 format


def serialize_outputs(outputs: list,custom_pushdata=False) -> bytes:

    """
    Serialize outputs [(address, satoshi), (address, satoshi), ...]
    to format (satoshi || LEN(locking_script) || locking_script) || (satoshi || LEN(locking_script) || locking_script) || ...)
    """
    output_block = b''
    #print(outputs)
    for data in outputs:
        dest, amount = data
        #print('data:',data)
        #print('dest:',dest)
        #print('amount:',amount)

        # Real recipient
        if amount:
            script = (OP_DUP + OP_HASH160 + OP_PUSH_20 +
                      address_to_public_key_hash(dest) +
                      OP_EQUALVERIFY + OP_CHECKSIG)
            #print(address_to_public_key_hash(dest))

            output_block += amount.to_bytes(8, byteorder='little')

        # Blockchain storage
        else:
            if custom_pushdata is False:
                script = OP_FALSE + OP_RETURN + get_op_pushdata_code(dest) + dest
                output_block += b'\x00\x00\x00\x00\x00\x00\x00\x00'

            elif custom_pushdata is True:
                #manual control over number of bytes in each batch of pushdata
                if type(dest) != bytes:
                    raise TypeError("custom pushdata must be of type: bytes")
                else:
                    script = (OP_FALSE + OP_RETURN + dest)

                output_block += b'\x00\x00\x00\x00\x00\x00\x00\x00'

        # Script length in wiki is "Var_int" but there's a note of "modern BitcoinQT" using a more compact "CVarInt"
        output_block += int_to_varint(len(script))
        output_block += script
        output_bytes=output_block

        

    #return output_block

    #print('output_bytes1:',output_bytes) 
    #output_bytes = b''
    #for output in outputs:
        #output_bytes += output.satoshi.to_bytes(8, byteorder='little') + build_locking_script(address_to_public_key_hash(output.address))
    #print('output_bytes2:',output_bytes)   
    return output_bytes


def transaction_digest(tx_ins: list, tx_outs: list, lock_time: bytes = LOCK_TIME, sighash: int = SIGHASH_ALL) -> list:
    """Returns the digest of unsigned transaction according to SIGHASH"""
    # BIP-143 https://github.com/bitcoin/bips/blob/master/bip-0143.mediawiki
    #  1. nVersion of the transaction (4-byte little endian)
    #  2. hashPrevouts (32-byte hash)
    #  3. hashSequence (32-byte hash)
    #  4. outpoint (32-byte hash + 4-byte little endian)
    #  5. scriptCode of the input (serialized as scripts inside CTxOuts)
    #  6. value of the output spent by this input (8-byte little endian)
    #  7. nSequence of the input (4-byte little endian)
    #  8. hashOutputs (32-byte hash)
    #  9. nLocktime of the transaction (4-byte little endian)
    # 10. sighash type of the signature (4-byte little endian)
    if sighash == SIGHASH_ALL:
        hash_prevouts = double_sha256(b''.join([tx_in.txid + tx_in.index for tx_in in tx_ins]))
        hash_sequence = double_sha256(b''.join([tx_in.sequence for tx_in in tx_ins]))
        hash_outputs = double_sha256(serialize_outputs(tx_outs))
        digests = []
        for tx_in in tx_ins:
            digests.append(
                VERSION +
                hash_prevouts + hash_sequence +
                tx_in.txid + tx_in.index + tx_in.locking_script_len + tx_in.locking_script + tx_in.satoshi + tx_in.sequence +
                hash_outputs +
                lock_time +
                sighash.to_bytes(4, byteorder='little')
            )
        return digests
    raise ValueError(f'Unsupported SIGHASH value {sighash}')


def serialize_transaction(tx_ins: list, tx_outs: list, lock_time: bytes = LOCK_TIME) -> bytes:
    """Serialize signed transaction"""
    # version
    raw_transaction = VERSION
    # inputs
    raw_transaction += int_to_varint(len(tx_ins))
    for tx_in in tx_ins:
        raw_transaction += tx_in.txid + tx_in.index + tx_in.unlocking_script_len + tx_in.unlocking_script + tx_in.sequence
    # outputs
    raw_transaction += int_to_varint(len(tx_outs)) + serialize_outputs(tx_outs)
    # lock_time
    raw_transaction += lock_time
    return raw_transaction



def address_str(priv_key:int):#整数key求地址
    
    pub_key = scalar_multiply(priv_key, curve.g)
    return public_key_to_address(pub_key)
    
def pub_key(priv_key:int):#整数key求公钥
    
    return scalar_multiply(priv_key, curve.g)

def get_data(url):# 获取网页数据

    req = request.Request(url)
    with request.urlopen(req) as f:
        data=f.read().decode()
    return data


    
def scriptPubKey(address):#获取锁定脚本
    url='https://api.whatsonchain.com/v1/bsv/main/address/{0}/info'.format(address)
    a=get_data(url).replace('true','"true"')
    b=a.replace('false','"false"')

    return(eval(b)["scriptPubKey"])
    
    

#print(address(123))
#print(pub_key(123))


def send_to(priv_key:int,send_to_address:str,send_to_satoshi=160,send_to_message=None):
    
    pub_key = scalar_multiply(priv_key, curve.g) # 公钥

    address=address_str(priv_key) #发送方地址
    
    
    url='https://api.whatsonchain.com/v1/bsv/main/address/{0}/unspent'.format(address)
    unspent=eval(get_data(url))
    address_locking=scriptPubKey(address)
    inputssss=''
    all_satoshi=0
    for i in unspent:
        unspent_satoshi=i['value']
        unspent_txid=i['tx_hash']
        unspent_index=i['tx_pos']
        all_satoshi+=unspent_satoshi  #未花费总数
        inputssss=inputssss+'TxIn(satoshi={0}, txid="{1}", index={2}, locking_script="{3}"),'.format(unspent_satoshi,unspent_txid,unspent_index,address_locking)
    inputss='['+inputssss[:-1]+']'
    #print(inputss)
    inputs=eval(inputss)
    #print(inputs)
        
    

    
    #inputs = [
        #TxIn(satoshi=100000, txid='b811bc9bbcc84c6b3a2376511478ee7d262e8ab6809b775f115cbce0577841d9', index=0, locking_script='76a914894acc947768ee6f16929e47ec4a0af137da086088ac'),]
    #print(inputs)
     

    serialized_pub_key = serialize_public_key(pub_key)
    tx_inputs = inputs[0:]
    #tx_outputs = [TxOut(address='1Lkqjn1L8Th2PkojGTorASNJL8s1mj1xZR', satoshi=111),]

    send_to_message=send_to_message.encode('utf-8')
    len_message=len(send_to_message) # 字节长度
    self_satoshi=all_satoshi-send_to_satoshi- len_message-200   #剩余返回自己
    
    tx_outputs = [(send_to_address,send_to_satoshi),(send_to_message,0),(address,self_satoshi)] #剩余返回自己

    
    #print(tx_outputs)
    tx_digests = transaction_digest(tx_inputs, tx_outputs)
    for i in range(len(tx_digests)):
        tx_digest = tx_digests[i]
        sig = sign(priv_key, tx_digest)
        serialized_sig = serialize_signature(sig)
        # unlocking_script = LEN + der + sighash + LEN + public_key
        tx_inputs[i].unlocking_script = bytes([len(serialized_sig) + 1]) + serialized_sig + bytes([SIGHASH_ALL, len(serialized_pub_key)]) + serialized_pub_key
        #print(hexlify(tx_inputs[i].unlocking_script))
        tx_inputs[i].unlocking_script_len = int_to_varint(len(tx_inputs[i].unlocking_script))
        #print(hexlify(tx_inputs[i].unlocking_script_len))
    raw = serialize_transaction(tx_inputs, tx_outputs)
    
    raw_tx=hexlify(raw).decode()
    #print(raw_tx)
    url='https://api.whatsonchain.com/v1/bsv/main/tx/raw'
    data = json.dumps({"txhex":raw_tx})
    r =requests.post(url, data=data, timeout=10)
    
    return r.json() # 返回交易哈希或者错误信息


    #print(get_data(url))
    #return hexlify(raw)
    #tx_id = double_sha256(raw)[::-1]
    #print(hexlify(tx_id))

if __name__ == '__main__':
    send_to(priv_key=123,send_to_address='1Lkqjn1L8Th2PkojGTorASNJL8s1mj1xZR',send_to_message='80tes1111t')

