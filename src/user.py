from lib2to3.pgen2.token import MINUS
from tkinter import N
from unicodedata import category
from connection import collections
from pprint import pp, pprint


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


        if (input("Would you like to choose a specific Movie? (yes/no): ").lower() == "yes"):
            movie = ''
            while movie.lower() not in all_movies:
                movie = input("select a Valid Title to get more information on: ")

            tconsts = self.basics.aggregate([
            {'$match':{'primaryTitle':{'$regex':'^' + movie + '$','$options':'i'}}},
            {'$lookup':{
                'from': 'title_ratings',
                'localField' : 'tconst',
                'foreignField' : 'tconst',
                'as' : 'ratings'
            }},
            {'$unwind':'$ratings'}, 
            {'$project':{'_id':0,'primaryTitle':'$primaryTitle','tconst':'$tconst','numVotes':'$ratings.numVotes','rating':'$ratings.averageRating'}} 
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
            print("Title: " + ratings['primaryTitle'] + ' | Number of Votes:  ' + str(ratings['numVotes']) + ' | Rating:  ' + str(ratings['rating']))

            names = list(self.name.find(
                {'nconst':{'$in':nconst_list}},
                {'nconst':'$nconst','primaryName':'$primaryName'}
            ))

            print("\nHere are the names of the Cast, their Category and the name of the Character they played\n")
            for cast in names:
                characters_str = ""
                for n_const in nconst:
                    if cast['nconst'] == n_const['nconst']:
                        if n_const['characters'] != None:
                            length = len(n_const['characters'][0])
                            characters_str += n_const['characters'][0][1:length-1]
                        else:
                            characters_str = "None"
                        print(cast['primaryName'] + ' | ' + n_const['category'] + ' | ' + characters_str)

            


           


    def search_for_genres(self,genres,minimum_vote):
        minimum_vote = int(minimum_vote)
        result = self.basics.aggregate([
                {'$unwind':'$genres'},
                {'$match':{'genres':{'$regex':'^'+ genres + '$','$options':'i'}}},
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
            {'$project':{'tconst':'$tconst','Average':'$averageRating','Votes':'$numVotes',"_id":0}}
        ]
        )

        new_result_list = list(new_result)
        filtered_list = []
        for r in new_result_list:
            filtered_list.append(r['tconst'])

        last_result = list(self.basics.aggregate([
            {'$match':{'tconst':{'$in':filtered_list}}},
            {'$project':{'tconst':'$tconst','Title of Movie':'$primaryTitle','_id':0}}
        ]))
        for j in range(0,len(new_result_list)):        
            for i in range(0,len(last_result)):
                if last_result[i]['tconst'] == new_result_list[j]['tconst']:
                    print(last_result[i]['Title of Movie'], '|' , str(new_result_list[j]['Average']) ,'|' , str(new_result_list[j]['Votes']))
                    break

        
    def search_for_member(self, name_input):
        output = []

        actorID = self.name.aggregate([
            {'$unwind':'$primaryProfession'},
            {'$match':{'primaryName':{'$regex': '^' + name_input + '$','$options':'i'}}},
            {'$group':{'_id':'$nconst',
                'primaryProfession':{'$addToSet':'$primaryProfession'},
                'primaryName':{'$first':'$primaryName'}
            }},
            {'$project':{'_id':'$_id','primaryProfession':'$primaryProfession','primaryName':'$primaryName'}}
        ])

            

        for r in actorID:
            print("\nHere is the Info for a cast that matches your description")
            new_result = self.principals.aggregate([
                {'$match':{'nconst':r['_id']}},
                 {'$match':{'$or':[{'job':{'$ne':None}} , {'characters':{'$ne':None}}]}},
                {'$lookup':{
                    'from': 'title_basics',
                    'localField' : 'tconst',
                    'foreignField' : 'tconst',
                    'as' : 'titles'
                }},
                {'$unwind':'$titles'},
                {'$project':{'Name':'$titles.primaryTitle','job':'$job','characters':'$characters'}}
            ])
            
            print("Name: ",r['primaryName'] ,'|','Profession(s): ',','.join(r['primaryProfession']),'\n')

            print("Here are their Movies, their jobs and the characters they played")
            for i in new_result:
                if i['characters'] == None:
                    print(i['Name'],'|',i['job'],'|',"No Characterss")
                else:
                    print(i['Name'],'|',i['job'],'|',",".join(i['characters']))
            
            print()





user = User()
keywords = input("what are your keywords: ").split()
# user.search_for_titles(keywords)
user.search_for_genres(keywords[0],keywords[1])
# user.search_for_member(keywords)


