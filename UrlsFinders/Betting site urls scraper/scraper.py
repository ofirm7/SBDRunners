from concurrent.futures import ThreadPoolExecutor

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert
import time
from bs4 import BeautifulSoup
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import concurrent.futures
import csv
import hashlib
import uuid
import os
import json
from twocaptcha import TwoCaptcha
import logging
import requests
from selenium.webdriver.common.action_chains import ActionChains
import pyautogui
import os
from PIL import ImageGrab, Image
from tkinter import Tk

URLS: list[str] = [
    r"https://sports.bet9ja.com/competition/soccer/internationalclubs/uefachampionsleague/1-11418-1695357?s=new&_gl=1*asaox2*_gcl_au*MjA1ODkwMDc3MC4xNjk2MDEzMDA2",
    r"https://sports.bet9ja.com/competition/soccer/internationalclubs/uefaeuropaleague/1-11418-1696294?s=new&_gl=1*asaox2*_gcl_au*MjA1ODkwMDc3MC4xNjk2MDEzMDA2",
    r"https://sports.bet9ja.com/competition/soccer/internationalclubs/uefaeuropaconferenceleague/1-11418-1697752?s=new&_gl=1*asaox2*_gcl_au*MjA1ODkwMDc3MC4xNjk2MDEzMDA2",
    r"https://sports.bet9ja.com/competition/soccer/internationalclubs/copalibertadores/1-11418-1542484?s=new&_gl=1*asaox2*_gcl_au*MjA1ODkwMDc3MC4xNjk2MDEzMDA2",
    r"https://sports.bet9ja.com/competition/soccer/internationalclubs/copasudamericana/1-11418-1542485?s=new&_gl=1*asaox2*_gcl_au*MjA1ODkwMDc3MC4xNjk2MDEzMDA2",
    r"https://sports.bet9ja.com/competition/soccer/internationalclubs/africanfootballleague/1-11418-4059833?s=new&_gl=1*asaox2*_gcl_au*MjA1ODkwMDc3MC4xNjk2MDEzMDA2",
    r"https://sports.bet9ja.com/competition/soccer/england/premierleague/1-11058-170880?s=new&_gl=1*asaox2*_gcl_au*MjA1ODkwMDc3MC4xNjk2MDEzMDA2",
    r"https://sports.bet9ja.com/competition/soccer/england/eflcup/1-11058-990749?s=new&_gl=1*asaox2*_gcl_au*MjA1ODkwMDc3MC4xNjk2MDEzMDA2",
    r"https://sports.bet9ja.com/competition/soccer/england/championship/1-11058-170881?s=new&_gl=1*asaox2*_gcl_au*MjA1ODkwMDc3MC4xNjk2MDEzMDA2",
    r"https://sports.bet9ja.com/competition/soccer/england/leagueone/1-11058-995354?s=new&_gl=1*asaox2*_gcl_au*MjA1ODkwMDc3MC4xNjk2MDEzMDA2",
    r"https://sports.bet9ja.com/competition/soccer/england/leaguetwo/1-11058-995355?s=new&_gl=1*asaox2*_gcl_au*MjA1ODkwMDc3MC4xNjk2MDEzMDA2",
    r"https://sports.bet9ja.com/competition/soccer/england/nationalleague/1-11058-1057831?s=new&_gl=1*asaox2*_gcl_au*MjA1ODkwMDc3MC4xNjk2MDEzMDA2",
    r"https://sports.bet9ja.com/competition/soccer/england/nationalleaguenorth/1-11058-1660731?s=new&_gl=1*asaox2*_gcl_au*MjA1ODkwMDc3MC4xNjk2MDEzMDA2",
    r"https://sports.bet9ja.com/competition/soccer/england/nationalleaguesouth/1-11058-1660637?s=new&_gl=1*asaox2*_gcl_au*MjA1ODkwMDc3MC4xNjk2MDEzMDA2",
    r"https://sports.bet9ja.com/competition/soccer/england/efltrophy/1-11058-1686314?s=new&_gl=1*asaox2*_gcl_au*MjA1ODkwMDc3MC4xNjk2MDEzMDA2",
    r"https://sports.bet9ja.com/competition/soccer/england/isthmianleaguepremierdivision/1-11058-1660692?s=new&_gl=1*asaox2*_gcl_au*MjA1ODkwMDc3MC4xNjk2MDEzMDA2",
    r"https://sports.bet9ja.com/competition/soccer/england/northernpremierleaguepremierdivision/1-11058-1660691?s=new&_gl=1*asaox2*_gcl_au*MjA1ODkwMDc3MC4xNjk2MDEzMDA2",
    r"https://sports.bet9ja.com/competition/soccer/england/southernleaguepremierdivisioncentral/1-11058-1660513?s=new&_gl=1*asaox2*_gcl_au*MjA1ODkwMDc3MC4xNjk2MDEzMDA2",
    r"https://sports.bet9ja.com/competition/soccer/england/southernleaguepremierdivisionsouth/1-11058-1660641?s=new&_gl=1*asaox2*_gcl_au*MjA1ODkwMDc3MC4xNjk2MDEzMDA2",
    r"https://sports.bet9ja.com/competition/soccer/internationalclubs/afccup/1-11418-1475778?s=new&_gl=1*asaox2*_gcl_au*MjA1ODkwMDc3MC4xNjk2MDEzMDA2",
    r"https://sports.bet9ja.com/competition/soccer/internationalclubs/concacafcaribbeancup/1-11418-4075179?s=new&_gl=1*asaox2*_gcl_au*MjA1ODkwMDc3MC4xNjk2MDEzMDA2",
    r"https://sports.bet9ja.com/competition/soccer/internationalclubs/concacafcentralamericancup/1-11418-3971002?s=new&_gl=1*asaox2*_gcl_au*MjA1ODkwMDc3MC4xNjk2MDEzMDA2",
    r"https://sports.bet9ja.com/competition/soccer/internationalyouth/u23panamericangames/1-11475-4067387?s=new&_gl=1*asaox2*_gcl_au*MjA1ODkwMDc3MC4xNjk2MDEzMDA2",
    r"https://sports.bet9ja.com/competition/soccer/spain/laliga/1-11441-180928?s=new&_gl=1*asaox2*_gcl_au*MjA1ODkwMDc3MC4xNjk2MDEzMDA2",
    r"https://sports.bet9ja.com/competition/soccer/spain/laliga2/1-11441-180929?s=new&_gl=1*asaox2*_gcl_au*MjA1ODkwMDc3MC4xNjk2MDEzMDA2",
    r"https://sports.bet9ja.com/competition/soccer/spain/primerarfef/1-11441-1687878?s=new&_gl=1*asaox2*_gcl_au*MjA1ODkwMDc3MC4xNjk2MDEzMDA2",
    r"https://sports.bet9ja.com/competition/soccer/spain/primeradivisionfemenina/1-11441-1062444?s=new&_gl=1*asaox2*_gcl_au*MjA1ODkwMDc3MC4xNjk2MDEzMDA2",
    r"https://sports.bet9ja.com/competition/soccer/italy/seriea/1-10924-167856?s=new&_gl=1*asaox2*_gcl_au*MjA1ODkwMDc3MC4xNjk2MDEzMDA2",
    r"https://sports.bet9ja.com/competition/soccer/italy/serieb/1-10924-907202?s=new&_gl=1*asaox2*_gcl_au*MjA1ODkwMDc3MC4xNjk2MDEzMDA2",
    r"https://sports.bet9ja.com/competition/soccer/italy/coppaitalia/1-10924-1042342?s=new&_gl=1*asaox2*_gcl_au*MjA1ODkwMDc3MC4xNjk2MDEzMDA2",
    r"https://sports.bet9ja.com/competition/soccer/italy/seriec/1-10924-1043683?s=new&_gl=1*asaox2*_gcl_au*MjA1ODkwMDc3MC4xNjk2MDEzMDA2",
    r"https://sports.bet9ja.com/competition/soccer/italy/seried/1-10924-1048505?s=new&_gl=1*asaox2*_gcl_au*MjA1ODkwMDc3MC4xNjk2MDEzMDA2",
    r"https://sports.bet9ja.com/competition/soccer/germany/bundesliga/1-10943-180923?s=new&_gl=1*asaox2*_gcl_au*MjA1ODkwMDc3MC4xNjk2MDEzMDA2",
    r"https://sports.bet9ja.com/competition/soccer/germany/2.bundesliga/1-10943-180924?s=new&_gl=1*asaox2*_gcl_au*MjA1ODkwMDc3MC4xNjk2MDEzMDA2",
    r"https://sports.bet9ja.com/competition/soccer/germany/3.liga/1-10943-168228?s=new&_gl=1*asaox2*_gcl_au*MjA1ODkwMDc3MC4xNjk2MDEzMDA2",
    r"https://sports.bet9ja.com/competition/soccer/germany/dfbpokal/1-10943-184976?s=new&_gl=1*asaox2*_gcl_au*MjA1ODkwMDc3MC4xNjk2MDEzMDA2",
    r"https://sports.bet9ja.com/competition/soccer/germany/regionalligasouthwest/1-10943-1010314?s=new&_gl=1*asaox2*_gcl_au*MjA1ODkwMDc3MC4xNjk2MDEzMDA2",
    r"https://sports.bet9ja.com/competition/soccer/germany/regionalligawest/1-10943-1014719?s=new&_gl=1*asaox2*_gcl_au*MjA1ODkwMDc3MC4xNjk2MDEzMDA2",
    r"https://sports.bet9ja.com/competition/soccer/france/ligue1/1-11442-950503?s=new&_gl=1*asaox2*_gcl_au*MjA1ODkwMDc3MC4xNjk2MDEzMDA2",
    r"https://sports.bet9ja.com/competition/soccer/france/ligue2/1-11442-958691?s=new&_gl=1*asaox2*_gcl_au*MjA1ODkwMDc3MC4xNjk2MDEzMDA2",
    r"https://sports.bet9ja.com/competition/soccer/netherlands/eredivisie/1-11077-1016657?s=new&_gl=1*asaox2*_gcl_au*MjA1ODkwMDc3MC4xNjk2MDEzMDA2",
    r"https://sports.bet9ja.com/competition/soccer/netherlands/eerstedivisie/1-11077-992239?s=new&_gl=1*asaox2*_gcl_au*MjA1ODkwMDc3MC4xNjk2MDEzMDA2",
    r"https://sports.bet9ja.com/competition/soccer/netherlands/knvbbeker/1-11077-1008683?s=new&_gl=1*asaox2*_gcl_au*MjA1ODkwMDc3MC4xNjk2MDEzMDA2",
    r"https://sports.bet9ja.com/competition/soccer/netherlands/tweededivisie/1-11077-1679712?s=new&_gl=1*asaox2*_gcl_au*MjA1ODkwMDc3MC4xNjk2MDEzMDA2",
    r"https://sports.bet9ja.com/competition/soccer/albania/kategoriasuperiore/1-11531-1115732?s=new&_gl=1*asaox2*_gcl_au*MjA1ODkwMDc3MC4xNjk2MDEzMDA2",
    r"https://sports.bet9ja.com/competition/soccer/andorra/primeradivisio/1-27230-1159100?s=new&_gl=1*asaox2*_gcl_au*MjA1ODkwMDc3MC4xNjk2MDEzMDA2",
    r"https://sports.bet9ja.com/competition/soccer/angola/girabola/1-29025-1209855?s=new&_gl=1*asaox2*_gcl_au*MjA1ODkwMDc3MC4xNjk2MDEzMDA2",
    r"https://sports.bet9ja.com/competition/soccer/argentina/copadelaliga/1-11451-1291347?s=new&_gl=1*asaox2*_gcl_au*MjA1ODkwMDc3MC4xNjk2MDEzMDA2",
    r"https://sports.bet9ja.com/competition/soccer/argentina/torneofederala/1-11451-1407000?s=new&_gl=1*asaox2*_gcl_au*MjA1ODkwMDc3MC4xNjk2MDEzMDA2",
    r"https://sports.bet9ja.com/competition/soccer/argentina/primerabgrandfinal/1-11451-1864089?s=new&_gl=1*asaox2*_gcl_au*MjA1ODkwMDc3MC4xNjk2MDEzMDA2",
    r"https://sports.bet9ja.com/competition/soccer/argentina/primerabpromotionplayoffs/1-11451-1886567?s=new&_gl=1*asaox2*_gcl_au*MjA1ODkwMDc3MC4xNjk2MDEzMDA2",
    r"https://sports.bet9ja.com/competition/soccer/argentina/primeracpromotionplayoffs/1-11451-1886218?s=new&_gl=1*asaox2*_gcl_au*MjA1ODkwMDc3MC4xNjk2MDEzMDA2",
    r"https://sports.bet9ja.com/competition/soccer/argentina/primeradclausura/1-11451-1656520?s=new&_gl=1*asaox2*_gcl_au*MjA1ODkwMDc3MC4xNjk2MDEzMDA2",
    r"https://sports.bet9ja.com/competition/soccer/argentina/primeranacionalgrandfinal/1-11451-1891891?s=new&_gl=1*asaox2*_gcl_au*MjA1ODkwMDc3MC4xNjk2MDEzMDA2",
    r"https://sports.bet9ja.com/competition/soccer/argentina/primeranacionalpromotionplayoffs/1-11451-1889635?s=new&_gl=1*asaox2*_gcl_au*MjA1ODkwMDc3MC4xNjk2MDEzMDA2",
    r"https://sports.bet9ja.com/competition/soccer/armenia/premierleague/1-12099-198738?s=new&_gl=1*asaox2*_gcl_au*MjA1ODkwMDc3MC4xNjk2MDEzMDA2",
    r"https://sports.bet9ja.com/competition/soccer/australia/a-league/1-11462-1164367?s=new&_gl=1*asaox2*_gcl_au*MjA1ODkwMDc3MC4xNjk2MDEzMDA2",
    r"https://sports.bet9ja.com/competition/soccer/australia/w-league/1-11462-1206086?s=new&_gl=1*asaox2*_gcl_au*MjA1ODkwMDc3MC4xNjk2MDEzMDA2",
    r"https://sports.bet9ja.com/competition/soccer/austria/bundesliga/1-11075-992336?s=new&_gl=1*asaox2*_gcl_au*MjA1ODkwMDc3MC4xNjk2MDEzMDA2",
    r"https://sports.bet9ja.com/competition/soccer/austria/2.liga/1-11075-188632?s=new&_gl=1*asaox2*_gcl_au*MjA1ODkwMDc3MC4xNjk2MDEzMDA2",
    r"https://sports.bet9ja.com/competition/soccer/azerbaijan/premierleague/1-11452-920377?s=new&_gl=1*asaox2*_gcl_au*MjA1ODkwMDc3MC4xNjk2MDEzMDA2",
    r"https://sports.bet9ja.com/competition/soccer/bahrain/premierleague/1-11553-974856?s=new&_gl=1*asaox2*_gcl_au*MjA1ODkwMDc3MC4xNjk2MDEzMDA2",
    r"https://sports.bet9ja.com/competition/soccer/belgium/proleague/1-11455-958370?s=new&_gl=1*asaox2*_gcl_au*MjA1ODkwMDc3MC4xNjk2MDEzMDA2",
    r"https://sports.bet9ja.com/competition/soccer/belgium/firstdivisionb/1-11455-989222?s=new&_gl=1*asaox2*_gcl_au*MjA1ODkwMDc3MC4xNjk2MDEzMDA2",
    r"https://sports.bet9ja.com/competition/soccer/bosnia%26herzegovina/premijerliga/1-12026-966967?s=new&_gl=1*asaox2*_gcl_au*MjA1ODkwMDc3MC4xNjk2MDEzMDA2",
    r"https://sports.bet9ja.com/competition/soccer/brazil/brasileiroseriea/1-10987-964311?s=new&_gl=1*asaox2*_gcl_au*MjA1ODkwMDc3MC4xNjk2MDEzMDA2",
    r"https://sports.bet9ja.com/competition/soccer/brazil/brasileiroserieb/1-10987-1500335?s=new&_gl=1*asaox2*_gcl_au*MjA1ODkwMDc3MC4xNjk2MDEzMDA2",
    r"https://sports.bet9ja.com/competition/soccer/bulgaria/parvaliga/1-11447-600906?s=new&_gl=1*asaox2*_gcl_au*MjA1ODkwMDc3MC4xNjk2MDEzMDA2",
    r"https://sports.bet9ja.com/competition/soccer/chile/primeradivision/1-11063-1004077?s=new&_gl=1*asaox2*_gcl_au*MjA1ODkwMDc3MC4xNjk2MDEzMDA2",
    r"https://sports.bet9ja.com/competition/soccer/china/chinesesuperleague/1-12016-1414963?s=new&_gl=1*asaox2*_gcl_au*MjA1ODkwMDc3MC4xNjk2MDEzMDA2",
    r"https://sports.bet9ja.com/competition/soccer/colombia/primeraaclausura/1-11069-1603893?s=new&_gl=1*asaox2*_gcl_au*MjA1ODkwMDc3MC4xNjk2MDEzMDA2",
    r"https://sports.bet9ja.com/competition/soccer/colombia/primerabclausurapromotion/1-11069-1846018?s=new&_gl=1*asaox2*_gcl_au*MjA1ODkwMDc3MC4xNjk2MDEzMDA2",
    r"https://sports.bet9ja.com/competition/soccer/colombia/copacolombia/1-11069-1047008?s=new&_gl=1*asaox2*_gcl_au*MjA1ODkwMDc3MC4xNjk2MDEzMDA2",
    r"https://sports.bet9ja.com/competition/soccer/costarica/primeradivisionapertura/1-11473-1627615?s=new&_gl=1*asaox2*_gcl_au*MjA1ODkwMDc3MC4xNjk2MDEzMDA2",
    r"https://sports.bet9ja.com/competition/soccer/costarica/ligadeascensoapertura/1-11473-1654218?s=new&_gl=1*asaox2*_gcl_au*MjA1ODkwMDc3MC4xNjk2MDEzMDA2",
    r"https://sports.bet9ja.com/competition/soccer/croatia/1.hnl/1-11421-180725?s=new&_gl=1*asaox2*_gcl_au*MjA1ODkwMDc3MC4xNjk2MDEzMDA2",
    r"https://sports.bet9ja.com/competition/soccer/croatia/2.hnl/1-11421-982563?s=new&_gl=1*asaox2*_gcl_au*MjA1ODkwMDc3MC4xNjk2MDEzMDA2",
    r"https://sports.bet9ja.com/competition/soccer/cyprus/1stdivision/1-11457-988097?s=new&_gl=1*asaox2*_gcl_au*MjA1ODkwMDc3MC4xNjk2MDEzMDA2",
    r"https://sports.bet9ja.com/competition/soccer/czechrepublic/1.liga/1-11491-187345?s=new&_gl=1*asaox2*_gcl_au*MjA1ODkwMDc3MC4xNjk2MDEzMDA2",
    r"https://sports.bet9ja.com/competition/soccer/czechrepublic/fnl/1-11491-813732?s=new&_gl=1*asaox2*_gcl_au*MjA1ODkwMDc3MC4xNjk2MDEzMDA2",
    r"https://sports.bet9ja.com/competition/soccer/denmark/superligaen/1-10940-587103?s=new&_gl=1*asaox2*_gcl_au*MjA1ODkwMDc3MC4xNjk2MDEzMDA2",
    r"https://sports.bet9ja.com/competition/soccer/denmark/1stdivision/1-10940-522097?s=new&_gl=1*asaox2*_gcl_au*MjA1ODkwMDc3MC4xNjk2MDEzMDA2",
    r"https://sports.bet9ja.com/competition/soccer/ecuador/ligaproprimeraa/1-11754-1619774?s=new&_gl=1*asaox2*_gcl_au*MjA1ODkwMDc3MC4xNjk2MDEzMDA2",
    r"https://sports.bet9ja.com/competition/soccer/egypt/premierleague/1-11419-973090?s=new&_gl=1*asaox2*_gcl_au*MjA1ODkwMDc3MC4xNjk2MDEzMDA2",
    r"https://sports.bet9ja.com/competition/soccer/egypt/2.divisiona/1-11419-3964508?s=new&_gl=1*asaox2*_gcl_au*MjA1ODkwMDc3MC4xNjk2MDEzMDA2",
    r"https://sports.bet9ja.com/competition/soccer/elsalvador/primeradivisionapertura/1-11530-1636914?s=new&_gl=1*asaox2*_gcl_au*MjA1ODkwMDc3MC4xNjk2MDEzMDA2",
    r"https://sports.bet9ja.com/competition/soccer/estonia/esiliiga/1-12021-1329525?s=new&_gl=1*asaox2*_gcl_au*MjA1ODkwMDc3MC4xNjk2MDEzMDA2",
    r"https://sports.bet9ja.com/competition/soccer/greece/superleague1/1-11071-1018979?s=new&_gl=1*asaox2*_gcl_au*MjA1ODkwMDc3MC4xNjk2MDEzMDA2",
    r"https://sports.bet9ja.com/competition/soccer/greece/superleague2/1-11071-1853372?s=new&_gl=1*asaox2*_gcl_au*MjA1ODkwMDc3MC4xNjk2MDEzMDA2",
    r"https://sports.bet9ja.com/competition/soccer/guatemala/liganacionalapertura/1-11478-1633787?s=new&_gl=1*asaox2*_gcl_au*MjA1ODkwMDc3MC4xNjk2MDEzMDA2",
    r"https://sports.bet9ja.com/competition/soccer/honduras/liganacionalapertura/1-11477-1651722?s=new&_gl=1*asaox2*_gcl_au*MjA1ODkwMDc3MC4xNjk2MDEzMDA2",
    r"https://sports.bet9ja.com/competition/soccer/hungary/nbi/1-11881-194328?s=new&_gl=1*asaox2*_gcl_au*MjA1ODkwMDc3MC4xNjk2MDEzMDA2",
    r"https://sports.bet9ja.com/competition/soccer/india/indiansuperleague/1-11066-1141249?s=new&_gl=1*asaox2*_gcl_au*MjA1ODkwMDc3MC4xNjk2MDEzMDA2",
    r"https://sports.bet9ja.com/competition/soccer/indonesia/liga1/1-11476-1692281?s=new&_gl=1*asaox2*_gcl_au*MjA1ODkwMDc3MC4xNjk2MDEzMDA2",
    r"https://sports.bet9ja.com/competition/soccer/ireland/premierdivision/1-11893-1345657?s=new&_gl=1*asaox2*_gcl_au*MjA1ODkwMDc3MC4xNjk2MDEzMDA2",
    r"https://sports.bet9ja.com/competition/soccer/ivorycoast/ligue1/1-11523-1381052?s=new&_gl=1*asaox2*_gcl_au*MjA1ODkwMDc3MC4xNjk2MDEzMDA2",
    r"https://sports.bet9ja.com/competition/soccer/jamaica/premierleague/1-11529-1567564?s=new&_gl=1*asaox2*_gcl_au*MjA1ODkwMDc3MC4xNjk2MDEzMDA2",
    r"https://sports.bet9ja.com/competition/soccer/japan/j.league/1-11072-918119?s=new&_gl=1*asaox2*_gcl_au*MjA1ODkwMDc3MC4xNjk2MDEzMDA2",
    r"https://sports.bet9ja.com/competition/soccer/japan/j.leaguecupplayoffs/1-11072-1509552?s=new&_gl=1*asaox2*_gcl_au*MjA1ODkwMDc3MC4xNjk2MDEzMDA2",
    r"https://sports.bet9ja.com/competition/soccer/japan/j.league2/1-11072-923979?s=new&_gl=1*asaox2*_gcl_au*MjA1ODkwMDc3MC4xNjk2MDEzMDA2",
    r"https://sports.bet9ja.com/competition/soccer/lithuania/alyga/1-12039-1332088?s=new&_gl=1*asaox2*_gcl_au*MjA1ODkwMDc3MC4xNjk2MDEzMDA2",
]

url_format: str = "r\"{url}\",\n"

# ? loading website
BASE_URL = "https://sports.bet9ja.com/competition/soccer/international/uefanationsleaguewomen/1-11463-3952843?s=new&_gl=1*asaox2*_gcl_au*MjA1ODkwMDc3MC4xNjk2MDEzMDA2"

options = Options()
# options.add_experimental_option('debuggerAddress', '127.0.0.1:9222')
options.add_argument('start-maximized')
driver = webdriver.Chrome(service=Service(
    executable_path='./chromedriver-win64/chromedriver-win64/chromedriver.exe'), options=options)
action=ActionChains(driver)
driver.get(BASE_URL)
time.sleep(5)

# clicking soccer 
WebDriverWait(driver,20).until(EC.presence_of_element_located((By.XPATH,"//div[text()='Soccer']")))
soccer=driver.find_elements(By.XPATH,"//div[text()='Soccer']")[0]
action.move_to_element(soccer).click().perform()
time.sleep(3)


# clicking showmore
showMore=driver.find_element(By.ID,"left_prematch_sport-1_soccer_buttonmore-toggle")
driver.execute_script("arguments[0].click();", showMore)

# # clicking on accordian items
container=WebDriverWait(driver,20).until(EC.presence_of_element_located((By.CLASS_NAME,"accordion-item.accordion-item--open")))
accordian_items=container.find_elements(By.CLASS_NAME,"accordion-item")
print(accordian_items[-1].get_attribute("innerText"))
with open("urls.txt",'a+') as f:
    for item in accordian_items:
        try:
           item.click()
        except:
           action.move_to_element(item).click().perform()
            
        links=item.find_elements(By.CLASS_NAME,'menu-list__item')
        
        for link in links:
            try:
                link.click()
                print(driver.current_url)
                f.write(url_format.format(url=driver.current_url))
            except:
                try:
                    action.move_to_element(link).click().perform()
                    print(driver.current_url)
                    f.write(url_format.format(url=driver.current_url))
                except:
                   continue
    
    for url in URLS:
        f.write(url_format.format(url=url))
                
                
