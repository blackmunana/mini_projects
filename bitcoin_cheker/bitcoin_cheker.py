import ecdsa
from ecdsa.util import randrange_from_seed__trytryagain
import requests
import json

while True:
    def generate_key():
        valid_key = False
        while not valid_key:
            private_key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)  
            public_key = private_key.verifying_key
            compressed = public_key.to_string()
            x_coor = compressed[:32]
            y_coor = compressed[32:]
            if(public_key.pubkey.point.x() == int.from_bytes(x_coor,byteorder="big")) and (public_key.pubkey.point.y() == int.from_bytes(y_coor,byteorder="big")):
                valid_key = True
        return private_key, public_key, x_coor, y_coor

    def balance_checker(address):

        url = f"https://blockchain.info/rawaddr/{address}"
        response = requests.get(url)
    
        if response.status_code == 200:
            if response.text:
                data = response.json()
                if 'final_balance' in data:
                    return data["final_balance"]
    
        return 0

    def main():
        private_key, public_key, x_coor, y_coor = generate_key()
        
        address = f'{x_coor.hex()}{y_coor.hex()}'
        balance = balance_checker(address)
        
        if balance > 0:
            with open("balances.txt", "a") as file:
                file.write(f"Адрес: {address}\nБаланс: {balance} BTC\n")
        
        print(f"Приватный ключ: {private_key.to_string().hex()}")
        print(f"Публичный адрес: {address}")
        print(f"Баланс: {balance} BTC")
        
    if __name__ == "__main__":
        main()