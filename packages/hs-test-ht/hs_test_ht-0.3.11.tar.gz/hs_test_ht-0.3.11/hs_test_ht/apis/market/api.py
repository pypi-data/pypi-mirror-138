import os,sys

from functools import wraps
from concurrent.futures import ThreadPoolExecutor

com_path = os.path.dirname(os.path.abspath(__file__))

sys.path.append(com_path)
sys.path.append(f'{com_path}/com')
sys.path.append(f"{com_path}/com/model")
sys.path.append(f"{com_path}/com/interface")
sys.path.append(f"{com_path}/com/libs")

from model import MarketData_pb2 as MarketData
from model import MDQuery_pb2 as MDQuery
from model import InsightErrorContext_pb2 as InsightErrorContext
from model import EMarketDataType_pb2 as EMarketDataType
from model import ESecurityIDSource_pb2 as ESecurityIDSource
from model import ESecurityType_pb2 as ESecurityType
from model import MDPlayback_pb2 as MDPlayback
from model import MDSubscribe_pb2 as MDSubscribe
from interface import mdc_gateway_interface as mdc_gateway_interface
from data_handle import OnRecvMarkertData
from data_handle import get_interface




class HsInsight(object):

    def __init__(self, username = '', pwd = '', backuplist= ['221.226.112.140','153.3.219.107'], ip='221.131.138.171', port=9362):
        self.username = username
        self.pwd = pwd
        self.backuplist = backuplist
        self.ip = ip
        self.port = port

        self.thread_pool = ThreadPoolExecutor()

        istoken = False
        certfolder = f"{com_path}/com/cert"
        backup_list = mdc_gateway_interface.BackupList()

        # 流量与日志开关设置
        # open_trace trace流量日志开关 # params:open_file_log 本地日志文件开关  # params:open_cout_log 控制台日志开关
        get_interface().init(False, False, False)

        #用set便于后续扩展
        self.market_callbacks = set()

        self.callback = OnRecvMarkertData()

        get_interface().setCallBack(self.callback)

        # backup_list 备选ip列表
        for backup_node in self.backuplist:
            backup_list.Add(backup_node, self.port)
        get_interface().login(self.ip, self.port, self.username, self.pwd, istoken, certfolder,backup_list)

    #OnMarketData的修饰函数,无修饰则用默认OnMarketData,处理订阅的数据,部分查询回调里面也会调用这个回调
    def hs_on_market_data(self, func):

        def callback_func(record):
            self.thread_pool.submit(func, record)

        self.callback.OnMarketData = callback_func

        @wraps(func)
        def decorator(*args, **kwargs):
            """ should receive a message-value parameter """
            return func(*args, **kwargs)

        return decorator

    #OnPlaybackPayload的修饰函数,无修饰则用默认OnPlaybackPayload，处理回测返回的数据
    def hs_on_playback_payload(self,func):
        self.callback.OnPlaybackPayload = func

        @wraps(func)
        def decorator(*args, **kwargs):
            """ should receive a message-value parameter """
            return func(*args, **kwargs)

        return decorator

    # OnPlaybackStatus 的修饰函数,无修饰则用默认 OnPlaybackStatus，处理回测的状态
    def hs_on_playback_status(self,func):
        self.callback.OnPlaybackStatus = func

        @wraps(func)
        def decorator(*args, **kwargs):
            """ should receive a message-value parameter """
            return func(*args, **kwargs)

        return decorator

    # OnPlaybackResponse 的修饰函数,无修饰则用默认 OnPlaybackResponse，处理回放请求返回结果
    def hs_on_playback_response(self,func):
        self.callback.OnPlaybackResponse = func

        @wraps(func)
        def decorator(*args, **kwargs):
            """ should receive a message-value parameter """
            return func(*args, **kwargs)

        return decorator

    # OnPlaybackControlResponse 的修饰函数,无修饰则用默认 OnPlaybackControlResponse，处理回放控制请求返回结果
    def hs_on_playback_control_response(self,func):
        self.callback.OnPlaybackControlResponse = func

        @wraps(func)
        def decorator(*args, **kwargs):
            """ should receive a message-value parameter """
            return func(*args, **kwargs)

        return decorator

    # OnSubscribeResponse 的修饰函数,无修饰则用默认 OnSubscribeResponse，处理订阅请求返回结果
    def hs_on_subscribe_response(self,func):
        self.callback.OnSubscribeResponse = func

        @wraps(func)
        def decorator(*args, **kwargs):
            """ should receive a message-value parameter """
            return func(*args, **kwargs)

        return decorator

    # OnQueryResponse 的修饰函数,无修饰则用默认 OnQueryResponse，处理查询请求返回结果
    def hs_on_query_response(self,func):
        self.callback.OnQueryResponse = func

        @wraps(func)
        def decorator(*args, **kwargs):
            """ should receive a message-value parameter """
            return func(*args, **kwargs)

        return decorator


    ###订阅，暂时先支持按照id的订阅
    def hs_subscribe_by_id(self,security_id_lists= [],marketdata_type_lists=[],action_type=MDSubscribe.COVERAGE):
        if (0 == len(security_id_lists) or 0 == len(marketdata_type_lists)):
            raise Exception(f'security_id_lists、marketdata_type_lists 不能为空')
        id_elements = []
        for id in security_id_lists:
            id_element = mdc_gateway_interface.SubscribeByIdElement(id,marketdata_type_lists)
            id_elements.append(id_element)
        # 订阅接口
        get_interface().subscribeById(action_type,id_elements);


    #查询历史上所有的指定证券的基础信息(MarketDataTypes = MD_CONSTANT)
    def hs_query_mdcontant(self, security_pair_list = [],security_id_lists= []):

        if (0 == len(security_pair_list) and 0 == len(security_id_lists)):
            raise Exception(f'security_idsource_list and security_id_lists 不能同时为空')
        security_idsource_and_types = []
        for security_idsource in security_pair_list:
            security_id = security_idsource[0]
            security_type = security_idsource[1]
            security_idsource_and_types.append(mdc_gateway_interface.SecurityIDSourceAndType(security_id, security_type))
        # params:security_id_lists 为 标的集合
        get_interface().queryMdContantCallback(security_idsource_and_types,security_id_lists)

    #查询今日最新的指定证券的基础信息(MarketDataTypes = MD_CONSTANT)
    def hs_last_mdcontant(self,security_pair_list = [],security_id_lists= []):
        if (0 == len(security_pair_list) and 0 == len(security_id_lists)):
            raise Exception(f'security_idsource_list and security_id_lists 不能同时为空')
        security_idsource_and_types = []
        for security_idsource in security_pair_list:
            security_id = security_idsource[0]
            security_type = security_idsource[1]
            security_idsource_and_types.append(mdc_gateway_interface.SecurityIDSourceAndType(security_id, security_type))

        # params:security_id_lists 为 标的集合
        get_interface().queryLastMdContantCallback(security_idsource_and_types,security_id_lists)


    #查询指定ETF证券的基础信息(MarketDataTypes = MD_ETFBasicInfo)
    def hs_query_ETFinfo(self,security_pair_list = [],security_id_lists= []):
        if (0 == len(security_pair_list) and 0 == len(security_id_lists)):
            raise Exception(f'security_idsource_list and security_id_lists 不能同时为空')
        security_idsource_and_types = []
        for security_idsource in security_pair_list:
            security_id = security_idsource[0]
            security_type = security_idsource[1]
            security_idsource_and_types.append(mdc_gateway_interface.SecurityIDSourceAndType(security_id, security_type))

        get_interface().queryETFInfoCallback(security_idsource_and_types,security_id_lists)

    #查询指定证券的最新快照信息(MarketDataTypes = MD_TICK)
    def hs_query_last_mdtick(self,security_pair_list = [],security_id_lists= []):
        if (0 == len(security_pair_list) and 0 == len(security_id_lists)):
            raise Exception(f'security_idsource_list and security_id_lists 不能同时为空')
        security_idsource_and_types = []
        for security_idsource in security_pair_list:
            security_id = security_idsource[0]
            security_type = security_idsource[1]
            security_idsource_and_types.append(mdc_gateway_interface.SecurityIDSourceAndType(security_id, security_type))

        get_interface().queryLastMdTickCallback(security_idsource_and_types,security_id_lists)


    # 回放接口 (注意：securitylist 和 securityIdList取并集!!!)
    # 回放限制
    # 对于回放而言，时间限制由股票只数和天数的乘积决定，要求 回放只数 × 回放天数 × 证券权重 ≤ 450，交易时间段内回放功能 乘积<=200。
    # Tick/Transaction/Order回放时间范围限制是30天，每支证券权重为1，即可以回放15只股票30天以内的数据或450支股票1天内数据。
    # 日K数据回放时间范围限制是365天，每支证券权重为0.005。
    # 分钟K线数据回放时间范围限制是90天，每支证券权重0.05。
    # 数据最早可以回放到 2017年1月2日
    #回测数据的起止时间为(starttime,stoptime]
    def hs_play_back(self,security_id_lists= [],marketdata_type=EMarketDataType.UNKNOWN_DATA_TYPE,start_time='20211103090000', end_time='20211103150000',exrights_type = MDPlayback.NO_EXRIGHTS):
        if(0 == len(security_id_lists)):
            raise Exception(f'security_id_lists 不能为空')
        if(marketdata_type == EMarketDataType.UNKNOWN_DATA_TYPE):
            raise Exception(f'marketdata_type 填写不正确')
        get_interface().playCallback(security_id_lists,marketdata_type, exrights_type, start_time,end_time)


    # 盘中回放接口 --securitylist 和 securityIdList取并集
    # Can only query data for one day
    def hs_play_sort_back(self,security_id_lists= [],marketdata_type=EMarketDataType.UNKNOWN_DATA_TYPE,start_time='20211103090000', end_time='20211103150000',exrights_type = MDPlayback.NO_EXRIGHTS,sort=True):
        if(0 == len(security_id_lists)):
            raise Exception(f'security_id_lists 不能为空')
        if(marketdata_type == EMarketDataType.UNKNOWN_DATA_TYPE):
            raise Exception(f'marketdata_type 填写不正确')
        string_list = mdc_gateway_interface.StrList()
        for security_id_list in security_id_lists:
            string_list.Add(security_id_list)
        get_interface().playSortCallback(string_list,start_time,end_time,marketdata_type,exrights_type,sort)


    def hs_sync(self):
        print("input any key to exit >>>")
        line = input()
        if len(str(line)) > 0:
            print("sync: input-->>" + str(line) + ",then exit this sync.")



def demo1(username,passwd):
    app = HsInsight(username, passwd)

    @app.hs_on_market_data
    def hs_on_market_data_back(marketdata:MarketData.MarketData):
        try:
            if marketdata.marketDataType == EMarketDataType.MD_TICK:  # .MD_TICK 快照
                if marketdata.HasField("mdStock"):  # 股票
                    print(
                        " hs_on_market_data_back HTSCSecurityID=%s " % (marketdata.mdStock.HTSCSecurityID))
                elif marketdata.HasField("mdIndex"):  # 指数
                    print(
                        "hs_on_market_data_back HTSCSecurityID=%s lastprice=%d" % (marketdata.mdIndex.HTSCSecurityID, marketdata.mdIndex.LastPx))
                elif marketdata.HasField("mdBond"):  # 债券
                    print(
                        "hs_on_market_data_back HTSCSecurityID=%s lastprice=%d" % (marketdata.mdBond.HTSCSecurityID, marketdata.mdBond.LastPx))
                elif marketdata.HasField("mdFund"):  # 基金
                    print(
                        "hs_on_market_data_back HTSCSecurityID=%s lastprice=%d" % (marketdata.mdFund.HTSCSecurityID, marketdata.mdFund.LastPx))
                elif marketdata.HasField("mdOption"):  # 期权
                    print(
                        "hs_on_market_data_back HTSCSecurityID=%s lastprice=%d" % (marketdata.mdOption.HTSCSecurityID, marketdata.mdOption.LastPx))
                elif marketdata.HasField("mdFuture"):  # 期权
                    print(
                        "hs_on_market_data_back HTSCSecurityID=%s lastprice=%d" % (marketdata.mdFuture.HTSCSecurityID, marketdata.mdFuture.LastPx))
            elif marketdata.marketDataType == EMarketDataType.MD_TRANSACTION:  # .MD_TRANSACTION:逐笔成交
                if marketdata.HasField("mdTransaction"):
                    print("hs_on_market_data_back %s" % (marketdata.mdTransaction))
            elif marketdata.marketDataType == EMarketDataType.MD_ORDER:  # .MD_ORDER:逐笔委托
                if marketdata.HasField("mdOrder"):
                    print("hs_on_market_data_back %s" % (marketdata.mdOrder))
            elif marketdata.marketDataType == EMarketDataType.MD_CONSTANT:  # .MD_CONSTANT:静态信息
                if marketdata.HasField("mdConstant"):
                    print("hs_on_market_data_back %s" % (marketdata.mdConstant.HTSCSecurityID))
                # MD_KLINE:实时数据只提供15S和1MIN K线
            elif marketdata.marketDataType == EMarketDataType.MD_KLINE_15S or marketdata.marketDataType == EMarketDataType.MD_KLINE_1MIN or marketdata.marketDataType == EMarketDataType.MD_KLINE_5MIN or marketdata.marketDataType == EMarketDataType.MD_KLINE_15MIN or marketdata.marketDataType == EMarketDataType.MD_KLINE_30MIN or marketdata.marketDataType == EMarketDataType.MD_KLINE_60MIN or marketdata.marketDataType == EMarketDataType.MD_KLINE_1D:
                if marketdata.HasField("mdKLine"):
                    print("hs_on_market_data_back %s" % (marketdata.mdKLine))
            elif marketdata.marketDataType == EMarketDataType.MD_TWAP_1S or marketdata.marketDataType == EMarketDataType.MD_TWAP_1MIN:  # .TWAP:TWAP数据
                if marketdata.HasField("mdTwap"):
                    print("hs_on_market_data_back %s" %  (marketdata.mdTwap))
            elif marketdata.marketDataType == EMarketDataType.MD_VWAP_1S or marketdata.marketDataType == EMarketDataType.MD_VWAP_1MIN:  # .VWAP:VWAP数据
                if marketdata.HasField("mdVwap"):
                    print("hs_on_market_data_back %s" % (marketdata.mdVwap))
            elif marketdata.marketDataType == EMarketDataType.AD_FUND_FLOW_ANALYSIS:  # .AD_FUND_FLOW_ANALYSIS:
                if marketdata.HasField("mdFundFlowAnalysis"):
                    print("hs_on_market_data_back %s" % (marketdata.mdFundFlowAnalysis))
            elif marketdata.marketDataType == EMarketDataType.MD_ETF_BASICINFO:#.MD_ETF_BASICINFO:ETF成分股信息
                if marketdata.HasField("mdETFBasicInfo"):
                    print("hs_on_market_data_back %s" % (marketdata.mdETFBasicInfo))
            elif marketdata.marketDataType == EMarketDataType.MD_SECURITY_LENDING:#.MD_SECURITY_LENDING
                if marketdata.HasField("mdSecurityLending"):
                    print("hs_on_market_data_back %s" % (marketdata.mdSecurityLending))

        except BaseException as e:
            print("hs_on_market_data_back error happended!")
            print(e)

    app.hs_query_mdcontant([(ESecurityIDSource.XSHG,ESecurityType.StockType),(ESecurityIDSource.XSHE,ESecurityType.IndexType)])

    #app.hs_play_back(["601688.SH"],EMarketDataType.MD_TICK);

    #app.hs_play_sort_back(["601688.SH"],EMarketDataType.MD_TICK);

    #app.hs_subscribe_by_id(["600570.SH"],[EMarketDataType.MD_ORDER]);

    app.hs_sync()

def demo2(username,passwd):
    app = HsInsight(username, passwd)

    @app.hs_on_market_data
    def hs_on_market_data_back(marketdata:MarketData.MarketData):
        try:
            if marketdata.marketDataType == EMarketDataType.MD_TICK:  # .MD_TICK 快照
                if marketdata.HasField("mdStock"):  # 股票
                    print(
                        " hs_on_market_data_back HTSCSecurityID=%s " % (marketdata.mdStock.HTSCSecurityID))
                elif marketdata.HasField("mdIndex"):  # 指数
                    print(
                        "hs_on_market_data_back HTSCSecurityID=%s lastprice=%d" % (marketdata.mdIndex.HTSCSecurityID, marketdata.mdIndex.LastPx))
                elif marketdata.HasField("mdBond"):  # 债券
                    print(
                        "hs_on_market_data_back HTSCSecurityID=%s lastprice=%d" % (marketdata.mdBond.HTSCSecurityID, marketdata.mdBond.LastPx))
                elif marketdata.HasField("mdFund"):  # 基金
                    print(
                        "hs_on_market_data_back HTSCSecurityID=%s lastprice=%d" % (marketdata.mdFund.HTSCSecurityID, marketdata.mdFund.LastPx))
                elif marketdata.HasField("mdOption"):  # 期权
                    print(
                        "hs_on_market_data_back HTSCSecurityID=%s lastprice=%d" % (marketdata.mdOption.HTSCSecurityID, marketdata.mdOption.LastPx))
                elif marketdata.HasField("mdFuture"):  # 期权
                    print(
                        "hs_on_market_data_back HTSCSecurityID=%s lastprice=%d" % (marketdata.mdFuture.HTSCSecurityID, marketdata.mdFuture.LastPx))
            elif marketdata.marketDataType == EMarketDataType.MD_TRANSACTION:  # .MD_TRANSACTION:逐笔成交
                if marketdata.HasField("mdTransaction"):
                    print("hs_on_market_data_back %s" % (marketdata.mdTransaction))
            elif marketdata.marketDataType == EMarketDataType.MD_ORDER:  # .MD_ORDER:逐笔委托
                if marketdata.HasField("mdOrder"):
                    print("hs_on_market_data_back %s" % (marketdata.mdOrder))
            elif marketdata.marketDataType == EMarketDataType.MD_CONSTANT:  # .MD_CONSTANT:静态信息
                if marketdata.HasField("mdConstant"):
                    print("hs_on_market_data_back %s" % (marketdata.mdConstant.HTSCSecurityID))
                # MD_KLINE:实时数据只提供15S和1MIN K线
            elif marketdata.marketDataType == EMarketDataType.MD_KLINE_15S or marketdata.marketDataType == EMarketDataType.MD_KLINE_1MIN or marketdata.marketDataType == EMarketDataType.MD_KLINE_5MIN or marketdata.marketDataType == EMarketDataType.MD_KLINE_15MIN or marketdata.marketDataType == EMarketDataType.MD_KLINE_30MIN or marketdata.marketDataType == EMarketDataType.MD_KLINE_60MIN or marketdata.marketDataType == EMarketDataType.MD_KLINE_1D:
                if marketdata.HasField("mdKLine"):
                    print("hs_on_market_data_back %s" % (marketdata.mdKLine))
            elif marketdata.marketDataType == EMarketDataType.MD_TWAP_1S or marketdata.marketDataType == EMarketDataType.MD_TWAP_1MIN:  # .TWAP:TWAP数据
                if marketdata.HasField("mdTwap"):
                    print("hs_on_market_data_back %s" %  (marketdata.mdTwap))
            elif marketdata.marketDataType == EMarketDataType.MD_VWAP_1S or marketdata.marketDataType == EMarketDataType.MD_VWAP_1MIN:  # .VWAP:VWAP数据
                if marketdata.HasField("mdVwap"):
                    print("hs_on_market_data_back %s" % (marketdata.mdVwap))
            elif marketdata.marketDataType == EMarketDataType.AD_FUND_FLOW_ANALYSIS:  # .AD_FUND_FLOW_ANALYSIS:
                if marketdata.HasField("mdFundFlowAnalysis"):
                    print("hs_on_market_data_back %s" % (marketdata.mdFundFlowAnalysis))
            elif marketdata.marketDataType == EMarketDataType.MD_ETF_BASICINFO:#.MD_ETF_BASICINFO:ETF成分股信息
                if marketdata.HasField("mdETFBasicInfo"):
                    print("hs_on_market_data_back %s" % (marketdata.mdETFBasicInfo))
            elif marketdata.marketDataType == EMarketDataType.MD_SECURITY_LENDING:#.MD_SECURITY_LENDING
                if marketdata.HasField("mdSecurityLending"):
                    print("hs_on_market_data_back %s" % (marketdata.mdSecurityLending))

        except BaseException as e:
            print("hs_on_market_data_back error happended!")
            print(e)

    @app.hs_on_playback_payload
    def hs_on_playback_payload(playload:MDPlayback.PlaybackPayload):
        marketDataStream = playload.marketDataStream;
        print("OnPlaybackPayload total number=%d, serial=%d, isfinish=%d" %(marketDataStream.totalNumber,marketDataStream.serial,
                                                                            marketDataStream.isFinished));
        marketDataList = marketDataStream.marketDataList
        marketDatas = marketDataList.marketDatas
        for data in marketDatas:
            hs_on_market_data_back(data)


    #app.hs_query_mdcontant([(ESecurityIDSource.XSHG,ESecurityType.StockType),(ESecurityIDSource.XSHE,ESecurityType.IndexType)])

    #app.hs_play_back(["601688.SH"],EMarketDataType.MD_TICK);

    app.hs_play_sort_back(["601688.SH"],EMarketDataType.MD_TICK);

    #app.hs_subscribe_by_id(["600570.SH"],[EMarketDataType.MD_ORDER]);

    app.hs_sync()

def demo3(username,passwd):
    app = HsInsight(username,passwd)

    @app.hs_on_market_data
    def hs_on_market_data_back(marketdata:MarketData.MarketData):
        try:
            if marketdata.marketDataType == EMarketDataType.MD_TICK:  # .MD_TICK 快照
                if marketdata.HasField("mdStock"):  # 股票
                    print(
                        " hs_on_market_data_back HTSCSecurityID=%s " % (marketdata.mdStock.HTSCSecurityID))
                elif marketdata.HasField("mdIndex"):  # 指数
                    print(
                        "hs_on_market_data_back HTSCSecurityID=%s lastprice=%d" % (marketdata.mdIndex.HTSCSecurityID, marketdata.mdIndex.LastPx))
                elif marketdata.HasField("mdBond"):  # 债券
                    print(
                        "hs_on_market_data_back HTSCSecurityID=%s lastprice=%d" % (marketdata.mdBond.HTSCSecurityID, marketdata.mdBond.LastPx))
                elif marketdata.HasField("mdFund"):  # 基金
                    print(
                        "hs_on_market_data_back HTSCSecurityID=%s lastprice=%d" % (marketdata.mdFund.HTSCSecurityID, marketdata.mdFund.LastPx))
                elif marketdata.HasField("mdOption"):  # 期权
                    print(
                        "hs_on_market_data_back HTSCSecurityID=%s lastprice=%d" % (marketdata.mdOption.HTSCSecurityID, marketdata.mdOption.LastPx))
                elif marketdata.HasField("mdFuture"):  # 期权
                    print(
                        "hs_on_market_data_back HTSCSecurityID=%s lastprice=%d" % (marketdata.mdFuture.HTSCSecurityID, marketdata.mdFuture.LastPx))
            elif marketdata.marketDataType == EMarketDataType.MD_TRANSACTION:  # .MD_TRANSACTION:逐笔成交
                if marketdata.HasField("mdTransaction"):
                    print("hs_on_market_data_back %s" % (marketdata.mdTransaction))
            elif marketdata.marketDataType == EMarketDataType.MD_ORDER:  # .MD_ORDER:逐笔委托
                if marketdata.HasField("mdOrder"):
                    print("hs_on_market_data_back %s" % (marketdata.mdOrder))
            elif marketdata.marketDataType == EMarketDataType.MD_CONSTANT:  # .MD_CONSTANT:静态信息
                if marketdata.HasField("mdConstant"):
                    print("hs_on_market_data_back %s" % (marketdata.mdConstant.HTSCSecurityID))
                # MD_KLINE:实时数据只提供15S和1MIN K线
            elif marketdata.marketDataType == EMarketDataType.MD_KLINE_15S or marketdata.marketDataType == EMarketDataType.MD_KLINE_1MIN or marketdata.marketDataType == EMarketDataType.MD_KLINE_5MIN or marketdata.marketDataType == EMarketDataType.MD_KLINE_15MIN or marketdata.marketDataType == EMarketDataType.MD_KLINE_30MIN or marketdata.marketDataType == EMarketDataType.MD_KLINE_60MIN or marketdata.marketDataType == EMarketDataType.MD_KLINE_1D:
                if marketdata.HasField("mdKLine"):
                    print("hs_on_market_data_back %s" % (marketdata.mdKLine))
            elif marketdata.marketDataType == EMarketDataType.MD_TWAP_1S or marketdata.marketDataType == EMarketDataType.MD_TWAP_1MIN:  # .TWAP:TWAP数据
                if marketdata.HasField("mdTwap"):
                    print("hs_on_market_data_back %s" %  (marketdata.mdTwap))
            elif marketdata.marketDataType == EMarketDataType.MD_VWAP_1S or marketdata.marketDataType == EMarketDataType.MD_VWAP_1MIN:  # .VWAP:VWAP数据
                if marketdata.HasField("mdVwap"):
                    print("hs_on_market_data_back %s" % (marketdata.mdVwap))
            elif marketdata.marketDataType == EMarketDataType.AD_FUND_FLOW_ANALYSIS:  # .AD_FUND_FLOW_ANALYSIS:
                if marketdata.HasField("mdFundFlowAnalysis"):
                    print("hs_on_market_data_back %s" % (marketdata.mdFundFlowAnalysis))
            elif marketdata.marketDataType == EMarketDataType.MD_ETF_BASICINFO:#.MD_ETF_BASICINFO:ETF成分股信息
                if marketdata.HasField("mdETFBasicInfo"):
                    print("hs_on_market_data_back %s" % (marketdata.mdETFBasicInfo))
            elif marketdata.marketDataType == EMarketDataType.MD_SECURITY_LENDING:#.MD_SECURITY_LENDING
                if marketdata.HasField("mdSecurityLending"):
                    print("hs_on_market_data_back %s" % (marketdata.mdSecurityLending))

        except BaseException as e:
            print("hs_on_market_data_back error happended!")
            print(e)

    @app.hs_on_playback_payload
    def hs_on_playback_payload(playload:MDPlayback.PlaybackPayload):
        marketDataStream = playload.marketDataStream;
        print("hs_on_playback_payload total number=%d, serial=%d, isfinish=%d" %(marketDataStream.totalNumber,marketDataStream.serial,
                                                                            marketDataStream.isFinished));
        marketDataList = marketDataStream.marketDataList
        marketDatas = marketDataList.marketDatas
        for data in marketDatas:
            hs_on_market_data_back(data)

    @app.hs_on_playback_status
    def hs_on_playback_status(status:MDPlayback.PlaybackStatus):
        try:
            print("hs_on_playback_status playback status=%d" %(status.taskStatus))
            get_interface().set_service_value(status.taskStatus)
            if(status.taskStatus == MDPlayback.CANCELED or status.taskStatus == MDPlayback.COMPLETED or status.taskStatus == MDPlayback.FAILED):
                get_interface().mutex.acquire()
                if status.taskId in get_interface().task_id_status:
                    del get_interface().task_id_status[status.taskId]
                get_interface().mutex.release()
        except BaseException as e:
            print("error happended in hs_on_playback_status")
            print(e)

    @app.hs_on_playback_response
    def hs_on_playback_response(response:MDPlayback.PlaybackResponse):
        try:
            if response.isSuccess:
                print("hs_on_playback_response Message id:" + response.taskId)
            else:
                #print(response.errorContext.errorCode)
                print("hs_on_playback_response failed --> %s" %(response.errorContext.message))
        except BaseException as e:
            print("error happended in hs_on_playback_response")
            print(e)

    @app.hs_on_playback_control_response
    def hs_on_playback_control_response(response:MDPlayback.PlaybackControlResponse):
        try:
            if response.isSuccess:
                print(response.currentReplayRate)
                print("hs_on_playback_control_response Message id:" + response.taskId)
            else:
                print("hs_on_playback_control_response failed!!! reason -> %s" %(response.errorContext.message))
        except BaseException as e:
            print("error happended in hs_on_playback_control_response")
            print(e)

    @app.hs_on_subscribe_response
    def hs_on_subscribe_response(response:MDSubscribe.MDSubscribeResponse):
        try:
            if response.isSuccess:
                print("hs_on_subscribe_response Subscribe Success!!!")
            else:
                #print(gateway.getErrorCodeValue(response.errorContext.errorCode))
                print("hs_on_subscribe_response Subscribe failed!!! reason ->%s" %(response.errorContext.message))
        except BaseException as e:
            print(" error happended in hs_on_subscribe_response")
            print(e)

    @app.hs_on_query_response
    def hs_on_query_response(response:MDQuery.MDQueryResponse):
        try:
            if response.isSuccess:
                marketDataStream = response.marketDataStream;
                print(
                    "hs_on_query_response query response total number=%d, serial=%d, isfinish=%d" % (marketDataStream.totalNumber, marketDataStream.serial,
                                                                                marketDataStream.isFinished));
                marketDataList = marketDataStream.marketDataList
                marketDatas = marketDataList.marketDatas
                for data in marketDatas:
                    hs_on_market_data_back(data)
                get_interface().set_query_exit(marketDataStream.isFinished == 1)
            else:
                print("hs_on_query_response failed!!! reason -> %s" %(response.errorContext.message))
                get_interface().set_query_exit(True)
        except BaseException as e:
            print(" error happended in hs_on_query_response")
            print(e)


    app.hs_query_mdcontant([(ESecurityIDSource.XSHG,ESecurityType.StockType),(ESecurityIDSource.XSHE,ESecurityType.IndexType)])

    #app.hs_play_back(["601688.SH"],EMarketDataType.MD_TICK);

    app.hs_play_sort_back(["601688.SH"],EMarketDataType.MD_TICK);

    #app.hs_subscribe_by_id(["600570.SH"],[EMarketDataType.MD_TICK]);

    app.hs_sync()