import asyncio
from playwright.async_api import Playwright, async_playwright
from collections import defaultdict
import json


"""
Returns a list of all of the <tr> elements from the funds table of the website at: 
'https://www.jhinvestments.com/investments'.

:param page: The current webpage playwright is scraping.
:type: playwright.async_api._generated.Page.

:raises Exception: If the selector cannot find <tr> elements on the current path.

:return: List of <tr> elements.
:rtype: List[playwright.async_api._generated.ElementHandle]
"""
async def get_tr_elements(page):
    path = "table.listingTable__table tbody tr"
    tr_elements = await page.query_selector_all(path)

    if not tr_elements:
        raise Exception(f'No <tr> elements found on this path: {path}')
    
    return tr_elements


"""
Return a dictionary such that each key is a JHIM fund type (Alternative, Assest Allocation, etc.),
and each JHIM fund type is a dictionary that maps a specific fund with information from its overview page.

:param tr_elements: List of <tr> elements.
:type: List[playwright.async_api._generated.ElementHandle].
:param playwright: A Playwright instance to allow for navigation to each specific fund.
:type: Playwright

:return: Dictionary of JHIM funds
:rtype: defaultdict.
"""
async def get_funds_dictionary(tr_elements, playwright):
    funds = defaultdict(dict)
    current_fund = ''

    for tr in tr_elements:
        class_attr = await tr.get_attribute('class')

        if class_attr == 'listingTable__legend--tr':
            fund_type = await tr.query_selector('div.listingTable__legend')
            current_fund = await fund_type.inner_text()
        elif class_attr == 'listingTable__tr':
            fund_element = await tr.query_selector("a.listingTable__tdLink")
            fund_name = await fund_element.inner_text()

            href = await fund_element.get_attribute('href')
            fund_values, fund_captions = await get_fund_details(playwright, href)
            
            fund_name_obj = funds[current_fund]            
            fund_name_obj[fund_name] = {
                'fund_values' : fund_values,
                'fund_captions' : fund_captions
            }
            
    return funds


"""
Return a list of text that contains information about a fund from its overview page.

:param detail_values: Playwright locator that contains the desire text.
:type: playwright.async_api._generated.Locator.

:return: List of strings with the information about the fund.
"rtype: List[String]
"""
async def get_details(detail_values):
    values = []

    values_len = await detail_values.count()

    for i in range(values_len):
        text = await detail_values.nth(i).text_content()
        values.append(text)

    return values


"""
Navigates to a fund's overview page to collect data about it.

:param playwright: A Playwright instance to allow for navigation to each specific fund.
:type: Playwright
:param url: String of the fund overview page's url.
:type: String

:return: Tuple with the values and captions of the fund.
:rtype: Tuple(List[String], List[String]).
"""
async def get_fund_details(playwright, url):
    fund_browser = await playwright.chromium.launch()
    fund_page = await fund_browser.new_page()

    await fund_page.goto(url)
    await fund_page.wait_for_selector(".strategySection__value")

    strategy_values = fund_page.locator(".strategySection__value")
    strategy_captions = fund_page.locator(".strategySection__caption")

    values = await get_details(strategy_values)
    captions = await get_details(strategy_captions)

    await fund_browser.close()

    return (values, captions)


"""
Responsible for runnning the main playwright instance and acquiring the funds dictionary.

:param playwright: A Playwright instance to allow for navigation to each specific fund.
:type: Playwright
:param url: String of the fund overview page's url.
:type: String

:raise Exception: If the program cannot locate an element based on given paths.

:return: Dictionary of JHIM funds
:rtype: defaultdict.
"""
async def run(playwright: Playwright, *, url: str) -> str:
    # Basic navigation to the url
    browser = await playwright.chromium.launch()
    page = await browser.new_page()

    try:
        await page.goto(url)
        await page.wait_for_selector("table.listingTable__table tbody tr")

        tr_elements = await get_tr_elements(page)
        funds = await get_funds_dictionary(tr_elements, playwright)
        
        return funds
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await browser.close()


async def main() -> None:
    url = 'https://www.jhinvestments.com/investments'

    async with async_playwright() as playwright:
       funds = await run(playwright, url=url)

    # Uncomment the code below to update the funds_data.json file.

    # funds = dict(funds)

    # json_file_path = 'funds_data.json'

    # with open(json_file_path, 'w+') as f:
    #     json.dump(funds, f, indent=4)


if __name__ == '__main__':
    asyncio.run(main())