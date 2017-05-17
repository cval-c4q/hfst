exec(compile(open('CompileOptions.py', 'rb').read(), 'CompileOptions.py', 'exec'))

# matches all symbols
pi = hfst.read_att_string("0 0 @_IDENTITY_SYMBOL_@ @_IDENTITY_SYMBOL_@\n\
0")

# matches all symbols except "|"
pi_house = hfst.read_att_string("0 0 @_IDENTITY_SYMBOL_@ @_IDENTITY_SYMBOL_@\n\
0 1 | |\n\
0")

# The possible values of a house color (spaces are added for better readability)
Color = hfst.fst(["blue", "green", "red", "white", "yellow"])

# The possible values of nationality
Nationality = hfst.fst(["Dane", "Englishman", "German", "Swede", "Norwegian"])

# The possible values of a drink
Drink = hfst.fst(["bier", "coffee", "milk", "tea", "water"])

# The possible values of cigarettes
Cigarette = hfst.fst(["Blend", "BlueMaster", "Dunhill", "PallMall", "Prince"])

# The possible values of animals
Pet = hfst.fst(["birds", "cats", "dogs", "fish", "horses"])

# Convert all strings into transducers
vars={}
for i in ("blue", "green", "red", "white", "yellow",
          "Dane", "Englishman", "German", "Swede", "Norwegian",
          "bier", "coffee", "milk", "tea", "water",
          "Blend", "BlueMaster", "Dunhill", "PallMall", "Prince",
          "birds", "cats", "dogs", "fish", "horses"):
    tr = hfst.fst(i)
    vars[i] = tr

# Separator character (spaces are included for better readability)
HouseSeparator = hfst.fst("| ")

# House contains the consecutive values "ColorNationalityDrinkCigarettePet"
House = hfst.concatenate((Color, Nationality, Drink, Cigarette, Pet))

# Houses is "House| House| House| House| House"
tmp = hfst.concatenate((House, HouseSeparator))
tmp.repeat_n(4)
Houses = hfst.concatenate((tmp, House))

Houses.write_to_file('Result')

# 1. The Englishman lives in the red house.
# Since color and nationality are adjacent, it is enough to accept all strings that contain "red Englishman"
tmp = hfst.fst("red Englishman")
C1 = hfst.concatenate((pi, tmp, pi)) # .* "red Englishman" .*

# 2. The Swede keeps dogs.
# Now we must match the string between Swede and dog inside the same house.
tmp1 = hfst.fst('Swede')
tmp2 = hfst.fst('dogs')
C2 = hfst.concatenate((pi, tmp1, pi, tmp2, pi)) # .* "Swede" .* "dogs" .*

# 3. The Dane drinks tea
C3 = hfst.concatenate((pi, vars['Dane'], vars['tea'], pi))

# 4. The green house is just to the left of the white one
C4 = hfst.concatenate((pi, vars['green'], pi_house, HouseSeparator, vars['white'], pi))

# 5. The owner of the green house drinks coffee
C5 = hfst.concatenate((pi, vars['green'], pi_house, vars['coffee'], pi))

# 6. The Pall Mall smoker keeps birds
C6 = hfst.concatenate((pi, vars['PallMall'], vars['birds'], pi))

# 7. The owner of the yellow house smokes Dunhills
C7 = hfst.concatenate((pi, vars['yellow'], pi_house, vars['Dunhill'], pi))

# 8. The man in the center house drinks milk
C8 = hfst.concatenate((pi_house, HouseSeparator, pi_house, HouseSeparator, pi_house,
                       vars['milk'], pi_house, HouseSeparator, pi_house, HouseSeparator, pi_house))

# 9. The Norwegian lives in the first house
C9 = hfst.concatenate((pi_house, vars['Norwegian'], pi))

# 10. The Blend smoker has a neighbor who keeps cats
C101 = hfst.concatenate((pi, vars['Blend'], Pet, HouseSeparator, pi_house, vars['cats'], pi))
C102 = hfst.concatenate((pi, vars['cats'], pi_house, HouseSeparator, pi_house, vars['Blend'], pi))
C10 = hfst.disjunct((C101, C102))
C10.minimize()

# 11. The man who keeps horses lives next to the Dunhill smoker
C111 = hfst.concatenate((pi, vars['horses'], HouseSeparator, pi_house, vars['Dunhill'], pi))
C112 = hfst.concatenate((pi, vars['Dunhill'], pi_house, HouseSeparator, pi_house, vars['horses'], pi))
C11 = hfst.disjunct((C111, C112))
C11.minimize()

# 12. The man who smokes Blue Masters drinks bier.
C12 = hfst.concatenate((pi, vars['bier'], vars['BlueMaster'], pi))

# 13. The German smokes Prince
C13 = hfst.concatenate((pi, vars['German'], Drink, vars['Prince'], pi))

C13.write_to_file('Result')
