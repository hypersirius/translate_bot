LANGUAGES = {
    'ru': 'Russian π·πΊ',
    'uz': 'Uzbek πΊπΏ',
    'es': 'Spanish πͺπΈ',
    'de': 'German π©πͺ',
    'zh-cn': 'Chinese π¨π³',
    'cs': 'Czech π¨πΏ',
    'en': 'English π¬π§',
    'sv': 'Swedish πΈπͺ',
    'ko': 'Korean π°π·',
    'ja': 'Japanese π―π΅'
}


def get_key(value):
    for k, v in LANGUAGES.items():
        if v == value:
            return k
