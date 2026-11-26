from collections import Counter


def summarize(rows):
    topics, brands, sentiments, aspects = Counter(), Counter(), Counter(), Counter()
    counts = Counter()
    evidence = []
    updated = None
    for row in rows:
        event, analysis = row["event"], row["analysis"]
        kind = event["event_type"]
        counts[kind] += 1
        if not analysis:
            if kind != "engagement":
                counts["pending"] += 1
            continue
        counts["analyzed"] += 1
        if kind == "comment":
            counts["analyzed_comments"] += 1
            if analysis["opinions"]:
                counts["comments_with_opinion"] += 1
        topics.update(analysis["topics"])
        # Count each brand once per source record, regardless of repeated mentions.
        brands.update({span["text"].casefold() for span in analysis["brands"]})
        for opinion in analysis["opinions"]:
            sentiments[opinion["sentiment"]] += 1
            aspects[f"{opinion['entity_type']}:{opinion['aspect']}:{opinion['sentiment']}"] += 1
            evidence.append(
                {
                    "source_id": event["source_id"],
                    "event_id": event["event_id"],
                    "event_time": event["event_time"],
                    "source": event["source"],
                    "url": event["payload"].get("url", ""),
                    "source_text": event["payload"].get("text", ""),
                    **opinion,
                }
            )
        processed = row.get("available_at")
        if processed and (updated is None or processed > updated):
            updated = processed
    return {
        "counts": {
            key: counts[key]
            for key in (
                "content",
                "comment",
                "engagement",
                "pending",
                "analyzed",
                "analyzed_comments",
                "comments_with_opinion",
            )
        },
        "topics": dict(topics),
        "brands": dict(brands),
        "sentiment_tuples": dict(sentiments),
        "aspect_sentiments": dict(aspects),
        "evidence": evidence,
        "updated_at": updated,
        "sentiment_denominator": "opinion tuples, not comments",
    }
