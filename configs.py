LANGUAGES = {
    'ru': 'Russian 🇷🇺',
    'uz': 'Uzbek 🇺🇿',
    'es': 'Spanish 🇪🇸',
    'de': 'German 🇩🇪',
    'zh-cn': 'Chinese 🇨🇳',
    'cs': 'Czech 🇨🇿',
    'en': 'English 🇬🇧',
    'sv': 'Swedish 🇸🇪',
    'ko': 'Korean 🇰🇷',
    'ja': 'Japanese 🇯🇵'
}


def get_key(value):
    for k, v in LANGUAGES.items():
        if v == value:
            return k
