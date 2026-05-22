import threading
import time
from datetime import datetime
from typing import Optional, Any, Dict, List, Tuple
from sqlalchemy.orm import Session
from app.models.activity import ActivityLog

class ActivityLoggerService:
    _buffer: List[Dict[str, Any]] = []
    _buffer_lock = threading.Lock()
    _last_flush = time.time()

    @staticmethod
    def log_event(
        db: Session,
        user_id: str,
        event_type: str,
        resource_type: Optional[str] = None,
        resource_id: Optional[str] = None,
        status: str = "success",
        metadata: Optional[Dict[str, Any]] = None,
        ip_address: Optional[str] = None,
        device_info: Optional[str] = None
    ):
        """Buffers a new activity log entry."""
        log_data = {
            "user_id": user_id,
            "event_type": event_type,
            "resource_type": resource_type,
            "resource_id": resource_id,
            "status": status,
            "metadata_json": metadata,
            "ip_address": ip_address,
            "device_info": device_info,
            "created_at": datetime.utcnow()
        }
        
        with ActivityLoggerService._buffer_lock:
            ActivityLoggerService._buffer.append(log_data)
            
        # Optional: check if buffer is too large and flush
        if len(ActivityLoggerService._buffer) >= 50:
             # We could trigger flush here, but better to let the background task handle it
             pass
        
        return log_data

    @classmethod
    def flush_logs(cls, db: Session):
        """Flushes buffered logs to the database."""
        with cls._buffer_lock:
            if not cls._buffer:
                return
            logs_to_flush = cls._buffer[:]
            cls._buffer.clear()
            cls._last_flush = time.time()

        try:
            for log_data in logs_to_flush:
                log = ActivityLog(**log_data)
                db.add(log)
            db.commit()
            # Clear cache when new logs are added
            ActivityHistoryService.clear_cache()
        except Exception as e:
            print(f"Error flushing logs: {e}")
            # Re-add to buffer if failed? (Better to log and move on or handle more robustly)

class ActivityHistoryService:
    _cache: Dict[str, Tuple[float, Any]] = {}  # key -> (expiry, data)
    _cache_ttl = 30  # 30 seconds cache
    _cache_lock = threading.Lock()

    @staticmethod
    def get_user_logs(db: Session, user_id: str, limit: int = 50, skip: int = 0):
        """Retrieves and sorts logs with caching."""
        cache_key = f"{user_id}_{limit}_{skip}"
        
        with ActivityHistoryService._cache_lock:
            if cache_key in ActivityHistoryService._cache:
                expiry, data = ActivityHistoryService._cache[cache_key]
                if time.time() < expiry:
                    return data

        # DB Query
        query = db.query(ActivityLog).filter(ActivityLog.user_id == user_id)
        total = query.count()
        items = query.order_by(ActivityLog.created_at.desc())\
            .offset(skip)\
            .limit(limit)\
            .all()
            
        result = (items, total)
        
        with ActivityHistoryService._cache_lock:
            ActivityHistoryService._cache[cache_key] = (time.time() + ActivityHistoryService._cache_ttl, result)
            
        return result

    @classmethod
    def clear_cache(cls):
        with cls._cache_lock:
            cls._cache.clear()
