query_lower = query.lower()
    genre_vector = np.zeros(len(genre_mapping))  # One-hot vector
    
    for idx, genre in enumerate(GENRE_NAMES.keys()):
        if genre in query_lower:
            genre_vector[idx] = 1 

    query_genre = genre_vector