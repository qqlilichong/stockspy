
#############################################################

import configparser
from mantools import *
from emailtools import EMailSender
from selenium import webdriver

#############################################################

class BondSpy:

    #############################################################

    url_base = r'http://quotes.money.163.com/bond/%s.html'
    price_good = float(7.0)
    price_cache = os.path.join(os.path.dirname(__file__), 'pbond')

    #############################################################

    @staticmethod
    def ontrading(sleep=1):
        time.sleep(sleep)
        return True
        # stm = time.struct_time(time.localtime(time.time()))
        # if 9 <= stm.tm_hour <= 15:
        # return True
        # return False

    #############################################################

    @staticmethod
    def price(paramlist):
        return reactor_reduce(paramlist, BondSpy.mapper_price, len(paramlist))

    #############################################################

    @staticmethod
    def finder_price(browser):
        tag_price = browser.find_element_by_tag_name('big')
        return float(tag_price.text)

    #############################################################

    @staticmethod
    def mapper_price(param):
        setting, scode = param
        if scode == 'timer':
            return BondSpy.mapper_timer()

        options = webdriver.ChromeOptions()
        options.add_argument(r'headless')
        browser = webdriver.Chrome(chrome_options=options)
        url_bond = BondSpy.url_base % scode
        cache = os.path.join(BondSpy.price_cache, '%s.price' % scode)
        timer_notify = TimeDeltaer()

        try:
            browser.get(url_bond)
            while BondSpy.ontrading():
                price_real = BondSpy.finder_price(browser)
                file_create(cache, str(price_real).encode('utf-8'))
                if price_real < BondSpy.price_good:
                    continue

                if timer_notify.check(seconds=300):
                    BondSpy.notify(setting, scode, price_real)

        finally:
            print('Spy Bond Price Quit : %s' % url_bond)
            browser.close()
            browser.quit()
            return 0

    #############################################################

    @staticmethod
    def mapper_timer():
        timer = TimeDeltaer()
        timer.check()
        while BondSpy.ontrading():
            if not timer.check(seconds=60):
                continue

            pricetable = dict()
            for pf in os.listdir(BondSpy.price_cache):
                pf = os.path.join(BondSpy.price_cache, pf)
                if pf.endswith('.price'):
                    pricetable[os.path.splitext(os.path.basename(pf))[0]] = stof(file_read(pf))

            pp = '****************** Bond Price %s ******************' % sftime()
            pp += '\n'
            pp += jformat(pricetable)
            print(pp)

    #############################################################

    @staticmethod
    def notify(setting, scode, price):
        info = 'Notify Bond Price [ %s : %s ] - %s' % (scode, price, sftime())
        notifyer = EMailSender(setting['email_smtp'], setting['email_user'], setting['email_pawd'])
        if not notifyer.sendmail(setting['email_toli'], info, info):
            print('ERROR, %s' % info)
        notifyer.close()

    #############################################################

#############################################################

if __name__ == '__main__':
    # Load Config.
    ini = configparser.ConfigParser()
    ini.read(os.path.join(os.path.dirname(__file__), 'stockspy.ini'))
    config = dict()
    config['email_smtp'] = ini.get('EMAIL', 'smtp').strip()
    config['email_user'] = ini.get('EMAIL', 'user').strip()
    config['email_pawd'] = ini.get('EMAIL', 'pawd').strip()
    config['email_toli'] = ini.get('EMAIL', 'toli').strip().split(',')

    # Running Spy.
    file_mkdir(BondSpy.price_cache)
    BondSpy.price([
        (config, 'timer'),

        (config, '204001'),
        (config, '204002'),
        (config, '204003'),
        (config, '204004'),
        (config, '204007'),
        (config, '204014'),
        (config, '204028'),
        (config, '204091'),
        (config, '204182'),

        (config, '131810'),
        (config, '131811'),
        (config, '131800'),
        (config, '131809'),
        (config, '131801'),
        (config, '131802'),
        (config, '131803'),
        (config, '131805'),
        (config, '131806'),
    ])
    exit(0)

#############################################################
