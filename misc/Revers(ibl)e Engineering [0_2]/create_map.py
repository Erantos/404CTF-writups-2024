import json
from tqdm import tqdm
from blueqat import Circuit

gate_map = {
    "NOT": 'x',
    "CNOT": 'cx',
    "TOFFOLI": 'ccx'
}

gate_map_inv = {
    "x": 'NOT',
    "cx": 'CNOT',
    "ccx": 'TOFFOLI'
}

unit_matrices = {}

not_index = [0, 1, 2]
cnot_index = [(0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1)]
ccx_index = [(0, 1, 2), (0, 2, 1), (1, 2, 0)]
all_gates = [('x', i) for i in not_index] + [('cx', i) for i in cnot_index] + [('ccx', i) for i in ccx_index]

# Generate all possible circuit of `level` number of gates (as hex number)
def gen_all_encoded(level=0):
    if level == 0:
        return [""]
    res = []
    for i in range(len(all_gates)):
        n_1 = gen_all_encoded(level-1)
        res += [hex(i)[-1] + ni for ni in n_1]
    return res

# Create bluequat circuit from gates
def ref_from_gates(gs):
    c = Circuit(3)
    for [n, idx] in gs:
        c.__getattr__(gate_map[n]).__getitem__(tuple(idx))
    return c

# From hex number, find corresponding gates
def decode_gate(ss):
    res = []
    for c in ss:
        (n, idx) = all_gates[int(c, 16)]
        idx = [idx] if isinstance(idx, int) else list(idx)
        res.append([gate_map_inv[n], json.loads(str(idx))])
    return res

# Fill unit map for circuit up to 4 gates (included)
for i in range(5):
    enc4 = gen_all_encoded(i)
    for e in tqdm(enc4):
        circ = ref_from_gates(decode_gate(e))
        u = circ.to_unitary()
        idc = ''.join([str(i) for i in u]) # Flat the unit matrice
        if not (idc in unit_matrices):
            unit_matrices[idc] = e

with open("unit_mat2.json", "w") as f:
    f.write(json.dumps(unit_matrices))