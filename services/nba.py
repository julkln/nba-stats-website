from operator import itemgetter,getitem
import requests
import json
import datetime
import itertools
from dateutil import parser

abb = {
    'PHX':'https://cdn.nba.com/logos/nba/1610612756/global/L/logo.svg', 'MIA':'https://cdn.nba.com/logos/nba/1610612748/global/L/logo.svg',
    'MEM':'https://cdn.nba.com/logos/nba/1610612763/global/L/logo.svg', 'MIL':'https://cdn.nba.com/logos/nba/1610612749/global/L/logo.svg',
    'GSW':'https://cdn.nba.com/logos/nba/1610612744/global/L/logo.svg', 'PHI':'https://cdn.nba.com/logos/nba/1610612755/global/L/logo.svg',
    'UTA':'https://cdn.nba.com/logos/nba/1610612762/global/L/logo.svg', 'CHI':'https://cdn.nba.com/logos/nba/1610612741/global/L/logo.svg',
    'DAL':'https://cdn.nba.com/logos/nba/1610612742/global/L/logo.svg', 'BOS':'https://cdn.nba.com/logos/nba/1610612738/global/L/logo.svg',
    'DEN':'https://cdn.nba.com/logos/nba/1610612743/global/L/logo.svg', 'CLE':'https://cdn.nba.com/logos/nba/1610612739/global/L/logo.svg',
    'MIN':'https://cdn.nba.com/logos/nba/1610612750/global/L/logo.svg', 'TOR':'https://cdn.nba.com/logos/nba/1610612761/global/L/logo.svg',
    'LAC':'https://cdn.nba.com/logos/nba/1610612746/global/L/logo.svg', 'BKN':'https://cdn.nba.com/logos/nba/1610612751/global/L/logo.svg',
    'LAL':'https://cdn.nba.com/logos/nba/1610612747/global/L/logo.svg', 'ATL':'https://cdn.nba.com/logos/nba/1610612737/global/L/logo.svg',
    'NOP':'https://cdn.nba.com/logos/nba/1610612740/global/L/logo.svg', 'CHA':'https://cdn.nba.com/logos/nba/1610612766/global/L/logo.svg',
    'POR':'https://cdn.nba.com/logos/nba/1610612757/global/L/logo.svg', 'WAS':'https://cdn.nba.com/logos/nba/1610612764/global/L/logo.svg',
    'SAS':'https://cdn.nba.com/logos/nba/1610612759/global/L/logo.svg', 'NYK':'https://cdn.nba.com/logos/nba/1610612752/global/L/logo.svg',
    'SAC':'https://cdn.nba.com/logos/nba/1610612758/global/L/logo.svg', 'IND':'https://cdn.nba.com/logos/nba/1610612754/global/L/logo.svg',
    'OKC':'https://cdn.nba.com/logos/nba/1610612760/global/L/logo.svg', 'DET':'https://cdn.nba.com/logos/nba/1610612765/global/L/logo.svg',
    'HOU':'https://cdn.nba.com/logos/nba/1610612745/global/L/logo.svg', 'ORL':'https://cdn.nba.com/logos/nba/1610612753/global/L/logo.svg',
}


def convert_hours(date_str):

    my_date = parser.parse(date_str)
    my_date = my_date + datetime.timedelta(hours=2)
    if my_date.hour >= 0 and my_date.hour < 10 :
        if my_date.minute >= 0 and my_date.minute < 10 :
            return '0' + str(my_date.hour) + ':' + '0' + str(my_date.minute) 
        else:
            return '0' + str(my_date.hour) + ':' + str(my_date.minute)
    else:
        if my_date.minute >= 0 and my_date.minute < 10 :
            return str(my_date.hour) + ':' + '0' + str(my_date.minute) 
        else:
            return str(my_date.hour) + ':' + str(my_date.minute)
            
def get_games_on_date(date):
    params={'start_date': date,'end_date': date}
    r = requests.get('https://www.balldontlie.io/api/v1/games',params=params)
    data = json.loads(r.text)
    games = data['data']
    info = []
    
    for idx,item in enumerate(games):
        home_team = item['home_team']['full_name']
        away_team = item['visitor_team']['full_name']
        abb_home_team = item['home_team']['abbreviation']
        abb_away_team = item['visitor_team']['abbreviation']
        home_team_score = item['home_team_score']
        away_team_score = item['visitor_team_score']
        logo_home = abb[abb_home_team]
        logo_away = abb[abb_away_team]
        dico={}
        dico['id_game'] = item['id']
        dico['home'] = home_team
        dico['away'] = away_team
        dico['period'] = item['period']
        dico['heure'] = ''
        if 'T' in item['status'] and 'Z' in item['status']:
            dico['heure'] = convert_hours(item['status'])
        else:
            dico['heure'] = 'TBD'
        dico['home_score'] = home_team_score
        dico['away_score'] = away_team_score
        dico['logo_away'] = logo_away
        dico['logo_home'] = logo_home
        if home_team_score > away_team_score:
            dico['winner'] = 'home'
        else:
            dico['winner'] = 'away'
        info.append(dico)
    info = sorted(info, key=itemgetter('heure')) 
    return info

def get_standing_total():
    #date = datetime.datetime.today()
    #date = date.strftime("%Y-%m-%d")

    url = 'https://www.balldontlie.io/api/v1/games/'
    
    total_games = []
    for i in range(13):
        params={'start_date':'2023-10-24','end_date':'2024-04-14','per_page':'100','page':str(i)}
        games = requests.get(url,params=params).json()['data']
        total_games.append(games)
    total_games = list(itertools.chain(*total_games))
    total_games = [i for n, i in enumerate(total_games) if i not in total_games[n + 1:]]

    classement = {}
    for idx,item in enumerate(total_games):
        home = item['home_team']['full_name']
        away = item['visitor_team']['full_name']
            
        if item['home_team_score'] > item['visitor_team_score'] :
            if home not in classement.keys():
                classement[home] = {}
                classement[home]['V'] = 0
                classement[home]['D'] = 0
                classement[home]['division'] = item['home_team']['conference']
                classement[home]['abb'] = item['home_team']['abbreviation']
            if away not in classement.keys():
                classement[away] = {}
                classement[away]['V'] = 0
                classement[away]['D'] = 0
                classement[away]['division'] = item['visitor_team']['conference']
                classement[away]['abb'] = item['visitor_team']['abbreviation']
            classement[home]['V'] += 1
            classement[away]['D'] += 1
        elif item['home_team_score'] < item['visitor_team_score']:
            if home not in classement.keys():
                classement[home] = {}
                classement[home]['V'] = 0
                classement[home]['D'] = 0
                classement[home]['division'] = item['home_team']['conference']
                classement[home]['abb'] = item['home_team']['abbreviation']
            if away not in classement.keys():
                classement[away] = {}
                classement[away]['V'] = 0
                classement[away]['D'] = 0
                classement[away]['division'] = item['visitor_team']['conference']
                classement[away]['abb'] = item['visitor_team']['abbreviation']
            classement[home]['D'] += 1
            classement[away]['V'] += 1
        else:
            pass
    standing = {}
    standing['West'] = []
    standing['East'] = []
    for key,value in classement.items():
        if value['division'] == 'East':
            dico={}
            dico['team'] = key 
            dico['V'] = value['V']
            dico['D'] = value['D']
            dico['pct'] = value['V']/(value['V']+value['D'])
            dico['logo'] = abb[value['abb']]
            standing['East'].append(dico)
        else:
            dico={}
            dico['team'] = key 
            dico['V'] = value['V']
            dico['D'] = value['D']
            dico['pct'] = value['V']/(value['V']+value['D'])
            dico['logo'] = abb[value['abb']]
            standing['West'].append(dico)
    standing['West'] = sorted(standing['West'], key=itemgetter('pct'),reverse=True)
    standing['East'] = sorted(standing['East'], key=itemgetter('pct'),reverse=True)
    return standing

def get_perfs_on_date(date):
    games = get_games_on_date(date)
    id_games = []
    for game in games:
        id_games.append(game['id_game'])

    players = {}
    ttfl = []
    for j in range(len(id_games)):
        players[id_games[j]] = {}
        total_stats = []
        params={'game_ids[]':[id_games[j]],'per_page':'35'}
        r = requests.get('https://www.balldontlie.io/api/v1/stats',params=params).json()
        stats = r['data']
        for stat in stats :
            if stat['min'] != '':
                min = int(stat['min'].split(':')[0])
                if  min > 2 :
                    total_stats.append(stat)
                    ttfl.append(stat)
        for i in total_stats:
            a = {}
            a['logo'] = abb[i['team']['abbreviation']]
            a['pts'] = i['pts']
            a['reb'] = i['reb']
            a['ast'] = i['ast']
            a['stl'] = i['stl']
            a['blk'] = i['blk']
            a['to'] = i['turnover']
            a['fg3a'] = i['fg3a']
            a['fg3m'] = i['fg3m']
            a['fga'] = i['fga']
            a['fgm'] = i['fgm']
            a['fta'] = i['fta']
            a['ftm'] = i['ftm']
            a['TTFL'] = i['pts'] + i['reb'] + i['ast'] + i['blk'] + i['stl'] + 2*i['fgm'] + 2*i['fg3m'] + 2*i['ftm'] - i['fga'] - i['fg3a'] - i['fta'] - i['turnover']
            players[id_games[j]][i['player']['first_name'] + ' ' + i['player']['last_name']] = a
        players[id_games[j]] = sorted(players[id_games[j]].items(), key=lambda x: getitem(x[1],'TTFL'),reverse=True)[:10]

    list_ttfl = []
    for i in ttfl:
        dico = {}
        dico['logo'] = abb[i['team']['abbreviation']]
        dico['player'] = i['player']['first_name'] + ' ' + i['player']['last_name']
        dico['TTFL'] = i['pts'] + i['reb'] + i['ast'] + i['blk'] + i['stl'] + 2*i['fgm'] + 2*i['fg3m'] + 2*i['ftm'] - i['fga'] - i['fg3a'] - i['fta'] - i['turnover']
        list_ttfl.append(dico)

    if len(list_ttfl) >= 15:
        list_ttfl = sorted(list_ttfl, key=lambda x: x['TTFL'],reverse=True)[:15]
    else:
        list_ttfl = sorted(list_ttfl, key=lambda x: x['TTFL'],reverse=True)
    return players,list_ttfl

def get_player_stats(name_player):
    r = json.loads(requests.get('https://www.balldontlie.io/api/v1/players?search='+name_player).text)
    data = r['data']
    
    players = []
    for i in data:
        id = str(i['id'])
        stats = json.loads(requests.get('https://www.balldontlie.io/api/v1/season_averages?season=2023&player_ids[]='+id).text)
        if len(stats['data']) > 0:
            a = {}
            a['games_played'] = stats['data'][0]['games_played']
            a['pts'] = round(stats['data'][0]['pts'],1)
            a['reb'] = round(stats['data'][0]['reb'],1)
            a['ast'] = round(stats['data'][0]['ast'],1)
            a['stl'] = round(stats['data'][0]['stl'],1)
            a['blk'] = round(stats['data'][0]['blk'],1)
            a['to'] = round(stats['data'][0]['turnover'],1)
            a['fgm'] = round(stats['data'][0]['fgm'],1)
            a['fga'] = round(stats['data'][0]['fga'],1)
            a['fg_pct'] = int(100*round(stats['data'][0]['fg_pct'],2))
            a['fg3m'] = round(stats['data'][0]['fg3m'],1)
            a['fg3a'] = round(stats['data'][0]['fg3a'],1)
            a['fg3_pct'] = int(100*round(stats['data'][0]['fg3_pct'],2))
            a['ftm'] = round(stats['data'][0]['ftm'],1)
            a['fta'] = round(stats['data'][0]['fta'],1)
            a['ft_pct'] = int(100*round(stats['data'][0]['ft_pct'],2))
            a['logo'] = abb[i['team']['abbreviation']]
            a['name'] = i['first_name'] + ' '+ i['last_name']
            players.append(a)
    players = sorted(players, key=itemgetter('pts'),reverse=True) 
    if (len(players) >= 1) and (len(players) <= 5):
        return players
    elif (len(players) > 5):
        return players[:5]
    else:
        return 'Existe pas'