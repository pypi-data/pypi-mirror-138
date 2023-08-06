from . import covelenth

addr = []

chains = {
    ('ronin', 2020, 'explorer.ronin.com', 'RONIN'),
    ('polygon', 137, 'polygonscan.com', 'MATIC'),
    ('BSC', 56, 'bscscan.com', 'BNB'),
    ('fantom', 250, 'ftmscan.com', 'FTM'),
    ('moonbeam', 1284, 'blockscout.moonbeam.network', 'GLMR'),
    ('monriver', 1285, 'blockscout.moonriver.moonbeam.network', 'MOVR'),
    ('rsk', 30, 'explorer.rsk.co', 'RSK'),
    ('arbitrum', 42161, 'explorer.offchainlabs.com', 'ARB'),
    ('palm', 11297108109, 'explorer.palm.io', 'Palm'),
    ('klayton', 8217, 'scope.klaytn.com', 'KLAY'),
    ('heco', 128, 'hecoinfo.com', 'HECO'),
    ('iotex', 4689, 'iotexscan.io', 'IOTX'),
    ('evmos', 900, 'explorer.evmos.org', 'PHOTON')
}

for chain in chains:
    #covelenth.Covelenth(chain[1], chain[2], chain[3])
    covelenth.Covelenth(*(chain[1:]))

# ronin = covelenth.Covelenth(2020, 'explorer.ronin.com', 'RONIN')
# tx = ronin.get_transactions(addr)

# polygon = covelenth.Covelenth(137, 'polygonscan.com', 'MATIC')
# tx = polygon.get_transactions(addr)

# binance = covelenth.Covelenth(97, 'bscscan.com', 'BSC')
# tx = binance.get_transactions(addr)

# fantom = covelenth.Covelenth(250, 'bscscan.com', 'FTM')
# tx = fantom.get_transactions(addr)

# moonbeam = covelenth.Covelenth(1284, 'blockscout.moonbeam.network', 'MOBM')
# tx = moonbeam.get_transactions(addr)

# moonriver = covelenth.Covelenth(1285, 'blockscout.moonriver.moonbeam.network', 'MOVR')
# tx = moonriver.get_transactions(addr)

# rsk = covelenth.Covelenth(30, 'explorer.rsk.co', 'RSK')
# tx = rsk.get_transactions(addr)

# arbitrum = covelenth.Covelenth(42161, 'explorer.offchainlabs.com', 'ARB')
# tx = arbitrum.get_transactions(addr)

# palm = covelenth.Covelenth(11297108109, 'explorer.palm.io', 'Palm')
# tx = palm.get_transactions(addr)

# klayton = covelenth.Covelenth(8217, 'scope.klaytn.com', 'KLAY')
# tx = klayton.get_transactions(addr)

# heco = covelenth.Covelenth(128, 'hecoinfo.com', 'HECO')
# tx = heco.get_transactions(addr)

# iotex = covelenth.Covelenth(4689, 'iotexscan.io', 'IOTX')
# tx = iotex.get_transactions(addr)

# evmos = covelenth.Covelenth(900, 'explorer.evmos.org', 'PHOTON')
# tx = evmos.get_transactions(addr)
















