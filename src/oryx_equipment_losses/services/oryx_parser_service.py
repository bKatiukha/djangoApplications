import re
from typing import Literal

import requests
from bs4 import BeautifulSoup

# oryx page urls for Documenting Russian and Ukraine Equipment Losses
LOAD_URLS = {
    'UA': 'https://www.oryxspioenkop.com/2022/02/attack-on-europe-documenting-ukrainian.html',
    'RU': 'https://www.oryxspioenkop.com/2022/02/attack-on-europe-documenting-equipment.html'
}


def parse_vehicle_category_info(vehicle_category_info):
    vehicle_category = vehicle_category_info.strip().split('(', 1)
    return {
        'name': vehicle_category[0].strip(),
    }


def get_vehicle_name(vehicle_info_element):
    def trim_vehicle_info_element_text(string):
        pattern = r'\([^)]*\)|\xa0'
        if ':' not in string:
            return re.sub(pattern, '', string)
        else:
            return string.split(':', 1)[0] + ':'

    vehicle_match = re.match(r'(\d*)\s*(.*)', trim_vehicle_info_element_text(vehicle_info_element.text).strip())
    return vehicle_match.group(2).strip()


def parse_loss_element_info(loss_element):
    return {
        'href': loss_element['href'].strip(),
        'name': loss_element.text.strip(),
    }


def parse_remote_oryx_page(parse_side: Literal['UA', 'RU']):
    response = requests.get(LOAD_URLS[parse_side])

    if response.status_code == 200:
        # replace '/>' to '>' because BeautifulSoup auto formatted html
        # BeautifulSoup add close tags for image </img> if not to replace '/>' to '>'
        soup = BeautifulSoup(response.text.replace('&nbsp;', ' ').replace('/>', '>'), 'html.parser')
        vehicle_categories_elements = soup.article.select('h3:has(+ ul)')
        losses = []
        parsed_total_count = 0
        for vehicle_category_element in vehicle_categories_elements:
            vehicle_elements = vehicle_category_element.find_next_sibling('ul').find_all('li')
            for vehicle_element in vehicle_elements if vehicle_elements else []:
                if vehicle_element:
                    losses_elements = vehicle_element.find_all('a')
                    for loss_element in losses_elements if losses_elements else []:
                        if loss_element:
                            loss_element_info = parse_loss_element_info(loss_element)
                            vehicle_category_info = parse_vehicle_category_info(vehicle_category_element.text)
                            href = loss_element_info['href']
                            name = loss_element_info['name']
                            vehicle_name = get_vehicle_name(vehicle_element)

                            # check if in array exist item with same name and parse_side and vehicle_name
                            if_already_exist_element = any(
                                name == loss['name'] and
                                parse_side == loss['side'] and
                                vehicle_name == loss['vehicle_name']
                                for loss in losses
                            )
                            # if_already_exist_element = False
                            if not if_already_exist_element:
                                parsed_total_count += 1
                                losses.append({
                                    'href': href,
                                    'name': name,
                                    'side': parse_side,
                                    'vehicle_name': vehicle_name,
                                    'vehicle_country_made_icon': vehicle_element.find('img')['src'].strip(),
                                    'vehicle_category_name': vehicle_category_info['name'],
                                })
        print('parsed total losses', parse_side, parsed_total_count)
        return losses
