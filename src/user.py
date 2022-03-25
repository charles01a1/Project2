from lib2to3.pgen2.token import MINUS
from tkinter import N
from connection import collections
from pprint import pprint


class User():
    def __init__(self):
        self.name = collections["name.basics"]
        self.basics = collections["title.basics"]
        self.principals = collections["title.principals"]
        self.ratings = collections["title.ratings"]

    def search_for_titles(self, keywords):
        strings = []
        years = []
        for i in range(0, len(keywords)):
            if keywords[i].isdigit():
                years.append(int(keywords[i]))
            else:
                strings.append(keywords[i])

        regex = '|'.join(strings)
        self.basics.create_index([('primaryTitle', 'text')])

        if (len(strings) > 0 and len(years) > 0):
            result = self.basics.find(
                {'$and': [
                    {'$text': {'$search': regex}},
                    {'startYear': {'$in': years}}
                ]}
                #  {'$or':[{'$text':{'$search':regex}},{'startYear':{'$in':years}}]}
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

        movie = ''
        while movie.lower() not in all_movies:
            movie = input("select a Valid Title to get more information on: ")

        tconst = self.basics.find({'primaryTitle':{'$regex':movie,'$options':'i'}})
        tconst = list(tconst)[0]['tconst']

        movie_rating = self.ratings.find(
            {'tconst': tconst},
            {'_id': movie, 'Ratings': '$averageRating', 'Number of Votes': '$numVotes'}
        )

        nconst = self.principals.find({'tconst': tconst})
        nconst_list = list(nconst)
        for i in range(0, len(nconst_list)):
            nconst_list[i] = nconst_list[i]['nconst']

        casts = self.name.find({'nconst': {'$in': nconst_list}})
        casts_list = list(casts)
        for i in range(len(casts_list)):
            casts_list[i] = casts_list[i]['primaryName']

        for r in movie_rating:
            pprint(r)
        print("These are the Cast Members of this movie:")
        for i in casts_list:
            print(i)


    def search_for_genres(self,genres,minimum_vote):
        minimum_vote = int(minimum_vote)
        result = self.basics.aggregate([
                {'$unwind':'$genres'},
                {'$match':{'genres':{'$regex':genres,'$options':'i'}}},
                {'$group':{'_id':'$tconst'}},
                {'$project':{'tconst':'$_id',"_id":0}}
            ]
        )

        result_list = []
        for r in result:
            result_list.append(r['tconst'])

        new_result = self.ratings.aggregate([
            {'$match':{'numVotes':{'$gte':minimum_vote}}},
            {'$match':{'tconst':{'$in':result_list}}},
            {'$sort':{'averageRating':-1}},
            {'$project':{'tconst':'$tconst',"_id":0}}
        ]
        )

        filtered_list = []
        for r in new_result:
            filtered_list.append(r['tconst'])


        last_result = self.basics.aggregate([
            {'$match':{'tconst':{'$in':filtered_list}}},
            {'$project':{'Title of Movie':'$primaryTitle','_id':0}}
        ])


        for r in last_result:
            print(r)
    
        


user = User()
keywords = input("what are your keywords: ").split()
user.search_for_titles(keywords)
# user.search_for_genres(keywords[0],keywords[1])


