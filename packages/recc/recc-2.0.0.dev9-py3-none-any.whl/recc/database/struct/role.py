# -*- coding: utf-8 -*-

from typing import Optional, Any
from datetime import datetime
from dataclasses import dataclass


@dataclass
class Role:
    uid: Optional[int] = None
    slug: Optional[str] = None

    name: Optional[str] = None
    description: Optional[str] = None
    extra: Optional[Any] = None

    hidden: Optional[bool] = None
    lock: Optional[bool] = None

    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
