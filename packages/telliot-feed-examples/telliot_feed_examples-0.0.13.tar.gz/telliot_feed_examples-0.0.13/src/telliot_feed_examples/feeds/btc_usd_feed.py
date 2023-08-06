"""Example datafeed used by BTCUSDReporter."""
from telliot_core.datafeed import DataFeed
from telliot_core.queries.legacy_query import LegacyRequest

from telliot_feed_examples.sources.bittrex import BittrexPriceSource
from telliot_feed_examples.sources.coinbase import CoinbasePriceSource
from telliot_feed_examples.sources.coingecko import CoinGeckoPriceSource
from telliot_feed_examples.sources.gemini import GeminiPriceSource
from telliot_feed_examples.sources.price_aggregator import PriceAggregator

btc_usd_median_feed = DataFeed(
    query=LegacyRequest(legacy_id=2),
    source=PriceAggregator(
        asset="btc",
        currency="usd",
        algorithm="median",
        sources=[
            CoinbasePriceSource(asset="btc", currency="usd"),
            CoinGeckoPriceSource(asset="btc", currency="usd"),
            BittrexPriceSource(asset="btc", currency="usd"),
            GeminiPriceSource(asset="btc", currency="usd"),
        ],
    ),
)
