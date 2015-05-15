'''
Created on 2015. 5. 14.

@author: Jay
'''


class sqlMap:
    
    connectInfo = ("61.96.111.174", "niks12", "12345", "kiruda")
    
    selectStockInfo = " \
        SELECT \
            A.CODE, A.EXP1, A.EXP2, A.EXP3, A.EXP4, A.ARRAYNUM, B.URL1, B.URL2 \
        FROM \
            (SELECT \
                EXP1, EXP2, EXP3, EXP4, ARRAYNUM, SITECODE, CODE \
            FROM \
                SITE_DATA) A, \
            (SELECT \
                URL1, URL2, CODE \
            FROM \
                SITE_INFO) B \
        WHERE \
             A.SITECODE = B.CODE"

    insertStockData = " \
        INSERT INTO \
            %s ( %s ) \
        VALUES \
            ( %s )"
    
    selectStockCode = " \
        SELECT \
            * \
        FROM \
            STOCK_INFO\
        "
            