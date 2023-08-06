import numpy as np
import pandas as pd
from hbshare.fe.XZ import db_engine as dbeng
from hbshare.fe.XZ import functionality
import datetime

until=functionality.Untils()
hbdb=dbeng.HBDB()



def grouping(df,factor_name,date_list):


    group_dict=dict()
    for date in date_list:
        temp=df[df['date']==date]
        temp['rank']=temp[factor_name].rank()
        temp=temp.sort_values('rank')

    print('')


def single_factor_ic(df,factor_name,fund_flag=True):

    date_list = df['date'].unique().tolist()
    date_list.sort()
    ic_df=pd.DataFrame()
    ic_df['date']=date_list[0:-1]
    ic_list=[]

    if(fund_flag):
        ticker_ret=pd.DataFrame()
        for i in range(len(date_list)-1):
            factor_date=date_list[i]
            #ret_date = (datetime.datetime.strptime(factor_date, '%Y%m%d')+ datetime.timedelta(days=91)).strftime('%Y%m%d')
            ret_date=date_list[i+1]
            ticker_list = df[df['date']==factor_date]['jjdm'].unique().tolist()
            ticker_con = until.list_sql_condition(ticker_list)
            sql="select jjdm,jzrq,zbnp from st_fund.t_st_gm_rqjhb where zblb='2103' and jjdm in ({0}) and jzrq ='{1}'"\
                .format(ticker_con,ret_date)
            tempdf=hbdb.db2df(sql,db='funduser')
            tempdf['rank_ret']=tempdf['zbnp'].rank()
            ticker_ret=pd.concat([ticker_ret,tempdf],axis=0)

            ic_list.append((tempdf['rank_ret'].reset_index(drop=True)).corr(df[df['date']==factor_date][factor_name].rank().reset_index(drop=True)))

    ic_df['ic']=ic_list
    grouping(df, factor_name, date_list)

    print('the average ic is {0}, the pro that ic >0 is {1},the IR of the factor is{2} '
          .format(ic_df['ic'].describe()['mean'],sum(ic_df['ic']>0)/len(ic_df),ic_df['ic'].describe()['mean']/ic_df['ic'].describe()['std'] ))


if __name__ == '__main__':

    localdb=dbeng.PrvFunDB().engine


    #pess scenario return factor ic test
    # factor_name='t3_ret'
    # sql="select jjdm,added_date,avg(ret) as {0} from new_joinner_ret  where qt='t3' GROUP BY jjdm,added_date "\
    #     .format(factor_name)
    #
    # raw_df=pd.read_sql(sql,con=localdb)
    # raw_df.rename(columns={'added_date':'date'},inplace=True)
    # raw_df[factor_name]=[np.nan] + raw_df[factor_name][1:].tolist()
    #
    # raw_df=raw_df[raw_df['date']!='20160331']
    # #take the last 3years mean t_ret as factor
    # raw_df['new_join_'+factor_name] = raw_df.groupby(by='jjdm',as_index=False)[factor_name].rolling(12, 1).mean().values
    # single_factor_ic(raw_df,factor_name='new_join_'+factor_name,fund_flag=True)


    #brinson ability ic test
    sql="select * from brinson_score "
    raw_df=pd.read_sql(sql,con=localdb)
    single_factor_ic(raw_df, factor_name='short_term_equity', fund_flag=True)


