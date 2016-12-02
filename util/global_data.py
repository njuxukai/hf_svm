from enum import Enum

CACHE_DIR = 'cache/'
RESULT_DIR ='result/'
SZ_MARKET_CODE = 'SZ'
SH_MARKET_CODE = 'SH'
MARKET_DATA_LABEL = "MarketData"
ORDER_QUEUE_LABEL = "OrderQueue"
TRANSACTION_LABEL = "Transaction"
ORDER_LABEL = "ORDER"
INDEX_DATA_LABEL = "INDEX_DATA"

TRANSACTION_BID_DIRECTION = 'B'
TRANSACTION_ASK_DIRECTION = 'S'
 
class Metrics(Enum):
    MidPriceMovement = 1,
    BidAskSpreadCrossingDirection = 2,
    PriceTrend = 3


basic_features = ['v1_ap1', 'v1_ap2', 'v1_ap3', 'v1_ap4', 'v1_ap5', \
    'v1_ap6', 'v1_ap7', 'v1_ap8', 'v1_ap9', 'v1_ap10', \
    'v1_av1', 'v1_av2', 'v1_av3', 'v1_av4', 'v1_av5', \
    'v1_av6', 'v1_av7', 'v1_av8', 'v1_av9', 'v1_av10', \
    'v1_bp1', 'v1_bp2', 'v1_bp3', 'v1_bp4', 'v1_bp5', \
    'v1_bp6', 'v1_bp7', 'v1_bp8', 'v1_bp9', 'v1_bp10', \
    'v1_bv1', 'v1_bv2', 'v1_bv3', 'v1_bv4', 'v1_bv5', \
    'v1_bv6', 'v1_bv7', 'v1_bv8', 'v1_bv9', 'v1_bv10']
time_insensitive_features = ['v2_(a-b)1', 'v2_(a-b)2', 'v2_(a-b)3', 'v2_(a-b)4', 'v2_(a-b)5', \
   'v2_(a-b)6', 'v2_(a-b)7', 'v2_(a-b)8', 'v2_(a-b)9', 'v2_(a-b)10', \
   'v2_(a+b)1', 'v2_(a+b)2', 'v2_(a+b)3', 'v2_(a+b)4', 'v2_(a+b)5', \
   'v2_(a+b)6', 'v2_(a+b)7', 'v2_(a+b)8', 'v2_(a+b)9', 'v2_(a+b)10', \
   'v3_a2-1',  'v3_a3-1', 'v3_a4-1', 'v3_a5-1', \
   'v3_a6-1', 'v3_a7-1', 'v3_a8-1', 'v3_a9-1', 'v3_a10-1', \
   'v3_b1-2', 'v3_b1-3', 'v3_b1-4', 'v3_b1-5', \
   'v3_b1-6', 'v3_b1-7', 'v3_b1-8', 'v3_b1-9', 'v3_b1-10', \
   'v3_a2-1', 'v3_a3-2', 'v3_a4-3', 'v3_a5-4', \
   'v3_a6-5', 'v3_a7-6', 'v3_a8-7', 'v3_a9-8', 'v3_a10-9', \
   'v3_b2-1', 'v3_b3-2', 'v3_b4-3', 'v3_b5-4', \
   'v3_b6-5', 'v3_b7-6', 'v3_b8-7', 'v3_b9-8', 'v3_b10-9', \
   'v4_avg_ap', 'v4_avg_av', 'v4_avg_bp', 'v4_avg_bv', \
   'v5_sum(ap-bp)', 'v5_sum(av-bv)']
time_sensitive_features = ['v6_dap1', 'v6_dap2', 'v6_dap3', 'v6_dap4', 'v6_dap5', \
    'v6_dap6', 'v6_dap7', 'v6_dap8', 'v6_dap9', 'v6_dap10', \
    'v6_dav1', 'v6_dav2', 'v6_dav3', 'v6_dav4', 'v6_dav5', \
    'v6_dav6', 'v6_dav7', 'v6_dav8', 'v6_dav9', 'v6_dav10', \
    'v6_dbp1', 'v6_dbp2', 'v6_dbp3', 'v6_dbp4', 'v6_dbp5', \
    'v6_dbp6', 'v6_dbp7', 'v6_dbp8', 'v6_dbp9', 'v6_dbp10', \
    'v6_dbv1', 'v6_dbv2', 'v6_dbv3', 'v6_dbv4', 'v6_dbv5', \
    'v6_dbv6', 'v6_dbv7', 'v6_dbv8', 'v6_dbv9', 'v6_dbv10', \
    'v7_avg_ask_rate', 'v7_avg_bid_rate', \
    'v8_ask_lambda', 'v8_bid_lambda']