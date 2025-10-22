#!/usr/bin/env python3
"""
Live demonstration of TradingView MCP Server capabilities
Running real queries with actual market data
"""

import sys
import json
import time
sys.path.insert(0, "src")

from tradingview_mcp.server import (
    top_gainers,
    top_losers,
    bollinger_scan,
    rating_filter,
    coin_analysis,
    consecutive_candles_scan,
    exchanges_list
)

def print_header(title, emoji="🎯"):
    print(f"\n{'='*80}")
    print(f"{emoji} {title}")
    print(f"{'='*80}\n")

def print_coins(coins, title):
    """Pretty print coin results"""
    if not coins:
        print("❌ No results (may be due to rate limiting - wait 5-10 mins)")
        return

    print(f"✅ Found {len(coins)} results:\n")
    for i, coin in enumerate(coins, 1):
        symbol = coin.get('symbol', 'N/A')
        change = coin.get('changePercent', 0)
        indicators = coin.get('indicators', {})

        print(f"{i}. {symbol}")
        print(f"   Change: {change:+.2f}%")

        if 'RSI' in indicators and indicators['RSI']:
            print(f"   RSI: {indicators['RSI']:.2f}")
        if 'close' in indicators and indicators['close']:
            print(f"   Price: ${indicators['close']:.4f}")
        if 'BB_upper' in indicators and 'BB_lower' in indicators:
            bb_upper = indicators.get('BB_upper')
            bb_lower = indicators.get('BB_lower')
            if bb_upper and bb_lower:
                print(f"   BB Range: ${bb_lower:.4f} - ${bb_upper:.4f}")

        print()

def main():
    print("\n" + "🚀"*40)
    print("   TRADINGVIEW MCP SERVER - LIVE DEMONSTRATION")
    print("🚀"*40)

    # ========================================================================
    # DEMO 1: TOP GAINERS
    # ========================================================================
    print_header("DEMO 1: Top 5 Crypto Gainers on KuCoin (15 min timeframe)", "📈")
    print("Query: top_gainers(exchange='KUCOIN', timeframe='15m', limit=5)")
    print("\nSearching for hottest movers...\n")

    try:
        gainers = top_gainers(exchange="KUCOIN", timeframe="15m", limit=5)
        print_coins(gainers, "Top Gainers")
    except Exception as e:
        print(f"❌ Error: {e}\n")

    time.sleep(2)  # Brief pause between queries

    # ========================================================================
    # DEMO 2: BOLLINGER BAND SQUEEZE
    # ========================================================================
    print_header("DEMO 2: Bollinger Band Squeeze Detection (Breakout Candidates)", "🎯")
    print("Query: bollinger_scan(exchange='KUCOIN', timeframe='4h', bbw_threshold=0.05, limit=5)")
    print("\nFinding coins with tight Bollinger Bands (potential breakouts)...\n")

    try:
        squeeze = bollinger_scan(exchange="KUCOIN", timeframe="4h", bbw_threshold=0.05, limit=5)
        print_coins(squeeze, "Squeeze Candidates")
    except Exception as e:
        print(f"❌ Error: {e}\n")

    time.sleep(2)

    # ========================================================================
    # DEMO 3: BITCOIN ANALYSIS
    # ========================================================================
    print_header("DEMO 3: Complete Technical Analysis of Bitcoin", "₿")
    print("Query: coin_analysis(symbol='BTCUSDT', exchange='KUCOIN', timeframe='1h')")
    print("\nAnalyzing BTCUSDT on 1-hour chart...\n")

    try:
        btc = coin_analysis(symbol="BTCUSDT", exchange="KUCOIN", timeframe="1h")

        if 'error' in btc:
            print(f"❌ {btc['error']}")
        else:
            print("✅ Analysis Complete!\n")
            print(json.dumps(btc, indent=2))
    except Exception as e:
        print(f"❌ Error: {e}\n")

    time.sleep(2)

    # ========================================================================
    # DEMO 4: RATING FILTER
    # ========================================================================
    print_header("DEMO 4: Strong Buy Signals (Rating +2)", "✅")
    print("Query: rating_filter(exchange='KUCOIN', timeframe='1h', rating=2, limit=5)")
    print("\nFinding coins with strong bullish signals...\n")

    try:
        rated = rating_filter(exchange="KUCOIN", timeframe="1h", rating=2, limit=5)
        print_coins(rated, "Strong Buy Signals")
    except Exception as e:
        print(f"❌ Error: {e}\n")

    time.sleep(2)

    # ========================================================================
    # DEMO 5: CONSECUTIVE CANDLES
    # ========================================================================
    print_header("DEMO 5: Momentum Detection - 3+ Consecutive Bullish Candles", "🕯️")
    print("Query: consecutive_candles_scan(exchange='KUCOIN', timeframe='15m', pattern_type='bullish')")
    print("\nScanning for strong upward momentum...\n")

    try:
        patterns = consecutive_candles_scan(
            exchange="KUCOIN",
            timeframe="15m",
            pattern_type="bullish",
            candle_count=3,
            min_growth=1.5,
            limit=5
        )

        if 'error' in patterns:
            print(f"❌ {patterns['error']}")
        else:
            data = patterns.get('data', [])
            if data:
                print(f"✅ Found {len(data)} coins with momentum patterns:\n")
                for i, item in enumerate(data, 1):
                    print(f"{i}. {item.get('symbol')}")
                    print(f"   Consecutive Candles: {item.get('consecutive_count', 'N/A')}")
                    print(f"   Total Change: {item.get('total_change', 0):+.2f}%")
                    print()
            else:
                print("❌ No patterns found")
    except Exception as e:
        print(f"❌ Error: {e}\n")

    # ========================================================================
    # DEMO 6: SUPPORTED EXCHANGES
    # ========================================================================
    print_header("DEMO 6: Available Markets & Exchanges", "🌍")
    print("Query: exchanges_list()")
    print()

    try:
        exchanges = exchanges_list()
        print(exchanges)
    except Exception as e:
        print(f"❌ Error: {e}")

    # ========================================================================
    # SUMMARY
    # ========================================================================
    print("\n" + "="*80)
    print("🎉 LIVE DEMONSTRATION COMPLETE!")
    print("="*80)
    print("""
KEY TAKEAWAYS:
✅ Real-time market data from TradingView
✅ Multi-exchange support (11 markets)
✅ Advanced technical analysis (7 indicators)
✅ Pattern recognition & momentum detection
✅ Bollinger Band squeeze detection
✅ Smart rating system for quick filtering

NOTE: Empty results may indicate:
- Rate limiting (wait 5-10 minutes between sessions)
- No assets matching the specific criteria
- Exchange-specific data availability

TIP: KuCoin and BIST typically have the most reliable data!
    """)

if __name__ == "__main__":
    main()
