# As seen here: https://ftwgl.net/match/1674

class Stat:
    def __init__(self, stat: str, abbreviation: str, value):
        self.stat: str = stat
        self.abbreviation: str = abbreviation
        self.value = value

def stats_table(match_stats: dict):
    table = {}

    nade_kills = {}
    nade_deaths = {}
    headshots_given = {}
    headshots_taken = {}

    for player in match_stats['stats']['Players']:
        nade_kills[player['PlayerNo']] = 0
        nade_deaths[player['PlayerNo']] = 0
        headshots_given[player['PlayerNo']] = 0
        headshots_taken[player['PlayerNo']] = 0

    for round in match_stats['stats']['TsRounds']:
        for kill in round['KillLog']:
            if kill['Weapon'] == 'HE':
                nade_kills[kill['Killer']] += 1
                nade_deaths[kill['Killed']] += 1

        for hit in round['HitLog']:
            if hit['Location'] in ['HEAD', 'HELMET']:
                if hit['Location'] in ['HEAD', 'HELMET']:
                    headshots_given[hit['Shooter']] += 1
                    headshots_taken[hit['Hit']] += 1

    for player in match_stats['stats']['Players']:
        if not player['Kills'] == 0 and not player['Deaths'] == 0:  # Ignore players who didn't play
            # mk          2  3  4  5
            multikills = [0, 0, 0, 0]
            # 1v        1  2  3  4  5
            clutches = [0, 0, 0, 0, 0]

            for ks in player['TS']['Kills']:
                if ks > 1:
                    if ks == 2:
                        multikills[0] += 1
                    elif ks == 3:
                        multikills[1] += 1
                    elif ks == 4:
                        multikills[2] += 1
                    else:
                        multikills[3] += 1

            for c in player['TS']['LastAlive']:
                if 'Clutch' in player['TS']:

                    for clutch in player['TS']['Clutch']:
                        if clutch == c['Round']:
                            if c['Opponents'] == 1:
                                clutches[0] += 1
                            elif c['Opponents'] == 2:
                                clutches[1] += 1
                            elif c['Opponents'] == 3:
                                clutches[2] += 1
                            elif c['Opponents'] == 4:
                                clutches[3] += 1
                            elif c['Opponents'] == 5:
                                clutches[4] += 1
            
            table[player['PlayerNo']] = [
                Stat('Kills', 'K', player['Kills']),
                Stat('Deaths', 'D', player['Deaths']),
                Stat('Assists', 'A', player['Assists']),
                Stat('Kill Death Ratio', 'KDR', player['Kills'] / player['Deaths']),
                Stat('Kill Death Assist Ratio', 'KDA', (player['Kills'] + player['Assists']) / player['Deaths']),
                Stat('Damage Given', 'DG', player['Damage']),
                Stat('Damage Taken', 'DT', player['DamageTaken']),
                Stat('Damage Ratio', 'DR', player['Damage'] / player['DamageTaken']),
                Stat('Average Damage Round', 'ADR', player['Damage'] / len(player['TS']['Kills'])),
                Stat('Friendly Damage Given', 'FDG', player['TeamDamage']),
                Stat('Friendly Damage Taken', 'FDT', player['TeamDamageTaken']),
                Stat('Friendly Kills', 'FK', player['TeamKills']),
                Stat('Friendly Deaths', 'FD', player['TeamKilled']),
                Stat('Suicides', 'S', player['Suicides']),
                Stat('2K Multikill', '2K', multikills[0]),
                Stat('3K Multikill', '3K', multikills[1]),
                Stat('4K Multikill', '4K', multikills[2]),
                Stat('5K Multikill', '5K', multikills[3]),
                Stat('Multikill Percent', 'MKP', sum(multikills) / (len(player['TS']['Kills'])) * 100),
                Stat('1v1 Clutch', '1v1', clutches[0]),
                Stat('1v2 Clutch', '1v2', clutches[1]),
                Stat('1v3 Clutch', '1v3', clutches[2]),
                Stat('1v4 Clutch', '1v3', clutches[3]),
                Stat('1v5 Clutch', '1v5', clutches[4]),
                Stat('Last Alive', 'LA', len(player['TS']['LastAlive'])),
                Stat('Clutch Percentage', 'CP', sum(clutches) / len(player['TS']['LastAlive']) * 100),
                Stat('Entry Frags', 'EF', player['EntryFrags']),
                Stat('Entry Deaths', 'ED', player['EntryFragged']),
                Stat('Entry Kill/Death Ratio', 'EKD', player['EntryFrags'] - player['EntryFragged']),
                Stat('Seconds Alive', 'SA', player['SecondsAlive']),
                Stat('Nade Kills', 'NK', nade_kills[player['PlayerNo']]),
                Stat('Nade Deaths', 'ND', nade_deaths[player['PlayerNo']]),
                Stat('Headshots', 'HS', headshots_given[player['PlayerNo']]),
                Stat('Headshots Taken', 'HST', headshots_taken[player['PlayerNo']])
            ]
    return table


if __name__ == '__main__':
    import json

    with open('sample_data.json') as f:
        stats = json.loads(f.read())

        extracted_stats = stats_table(stats)

        print(stats['stats']['Players'][9]['Name'])
        for stat in extracted_stats[9]:
            print(f"{stat.stat  : <25} {stat.abbreviation  : ^20} {round(stat.value, 2)  : >20}")
