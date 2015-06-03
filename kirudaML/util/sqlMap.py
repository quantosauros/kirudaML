'''
Created on 2015. 5. 14.

@author: Jay
'''


class sqlMap:
    
    connectInfo = ("61.96.111.174", "niks12", "12345", "kiruda")
    
    selectStockInfo = " \
        SELECT \
            A.CODE, A.XPATH, A.ARRAYNUM, B.URL1, B.URL2, A.DATANAME, A.SITECODE \
        FROM \
            (SELECT \
                XPATH, ARRAYNUM, SITECODE, CODE, DATANAME, YN\
            FROM \
                SITE_DATA) A, \
            (SELECT \
                URL1, URL2, CODE \
            FROM \
                SITE_INFO) B \
        WHERE \
             A.SITECODE = B.CODE\
             AND A.YN = 'Y'"

    SELECTSITEDATA_XPATH = "\
        SELECT \
            DISTINCT(XPATH) \
        FROM \
            SITE_DATA \
        WHERE \
            YN = 'Y' \
            AND DATATYPE = '%s'"
    
    SELECTPARSEINGINFO = " \
        SELECT \
            A.DATANAME, B.URL1, B.URL2, C.XPATH, A.ARRAYNUM \
        FROM \
            SITE_DATA A, \
            SITE_INFO B, \
            XPATH_INFO C \
        WHERE \
            C.CODE = A.XPATH \
            AND B.CODE = A.SITECODE \
            AND A.YN = 'Y' \
            AND A.XPATH = '%s'"

    selectSiteDataDaily = " \
        SELECT \
            A.CODE, A.XPATH, A.ARRAYNUM, B.URL1, B.URL2, A.DATANAME, A.SITECODE \
        FROM \
            (SELECT \
                XPATH, ARRAYNUM, SITECODE, CODE, DATANAME, YN, DATATYPE\
            FROM \
                SITE_DATA) A, \
            (SELECT \
                URL1, URL2, CODE \
            FROM \
                SITE_INFO) B \
        WHERE \
             A.SITECODE = B.CODE\
             AND A.YN = 'Y'\
             AND A.DATATYPE IN ('D')"    
    
    selectStockListUpdate = "\
        SELECT \
            A.CODE, A.XPATH, A.ARRAYNUM, B.URL1, B.URL2, A.DATANAME, A.SITECODE \
        FROM \
            (SELECT \
                XPATH, ARRAYNUM, SITECODE, CODE, DATANAME, YN, DATATYPE\
            FROM \
                SITE_DATA) A, \
            (SELECT \
                URL1, URL2, CODE \
            FROM \
                SITE_INFO) B \
        WHERE \
             A.SITECODE = B.CODE\
             AND A.YN = 'Y'\
             AND A.DATANAME IN ('KS','KQ')"

    selectStockListMAX = "\
        SELECT \
            A.CODE, A.XPATH, A.ARRAYNUM, B.URL1, B.URL2, A.DATANAME, A.SITECODE \
        FROM \
            (SELECT \
                XPATH, ARRAYNUM, SITECODE, CODE, DATANAME, YN, DATATYPE\
            FROM \
                SITE_DATA) A, \
            (SELECT \
                URL1, URL2, CODE \
            FROM \
                SITE_INFO) B \
        WHERE \
             A.SITECODE = B.CODE\
             AND A.YN = 'Y'\
             AND A.DATANAME IN ('KS_MAX','KQ_MAX')"


    insertStockData = " \
        INSERT INTO \
            %s ( %s ) \
        VALUES \
            ( %s )"
    
    selectStockCode = " \
        SELECT \
            CODE, TICKER, MARKET \
        FROM \
            STOCK_INFO\
        "
        
    selectDataInfo = " \
        SELECT \
            CODE, UNIT, CCY_CD \
        FROM \
            DATA_INFO \
        WHERE \
            SITECODE = '%s' \
            AND CODE = '%s' \
        "
    selectXpathInfo = "\
        SELECT \
            XPATH \
        FROM \
            XPATH_INFO \
        WHERE \
            CODE = '%s' \
    "
        
        
        
        
        