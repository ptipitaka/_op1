from tipitaka.models import CommonReference, WordList
from padanukkama.models import Padanukkama, Pada

def post(padanukkama_id):
    padanukkama = Padanukkama.objects.get(pk=padanukkama_id)
    # Retrieve the structures related to the padanukkama
    structures = padanukkama.structure.all()
    # Retrieve all the related CommonReference instances for the structures
    common_references = CommonReference.objects.filter(structure__in=structures)

    for common_reference in common_references:
        from_position = common_reference.from_position
        to_position = common_reference.to_position
        wordlist_version = common_reference.wordlist_version
        
        # Retrieve the WordList instances within the specified range and wordlist version
        wordlists = WordList.objects.filter(
            wordlist_version=wordlist_version,
            code__gte=from_position,
            code__lte=to_position
        ).distinct('word') # TODO : have to be chaange to pada_roman_script
        
        # Add the retrieved WordList instances to the Pada model
        for wordlist in wordlists:
            is_pada_exists = Pada.objects.filter(
                padanukkama=padanukkama,
                pada=wordlist.word # TODO : have to be chaange to pada_roman_script
            ).exists()

            if not is_pada_exists:
                Pada.objects.create(
                    padanukkama=padanukkama,
                    pada=wordlist.word,
                    pada_seq=wordlist.word_seq,
                    pada_roman_script=wordlist.word_roman_script,
                )
                print(wordlist)
