from ast import keyword
from curses.ascii import isdigit
from telnetlib import KERMIT
from turtle import title
from connection import collections
from pprint import pprint


class User():
    def __init__(self):
        self.name = collections["name.basics"]
        self.basics = collections["title.basics"]
        self.principals= collections["title.principals"]
        self.ratings = collections["title.ratings"]

    def search_for_titles(self):
        keywords = input("what are your keywords: ").split()
        strings = []
        years = []
        for i in range(0,len(keywords)):
            if keywords[i].isdigit():
                years.append(int(keywords[i]))
            else: 
                strings.append(keywords[i])

        regex = ' AND'.join(strings)

        self.basics.create_index([('primaryTitle','text')])

        if (len(strings)  > 0 and len(years) > 0):
            result = self.basics.find(
                {'$and':[
                {'$text':{'$search':regex}},
                {'startYear':{'$in':years}}
                ]}
                #  {'$or':[{'$text':{'$search':regex}},{'startYear':{'$in':years}}]}
            )
        elif len(years) == 0:
            result = self.basics.find(
                {'$text':{'$search':regex}})
        elif len(strings) == 0:
            result = self.basics.find(
                {'startYear':{'$in':years}})
            

        all_movies = []
        for r in result:
            pprint(r)
            print("\n")
            all_movies.append(r['primaryTitle'])

        movie =''
        while movie not in all_movies:
            movie = input("select a Valid Title to get more information on: ")

        tconst = self.basics.find({'primaryTitle':movie})
        tconst = list(tconst)[0]['tconst']


        movie_rating = self.ratings.find(
            {'tconst': tconst},
            {'_id':movie,'Ratings': '$averageRating','Number of Votes':'$numVotes'}
        )

        nconst = self.principals.find({'tconst':tconst})
        nconst_list = list(nconst)
        for i in range(0,len(nconst_list)):
            nconst_list[i] = nconst_list[i]['nconst']

        casts = self.name.find({'nconst':{'$in':nconst_list}})
        casts_list = list(casts)
        for i in range(len(casts_list)):
            casts_list[i] = casts_list[i]['primaryName']



        for r in movie_rating:
            pprint(r)
        print("These are the Cast Members of this movie:")
        print(casts_list)


user = User()
user.search_for_titles()
