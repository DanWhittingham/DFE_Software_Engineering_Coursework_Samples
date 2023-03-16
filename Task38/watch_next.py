'''
Read in the movies.txt file. Each separate line is a description of a different movie.

Create a function to return which movies a user would watch next if they have watched Planet Hulk.
Planet Hulk: “Will he save their world or destroy it? When the Hulk becomes too dangerous for the
Earth, the Illuminati trick Hulk into a shuttle and launch him into space to a planet where the
Hulk can live in peace. Unfortunately, Hulk land on the planet Sakaar where he is sold into slavery
and trained as a gladiator.”

The function should take in the description as a parameter and return the title of the most similar movie.
'''

#==== Imports
import spacy

#==== load language module
nlp = spacy.load('en_core_web_md')


#==== Function definitions
def load_movies_descriptions(source_file: str):
    '''Obtains the movies from the source file'''
    movies_dict = {}
    with open(source_file, "r") as movie_details:
        for line in movie_details:
            details = line.strip().split(" :")
            if len(details[0]) > 0:
                try:
                    movies_dict[details[0]] = details[1]
                except IndexError:
                    print("\nWarning: unexpected formatting of movie-description.")
            else:
                print("\nWarning: unnamed movie found")
    return movies_dict


def pick_next_film(latest_film_description: str):
    '''Given a string (description of last film watched), makes a recommendation for next watch.'''

    # Load and store the movies with descriptions
    movies_descriptions = load_movies_descriptions("movies.txt")

    # Run the string through nlp
    latest_watch_description_nlp = nlp(latest_film_description)

    best_rating = 0         # Set a starting similarity of 0
    recommendation = ""     # Empty recommendation

    # Compare the master description to each candidate
    for key in movies_descriptions:

        # Obtain the similarity
        similarity = nlp(movies_descriptions[key]).similarity(latest_watch_description_nlp)

        if similarity > best_rating:
            # New best match
            recommendation = key
            best_rating = similarity

        elif best_rating > 0 and similarity == best_rating:
            # Unlikely case for if we find a tie
            recommendation = recommendation + " or " + key


    if recommendation == "":
        # Only happens if all similarities were non-zero; most likely indicates a fault.
        print("None of the candidates are remotely similar. Sorry!")
    else:
        # Display the recommendations
        print(f"Your next watch should be {recommendation}.")


#==== Execute
pick_next_film('''
Will he save their world or destroy it? When the Hulk becomes too dangerous for the
Earth, the Illuminati trick Hulk into a shuttle and launch him into space to a planet where the
Hulk can live in peace. Unfortunately, Hulk land on the planet Sakaar where he is sold into slavery
and trained as a gladiator.
''')
