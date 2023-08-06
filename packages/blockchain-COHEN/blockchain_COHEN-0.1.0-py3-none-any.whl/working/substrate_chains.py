from . import substrate

addr = []

# Substrate format information here
# https://github.com/paritytech/ss58-registry/blob/main/ss58-registry.json
chains = {
    ('polkadot', 'DOT', 1e10),
    ('kusama', 'KSM', 1e12),
    ('astar', 'PLM', 1e15),
    ('astar', 'ASTR', 1e15)
    ('karura', 'KAR', 1e12),
    ('kulupu', 'KLP', 1e12),
    ('acala', 'ACA', 1e18),
    ('bifrost', 'BNC', 1e12),
    ('edgeware', 'EDG', 1e18),
    ('integritee', 'TEER', 1e12),
    ('darwinia', 'RING', 1e9),
    ('darwinia', 'KTON', 1e9),
    ('stafi', 'FIS', 1e12),
    ('dock', 'DCK', 1e6),
    ('khala', 'PHA', 1e12),
    ('robonomics', 'XRT', 1e9),
    ('centrifuge', 'CFG', 1e18),
    ('chainx', 'PCX', 1e8),
    ('uniarts', 'UART', 1e12),
    ('uniarts', 'UINK', 1e12),
    ('crust', 'CRU', 1e12),
    ('equlibrium', 'EQ', 1e9),
    ('sora', 'XOR', 1e18),
    ('polkadex', 'PDEX', 1e12),
    ('parallel', 'HKO', 1e12),
    ('clover', 'CLV', 1e18),
    ('altair', 'AIR', 1e18),
    ('moonbeam', 'GLMR', 1e18),
    ('moonriver', 'MOVR', 1e18),
    ('kintsugi', 'KINT', 1e12),
    
}

for chain in chains:
    #substrate.Substrate(chain[0), chain[1], chain[2])
    substrate.Substrate(*(chain[0:]))

