from pprint import pprint

from utils import *


class User:
    def __init__(self):
        from connection import collections

        self.name = collections["name.basics"]
        self.basics = collections["title.basics"]
        self.principals = collections["title.principals"]
        self.ratings = collections["title.ratings"]

    def add_movie(self, movie_id, title, start_year, runtime, genres_str):
        assertion_pairs = {
            movie_id.isdigit(): "Invalid movie id",
            title: "Title cannot be empty",
            is_valid_year(start_year): "Invalid year",
            is_valid_int(runtime): "Invalid runtime",
        }

        if validate_data(assertion_pairs):
            movie_id = f"tt{movie_id}"

            if self.is_movie_exists(movie_id):
                print(f"Movie {movie_id}: {title} exists\n")
                return

            genres = genres_str.split(" ")

            doc = {
                "tconst": movie_id,
                "titleType": "movie",
                "primaryTitle": title,
                "originalTitle": title,
                "isAdult": None,
                "startYear": int(start_year),
                "endYear": None,
                "runtimeMinutes": runtime,
                "genres": genres
            }

            self.basics.insert_one(doc)
            print(f"Movie {movie_id}: {title} has been added\n")

    def add_cast_crew(self, member_id, title_id, category):
        assertion_pairs = {
            member_id.isdigit(): "Invalid member id",
            title_id.isdigit(): "Invalid title id",
        }

        if validate_data(assertion_pairs):
            member_id = f"nm{member_id}"
            title_id = f"tt{title_id}"

            if not self.is_member_exists(member_id):
                print(f"Member {member_id} does not exists\n")
                return

            if not self.is_movie_exists(title_id):
                print(f"Title {title_id} does not exists\n")
                return

            ordering = self.get_ordering(title_id)

            doc = {
                "tconst": title_id,
                "ordering": ordering + 1,
                "nconst": member_id,
                "category": category,
                "job": None,
                "characters": None,
            }

            self.principals.insert_one(doc)
            print(f"Member {member_id} has been associated to title {title_id} "
                  f"with category: {category}\n")

    def get_ordering(self, title_id):
        selector = {"tconst": title_id}

        result = self.principals.find(selector)
        if result:
            result.sort("ordering", -1).limit(1)

            return result[0]["ordering"]

        return 0

    def is_member_exists(self, member_id):
        selector = {"nconst": member_id}

        return True if self.name.find_one(selector) else False

    def is_movie_exists(self, movie_id):
        selector = {"tconst": movie_id}

        return True if self.basics.find_one(selector) else False

    def search_for_member(self, name_input):
        actorID = self.name.aggregate([
            {'$unwind': '$primaryProfession'},
            {'$match': {'primaryName': {'$regex': '^' + name_input + '$', '$options': 'i'}}},
            {'$group': {'_id': '$nconst',
                        'primaryProfession': {'$addToSet': '$primaryProfession'},
                        'primaryName': {'$first': '$primaryName'}
                        }},
            {'$project': {'_id': '$_id', 'primaryProfession': '$primaryProfession', 'primaryName': '$primaryName'}}
        ])

        for r in actorID:
            print("\nHere is the Info for a cast that matches your description")
            new_result = self.principals.aggregate([
                {'$match': {'nconst': r['_id']}},
                {'$match': {'job': {'$ne': 'null'}}},
                {'$lookup': {
                    'from': 'title_basics',
                    'localField': 'tconst',
                    'foreignField': 'tconst',
                    'as': 'titles'
                }},
                {'$unwind': '$titles'},
                {'$project': {'Name': '$titles.primaryTitle', 'job': '$job', 'characters': '$characters'}}
            ])

            print("Name: ", r['primaryName'], '|', 'Profession(s): ', ','.join(r['primaryProfession']), '\n')

            print("Here are their Movies, their jobs and the characters they played")
            for i in new_result:
                if not i['characters']:
                    print(i['Name'], '|', i['job'], '|', "No Characters")
                else:
                    print(i['Name'], '|', i['job'], '|', ",".join(i['characters']))

            print()

    def search_for_genres(self, genres, minimum_vote):
        minimum_vote = int(minimum_vote)
        result = self.basics.aggregate([
            {'$unwind': '$genres'},
            {'$match': {'genres': {'$regex': '^' + genres + '$', '$options': 'i'}}},
            {'$group': {'_id': '$tconst'}},
            {'$project': {'tconst': '$_id', "_id": 0}}
        ]
        )

        result_list = []
        for r in result:
            result_list.append(r['tconst'])

        new_result = self.ratings.aggregate([
            {'$match': {'numVotes': {'$gte': minimum_vote}}},
            {'$match': {'tconst': {'$in': result_list}}},
            {'$sort': {'averageRating': -1}},
            {'$project': {'tconst': '$tconst', 'Average': '$averageRating', 'Votes': '$numVotes', "_id": 0}}
        ]
        )

        new_result_list = list(new_result)
        filtered_list = []
        for r in new_result_list:
            filtered_list.append(r['tconst'])

        last_result = list(self.basics.aggregate([
            {'$match': {'tconst': {'$in': filtered_list}}},
            {'$project': {'tconst': '$tconst', 'Title of Movie': '$primaryTitle', '_id': 0}}
        ]))
        for j in range(0, len(new_result_list)):
            for i in range(0, len(last_result)):
                if last_result[i]['tconst'] == new_result_list[j]['tconst']:
                    print(last_result[i]['Title of Movie'], '|', str(new_result_list[j]['Average']), '|',
                          str(new_result_list[j]['Votes']))
                    break

    def search_for_titles(self, keywords, years=None):
        strings = []
        years = [int(year) for year in years.split(";")] if years else []
        
        for keyword in keywords.split(";"):
            if keyword.isdigit() and is_valid_year(keyword):
                years.append(int(keyword))
            else:
                strings.append(keyword)

        regex = '"' + '" "'.join(strings) + '"'
        self.basics.create_index([('primaryTitle', 'text')])

        if len(strings) > 0 and len(years) > 0:
            result = self.basics.find(
                # maybe use all for the regex
                {'$and': [
                    {'$text': {'$search': regex}},
                    {'startYear': {'$in': years}}
                ]}
            )
        elif len(years) == 0:
            result = self.basics.find(
                {'$text': {'$search': regex}})
        elif len(strings) == 0:
            result = self.basics.find(
                {'startYear': {'$in': years}})

        all_movies = []
        for r in result:
            pprint(r)
            print("\n")
            all_movies.append(r['primaryTitle'].lower())

        if input("Would you like to choose a specific Movie? (yes/no): ").lower() == "yes":
            movie = ''
            while movie.lower() not in all_movies:
                movie = input("select a Valid Title to get more information on: ")

            tconsts = self.basics.aggregate([
                {'$match': {'primaryTitle': {'$regex': '^' + movie + '$', '$options': 'i'}}},
                {'$lookup': {
                    'from': 'title_ratings',
                    'localField': 'tconst',
                    'foreignField': 'tconst',
                    'as': 'ratings'
                }},
                {'$unwind': '$ratings'},
                {'$project': {'_id': 0, 'primaryTitle': '$primaryTitle', 'tconst': '$tconst',
                              'numVotes': '$ratings.numVotes', 'rating': '$ratings.averageRating'}}
            ])
            ratings = list(tconsts)[0]
            tconst = ratings['tconst']

            nconst = list(self.principals.find({'tconst': tconst}))
            nconst_list = list(nconst)
            for i in range(0, len(nconst_list)):
                nconst_list[i] = nconst_list[i]['nconst']

            for i in tconsts:
                print(i)

            print("\nHere is info about the Movie")
            print("Title: " + ratings['primaryTitle'] + ' | Number of Votes:  ' + str(
                ratings['numVotes']) + ' | Rating:  ' + str(ratings['rating']))

            names = list(self.name.find(
                {'nconst': {'$in': nconst_list}},
                {'nconst': '$nconst', 'primaryName': '$primaryName'}
            ))

            print("\nHere are the names of the Cast, their Category and the name of the Character they played\n")
            for cast in names:
                characters_str = ""
                for n_const in nconst:
                    if cast['nconst'] == n_const['nconst']:
                        if n_const['characters']:
                            length = len(n_const['characters'][0])
                            characters_str += n_const['characters'][0][0:length]
                        else:
                            characters_str = "None"
                        print(cast['primaryName'] + ' | ' + n_const['category'] + ' | ' + characters_str)
