import json
import os
import sys
import argparse
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions

options = FirefoxOptions()
# options.add_argument("--headless")
driver = webdriver.Firefox(options=options)


baseurl = "https://dexscreener.com/"
chains = {
    1: "ethereum",
    56: "bsc",
    137: "polygon",
    250: "fantom",
    43114: "avalanche",
    42161: "arbitrum",
    10: "optimism",
}

dexes = {
    1: [
        "Uniswap",
        "SushiSwap",
        "Balancer",
        "PancakeSwap",
        "ShibaSwap",
        "DefiSwap",
        "Fraxswap",
        "STEPN",
        "SafeMoonSwap",
        "Swapr",
        "TempleDAO",
        "RadioShack"
    ],
    10: [
        "Uniswap",
        "Velodrome",
        "BeethovenX",
        "ZipSwap",
        "KyberSwap",
    ],
    56: [
        "PancakeSwap",
        "ApeSwap",
        "Biswap",
        "MDEX",
        "BabySwap",
        "Fstswap",
        "SafeMoon Swap",
        "Nomiswap",
        "BabyDogeSwap",
        "KnightSwap",
        "Pandora",
        "ConeExchange",
        "BakerySwap",
        "W3Swap",
        "PlanetFinance",
        "Leonicorn",
        "KyberSwap",
        "Swych",
        "BaryonSwap",
        "JSwap",
        "OrbitalSwap",
        "MarsEcosystem",
        "RadioShack",
        "SushiSwap",
        "OpenOcean",
        "DinosaurEggs",
        "Sphynx",
        "AnnexFinance",
        "WaultFinance",
        "MoonLift",
        "Niob",
        "JetSwap",
        "Aequinox",
        "PadSwap",
        "HyperJump",
        "CobraSwap",
        "PYESwap",
        "BridgesExchange",
        "Mochiswap",
    ],
    137: [
        "Uniswap",
        "MMFinance",
        "QuickSwap",
        "KyberSwap",
        "Balancer",
        "ApeSwap",
        "DFYN",
        "RadioShack",
        "Dystopia",
        "VulcanDex",
        "JetSwap",
        "ElkFinance",
        "GravityFinance",
        "Polycat",
        "ComethSwap",
        "Algebra",
        "Firebird",
        "WaultFinance",
        "JamonSwap",
        "TetuSwap",
        "DinoSwap",
        "NachoFinance",
        "PolyZap",
    ],
    250: [
        "SpookySwap",
        "Solidly",
        "SpiritSwap",
        "SushiSwap",
        "BeethovenX",
        "TombSwap",
        "ProtoFi",
        "KnightSwap",
        "WigoSwap",
        "Redemption",
        "Excalibur",
        "MorpheusSwap",
        "PaintSwap",
        "YoshiExchange",
        "SoulSwap",
        "ElkFinance",
        "BombSwap",
        "JetSwap",
        "WingSwap",
        "HyperJump",
        "DegenHaus",
        "Farmtom",
        "DeFySwap",
    ],
    42161: [
        "Uniswap",
        "SushiSwap",
        "Balancer",
        "KyberSwap",
        "3xcalibur",
        "Swapr",
    ],
    43114: [
        "TraderJoe",
        "Pangolin",
        "KyberSwap",
        "SushiSwap",
        "RadioShack",
        "Swapsicle",
        "Elk Finance",
        "onAVAX",
        "HurricanSwap",
        "LydiaFinance",
        "HakuSwap",
        "ApexSwap",
        "YetiSwap",
        "Thorus",
        "Alligator",
        "PartySwap",
    ],
}

org_types = [
    "txs",
    "volume",
    "5min",
    "1hr",
    "6hr",
    "24hr",
    "liquidity",
    "fdv"
]

dexcoins = []
dexpairs = []

def main():
    parser = argparse.ArgumentParser(
        prog="DexScreener Scraper", description="Coin scraper for dexscreener.com")
    parser.add_argument("-c", "--chain",
                        type=int, default=1, help="Chain ID (available: %s)" % str(list(chains.keys())))
    parser.add_argument("--dex",
                        type=str, help="Filter coins for chain by dex")
    parser.add_argument("-o",
                        action="store_true", default=False, help="Output to json file")
    parser.add_argument("--org",
                        type=str, help="Organize by %s (Default: txs)" % str(org_types))
    parser.add_argument("--max",
                        type=int, default=100, help="Max amount of pairs to output (Limit is 100)")
    args = parser.parse_args()

    if args.chain not in chains:
        print("Invalid chain ID")
        sys.exit(1)

    dexs = map(lambda x: x.lower(), dexes[args.chain])
    if args.dex.lower() not in dexs:
        print("Invalid dex name")
        print("Available dexes for chain: %s" % str(dexes[args.chain]))
        sys.exit(1)

    if args.org not in org_types:
        print("Invalid organization type")
        print("Available org types: %s" % str(org_types))
        sys.exit(1)

    url = baseurl + chains[args.chain] + "/" + args.dex.lower()
    driver.get(url)
    
    # These are all of the coin pairs on the page
    coins = driver.find_elements(By.CLASS_NAME,"custom-1oo4dn7")

    org_nav_bar = driver.find_element(By.CLASS_NAME,"custom-1m4s57r")
    buttons = org_nav_bar.find_elements(By.CLASS_NAME, "custom-10m692w")
    # We don't need to click anything for txs bc that's the default
    if args.org == "volume":
        buttons[1].find_element(By.CLASS_NAME, "custom-1d8har").click()
    elif args.org == "5min":
        buttons[2].find_element(By.CLASS_NAME, "custom-1d8har").click()
    elif args.org == "1hr":
        buttons[3].find_element(By.CLASS_NAME, "custom-1d8har").click()
    elif args.org == "6hr":
        buttons[4].find_element(By.CLASS_NAME, "custom-1d8har").click()
    elif args.org == "24hr":
        buttons[5].find_element(By.CLASS_NAME, "custom-1d8har").click()
    elif args.org == "liquidity":
        buttons[6].find_element(By.CLASS_NAME, "custom-1d8har").click()
    elif args.org == "fdv":
        buttons[7].find_element(By.CLASS_NAME, "custom-1d8har").click()

    if args.max > 100:
        args.max = 100

    hrefs = []
    for coin in coins:
        hrefs.append(coin.get_attribute("href"))
    for href in hrefs:
        print("Scraping %s" % href)
        driver.get(href)

        price_div = driver.find_element(By.CLASS_NAME,"custom-1obyyr8")
        price_usd_div = price_div.find_element(By.CLASS_NAME,"custom-1s98r5u")
        price_usd = price_usd_div.find_element(By.CLASS_NAME,"custom-1baulvz").text

        price_denom_div = price_div.find_element(By.CLASS_NAME,"custom-6mn1g4")
        price_denom = price_denom_div.find_element(By.CLASS_NAME,"custom-zvlevn").text

        liquidity_div = driver.find_element(By.CLASS_NAME,"custom-6r1s40")
        liquidity_usd = liquidity_div.find_element(By.CLASS_NAME,"custom-j7qwjs").find_element(By.CLASS_NAME,"custom-5sxn50").text
        fdv = liquidity_div.find_element(By.CLASS_NAME,"custom-gdx2i7").find_element(By.CLASS_NAME,"custom-5sxn50").text
        mkt_cap = liquidity_div.find_element(By.CLASS_NAME,"custom-wox1fj").find_element(By.CLASS_NAME,"custom-5sxn50").text

        tx_action_div = driver.find_element(By.CLASS_NAME,"custom-1tsszuf").find_elements(By.CLASS_NAME,"custom-5sxn50")
        txs = tx_action_div[0].text
        buys = tx_action_div[1].text
        sells = tx_action_div[2].text
        volume = tx_action_div[3].text
        contracts_div = driver.find_element(By.CLASS_NAME,"custom-1gx88nn")
        contracts = contracts_div.find_elements(By.CLASS_NAME,"custom-1v4xcoh")
        names = contracts_div.find_elements(By.CLASS_NAME,"custom-1vlf9fm")
        token1_name = names[1].text.replace(":","").replace("$","")
        token2_name = names[2].text.replace(":","").replace("$","")

        pair_contract = contracts[0].get_attribute("title")
        token1_contract = contracts[1].get_attribute("title")
        token2_contract = contracts[2].get_attribute("title")

        reserves_div = driver.find_element(By.CLASS_NAME,"custom-1iqogjt")
        reserves = reserves_div.find_elements(By.CLASS_NAME,"custom-m75dnw")
        token1_reserve = reserves[0].text
        token2_reserve = reserves[1].text

        dexcoin1 = {
            "name": token1_name,
            "chainId": args.chain,
            "chain": chains[args.chain],
            "contract": token1_contract,
        }
        dexcoin2 = {
            "name": token2_name,
            "chainId": args.chain,
            "chain": chains[args.chain],
            "contract": token2_contract,
        }
        dexpair = {
            "pair": token1_name + "/" + token2_name,
            "chainId": args.chain,
            "chain": chains[args.chain],
            "pairContract": pair_contract,
            "token1": token1_name,
            "token1Contract": token1_contract,
            "token1Reserve": token1_reserve,
            "token2": token2_name,
            "token2Contract": token2_contract,
            "token2Reserve": token2_reserve,
            "price_usd": price_usd,
            "price_denom": price_denom,
            "liquidity_usd": liquidity_usd,
            "fdv": fdv,
            "mkt_cap": mkt_cap,
            "txs": txs,
            "buys": buys,
            "sells": sells,
            "volume": volume,
        }

        if dexcoin1 not in dexcoins:
            print("Adding coin: %s" % token1_name)
            dexcoins.append(dexcoin1)
        if dexcoin2 not in dexcoins:
            print("Adding coin: %s" % token2_name)
            dexcoins.append(dexcoin2)
        if dexpair not in dexpairs:
            print("Adding pair: %s" % dexpair["pair"])
            dexpairs.append(dexpair)

    if args.o:
        with open("dexcoins.json", "w") as f:
            json.dump(dexcoins, f, indent=4)
        with open("dexpairs.json", "w") as f:
            json.dump(dexpairs, f, indent=4)


if __name__ == "__main__":
    main()
