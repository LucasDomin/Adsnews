def safe_get(data, path, default=None):

    try:

        for key in path:
            data = data[key]

        return data

    except:
        return default


def normalize_ad(ad):

    snapshot = ad.get("snapshot", {})

    images = snapshot.get("images", [])
    videos = snapshot.get("videos", [])
    cards = snapshot.get("cards", [])

    image_url = None
    video_preview = None

    media_type = "unknown"

    headline = (
        safe_get(snapshot, ["title"])
        or safe_get(snapshot, ["body", "text"])
        or ""
    )

    body = (
        safe_get(snapshot, ["body", "text"])
        or ""
    )

    cta = snapshot.get("cta_text")

    cta_link = snapshot.get("link_url")

    # =========================
    # IMAGE ADS
    # =========================

    if images:

        media_type = "image"

        image_url = (
            images[0].get("original_image_url")
            or images[0].get("resized_image_url")
        )

    # =========================
    # VIDEO ADS
    # =========================

    elif videos:

        media_type = "video"

        video_preview = videos[0].get(
            "video_preview_image_url"
        )

    # =========================
    # CAROUSEL / DYNAMIC ADS
    # =========================

    elif cards:

        media_type = "carousel"

        first_card = cards[0]

        # headline real
        headline = (
            first_card.get("title")
            or headline
        )

        # body real
        body = (
            first_card.get("body")
            or body
        )

        # CTA real
        cta = (
            first_card.get("cta_text")
            or cta
        )

        # LINK real
        cta_link = (
            first_card.get("link_url")
            or cta_link
        )

        # imagem real
        card_images = first_card.get(
            "images",
            []
        )

        if card_images:

            image_url = (
                card_images[0].get(
                    "original_image_url"
                )
                or card_images[0].get(
                    "resized_image_url"
                )
            )

    # =========================
    # DYNAMIC TEMPLATE DETECTION
    # =========================

    if "{{" in str(headline):

        media_type = "dynamic_template"

    normalized = {

        "ad_id": ad.get("ad_archive_id"),

        "page_name": snapshot.get("page_name"),

        "headline": headline,

        "body": body,

        "cta": cta,

        "cta_link": cta_link,

        "media_type": media_type,

        "image_url": image_url,

        "video_preview": video_preview,

        "start_date": ad.get("start_date"),

        "end_date": ad.get("end_date"),

        "publisher_platform": ad.get(
            "publisher_platform"
        ),

        "caption": snapshot.get("caption"),

        "page_profile_picture": snapshot.get(
            "page_profile_picture_url"
        ),

        "cards_count": len(cards),

        "has_cards": len(cards) > 0,

        "raw": ad
    }

    return normalized