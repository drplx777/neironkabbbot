import etcd3
import os
import logging
import threading
#писи попы
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EtcdConfigLoader:
    def __init__(self):
        self.client = etcd3.client(
            host=os.getenv('ETCD_HOST', '192.168.0.157'),
            port=int(os.getenv('ETCD_PORT', '2379')))
        self._cache = {}
        self.lock = threading.Lock()
        self._initialized = False
        
    def initialize(self):
        required_keys = [
            '/neiro/ENV_DATABASE',
            '/neiro/ENV_BOT_TOKEN',
            '/neiro/ENV_AI_TOKEN',
            '/neiro/ENV_PROXY'
        ]
        
        for key in required_keys:
            try:
                self.get(key)
            except Exception as e:
                logger.critical(f"Failed to load required key {key}: {str(e)}")
                raise
                
        self._initialized = True
    
    def get(self, key: str) -> str:
        """Безопасное получение значения с кэшированием"""
        with self.lock:
            if key in self._cache:
                return self._cache[key]
            
            try:
                value, _ = self.client.get(key)
                if value is None:
                    raise ValueError(f"Key {key} not found in etcd")
                    
                decoded_value = value.decode('utf-8')
                self._cache[key] = decoded_value
                return decoded_value
            except Exception as e:
                logger.error(f"Etcd error for key {key}: {str(e)}")
                raise
    
    def watch_changes(self):
        """Фоновое отслеживание изменений в etcd"""
        try:
            events_iterator, cancel = self.client.watch_prefix("/config/")
            logger.info("Started etcd config watcher")
            
            for event in events_iterator:
                if isinstance(event, etcd3.events.PutEvent):
                    key = event.key.decode('utf-8')
                    value = event.value.decode('utf-8')
                    with self.lock:
                        self._cache[key] = value
                    logger.info(f"Config updated: {key}")
                    
                elif isinstance(event, etcd3.events.DeleteEvent):
                    key = event.key.decode('utf-8')
                    with self.lock:
                        if key in self._cache:
                            del self._cache[key]
                    logger.warning(f"Config deleted: {key}")
                    
        except Exception as e:
            logger.error(f"Etcd watcher failed: {str(e)}")

# Глобальный инстанс
config_loader = EtcdConfigLoader()