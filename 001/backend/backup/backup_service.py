import asyncio
from datetime import datetime
import boto3
import json
from typing import List, Dict

class BackupService:
    def __init__(self, s3_client):
        self.s3_client = s3_client
        self.backup_queue = asyncio.Queue()
        
    async def schedule_backup(self, data: Dict, backup_type: str):
        """Programme un backup des données"""
        await self.backup_queue.put({
            'data': data,
            'type': backup_type,
            'timestamp': datetime.now().isoformat()
        })
        
    async def process_backup_queue(self):
        """Traite la file d'attente des backups"""
        while True:
            backup_item = await self.backup_queue.get()
            try:
                await self._perform_backup(backup_item)
            except Exception as e:
                logger.error(f"Erreur de backup: {str(e)}")
            finally:
                self.backup_queue.task_done()
                
    async def _perform_backup(self, backup_item: Dict):
        """Effectue le backup vers S3"""
        bucket_name = f"deepstudy-backups-{backup_item['type']}"
        key = f"{backup_item['timestamp']}.json"
        
        self.s3_client.put_object(
            Bucket=bucket_name,
            Key=key,
            Body=json.dumps(backup_item['data'])
        ) 