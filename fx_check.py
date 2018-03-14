
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
import wget
from sys import exit


headers = {
    'User-Agent': "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"}


def get_site_data():

    link = 'http://cdn01.foxitsoftware.com/pub/foxit/reader/desktop/linux/2.x'
    print('\n')
    print('Getting Site ...')
    req = urllib.request.Request(link, headers=headers)
    resp = urllib.request.urlopen(req)
    resp_data = resp.read()
    return resp_data


def get_latest_version_dir(resp_site_data):
    """
    Extract the table of available versions, the latest is 2.4
    Starting from row 3 to the latest row (of version 2.4)
    """
    soup = BeautifulSoup(resp_site_data, "lxml")
    table = soup.find('table')
    row = table.find_all('tr')[3:7]

    versions = []
    for v in row:
        v = v.text
        versions.append(v[0:3])

    print("Available versions {}".format(versions))
    return versions


def check_latest_directory(versions):
    if versions[-1] != '2.4':
        print('########################################################')
        print('###################### NEW VERSION!! ###################')
        print('########################################################')
        latest_version_num = versions[-1]
        print('Latest Version is {}'.format(latest_version_num))
        return latest_version_num

    else:
        print('########################################################')
        print('################### NO NEW VERSION!! ###################')
        print('########################################################')
        exit()


def souping_latest_version(latest_version_num):
    link_directory = 'http://cdn01.foxitsoftware.com/pub/foxit/reader/desktop/linux/2.x/{}/en_us/'.format(
        latest_version_num)
    open_link = urllib.request.Request(link_directory, headers=headers)
    resp_data = urllib.request.urlopen(open_link)
    soup = BeautifulSoup(resp_data, "lxml")
    table = soup.find('table')
    tr = table.find_all('tr')[3]
    # print(tr)
    td = tr.find_all('td')[1]
    row_version = td.text
    print("Getting Latest App Version: {}".format(row_version))
    # row_version = table.find_all('tr')[3]
    # row_version = row_version.text
    print(row_version)
    return row_version, link_directory


def updating(row_version, link_directory):
    user_input = input(
        'Do You Want To Download the latest version [Y | N ] > ')

    if user_input.lower() == 'y':
        print('Downloading The Latest version ...')
        dl_link = link_directory + "{}".format(
            row_version)

        wget.download(dl_link)


def main():
    try:
        site_data = get_site_data()
        latest_v_dir = get_latest_version_dir(site_data)
        check_latest_v_dir = check_latest_directory(latest_v_dir)
        latest_v_app = souping_latest_version(check_latest_v_dir)
        update = updating(latest_v_app[0], latest_v_app[1])

        update
    except KeyboardInterrupt:
        print('\n')
        print('Bye Bye')
        print('\n')


main()
