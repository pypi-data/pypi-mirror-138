from askdata.smart_synonym import suggest_synonyms

if __name__ == "__main__":

    word = "home"
    lang = "en"
    already_added = []

    synonyms, business_name = suggest_synonyms(word=word, lang=lang, already_added=already_added)

    print("Synonyms: ")
    print(synonyms)
    print()
    print("Business name:")
    print(business_name)
