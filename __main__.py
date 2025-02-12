import src
import src_calbaptist
import asyncio
import pandas as pd


async def main():
    meadows = await src.run_meadows()
    cbu = await src_calbaptist.run_cbu()
    all_data = pd.concat([meadows, pd.DataFrame(cbu)], ignore_index=True)
    df = pd.DataFrame(all_data)
    df.to_excel("Output.xlsx", index=False, engine="openpyxl", header=True)
    print('Done Web Scrapping!')

if __name__ == '__main__':
    asyncio.run(main())

