# -*- coding: utf-8 -*-
"""
Created on Wed Nov 18 10:53:41 2020

@author: Charlie
"""

from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np
import json
import pandas as pd

def load_dataset(tournament):
    matches, events = {}, {}
    matches = json.load(open('./epldata/matches/matches_{}.json'.format(tournament)))
    events = json.load(open('./epldata/events/events_{}.json'.format(tournament)))
    players = json.load(open('./epldata/players.json'))
    competitions = json.load(open('./epldata/competitions.json'))
    teams = json.load(open('./epldata/teams.json'))
    return matches, events, players, competitions, teams

def get_match(matches, events):
    match_id2events = defaultdict(list)
    match_id2match = defaultdict(dict)
    for event in events:
        match_id = event['matchId']
        match_id2events[match_id].append(event)
                                         
    for match in matches:
        match_id = match['wyId']
        match_id2match[match_id] = match

def get_player(players):
    player_id2player = defaultdict(dict)
    for player in players:
        player_id = player['wyId']
        player_id2player[player_id] = player
    return player_id2player

def get_competitions(competitions):
    competition_id2competition = defaultdict(dict)
    for competition in competitions:
        competition_id = competition['wyId']
        competition_id2competition[competition_id] = competition
    return competition_id2competition

def get_teams(teams):
    team_id2team = defaultdict(dict)
    for team in teams:
        team_id = team['wyId']
        team_id2team[team_id] = team
    return team_id2team

matches, events, players, competitions, teams = load_dataset('England')


def id_finder(lastname, players):
    players=(pd.DataFrame(players))
    for i in range(len(players)):
        if players['lastName'][i] == lastname:
            return players['wyId'][i]
        
def event_assigner(iden,events):
    subevents=[]
    for j in range(len(events)):
        if events[j]['playerId'] == iden:
            subevents.append(events[j]['subEventName'])
            
    subevents = sorted(subevents)
    return subevents

'''now we would like to produce histograms of each players actions'''

def hist_plot(subevents):
    fig,ax = plt.subplots(1,1)  
    ax.hist(subevents)
    ax.set_title('histogram of height')
    ax.set_xlabel('event [cm]')
    ax.set_ylabel('frequency')
    return plt.show()

def simple_pass_ratio(subevents):
    m=0
    n=0
    for i in range(len(subevents)):
        if subevents[i] == 'Simple pass':
            m=m+1
        else:
            n=n+1
    
    if n+m !=0:
        simple_pass_per = (m/(n+m))*100
    else:
        simple_pass_per=0
    
    return simple_pass_per

def ball_retentions(subevents):
    m=0
    n=0
    for i in range(len(subevents)):
        if subevents[i] == 'Simple pass' or 'Head pass' or 'High pass' or 'Smart pass':
            m=m+1
        if subevents[i] == 'Clearance':
            n=n+1
    
    if n+m !=0:
        ball_ret_per = (m/(n+m))*100
    else:
        ball_ret_per=0
    
    return ball_ret_per

def smart_pass_per(subevents):    
    m=0
    n=0
    for i in range(len(subevents)):
        if subevents[i] == 'Smart pass':
            m=m+1
        if subevents[i] == 'Simple pass' or 'Head pass' or 'High pass':
            n=n+1
    
    if n+m !=0:
        smart_pass_per = (m/(n+m))*100
    else:
        smart_pass_per=0
    
    return smart_pass_per

def defenders_under_26(players):
    players=(pd.DataFrame(players))
    ident=[]
    birthyear=[]
    defenders=[]
    for i in range(len(players)):
        if int(players['birthDate'][i][0:4]) >= 1994 and players['role'][i]['name']=='Defender':
            birthyear.append((players['birthDate'][i][0:4]))
            ident.append(players['wyId'][i])
            
    defenders=ident

    return defenders

def pass_ability_plotter(players, events):
    defenders=defenders_under_26(players)
    for i in range(len(defenders)):
        subevents=event_assigner(defenders[i],events)
        spr=smart_pass_per(subevents)
        br=ball_retentions(subevents)
        if spr != 0 and br != 0:
            plt.scatter(spr, br)
            plt.xlabel('smart pass ratio')
            plt.ylabel('ball retention')
            plt.annotate(defenders[i],xy=(spr,br),textcoords='offset points')
            
    return plt.show
        
def name_finder(iden, players):
    players=(pd.DataFrame(players))
    for i in range(len(players)):
        if players['wyId'][i] == iden:
            return players['lastName'][i]



pass_ability_plotter(players, events)

print(name_finder(8135, players))