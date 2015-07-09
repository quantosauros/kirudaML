'''
Created on 2015. 5. 14.

@author: Jay
'''


class sqlMap:
    
    connectInfo = ("61.96.111.175", "niks12", "1qaz2wsx", "kiruda")
    
    #SELECT QUERY    
    SELECTPARSEINGINFO = " \
        CALL PC_SLT_PARSINGINFO('%s')"

    SELECTSTOCKCODE = " \
        CALL PC_SLT_STOCKCODE()"
        
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
        
    SELECTGICSINFO = " \
        SELECT \
            CODE \
        FROM \
            GICS_INFO \
        WHERE \
            TYPE ='IG'"
    
    #UPDATE QUERY
    UPDATEGICSDATA = "\
        UPDATE \
            STOCK_INFO \
        SET \
            GICS = %s \
        WHERE \
            TICKER IN \
            %s"

    #INSERT QUERY
    INSERTDATAWITHOUTPARENTHESES = "\
        INSERT INTO \
            %s  %s \
        VALUES \
            %s "
    
    INSERTSTOCKLIST = " \
        INSERT INTO\
            STOCK_INFO\
            (CODE, TICKER, MARKET, KRXCODE, NAME, COUNTRYCODE, CREATE_AT) \
        VALUES \
            %s \
        ON DUPLICATE KEY UPDATE \
            CODE = VALUES(CODE), \
            TICKER = VALUES(TICKER), \
            MARKET = VALUES(MARKET), \
            KRXCODE = VALUES(KRXCODE), \
            NAME = VALUES(NAME), \
            COUNTRYCODE = VALUES(COUNTRYCODE), \
            UPDATE_AT = NOW() "
    
    INSERTINVESTINDEXDATA = "\
        INSERT INTO\
            STOCK_SISAE\
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
            STOCK_SISAE\
            (code,date,foreignLimitStock, foreignHoldingStock) \
        VALUES \
            %s \
        ON DUPLICATE KEY UPDATE \
            foreignLimitStock = VALUES(foreignLimitStock), \
            foreignHoldingStock = VALUES(foreignHoldingStock)"
    
    INSERTSHORTSALEDATA = "\
        INSERT INTO\
            STOCK_SISAE\
            (code,date,shortVolume, shortNotional) \
        VALUES \
            %s \
        ON DUPLICATE KEY UPDATE \
            shortVolume = VALUES(shortVolume), \
            shortNotional = VALUES(shortNotional)"
    
        