import time
from web3 import Web3

# Konfigurasi URL RPC dan detail transaksi
RPC_URL = 'https://hybrid-testnet.rpc.caldera.xyz/http'
PRIVATE_KEY = '26bb674281e0a202edea424c7da4ecedbe25d8bf7ceb5ece6c016f7eb021b6bb'
RECIPIENT_ADDRESS = '0xb9dbb5d661a8258b4C8CF70bA47c16290A573d80'
METHOD_SIGNATURE = '0x1249c58b'

# Inisialisasi Web3
web3 = Web3(Web3.HTTPProvider(RPC_URL))

# Mengecek koneksi
if not web3.is_connected():
    print("Gagal terhubung ke jaringan Ethereum.")
    exit()

# Mendapatkan alamat dari private key
account = web3.eth.account.from_key(PRIVATE_KEY)
address = account.address
print(f'Connected to address: {address}')

# Pastikan alamat penerima dalam format checksum
try:
    RECIPIENT_ADDRESS = web3.to_checksum_address(RECIPIENT_ADDRESS)
except Exception as e:
    print(f"Kesalahan saat mengonversi alamat penerima: {e}")
    exit()

while True:
    try:
        # Mengambil saldo
        balance = web3.eth.get_balance(address)
        print(f'Saldo: {web3.from_wei(balance, "ether")} ETH')

        # Mendapatkan estimasi gas untuk transaksi
        gas_estimate = web3.eth.estimate_gas({
            'from': address,
            'to': RECIPIENT_ADDRESS,
            'data': METHOD_SIGNATURE
        })

        # Membuat transaksi
        transaction = {
            'from': address,
            'to': RECIPIENT_ADDRESS,
            'value': web3.to_wei(0, 'ether'),
            'gas': gas_estimate,
            'gasPrice': web3.eth.gas_price,
            'nonce': web3.eth.get_transaction_count(address),
            'chainId': 1225,
            'data': METHOD_SIGNATURE
        }

        # Menandatangani transaksi
        signed_txn = web3.eth.account.sign_transaction(transaction, PRIVATE_KEY)

        # Mengirim transaksi
        txn_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)
        txn_hash_hex = web3.to_hex(txn_hash)
        print(f'Transaksi dikirim dengan hash: {txn_hash_hex}')

        # Memeriksa status transaksi
        txn_receipt = web3.eth.wait_for_transaction_receipt(txn_hash)

        # Menampilkan informasi transaksi
        print(f'Transaksi berhasil dengan status: {txn_receipt.status}')
        print(f'Gas digunakan: {txn_receipt.gasUsed}')

        # Menampilkan data sesuai format JSON
        json_data = {
            "callType": "call",
            "from": address,
            "gas": hex(gas_estimate),
            "input": METHOD_SIGNATURE,
            "to": RECIPIENT_ADDRESS,
            "value": "0x0",
            "result": {
                "gasUsed": hex(txn_receipt.gasUsed),
                "output": txn_receipt.logs[0].data if txn_receipt.logs else "0x"
            },
            "subtraces": 0,
            "traceAddress": [],
            "type": "call"
        }
        print(f'Data format JSON: {json_data}')

        # Tunggu sebelum mengulangi transaksi
        time.sleep(5)

    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
        # Mengabaikan kesalahan dan melanjutkan ke iterasi berikutnya
        continue