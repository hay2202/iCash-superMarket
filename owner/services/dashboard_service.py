from sqlalchemy.orm import Session
from sqlalchemy import text
from collections import Counter
import logging

logger = logging.getLogger(__name__)

class PurchaseService:

    @classmethod
    def unique_buyers(cls, db: Session):
        logger.info("Calculating unique buyers")
        # count distinct user_id in purchases
        q = db.execute(text("SELECT COUNT(DISTINCT user_id) FROM purchases"))
        count = q.scalar()
        logger.info(f"Unique buyers count: {count}")
        return count

    @classmethod
    def loyal_buyers(cls, db: Session, min_purchases: int = 3):
        logger.info(f"Fetching loyal buyers with min_purchases={min_purchases}")
        q = db.execute(
            text("SELECT user_id, COUNT(*) as cnt FROM purchases GROUP BY user_id HAVING COUNT(*) >= :min ORDER BY cnt DESC"),
            {"min": min_purchases}
        )
        rows = [ {"user_id": r[0], "purchases": r[1]} for r in q.fetchall() ]
        logger.info(f"Found {len(rows)} loyal buyers")
        return rows

    @classmethod
    def top_products(cls, db: Session, top_n: int = 3):
        logger.info(f"Calculating top products with top_n={top_n}")
        # fetch items_list and count occurrences
        res = db.execute(text("SELECT items_list FROM purchases"))
        counts = Counter()
        for r in res:
            items = r[0].split(",") if r[0] else []
            for it in items:
                item = it.strip()
                logger.debug(f"Counting product occurrence: {item}")
                if item:
                    counts[item] += 1
        if not counts:
            return []

        # get threshold based on top_n (include ties)
        most_common = counts.most_common()
        threshold = most_common[ min(top_n-1, len(most_common)-1) ][1]
        result = [ {"product": k, "count": v} for k,v in most_common if v >= threshold ]
        logger.info(f"Top products calculated: {result}")
        return result
