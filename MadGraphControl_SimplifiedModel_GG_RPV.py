include ( 'MC15JobOptions/MadGraphControl_SimplifiedModelPreInclude.py' )
import math
evt_multiplier = 1.05
njets=0
def calculateAlpha(q,nf=6.0):
    alpha = 0.1185
    beta0 = 33.0-2.0*nf
    beta0 /= (12*math.pi)
    mu = 91.1876
    return alpha/(1+alpha*beta0*math.log((q*q)/(mu*mu)))
def calculateWidth(mg,mq):
    alpha = calculateAlpha(mq)
    w = 2*alpha/3
    w *= (mq*mq-mg*mg)*(mq*mq-mg*mg)
    w /= mq*mq*mq
    return w
masses['1000021'] = float(runArgs.jobConfig[0].split('_')[4])
masses['1000022'] = float(runArgs.jobConfig[0].split('_')[5])
if masses['1000022']<0.5: masses['1000022']=0.5
for squark in squarks:
    masses[str(squark)] = float(runArgs.jobConfig[0].split('_')[6].split('.')[0])
    decays[str(squark)] = 'DECAY   '+str(squark)+'     '+str(calculateWidth(float(masses['1000021']),float(masses[str(squark)])))
gentype = str(runArgs.jobConfig[0].split('_')[2])
decaytype = str(runArgs.jobConfig[0].split('_')[3])
if masses['1000022'] > 173.34:
    if decaytype == 'RPV10':
        decays['1000022'] = '''DECAY   1000022  1.0000000000E+00   # neutralino1 decays
#          BR          NDA       ID1       ID2       ID3       ID4		
      1	   		3    2	1  3
      1			3    2	1  5
      1			3    2	3  5
      1			3    4	1  3
      1			3    4	1  5
      1			3    4	3  5
      1			3    6	1  3
      1			3    6	1  5
      1			3    6	3  5
      1			3   -2 -1 -3
      1			3   -2 -1 -5
      1			3   -2 -3 -5
      1			3   -4 -1 -3
      1			3   -4 -1 -5
      1			3   -4 -3 -5
      1			3   -6 -1 -3
      1			3   -6 -1 -5
      1			3   -6 -3 -5
#'''
    elif decaytype == 'RPV6':
        decays['1000021'] = '''DECAY   1000021  1.0000000000E+00   # gluino decays
#          BR          NDA       ID1       ID2       ID3       ID4		
      1	   		3    2	1  3
      1			3    2	1  5
      1			3    2	3  5
      1			3    4	1  3
      1			3    4	1  5
      1			3    4	3  5
      1			3    6	1  3
      1			3    6	1  5
      1			3    6	3  5
      1			3   -2 -1 -3
      1			3   -2 -1 -5
      1			3   -2 -3 -5
      1			3   -4 -1 -3
      1			3   -4 -1 -5
      1			3   -4 -3 -5
      1			3   -6 -1 -3
      1			3   -6 -1 -5
      1			3   -6 -3 -5
#'''
process = '''
define sq = susylq susylq~
generate p p > go go
'''
if njets == 2:
    process = '''
define sq = susylq susylq~
generate p p > go go @1
add process p p > go go j @2
add process p p > go go j j @3
'''
evgenLog.info('Registered generation of gluino grid '+str(runArgs.runNumber))

evgenConfig.contact  = [ "brian.thomas.amadio@cern.ch" ]
evgenConfig.keywords += ['gluino','SUSY','simplifiedModel','RPV']
evgenConfig.description = 'gluino production with RPV decays, m_glu = %s GeV, m_N1 = %s GeV'%(masses['1000021'],masses['1000022'])

include ( 'MC15JobOptions/MadGraphControl_SimplifiedModelPostInclude.py' )

if njets>0:
    genSeq.Pythia8.Commands += ["Merging:Process = pp>{go,1000021}{go,1000021}"]
