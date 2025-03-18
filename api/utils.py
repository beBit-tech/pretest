# api/utils.py

import json
import datetime

from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist

from .models import OrderNumberSequence

def parse_json_request(request):
    """
    解析 Request 的 JSON，失敗則回傳 None。
    """
    try:
        return json.loads(request.body)
    except json.JSONDecodeError:
        return None


def generate_order_number() -> str:
    """
    產生業務訂單編號：ORD{YYYYMMDD}{5位累計數}。
    例如：ORD2025031700001
    
    搭配 OrderNumberSequence model，紀錄每日自動累加。
    """
    today_str = datetime.datetime.now().strftime("%Y%m%d")

    with transaction.atomic():
        try:
            seq_record = OrderNumberSequence.objects.get(date=today_str)
            seq_record.sequence += 1
            seq_record.save()
        except ObjectDoesNotExist:
            seq_record = OrderNumberSequence.objects.create(
                date=today_str,
                sequence=1
            )

    sequence_str = f"{seq_record.sequence:05d}"  # 5位數，不足補 0
    return f"ORD{today_str}{sequence_str}"
