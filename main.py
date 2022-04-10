import setup
import getDataFromDatabase as db
from app import MainApp
import solve

if __name__ == '__main__':

    nouns = db.getData()
    print('Nouns have been loaded : ', len(nouns))

    setup.loadMeanings(nouns)
    setup.loadEncodedNouns(nouns)
    solve.loadNounsToDll()
    # print(meanings)
    # print(nouns)

    app = MainApp()
    app.run()
