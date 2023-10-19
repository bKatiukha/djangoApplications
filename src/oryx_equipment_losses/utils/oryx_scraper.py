import re
from typing import Literal, List, Optional, Dict, Union, Pattern

import requests
from bs4 import BeautifulSoup, Tag, ResultSet, PageElement

URLDict = Dict[str, str]
LossDict = Dict[str, Union[str, List[str]]]
LossList = List[LossDict]


class OryxScraper:
    LOAD_URLS: URLDict = {
        'UA': 'https://www.oryxspioenkop.com/2022/02/attack-on-europe-documenting-ukrainian.html',
        'RU': 'https://www.oryxspioenkop.com/2022/02/attack-on-europe-documenting-equipment.html'
    }

    def __init__(self) -> None:
        pass

    # Public methods
    def scrape_oryx_sides(self, parse_side: Optional[Literal['UA', 'RU']] = None) -> LossList:
        if parse_side:
            url: Optional[str] = self.LOAD_URLS.get(parse_side)
            if not url:
                raise ValueError(f"Invalid side. Use 'UA' or 'RU'.")
            return self._scrape_side(parse_side)
        else:
            all_losses: LossList = []
            for parse_side in self.LOAD_URLS.keys():
                all_losses.extend(self._scrape_side(parse_side))
            return all_losses

    # Private methods
    def _parse_vehicle_category_info(self, vehicle_category_info: str) -> Dict[str, str]:
        vehicle_category: List[str] = vehicle_category_info.strip().split('(', 1)
        return {
            'name': vehicle_category[0].strip(),
        }

    def _get_vehicle_name(self, vehicle_info_element: Tag) -> str:
        def trim_text(text: str, pattern: Pattern[str]) -> str:
            if ':' not in text:
                return re.sub(pattern, '', text)
            else:
                return text.split(':', 1)[0] + ':'

        pattern: Pattern[str] = re.compile(r'\([^)]*\)|\xa0')
        vehicle_match: Optional[re.Match] = re.match(
            r'(\d*)\s*(.*)',
            trim_text(vehicle_info_element.text, pattern).strip()
        )
        assert vehicle_match is not None
        return vehicle_match.group(2).strip()

    def _parse_loss_element_info(self, loss_element: Tag) -> LossDict:
        return {
            'href': loss_element['href'].strip(),
            'name': loss_element.text.strip(),
        }

    def _scrape_side(self, parse_side: str) -> LossList:
        response: requests.Response = requests.get(self.LOAD_URLS[parse_side])
        if response.status_code != 200:
            raise ValueError(f"Failed to fetch data from URL: {self.LOAD_URLS[parse_side]}")

        soup: BeautifulSoup = BeautifulSoup(response.text.replace('&nbsp;', ' ').replace('/>', '>'), 'html.parser')
        vehicle_categories_elements: ResultSet[PageElement] = soup.article.select('h3:has(+ ul)')

        losses: LossList = []
        for vehicle_category_element in vehicle_categories_elements:
            vehicle_elements: ResultSet[Tag] = vehicle_category_element.find_next_sibling('ul').find_all('li')
            for vehicle_element in vehicle_elements:
                losses_elements: ResultSet[Tag] = vehicle_element.find_all('a')
                for loss_element in losses_elements:
                    loss_element_info: LossDict = self._parse_loss_element_info(loss_element)
                    vehicle_category_info: Dict[str, str] = self._parse_vehicle_category_info(vehicle_category_element.text)
                    vehicle_name: str = self._get_vehicle_name(vehicle_element)

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
