# As seen here: https://ftwgl.net/match/1674
def stats_table(match_stats: dict):
    table = {}

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

            table[player['Name']] = [
                player['Kills'],
                player['Deaths'],
                player['Assists'],
                player['Kills'] / player['Deaths'],
                (player['Kills'] + player['Assists']) / player['Deaths'],
                player['Damage'],
                player['DamageTaken'],
                player['Damage'] / player['DamageTaken'],
                player['Damage'] / len(player['TS']['Kills']),
                player['TeamDamage'],
                player['TeamDamageTaken'],
                player['TeamKills'],
                player['TeamKilled'],
                player['Suicides'],
                multikills[0], multikills[1], multikills[2], multikills[3],
                sum(multikills) / (len(player['TS']['Kills'])) * 100,
                clutches[0], clutches[1], clutches[2], clutches[3], clutches[4],
                len(player['TS']['LastAlive']),
                sum(clutches) / len(player['TS']['LastAlive']) * 100,
                player['EntryFrags'],
                player['EntryFragged'],
                player['EntryFrags'] - player['EntryFragged'],
                player['SecondsAlive']
            ]
    return table


if __name__ == '__main__':
    import json

    with open('sample_data.json') as f:
        stats = json.loads(f.read())

        headings = ['Kills', 'Deaths', 'Assists', 'K/D', 'KA/D', 'Damage Given', 'Damage Taken',
                    'Damage Ratio', 'Average Damage per Round', 'Friendly Damage Given', 'Friendly Damage Taken',
                    'Friendly Kills', 'Friendly Deaths', 'Suicides',
                    '2K', '3K', '4K', '5K', 'Multi Kill Percentage',  # Multi kills
                    '1v1', '1v2', '1v3', '1v4', '1v5',  # Clutches
                    'Last Alive', 'Clutch Percentage', 'Entry Kills', 'Entry Deaths', 'Entry Kill +/-', 'Seconds Alive']

        extracted_stats = stats_table(stats)

        for i in range(0, len(headings)):
            print(headings[i], extracted_stats['solitary'][i])

