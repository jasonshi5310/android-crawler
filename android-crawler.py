# CSE 337 Extra Credit

from bs4 import BeautifulSoup
from urllib import request
import os


# This function is inspired by has_class_but_no_id(tag)
# https://www.crummy.com/software/BeautifulSoup/bs4/doc/#a-function
def has_data_version_added(tag):
    return tag.has_attr('data-version-added') and tag.find('h3') != None

# def has(tag):
#     return tag.name == 'div' and tag.has_attr('data-version-deprecated')


def output(tag_list, dirPath, appURL):
    for tag in tag_list:
        name = tag.text
        url = appURL+name
        r = request.urlopen(url)
        source = r.read().decode('utf-8')
        file_soup = BeautifulSoup(source, 'html.parser')
        # content = file_soup.find(id='jd-content')
        added_list = file_soup.find_all(has_data_version_added)
        # first = content.find(has_data_version_added)
        caution_list = []
        for de in added_list:
            if de.find_all('p','caution') != []:
                caution_list.append(de)
            elif de.find_all('p','note') != []:
                caution_list.append(de)
        if len(caution_list) > 0:
            if caution_list[0].has_attr('id') and caution_list[0]['id'] == 'jd-content':
                caution_list.pop(0)
        if len(caution_list) > 0:
            file = open(dirPath+name, 'w')
            result = ''
            for i in caution_list:
                h3 = i.find('h3')
                c = i.find_all(class_='caution')
                n = i.find_all(class_='note')
                if c != []:
                    result += h3.text.strip() + ':'
                    for ca in c:
                        result += ca.text.strip() + '\n'
                elif n != []:
                    result += h3.text.strip() + ':'
                    for note in n:
                        result += note.text.strip() + '\n'
            file.write(result)
            file.close()


def main():
    app_url = "https://developer.android.com/reference/android/app/"
    ps_url = app_url+"package-summary"
    response = request.urlopen(ps_url)
    page_source = response.read().decode("utf-8")
    soup = BeautifulSoup(page_source, 'html.parser')
    interfaces = []
    classes = []
    exceptions = []
    tables = soup.find_all("table", class_="jd-sumtable-expando")
    i = 0
    for t in tables:
        td_list = t.find_all('td', class_='jd-linkcol')
        for td in td_list:
            a = td.find('a')
            if i == 0:
                interfaces.append(a)
            elif i == 1:
                classes.append(a)
            else:
                exceptions.append(a)
        i+=1
    dir_path = "./outFiles/"
    if not os.path.isdir(dir_path):
        os.mkdir(dir_path)
    output(interfaces, dir_path, app_url)
    output(classes,dir_path,app_url)
    output(exceptions, dir_path, app_url)


if __name__ == '__main__':
    main()