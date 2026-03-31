import os
import hashlib
import json
import base64
from typing import Any, Dict, List
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from datetime import datetime

# AES-256 Vaulting
class MedVault:
    def __init__(self, key: bytes = None):
        # Generate a 256-bit (32 byte) key if not provided
        self.key = key if key else AESGCM.generate_key(bit_length=256)
        self.aesgcm = AESGCM(self.key)

    def encrypt_data(self, data: Dict[str, Any]) -> str:
        """Encrypt JSON-serializable data using AES-256-GCM."""
        nonce = os.urandom(12)  # Recommended 96-bit nonce for GCM
        json_data = json.dumps(data).encode('utf-8')
        ciphertext = self.aesgcm.encrypt(nonce, json_data, None)
        # Store as base64 to be easily transportable: nonce + ciphertext
        return base64.b64encode(nonce + ciphertext).decode('utf-8')

    def decrypt_data(self, encrypted_string: str) -> Dict[str, Any]:
        """Decrypt AES-256-GCM payload and return dictionary."""
        try:
            raw_data = base64.b64decode(encrypted_string.encode('utf-8'))
            nonce = raw_data[:12]
            ciphertext = raw_data[12:]
            decrypted_data = self.aesgcm.decrypt(nonce, ciphertext, None)
            return json.loads(decrypted_data.decode('utf-8'))
        except Exception as e:
            return {"error": f"Decryption failed: {str(e)}"}

    def get_key_base64(self) -> str:
        """Export key safely."""
        return base64.b64encode(self.key).decode('utf-8')

# SHA-256 Hash Chain Ledger
class LedgerBlock:
    def __init__(self, index: int, timestamp: str, action: str, details: str, previous_hash: str):
        self.index = index
        self.timestamp = timestamp
        self.action = action
        self.details = details
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self) -> str:
        data_string = f"{self.index}{self.timestamp}{self.action}{self.details}{self.previous_hash}"
        return hashlib.sha256(data_string.encode('utf-8')).hexdigest()

    def to_dict(self):
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "action": self.action,
            "details": self.details,
            "previous_hash": self.previous_hash,
            "hash": self.hash
        }

class LedgerChain:
    def __init__(self):
        self.chain: List[LedgerBlock] = []
        self._create_genesis_block()

    def _create_genesis_block(self):
        genesis = LedgerBlock(0, datetime.now().isoformat(), "System Init", "MedVault initialized", "0")
        self.chain.append(genesis)

    def add_record(self, action: str, details: str) -> LedgerBlock:
        last_block = self.chain[-1]
        new_block = LedgerBlock(
            index=last_block.index + 1,
            timestamp=datetime.now().isoformat(),
            action=action,
            details=details,
            previous_hash=last_block.hash
        )
        self.chain.append(new_block)
        return new_block

    def verify_chain(self) -> bool:
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            if current_block.hash != current_block.calculate_hash():
                return False
            if current_block.previous_hash != previous_block.hash:
                return False
        return True

    def get_chain_data(self) -> List[Dict]:
        return [block.to_dict() for block in self.chain]
