from bs4 import BeautifulSoup
import requests
import json

from constants import SCREENER_KEYS


def prepare_url(p_ticker):
    return 'https://www.screener.in/company/' + p_ticker + '/'
    # return 'https://www.screener.in/company/' + 'TATAELXSI' + '/consolidated/'


def get_html_from_screener(p_url):
    response = requests.get(p_url).text
    # print(response)
    return response


def parse_data_from_screener(p_ticker, p_response):
    dictionary = {}
    soup = BeautifulSoup(p_response, 'lxml')
    singular_data = soup.find(class_="company-ratios").find_all('li')
    dictionary['CHECK'] = singular_data[0].find(class_="nowrap value").find(class_="number").text.strip()
    if dictionary['CHECK'] == '':
        response = requests.get('https://www.screener.in/company/' + p_ticker).text
        soup = BeautifulSoup(response, 'lxml')
        dictionary = {}
        # print('match')
    singular_data = soup.find(class_="company-ratios").find_all('li')
    single_value_data_keys = [
        SCREENER_KEYS.MARKET_CAP,
        SCREENER_KEYS.PRICE,
        SCREENER_KEYS.HIGH,
        SCREENER_KEYS.PE,
        SCREENER_KEYS.BOOK_VALUE,
        SCREENER_KEYS.DIV_YIELD,
        SCREENER_KEYS.ROCE,
        SCREENER_KEYS.ROE,
        SCREENER_KEYS.FACE_VALUE,
    ]

    # print(singular_data)
    for index, i in enumerate(singular_data):
        # print(i.find(class_="name").text.strip(), end=" = ")
        # print(i.find(class_="nowrap value").find(class_="number").text.strip())
        dictionary[single_value_data_keys[index]] = i.find(class_="nowrap value").find(class_="number").text.strip()
        if index == 2:
            # print(i.find(class_="nowrap value").find_all(class_="number")[1].text.strip())
            dictionary[SCREENER_KEYS.LOW] = i.find(class_="nowrap value").find_all(class_="number")[1].text.strip()

    list_tables = []
    var_tables = soup.find_all(True, {'class': ['responsive-holder', 'fill-card-width']})
    for index, var_table in enumerate(var_tables):
        if var_table['class'][0] == 'responsive-holder' and var_table['class'][1] != 'hidden':
            list_tables.append(var_table)

    # modifier = 0
    print('list_tables', len(list_tables))
    list_tables = list_tables[:-1]
    # for outer_index, var_table in range(0, 6):
    for outer_index, var_table in enumerate(list_tables):
        heading = var_table.find('thead').find('tr').find_all('th')[1:]
        body = var_table.find('tbody').find_all('tr')
        dictionary[SCREENER_KEYS.ARRAY_HEADINGS[outer_index]] = [val.text.strip() for val in heading]

        for index, row in enumerate(body):
            each_body_row = row.find_all('td')[1:]
            if index < len(SCREENER_KEYS.ARRAY_ALL[outer_index]):
                dictionary[SCREENER_KEYS.ARRAY_ALL[outer_index][index]] = [val.text.strip() if val.text else '' for val in
                                                                           each_body_row]
            else:
                dictionary[SCREENER_KEYS.SP_GOVT] = dictionary[SCREENER_KEYS.SP_PUBLIC]
                dictionary[SCREENER_KEYS.SP_PUBLIC] = [val.text.strip() if val.text else '' for val in each_body_row]

    return dictionary


def get_data_from_screener_using_bs4(p_ticker):
    url = prepare_url(p_ticker)
    response = get_html_from_screener(url)
    dictionary = parse_data_from_screener(p_ticker, response)
    # print(dictionary)

    keys = [
        SCREENER_KEYS.QR_SALES,
        SCREENER_KEYS.QR_EXPENSES,
        SCREENER_KEYS.QR_OPERATING_PROFIT,
        SCREENER_KEYS.QR_PBT,
        SCREENER_KEYS.QR_NET_PROFIT,
        SCREENER_KEYS.QR_EPS,
        SCREENER_KEYS.AR_SALES,
        SCREENER_KEYS.AR_EXPENSES,
        SCREENER_KEYS.AR_OPERATING_PROFIT,
        SCREENER_KEYS.AR_PBT,
        SCREENER_KEYS.AR_NET_PROFIT,
        SCREENER_KEYS.AR_EPS,
        SCREENER_KEYS.CF_OA
    ]

    sh_keys = [
        SCREENER_KEYS.SP_PROMOTERS,
        SCREENER_KEYS.SP_DII,
        SCREENER_KEYS.SP_FII,
        SCREENER_KEYS.SP_GOVT,
        SCREENER_KEYS.SP_PUBLIC
    ]

    if SCREENER_KEYS.SP_GOVT not in dictionary:
        del sh_keys[3]

    # print(sh_keys)

    for index, sh_key in enumerate(sh_keys):
        temp_list = dictionary[sh_key]
        dictionary['Diff ' + sh_key] = ["{:.2f}".format(float(temp_list[index + 1]) - float(val)) for index, val in
                                        enumerate(temp_list[:-1])]

    for key in keys:
        temp_list = dictionary[key]
        try:
            dictionary['Rel ' + key] = ["{:.2f}".format((float(temp_list[index + 1].replace(',', '')) if temp_list[
                                                                                                             index + 1] != '' else float(
                val.replace(',', ''))) / float(val.replace(',', ''))) for index, val in enumerate(temp_list[:-1]) if
                                        val != '']
        except ValueError:
            break
        except ZeroDivisionError:
            print(key)

    return dictionary


# parsed_json = json.loads()
print(json.dumps(get_data_from_screener_using_bs4('TATAELXSI'), indent=4))

