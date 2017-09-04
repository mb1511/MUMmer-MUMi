'''
MUMmer Index value (MUMi) from MUMmer file

Translated from give_mumi.pl (from MUMmer/Sripts)
Further optimisations can definitely be made
'''

from itertools import izip
import re

def order(Gx, Gy):
    return lambda x: (x[Gx]['init'], -x[Gx]['long'], x[Gy]['init'])

def reversed_enum(sequence):
    return izip(reversed(xrange(len(sequence))), reversed(sequence))

def _read_mums(lines):
    flag_reverse = False
    for line in lines:
        if line.startswith('>'):
            if 'Reverse' not in line:
                flag_reverse = False
            else:
                flag_reverse = True
        else:
            vals = [int(v) for v in line.split()]
            if not flag_reverse:
                yield {'G0': {'init': vals[0], 'long': vals[2],
                              'fin': vals[0] + vals[2] - 1},
                       'G1': {'sens': 1, 'init': vals[1], 'long': vals[2],
                              'fin': vals[1] + vals[2] - 1}}
            else:
                yield {'G0': {'init': vals[0], 'long': vals[2],
                              'fin': vals[0] + vals[2] - 1},
                       'G1': {'sens': 0, 'fin': vals[1], 'long': vals[2],
                              'init': vals[1] - vals[2] + 1}}

def Read_mums(from_file=False, from_text=None):
    if from_file:
        with open(from_file) as s:
            tms = _read_mums(s)
    else:
        tms = _read_mums(x.group(0) for x in re.finditer('(.*\n|.+$)', from_text))
    return tms

def RechInc(tab_in, G):
    Gx, Gy = 'G%d' % G, 'G%d' % (1 - G)
    tab_in = sorted(tab_in, key=order(Gx, Gy))
    i = 0
    while True:
        try:
            if tab_in[i][Gx]['fin'] >= tab_in[i+1][Gx]['fin']:
                del tab_in[i+1]
            else:
                i += 1
        except IndexError:
            break
    return tab_in

def DoubleChev(t, g):
    t = RechInc(t, int(g[1]))
    i = len(t) - 2
    while i > 0:
        try: 
            if t[i-1][g]['fin'] >= t[i+1][g]['init'] - 1 and t[i][g]['fin'] <= t[i+1][g]['fin']:
                del t[i]
                i-=2
            else:
                i-=1
        except IndexError:
            break
    return t
       
def RechChev_trimbyend(tab_in, G):
    Gx, Gy = 'G%d' % G, 'G%d' % (1 - G)
    pval = tab_in.pop()
    end_val = pval
    for i, val in reversed_enum(tab_in):
        if val[Gx]['fin'] >= pval[Gx]['init']:
            tmp_len_ch = val[Gx]['fin'] - pval[Gx]['init'] + 1
            tab_in[i][Gx]['fin'] = pval[Gx]['init'] - 1
            tab_in[i][Gx]['long'] = val[Gx]['fin'] - val[Gx]['init'] + 1
            if val['G1']['sens']:
                tab_in[i][Gy]['fin'] = val[Gy]['fin'] - tmp_len_ch
                tab_in[i][Gy]['long'] = val[Gy]['fin'] - val[Gy]['init'] + 1
            else:
                tab_in[i][Gy]['init'] = val[Gy]['init'] + tmp_len_ch
                tab_in[i][Gy]['long'] = val[Gy]['fin'] - val[Gy]['init'] + 1
        pval = val
    tab_in.append(end_val)
    return tab_in
  
def Give_MUMI(pmums, G, l1, l2):
    out = RechChev_trimbyend(pmums, G)
    out = RechInc(out, 1 - G)
    s = sum(i['G0']['long'] for i in RechChev_trimbyend(out, 1 - G))
    return 1.0 - s / ((l1 + l2)/2.0)

def get(from_file=None, from_text=None, l1=0, l2=0):
    rtab_in = [r for r in Read_mums(from_file, from_text)]
    rtab_in = DoubleChev(rtab_in, 'G0')
    pmums = DoubleChev(rtab_in, 'G1')
    G1 = Give_MUMI(pmums, 1, l1, l2)
    G0 = Give_MUMI(sorted(pmums, key=order('G0', 'G1')), 0, l1, l2)
    return (G0 + G1)/2.0