# core/config.py
import etcd3
import os

client = etcd3.client(
    host=os.getenv('ETCD_HOST', '192.168.0.157'),
    port=int(os.getenv('ETCD_PORT', '2379'))
)

def get(key: str) -> str:
    value, _ = client.get(key)
    if value is None:
        raise KeyError(f"Key {key} not found in etcd")
    return value.decode('utf-8')
