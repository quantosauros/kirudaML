'''
Created on 2015. 5. 14.

@author: Jay
'''


class sqlMap:
    
    connectInfo = ("61.96.111.175", "niks12", "1qaz2wsx", "kiruda")
    
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
            AND A.XPATH = '%s'\
        ORDER BY A.ARRAYNUM"
        
    SELECTTRADERINFO_XPATH = " \
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
            AND A.XPATH = 'xpath_da_trader01'\
        ORDER BY A.ARRAYNUM"
    
    SELECTFRGNINFO_XPATH = " \
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
            AND A.XPATH = 'xpath_na_frgn01'\
        ORDER BY A.ARRAYNUM"
    
    SELECTINVESTORINFO_XPATH = " \
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
            AND A.XPATH = 'xpath_krx_investor01'\
        ORDER BY A.ARRAYNUM"
    
    SELECTSTOCKLISTINFO_XPATH = " \
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
            AND A.XPATH = 'xpath_krx_stockList'\
        ORDER BY A.ARRAYNUM"
    
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
    
    insertStockData = " \
        INSERT INTO \
            %s ( %s ) \
        VALUES \
            ( %s )"
            
    insertStockSisaeData =  " \
        INSERT INTO \
            stock_sisae ( %s ) \
        VALUES \
            ( %s ) \
        ON DUPLICATE KEY UPDATE \
            LOANDONE = IF(VALUES(LOANDONE) IS NOT NULL,VALUES(LOANDONE),LOANDONE), \
            LOANCLEAN = IF(VALUES(LOANCLEAN) IS NOT NULL,VALUES(LOANCLEAN),LOANCLEAN), \
            LOANBALANCEVOL = IF(VALUES(LOANBALANCEVOL) IS NOT NULL,VALUES(LOANBALANCEVOL),LOANBALANCEVOL), \
            LOANBALANCENTL = IF(VALUES(LOANBALANCENTL) IS NOT NULL,VALUES(LOANBALANCENTL),LOANBALANCENTL), \
            SHORTVOLUMERATIO = IF(VALUES(SHORTVOLUMERATIO) IS NOT NULL,VALUES(SHORTVOLUMERATIO),SHORTVOLUMERATIO), \
            SHORTVOLUME = IF(VALUES(SHORTVOLUME) IS NOT NULL,VALUES(SHORTVOLUME),SHORTVOLUME), \
            SHORTNOTIONAL = IF(VALUES(SHORTNOTIONAL) IS NOT NULL,VALUES(SHORTNOTIONAL),SHORTNOTIONAL)"
            
    INSERTDATAWITHOUTPARENTHESES = "\
        INSERT INTO \
            %s  %s \
        VALUES \
            %s "
    
    selectStockCode = " \
        SELECT \
            CODE, TICKER, MARKET, KRXCODE, NAME\
        FROM \
            STOCK_INFO "
        
    selectDataInfo = " \
        SELECT \
            CODE, UNIT, CCY_CD \
        FROM \
            DATA_INFO \
        WHERE \
            SITECODE = '%s' \
            AND CODE = '%s' "
        
    selectXpathInfo = "\
        SELECT \
            XPATH \
        FROM \
            XPATH_INFO \
        WHERE \
            CODE = '%s' "
    
    INSERTSTOCKLIST = " \
        INSERT INTO\
            STOCK_INFO\
            (CODE, TICKER, MARKET, KRXCODE, NAME, COUNTRYCODE, CREATE_DATE) \
        VALUES \
            %s \
        ON DUPLICATE KEY UPDATE \
            CODE = VALUES(CODE), \
            TICKER = VALUES(TICKER), \
            MARKET = VALUES(MARKET), \
            KRXCODE = VALUES(KRXCODE), \
            NAME = VALUES(NAME), \
            COUNTRYCODE = VALUES(COUNTRYCODE), \
            mod_date = NOW() "
    
    INSERTINVESTINDEXDATA = "\
        INSERT INTO\
            stock_sisae_test\
            (code,date,designated, EPS,PER,BPS,PBR,dividendAmount, dividendPercent) \
        VALUES \
            %s \
        ON DUPLICATE KEY UPDATE \
            designated = VALUES(designated), \
            EPS = VALUES(EPS), \
            PER = VALUES(PER), \
            BPS = VALUES(BPS), \
            PBR = VALUES(PBR), \
            dividendAmount = VALUES(dividendAmount), \
            dividendPercent = VALUES(dividendPercent)"
    
    INSERTFOREIGNDATA = "\
        INSERT INTO\
            stock_sisae_test\
            (code,date,foreignLimitStock, foreignHoldingStock) \
        VALUES \
            %s \
        ON DUPLICATE KEY UPDATE \
            foreignLimitStock = VALUES(foreignLimitStock), \
            foreignHoldingStock = VALUES(foreignHoldingStock)"
    
    INSERTSHORTSALEDATA = "\
        INSERT INTO\
            stock_sisae_test\
            (code,date,shortVolume, shortNotional) \
        VALUES \
            %s \
        ON DUPLICATE KEY UPDATE \
            shortVolume = VALUES(shortVolume), \
            shortNotional = VALUES(shortNotional)"
    
    
    INSERTFRGNDATA = " \
        INSERT INTO \
            STOCK_SISAE \
            (CODE, DATE, NETVOLUME_INSTITUTION, NETVOLUME_FOREIGN, foreignHoldingStock, FOREIGNSTOCKHOLDINGPERCENT) \
        VALUES \
            %s \
        ON DUPLICATE KEY UPDATE \
            NETVOLUME_INSTITUTION = VALUES(NETVOLUME_INSTITUTION), \
            NETVOLUME_FOREIGN = VALUES(NETVOLUME_FOREIGN), \
            foreignHoldingStock = VALUES(foreignHoldingStock), \
            FOREIGNSTOCKHOLDINGPERCENT = VALUES(FOREIGNSTOCKHOLDINGPERCENT)"
        
    SELECTTRADERINFO = "\
        SELECT \
            * \
        FROM \
            TRADER_INFO"
        
    SELECTINVESTORINFO = "\
        SELECT \
            * \
        FROM \
            INVESTOR_INFO \
        ORDER BY NUM"  