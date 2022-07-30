for rounds in match_stats['stats']['TsRounds']:
	hs=0
	nades=0
	for hits in rounds['HitLog']:
		if hits['Damage'] == 51:
			hs+=1
	for nds in rounds['KillLog']:
		if nds['Weapon'] == 'HE':
			nades+=1
