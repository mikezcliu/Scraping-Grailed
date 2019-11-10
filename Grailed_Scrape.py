import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
import time
#https://stackoverflow.com/questions/56478652/scraping-text-in-h3-and-p-tags-using-beautifulsoup-python
#https://omnianalytics.io/2018/08/28/ebay-web-scrape-tutorial/

# https://medium.com/the-andela-way/introduction-to-web-scraping-using-selenium-7ec377a8cf72

# THIS FUCKING WORKS!!!!!!!!!!!!!!!
# THIS FUCKING WORKS!!!!!!!!!!!!!!!
# THIS FUCKING WORKS!!!!!!!!!!!!!!!


# Set a "base" URL that we can append onto
base_url = "https://www.grailed.com/sold/hLVZqhMQcg"



# open up chrome. Don't use headless otherwise the feed-item doesn't fully load all the way
chrome_options = webdriver.ChromeOptions()
        # dont open up the chrome
#chrome_options.add_argument('--headless')
driver = webdriver.Chrome(options=chrome_options)
driver.get(base_url)
# wait 30 sec
timeout = 30
try:
    WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='feed-item']")))
except TimeoutException:
    print("Timed out waiting for page to load")
    driver.quit()

python_button = driver.find_elements_by_xpath("//a[@class='all']")[0]
python_button.click()



# Add list to append to
Name=[]
Price=[]
NewPrice=[]
OldPrice=[]
Size=[]
Time=[]
LastBump=[]
Link=[]


# I don't want the staff recommendations and other items, just the ones that show up in the search
results = driver.find_elements_by_xpath('//div[@class="FiltersInstantSearch"]//div[@class="feed-item"]')
# just so i can see how many iterations i probably need. Should be 40
len(results)

# Get the number of listings and turn it into a number to find out how many pages I need to scroll
ListingNumber=driver.find_element_by_xpath('//span[@class="designer-profile-stats"]').text
ListingNumber=int(ListingNumber.split(" ")[0].replace(",",""))
ListingNumber

# Number of Scrolls, add one in case the function rounds down
ScrollNumber=round(ListingNumber/40)+1
ScrollNumber

# Number of times i want it to scroll down by (initial 40 is already selected if i run code above)
for i in range(0,ScrollNumber):
    #results = driver.find_elements_by_xpath('//div[@class="feed-item"]')
    #Results=Results+results
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    time.sleep(2)

# Run again to see total number of results the scraper is going to get. It should be 40*ScrollNumber + Initial amount
results = driver.find_elements_by_xpath('//div[@class="FiltersInstantSearch"]//div[@class="feed-item"]')
len(results)


# Start scraping. Notice there's a . in front of //div. It's so that I start searching in each feed-item
# Certain items don't have some of these tags in them, so I have to make a "If-Then" statement
for result in results:

        name = result.find_element_by_xpath('.//div[@class="truncate"]').text
        Name.append(name)

        try:
            price = result.find_element_by_xpath('.//p[@class="sub-title original-price"]').text
            new_price=""
            old_price=""
            Price.append(price)
            NewPrice.append(new_price)
            OldPrice.append(old_price)
        except NoSuchElementException:
            price=""
            new_price = result.find_element_by_xpath('.//p[@class="sub-title new-price"]').text
            old_price = result.find_element_by_xpath('.//p[@class="sub-title original-price strike-through"]').text
            Price.append(price)
            NewPrice.append(new_price)
            OldPrice.append(old_price)

        size = result.find_element_by_xpath('.//p[@class="listing-size sub-title"]').text
        Size.append(size)

        time=result.find_element_by_xpath(".//span[@class='date-ago']").text
        Time.append(time)

        try:
            last_bump=result.find_element_by_xpath(".//span[@class='strike-through']").text
            LastBump.append(last_bump)
        except NoSuchElementException:
            last_bump=""
            LastBump.append(last_bump)

        link = result.find_element_by_xpath('./a').get_attribute("href")
        Link.append(link)

# Turn the lists into a DataFrame with some nice names
ItemDF=pd.DataFrame(zip(Name,Price,NewPrice,OldPrice,Size,Time,LastBump,Link),columns=['Name','Price','NewPrice','OldPrice','Size','Time','LastBump','Link'])
ItemDF

# Turn it into a csv
ItemDF.to_csv('C:/Datasets/Sacai_Sep22.csv')

driver.quit()

### Getting all user information
### make it headless this time or it's going to be very slow going page by page
### base_url doesn't really matter since we are going to get new URLs later
chrome_options = webdriver.ChromeOptions()
# headless:dont open up the chrome
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://www.grailed.com/designers/chrome-hearts")
# timeout after 30 sec
timeout = 30
try:
    WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='feed-item']")))
except TimeoutException:
    print("Timed out waiting for page to load")
    driver.quit()


# Lists to append everything to
UserName=[]
Sold=[]
Feedback=[]
CurrentListings=[]
Description=[]
ProfileLink=[]
FeedBack=[]
FeedbackLink=[]
FollowerCount=[]
FullSize=[]
PostedTime=[]
BumpedTime=[]
Location=[]
PictureNumber=[]
Transactions=[]

# Could just read a csv from before and take the Links from it
JE=pd.read_csv('C:/Datasets/JohnElliott_Sep.11.csv')
# Transform the Link column to a list to loop through
Link=JE.Link.values.tolist()
# See how many to loop through
# Not every single tag is found, so I used try/except for everything just in case
NewLink=Link[0:40]
len(NewLink)


### Start Process
for link in Link:

    driver.get(link)

    try:
        user_name=driver.find_element_by_xpath('//span[@class="-username"]').text
        UserName.append(user_name)
    except NoSuchElementException:
        UserName.append("")

    try:
        sold=driver.find_element_by_xpath('//a[@class="-link"]/span[2]').text
        Sold.append(sold)
    except NoSuchElementException:
        Sold.append("")

    try:
        feedback=driver.find_element_by_xpath('//span[@class="-feedback-count"]').text
        FeedBack.append(feedback)
    except NoSuchElementException:
        FeedBack.append("")

    try:
        currentlistings=driver.find_element_by_xpath('//a[@class="-for-sale-link"]').text
        CurrentListings.append(currentlistings)
    except NoSuchElementException:
        CurrentListings.append(currentlistings)

    try:
        description=driver.find_element_by_xpath('//div[@class="listing-description"]').text
        Description.append(description)
    except NoSuchElementException:
        Description.append(description)

    try:
        profilelink=driver.find_element_by_xpath('//span[@class="Username"]/a').get_attribute("href")
        ProfileLink.append(profilelink)
    except NoSuchElementException:
        ProfileLink.append("")

    try:
        feedbacklink=driver.find_element_by_xpath('//div[@class="-details"]/a').get_attribute("href")
        FeedbackLink.append(feedbacklink)
    except NoSuchElementException:
        FeedbackLink.append("")

    try:
        followercount=driver.find_element_by_xpath('//p[@class="-follower-count"]').text
        FollowerCount.append(followercount)
    except NoSuchElementException:
        FollowerCount.append("")

    try:
        fullsize=driver.find_element_by_xpath('//h2[@class="listing-size sub-title"]').text
        FullSize.append(fullsize)
    except NoSuchElementException:
        FullSize.append("")

    try:
        postedtime=driver.find_element_by_xpath('//div[@class="-metadata"]/span[2]').text
        PostedTime.append(postedtime)
    except NoSuchElementException:
        PostedTime.append("")

    try:
        bumpedtime=driver.find_element_by_xpath('//div[@class="-metadata"]/span[4]').text
        BumpedTime.append(bumpedtime)
    except NoSuchElementException:
        BumpedTime.append("")

    try:
        location=driver.find_element_by_xpath('//label[@class="--label"]').text
        Location.append(location)
    except NoSuchElementException:
        Location.append("")

    count_of_divs = len(driver.find_elements_by_xpath("//div[@class='-image-wrapper -thumbnail']"))
    PictureNumber.append(count_of_divs)


# Turn it into DataFrame
SellerDF=pd.DataFrame(zip(UserName,Sold,FeedBack,CurrentListings,Description,ProfileLink,FeedbackLink,FollowerCount,FullSize,PostedTime,BumpedTime,Location,PictureNumber),
columns=['UserName','Sold','FeedBack','CurrentListings','Description','ProfileLink','FeedbackLink','FollowerCount','FullSize','PostedTime','BumpedTime','Location','PictureNumber'])

SellerDF
SellerDF.tail()

# Export to csv
SellerDF.to_csv('C:/Datasets/JESellers_Sep.17(-884).csv')


##### List of Designers
"https://www.grailed.com/designers/john-elliott"
"https://www.grailed.com/designers/chrome-hearts"
"https://www.grailed.com/designers/momotaro"
"https://www.grailed.com/designers/studio-dartisan"
"https://www.grailed.com/designers/junya-watanabe"
"https://www.grailed.com/designers/rick-owens"
"https://www.grailed.com/designers/visvim"
"https://www.grailed.com/designers/common-projects"
"https://www.grailed.com/designers/arcteryx-veilance"


### Sold
# ChromeHeartsSold
https://www.grailed.com/sold/mEoBfSVrUQ


#########################################################################

### Scraping Sold Page


# Sold Page, filter = grails + john elliott + sweaters&knitwear
base_url = "https://www.grailed.com/sold/hLVZqhMQcg"



# open up chrome. Don't use headless otherwise the feed-item doesn't fully load all the way
chrome_options = webdriver.ChromeOptions()
        # dont open up the chrome
#chrome_options.add_argument('--headless')
driver = webdriver.Chrome(options=chrome_options)
driver.get(base_url)
# wait 30 sec
timeout = 30
try:
    WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='feed-item']")))
except TimeoutException:
    print("Timed out waiting for page to load")
    driver.quit()


# I don't want the staff recommendations and other items, just the ones that show up in the search
results = driver.find_elements_by_xpath('//div[@class="FiltersInstantSearch"]//div[@class="feed-item"]')
# just so i can see how many iterations i probably need. Should be 40
len(results)

# Get the number of listings and turn it into a number to find out how many pages I need to scroll
ListingNumber=driver.find_element_by_xpath('//div[@class="ais-Panel-body"]').text
ListingNumber=int(ListingNumber.split(" ")[0].replace(",",""))
ListingNumber

# Number of Scrolls, add one in case the function rounds down
ScrollNumber=round(ListingNumber/40)+1
ScrollNumber

# Number of times i want it to scroll down by (initial 40 is already selected if i run code above)
for i in range(0,ScrollNumber):
    #results = driver.find_elements_by_xpath('//div[@class="feed-item"]')
    #Results=Results+results
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    time.sleep(2)

# Run again to see total number of results the scraper is going to get. It should be 40*ScrollNumber + Initial amount
results = driver.find_elements_by_xpath('//div[@class="FiltersInstantSearch"]//div[@class="feed-item"]')
len(results)

Name=[]
SoldPrice=[]
#NewPrice=[]
#OldPrice=[]
Size=[]
Time=[]
LastBump=[]
Link=[]


for result in results:

        name = result.find_element_by_xpath('.//div[@class="truncate"]').text
        Name.append(name)


        price = result.find_element_by_xpath('.//p[@class="sub-title sold-price"]').text
        new_price=""
        old_price=""
        SoldPrice.append(price)
        #except NoSuchElementException:
            #price=""
            #new_price = result.find_element_by_xpath('.//p[@class="sub-title new-price"]').text
            #old_price = result.find_element_by_xpath('.//p[@class="sub-title original-price strike-through"]').text
            #Price.append(price)
            #NewPrice.append(new_price)
            #OldPrice.append(old_price)

        size = result.find_element_by_xpath('.//p[@class="listing-size sub-title"]').text
        Size.append(size)

        time=result.find_element_by_xpath(".//span[@class='date-ago']").text
        Time.append(time)

        try:
            last_bump=result.find_element_by_xpath(".//span[@class='strike-through']").text
            LastBump.append(last_bump)
        except NoSuchElementException:
            last_bump=""
            LastBump.append(last_bump)

        link = result.find_element_by_xpath('./a').get_attribute("href")
        Link.append(link)

# Turn the lists into a DataFrame with some nice names
SoldDF=pd.DataFrame(zip(Name,SoldPrice,Size,Time,LastBump,Link),columns=['Name','SoldPrice','Size','Time','LastBump','Link'])
SoldDF

SoldDF.to_csv('C:/Datasets/JE_Jeans_Sold.csv')




############################################################

### Sold Item Page

CH=pd.read_csv('C:/Datasets/JE_Jeans_Sold.csv')
Link=CH.Link

chrome_options = webdriver.ChromeOptions()
# headless:dont open up the chrome
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://www.grailed.com/designers/chrome-hearts")
# timeout after 30 sec
timeout = 30
try:
    WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='feed-item']")))
except TimeoutException:
    print("Timed out waiting for page to load")
    driver.quit()

driver.quit()

# Lists to append everything to
UserName=[]
ItemsSold=[]
FullPrice=[]
Feedback=[]
CurrentListings=[]
Description=[]
ProfileLink=[]
FeedBack=[]
FeedbackLink=[]
FollowerCount=[]
FullSize=[]
PostedTime=[]
BumpedTime=[]
Location=[]
PictureNumber=[]
Transactions=[]

### Start Process
for link in Link:

    driver.get(link)

    try:
        user_name=driver.find_element_by_xpath('//span[@class="-username"]').text
        UserName.append(user_name)
    except NoSuchElementException:
        UserName.append("")

    try:
        price_drop=driver.find_element_by_xpath('//h3[@class="-price _drop"]').text
        FullPrice.append(price_drop)
    except NoSuchElementException:
        FullPrice.append("")

    try:
        itemssold=driver.find_element_by_xpath('//a[@class="-link"]/span[2]').text
        ItemsSold.append(itemssold)
    except NoSuchElementException:
        ItemsSold.append("")

    try:
        feedback=driver.find_element_by_xpath('//span[@class="-feedback-count"]').text
        FeedBack.append(feedback)
    except NoSuchElementException:
        FeedBack.append("")

    try:
        currentlistings=driver.find_element_by_xpath('//a[@class="-for-sale-link"]').text
        CurrentListings.append(currentlistings)
    except NoSuchElementException:
        CurrentListings.append(currentlistings)

    try:
        description=driver.find_element_by_xpath('//div[@class="listing-description"]').text
        Description.append(description)
    except NoSuchElementException:
        Description.append(description)

    try:
        profilelink=driver.find_element_by_xpath('//span[@class="Username"]/a').get_attribute("href")
        ProfileLink.append(profilelink)
    except NoSuchElementException:
        ProfileLink.append("")

    try:
        feedbacklink=driver.find_element_by_xpath('//div[@class="-details"]/a').get_attribute("href")
        FeedbackLink.append(feedbacklink)
    except NoSuchElementException:
        FeedbackLink.append("")

    try:
        followercount=driver.find_element_by_xpath('//p[@class="-follower-count"]').text
        FollowerCount.append(followercount)
    except NoSuchElementException:
        FollowerCount.append("")

    try:
        fullsize=driver.find_element_by_xpath('//h2[@class="listing-size sub-title"]').text
        FullSize.append(fullsize)
    except NoSuchElementException:
        FullSize.append("")

    try:
        postedtime=driver.find_element_by_xpath('//div[@class="-metadata"]/span[2]').text
        PostedTime.append(postedtime)
    except NoSuchElementException:
        PostedTime.append("")

    try:
        bumpedtime=driver.find_element_by_xpath('//div[@class="-metadata"]/span[4]').text
        BumpedTime.append(bumpedtime)
    except NoSuchElementException:
        BumpedTime.append("")


    count_of_divs = len(driver.find_elements_by_xpath("//div[@class='-image-wrapper -thumbnail']"))
    PictureNumber.append(count_of_divs)

# Turn it into DataFrames
SellerDF=pd.DataFrame(zip(UserName,ItemsSold,FollowerCount,FullPrice,FeedBack,CurrentListings,Description,FullSize,PostedTime,BumpedTime,PictureNumber,ProfileLink,FeedbackLink),
columns=['UserName','ItemsSold','FollowerCount','FullPrice','FeedBack','CurrentListings','Description','FullSize','PostedTime','BumpedTime','NumberOfPictures','ProfileLink','FeedbackLink'])

SellerDF

SellerDF.to_csv('C:/Datasets/JE_Jeans_Seller(new).csv')

# Merge with SoldDF
SellerDF = pd.read_csv("C:/Datasets/CH_Jewellery_Seller(new).csv",index_col=[0])
SellerDF
SoldDF = pd.read_csv("C:/Datasets/CH_Jewellery_Sold.csv",index_col=[0])
SoldDF

TotalDF=SoldDF.join(SellerDF)
TotalDF.to_csv("C:/Datasets/CH_Jewellery_Total.csv")
TotalDF



################################################### Scrapy Test
### Links
#https://medium.com/@arunshaji95/web-scraping-using-scrapy-b4c91716cca1
#https://towardsdatascience.com/web-scraping-a-simple-way-to-start-scrapy-and-selenium-part-i-10367164c6c0









################################ Data Cleaning

import pandas as pd
import numpy as np

TotalDF=pd.read_csv("C:/Datasets/JE_Jeans_Total.csv",index_col=[0])
TotalDF
### Cleaning

# Remove dollar sign from SoldPrice
TotalDF['SoldPrice'] = TotalDF['SoldPrice'].str.replace('$', '')

# Remove 'days ago' from Time
TotalDF['Time'] = TotalDF['Time'].str.replace('ago', '')

# remove brackets from LastBump
TotalDF['LastBump'] = TotalDF['LastBump'].str.replace('(', '')
TotalDF['LastBump'] = TotalDF['LastBump'].str.replace(')', '')


# remove brackets from FollowerCount & ItemsSold
TotalDF['FollowerCount'] = TotalDF['FollowerCount'].astype(str).str.replace(')', '')
TotalDF['FollowerCount'] = TotalDF['FollowerCount'].astype(str).str.replace('(', '')

# not that useful
TotalDF['ItemsSold'] = TotalDF['ItemsSold'].astype(str).str.replace('(', '')
TotalDF['ItemsSold'] = TotalDF['ItemsSold'].astype(str).str.replace(')', '')

### not sure what this is anymore
# remove - from Sold
#TotalDF['Sold'] = TotalDF['Sold'].astype(str).str.replace('-', '')
#TotalDF.Sold = pd.to_numeric(TotalDF['Sold'],errors='coerce')

# remove 'feedback' from Feedback
TotalDF['FeedBack'] = TotalDF['FeedBack'].astype(str).str.replace('Feedback', '')

TotalDF['CurrentListings'] = TotalDF['CurrentListings'].astype(str).str.replace(' Listings for Sale', '')
# Some don't have an s at the end of Listing
TotalDF['CurrentListings'] = TotalDF['CurrentListings'].astype(str).str.replace(' Listing for Sale', '')


# trying to format the columns
#cols = TotalDF.columns.tolist()
#cols
#n = int(cols.index('Link'))
#n
#cols = cols[:n] + cols[n+1:] + [cols[n]]
#TotalDF= TotalDF[cols]


# Extract days/months/years from column
# order is pretty important here. If I put day first, it actually extracts day from days and leaves an s
TotalDF['Period'] = TotalDF.Time.str.extract('(days|months|month|year|years|hours|day)')
TotalDF['Period']

TotalDF['LastBumpPeriod'] = TotalDF.LastBump.str.extract('(days|months|month|year|years|hours|day)')

# remove these words. Any almost/about/over i'll assume its exactly that time to be simple
TotalDF['Time'] = TotalDF['Time'].astype(str).str.replace('days|months|years|almost|about|over|month|year|hours|day', '')
TotalDF['LastBump'] = TotalDF['LastBump'].astype(str).str.replace('days|months|years|almost|about|over|month|year|hours|day|', '')
TotalDF
# remove white space
TotalDF.Time.str.strip()
TotalDF.LastBump.str.strip()

# make sure there are no more words
TotalDF.Time.unique()
TotalDF.LastBump.unique()

# remove the links cuz not that important for this analysis.
TotalDF = TotalDF.drop(['ProfileLink','FeedbackLink','Link'],axis=1)

# create length of description column
TotalDF['LengthOfCaptions'] = TotalDF.Description.str.len()

TotalDF.Time = pd.to_numeric(TotalDF.Time)
TotalDF


# Transform Time to integers.
TotalDF.Time = np.where(TotalDF.Period =='hours',1,1)
TotalDF.Time *= np.where(TotalDF.Period =='days',1,1)
TotalDF.Time *= np.where(TotalDF.Period =='month',30,1)
TotalDF.Time *= np.where(TotalDF.Period =='months',30,1)
TotalDF.Time *= np.where(TotalDF.Period =='years',360,1)
TotalDF.Time *= np.where(TotalDF.Period =='year',360,1)

TotalDF.LastBump = pd.to_numeric(TotalDF.LastBump,errors='coerce')
TotalDF.LastBump.fillna(0,inplace=True)
TotalDF

 # Transform LastBump to integers.
 TotalDF.LastBump *= np.where(TotalDF.LastBumpPeriod =='days',1,1)
 TotalDF.LastBump *= np.where(TotalDF.LastBumpPeriod =='months',30,1)
 TotalDF.LastBump *= np.where(TotalDF.LastBumpPeriod =='month',30,1)
 TotalDF.LastBump *= np.where(TotalDF.LastBumpPeriod =='years',360,1)
 TotalDF.LastBump *= np.where(TotalDF.LastBumpPeriod =='year',360,1)

# find difference between posted Time and Last Bumped Time
# negative values mean that there wasn't a LastBump time
TotalDF['TimeDifference'] = TotalDF.LastBump - TotalDF.Time
TotalDF.TimeDifference

# 141 negative observations.
(TotalDF.TimeDifference < 0).sum()/TotalDF.TimeDifference.count()
