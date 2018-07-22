#fichier readwebwindows
#outils d'ini du driver selenium avec chrom pour windows
#initwebwindows renvoie le driver initialisé, et avec telechargement dans c:\tmp

# attention, avec les derniers selenium (3.13 il faut chrome driver 2.33 sinon le change dowload directory ne marche pas


from selenium import webdriver
import selenium

timeout = 120

def initwebwindows():

    # personalisation des options(rep de download et adresse vers chromdriver
    options = webdriver.ChromeOptions()
    prefs = {"download.default_directory": "c:\\tmp"} #\\pour windows
    options.add_experimental_option("prefs", prefs)
   # options.add_argument("headless");
    chromedriver = u"c:/windows/system32/chromedriver.exe"
    driver = webdriver.Chrome(executable_path=chromedriver, chrome_options=options)
    driver.set_page_load_timeout(timeout)
    return driver