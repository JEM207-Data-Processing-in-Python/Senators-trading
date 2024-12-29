"""
This module contains the help functions for scraper.py module
"""
import pandas as pd
import numpy as np

# Tickers not found via yahoo finance
exclude_tickers = ['T$A', 'BRK.B', 'GLAS', 'GLA', 'WY.Z', 'LSXMA', 'LSXMK', 'WNRP', 'CHUY', 'BRKB', 'HZNP',
                    'CEQP', 'RGBM', 'EFC$D', 'FEI', 'PXD', 'BRP', 'VMW', 'BAC$I', 'NS', 'NYCB', 'ETRN', 'DUK$A',
                    'AMEH', 'ATVI', 'SGEN', 'FMBA', 'MMP', 'AAM$A', 'VGR', 'GPP', 'WTT', 'HEI.A', 'PEAK', 'EVBG',
                    'SGH', 'UBA', 'HHC', 'AYX', 'LSI', 'YAMHY', 'FRRVY', 'SMFKY', 'NCMGY', 'ITTOY', 'DISH', 'RDS.B',
                    'BBT', 'UTX', 'ARGO', 'SRE$A', 'ABB', 'WBK', 'SIRE', 'AQUA', 'MRTX', 'KRTX', 'CONN', 'VIV.V',
                    'CEMCF', 'NCMGF', 'AUY', 'LMST', 'FLT', 'FRC', 'SIVB', 'CSII', 'CNHI', 'DPSGY', 'CS', 'RTN',
                    'SILK', 'PACW', 'TOSYY', 'CANO', 'BRK.A', 'SPWR', 'SWAV', 'SYNH', 'MAXR', 'ESALY', 'RDSMY',
                    'TELL', 'MNRL', 'RNWK', 'BLL', 'CLR', 'TIF', 'BKI', 'DSEY', 'SSLTY', 'HFC', 'CTRL', 'HSAC',
                    'SI', 'TLRN', 'ENOB', 'BCEL', 'COUP', 'TWTR', 'ISEE', 'VTNR', 'BRMK', 'FB', 'CCXI', 'BRCM',
                    'NID', 'CVET', 'ABMD', 'ECOM', 'WRK', 'VTRSV', 'GNKOQ', 'ASBC', 'ESTE', 'CDEV', 'BKEPP',
                    'VIAC', 'HIL', 'PYPLV', 'MS$P', 'RTL', 'PLAN', 'CPE', 'NEX', 'LHCG', 'CERN', 'MTBC', 'Y',
                    'DRE', 'ECOL', 'TCF', 'SDC', 'NEE$Q', 'T+A', 'SKHCY', 'NTT', 'VOLVY', 'DNHBY', 'TACO',
                    'PBCT', 'KMI.W', 'AZSEY', 'IAA', 'ANTM', 'DISCA', 'PSXP', 'DWDP', 'NUVA', 'ABC','PBFX',
                    'BF.B', 'HTZWW', 'AXHE', 'AXTE', 'SRLP', 'SPLK', 'ASXC', 'BKEP', 'WRK.V', 'IS', 'SCU',
                    'CEM', 'SHLX', 'ORCC', 'CTAA', 'UN', 'OFC', 'CONE', 'KPLTW', 'ENBL', 'TSS', 'GPS', 'DWAC',
                    'WLTW', 'CREE', 'GCGMF', 'AVYA', 'RLGY', 'SOLO', 'IPHI', 'JMP', 'FEYE', 'ECA', 'XON', 'BAF',
                    'TOT', 'MNK', 'PCLN', 'CDK', 'ESGC', 'LMRK', 'DMTK', 'APPAD', 'PCPL', 'GFN', 'CSLT', 'APEN',
                    'CMLFU', 'VIVO', 'BLFSD', 'NVIGF', 'FLXN', 'TLND', 'TRHC', 'ORAN', 'ALXN', 'NLOK', 'LTD',
                    'RDSA', 'ROLL', 'QTS', 'BREW', 'FDRXX', 'CNR', 'STOR', 'CCC', 'ALYF', 'AESE', 'FFG', 'TRIT',
                    'MANT', 'STAY', 'LL', 'VVNT', 'BRKS', 'CMLTU', 'BOWX', 'TPCO', 'VAR', 'GSS', 'NUAN', 'BPMP',
                    'RDS.A', 'DGNR', 'ACST', 'APHA', 'LUKOY', 'CLGX', 'SC', 'HRC', 'WYND', 'XEC', 'ATH', 'UNVR',
                    'PFPT', 'GRUB', 'QUMU', 'CMLF', 'WPX', 'POEFF', 'CEMI', 'NEWR', 'TCO', 'AMBR', 'RHT', 'ARNA',
                    'LMACU', 'FSKR', 'RETA', 'ZOOM', 'NYMX', 'WAIR', 'CHNG', 'NGLS', 'JIH', 'EVOP', 'AJRD', 'PSTH',
                    'FLIR', 'DNKN', 'PRAH', 'CCMP', 'HDS', 'ARNC', 'CTXS', 'SNE', 'CHL', 'BGG', 'SWN', 'CATM', 'RAD',
                    'WORK', 'VRTU', 'GMLP', 'AGN', 'CTRCF', 'NBL', 'SMLP', 'CAJ', 'TLSYY', 'MRWSY', 'ANZBY', 'MFGP',
                    'ATASY', 'NTXFY', 'WOPEY', 'GLOP', 'GWPH', 'XLNX', 'CRY', 'EBSB', 'CDAY', 'YNDX', 'ETFC', 'NBLX',
                    'AVLR', 'SVCBY', 'PKI', 'DRQ', 'CCXX', 'SPKE', 'SKVKY', 'RXN', 'MINI', 'DCP', 'TMUSR', 'FFHRX',
                    'MSBHY', 'VSLR', 'LTHM', 'LEN.B', 'CMD', 'ADS', 'GLIBA', 'LBDAV', 'AIMC', 'BIF', 'CTL', 'TCP',
                    'EQM', 'PS', 'DISCK', 'HCN', 'FPL', 'DEACU', 'SNP', 'RP', 'FII', 'TMK', 'SRC', 'NATI', 'BAMXY',
                    'FBC', 'GBT', 'BXS', 'APC', 'CXP', 'UMPQ', 'ZEN', 'LLL', 'PDCE', 'SCHN', 'VCRA', 'BIG', 'WDR',
                    'DOOR', 'RCII', 'XENT', 'CTB', 'PSB', 'AOBC', 'PEGI', 'AAN', 'MTSC', 'HTA', 'SZEVY', 'WCAGY',
                    'CCLAY', 'HLUYY', 'RBS', 'PDYPY', 'SWMAY', 'PCRFY', 'GEAGY', 'BBBY', 'WMGI', 'KL', 'POL', 'HZN',
                    'PRSP', 'WCG', 'CELG', 'GSAH', 'GRA', 'GCP', 'LPT', 'CLNC', 'NLSN', 'CBS', 'MYL', 'VIAB', 'SPN',
                    'DDAIF', 'IBKC', 'SIX', 'ERI', 'TWOU', 'AYR', 'CBM', 'MN', 'IIVI', 'TVTY', 'GFSZY', 'SNH', 'DNSKY',
                    'CLNY', 'SEMG', 'ETM', 'LM', 'BPL', 'MGP', 'COT', 'UPMKY', 'MDSO', 'JEC', 'TUP', 'WP', 'ANDX',
                    'HUB.A', 'WAGE', 'FDC', 'PDRDY', 'OOCP', 'RYDBF', 'GMXAY', 'NJ', 'WBC', 'AVP', 'HPT', 'UBNT',
                    'NTDMF', 'II', 'ADSW', 'ULTI', 'TFCFA', 'TFCF', 'CTRP', 'BGCP', 'PNM', 'JCOM', 'HA', 'AHONY',
                    'WGHPY', 'CHEUY', 'ELLI', 'HRS', 'PER', 'MSG', 'ORBK', 'DPLO', 'ZAYO', 'ATHN', 'APU', 'CNXM',
                    'SPKEP', 'CINR', 'UFS', 'BEL', 'LABL', 'TNTOF', 'SNHY', 'PETQ', 'CXO', 'ARRS', 'ESL', 'MIC',
                    'STAR', 'LN', 'NRBAY', 'GOV', 'INGIY', 'AMCRY', 'SMTA', 'BKCC', 'WBT', 'ARAV', 'WGP', 'BBL',
                    'AMGP', 'PTLA', 'BBAVY', 'BHGE', 'SAFM', 'NRZ', 'TKPYY', 'TI', 'CDR', 'MTZPY', 'ACGPF', 'VSM',
                    'CBLK', 'ABX', 'RVI', 'IDTI', 'DLPH', 'CCH', 'LOGM', 'HIBB', 'WPG', 'CCP', 'TLRD', 'TANN', 'TIS',
                    'GOOCV', 'KSU', 'OZM', 'NYLD', 'IIN', 'NILSY', 'LNEGY', 'ACC', 'RAI', 'TGE', 'TEUM', 'BONT',
                    'DXTR', 'TRXC', 'NEOT', 'NETE', 'LBIX', 'INFI', 'OTIC', 'ITEK', 'ARCI', 'CYTR', 'TEAR', 'AEZS',
                    'CBAY', 'ZN', 'CLSN', 'FNBC', 'OCN', 'OZRK', 'VRAY', 'MIK', 'TTM', 'APY', 'CHK', 'ACXM', 'CLNS',
                    'BT', 'LVNTA', 'CVA', 'FTSI', 'DPS', 'FNGN', 'APTS', 'CBG', 'VER', 'HIFR', 'PEI', 'JCAP', 'VNTV',
                    'TNTR', 'TNTR', 'AXE', 'OAK', 'FIT', 'OREX', 'TEGP', 'FSD', 'ESV', 'AFT', 'INWK', 'LKSD', 'ITYBY',
                    'LVLT', 'PHLD', '^MWE', '^RGP', 'MRLN', 'CSGKF', 'WFM', 'WIN', 'TUES', 'ELGX', 'ZIOP', 'SGBK', 'SCX',
                    'SPLS', 'WTR', 'WPPGY', 'NPSND', 'BCR', 'Q', 'SRF', 'EXXI', 'MBFI', 'RAS', 'FTR', 'ABDC', 'SHPGF',
                    'OKS', 'WLL', 'QIHU', 'NRF', 'NRE', 'SZYM', 'AINV', 'MCC', 'TLLP', 'JCS', 'CST', 'MDC', 'MXIM', 'COH',
                    'GTOMY', 'JHB', 'POT', 'CWEI', 'LCI', 'QTM', 'PE', 'PRXL', 'JNS', 'ARG', 'MGU', 'CMCSK', 'LLTC', 'WETF',
                    'AGU', 'VSAR', 'MJN', 'BABY', 'SXL', 'FCGYF', 'AQFH', 'WFT', 'IMGN', 'BXLT', 'CLMS', 'COG', 'WSH', 'NSR',
                    'PLM', 'STRZA', 'TGP', 'HBHC', 'ZNGA', 'SCTY', 'DRYS', 'IQNT', 'FGP', 'JCP', 'IXYS', 'DPM', 'NHF', 'SYRG',
                    'LEXEA', 'ENH', 'UNRDY', 'TYC', 'MDVN', 'ELRC', 'STON', 'HYH', 'MON', 'GCAP', 'TECO', 'XLS', 'OCR',
                    'MRKT', 'AXLL', 'LMCA', 'XPOI', 'ACMP', 'MXWL', 'FLTX', 'RAVN', 'SSNI', 'UA.C', 'CPGX', 'SHOS', 'GG',
                    'PLGTF', 'SLW', 'KKD', 'IRLBF', 'AIRM', 'TWC', 'SNDK', 'BKJAY', 'LNKD', 'STJ', 'TFM', 'CVSL', 'CEB', 'CLC',
                    'ETE', 'DCM', 'SWH', 'BHI', 'FMCMF', 'DDR', 'DD.PA', 'CIU', 'PCP', 'IM', 'ACE', 'COV', 'CAB', 'GAS', 'BUNT',
                    'TEG', 'BIN', 'BURFX', 'DNO', 'TCAP']


# TODO error handling, tests
def senators_data_preparation(data: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the scrapped senators data and extract all relevant information
    Args:
        data: pd.DataFrame - The senators data to be cleaned and transformed.
    Returns:
        pd.DataFrame - The cleaned data.
    """

    # Extract the "Type" and "Amount" from the "Transaction" column
    data["Amount"] = data["Amount"].str.replace("[$,]", "", regex=True)
    data[["Min", "Max"]] = data["Amount"].str.split(" - ", expand=True)
    data[["Min", "Max"]] = data[["Min", "Max"]].apply(pd.to_numeric, errors="coerce")

    # Change to the datetime format for "Traded" and "Filed"
    data["Traded"] = pd.to_datetime(data["Traded Date"], format="%b %d, %Y").dt.strftime("%Y-%m-%d")
    data["Filed"] = pd.to_datetime(data["Filed Date"], format="%b %d, %Y").dt.strftime("%Y-%m-%d")

    # Calculate the adjusted investment, since sale should decrease your total invested amount
    data["Invested"] = np.where(
                                data["Transaction"] == "Purchase",
                                (data["Min"] + data["Max"]) / 2,
                                -(data["Min"] + data["Max"]) / 2
                        )

    # Drop the unnecessary columns
    data.drop(columns=["Amount", "Min", "Max", "Traded Date", "Filed Date"], inplace=True)
    
    # Drop all with tickers longer then 5 characters
    data = data[(data["Ticker"].str.len() <= 5) & (~data["Ticker"].isin(exclude_tickers))]

    return data


# TODO error handling, tests
def fin_history_preparation(data: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the history financial market data
    Args:
        data: pd.DataFrame - The history data to be cleaned.
    Returns:
        pd.DataFrame - The cleaned history data.
    """

    # Keep only the "Close" and "Date" columns
    data = data[["Close", "Date"]]

    # Round the values
    data["Close"] = data["Close"].round(2)

    # Change the date format
    data["Date"] = pd.to_datetime(data["Date"]).dt.strftime("%Y-%m-%d")
    data = data[pd.to_datetime(data["Date"]).dt.year >= 2013]

    return data


# TODO error handling, tests
def fin_info_preparation(data: pd.DataFrame) -> pd.DataFrame:
    """
    The function choose only the relevant columns from the financial information
    Args:
        data: pd.DataFrame - The financial information to be cleaned.
    Returns:
        pd.DataFrame - The cleaned fiancial data.
    """
    # list of columns of interests
    relevant_columns = ["Ticker", "quoteType", "longName","shortName",
                        "city", "country", "industryKey", "sectorKey",
                        "longBusinessSummary", "financialCurrency", "currency"
                        ]
    relevant_columns = [col for col in relevant_columns if col in data.columns]
    data = data[relevant_columns]

    return data


# TODO error handling, tests
def fin_ticker_preparation(data: pd.DataFrame) -> pd.DataFrame:
    """
    Remove the tickers that are not found via yahoo
    Args:
        data: pd.DataFrame - The tickers to be filtered.
    Returns:
        pd.DataFrame - The cleaned Tickers.
    """

    data = [ticker for ticker in data if ticker not in exclude_tickers]

    return data
