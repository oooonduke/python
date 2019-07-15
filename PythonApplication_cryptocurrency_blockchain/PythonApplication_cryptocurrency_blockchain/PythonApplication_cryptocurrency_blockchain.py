import datetime as date
import hashlib as hasher

class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.hash_block()

    def hash_block(self):
        """
        generates a cryptographic hash of the block’s index, timestamp, data, and the hash of the previous block’s hash.
        hash_block => '18627f84562249c397955a1bbde617992fea2180afe0e4645ea131df12051a20'
        """
        sha = hasher.sha256()
        sha.update((str(self.index) +
                   str(self.timestamp) +
                   str(self.data) +
                   str(self.previous_hash)).encode('utf-8'))
        return sha.hexdigest()

def create_genesis_block():
    """
    manually creates a first block of a blockchain with index of 0 and
    arbitrary previous hash.
    first_block = create_genesis_block()
    first_block
    """
    return Block(0, date.datetime.now(), "Genesis Block", "0")

def next_block(last_block):
    this_index = last_block.index + 1
    this_timestamp = date.datetime.now()
    this_data = "Hey! I'm block " + str(this_index)
    this_hash = last_block.hash
    return Block(this_index, this_timestamp, this_data, this_hash)

blockchain = [create_genesis_block()]
previous_block = blockchain[0]

num_of_blocks_to_add = 20

for i in range(0, num_of_blocks_to_add):
    blocks_to_add = next_block(previous_block)
    blockchain.append(blocks_to_add)
    previous_block = blocks_to_add
    print("Block {} has been added to the blockchain!".format(blocks_to_add.index))
    print("Hash: {}\n".format(blocks_to_add.hash))