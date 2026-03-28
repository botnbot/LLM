from urllib.parse import urlparse

from rest_framework.serializers import ValidationError


def validate_youtube_link(value):
    if not value:
        return

    parsed = urlparse(value)

    allowed_domains = ("youtube.com", "youtu.be")

    if not parsed.scheme.startswith("http"):
        raise ValidationError("Некорректный протокол ссылки")

    if not any(parsed.netloc.endswith(domain) for domain in allowed_domains):
        raise ValidationError("Разрешены только ссылки на YouTube")