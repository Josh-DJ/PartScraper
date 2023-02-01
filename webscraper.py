from urllib.request import urlopen as uO
from bs4 import BeautifulSoup  as soup
import requests

def print_menu ():
    print("Choose an option. \n")
    print("1. GPU Products")
    print("2. CPU Products")
    print("3. Motherboard Products")
    print("4. Go back to Stores")
    print("5. Exit")

def storeChoice():
    print("Select store. \n")
    print("1. Best Buy")
    print("2. NewEgg.")
    print("3. Exit")

def gpu():
    url = 'https://www.newegg.com/Video-Cards-Video-Devices/Category/ID-38?Tpk=graphics%20card'
    html = uO(url) #This opens up the url
    page_html = html.read() #Reads the lines from the page
    html.close() #Closes the website
    page_soup = soup(page_html, "html.parser") #Calls BS to parse and clean up html
    #Finds all item-container tags and stores them in an array. All GPU's on page are stored there.
    items = page_soup.findAll("div", {"class" : "item-container"})
    print("\nGPU")
    print("---------------------------------------------------------------------------------\n")

    #Item is an individual item-container. In this case it would mean an individual product.
    for item in items:
        neProdInfo(item)
        
def cpu ():
    url = 'https://www.newegg.com/CPUs-Processors/Category/ID-34'
    html = uO(url) 
    page_html = html.read()
    html.close()
    page_soup = soup(page_html, "html.parser")
    cpus = page_soup.findAll("div", {"class" : "item-container"})
    print("CPU")
    print("---------------------------------------------------------------------------------")

    for cpu in cpus:
        neProdInfo(cpu)
        
def Motherbrd():
    url = 'https://www.newegg.com/Motherboards/Category/ID-20'
    html = uO(url) 
    page_html = html.read()
    html.close()
    page_soup = soup(page_html, "html.parser")
    MOBOS = page_soup.findAll("div", {"class" : "item-container"})
    print("MOBOS")
    print("---------------------------------------------------------------------------------")
    for MOBO in MOBOS:
        neProdInfo(MOBO)

def neProdInfo(product):
    #Goes to the first div inside the item-container. Would be item-branding.
    brand = product.div.a.img["title"]
    print(brand)

    #To find the rest of the information we need to use find.
    if product.find("div", {"class" : "item-branding"}).find("a", {"class" , "item-rating"}) is None:
        print("No Rating")
    else:
        rating = product.find("div", {"class" : "item-branding"}).find("a", {"class", "item-rating"})["title"]
        print(rating)
    title = product.find("a", {"class": "item-title"}).text
    print(title)


    if product.find("div", {"class": "item-action"}).ul.find("li", {"class": "price-current"}).strong == None:
        print("Item has no price.")
    else:
        price = product.find("div", {"class": "item-action"}).ul.find("li", {"class": "price-current"}).strong.text
        cents = product.find("div", {"class": "item-action"}).ul.find("li", {"class": "price-current"}).sup.text
        print("$" + price + cents)
    shipping = product.find("div", {"class": "item-action"}).ul.find("li", {"class": "price-ship"}).text.strip()
    if(shipping == ""):
        print("No shipping. \n")
    else:
        print(shipping + "\n")

def bbCPU(header):

    url = 'https://www.bestbuy.com/site/computer-cards-components/computer-pc-processors/abcat0507010.c?id=abcat0507010'
    r = requests.get(url, headers=header)
    sop = soup(r.text, 'html.parser')
    pages = len(sop.findAll("li" , {"class" : "page-item"})) #Finds the html for page count. The length is how many pages it
    #Looping through the pages
    for x in range(1,pages+1):
        #Here the {x} signifies data we are changing. It signifies when we change a page.
        url = f'https://www.bestbuy.com/site/searchpage.jsp?_dyncharset=UTF-8&browsedCategory=abcat0507010&cp={x}&id=pcat17071&iht=n&ks=960&list=y&sc=Global&st=categoryid%24abcat0507010&type=page&usc=All%20Categories'
        r = requests.get(url, headers=header)
        sop = soup(r.text, 'html.parser')
        # The reason we use {"class":"sku-item"} as a dict, is because we are searching a tag by the CSS class.
        items = sop.findAll("li", {"class": "sku-item"})
        for item in items:
            bbProdInfo(item)

def bbGPU(header):
    url = 'https://www.bestbuy.com/site/computer-cards-components/video-graphics-cards/abcat0507002.c?id=abcat0507002'
    r = requests.get(url, headers = header)
    sop = soup(r.text, 'html.parser')
    pages = len(sop.findAll("li", {"class":"page-item"}))

    for x in range(1, pages+1):
        url = f'https://www.bestbuy.com/site/searchpage.jsp?_dyncharset=UTF-8&browsedCategory=abcat0507002&cp={x}&id=pcat17071&iht=n&ks=960&list=y&sc=Global&st=categoryid%24abcat0507002&type=page&usc=All%20Categories'
        r = requests.get(url, headers=header)
        sop = soup(r.text, 'html.parser')
        items = sop.findAll("li", {"class": "sku-item"})
        for item in items:
            bbProdInfo(item)


def bbMobo(header):
    url = 'https://www.bestbuy.com/site/computer-cards-components/motherboards/abcat0507008.c?id=abcat0507008'
    r = requests.get(url, headers=header)
    sop = soup(r.text, 'html.parser')
    pages = len(sop.findAll("li", {"class": "page-item"}))

    for x in range(1, pages + 1):
        url = f'https://www.bestbuy.com/site/searchpage.jsp?_dyncharset=UTF-8&browsedCategory=abcat0507008&cp=2&id=pcat17071&iht=n&ks=960&list=y&sc=Global&st=categoryid%24abcat0507008&type=page&usc=All%20Categories'
        r = requests.get(url, headers=header)
        sop = soup(r.text, 'html.parser')
        items = sop.findAll("li", {"class": "sku-item"})
        for item in items:
            bbProdInfo(item)


def bbProdInfo(item):
    # Rating
    ratings = item.find("p", {"class": "visually-hidden"}).text
    print(ratings)

    # Name
    name = item.find("h4", {"class": "sku-title"})  # No bundle product
    if name is not None:
        print(name.a.text)
    else:
        name = item.find("h4", {"class": "sku-header"}).a.text  # Bundled product
        print(name)

    # Pricing
    price = item.find("div", {"class": "priceView-hero-price priceView-customer-price"}).span.text
    print(price + "\n")

def menuRun(store, header):
    i = 0
    while i == 0:
        print_menu()
        choice = input()
        if choice == "1":
            if store == 1:
                bbGPU(header)
            elif store == 2:
                gpu()
        elif choice == "2":
            #cpu()
            if store == 1:
                bbCPU(header)
            elif store == 2:
                cpu()
        elif choice == "3":
            #Motherbrd()
            if store == 1:
                bbMobo(header)
            elif store == 2:
                Motherbrd()
        elif choice == "4":
            break
        elif choice == "5":
            exit()
        else:
            print("Wrong input. Please enter correct input.\n")

def main():
    headers = {
        'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36',
        'Accept-Language' : 'en-GB,en;q=0.5',
        'Referer': 'https://www.bestbuy.com'}
    i = 0
    while i == 0:
        storeChoice()
        choice = input()
        if choice == "1":
            menuRun(1, headers)
        elif choice == "2":
            menuRun(2, headers)
        elif choice == "3":
            exit()
        else:
            print("Wrong input. Please enter correct input.\n")
main()