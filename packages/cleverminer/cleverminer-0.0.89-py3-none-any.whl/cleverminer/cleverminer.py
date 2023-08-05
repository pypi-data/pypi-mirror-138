import time #line:1
from time import strftime #line:3
from time import gmtime #line:4
import pandas as pd #line:6
class cleverminer :#line:8
    version_string ="0.0.89"#line:10
    def __init__ (O0OOOO0O0OO0OO00O ,**O0OO00OOO000O000O ):#line:12
        O0OOOO0O0OO0OO00O ._print_disclaimer ()#line:13
        O0OOOO0O0OO0OO00O .stats ={'total_cnt':0 ,'total_valid':0 ,'control_number':0 ,'start_prep_time':time .time (),'end_prep_time':time .time (),'start_proc_time':time .time (),'end_proc_time':time .time ()}#line:21
        O0OOOO0O0OO0OO00O ._init_data ()#line:22
        O0OOOO0O0OO0OO00O ._init_task ()#line:23
        if len (O0OO00OOO000O000O )>0 :#line:24
            O0OOOO0O0OO0OO00O .kwargs =O0OO00OOO000O000O #line:25
            O0OOOO0O0OO0OO00O ._calc_all (**O0OO00OOO000O000O )#line:26
    def _init_data (O0OO0OOOO000000OO ):#line:28
        O0OO0OOOO000000OO .data ={}#line:30
        O0OO0OOOO000000OO .data ["varname"]=[]#line:31
        O0OO0OOOO000000OO .data ["catnames"]=[]#line:32
        O0OO0OOOO000000OO .data ["vtypes"]=[]#line:33
        O0OO0OOOO000000OO .data ["dm"]=[]#line:34
        O0OO0OOOO000000OO .data ["rows_count"]=int (0 )#line:35
        O0OO0OOOO000000OO .data ["data_prepared"]=0 #line:36
    def _init_task (OOO0OO0O0O00OO000 ):#line:38
        OOO0OO0O0O00OO000 .cedent ={'cedent_type':'none','defi':{},'num_cedent':0 ,'trace_cedent':[],'traces':[],'generated_string':'','filter_value':int (0 )}#line:47
        OOO0OO0O0O00OO000 .task_actinfo ={'proc':'','cedents_to_do':[],'cedents':[]}#line:51
        OOO0OO0O0O00OO000 .rulelist =[]#line:52
        OOO0OO0O0O00OO000 .stats ['total_cnt']=0 #line:54
        OOO0OO0O0O00OO000 .stats ['total_valid']=0 #line:55
        OOO0OO0O0O00OO000 .stats ['control_number']=0 #line:56
        OOO0OO0O0O00OO000 .result ={}#line:57
    def _get_ver (OOO0OO000OO0OOO0O ):#line:59
        return OOO0OO000OO0OOO0O .version_string #line:60
    def _print_disclaimer (O00000000OOO0OOO0 ):#line:62
        print ("***********************************************************************************************************************************************************************")#line:63
        print ("Cleverminer version ",O00000000OOO0OOO0 ._get_ver ())#line:64
        print ("IMPORTANT NOTE: this is preliminary development version of CleverMiner procedure. This procedure is under intensive development and early released for educational use,")#line:65
        print ("    so there is ABSOLUTELY no guarantee of results, possible gaps in functionality and no guarantee of keeping syntax and parameters as in current version.")#line:66
        print ("    (That means we need to tidy up and make proper design, input validation, documentation and instrumentation before launch)")#line:67
        print ("This version is for personal and educational use only.")#line:68
        print ("***********************************************************************************************************************************************************************")#line:69
    def _prep_data (OO0O00O0000OO00OO ,O0OO000O00O0O000O ):#line:71
        print ("Starting data preparation ...")#line:72
        OO0O00O0000OO00OO ._init_data ()#line:73
        OO0O00O0000OO00OO .stats ['start_prep_time']=time .time ()#line:74
        OO0O00O0000OO00OO .data ["rows_count"]=O0OO000O00O0O000O .shape [0 ]#line:75
        for OOOO0OOOO00O00OOO in O0OO000O00O0O000O .select_dtypes (exclude =['category']).columns :#line:76
            O0OO000O00O0O000O [OOOO0OOOO00O00OOO ]=O0OO000O00O0O000O [OOOO0OOOO00O00OOO ].apply (str )#line:77
        OO0O0O00O0O0000O0 =pd .DataFrame .from_records ([(OO0OO0O0000OO00OO ,O0OO000O00O0O000O [OO0OO0O0000OO00OO ].nunique ())for OO0OO0O0000OO00OO in O0OO000O00O0O000O .columns ],columns =['Column_Name','Num_Unique']).sort_values (by =['Num_Unique'])#line:79
        print ("Unique value counts are:")#line:80
        print (OO0O0O00O0O0000O0 )#line:81
        for OOOO0OOOO00O00OOO in O0OO000O00O0O000O .columns :#line:82
            if O0OO000O00O0O000O [OOOO0OOOO00O00OOO ].nunique ()<100 :#line:83
                O0OO000O00O0O000O [OOOO0OOOO00O00OOO ]=O0OO000O00O0O000O [OOOO0OOOO00O00OOO ].astype ('category')#line:84
            else :#line:85
                print (f"WARNING: attribute {OOOO0OOOO00O00OOO} has more than 100 values, will be ignored.")#line:86
                del O0OO000O00O0O000O [OOOO0OOOO00O00OOO ]#line:87
        print ("Encoding columns into bit-form...")#line:88
        O00OOOOO0O000OOO0 =0 #line:89
        O000OOO00O0O0O000 =0 #line:90
        for O000000O0O0O0OO0O in O0OO000O00O0O000O :#line:91
            print ('Column: '+O000000O0O0O0OO0O )#line:93
            OO0O00O0000OO00OO .data ["varname"].append (O000000O0O0O0OO0O )#line:94
            O000OO0000O00OO00 =pd .get_dummies (O0OO000O00O0O000O [O000000O0O0O0OO0O ])#line:95
            OO000O00O00OOOOOO =0 #line:96
            if (O0OO000O00O0O000O .dtypes [O000000O0O0O0OO0O ].name =='category'):#line:97
                OO000O00O00OOOOOO =1 #line:98
            OO0O00O0000OO00OO .data ["vtypes"].append (OO000O00O00OOOOOO )#line:99
            OOOOOOOOO00O00O00 =0 #line:102
            O000O0000OOO00OO0 =[]#line:103
            O0O0OOO0OO0OO00O0 =[]#line:104
            for O00000O0000O0O0O0 in O000OO0000O00OO00 :#line:106
                print ('....category : '+str (O00000O0000O0O0O0 )+" @ "+str (time .time ()))#line:108
                O000O0000OOO00OO0 .append (O00000O0000O0O0O0 )#line:109
                O000OO0O0000OOOOO =int (0 )#line:110
                OOOO0OOO000OO00O0 =O000OO0000O00OO00 [O00000O0000O0O0O0 ].values #line:111
                for OO0OO00OOOOOOO0O0 in range (OO0O00O0000OO00OO .data ["rows_count"]):#line:113
                    if OOOO0OOO000OO00O0 [OO0OO00OOOOOOO0O0 ]>0 :#line:114
                        O000OO0O0000OOOOO +=1 <<OO0OO00OOOOOOO0O0 #line:115
                O0O0OOO0OO0OO00O0 .append (O000OO0O0000OOOOO )#line:116
                OOOOOOOOO00O00O00 +=1 #line:126
                O000OOO00O0O0O000 +=1 #line:127
            OO0O00O0000OO00OO .data ["catnames"].append (O000O0000OOO00OO0 )#line:129
            OO0O00O0000OO00OO .data ["dm"].append (O0O0OOO0OO0OO00O0 )#line:130
        print ("Encoding columns into bit-form...done")#line:132
        print ("Encoding columns into bit-form...done")#line:133
        print (f"List of attributes for analysis is: {OO0O00O0000OO00OO.data['varname']}")#line:134
        print (f"List of category names for individual attributes is : {OO0O00O0000OO00OO.data['catnames']}")#line:135
        print (f"List of vtypes is (all should be 1) : {OO0O00O0000OO00OO.data['vtypes']}")#line:136
        OO0O00O0000OO00OO .data ["data_prepared"]=1 #line:138
        print ("Data preparation finished ...")#line:139
        print ('Number of variables : '+str (len (OO0O00O0000OO00OO .data ["dm"])))#line:140
        print ('Total number of categories in all variables : '+str (O000OOO00O0O0O000 ))#line:141
        OO0O00O0000OO00OO .stats ['end_prep_time']=time .time ()#line:142
        print ('Time needed for data preparation : ',str (OO0O00O0000OO00OO .stats ['end_prep_time']-OO0O00O0000OO00OO .stats ['start_prep_time']))#line:143
    def bitcount (OOO0O00O0OO000OO0 ,O000OO0O000OO0OOO ):#line:146
        O00OOOOOO0O00OOO0 =0 #line:147
        while O000OO0O000OO0OOO >0 :#line:148
            if (O000OO0O000OO0OOO &1 ==1 ):O00OOOOOO0O00OOO0 +=1 #line:149
            O000OO0O000OO0OOO >>=1 #line:150
        return O00OOOOOO0O00OOO0 #line:151
    def _verifyCF (OO00000O000O00000 ,_OO0OOOO000OOOOOOO ):#line:154
        OO0OOOO0O0OO00O00 =bin (_OO0OOOO000OOOOOOO ).count ("1")#line:155
        O0OO0O000O0OOOOO0 =[]#line:156
        O00O00O0O0O0OOO00 =[]#line:157
        O0000000O0O00OO00 =0 #line:158
        O0OO000OO0OOOO00O =0 #line:159
        OOO0000O0OO0OOO00 =0 #line:160
        O0O00O0O0OOOOO00O =0 #line:161
        O0O0OO0O0O00OOOO0 =0 #line:162
        OO0O0O0OO0OOOOO00 =0 #line:163
        O000OOO00OOO0O00O =0 #line:164
        O0000O0OOO0OO0000 =0 #line:165
        OOO0OOO0OOO00O000 =0 #line:166
        OOOO0OO0O0OO00O0O =OO00000O000O00000 .data ["dm"][OO00000O000O00000 .data ["varname"].index (OO00000O000O00000 .kwargs .get ('target'))]#line:167
        for OOO00O0O00O0O0O00 in range (len (OOOO0OO0O0OO00O0O )):#line:168
            O0OO000OO0OOOO00O =O0000000O0O00OO00 #line:169
            O0000000O0O00OO00 =bin (_OO0OOOO000OOOOOOO &OOOO0OO0O0OO00O0O [OOO00O0O00O0O0O00 ]).count ("1")#line:170
            O0OO0O000O0OOOOO0 .append (O0000000O0O00OO00 )#line:171
            if OOO00O0O00O0O0O00 >0 :#line:172
                if (O0000000O0O00OO00 >O0OO000OO0OOOO00O ):#line:173
                    if (OOO0000O0OO0OOO00 ==1 ):#line:174
                        O0000O0OOO0OO0000 +=1 #line:175
                    else :#line:176
                        O0000O0OOO0OO0000 =1 #line:177
                    if O0000O0OOO0OO0000 >O0O00O0O0OOOOO00O :#line:178
                        O0O00O0O0OOOOO00O =O0000O0OOO0OO0000 #line:179
                    OOO0000O0OO0OOO00 =1 #line:180
                    OO0O0O0OO0OOOOO00 +=1 #line:181
                if (O0000000O0O00OO00 <O0OO000OO0OOOO00O ):#line:182
                    if (OOO0000O0OO0OOO00 ==-1 ):#line:183
                        OOO0OOO0OOO00O000 +=1 #line:184
                    else :#line:185
                        OOO0OOO0OOO00O000 =1 #line:186
                    if OOO0OOO0OOO00O000 >O0O0OO0O0O00OOOO0 :#line:187
                        O0O0OO0O0O00OOOO0 =OOO0OOO0OOO00O000 #line:188
                    OOO0000O0OO0OOO00 =-1 #line:189
                    O000OOO00OOO0O00O +=1 #line:190
                if (O0000000O0O00OO00 ==O0OO000OO0OOOO00O ):#line:191
                    OOO0000O0OO0OOO00 =0 #line:192
                    OOO0OOO0OOO00O000 =0 #line:193
                    O0000O0OOO0OO0000 =0 #line:194
        O00O0000OOO00O00O =True #line:197
        for OO00000O0O0O00OO0 in OO00000O000O00000 .quantifiers .keys ():#line:198
            if OO00000O0O0O00OO0 .upper ()=='BASE':#line:199
                O00O0000OOO00O00O =O00O0000OOO00O00O and (OO00000O000O00000 .quantifiers .get (OO00000O0O0O00OO0 )<=OO0OOOO0O0OO00O00 )#line:200
            if OO00000O0O0O00OO0 .upper ()=='RELBASE':#line:201
                O00O0000OOO00O00O =O00O0000OOO00O00O and (OO00000O000O00000 .quantifiers .get (OO00000O0O0O00OO0 )<=OO0OOOO0O0OO00O00 *1.0 /OO00000O000O00000 .data ["rows_count"])#line:202
            if OO00000O0O0O00OO0 .upper ()=='S_UP':#line:203
                O00O0000OOO00O00O =O00O0000OOO00O00O and (OO00000O000O00000 .quantifiers .get (OO00000O0O0O00OO0 )<=O0O00O0O0OOOOO00O )#line:204
            if OO00000O0O0O00OO0 .upper ()=='S_DOWN':#line:205
                O00O0000OOO00O00O =O00O0000OOO00O00O and (OO00000O000O00000 .quantifiers .get (OO00000O0O0O00OO0 )<=O0O0OO0O0O00OOOO0 )#line:206
            if OO00000O0O0O00OO0 .upper ()=='S_ANY_UP':#line:207
                O00O0000OOO00O00O =O00O0000OOO00O00O and (OO00000O000O00000 .quantifiers .get (OO00000O0O0O00OO0 )<=O0O00O0O0OOOOO00O )#line:208
            if OO00000O0O0O00OO0 .upper ()=='S_ANY_DOWN':#line:209
                O00O0000OOO00O00O =O00O0000OOO00O00O and (OO00000O000O00000 .quantifiers .get (OO00000O0O0O00OO0 )<=O0O0OO0O0O00OOOO0 )#line:210
            if OO00000O0O0O00OO0 .upper ()=='MAX':#line:211
                O00O0000OOO00O00O =O00O0000OOO00O00O and (OO00000O000O00000 .quantifiers .get (OO00000O0O0O00OO0 )<=max (O0OO0O000O0OOOOO0 ))#line:212
            if OO00000O0O0O00OO0 .upper ()=='MIN':#line:213
                O00O0000OOO00O00O =O00O0000OOO00O00O and (OO00000O000O00000 .quantifiers .get (OO00000O0O0O00OO0 )<=min (O0OO0O000O0OOOOO0 ))#line:214
            if OO00000O0O0O00OO0 .upper ()=='RELMAX':#line:215
                if sum (O0OO0O000O0OOOOO0 )>0 :#line:216
                    O00O0000OOO00O00O =O00O0000OOO00O00O and (OO00000O000O00000 .quantifiers .get (OO00000O0O0O00OO0 )<=max (O0OO0O000O0OOOOO0 )*1.0 /sum (O0OO0O000O0OOOOO0 ))#line:217
                else :#line:218
                    O00O0000OOO00O00O =False #line:219
            if OO00000O0O0O00OO0 .upper ()=='RELMIN':#line:220
                if sum (O0OO0O000O0OOOOO0 )>0 :#line:221
                    O00O0000OOO00O00O =O00O0000OOO00O00O and (OO00000O000O00000 .quantifiers .get (OO00000O0O0O00OO0 )<=min (O0OO0O000O0OOOOO0 )*1.0 /sum (O0OO0O000O0OOOOO0 ))#line:222
                else :#line:223
                    O00O0000OOO00O00O =False #line:224
        O0OO0OOO0000OOO0O ={}#line:225
        if O00O0000OOO00O00O ==True :#line:226
            OO00000O000O00000 .stats ['total_valid']+=1 #line:228
            O0OO0OOO0000OOO0O ["base"]=OO0OOOO0O0OO00O00 #line:229
            O0OO0OOO0000OOO0O ["rel_base"]=OO0OOOO0O0OO00O00 *1.0 /OO00000O000O00000 .data ["rows_count"]#line:230
            O0OO0OOO0000OOO0O ["s_up"]=O0O00O0O0OOOOO00O #line:231
            O0OO0OOO0000OOO0O ["s_down"]=O0O0OO0O0O00OOOO0 #line:232
            O0OO0OOO0000OOO0O ["s_any_up"]=OO0O0O0OO0OOOOO00 #line:233
            O0OO0OOO0000OOO0O ["s_any_down"]=O000OOO00OOO0O00O #line:234
            O0OO0OOO0000OOO0O ["max"]=max (O0OO0O000O0OOOOO0 )#line:235
            O0OO0OOO0000OOO0O ["min"]=min (O0OO0O000O0OOOOO0 )#line:236
            O0OO0OOO0000OOO0O ["rel_max"]=max (O0OO0O000O0OOOOO0 )*1.0 /OO00000O000O00000 .data ["rows_count"]#line:237
            O0OO0OOO0000OOO0O ["rel_min"]=min (O0OO0O000O0OOOOO0 )*1.0 /OO00000O000O00000 .data ["rows_count"]#line:238
            O0OO0OOO0000OOO0O ["hist"]=O0OO0O000O0OOOOO0 #line:239
        return O00O0000OOO00O00O ,O0OO0OOO0000OOO0O #line:241
    def _verify4ft (O000O00OO0000OO0O ,_O000OO0O000OO00O0 ):#line:243
        O0000O0O0OOOO0O0O ={}#line:244
        OOOO000O000000000 =0 #line:245
        for O00O0OOOO0000O0OO in O000O00OO0000OO0O .task_actinfo ['cedents']:#line:246
            O0000O0O0OOOO0O0O [O00O0OOOO0000O0OO ['cedent_type']]=O00O0OOOO0000O0OO ['filter_value']#line:248
            OOOO000O000000000 =OOOO000O000000000 +1 #line:249
        OOO000OOO000OO000 =bin (O0000O0O0OOOO0O0O ['ante']&O0000O0O0OOOO0O0O ['succ']&O0000O0O0OOOO0O0O ['cond']).count ("1")#line:251
        O00O0O0O0O0OO0OOO =None #line:252
        O00O0O0O0O0OO0OOO =0 #line:253
        if OOO000OOO000OO000 >0 :#line:262
            O00O0O0O0O0OO0OOO =bin (O0000O0O0OOOO0O0O ['ante']&O0000O0O0OOOO0O0O ['succ']&O0000O0O0OOOO0O0O ['cond']).count ("1")*1.0 /bin (O0000O0O0OOOO0O0O ['ante']&O0000O0O0OOOO0O0O ['cond']).count ("1")#line:263
        OO00O00O0OOO000O0 =1 <<O000O00OO0000OO0O .data ["rows_count"]#line:265
        O0OO0O00O0O0O0O00 =bin (O0000O0O0OOOO0O0O ['ante']&O0000O0O0OOOO0O0O ['succ']&O0000O0O0OOOO0O0O ['cond']).count ("1")#line:266
        O0000O0O00OOOOOOO =bin (O0000O0O0OOOO0O0O ['ante']&~(OO00O00O0OOO000O0 |O0000O0O0OOOO0O0O ['succ'])&O0000O0O0OOOO0O0O ['cond']).count ("1")#line:267
        O00O0OOOO0000O0OO =bin (~(OO00O00O0OOO000O0 |O0000O0O0OOOO0O0O ['ante'])&O0000O0O0OOOO0O0O ['succ']&O0000O0O0OOOO0O0O ['cond']).count ("1")#line:268
        OOO0O0OO000O0O0OO =bin (~(OO00O00O0OOO000O0 |O0000O0O0OOOO0O0O ['ante'])&~(OO00O00O0OOO000O0 |O0000O0O0OOOO0O0O ['succ'])&O0000O0O0OOOO0O0O ['cond']).count ("1")#line:269
        O0OO00O0000O0O0O0 =0 #line:270
        if (O0OO0O00O0O0O0O00 +O0000O0O00OOOOOOO )*(O0OO0O00O0O0O0O00 +O00O0OOOO0000O0OO )>0 :#line:271
            O0OO00O0000O0O0O0 =O0OO0O00O0O0O0O00 *(O0OO0O00O0O0O0O00 +O0000O0O00OOOOOOO +O00O0OOOO0000O0OO +OOO0O0OO000O0O0OO )/(O0OO0O00O0O0O0O00 +O0000O0O00OOOOOOO )/(O0OO0O00O0O0O0O00 +O00O0OOOO0000O0OO )-1 #line:272
        else :#line:273
            O0OO00O0000O0O0O0 =None #line:274
        OOOOO0O0OO00O000O =0 #line:275
        if (O0OO0O00O0O0O0O00 +O0000O0O00OOOOOOO )*(O0OO0O00O0O0O0O00 +O00O0OOOO0000O0OO )>0 :#line:276
            OOOOO0O0OO00O000O =1 -O0OO0O00O0O0O0O00 *(O0OO0O00O0O0O0O00 +O0000O0O00OOOOOOO +O00O0OOOO0000O0OO +OOO0O0OO000O0O0OO )/(O0OO0O00O0O0O0O00 +O0000O0O00OOOOOOO )/(O0OO0O00O0O0O0O00 +O00O0OOOO0000O0OO )#line:277
        else :#line:278
            OOOOO0O0OO00O000O =None #line:279
        O0O00O0O00OO0O0O0 =True #line:280
        for OO0OO0OO0O0000000 in O000O00OO0000OO0O .quantifiers .keys ():#line:281
            if OO0OO0OO0O0000000 .upper ()=='BASE':#line:282
                O0O00O0O00OO0O0O0 =O0O00O0O00OO0O0O0 and (O000O00OO0000OO0O .quantifiers .get (OO0OO0OO0O0000000 )<=OOO000OOO000OO000 )#line:283
            if OO0OO0OO0O0000000 .upper ()=='RELBASE':#line:284
                O0O00O0O00OO0O0O0 =O0O00O0O00OO0O0O0 and (O000O00OO0000OO0O .quantifiers .get (OO0OO0OO0O0000000 )<=OOO000OOO000OO000 *1.0 /O000O00OO0000OO0O .data ["rows_count"])#line:285
            if (OO0OO0OO0O0000000 .upper ()=='PIM')or (OO0OO0OO0O0000000 .upper ()=='CONF'):#line:286
                O0O00O0O00OO0O0O0 =O0O00O0O00OO0O0O0 and (O000O00OO0000OO0O .quantifiers .get (OO0OO0OO0O0000000 )<=O00O0O0O0O0OO0OOO )#line:287
            if OO0OO0OO0O0000000 .upper ()=='AAD':#line:288
                if O0OO00O0000O0O0O0 !=None :#line:289
                    O0O00O0O00OO0O0O0 =O0O00O0O00OO0O0O0 and (O000O00OO0000OO0O .quantifiers .get (OO0OO0OO0O0000000 )<=O0OO00O0000O0O0O0 )#line:290
                else :#line:291
                    O0O00O0O00OO0O0O0 =False #line:292
            if OO0OO0OO0O0000000 .upper ()=='BAD':#line:293
                if OOOOO0O0OO00O000O !=None :#line:294
                    O0O00O0O00OO0O0O0 =O0O00O0O00OO0O0O0 and (O000O00OO0000OO0O .quantifiers .get (OO0OO0OO0O0000000 )<=OOOOO0O0OO00O000O )#line:295
                else :#line:296
                    O0O00O0O00OO0O0O0 =False #line:297
            O0O00O00O00OO000O ={}#line:298
        if O0O00O0O00OO0O0O0 ==True :#line:299
            O000O00OO0000OO0O .stats ['total_valid']+=1 #line:301
            O0O00O00O00OO000O ["base"]=OOO000OOO000OO000 #line:302
            O0O00O00O00OO000O ["rel_base"]=OOO000OOO000OO000 *1.0 /O000O00OO0000OO0O .data ["rows_count"]#line:303
            O0O00O00O00OO000O ["conf"]=O00O0O0O0O0OO0OOO #line:304
            O0O00O00O00OO000O ["aad"]=O0OO00O0000O0O0O0 #line:305
            O0O00O00O00OO000O ["bad"]=OOOOO0O0OO00O000O #line:306
            O0O00O00O00OO000O ["fourfold"]=[O0OO0O00O0O0O0O00 ,O0000O0O00OOOOOOO ,O00O0OOOO0000O0OO ,OOO0O0OO000O0O0OO ]#line:307
        return O0O00O0O00OO0O0O0 ,O0O00O00O00OO000O #line:311
    def _verifysd4ft (OO0OOO00O00000OOO ,_OOOO0OOO000O0O0OO ):#line:313
        OOOOO0OO0OOO0O0OO ={}#line:314
        O000000OO0O0O0000 =0 #line:315
        for OO00000O0OOO00O0O in OO0OOO00O00000OOO .task_actinfo ['cedents']:#line:316
            OOOOO0OO0OOO0O0OO [OO00000O0OOO00O0O ['cedent_type']]=OO00000O0OOO00O0O ['filter_value']#line:318
            O000000OO0O0O0000 =O000000OO0O0O0000 +1 #line:319
        OOO00O0OO000O0O00 =bin (OOOOO0OO0OOO0O0OO ['ante']&OOOOO0OO0OOO0O0OO ['succ']&OOOOO0OO0OOO0O0OO ['cond']&OOOOO0OO0OOO0O0OO ['frst']).count ("1")#line:321
        OO00O0O0OOOOOOO00 =bin (OOOOO0OO0OOO0O0OO ['ante']&OOOOO0OO0OOO0O0OO ['succ']&OOOOO0OO0OOO0O0OO ['cond']&OOOOO0OO0OOO0O0OO ['scnd']).count ("1")#line:322
        OOOOO0OOOO0000O00 =None #line:323
        OO0OOO0O0000000OO =0 #line:324
        O0O0OO0OO0OO0OOOO =0 #line:325
        if OOO00O0OO000O0O00 >0 :#line:334
            OO0OOO0O0000000OO =bin (OOOOO0OO0OOO0O0OO ['ante']&OOOOO0OO0OOO0O0OO ['succ']&OOOOO0OO0OOO0O0OO ['cond']&OOOOO0OO0OOO0O0OO ['frst']).count ("1")*1.0 /bin (OOOOO0OO0OOO0O0OO ['ante']&OOOOO0OO0OOO0O0OO ['cond']&OOOOO0OO0OOO0O0OO ['frst']).count ("1")#line:335
        if OO00O0O0OOOOOOO00 >0 :#line:336
            O0O0OO0OO0OO0OOOO =bin (OOOOO0OO0OOO0O0OO ['ante']&OOOOO0OO0OOO0O0OO ['succ']&OOOOO0OO0OOO0O0OO ['cond']&OOOOO0OO0OOO0O0OO ['scnd']).count ("1")*1.0 /bin (OOOOO0OO0OOO0O0OO ['ante']&OOOOO0OO0OOO0O0OO ['cond']&OOOOO0OO0OOO0O0OO ['scnd']).count ("1")#line:337
        OOOO000OO00OO0O0O =1 <<OO0OOO00O00000OOO .data ["rows_count"]#line:339
        OOO00OO0O0OOO00OO =bin (OOOOO0OO0OOO0O0OO ['ante']&OOOOO0OO0OOO0O0OO ['succ']&OOOOO0OO0OOO0O0OO ['cond']&OOOOO0OO0OOO0O0OO ['frst']).count ("1")#line:340
        O0OOOOO00O0OO0000 =bin (OOOOO0OO0OOO0O0OO ['ante']&~(OOOO000OO00OO0O0O |OOOOO0OO0OOO0O0OO ['succ'])&OOOOO0OO0OOO0O0OO ['cond']&OOOOO0OO0OOO0O0OO ['frst']).count ("1")#line:341
        O0O0O00OO0O00O000 =bin (~(OOOO000OO00OO0O0O |OOOOO0OO0OOO0O0OO ['ante'])&OOOOO0OO0OOO0O0OO ['succ']&OOOOO0OO0OOO0O0OO ['cond']&OOOOO0OO0OOO0O0OO ['frst']).count ("1")#line:342
        O000OOOOO00OO000O =bin (~(OOOO000OO00OO0O0O |OOOOO0OO0OOO0O0OO ['ante'])&~(OOOO000OO00OO0O0O |OOOOO0OO0OOO0O0OO ['succ'])&OOOOO0OO0OOO0O0OO ['cond']&OOOOO0OO0OOO0O0OO ['frst']).count ("1")#line:343
        O00OOOOOOOOO0000O =bin (OOOOO0OO0OOO0O0OO ['ante']&OOOOO0OO0OOO0O0OO ['succ']&OOOOO0OO0OOO0O0OO ['cond']&OOOOO0OO0OOO0O0OO ['scnd']).count ("1")#line:344
        OO00O0O0OOOO00O00 =bin (OOOOO0OO0OOO0O0OO ['ante']&~(OOOO000OO00OO0O0O |OOOOO0OO0OOO0O0OO ['succ'])&OOOOO0OO0OOO0O0OO ['cond']&OOOOO0OO0OOO0O0OO ['scnd']).count ("1")#line:345
        OOOO000O0O0OO0O0O =bin (~(OOOO000OO00OO0O0O |OOOOO0OO0OOO0O0OO ['ante'])&OOOOO0OO0OOO0O0OO ['succ']&OOOOO0OO0OOO0O0OO ['cond']&OOOOO0OO0OOO0O0OO ['scnd']).count ("1")#line:346
        OO000OOO0O0O0OOOO =bin (~(OOOO000OO00OO0O0O |OOOOO0OO0OOO0O0OO ['ante'])&~(OOOO000OO00OO0O0O |OOOOO0OO0OOO0O0OO ['succ'])&OOOOO0OO0OOO0O0OO ['cond']&OOOOO0OO0OOO0O0OO ['scnd']).count ("1")#line:347
        O0OOOO0O0OO00000O =True #line:348
        for OO0OOOOO0O000OO0O in OO0OOO00O00000OOO .quantifiers .keys ():#line:349
            if (OO0OOOOO0O000OO0O .upper ()=='FRSTBASE')|(OO0OOOOO0O000OO0O .upper ()=='BASE1'):#line:350
                O0OOOO0O0OO00000O =O0OOOO0O0OO00000O and (OO0OOO00O00000OOO .quantifiers .get (OO0OOOOO0O000OO0O )<=OOO00O0OO000O0O00 )#line:351
            if (OO0OOOOO0O000OO0O .upper ()=='SCNDBASE')|(OO0OOOOO0O000OO0O .upper ()=='BASE2'):#line:352
                O0OOOO0O0OO00000O =O0OOOO0O0OO00000O and (OO0OOO00O00000OOO .quantifiers .get (OO0OOOOO0O000OO0O )<=OO00O0O0OOOOOOO00 )#line:353
            if (OO0OOOOO0O000OO0O .upper ()=='FRSTRELBASE')|(OO0OOOOO0O000OO0O .upper ()=='RELBASE1'):#line:354
                O0OOOO0O0OO00000O =O0OOOO0O0OO00000O and (OO0OOO00O00000OOO .quantifiers .get (OO0OOOOO0O000OO0O )<=OOO00O0OO000O0O00 *1.0 /OO0OOO00O00000OOO .data ["rows_count"])#line:355
            if (OO0OOOOO0O000OO0O .upper ()=='SCNDRELBASE')|(OO0OOOOO0O000OO0O .upper ()=='RELBASE2'):#line:356
                O0OOOO0O0OO00000O =O0OOOO0O0OO00000O and (OO0OOO00O00000OOO .quantifiers .get (OO0OOOOO0O000OO0O )<=OO00O0O0OOOOOOO00 *1.0 /OO0OOO00O00000OOO .data ["rows_count"])#line:357
            if (OO0OOOOO0O000OO0O .upper ()=='FRSTPIM')|(OO0OOOOO0O000OO0O .upper ()=='PIM1')|(OO0OOOOO0O000OO0O .upper ()=='FRSTCONF')|(OO0OOOOO0O000OO0O .upper ()=='CONF1'):#line:358
                O0OOOO0O0OO00000O =O0OOOO0O0OO00000O and (OO0OOO00O00000OOO .quantifiers .get (OO0OOOOO0O000OO0O )<=OO0OOO0O0000000OO )#line:359
            if (OO0OOOOO0O000OO0O .upper ()=='SCNDPIM')|(OO0OOOOO0O000OO0O .upper ()=='PIM2')|(OO0OOOOO0O000OO0O .upper ()=='SCNDCONF')|(OO0OOOOO0O000OO0O .upper ()=='CONF2'):#line:360
                O0OOOO0O0OO00000O =O0OOOO0O0OO00000O and (OO0OOO00O00000OOO .quantifiers .get (OO0OOOOO0O000OO0O )<=O0O0OO0OO0OO0OOOO )#line:361
            if (OO0OOOOO0O000OO0O .upper ()=='DELTAPIM')|(OO0OOOOO0O000OO0O .upper ()=='DELTACONF'):#line:362
                O0OOOO0O0OO00000O =O0OOOO0O0OO00000O and (OO0OOO00O00000OOO .quantifiers .get (OO0OOOOO0O000OO0O )<=OO0OOO0O0000000OO -O0O0OO0OO0OO0OOOO )#line:363
            if (OO0OOOOO0O000OO0O .upper ()=='RATIOPIM')|(OO0OOOOO0O000OO0O .upper ()=='RATIOCONF'):#line:366
                if (O0O0OO0OO0OO0OOOO >0 ):#line:367
                    O0OOOO0O0OO00000O =O0OOOO0O0OO00000O and (OO0OOO00O00000OOO .quantifiers .get (OO0OOOOO0O000OO0O )<=OO0OOO0O0000000OO *1.0 /O0O0OO0OO0OO0OOOO )#line:368
                else :#line:369
                    O0OOOO0O0OO00000O =False #line:370
        OO0OOOO0O0000O000 ={}#line:371
        if O0OOOO0O0OO00000O ==True :#line:372
            OO0OOO00O00000OOO .stats ['total_valid']+=1 #line:374
            OO0OOOO0O0000O000 ["base1"]=OOO00O0OO000O0O00 #line:375
            OO0OOOO0O0000O000 ["base2"]=OO00O0O0OOOOOOO00 #line:376
            OO0OOOO0O0000O000 ["rel_base1"]=OOO00O0OO000O0O00 *1.0 /OO0OOO00O00000OOO .data ["rows_count"]#line:377
            OO0OOOO0O0000O000 ["rel_base2"]=OO00O0O0OOOOOOO00 *1.0 /OO0OOO00O00000OOO .data ["rows_count"]#line:378
            OO0OOOO0O0000O000 ["conf1"]=OO0OOO0O0000000OO #line:379
            OO0OOOO0O0000O000 ["conf2"]=O0O0OO0OO0OO0OOOO #line:380
            OO0OOOO0O0000O000 ["deltaconf"]=OO0OOO0O0000000OO -O0O0OO0OO0OO0OOOO #line:381
            if (O0O0OO0OO0OO0OOOO >0 ):#line:382
                OO0OOOO0O0000O000 ["ratioconf"]=OO0OOO0O0000000OO *1.0 /O0O0OO0OO0OO0OOOO #line:383
            else :#line:384
                OO0OOOO0O0000O000 ["ratioconf"]=None #line:385
            OO0OOOO0O0000O000 ["fourfold1"]=[OOO00OO0O0OOO00OO ,O0OOOOO00O0OO0000 ,O0O0O00OO0O00O000 ,O000OOOOO00OO000O ]#line:386
            OO0OOOO0O0000O000 ["fourfold2"]=[O00OOOOOOOOO0000O ,OO00O0O0OOOO00O00 ,OOOO000O0O0OO0O0O ,OO000OOO0O0O0OOOO ]#line:387
        return O0OOOO0O0OO00000O ,OO0OOOO0O0000O000 #line:391
    def _verifynewact4ft (OOO000000OOO0OOO0 ,_O00O0OO000OOOO00O ):#line:393
        OOOOOO00OO0O0OOO0 ={}#line:394
        for O0O0O0O0O0O0O0OO0 in OOO000000OOO0OOO0 .task_actinfo ['cedents']:#line:395
            OOOOOO00OO0O0OOO0 [O0O0O0O0O0O0O0OO0 ['cedent_type']]=O0O0O0O0O0O0O0OO0 ['filter_value']#line:397
        OOO00OO0O000O00O0 =bin (OOOOOO00OO0O0OOO0 ['ante']&OOOOOO00OO0O0OOO0 ['succ']&OOOOOO00OO0O0OOO0 ['cond']).count ("1")#line:399
        OO0O000OO0OO00000 =bin (OOOOOO00OO0O0OOO0 ['ante']&OOOOOO00OO0O0OOO0 ['succ']&OOOOOO00OO0O0OOO0 ['cond']&OOOOOO00OO0O0OOO0 ['antv']&OOOOOO00OO0O0OOO0 ['sucv']).count ("1")#line:400
        O00000O00O0OOOO0O =None #line:401
        O0OOO00000O0O0000 =0 #line:402
        O0O0O0000O00OO0O0 =0 #line:403
        if OOO00OO0O000O00O0 >0 :#line:412
            O0OOO00000O0O0000 =bin (OOOOOO00OO0O0OOO0 ['ante']&OOOOOO00OO0O0OOO0 ['succ']&OOOOOO00OO0O0OOO0 ['cond']).count ("1")*1.0 /bin (OOOOOO00OO0O0OOO0 ['ante']&OOOOOO00OO0O0OOO0 ['cond']).count ("1")#line:414
        if OO0O000OO0OO00000 >0 :#line:415
            O0O0O0000O00OO0O0 =bin (OOOOOO00OO0O0OOO0 ['ante']&OOOOOO00OO0O0OOO0 ['succ']&OOOOOO00OO0O0OOO0 ['cond']&OOOOOO00OO0O0OOO0 ['antv']&OOOOOO00OO0O0OOO0 ['sucv']).count ("1")*1.0 /bin (OOOOOO00OO0O0OOO0 ['ante']&OOOOOO00OO0O0OOO0 ['cond']&OOOOOO00OO0O0OOO0 ['antv']).count ("1")#line:417
        O000O0O0000OO0O0O =1 <<OOO000000OOO0OOO0 .rows_count #line:419
        O0O0OO00OOO0000O0 =bin (OOOOOO00OO0O0OOO0 ['ante']&OOOOOO00OO0O0OOO0 ['succ']&OOOOOO00OO0O0OOO0 ['cond']).count ("1")#line:420
        O00OO0000OOOOOO0O =bin (OOOOOO00OO0O0OOO0 ['ante']&~(O000O0O0000OO0O0O |OOOOOO00OO0O0OOO0 ['succ'])&OOOOOO00OO0O0OOO0 ['cond']).count ("1")#line:421
        OO000O00OOO000OO0 =bin (~(O000O0O0000OO0O0O |OOOOOO00OO0O0OOO0 ['ante'])&OOOOOO00OO0O0OOO0 ['succ']&OOOOOO00OO0O0OOO0 ['cond']).count ("1")#line:422
        O0O00O0OOOO0OOO0O =bin (~(O000O0O0000OO0O0O |OOOOOO00OO0O0OOO0 ['ante'])&~(O000O0O0000OO0O0O |OOOOOO00OO0O0OOO0 ['succ'])&OOOOOO00OO0O0OOO0 ['cond']).count ("1")#line:423
        OO0O0O000O00O0O00 =bin (OOOOOO00OO0O0OOO0 ['ante']&OOOOOO00OO0O0OOO0 ['succ']&OOOOOO00OO0O0OOO0 ['cond']&OOOOOO00OO0O0OOO0 ['antv']&OOOOOO00OO0O0OOO0 ['sucv']).count ("1")#line:424
        O00O0OO000O0OOO00 =bin (OOOOOO00OO0O0OOO0 ['ante']&~(O000O0O0000OO0O0O |(OOOOOO00OO0O0OOO0 ['succ']&OOOOOO00OO0O0OOO0 ['sucv']))&OOOOOO00OO0O0OOO0 ['cond']).count ("1")#line:425
        O00OO0O0OOOOO0000 =bin (~(O000O0O0000OO0O0O |(OOOOOO00OO0O0OOO0 ['ante']&OOOOOO00OO0O0OOO0 ['antv']))&OOOOOO00OO0O0OOO0 ['succ']&OOOOOO00OO0O0OOO0 ['cond']&OOOOOO00OO0O0OOO0 ['sucv']).count ("1")#line:426
        OOOO00OO0O00O00OO =bin (~(O000O0O0000OO0O0O |(OOOOOO00OO0O0OOO0 ['ante']&OOOOOO00OO0O0OOO0 ['antv']))&~(O000O0O0000OO0O0O |(OOOOOO00OO0O0OOO0 ['succ']&OOOOOO00OO0O0OOO0 ['sucv']))&OOOOOO00OO0O0OOO0 ['cond']).count ("1")#line:427
        OO0O0O00000O00O00 =True #line:428
        for OO0000O0000OOO000 in OOO000000OOO0OOO0 .quantifiers .keys ():#line:429
            if (OO0000O0000OOO000 =='PreBase')|(OO0000O0000OOO000 =='Base1'):#line:430
                OO0O0O00000O00O00 =OO0O0O00000O00O00 and (OOO000000OOO0OOO0 .quantifiers .get (OO0000O0000OOO000 )<=OOO00OO0O000O00O0 )#line:431
            if (OO0000O0000OOO000 =='PostBase')|(OO0000O0000OOO000 =='Base2'):#line:432
                OO0O0O00000O00O00 =OO0O0O00000O00O00 and (OOO000000OOO0OOO0 .quantifiers .get (OO0000O0000OOO000 )<=OO0O000OO0OO00000 )#line:433
            if (OO0000O0000OOO000 =='PreRelBase')|(OO0000O0000OOO000 =='RelBase1'):#line:434
                OO0O0O00000O00O00 =OO0O0O00000O00O00 and (OOO000000OOO0OOO0 .quantifiers .get (OO0000O0000OOO000 )<=OOO00OO0O000O00O0 *1.0 /OOO000000OOO0OOO0 .data ["rows_count"])#line:435
            if (OO0000O0000OOO000 =='PostRelBase')|(OO0000O0000OOO000 =='RelBase2'):#line:436
                OO0O0O00000O00O00 =OO0O0O00000O00O00 and (OOO000000OOO0OOO0 .quantifiers .get (OO0000O0000OOO000 )<=OO0O000OO0OO00000 *1.0 /OOO000000OOO0OOO0 .data ["rows_count"])#line:437
            if (OO0000O0000OOO000 =='Prepim')|(OO0000O0000OOO000 =='pim1')|(OO0000O0000OOO000 =='PreConf')|(OO0000O0000OOO000 =='conf1'):#line:438
                OO0O0O00000O00O00 =OO0O0O00000O00O00 and (OOO000000OOO0OOO0 .quantifiers .get (OO0000O0000OOO000 )<=O0OOO00000O0O0000 )#line:439
            if (OO0000O0000OOO000 =='Postpim')|(OO0000O0000OOO000 =='pim2')|(OO0000O0000OOO000 =='PostConf')|(OO0000O0000OOO000 =='conf2'):#line:440
                OO0O0O00000O00O00 =OO0O0O00000O00O00 and (OOO000000OOO0OOO0 .quantifiers .get (OO0000O0000OOO000 )<=O0O0O0000O00OO0O0 )#line:441
            if (OO0000O0000OOO000 =='Deltapim')|(OO0000O0000OOO000 =='DeltaConf'):#line:442
                OO0O0O00000O00O00 =OO0O0O00000O00O00 and (OOO000000OOO0OOO0 .quantifiers .get (OO0000O0000OOO000 )<=O0OOO00000O0O0000 -O0O0O0000O00OO0O0 )#line:443
            if (OO0000O0000OOO000 =='Ratiopim')|(OO0000O0000OOO000 =='RatioConf'):#line:446
                if (O0O0O0000O00OO0O0 >0 ):#line:447
                    OO0O0O00000O00O00 =OO0O0O00000O00O00 and (OOO000000OOO0OOO0 .quantifiers .get (OO0000O0000OOO000 )<=O0OOO00000O0O0000 *1.0 /O0O0O0000O00OO0O0 )#line:448
                else :#line:449
                    OO0O0O00000O00O00 =False #line:450
        OOO0O0OO0OO0OOOOO ={}#line:451
        if OO0O0O00000O00O00 ==True :#line:452
            OOO000000OOO0OOO0 .stats ['total_valid']+=1 #line:454
            OOO0O0OO0OO0OOOOO ["base1"]=OOO00OO0O000O00O0 #line:455
            OOO0O0OO0OO0OOOOO ["base2"]=OO0O000OO0OO00000 #line:456
            OOO0O0OO0OO0OOOOO ["rel_base1"]=OOO00OO0O000O00O0 *1.0 /OOO000000OOO0OOO0 .data ["rows_count"]#line:457
            OOO0O0OO0OO0OOOOO ["rel_base2"]=OO0O000OO0OO00000 *1.0 /OOO000000OOO0OOO0 .data ["rows_count"]#line:458
            OOO0O0OO0OO0OOOOO ["conf1"]=O0OOO00000O0O0000 #line:459
            OOO0O0OO0OO0OOOOO ["conf2"]=O0O0O0000O00OO0O0 #line:460
            OOO0O0OO0OO0OOOOO ["deltaconf"]=O0OOO00000O0O0000 -O0O0O0000O00OO0O0 #line:461
            if (O0O0O0000O00OO0O0 >0 ):#line:462
                OOO0O0OO0OO0OOOOO ["ratioconf"]=O0OOO00000O0O0000 *1.0 /O0O0O0000O00OO0O0 #line:463
            else :#line:464
                OOO0O0OO0OO0OOOOO ["ratioconf"]=None #line:465
            OOO0O0OO0OO0OOOOO ["fourfoldpre"]=[O0O0OO00OOO0000O0 ,O00OO0000OOOOOO0O ,OO000O00OOO000OO0 ,O0O00O0OOOO0OOO0O ]#line:466
            OOO0O0OO0OO0OOOOO ["fourfoldpost"]=[OO0O0O000O00O0O00 ,O00O0OO000O0OOO00 ,O00OO0O0OOOOO0000 ,OOOO00OO0O00O00OO ]#line:467
        return OO0O0O00000O00O00 ,OOO0O0OO0OO0OOOOO #line:469
    def _verifyact4ft (O00OO0OOOOOOOO000 ,_O00O000O000O0O0OO ):#line:471
        OOO00OO0OO0O0OOO0 ={}#line:472
        for O00OOOO0O0OO00O0O in O00OO0OOOOOOOO000 .task_actinfo ['cedents']:#line:473
            OOO00OO0OO0O0OOO0 [O00OOOO0O0OO00O0O ['cedent_type']]=O00OOOO0O0OO00O0O ['filter_value']#line:475
        OO00O0OO000000O00 =bin (OOO00OO0OO0O0OOO0 ['ante']&OOO00OO0OO0O0OOO0 ['succ']&OOO00OO0OO0O0OOO0 ['cond']&OOO00OO0OO0O0OOO0 ['antv-']&OOO00OO0OO0O0OOO0 ['sucv-']).count ("1")#line:477
        O0O0OOO0000OO0O0O =bin (OOO00OO0OO0O0OOO0 ['ante']&OOO00OO0OO0O0OOO0 ['succ']&OOO00OO0OO0O0OOO0 ['cond']&OOO00OO0OO0O0OOO0 ['antv+']&OOO00OO0OO0O0OOO0 ['sucv+']).count ("1")#line:478
        OOOOO0O0O0000O00O =None #line:479
        O00000OOO000OOO0O =0 #line:480
        OO0O0O0OO0O0O0OOO =0 #line:481
        if OO00O0OO000000O00 >0 :#line:490
            O00000OOO000OOO0O =bin (OOO00OO0OO0O0OOO0 ['ante']&OOO00OO0OO0O0OOO0 ['succ']&OOO00OO0OO0O0OOO0 ['cond']&OOO00OO0OO0O0OOO0 ['antv-']&OOO00OO0OO0O0OOO0 ['sucv-']).count ("1")*1.0 /bin (OOO00OO0OO0O0OOO0 ['ante']&OOO00OO0OO0O0OOO0 ['cond']&OOO00OO0OO0O0OOO0 ['antv-']).count ("1")#line:492
        if O0O0OOO0000OO0O0O >0 :#line:493
            OO0O0O0OO0O0O0OOO =bin (OOO00OO0OO0O0OOO0 ['ante']&OOO00OO0OO0O0OOO0 ['succ']&OOO00OO0OO0O0OOO0 ['cond']&OOO00OO0OO0O0OOO0 ['antv+']&OOO00OO0OO0O0OOO0 ['sucv+']).count ("1")*1.0 /bin (OOO00OO0OO0O0OOO0 ['ante']&OOO00OO0OO0O0OOO0 ['cond']&OOO00OO0OO0O0OOO0 ['antv+']).count ("1")#line:495
        OOO0O0OO0O0O0OOO0 =1 <<O00OO0OOOOOOOO000 .data ["rows_count"]#line:497
        O0OO0O0O0O0O00OO0 =bin (OOO00OO0OO0O0OOO0 ['ante']&OOO00OO0OO0O0OOO0 ['succ']&OOO00OO0OO0O0OOO0 ['cond']&OOO00OO0OO0O0OOO0 ['antv-']&OOO00OO0OO0O0OOO0 ['sucv-']).count ("1")#line:498
        O0OOOO000O0O0O000 =bin (OOO00OO0OO0O0OOO0 ['ante']&OOO00OO0OO0O0OOO0 ['antv-']&~(OOO0O0OO0O0O0OOO0 |(OOO00OO0OO0O0OOO0 ['succ']&OOO00OO0OO0O0OOO0 ['sucv-']))&OOO00OO0OO0O0OOO0 ['cond']).count ("1")#line:499
        O0OOO0000000O0O00 =bin (~(OOO0O0OO0O0O0OOO0 |(OOO00OO0OO0O0OOO0 ['ante']&OOO00OO0OO0O0OOO0 ['antv-']))&OOO00OO0OO0O0OOO0 ['succ']&OOO00OO0OO0O0OOO0 ['cond']&OOO00OO0OO0O0OOO0 ['sucv-']).count ("1")#line:500
        OO0O000O000OO00O0 =bin (~(OOO0O0OO0O0O0OOO0 |(OOO00OO0OO0O0OOO0 ['ante']&OOO00OO0OO0O0OOO0 ['antv-']))&~(OOO0O0OO0O0O0OOO0 |(OOO00OO0OO0O0OOO0 ['succ']&OOO00OO0OO0O0OOO0 ['sucv-']))&OOO00OO0OO0O0OOO0 ['cond']).count ("1")#line:501
        OO0OO000O000O0OO0 =bin (OOO00OO0OO0O0OOO0 ['ante']&OOO00OO0OO0O0OOO0 ['succ']&OOO00OO0OO0O0OOO0 ['cond']&OOO00OO0OO0O0OOO0 ['antv+']&OOO00OO0OO0O0OOO0 ['sucv+']).count ("1")#line:502
        OOOO0O00000OO0O0O =bin (OOO00OO0OO0O0OOO0 ['ante']&OOO00OO0OO0O0OOO0 ['antv+']&~(OOO0O0OO0O0O0OOO0 |(OOO00OO0OO0O0OOO0 ['succ']&OOO00OO0OO0O0OOO0 ['sucv+']))&OOO00OO0OO0O0OOO0 ['cond']).count ("1")#line:503
        O00OOOO0O0O000OO0 =bin (~(OOO0O0OO0O0O0OOO0 |(OOO00OO0OO0O0OOO0 ['ante']&OOO00OO0OO0O0OOO0 ['antv+']))&OOO00OO0OO0O0OOO0 ['succ']&OOO00OO0OO0O0OOO0 ['cond']&OOO00OO0OO0O0OOO0 ['sucv+']).count ("1")#line:504
        O0O0OOO0OOOOOO0OO =bin (~(OOO0O0OO0O0O0OOO0 |(OOO00OO0OO0O0OOO0 ['ante']&OOO00OO0OO0O0OOO0 ['antv+']))&~(OOO0O0OO0O0O0OOO0 |(OOO00OO0OO0O0OOO0 ['succ']&OOO00OO0OO0O0OOO0 ['sucv+']))&OOO00OO0OO0O0OOO0 ['cond']).count ("1")#line:505
        O00OOOO0000O0000O =True #line:506
        for OOO0O0OOO0O000O0O in O00OO0OOOOOOOO000 .quantifiers .keys ():#line:507
            if (OOO0O0OOO0O000O0O =='PreBase')|(OOO0O0OOO0O000O0O =='Base1'):#line:508
                O00OOOO0000O0000O =O00OOOO0000O0000O and (O00OO0OOOOOOOO000 .quantifiers .get (OOO0O0OOO0O000O0O )<=OO00O0OO000000O00 )#line:509
            if (OOO0O0OOO0O000O0O =='PostBase')|(OOO0O0OOO0O000O0O =='Base2'):#line:510
                O00OOOO0000O0000O =O00OOOO0000O0000O and (O00OO0OOOOOOOO000 .quantifiers .get (OOO0O0OOO0O000O0O )<=O0O0OOO0000OO0O0O )#line:511
            if (OOO0O0OOO0O000O0O =='PreRelBase')|(OOO0O0OOO0O000O0O =='RelBase1'):#line:512
                O00OOOO0000O0000O =O00OOOO0000O0000O and (O00OO0OOOOOOOO000 .quantifiers .get (OOO0O0OOO0O000O0O )<=OO00O0OO000000O00 *1.0 /O00OO0OOOOOOOO000 .data ["rows_count"])#line:513
            if (OOO0O0OOO0O000O0O =='PostRelBase')|(OOO0O0OOO0O000O0O =='RelBase2'):#line:514
                O00OOOO0000O0000O =O00OOOO0000O0000O and (O00OO0OOOOOOOO000 .quantifiers .get (OOO0O0OOO0O000O0O )<=O0O0OOO0000OO0O0O *1.0 /O00OO0OOOOOOOO000 .data ["rows_count"])#line:515
            if (OOO0O0OOO0O000O0O =='Prepim')|(OOO0O0OOO0O000O0O =='pim1')|(OOO0O0OOO0O000O0O =='PreConf')|(OOO0O0OOO0O000O0O =='conf1'):#line:516
                O00OOOO0000O0000O =O00OOOO0000O0000O and (O00OO0OOOOOOOO000 .quantifiers .get (OOO0O0OOO0O000O0O )<=O00000OOO000OOO0O )#line:517
            if (OOO0O0OOO0O000O0O =='Postpim')|(OOO0O0OOO0O000O0O =='pim2')|(OOO0O0OOO0O000O0O =='PostConf')|(OOO0O0OOO0O000O0O =='conf2'):#line:518
                O00OOOO0000O0000O =O00OOOO0000O0000O and (O00OO0OOOOOOOO000 .quantifiers .get (OOO0O0OOO0O000O0O )<=OO0O0O0OO0O0O0OOO )#line:519
            if (OOO0O0OOO0O000O0O =='Deltapim')|(OOO0O0OOO0O000O0O =='DeltaConf'):#line:520
                O00OOOO0000O0000O =O00OOOO0000O0000O and (O00OO0OOOOOOOO000 .quantifiers .get (OOO0O0OOO0O000O0O )<=O00000OOO000OOO0O -OO0O0O0OO0O0O0OOO )#line:521
            if (OOO0O0OOO0O000O0O =='Ratiopim')|(OOO0O0OOO0O000O0O =='RatioConf'):#line:524
                if (O00000OOO000OOO0O >0 ):#line:525
                    O00OOOO0000O0000O =O00OOOO0000O0000O and (O00OO0OOOOOOOO000 .quantifiers .get (OOO0O0OOO0O000O0O )<=OO0O0O0OO0O0O0OOO *1.0 /O00000OOO000OOO0O )#line:526
                else :#line:527
                    O00OOOO0000O0000O =False #line:528
        OOO0OOOOO000O00OO ={}#line:529
        if O00OOOO0000O0000O ==True :#line:530
            O00OO0OOOOOOOO000 .stats ['total_valid']+=1 #line:532
            OOO0OOOOO000O00OO ["base1"]=OO00O0OO000000O00 #line:533
            OOO0OOOOO000O00OO ["base2"]=O0O0OOO0000OO0O0O #line:534
            OOO0OOOOO000O00OO ["rel_base1"]=OO00O0OO000000O00 *1.0 /O00OO0OOOOOOOO000 .data ["rows_count"]#line:535
            OOO0OOOOO000O00OO ["rel_base2"]=O0O0OOO0000OO0O0O *1.0 /O00OO0OOOOOOOO000 .data ["rows_count"]#line:536
            OOO0OOOOO000O00OO ["conf1"]=O00000OOO000OOO0O #line:537
            OOO0OOOOO000O00OO ["conf2"]=OO0O0O0OO0O0O0OOO #line:538
            OOO0OOOOO000O00OO ["deltaconf"]=O00000OOO000OOO0O -OO0O0O0OO0O0O0OOO #line:539
            if (O00000OOO000OOO0O >0 ):#line:540
                OOO0OOOOO000O00OO ["ratioconf"]=OO0O0O0OO0O0O0OOO *1.0 /O00000OOO000OOO0O #line:541
            else :#line:542
                OOO0OOOOO000O00OO ["ratioconf"]=None #line:543
            OOO0OOOOO000O00OO ["fourfoldpre"]=[O0OO0O0O0O0O00OO0 ,O0OOOO000O0O0O000 ,O0OOO0000000O0O00 ,OO0O000O000OO00O0 ]#line:544
            OOO0OOOOO000O00OO ["fourfoldpost"]=[OO0OO000O000O0OO0 ,OOOO0O00000OO0O0O ,O00OOOO0O0O000OO0 ,O0O0OOO0OOOOOO0OO ]#line:545
        return O00OOOO0000O0000O ,OOO0OOOOO000O00OO #line:547
    def _verify_opt (O00O0000O0OO00O0O ,O000OO00O000O00OO ,O0O000O000OO0O0OO ):#line:549
        OOOOOO000OOOOO000 =False #line:550
        if not (O000OO00O000O00OO ['optim'].get ('only_con')):#line:553
            return False #line:554
        O0O0OO000O000000O ={}#line:555
        for OOO0OO0O0O0OO0O0O in O00O0000O0OO00O0O .task_actinfo ['cedents']:#line:556
            O0O0OO000O000000O [OOO0OO0O0O0OO0O0O ['cedent_type']]=OOO0OO0O0O0OO0O0O ['filter_value']#line:558
        O0OO0OO0O0000OOOO =1 <<O00O0000O0OO00O0O .data ["rows_count"]#line:560
        OO00OOOOOO0OO0O00 =O0OO0OO0O0000OOOO -1 #line:561
        O0O0O0OOO00O00O0O =""#line:562
        O0OO00OOOOOOO0O0O =0 #line:563
        if (O0O0OO000O000000O .get ('ante')!=None ):#line:564
            OO00OOOOOO0OO0O00 =OO00OOOOOO0OO0O00 &O0O0OO000O000000O ['ante']#line:565
        if (O0O0OO000O000000O .get ('succ')!=None ):#line:566
            OO00OOOOOO0OO0O00 =OO00OOOOOO0OO0O00 &O0O0OO000O000000O ['succ']#line:567
        if (O0O0OO000O000000O .get ('cond')!=None ):#line:568
            OO00OOOOOO0OO0O00 =OO00OOOOOO0OO0O00 &O0O0OO000O000000O ['cond']#line:569
        OOOOO0O0O00O0O000 =None #line:572
        if (O00O0000O0OO00O0O .proc =='CFMiner')|(O00O0000O0OO00O0O .proc =='4ftMiner'):#line:597
            OO000O0OO0000OOOO =bin (OO00OOOOOO0OO0O00 ).count ("1")#line:598
            for OO00000O0O0O0O00O in O00O0000O0OO00O0O .quantifiers .keys ():#line:599
                if OO00000O0O0O0O00O =='Base':#line:600
                    if not (O00O0000O0OO00O0O .quantifiers .get (OO00000O0O0O0O00O )<=OO000O0OO0000OOOO ):#line:601
                        OOOOOO000OOOOO000 =True #line:602
                if OO00000O0O0O0O00O =='RelBase':#line:604
                    if not (O00O0000O0OO00O0O .quantifiers .get (OO00000O0O0O0O00O )<=OO000O0OO0000OOOO *1.0 /O00O0000O0OO00O0O .data ["rows_count"]):#line:605
                        OOOOOO000OOOOO000 =True #line:606
        return OOOOOO000OOOOO000 #line:609
        if O00O0000O0OO00O0O .proc =='CFMiner':#line:612
            if (O0O000O000OO0O0OO ['cedent_type']=='cond')&(O0O000O000OO0O0OO ['defi'].get ('type')=='con'):#line:613
                OO000O0OO0000OOOO =bin (O0O0OO000O000000O ['cond']).count ("1")#line:614
                OOO00OO000O00O0OO =True #line:615
                for OO00000O0O0O0O00O in O00O0000O0OO00O0O .quantifiers .keys ():#line:616
                    if OO00000O0O0O0O00O =='Base':#line:617
                        OOO00OO000O00O0OO =OOO00OO000O00O0OO and (O00O0000O0OO00O0O .quantifiers .get (OO00000O0O0O0O00O )<=OO000O0OO0000OOOO )#line:618
                        if not (OOO00OO000O00O0OO ):#line:619
                            print (f"...optimization : base is {OO000O0OO0000OOOO} for {O0O000O000OO0O0OO['generated_string']}")#line:620
                    if OO00000O0O0O0O00O =='RelBase':#line:621
                        OOO00OO000O00O0OO =OOO00OO000O00O0OO and (O00O0000O0OO00O0O .quantifiers .get (OO00000O0O0O0O00O )<=OO000O0OO0000OOOO *1.0 /O00O0000O0OO00O0O .data ["rows_count"])#line:622
                        if not (OOO00OO000O00O0OO ):#line:623
                            print (f"...optimization : base is {OO000O0OO0000OOOO} for {O0O000O000OO0O0OO['generated_string']}")#line:624
                OOOOOO000OOOOO000 =not (OOO00OO000O00O0OO )#line:625
        elif O00O0000O0OO00O0O .proc =='4ftMiner':#line:626
            if (O0O000O000OO0O0OO ['cedent_type']=='cond')&(O0O000O000OO0O0OO ['defi'].get ('type')=='con'):#line:627
                OO000O0OO0000OOOO =bin (O0O0OO000O000000O ['cond']).count ("1")#line:628
                OOO00OO000O00O0OO =True #line:629
                for OO00000O0O0O0O00O in O00O0000O0OO00O0O .quantifiers .keys ():#line:630
                    if OO00000O0O0O0O00O =='Base':#line:631
                        OOO00OO000O00O0OO =OOO00OO000O00O0OO and (O00O0000O0OO00O0O .quantifiers .get (OO00000O0O0O0O00O )<=OO000O0OO0000OOOO )#line:632
                        if not (OOO00OO000O00O0OO ):#line:633
                            print (f"...optimization : base is {OO000O0OO0000OOOO} for {O0O000O000OO0O0OO['generated_string']}")#line:634
                    if OO00000O0O0O0O00O =='RelBase':#line:635
                        OOO00OO000O00O0OO =OOO00OO000O00O0OO and (O00O0000O0OO00O0O .quantifiers .get (OO00000O0O0O0O00O )<=OO000O0OO0000OOOO *1.0 /O00O0000O0OO00O0O .data ["rows_count"])#line:636
                        if not (OOO00OO000O00O0OO ):#line:637
                            print (f"...optimization : base is {OO000O0OO0000OOOO} for {O0O000O000OO0O0OO['generated_string']}")#line:638
                OOOOOO000OOOOO000 =not (OOO00OO000O00O0OO )#line:639
            if (O0O000O000OO0O0OO ['cedent_type']=='ante')&(O0O000O000OO0O0OO ['defi'].get ('type')=='con'):#line:640
                OO000O0OO0000OOOO =bin (O0O0OO000O000000O ['ante']&O0O0OO000O000000O ['cond']).count ("1")#line:641
                OOO00OO000O00O0OO =True #line:642
                for OO00000O0O0O0O00O in O00O0000O0OO00O0O .quantifiers .keys ():#line:643
                    if OO00000O0O0O0O00O =='Base':#line:644
                        OOO00OO000O00O0OO =OOO00OO000O00O0OO and (O00O0000O0OO00O0O .quantifiers .get (OO00000O0O0O0O00O )<=OO000O0OO0000OOOO )#line:645
                        if not (OOO00OO000O00O0OO ):#line:646
                            print (f"...optimization : ANTE: base is {OO000O0OO0000OOOO} for {O0O000O000OO0O0OO['generated_string']}")#line:647
                    if OO00000O0O0O0O00O =='RelBase':#line:648
                        OOO00OO000O00O0OO =OOO00OO000O00O0OO and (O00O0000O0OO00O0O .quantifiers .get (OO00000O0O0O0O00O )<=OO000O0OO0000OOOO *1.0 /O00O0000O0OO00O0O .data ["rows_count"])#line:649
                        if not (OOO00OO000O00O0OO ):#line:650
                            print (f"...optimization : ANTE:  base is {OO000O0OO0000OOOO} for {O0O000O000OO0O0OO['generated_string']}")#line:651
                OOOOOO000OOOOO000 =not (OOO00OO000O00O0OO )#line:652
            if (O0O000O000OO0O0OO ['cedent_type']=='succ')&(O0O000O000OO0O0OO ['defi'].get ('type')=='con'):#line:653
                OO000O0OO0000OOOO =bin (O0O0OO000O000000O ['ante']&O0O0OO000O000000O ['cond']&O0O0OO000O000000O ['succ']).count ("1")#line:654
                OOOOO0O0O00O0O000 =0 #line:655
                if OO000O0OO0000OOOO >0 :#line:656
                    OOOOO0O0O00O0O000 =bin (O0O0OO000O000000O ['ante']&O0O0OO000O000000O ['succ']&O0O0OO000O000000O ['cond']).count ("1")*1.0 /bin (O0O0OO000O000000O ['ante']&O0O0OO000O000000O ['cond']).count ("1")#line:657
                O0OO0OO0O0000OOOO =1 <<O00O0000O0OO00O0O .data ["rows_count"]#line:658
                OO00OOO0OOOO000OO =bin (O0O0OO000O000000O ['ante']&O0O0OO000O000000O ['succ']&O0O0OO000O000000O ['cond']).count ("1")#line:659
                OOOO000O00O00O00O =bin (O0O0OO000O000000O ['ante']&~(O0OO0OO0O0000OOOO |O0O0OO000O000000O ['succ'])&O0O0OO000O000000O ['cond']).count ("1")#line:660
                OOO0OO0O0O0OO0O0O =bin (~(O0OO0OO0O0000OOOO |O0O0OO000O000000O ['ante'])&O0O0OO000O000000O ['succ']&O0O0OO000O000000O ['cond']).count ("1")#line:661
                O0000O0OO000OOOOO =bin (~(O0OO0OO0O0000OOOO |O0O0OO000O000000O ['ante'])&~(O0OO0OO0O0000OOOO |O0O0OO000O000000O ['succ'])&O0O0OO000O000000O ['cond']).count ("1")#line:662
                OOO00OO000O00O0OO =True #line:663
                for OO00000O0O0O0O00O in O00O0000O0OO00O0O .quantifiers .keys ():#line:664
                    if OO00000O0O0O0O00O =='pim':#line:665
                        OOO00OO000O00O0OO =OOO00OO000O00O0OO and (O00O0000O0OO00O0O .quantifiers .get (OO00000O0O0O0O00O )<=OOOOO0O0O00O0O000 )#line:666
                    if not (OOO00OO000O00O0OO ):#line:667
                        print (f"...optimization : SUCC:  pim is {OOOOO0O0O00O0O000} for {O0O000O000OO0O0OO['generated_string']}")#line:668
                    if OO00000O0O0O0O00O =='aad':#line:670
                        if (OO00OOO0OOOO000OO +OOOO000O00O00O00O )*(OO00OOO0OOOO000OO +OOO0OO0O0O0OO0O0O )>0 :#line:671
                            OOO00OO000O00O0OO =OOO00OO000O00O0OO and (O00O0000O0OO00O0O .quantifiers .get (OO00000O0O0O0O00O )<=OO00OOO0OOOO000OO *(OO00OOO0OOOO000OO +OOOO000O00O00O00O +OOO0OO0O0O0OO0O0O +O0000O0OO000OOOOO )/(OO00OOO0OOOO000OO +OOOO000O00O00O00O )/(OO00OOO0OOOO000OO +OOO0OO0O0O0OO0O0O )-1 )#line:672
                        else :#line:673
                            OOO00OO000O00O0OO =False #line:674
                        if not (OOO00OO000O00O0OO ):#line:675
                            OO00O00OO0OO00000 =OO00OOO0OOOO000OO *(OO00OOO0OOOO000OO +OOOO000O00O00O00O +OOO0OO0O0O0OO0O0O +O0000O0OO000OOOOO )/(OO00OOO0OOOO000OO +OOOO000O00O00O00O )/(OO00OOO0OOOO000OO +OOO0OO0O0O0OO0O0O )-1 #line:676
                            print (f"...optimization : SUCC:  aad is {OO00O00OO0OO00000} for {O0O000O000OO0O0OO['generated_string']}")#line:677
                    if OO00000O0O0O0O00O =='bad':#line:678
                        if (OO00OOO0OOOO000OO +OOOO000O00O00O00O )*(OO00OOO0OOOO000OO +OOO0OO0O0O0OO0O0O )>0 :#line:679
                            OOO00OO000O00O0OO =OOO00OO000O00O0OO and (O00O0000O0OO00O0O .quantifiers .get (OO00000O0O0O0O00O )<=1 -OO00OOO0OOOO000OO *(OO00OOO0OOOO000OO +OOOO000O00O00O00O +OOO0OO0O0O0OO0O0O +O0000O0OO000OOOOO )/(OO00OOO0OOOO000OO +OOOO000O00O00O00O )/(OO00OOO0OOOO000OO +OOO0OO0O0O0OO0O0O ))#line:680
                        else :#line:681
                            OOO00OO000O00O0OO =False #line:682
                        if not (OOO00OO000O00O0OO ):#line:683
                            OOOOOO0OOO00OO000 =1 -OO00OOO0OOOO000OO *(OO00OOO0OOOO000OO +OOOO000O00O00O00O +OOO0OO0O0O0OO0O0O +O0000O0OO000OOOOO )/(OO00OOO0OOOO000OO +OOOO000O00O00O00O )/(OO00OOO0OOOO000OO +OOO0OO0O0O0OO0O0O )#line:684
                            print (f"...optimization : SUCC:  bad is {OOOOOO0OOO00OO000} for {O0O000O000OO0O0OO['generated_string']}")#line:685
                OOOOOO000OOOOO000 =not (OOO00OO000O00O0OO )#line:686
        if (OOOOOO000OOOOO000 ):#line:687
            print (f"... OPTIMALIZATION - SKIPPING BRANCH at cedent {O0O000O000OO0O0OO['cedent_type']}")#line:688
        return OOOOOO000OOOOO000 #line:689
    def _print (O00OOOOO0OO0OOO00 ,OOO00000O0O0OO0OO ,_OO0O0OO000OO00000 ,_OO0OOOOO00OO0OOO0 ):#line:692
        if (len (_OO0O0OO000OO00000 ))!=len (_OO0OOOOO00OO0OOO0 ):#line:693
            print ("DIFF IN LEN for following cedent : "+str (len (_OO0O0OO000OO00000 ))+" vs "+str (len (_OO0OOOOO00OO0OOO0 )))#line:694
            print ("trace cedent : "+str (_OO0O0OO000OO00000 )+", traces "+str (_OO0OOOOO00OO0OOO0 ))#line:695
        OO0OOOOO0O00OOO00 =''#line:696
        for O0O000OOOOO0OO00O in range (len (_OO0O0OO000OO00000 )):#line:697
            OOO0OO0000O0OO0OO =O00OOOOO0OO0OOO00 .data ["varname"].index (OOO00000O0O0OO0OO ['defi'].get ('attributes')[_OO0O0OO000OO00000 [O0O000OOOOO0OO00O ]].get ('name'))#line:698
            OO0OOOOO0O00OOO00 =OO0OOOOO0O00OOO00 +O00OOOOO0OO0OOO00 .data ["varname"][OOO0OO0000O0OO0OO ]+'('#line:700
            for O00OO0O0OO00OO000 in _OO0OOOOO00OO0OOO0 [O0O000OOOOO0OO00O ]:#line:701
                OO0OOOOO0O00OOO00 =OO0OOOOO0O00OOO00 +O00OOOOO0OO0OOO00 .data ["catnames"][OOO0OO0000O0OO0OO ][O00OO0O0OO00OO000 ]+" "#line:702
            OO0OOOOO0O00OOO00 =OO0OOOOO0O00OOO00 +')'#line:703
            if O0O000OOOOO0OO00O +1 <len (_OO0O0OO000OO00000 ):#line:704
                OO0OOOOO0O00OOO00 =OO0OOOOO0O00OOO00 +' & '#line:705
        return OO0OOOOO0O00OOO00 #line:709
    def _print_hypo (O00O0000OOO0OOOO0 ,OOOOOO000000OOOOO ):#line:711
        O00O0000OOO0OOOO0 .print_rule (OOOOOO000000OOOOO )#line:712
    def _print_rule (O00O0OO00OO00O0OO ,O0OO0O00OOO0OO0O0 ):#line:714
        print ('Rules info : '+str (O0OO0O00OOO0OO0O0 ['params']))#line:715
        for O00000OO00OOO0O0O in O00O0OO00OO00O0OO .task_actinfo ['cedents']:#line:716
            print (O00000OO00OOO0O0O ['cedent_type']+' = '+O00000OO00OOO0O0O ['generated_string'])#line:717
    def _genvar (O0OO000O0O0OO00O0 ,O000OOOO0OOO0OOO0 ,OOOOO00OOO0O0O00O ,_O0OOOOO0O00OOO0O0 ,_OOOOO000OOO0OO000 ,_OO0OO0OO0O0O0OOOO ,_OO0O0OO0O000OOOO0 ,_OO0O0O0O0OOO0000O ):#line:719
        for OO00OO0O0O0O00000 in range (OOOOO00OOO0O0O00O ['num_cedent']):#line:720
            if len (_O0OOOOO0O00OOO0O0 )==0 or OO00OO0O0O0O00000 >_O0OOOOO0O00OOO0O0 [-1 ]:#line:721
                _O0OOOOO0O00OOO0O0 .append (OO00OO0O0O0O00000 )#line:722
                OO0OO0O0O000OO00O =O0OO000O0O0OO00O0 .data ["varname"].index (OOOOO00OOO0O0O00O ['defi'].get ('attributes')[OO00OO0O0O0O00000 ].get ('name'))#line:723
                _OO0O0O0OOOOOO000O =OOOOO00OOO0O0O00O ['defi'].get ('attributes')[OO00OO0O0O0O00000 ].get ('minlen')#line:724
                _OOOO00O0O0000O0OO =OOOOO00OOO0O0O00O ['defi'].get ('attributes')[OO00OO0O0O0O00000 ].get ('maxlen')#line:725
                _O00OO00O00O0OO0O0 =OOOOO00OOO0O0O00O ['defi'].get ('attributes')[OO00OO0O0O0O00000 ].get ('type')#line:726
                O000OOO000O0O00O0 =len (O0OO000O0O0OO00O0 .data ["dm"][OO0OO0O0O000OO00O ])#line:727
                _OOOO0O0OO0OO000O0 =[]#line:728
                _OOOOO000OOO0OO000 .append (_OOOO0O0OO0OO000O0 )#line:729
                _OO0OO0OO0OOO0O00O =int (0 )#line:730
                O0OO000O0O0OO00O0 ._gencomb (O000OOOO0OOO0OOO0 ,OOOOO00OOO0O0O00O ,_O0OOOOO0O00OOO0O0 ,_OOOOO000OOO0OO000 ,_OOOO0O0OO0OO000O0 ,_OO0OO0OO0O0O0OOOO ,_OO0OO0OO0OOO0O00O ,O000OOO000O0O00O0 ,_O00OO00O00O0OO0O0 ,_OO0O0OO0O000OOOO0 ,_OO0O0O0O0OOO0000O ,_OO0O0O0OOOOOO000O ,_OOOO00O0O0000O0OO )#line:731
                _OOOOO000OOO0OO000 .pop ()#line:732
                _O0OOOOO0O00OOO0O0 .pop ()#line:733
    def _gencomb (OO0OO00OO0O0O0O00 ,OO00000O0O0O0O000 ,O00O0OOOO0O000OOO ,_OO00O0O0OO000O000 ,_O0OOO00OOO0O0OO00 ,_OO0O00O00OO0OO0OO ,_O00O0OOOOOO0O0OO0 ,_OOO000OO0O0OO000O ,OOO0O00000O00O0OO ,_O00OO0O0OO00OOO00 ,_OOO000OOOO0OOO00O ,_O00O0O0O0000O00O0 ,_O00O0O0O0O0O0OOO0 ,_O000OOOO00O00OO0O ):#line:735
        _O0O00O00O0O00O0O0 =[]#line:736
        if _O00OO0O0OO00OOO00 =="subset":#line:737
            if len (_OO0O00O00OO0OO0OO )==0 :#line:738
                _O0O00O00O0O00O0O0 =range (OOO0O00000O00O0OO )#line:739
            else :#line:740
                _O0O00O00O0O00O0O0 =range (_OO0O00O00OO0OO0OO [-1 ]+1 ,OOO0O00000O00O0OO )#line:741
        elif _O00OO0O0OO00OOO00 =="seq":#line:742
            if len (_OO0O00O00OO0OO0OO )==0 :#line:743
                _O0O00O00O0O00O0O0 =range (OOO0O00000O00O0OO -_O00O0O0O0O0O0OOO0 +1 )#line:744
            else :#line:745
                if _OO0O00O00OO0OO0OO [-1 ]+1 ==OOO0O00000O00O0OO :#line:746
                    return #line:747
                O00O000OO0O000O00 =_OO0O00O00OO0OO0OO [-1 ]+1 #line:748
                _O0O00O00O0O00O0O0 .append (O00O000OO0O000O00 )#line:749
        elif _O00OO0O0OO00OOO00 =="lcut":#line:750
            if len (_OO0O00O00OO0OO0OO )==0 :#line:751
                O00O000OO0O000O00 =0 ;#line:752
            else :#line:753
                if _OO0O00O00OO0OO0OO [-1 ]+1 ==OOO0O00000O00O0OO :#line:754
                    return #line:755
                O00O000OO0O000O00 =_OO0O00O00OO0OO0OO [-1 ]+1 #line:756
            _O0O00O00O0O00O0O0 .append (O00O000OO0O000O00 )#line:757
        elif _O00OO0O0OO00OOO00 =="rcut":#line:758
            if len (_OO0O00O00OO0OO0OO )==0 :#line:759
                O00O000OO0O000O00 =OOO0O00000O00O0OO -1 ;#line:760
            else :#line:761
                if _OO0O00O00OO0OO0OO [-1 ]==0 :#line:762
                    return #line:763
                O00O000OO0O000O00 =_OO0O00O00OO0OO0OO [-1 ]-1 #line:764
            _O0O00O00O0O00O0O0 .append (O00O000OO0O000O00 )#line:766
        elif _O00OO0O0OO00OOO00 =="one":#line:767
            if len (_OO0O00O00OO0OO0OO )==0 :#line:768
                OO00O00OO0O0O0O0O =OO0OO00OO0O0O0O00 .data ["varname"].index (O00O0OOOO0O000OOO ['defi'].get ('attributes')[_OO00O0O0OO000O000 [-1 ]].get ('name'))#line:769
                try :#line:770
                    O00O000OO0O000O00 =OO0OO00OO0O0O0O00 .data ["catnames"][OO00O00OO0O0O0O0O ].index (O00O0OOOO0O000OOO ['defi'].get ('attributes')[_OO00O0O0OO000O000 [-1 ]].get ('value'))#line:771
                except :#line:772
                    print (f"ERROR: attribute '{O00O0OOOO0O000OOO['defi'].get('attributes')[_OO00O0O0OO000O000[-1]].get('name')}' has not value '{O00O0OOOO0O000OOO['defi'].get('attributes')[_OO00O0O0OO000O000[-1]].get('value')}'")#line:773
                    exit (1 )#line:774
                _O0O00O00O0O00O0O0 .append (O00O000OO0O000O00 )#line:775
                _O00O0O0O0O0O0OOO0 =1 #line:776
                _O000OOOO00O00OO0O =1 #line:777
            else :#line:778
                print ("DEBUG: one category should not have more categories")#line:779
                return #line:780
        else :#line:781
            print ("Attribute type "+_O00OO0O0OO00OOO00 +" not supported.")#line:782
            return #line:783
        for O000O0O000O00000O in _O0O00O00O0O00O0O0 :#line:786
                _OO0O00O00OO0OO0OO .append (O000O0O000O00000O )#line:788
                _O0OOO00OOO0O0OO00 .pop ()#line:789
                _O0OOO00OOO0O0OO00 .append (_OO0O00O00OO0OO0OO )#line:790
                _OO00OO00OO0000O00 =_OOO000OO0O0OO000O |OO0OO00OO0O0O0O00 .data ["dm"][OO0OO00OO0O0O0O00 .data ["varname"].index (O00O0OOOO0O000OOO ['defi'].get ('attributes')[_OO00O0O0OO000O000 [-1 ]].get ('name'))][O000O0O000O00000O ]#line:794
                _OOOOO00OO0OOO0O0O =1 #line:796
                if (len (_OO00O0O0OO000O000 )<_OOO000OOOO0OOO00O ):#line:797
                    _OOOOO00OO0OOO0O0O =-1 #line:798
                if (len (_O0OOO00OOO0O0OO00 [-1 ])<_O00O0O0O0O0O0OOO0 ):#line:800
                    _OOOOO00OO0OOO0O0O =0 #line:801
                _O0OOOO000OO00O0OO =0 #line:803
                if O00O0OOOO0O000OOO ['defi'].get ('type')=='con':#line:804
                    _O0OOOO000OO00O0OO =_O00O0OOOOOO0O0OO0 &_OO00OO00OO0000O00 #line:805
                else :#line:806
                    _O0OOOO000OO00O0OO =_O00O0OOOOOO0O0OO0 |_OO00OO00OO0000O00 #line:807
                O00O0OOOO0O000OOO ['trace_cedent']=_OO00O0O0OO000O000 #line:808
                O00O0OOOO0O000OOO ['traces']=_O0OOO00OOO0O0OO00 #line:809
                O00O0OOOO0O000OOO ['generated_string']=OO0OO00OO0O0O0O00 ._print (O00O0OOOO0O000OOO ,_OO00O0O0OO000O000 ,_O0OOO00OOO0O0OO00 )#line:810
                O00O0OOOO0O000OOO ['filter_value']=_O0OOOO000OO00O0OO #line:811
                OO00000O0O0O0O000 ['cedents'].append (O00O0OOOO0O000OOO )#line:812
                O0000O00OOO00OO0O =OO0OO00OO0O0O0O00 ._verify_opt (OO00000O0O0O0O000 ,O00O0OOOO0O000OOO )#line:813
                if not (O0000O00OOO00OO0O ):#line:819
                    if _OOOOO00OO0OOO0O0O ==1 :#line:820
                        if len (OO00000O0O0O0O000 ['cedents_to_do'])==len (OO00000O0O0O0O000 ['cedents']):#line:822
                            if OO0OO00OO0O0O0O00 .proc =='CFMiner':#line:823
                                OOO00OO0OOO0OOOO0 ,O00O00O0OOO0O0000 =OO0OO00OO0O0O0O00 ._verifyCF (_O0OOOO000OO00O0OO )#line:824
                            elif OO0OO00OO0O0O0O00 .proc =='4ftMiner':#line:825
                                OOO00OO0OOO0OOOO0 ,O00O00O0OOO0O0000 =OO0OO00OO0O0O0O00 ._verify4ft (_OO00OO00OO0000O00 )#line:826
                            elif OO0OO00OO0O0O0O00 .proc =='SD4ftMiner':#line:827
                                OOO00OO0OOO0OOOO0 ,O00O00O0OOO0O0000 =OO0OO00OO0O0O0O00 ._verifysd4ft (_OO00OO00OO0000O00 )#line:828
                            elif OO0OO00OO0O0O0O00 .proc =='NewAct4ftMiner':#line:829
                                OOO00OO0OOO0OOOO0 ,O00O00O0OOO0O0000 =OO0OO00OO0O0O0O00 ._verifynewact4ft (_OO00OO00OO0000O00 )#line:830
                            elif OO0OO00OO0O0O0O00 .proc =='Act4ftMiner':#line:831
                                OOO00OO0OOO0OOOO0 ,O00O00O0OOO0O0000 =OO0OO00OO0O0O0O00 ._verifyact4ft (_OO00OO00OO0000O00 )#line:832
                            else :#line:833
                                print ("Unsupported procedure : "+OO0OO00OO0O0O0O00 .proc )#line:834
                                exit (0 )#line:835
                            if OOO00OO0OOO0OOOO0 ==True :#line:836
                                O0000O00OOO0OOOOO ={}#line:837
                                O0000O00OOO0OOOOO ["rule_id"]=OO0OO00OO0O0O0O00 .stats ['total_valid']#line:838
                                O0000O00OOO0OOOOO ["cedents"]={}#line:839
                                for O0O00O000OOO0O000 in OO00000O0O0O0O000 ['cedents']:#line:840
                                    O0000O00OOO0OOOOO ['cedents'][O0O00O000OOO0O000 ['cedent_type']]=O0O00O000OOO0O000 ['generated_string']#line:841
                                O0000O00OOO0OOOOO ["params"]=O00O00O0OOO0O0000 #line:843
                                O0000O00OOO0OOOOO ["trace_cedent"]=_OO00O0O0OO000O000 #line:844
                                OO0OO00OO0O0O0O00 ._print_rule (O0000O00OOO0OOOOO )#line:845
                                O0000O00OOO0OOOOO ["traces"]=_O0OOO00OOO0O0OO00 #line:848
                                OO0OO00OO0O0O0O00 .rulelist .append (O0000O00OOO0OOOOO )#line:849
                            OO0OO00OO0O0O0O00 .stats ['total_cnt']+=1 #line:850
                    if _OOOOO00OO0OOO0O0O >=0 :#line:851
                        if len (OO00000O0O0O0O000 ['cedents_to_do'])>len (OO00000O0O0O0O000 ['cedents']):#line:852
                            OO0OO00OO0O0O0O00 ._start_cedent (OO00000O0O0O0O000 )#line:853
                    OO00000O0O0O0O000 ['cedents'].pop ()#line:854
                    if (len (_OO00O0O0OO000O000 )<_O00O0O0O0000O00O0 ):#line:855
                        OO0OO00OO0O0O0O00 ._genvar (OO00000O0O0O0O000 ,O00O0OOOO0O000OOO ,_OO00O0O0OO000O000 ,_O0OOO00OOO0O0OO00 ,_O0OOOO000OO00O0OO ,_OOO000OOOO0OOO00O ,_O00O0O0O0000O00O0 )#line:856
                else :#line:857
                    OO00000O0O0O0O000 ['cedents'].pop ()#line:858
                if len (_OO0O00O00OO0OO0OO )<_O000OOOO00O00OO0O :#line:859
                    OO0OO00OO0O0O0O00 ._gencomb (OO00000O0O0O0O000 ,O00O0OOOO0O000OOO ,_OO00O0O0OO000O000 ,_O0OOO00OOO0O0OO00 ,_OO0O00O00OO0OO0OO ,_O00O0OOOOOO0O0OO0 ,_OO00OO00OO0000O00 ,OOO0O00000O00O0OO ,_O00OO0O0OO00OOO00 ,_OOO000OOOO0OOO00O ,_O00O0O0O0000O00O0 ,_O00O0O0O0O0O0OOO0 ,_O000OOOO00O00OO0O )#line:860
                _OO0O00O00OO0OO0OO .pop ()#line:861
    def _start_cedent (OO0O0O0000OO000O0 ,OO00O0OOOOO0O00O0 ):#line:863
        if len (OO00O0OOOOO0O00O0 ['cedents_to_do'])>len (OO00O0OOOOO0O00O0 ['cedents']):#line:864
            _OOO0O0OO0OOO0O0O0 =[]#line:865
            _OO00OOOO00OOOOO0O =[]#line:866
            OO00O0000000O0OO0 ={}#line:867
            OO00O0000000O0OO0 ['cedent_type']=OO00O0OOOOO0O00O0 ['cedents_to_do'][len (OO00O0OOOOO0O00O0 ['cedents'])]#line:868
            O0O0O0O00OOO0OOOO =OO00O0000000O0OO0 ['cedent_type']#line:869
            if ((O0O0O0O00OOO0OOOO [-1 ]=='-')|(O0O0O0O00OOO0OOOO [-1 ]=='+')):#line:870
                O0O0O0O00OOO0OOOO =O0O0O0O00OOO0OOOO [:-1 ]#line:871
            OO00O0000000O0OO0 ['defi']=OO0O0O0000OO000O0 .kwargs .get (O0O0O0O00OOO0OOOO )#line:873
            if (OO00O0000000O0OO0 ['defi']==None ):#line:874
                print ("Error getting cedent ",OO00O0000000O0OO0 ['cedent_type'])#line:875
            _O000O00O0O00OO0O0 =int (0 )#line:876
            OO00O0000000O0OO0 ['num_cedent']=len (OO00O0000000O0OO0 ['defi'].get ('attributes'))#line:881
            if (OO00O0000000O0OO0 ['defi'].get ('type')=='con'):#line:882
                _O000O00O0O00OO0O0 =(1 <<OO0O0O0000OO000O0 .data ["rows_count"])-1 #line:883
            OO0O0O0000OO000O0 ._genvar (OO00O0OOOOO0O00O0 ,OO00O0000000O0OO0 ,_OOO0O0OO0OOO0O0O0 ,_OO00OOOO00OOOOO0O ,_O000O00O0O00OO0O0 ,OO00O0000000O0OO0 ['defi'].get ('minlen'),OO00O0000000O0OO0 ['defi'].get ('maxlen'))#line:884
    def _calc_all (O00O00000OOO0O000 ,**OO0O0000OO0OOOO00 ):#line:887
        O00O00000OOO0O000 ._prep_data (O00O00000OOO0O000 .kwargs .get ("df"))#line:888
        O00O00000OOO0O000 ._calculate (**OO0O0000OO0OOOO00 )#line:889
    def _check_cedents (O000OOO0OOOO00OOO ,O00OOOOOO000OOOOO ,**OO0O0OOO00OO00000 ):#line:891
        O0O00000O0O00OOOO =True #line:892
        if (OO0O0OOO00OO00000 .get ('quantifiers',None )==None ):#line:893
            print (f"Error: missing quantifiers.")#line:894
            O0O00000O0O00OOOO =False #line:895
            return O0O00000O0O00OOOO #line:896
        if (type (OO0O0OOO00OO00000 .get ('quantifiers'))!=dict ):#line:897
            print (f"Error: quantifiers are not dictionary type.")#line:898
            O0O00000O0O00OOOO =False #line:899
            return O0O00000O0O00OOOO #line:900
        for OO0O000OOO0O0OOOO in O00OOOOOO000OOOOO :#line:902
            if (OO0O0OOO00OO00000 .get (OO0O000OOO0O0OOOO ,None )==None ):#line:903
                print (f"Error: cedent {OO0O000OOO0O0OOOO} is missing in parameters.")#line:904
                O0O00000O0O00OOOO =False #line:905
                return O0O00000O0O00OOOO #line:906
            OO0000OO0OOOOO00O =OO0O0OOO00OO00000 .get (OO0O000OOO0O0OOOO )#line:907
            if (OO0000OO0OOOOO00O .get ('minlen'),None )==None :#line:908
                print (f"Error: cedent {OO0O000OOO0O0OOOO} has no minimal length specified.")#line:909
                O0O00000O0O00OOOO =False #line:910
                return O0O00000O0O00OOOO #line:911
            if not (type (OO0000OO0OOOOO00O .get ('minlen'))is int ):#line:912
                print (f"Error: cedent {OO0O000OOO0O0OOOO} has invalid type of minimal length ({type(OO0000OO0OOOOO00O.get('minlen'))}).")#line:913
                O0O00000O0O00OOOO =False #line:914
                return O0O00000O0O00OOOO #line:915
            if (OO0000OO0OOOOO00O .get ('maxlen'),None )==None :#line:916
                print (f"Error: cedent {OO0O000OOO0O0OOOO} has no maximal length specified.")#line:917
                O0O00000O0O00OOOO =False #line:918
                return O0O00000O0O00OOOO #line:919
            if not (type (OO0000OO0OOOOO00O .get ('maxlen'))is int ):#line:920
                print (f"Error: cedent {OO0O000OOO0O0OOOO} has invalid type of maximal length.")#line:921
                O0O00000O0O00OOOO =False #line:922
                return O0O00000O0O00OOOO #line:923
            if (OO0000OO0OOOOO00O .get ('type'),None )==None :#line:924
                print (f"Error: cedent {OO0O000OOO0O0OOOO} has no type specified.")#line:925
                O0O00000O0O00OOOO =False #line:926
                return O0O00000O0O00OOOO #line:927
            if not ((OO0000OO0OOOOO00O .get ('type'))in (['con','dis'])):#line:928
                print (f"Error: cedent {OO0O000OOO0O0OOOO} has invalid type. Allowed values are 'con' and 'dis'.")#line:929
                O0O00000O0O00OOOO =False #line:930
                return O0O00000O0O00OOOO #line:931
            if (OO0000OO0OOOOO00O .get ('attributes'),None )==None :#line:932
                print (f"Error: cedent {OO0O000OOO0O0OOOO} has no attributes specified.")#line:933
                O0O00000O0O00OOOO =False #line:934
                return O0O00000O0O00OOOO #line:935
            for O0O0O00O0OO000OOO in OO0000OO0OOOOO00O .get ('attributes'):#line:936
                if (O0O0O00O0OO000OOO .get ('name'),None )==None :#line:937
                    print (f"Error: cedent {OO0O000OOO0O0OOOO} / attribute {O0O0O00O0OO000OOO} has no 'name' attribute specified.")#line:938
                    O0O00000O0O00OOOO =False #line:939
                    return O0O00000O0O00OOOO #line:940
                if not ((O0O0O00O0OO000OOO .get ('name'))in O000OOO0OOOO00OOO .data ["varname"]):#line:941
                    print (f"Error: cedent {OO0O000OOO0O0OOOO} / attribute {O0O0O00O0OO000OOO.get('name')} not in variable list. Please check spelling.")#line:942
                    O0O00000O0O00OOOO =False #line:943
                    return O0O00000O0O00OOOO #line:944
                if (O0O0O00O0OO000OOO .get ('type'),None )==None :#line:945
                    print (f"Error: cedent {OO0O000OOO0O0OOOO} / attribute {O0O0O00O0OO000OOO.get('name')} has no 'type' attribute specified.")#line:946
                    O0O00000O0O00OOOO =False #line:947
                    return O0O00000O0O00OOOO #line:948
                if not ((O0O0O00O0OO000OOO .get ('type'))in (['rcut','lcut','seq','subset','one'])):#line:949
                    print (f"Error: cedent {OO0O000OOO0O0OOOO} / attribute {O0O0O00O0OO000OOO.get('name')} has unsupported type {O0O0O00O0OO000OOO.get('type')}. Supported types are 'subset','seq','lcut','rcut','one'.")#line:950
                    O0O00000O0O00OOOO =False #line:951
                    return O0O00000O0O00OOOO #line:952
                if (O0O0O00O0OO000OOO .get ('minlen'),None )==None :#line:953
                    print (f"Error: cedent {OO0O000OOO0O0OOOO} / attribute {O0O0O00O0OO000OOO.get('name')} has no minimal length specified.")#line:954
                    O0O00000O0O00OOOO =False #line:955
                    return O0O00000O0O00OOOO #line:956
                if not (type (O0O0O00O0OO000OOO .get ('minlen'))is int ):#line:957
                    if not (O0O0O00O0OO000OOO .get ('type')=='one'):#line:958
                        print (f"Error: cedent {OO0O000OOO0O0OOOO} / attribute {O0O0O00O0OO000OOO.get('name')} has invalid type of minimal length.")#line:959
                        O0O00000O0O00OOOO =False #line:960
                        return O0O00000O0O00OOOO #line:961
                if (O0O0O00O0OO000OOO .get ('maxlen'),None )==None :#line:962
                    print (f"Error: cedent {OO0O000OOO0O0OOOO} / attribute {O0O0O00O0OO000OOO.get('name')} has no maximal length specified.")#line:963
                    O0O00000O0O00OOOO =False #line:964
                    return O0O00000O0O00OOOO #line:965
                if not (type (O0O0O00O0OO000OOO .get ('maxlen'))is int ):#line:966
                    if not (O0O0O00O0OO000OOO .get ('type')=='one'):#line:967
                        print (f"Error: cedent {OO0O000OOO0O0OOOO} / attribute {O0O0O00O0OO000OOO.get('name')} has invalid type of maximal length.")#line:968
                        O0O00000O0O00OOOO =False #line:969
                        return O0O00000O0O00OOOO #line:970
        return O0O00000O0O00OOOO #line:971
    def _calculate (O0OO0OO00OOOOO0O0 ,**O0OOO0OOO0OO000O0 ):#line:973
        if O0OO0OO00OOOOO0O0 .data ["data_prepared"]==0 :#line:974
            print ("Error: data not prepared")#line:975
            return #line:976
        O0OO0OO00OOOOO0O0 .kwargs =O0OOO0OOO0OO000O0 #line:977
        O0OO0OO00OOOOO0O0 .proc =O0OOO0OOO0OO000O0 .get ('proc')#line:978
        O0OO0OO00OOOOO0O0 .quantifiers =O0OOO0OOO0OO000O0 .get ('quantifiers')#line:979
        O0OO0OO00OOOOO0O0 ._init_task ()#line:981
        O0OO0OO00OOOOO0O0 .stats ['start_proc_time']=time .time ()#line:982
        O0OO0OO00OOOOO0O0 .task_actinfo ['cedents_to_do']=[]#line:983
        O0OO0OO00OOOOO0O0 .task_actinfo ['cedents']=[]#line:984
        if O0OOO0OOO0OO000O0 .get ("proc")=='CFMiner':#line:987
            O0OO0OO00OOOOO0O0 .task_actinfo ['cedents_to_do']=['cond']#line:988
            if O0OOO0OOO0OO000O0 .get ('target',None )==None :#line:989
                print ("ERROR: no target variable defined for CF Miner")#line:990
                return #line:991
            if not (O0OO0OO00OOOOO0O0 ._check_cedents (['cond'],**O0OOO0OOO0OO000O0 )):#line:992
                return #line:993
            if not (O0OOO0OOO0OO000O0 .get ('target')in O0OO0OO00OOOOO0O0 .data ["varname"]):#line:994
                print ("ERROR: target parameter is not variable. Please check spelling of variable name in parameter 'target'.")#line:995
                return #line:996
        elif O0OOO0OOO0OO000O0 .get ("proc")=='4ftMiner':#line:998
            if not (O0OO0OO00OOOOO0O0 ._check_cedents (['ante','succ'],**O0OOO0OOO0OO000O0 )):#line:999
                return #line:1000
            _OO0OOOO00000000OO =O0OOO0OOO0OO000O0 .get ("cond")#line:1002
            if _OO0OOOO00000000OO !=None :#line:1003
                O0OO0OO00OOOOO0O0 .task_actinfo ['cedents_to_do'].append ('cond')#line:1004
            else :#line:1005
                O00O000OOO0OOO0O0 =O0OO0OO00OOOOO0O0 .cedent #line:1006
                O00O000OOO0OOO0O0 ['cedent_type']='cond'#line:1007
                O00O000OOO0OOO0O0 ['filter_value']=(1 <<O0OO0OO00OOOOO0O0 .data ["rows_count"])-1 #line:1008
                O00O000OOO0OOO0O0 ['generated_string']='---'#line:1009
                O0OO0OO00OOOOO0O0 .task_actinfo ['cedents_to_do'].append ('cond')#line:1011
                O0OO0OO00OOOOO0O0 .task_actinfo ['cedents'].append (O00O000OOO0OOO0O0 )#line:1012
            O0OO0OO00OOOOO0O0 .task_actinfo ['cedents_to_do'].append ('ante')#line:1016
            O0OO0OO00OOOOO0O0 .task_actinfo ['cedents_to_do'].append ('succ')#line:1017
        elif O0OOO0OOO0OO000O0 .get ("proc")=='NewAct4ftMiner':#line:1018
            _OO0OOOO00000000OO =O0OOO0OOO0OO000O0 .get ("cond")#line:1021
            if _OO0OOOO00000000OO !=None :#line:1022
                O0OO0OO00OOOOO0O0 .task_actinfo ['cedents_to_do'].append ('cond')#line:1023
            else :#line:1024
                O00O000OOO0OOO0O0 =O0OO0OO00OOOOO0O0 .cedent #line:1025
                O00O000OOO0OOO0O0 ['cedent_type']='cond'#line:1026
                O00O000OOO0OOO0O0 ['filter_value']=(1 <<O0OO0OO00OOOOO0O0 .data ["rows_count"])-1 #line:1027
                O00O000OOO0OOO0O0 ['generated_string']='---'#line:1028
                print (O00O000OOO0OOO0O0 ['filter_value'])#line:1029
                O0OO0OO00OOOOO0O0 .task_actinfo ['cedents_to_do'].append ('cond')#line:1030
                O0OO0OO00OOOOO0O0 .task_actinfo ['cedents'].append (O00O000OOO0OOO0O0 )#line:1031
            O0OO0OO00OOOOO0O0 .task_actinfo ['cedents_to_do'].append ('antv')#line:1032
            O0OO0OO00OOOOO0O0 .task_actinfo ['cedents_to_do'].append ('sucv')#line:1033
            O0OO0OO00OOOOO0O0 .task_actinfo ['cedents_to_do'].append ('ante')#line:1034
            O0OO0OO00OOOOO0O0 .task_actinfo ['cedents_to_do'].append ('succ')#line:1035
        elif O0OOO0OOO0OO000O0 .get ("proc")=='Act4ftMiner':#line:1036
            _OO0OOOO00000000OO =O0OOO0OOO0OO000O0 .get ("cond")#line:1039
            if _OO0OOOO00000000OO !=None :#line:1040
                O0OO0OO00OOOOO0O0 .task_actinfo ['cedents_to_do'].append ('cond')#line:1041
            else :#line:1042
                O00O000OOO0OOO0O0 =O0OO0OO00OOOOO0O0 .cedent #line:1043
                O00O000OOO0OOO0O0 ['cedent_type']='cond'#line:1044
                O00O000OOO0OOO0O0 ['filter_value']=(1 <<O0OO0OO00OOOOO0O0 .data ["rows_count"])-1 #line:1045
                O00O000OOO0OOO0O0 ['generated_string']='---'#line:1046
                print (O00O000OOO0OOO0O0 ['filter_value'])#line:1047
                O0OO0OO00OOOOO0O0 .task_actinfo ['cedents_to_do'].append ('cond')#line:1048
                O0OO0OO00OOOOO0O0 .task_actinfo ['cedents'].append (O00O000OOO0OOO0O0 )#line:1049
            O0OO0OO00OOOOO0O0 .task_actinfo ['cedents_to_do'].append ('antv-')#line:1050
            O0OO0OO00OOOOO0O0 .task_actinfo ['cedents_to_do'].append ('antv+')#line:1051
            O0OO0OO00OOOOO0O0 .task_actinfo ['cedents_to_do'].append ('sucv-')#line:1052
            O0OO0OO00OOOOO0O0 .task_actinfo ['cedents_to_do'].append ('sucv+')#line:1053
            O0OO0OO00OOOOO0O0 .task_actinfo ['cedents_to_do'].append ('ante')#line:1054
            O0OO0OO00OOOOO0O0 .task_actinfo ['cedents_to_do'].append ('succ')#line:1055
        elif O0OOO0OOO0OO000O0 .get ("proc")=='SD4ftMiner':#line:1056
            if not (O0OO0OO00OOOOO0O0 ._check_cedents (['ante','succ','frst','scnd'],**O0OOO0OOO0OO000O0 )):#line:1059
                return #line:1060
            _OO0OOOO00000000OO =O0OOO0OOO0OO000O0 .get ("cond")#line:1061
            if _OO0OOOO00000000OO !=None :#line:1062
                O0OO0OO00OOOOO0O0 .task_actinfo ['cedents_to_do'].append ('cond')#line:1063
            else :#line:1064
                O00O000OOO0OOO0O0 =O0OO0OO00OOOOO0O0 .cedent #line:1065
                O00O000OOO0OOO0O0 ['cedent_type']='cond'#line:1066
                O00O000OOO0OOO0O0 ['filter_value']=(1 <<O0OO0OO00OOOOO0O0 .data ["rows_count"])-1 #line:1067
                O00O000OOO0OOO0O0 ['generated_string']='---'#line:1068
                O0OO0OO00OOOOO0O0 .task_actinfo ['cedents_to_do'].append ('cond')#line:1070
                O0OO0OO00OOOOO0O0 .task_actinfo ['cedents'].append (O00O000OOO0OOO0O0 )#line:1071
            O0OO0OO00OOOOO0O0 .task_actinfo ['cedents_to_do'].append ('frst')#line:1072
            O0OO0OO00OOOOO0O0 .task_actinfo ['cedents_to_do'].append ('scnd')#line:1073
            O0OO0OO00OOOOO0O0 .task_actinfo ['cedents_to_do'].append ('ante')#line:1074
            O0OO0OO00OOOOO0O0 .task_actinfo ['cedents_to_do'].append ('succ')#line:1075
        else :#line:1076
            print ("Unsupported procedure")#line:1077
            return #line:1078
        print ("Will go for ",O0OOO0OOO0OO000O0 .get ("proc"))#line:1079
        O0OO0OO00OOOOO0O0 .task_actinfo ['optim']={}#line:1082
        O0O0000OOOOOO00O0 =True #line:1083
        for OO0OO00O0OO00OOOO in O0OO0OO00OOOOO0O0 .task_actinfo ['cedents_to_do']:#line:1084
            try :#line:1085
                O00OO0O00O00O0O00 =O0OO0OO00OOOOO0O0 .kwargs .get (OO0OO00O0OO00OOOO )#line:1086
                if O00OO0O00O00O0O00 .get ('type')!='con':#line:1089
                    O0O0000OOOOOO00O0 =False #line:1090
            except :#line:1091
                O0000OOOOO0O0O0OO =1 <2 #line:1092
        if "opts"in O0OOO0OOO0OO000O0 :#line:1094
            if "no_optimizations"in O0OOO0OOO0OO000O0 .get ('opts'):#line:1095
                O0O0000OOOOOO00O0 =False #line:1096
                print ("No optimization will be made.")#line:1097
        OO000000O0OO00OOO ={}#line:1099
        OO000000O0OO00OOO ['only_con']=O0O0000OOOOOO00O0 #line:1100
        O0OO0OO00OOOOO0O0 .task_actinfo ['optim']=OO000000O0OO00OOO #line:1101
        print ("Starting to mine rules.")#line:1109
        O0OO0OO00OOOOO0O0 ._start_cedent (O0OO0OO00OOOOO0O0 .task_actinfo )#line:1110
        O0OO0OO00OOOOO0O0 .stats ['end_proc_time']=time .time ()#line:1112
        print ("Done. Total verifications : "+str (O0OO0OO00OOOOO0O0 .stats ['total_cnt'])+", rules "+str (O0OO0OO00OOOOO0O0 .stats ['total_valid'])+",control number:"+str (O0OO0OO00OOOOO0O0 .stats ['control_number'])+", times: prep "+str (O0OO0OO00OOOOO0O0 .stats ['end_prep_time']-O0OO0OO00OOOOO0O0 .stats ['start_prep_time'])+", processing "+str (O0OO0OO00OOOOO0O0 .stats ['end_proc_time']-O0OO0OO00OOOOO0O0 .stats ['start_proc_time']))#line:1115
        OOO000OOO0O0O0O00 ={}#line:1116
        O000O0O00000O0O0O ={}#line:1117
        O000O0O00000O0O0O ["task_type"]=O0OOO0OOO0OO000O0 .get ('proc')#line:1118
        O000O0O00000O0O0O ["target"]=O0OOO0OOO0OO000O0 .get ('target')#line:1120
        O000O0O00000O0O0O ["self.quantifiers"]=O0OO0OO00OOOOO0O0 .quantifiers #line:1121
        if O0OOO0OOO0OO000O0 .get ('cond')!=None :#line:1123
            O000O0O00000O0O0O ['cond']=O0OOO0OOO0OO000O0 .get ('cond')#line:1124
        if O0OOO0OOO0OO000O0 .get ('ante')!=None :#line:1125
            O000O0O00000O0O0O ['ante']=O0OOO0OOO0OO000O0 .get ('ante')#line:1126
        if O0OOO0OOO0OO000O0 .get ('succ')!=None :#line:1127
            O000O0O00000O0O0O ['succ']=O0OOO0OOO0OO000O0 .get ('succ')#line:1128
        if O0OOO0OOO0OO000O0 .get ('opts')!=None :#line:1129
            O000O0O00000O0O0O ['opts']=O0OOO0OOO0OO000O0 .get ('opts')#line:1130
        OOO000OOO0O0O0O00 ["taskinfo"]=O000O0O00000O0O0O #line:1131
        OO0O0OO000OOOO00O ={}#line:1132
        OO0O0OO000OOOO00O ["total_verifications"]=O0OO0OO00OOOOO0O0 .stats ['total_cnt']#line:1133
        OO0O0OO000OOOO00O ["valid_rules"]=O0OO0OO00OOOOO0O0 .stats ['total_valid']#line:1134
        OO0O0OO000OOOO00O ["time_prep"]=O0OO0OO00OOOOO0O0 .stats ['end_prep_time']-O0OO0OO00OOOOO0O0 .stats ['start_prep_time']#line:1135
        OO0O0OO000OOOO00O ["time_processing"]=O0OO0OO00OOOOO0O0 .stats ['end_proc_time']-O0OO0OO00OOOOO0O0 .stats ['start_proc_time']#line:1136
        OO0O0OO000OOOO00O ["time_total"]=O0OO0OO00OOOOO0O0 .stats ['end_prep_time']-O0OO0OO00OOOOO0O0 .stats ['start_prep_time']+O0OO0OO00OOOOO0O0 .stats ['end_proc_time']-O0OO0OO00OOOOO0O0 .stats ['start_proc_time']#line:1137
        OOO000OOO0O0O0O00 ["summary_statistics"]=OO0O0OO000OOOO00O #line:1138
        OOO000OOO0O0O0O00 ["rules"]=O0OO0OO00OOOOO0O0 .rulelist #line:1139
        O0OO00O0OOO0O0O00 ={}#line:1140
        O0OO00O0OOO0O0O00 ["varname"]=O0OO0OO00OOOOO0O0 .data ["varname"]#line:1141
        O0OO00O0OOO0O0O00 ["catnames"]=O0OO0OO00OOOOO0O0 .data ["catnames"]#line:1142
        OOO000OOO0O0O0O00 ["datalabels"]=O0OO00O0OOO0O0O00 #line:1143
        O0OO0OO00OOOOO0O0 .result =OOO000OOO0O0O0O00 #line:1146
    def print_summary (O00000OO0O0OOO00O ):#line:1148
        print ("")#line:1149
        print ("CleverMiner task processing summary:")#line:1150
        print ("")#line:1151
        print (f"Task type : {O00000OO0O0OOO00O.result['taskinfo']['task_type']}")#line:1152
        print (f"Number of verifications : {O00000OO0O0OOO00O.result['summary_statistics']['total_verifications']}")#line:1153
        print (f"Number of rules : {O00000OO0O0OOO00O.result['summary_statistics']['valid_rules']}")#line:1154
        print (f"Total time needed : {strftime('%Hh %Mm %Ss', gmtime(O00000OO0O0OOO00O.result['summary_statistics']['time_total']))}")#line:1155
        print (f"Time of data preparation : {strftime('%Hh %Mm %Ss', gmtime(O00000OO0O0OOO00O.result['summary_statistics']['time_prep']))}")#line:1157
        print (f"Time of rule mining : {strftime('%Hh %Mm %Ss', gmtime(O00000OO0O0OOO00O.result['summary_statistics']['time_processing']))}")#line:1158
        print ("")#line:1159
    def print_hypolist (OO0O0OOOOOOO00O0O ):#line:1161
        OO0O0OOOOOOO00O0O .print_rulelist ();#line:1162
    def print_rulelist (O00OO0O00O0O00O00 ):#line:1164
        print ("")#line:1166
        print ("List of rules:")#line:1167
        if O00OO0O00O0O00O00 .result ['taskinfo']['task_type']=="4ftMiner":#line:1168
            print ("RULEID BASE  CONF  AAD    Rule")#line:1169
        elif O00OO0O00O0O00O00 .result ['taskinfo']['task_type']=="CFMiner":#line:1170
            print ("RULEID BASE  S_UP  S_DOWN Condition")#line:1171
        elif O00OO0O00O0O00O00 .result ['taskinfo']['task_type']=="SD4ftMiner":#line:1172
            print ("RULEID BASE1 BASE2 RatioConf DeltaConf Rule")#line:1173
        else :#line:1174
            print ("Unsupported task type for rulelist")#line:1175
            return #line:1176
        for OO0O0O00000O00000 in O00OO0O00O0O00O00 .result ["rules"]:#line:1177
            OOOO00O00O000O000 ="{:6d}".format (OO0O0O00000O00000 ["rule_id"])#line:1178
            if O00OO0O00O0O00O00 .result ['taskinfo']['task_type']=="4ftMiner":#line:1179
                OOOO00O00O000O000 =OOOO00O00O000O000 +" "+"{:5d}".format (OO0O0O00000O00000 ["params"]["base"])+" "+"{:.3f}".format (OO0O0O00000O00000 ["params"]["conf"])+" "+"{:+.3f}".format (OO0O0O00000O00000 ["params"]["aad"])#line:1180
                OOOO00O00O000O000 =OOOO00O00O000O000 +" "+OO0O0O00000O00000 ["cedents"]["ante"]+" => "+OO0O0O00000O00000 ["cedents"]["succ"]+" | "+OO0O0O00000O00000 ["cedents"]["cond"]#line:1181
            elif O00OO0O00O0O00O00 .result ['taskinfo']['task_type']=="CFMiner":#line:1182
                OOOO00O00O000O000 =OOOO00O00O000O000 +" "+"{:5d}".format (OO0O0O00000O00000 ["params"]["base"])+" "+"{:5d}".format (OO0O0O00000O00000 ["params"]["s_up"])+" "+"{:5d}".format (OO0O0O00000O00000 ["params"]["s_down"])#line:1183
                OOOO00O00O000O000 =OOOO00O00O000O000 +" "+OO0O0O00000O00000 ["cedents"]["cond"]#line:1184
            elif O00OO0O00O0O00O00 .result ['taskinfo']['task_type']=="SD4ftMiner":#line:1185
                OOOO00O00O000O000 =OOOO00O00O000O000 +" "+"{:5d}".format (OO0O0O00000O00000 ["params"]["base1"])+" "+"{:5d}".format (OO0O0O00000O00000 ["params"]["base2"])+"    "+"{:.3f}".format (OO0O0O00000O00000 ["params"]["ratioconf"])+"    "+"{:+.3f}".format (OO0O0O00000O00000 ["params"]["deltaconf"])#line:1186
                OOOO00O00O000O000 =OOOO00O00O000O000 +"  "+OO0O0O00000O00000 ["cedents"]["ante"]+" => "+OO0O0O00000O00000 ["cedents"]["succ"]+" | "+OO0O0O00000O00000 ["cedents"]["cond"]+" : "+OO0O0O00000O00000 ["cedents"]["frst"]+" x "+OO0O0O00000O00000 ["cedents"]["scnd"]#line:1187
            print (OOOO00O00O000O000 )#line:1189
        print ("")#line:1190
    def print_hypo (O00O0O00OOOO0O00O ,OO0O0000OOO0000OO ):#line:1192
        O00O0O00OOOO0O00O .print_rule (OO0O0000OOO0000OO )#line:1193
    def print_rule (O0OO00O00OO00O00O ,O0O000000OO0O000O ):#line:1196
        print ("")#line:1197
        if (O0O000000OO0O000O <=len (O0OO00O00OO00O00O .result ["rules"])):#line:1198
            if O0OO00O00OO00O00O .result ['taskinfo']['task_type']=="4ftMiner":#line:1199
                print ("")#line:1200
                O0O00O00O000OO000 =O0OO00O00OO00O00O .result ["rules"][O0O000000OO0O000O -1 ]#line:1201
                print (f"Rule id : {O0O00O00O000OO000['rule_id']}")#line:1202
                print ("")#line:1203
                print (f"Base : {'{:5d}'.format(O0O00O00O000OO000['params']['base'])}  Relative base : {'{:.3f}'.format(O0O00O00O000OO000['params']['rel_base'])}  CONF : {'{:.3f}'.format(O0O00O00O000OO000['params']['pim'])}  AAD : {'{:+.3f}'.format(O0O00O00O000OO000['params']['aad'])}  BAD : {'{:+.3f}'.format(O0O00O00O000OO000['params']['bad'])}")#line:1204
                print ("")#line:1205
                print ("Cedents:")#line:1206
                print (f"  antecedent : {O0O00O00O000OO000['cedents']['ante']}")#line:1207
                print (f"  succcedent : {O0O00O00O000OO000['cedents']['succ']}")#line:1208
                print (f"  condition  : {O0O00O00O000OO000['cedents']['cond']}")#line:1209
                print ("")#line:1210
                print ("Fourfold table")#line:1211
                print (f"    |  S  |  ¬S |")#line:1212
                print (f"----|-----|-----|")#line:1213
                print (f" A  |{'{:5d}'.format(O0O00O00O000OO000['params']['fourfold'][0])}|{'{:5d}'.format(O0O00O00O000OO000['params']['fourfold'][1])}|")#line:1214
                print (f"----|-----|-----|")#line:1215
                print (f"¬A  |{'{:5d}'.format(O0O00O00O000OO000['params']['fourfold'][2])}|{'{:5d}'.format(O0O00O00O000OO000['params']['fourfold'][3])}|")#line:1216
                print (f"----|-----|-----|")#line:1217
            elif O0OO00O00OO00O00O .result ['taskinfo']['task_type']=="CFMiner":#line:1218
                print ("")#line:1219
                O0O00O00O000OO000 =O0OO00O00OO00O00O .result ["rules"][O0O000000OO0O000O -1 ]#line:1220
                print (f"Rule id : {O0O00O00O000OO000['rule_id']}")#line:1221
                print ("")#line:1222
                print (f"Base : {'{:5d}'.format(O0O00O00O000OO000['params']['base'])}  Relative base : {'{:.3f}'.format(O0O00O00O000OO000['params']['rel_base'])}  Steps UP (consecutive) : {'{:5d}'.format(O0O00O00O000OO000['params']['s_up'])}  Steps DOWN (consecutive) : {'{:5d}'.format(O0O00O00O000OO000['params']['s_down'])}  Steps UP (any) : {'{:5d}'.format(O0O00O00O000OO000['params']['s_any_up'])}  Steps DOWN (any) : {'{:5d}'.format(O0O00O00O000OO000['params']['s_any_down'])}  Histogram maximum : {'{:5d}'.format(O0O00O00O000OO000['params']['max'])}  Histogram minimum : {'{:5d}'.format(O0O00O00O000OO000['params']['min'])}  Histogram relative maximum : {'{:.3f}'.format(O0O00O00O000OO000['params']['rel_max'])} Histogram relative minimum : {'{:.3f}'.format(O0O00O00O000OO000['params']['rel_min'])}")#line:1224
                print ("")#line:1225
                print (f"Condition  : {O0O00O00O000OO000['cedents']['cond']}")#line:1226
                print ("")#line:1227
                print (f"Histogram {O0O00O00O000OO000['params']['hist']}")#line:1228
            elif O0OO00O00OO00O00O .result ['taskinfo']['task_type']=="SD4ftMiner":#line:1229
                print ("")#line:1230
                O0O00O00O000OO000 =O0OO00O00OO00O00O .result ["rules"][O0O000000OO0O000O -1 ]#line:1231
                print (f"Rule id : {O0O00O00O000OO000['rule_id']}")#line:1232
                print ("")#line:1233
                print (f"Base1 : {'{:5d}'.format(O0O00O00O000OO000['params']['base1'])} Base2 : {'{:5d}'.format(O0O00O00O000OO000['params']['base2'])}  Relative base 1 : {'{:.3f}'.format(O0O00O00O000OO000['params']['rel_base1'])} Relative base 2 : {'{:.3f}'.format(O0O00O00O000OO000['params']['rel_base2'])} CONF1 : {'{:.3f}'.format(O0O00O00O000OO000['params']['conf1'])}  CONF2 : {'{:+.3f}'.format(O0O00O00O000OO000['params']['conf2'])}  Delta Conf : {'{:+.3f}'.format(O0O00O00O000OO000['params']['deltaconf'])} Ratio Conf : {'{:+.3f}'.format(O0O00O00O000OO000['params']['ratioconf'])}")#line:1234
                print ("")#line:1235
                print ("Cedents:")#line:1236
                print (f"  antecedent : {O0O00O00O000OO000['cedents']['ante']}")#line:1237
                print (f"  succcedent : {O0O00O00O000OO000['cedents']['succ']}")#line:1238
                print (f"  condition  : {O0O00O00O000OO000['cedents']['cond']}")#line:1239
                print (f"  first set  : {O0O00O00O000OO000['cedents']['frst']}")#line:1240
                print (f"  second set : {O0O00O00O000OO000['cedents']['scnd']}")#line:1241
                print ("")#line:1242
                print ("Fourfold tables:")#line:1243
                print (f"FRST|  S  |  ¬S |  SCND|  S  |  ¬S |");#line:1244
                print (f"----|-----|-----|  ----|-----|-----| ")#line:1245
                print (f" A  |{'{:5d}'.format(O0O00O00O000OO000['params']['fourfold1'][0])}|{'{:5d}'.format(O0O00O00O000OO000['params']['fourfold1'][1])}|   A  |{'{:5d}'.format(O0O00O00O000OO000['params']['fourfold2'][0])}|{'{:5d}'.format(O0O00O00O000OO000['params']['fourfold2'][1])}|")#line:1246
                print (f"----|-----|-----|  ----|-----|-----|")#line:1247
                print (f"¬A  |{'{:5d}'.format(O0O00O00O000OO000['params']['fourfold1'][2])}|{'{:5d}'.format(O0O00O00O000OO000['params']['fourfold1'][3])}|  ¬A  |{'{:5d}'.format(O0O00O00O000OO000['params']['fourfold2'][2])}|{'{:5d}'.format(O0O00O00O000OO000['params']['fourfold2'][3])}|")#line:1248
                print (f"----|-----|-----|  ----|-----|-----|")#line:1249
            else :#line:1250
                print ("Unsupported task type for rule details")#line:1251
            print ("")#line:1255
        else :#line:1256
            print ("No such rule.")#line:1257
