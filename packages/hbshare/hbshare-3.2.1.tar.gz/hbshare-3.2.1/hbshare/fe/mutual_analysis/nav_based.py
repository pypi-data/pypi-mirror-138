import datetime
import pandas as pd
import numpy as np
from hbshare.fe.XZ import db_engine


localdb=db_engine.PrvFunDB().engine
hbdb=db_engine.HBDB()


def get_monthly_jjnav(jjdm):

    #get the nav ret  for given jjdm and time zone(already times 100)
    sql="select jjdm,tjyf,rqzh,hb1y from st_fund.t_st_gm_yhb where jjdm ='{0}' and rq1y!=99999  "\
        .format(jjdm)
    navdf=hbdb.db2df(sql, db='funduser')

    max_yearmonth=navdf['tjyf'].max()
    min_yearmonth=navdf['tjyf'].min()

    return navdf,max_yearmonth,min_yearmonth

def get_benchmark_ret():

    sql="select zqdm,tjyf,rqzh,hb1y from st_market.t_st_zs_yhb where zqdm='000002' and abs(hb1y)!=99999 "

    benchmark_ret=hbdb.db2df(sql, db='alluser')

    benchmark_ret['med']=99999
    benchmark_ret['scenario'] = ''
    for i in range(1,len(benchmark_ret)):
        benchmark_ret.loc[i,'med']=benchmark_ret.loc[0:i-1]['hb1y'].median()
        if(benchmark_ret.loc[i,'med']>=benchmark_ret.loc[i,'hb1y']):
            benchmark_ret.loc[i, 'scenario']='opt'
        else:
            benchmark_ret.loc[i, 'scenario'] = 'pes'

    return  benchmark_ret[['scenario','hb1y','tjyf']]

def bhar(arr):
    return 100*(np.power(np.cumprod((arr+100)/100).tolist()[-1],1/12)-1)

def pessimistic_ret(jjdm):

    navdf,max_yearmonth,min_yearmonth=get_monthly_jjnav(jjdm)

    navdf=pd.merge(navdf,benchmark_ret,how='left',on='tjyf')

    navdf['ext_ret']=navdf['hb1y_x']-navdf['hb1y_y']

    #last 12 month average month return by calculating last 12 month cul ret and turn it into month return

    temp=navdf[navdf['scenario']=='pes']['ext_ret'].rolling(12).apply(bhar)
    temp=temp.to_frame('pes_ext_ret')
    navdf=pd.merge(navdf,temp,how='left',left_index=True, right_index=True)

    temp=navdf[navdf['scenario']=='opt']['ext_ret'].rolling(12).apply(bhar)
    temp=temp.to_frame('opt_ext_ret')
    navdf=pd.merge(navdf,temp,how='left',left_index=True, right_index=True)

    navdf['ext_ret'] = navdf['ext_ret'].rolling(12).apply(bhar)


    last_pes_ret=np.nan
    last_opt_ret=np.nan

    for i in range(0,len(navdf)):
        if(navdf.loc[i]['pes_ext_ret']==navdf.loc[i]['pes_ext_ret']):
            last_pes_ret=navdf.loc[i]['pes_ext_ret']

        else:
            navdf.loc[i,'pes_ext_ret']=last_pes_ret

        if(navdf.loc[i]['opt_ext_ret']==navdf.loc[i]['opt_ext_ret']):
            last_opt_ret=navdf.loc[i]['opt_ext_ret']

        else:
            navdf.loc[i,'opt_ext_ret']=last_opt_ret

    navdf=navdf[navdf['ext_ret'].notnull()]

    for col in['ext_ret','pes_ext_ret','opt_ext_ret']:
        navdf[col] = (navdf[col]/100).astype(float).map("{:.2%}".format)

    return navdf[['jjdm','tjyf','rqzh','ext_ret','pes_ext_ret','opt_ext_ret']]




if __name__ == '__main__':

    sql = "select distinct jjdm from st_fund.t_st_gm_jjxx where  cpfl='2' and (jjfl='1' or (jjfl='3' and (ejfl='35' or ejfl='37'))) "
    stock_jjdm_list = hbdb.db2df(sql, db='funduser')['jjdm'].tolist()
    stock_jjdm_list.sort()
    benchmark_ret = get_benchmark_ret()
    for jjdm in stock_jjdm_list:
        scenario_ret=pessimistic_ret(jjdm)