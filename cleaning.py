df['no_reviews'] = df['no_reviews'].str.replace(',', '')
df['no_reviews'] = df['no_reviews'].astype(int)
# change ratings to int
df['no_ratings'] = df['no_ratings'].str.replace(',', '')
df['no_ratings'] = df['no_ratings'].astype(int)
# change image to none if it's a placeholder
df.loc[df['img'] == "https://cdn.beeradvocate.com/im/placeholder-beer.jpg", 'img'] = None
# change ABV to float
df['abv'] = df['abv'].str.replace('%', '')
df['abv'] = df['abv'].astype(float)


def get_avg_taste(string):
	"""takes in the review and pulls out the rating for the taste and returns an average"""
    list_list = [re.findall("\d{1}\.*\d*", item) for item in re.findall("taste: \d{1}\.*\d*", string)]
    sum_feel = 0
    tot = len(list_list)
    for list_item in list_list:
        for item in list_item:
            sum_feel += float(item)
    if not tot == 0:
        return sum_feel/tot
    else:
        return None


def get_avg_look(string):
    list_list = [re.findall("\d{1}\.*\d*", item) for item in re.findall("look: \d{1}\.*\d*", string)]
    sum_feel = 0
    tot = len(list_list)
    for list_item in list_list:
        for item in list_item:
            sum_feel += float(item)
    if not tot == 0:
        return sum_feel/tot
    else:
        return None

def get_avg_smell(string):
    list_list = [re.findall("\d{1}\.*\d*", item) for item in re.findall("smell: \d{1}\.*\d*", string)]
    sum_feel = 0
    tot = len(list_list)
    for list_item in list_list:
        for item in list_item:
            sum_feel += float(item)
    if not tot == 0:
        return sum_feel/tot
    else:
        return None


def get_avg_feel(string):
    list_list = [re.findall("\d{1}\.*\d*", item) for item in re.findall("smell: \d{1}\.*\d*", string)]
    sum_feel = 0
    tot = len(list_list)
    for list_item in list_list:
        for item in list_item:
            sum_feel += float(item)
    if not tot == 0:
        return sum_feel/tot
    else:
        return None



 df['taste_avg'] = df['review'].apply(get_avg_taste)
 df['look_avg'] = df['review'].apply(get_avg_look)
 df['smell_avg'] = df['review'].apply(get_avg_smell)
 df['feel_avg'] = df['review'].apply(get_avg_feel)

 # I might need to drop short reviews - do this on the cleaned reviews.
 def drop_short_reviews(review):
    if len(review) < 5:
        return None
    else:
        return review

def clean_review(review):
    """takes in a review and does the following:
    1. removes the '\xa0'
    2. removes the '\n'
    3. performs the simple preprocess from gensim"""
    review = review.replace(u'\\xa0', '')
    review = review.replace('\\n', '')
    review = gensim.utils.simple_preprocess(str(review), deacc=True)
    review = [word for word in review if word not in stop_words]
    meta_lemmed = [lemmatizer.lemmatize(word) for word in review]
#     c = " ".join(str(x) for x in meta_lemmed)
#     cleaned.append(c)
    return meta_lemmed
