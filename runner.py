from flask import Flask,render_template,request
from services.nba import get_standing_total,get_player_stats,get_games_on_date,get_perfs_on_date
import datetime
from dateutil.relativedelta import relativedelta

app = Flask(__name__)

date = datetime.datetime.today()
date_hier = date - relativedelta(days=1)
date_hier = date_hier.strftime("%Y-%m-%d")

standing = get_standing_total() #obtenir le classement de la ligue, des deux conférences
games = get_games_on_date(date_hier) #obtenir les résultats des matchs de la veille
perfs, ttfl = get_perfs_on_date(date_hier) #obtenir les performances des joueurs durant les matchs de la veille


@app.route("/")

def home():
    averages=''
    if request.args.get('joueur') is not None:
        name = request.args.get('joueur')
        averages = get_player_stats(name)
        return render_template("home.html", games=games, standing=standing, perfs=perfs, ttfl=ttfl, averages=averages)
    elif request.args.get('date_choisie') is not None:
        date = request.args.get('date_choisie')
        games_date = get_games_on_date(date)
        perfs_date, ttfl_date = get_perfs_on_date(date)
        return render_template("home.html", games=games_date, standing=standing, perfs=perfs_date, ttfl=ttfl_date, averages=averages)
    else:
        return render_template("home.html", games=games, standing=standing, perfs=perfs, ttfl=ttfl, averages=averages) 

if __name__ == "__main__":
    app.run(debug=True)