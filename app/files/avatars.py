from hashlib import sha1


def generate_avatar(metadata: str, title: str) -> bytes:
    metadata_hash = sha1(metadata.encode()).hexdigest()
    font_color = f"#{metadata_hash[:6]}"
    background = f"{font_color}55"
    svg = f"""
    <?xml version="1.0" encoding="utf-8"?>
    <!-- License: CC Attribution. Made by Umar Irshad: https://dribbble.com/Umar -->
    <svg fill="#ffffff" width="100px" height="100px" xmlns="http://www.w3.org/2000/svg">
        <rect width="100px" height="100px" fill="{background}"></rect>
        <text fill="{font_color}" x="50%" y="50%" dominant-baseline="middle" text-anchor="middle">{title}</text>
    </svg>
    """
    return svg.encode()


def avatar_generator(metadata: str, title: str):
    avatar = generate_avatar(metadata, title)
    yield avatar
