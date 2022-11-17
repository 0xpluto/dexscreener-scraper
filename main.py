import json
import os
import sys
import argparse
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.firefox.options import Options as FirefoxOptions

options = FirefoxOptions()
options.add_argument("--headless")
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


def main():
    parser = argparse.ArgumentParser(
        prog="DexScreener Scraper", description="Coin scraper for dexscreener.com")
    parser.add_argument("-c", "--chain", type=int, default=1,
                        help="Chain ID (available: %s)" % str(list(chains.keys())))
    parser.add_argument("--dex", type=str,
                        help="Filter coins for chain by dex")
    parser.add_argument("-o", action="store_true",
                        default=False, help="Output to json file")
    args = parser.parse_args()

    if args.chain not in chains:
        print("Invalid chain ID")
        sys.exit(1)

    dexs = (map(lambda x: x.lower(), dexes[args.chain]))
    if args.dex.lower() not in dexs:
        print("Invalid dex name")
        print("Available dexes for chain: %s" % str(dexes[args.chain]))
        sys.exit(1)
        
    url = baseurl + chains[args.chain] + "/" + args.dex
    driver.get(url)


if __name__ == "__main__":
    main()
