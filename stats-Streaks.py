		
streak = 0
antistreak = 0           
continuation = 0
absence = 0
for i in range(0, len(player['TS']['Kills'])-2):
    if player['TS']['Kills'][i] and player['TS']['Kills'][i+1]: #if kills in consecutive rounds exist:
	continuation += 1

	if continuation > streak:   # growing
	    streak=continuation     

    elif player['TS']['Kills'][i] == 0 and player['TS']['Kills'][i+1] == 0:              
	absence += 1

	if absence > antistreak:
	    antistreak=absence

    else:
	continuation = 0
	absence = 0 

streak += 1
antistreak += 1

#antistreak and streak must be increased by one at the end
