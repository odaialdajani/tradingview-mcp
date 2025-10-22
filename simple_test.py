#!/usr/bin/env python3
"""
Minimal test to get actual results from TradingView
"""

import sys
sys.path.insert(0, "src")

from tradingview_mcp.server import exchanges_list, top_gainers, coin_analysis

print("=" * 80)
print("TEST 1: List Exchanges (Resource)")
print("=" * 80)
try:
    result = exchanges_list()
    print("✅ SUCCESS!")
    print(result)
    print()
except Exception as e:
    print(f"❌ Error: {e}\n")

print("=" * 80)
print("TEST 2: Try BIST Exchange (Usually more reliable)")
print("=" * 80)
print("Query: top_gainers(exchange='BIST', timeframe='1D', limit=3)")
try:
    result = top_gainers(exchange="BIST", timeframe="1D", limit=3)
    if result:
        print(f"✅ SUCCESS! Found {len(result)} results:")
        import json
        print(json.dumps(result, indent=2, default=str))
    else:
        print("⚠️ Empty result (no matches or rate limited)")
except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "=" * 80)
print("TEST 3: Try NASDAQ Exchange")
print("=" * 80)
print("Query: top_gainers(exchange='NASDAQ', timeframe='1D', limit=3)")
try:
    result = top_gainers(exchange="NASDAQ", timeframe="1D", limit=3)
    if result:
        print(f"✅ SUCCESS! Found {len(result)} results:")
        import json
        print(json.dumps(result, indent=2, default=str))
    else:
        print("⚠️ Empty result (no matches or rate limited)")
except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "=" * 80)
print("TEST 4: Direct coin analysis - Apple Stock")
print("=" * 80)
print("Query: coin_analysis(symbol='AAPL', exchange='NASDAQ', timeframe='1D')")
try:
    result = coin_analysis(symbol="AAPL", exchange="NASDAQ", timeframe="1D")
    if result:
        print("✅ GOT RESULT:")
        import json
        print(json.dumps(result, indent=2, default=str))
    else:
        print("⚠️ Empty result")
except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "=" * 80)
print("TESTS COMPLETE")
print("=" * 80)
