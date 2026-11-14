import re


class TextNormalizer:
    def normalize(self, text: str) -> str:

        # Remove unwanted control characters.
        text = re.sub(
            r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]",
            "",
            text,
        )

        # Normalize line endings.
        text = text.replace("\r\n", "\n")
        text = text.replace("\r", "\n")

        # Normalize spaces and tabs.
        text = re.sub(r"[ \t]+", " ", text)

        # Reduce excessive blank lines.
        text = re.sub(r"\n{3,}", "\n\n", text)

        return text.strip()
