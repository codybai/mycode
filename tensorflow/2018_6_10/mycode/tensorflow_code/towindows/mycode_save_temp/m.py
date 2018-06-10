indices=[[0,0],[0,1],[0,2],[1,1],[1,2],[2,2,],[2,3],[3,2],[3,3],[3,4]]
value=[1,2,3,4,5,6,7,8,9,7]
shape=[4,6]
y=[indices,value,shape]
def deconde(sparse_tensor):
    decoded_indexes = list()
    current_i = 0
    current_seq = []
    for offset, i_and_index in enumerate(sparse_tensor[0]):
        i = i_and_index[0]
        if i != current_i:
            decoded_indexes.append(current_seq)
            current_i = i
            current_seq = list()
        current_seq.append(offset)
    decoded_indexes.append(current_seq)
    result = []
    for index in decoded_indexes:
        result.append(decode_a_seq(index, sparse_tensor))
    return result
def decode_a_seq(indexes, spars_tensor):
    decoded = []
    for m in indexes:
        str = spars_tensor[1][m]
        decoded.append(str)
    return decoded
print(deconde(y))
