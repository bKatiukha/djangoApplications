import re
from typing import Literal, List, Optional

import requests
from bs4 import BeautifulSoup


class OryxScraper:
    def __init__(self):
        self.LOAD_URLS = {
            'UA': 'https://www.oryxspioenkop.com/2022/02/attack-on-europe-documenting-ukrainian.html',
            'RU': 'https://www.oryxspioenkop.com/2022/02/attack-on-europe-documenting-equipment.html'
        }

    # Public methods
    def scrape_oryx_sides(self, parse_side: Optional[Literal['UA', 'RU']] = None) -> List[dict]:
        if parse_side:
            url = self.LOAD_URLS.get(parse_side)
            if not url:
                raise ValueError(f"Invalid side. Use 'UA' or 'RU'.")
            return self._scrape_side(parse_side)
        else:
            all_losses = []
            for parse_side in self.LOAD_URLS.keys():
                all_losses.extend(self._scrape_side(parse_side))
            return all_losses

    # Private methods
    def _parse_vehicle_category_info(self, vehicle_category_info: str) -> dict:
        vehicle_category = vehicle_category_info.strip().split('(', 1)
        return {
            'name': vehicle_category[0].strip(),
        }

    def _get_vehicle_name(self, vehicle_info_element: object) -> str:
        def trim_vehicle_info_element_text(string):
            pattern = r'\([^)]*\)|\xa0'
            if ':' not in string:
                return re.sub(pattern, '', string)
            else:
                return string.split(':', 1)[0] + ':'

        vehicle_match = re.match(r'(\d*)\s*(.*)', trim_vehicle_info_element_text(vehicle_info_element.text).strip())
        return vehicle_match.group(2).strip()

    def _parse_loss_element_info(self, loss_element) -> dict:
        return {
            'href': loss_element['href'].strip(),
            'name': loss_element.text.strip(),
        }

    def _scrape_side(self, parse_side: str) -> List[dict]:
        response = requests.get(self.LOAD_URLS[parse_side])
        if response.status_code != 200:
            raise ValueError(f"Failed to fetch data from URL: {self.LOAD_URLS[parse_side]}")

        soup = BeautifulSoup(response.text.replace('&nbsp;', ' ').replace('/>', '>'), 'html.parser')
        vehicle_categories_elements = soup.article.select('h3:has(+ ul)')

        losses = []
        for vehicle_category_element in vehicle_categories_elements:
            vehicle_elements = vehicle_category_element.find_next_sibling('ul').find_all('li')
            for vehicle_element in vehicle_elements:
                losses_elements = vehicle_element.find_all('a')
                for loss_element in losses_elements:
                    loss_element_info = self._parse_loss_element_info(loss_element)
                    vehicle_category_info = self._parse_vehicle_category_info(vehicle_category_element.text)
                    vehicle_name = self._get_vehicle_name(vehicle_element)

                    if not any(
                        loss['name'] == loss_element_info['name'] and
                        loss['side'] == parse_side and
                        loss['vehicle_name'] == vehicle_name
                        for loss in losses
                    ):
                        losses.append({
                            'href': loss_element_info['href'],
                            'name': loss_element_info['name'],
                            'side': parse_side,
                            'vehicle_name': vehicle_name,
                            'vehicle_country_made_icon': vehicle_element.find('img')['src'].strip(),
                            'vehicle_category_name': vehicle_category_info['name'],
                        })
        return losses
