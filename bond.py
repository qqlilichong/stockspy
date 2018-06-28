
#############################################################

import configparser
from mantools import *
from emailtools import EMailSender
from selenium import webdriver

#############################################################

class PriceSpy:

    #############################################################

    @staticmethod
    def run(paramlist):
        return reactor_reduce(paramlist, PriceSpy.mapper_job, len(paramlist))

    #############################################################

    @staticmethod
    def mapper_job(env):
        return env['MAIN'](env)

    #############################################################

    @staticmethod
    def mapper_main(env):
        options = webdriver.ChromeOptions()
        options.add_argument(r'headless')
        browser = webdriver.Chrome(chrome_options=options)
        timer_notify = TimeDeltaer()

        try:
            browser.get(env['URL'])
            tag_price = env['PRICEFINDER'](browser)

            while env['CHECKER_TRADING']():
                price_real = stof(tag_price.text)
                env['RT_REAL'] = price_real
                file_create(env['CACHE'], str(price_real).encode('utf-8'))
                if price_real < env['NICE']:
                    continue

                env['RT_PAGESOURCE'] = browser.page_source
                if timer_notify.check(seconds=300):
                    env['NOTIFYER'](env)

        finally:
            print('Spy Bond Price Quit : %s' % env['URL'])
            browser.close()
            browser.quit()
            return 0

    #############################################################

    @staticmethod
    def checker_trading_bond(sleep=1):
        time.sleep(sleep)
        return True
        # stm = time.struct_time(time.localtime(time.time()))
        # if 9 <= stm.tm_hour <= 15:
        # return True
        # return False

    #############################################################

    @staticmethod
    def pricefinder_bond(browser):
        return browser.find_element_by_tag_name('big')

    #############################################################

    @staticmethod
    def timer_bond(env):
        timer = TimeDeltaer()
        timer.check()
        while env['CHECKER_TRADING']():
            if not timer.check(seconds=60):
                continue

            pricetable = dict()
            for pf in os.listdir(env['CACHE']):
                pf = os.path.join(env['CACHE'], pf)
                if pf.endswith('.price'):
                    pricetable[os.path.splitext(os.path.basename(pf))[0]] = stof(file_read(pf))

            pp = '****************** Bond Price %s ******************' % sftime()
            pp += '\n'
            pp += jformat(pricetable)
            print(pp)

    #############################################################

    @staticmethod
    def notifyer_email_bond(env):
        ini = configparser.ConfigParser()
        ini.read(os.path.join(os.path.dirname(__file__), 'stockspy.ini'))
        smtp = ini.get('EMAIL', 'smtp').strip()
        user = ini.get('EMAIL', 'user').strip()
        pawd = ini.get('EMAIL', 'pawd').strip()
        toli = ini.get('EMAIL', 'toli').strip().split(',')

        info = r'$$[ %s : %s ] - BondPrice - %s$$' % (env['SCODE'], env['RT_REAL'], sftime())
        notifyer = EMailSender(smtp, user, pawd)
        if not notifyer.sendmail(toli, info, env['RT_PAGESOURCE'], 'html'):
            print('ERROR, %s' % info)
        notifyer.close()

    #############################################################

#############################################################

if __name__ == '__main__':

    # All Spy.
    envlist = list()

    # Init Spy Bond.
    cache_bond = os.path.join(os.path.dirname(__file__), 'spy_bond')
    file_remove(cache_bond)
    file_mkdir(cache_bond)
    bond_scodelist = [
        '204001',
        '204002',
        '204003',
        '204004',
        '204007',
        '204014',
        '204028',
        '204091',
        '204182',
        '131810',
        '131811',
        '131800',
        '131809',
        '131801',
        '131802',
        '131803',
        '131805',
        '131806',
    ]

    # Ready Spy Bond.
    env_bondtimer = dict()
    env_bondtimer['MAIN'] = PriceSpy.timer_bond
    env_bondtimer['CHECKER_TRADING'] = PriceSpy.checker_trading_bond
    env_bondtimer['CACHE'] = cache_bond
    envlist.append(env_bondtimer)
    for bond_scode in bond_scodelist:
        env_bond = dict()
        env_bond['NICE'] = float(15.0)
        env_bond['MAIN'] = PriceSpy.mapper_main
        env_bond['SCODE'] = bond_scode
        env_bond['URL'] = r'http://quotes.money.163.com/bond/%s.html' % bond_scode
        env_bond['CACHE'] = os.path.join(cache_bond, '%s.price' % bond_scode)
        env_bond['CHECKER_TRADING'] = PriceSpy.checker_trading_bond
        env_bond['PRICEFINDER'] = PriceSpy.pricefinder_bond
        env_bond['NOTIFYER'] = PriceSpy.notifyer_email_bond
        envlist.append(env_bond)

    # Running Spy.
    PriceSpy.run(envlist)

#############################################################
