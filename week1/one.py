favorite_languages = {
    'jen': ['python', 'ruby'],
    'sarah': 'c#',
    'awais': 'c',
    'edward': ['ruby', 'go'],
    'phil': ['python', 'haskell'],
}

for name, languages in favorite_languages.items():
    if isinstance(languages, str):
    # if len(languages) == 1:
        print(f'{name} favorite language is: ')
    else:    
        print(f'{name} favorite languages are: ')
    for index, language in enumerate(languages):
        print(f'{index}  {language}')