"""
524127

Add mathematical signs (  +, - ,),( *,/ ) in between all or some of the above digits so the
result of the  created mathematical equation will be 100.
"""
import itertools
import re

number_string = '524127'
possible_symbols = set(['+', '-', ')', '(', '*', '/', ''])
legal_openings = set(['(', ''])
legal_endings = set([')', ''])
bad_openings = possible_symbols.difference(legal_openings)
bad_endings = possible_symbols.difference(legal_endings)

# make a list of bad operator combinations ('e.g., '*+' is never a good combination)
bad_duos = list(''.join(x) for x in itertools.product('+-*/', repeat=2))
lll = list(''.join(x) for x in itertools.product('+-*/', repeat=3))
for i in lll:
    bad_duos.append(i)

# first make list of possible operator combinations, filtering out bad ones
operator_combos = set()
for i in range(1, 4):  # 1, 2, or 3 operators between each number, including empty string
    for x in itertools.permutations(possible_symbols, i):
        combo = ''.join(x)
        if any(x in combo for x in bad_duos):
            continue
        elif '()' in combo or ')(' in combo:
            continue
        elif '+)' in combo or '-)' in combo or '*)' in combo or '/)' in combo:
            continue
        elif '(+' in combo or '(-' in combo or '(*' in combo or '(/' in combo:
            continue
        else:
            operator_combos.add(''.join(x))

cntr = 0
valid_exps = 0
winners = set()
for opening, operators, closing in itertools.product(
        legal_openings, itertools.permutations(operator_combos, 5), legal_endings):
    cntr += 1
    if cntr % 100000 == 0:
        print('Finished {0} attempts, found {1} valid expressions'.format(
            cntr, valid_exps))
    try:
        expr = opening
        expr += ''.join(''.join(a) for a in itertools.zip_longest(
            number_string, [''.join(y) for y in operators], fillvalue=''))
        expr += closing
        val = eval(expr)
        valid_exps += 1
        if val == 100:
            winners.add(expr)
    except:  # syntax error from illegal expression
        pass

unique_winners = set()
single_nums_in_parens = [(re.compile('\({0}\)'.format(x)), x) for x in number_string]
for winner in winners:
    for regex, snip in single_nums_in_parens:
        winner = regex.sub(snip, winner)
    unique_winners.add(winner)

print('Found {0} winning combinations:'.format(len(winners)))
print('Found {0} unique winning combinations:'.format(len(unique_winners)))
for winner in unique_winners:
    print('{0} = 100'.format(winner))
