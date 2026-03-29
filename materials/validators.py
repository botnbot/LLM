from urllib.parse import urlparse

from rest_framework.serializers import ValidationError

ALLOWED_DOMAINS = {"youtube.com", "youtu.be"}


class YouTubeLinkValidator:
    def __init__(self, field: str):
        self.field = field

    def __call__(self, attrs):
        value = attrs.get(self.field)
        if not value:
            return

        parsed = urlparse(value)

        if parsed.scheme not in ("http", "https"):
            raise ValidationError({self.field: "Ссылка должна начинаться с http:// или https://"})

        domain_parts = parsed.netloc.lower().split('.')
        if len(domain_parts) < 2:
            raise ValidationError({self.field: "Некорректный домен ссылки"})

        domain = ".".join(domain_parts[-2:])
        if domain not in ALLOWED_DOMAINS:
            raise ValidationError({self.field: "Разрешены только ссылки на YouTube"})