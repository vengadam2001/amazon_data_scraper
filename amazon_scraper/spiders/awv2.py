import scrapy
import selenium
from    shutil                             import which
from    scrapy.selector                    import Selector 
from    selenium                           import webdriver
from    selenium.webdriver.chrome.options  import Options


purify = lambda x:x.replace('\n','').replace(' ','')

def rmc(x, split= -1, sep=' ',rep=' ## ' , arr =-1 ):  # rmc is for remove comma
    if x == None:
        return None
    else :
        if split >=0:
            return x.split(sep)[split].replace(',',rep) 
        elif arr>=0:
            if x == []:
                return None
            else :
                if len(x) >0:
                    if len(x) > arr:
                        return x[arr]
                    else:
                        return x[len(x)-1]
                else :
                    return None
        else :
            return x.replace(',',rep).replace('/n','')
class AmazonSpider(scrapy.Spider):
    name = 'aw2'
    allowed_domains = ["amazon.in"]
    start_urls = ['https://www.amazon.in/s?rh=n%3A1375424031&fs=true&ref=lp_1375424031_sar']
    def parse(self, response):    
        chrome_options = Options()
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1920,1080")
        chromepath=which("ch")
        driver = webdriver.Chrome(executable_path=chromepath,options=chrome_options)
        link = response.request.url
        driver.get(link)
        res=driver.page_source            
        res=Selector(text=res)
        lists= response.xpath('//div[@class="a-section a-spacing-medium"]/div/div/h2/a/@href').getall()
        for i in lists:
            yield scrapy.Request(
                            url=response.urljoin(i),
                            callback=self.parse_two,

                        )           
        # if "c_d" not in response.request.meta :    #  to scrap beyond the first page  
        #     yield scrapy.Request(
        #                     url=response.urljoin(response.xpath('//li[@class="a-last"]/a/@href').get() ),
        #                     callback=self.parse,
        #                     meta={"c_d": 1}
        #                 )
        # else :
        #     if response.request.meta["c_d"] < 10:
        #         yield scrapy.Request(
        #                         url=response.urljoin(response.xpath('//li[@class="a-last"]/a/@href').get() ),
        #                         callback=self.parse,
        #                         meta={ "c_d": response.request.meta["c_d"]+1 }
        #                     )
        #         print(response.request.meta["c_d"])


    def parse_two(self, response):
        
        if rmc (response.xpath('//span[@id="productTitle"]/text()').get() ) == None:
            name        = rmc (response.xpath("//span[contains(@id,'Title') ]") )
        no_of_rating    = rmc (response.xpath('//span[contains (@id,"CustomerReviewText")]/text()').get())
        total_no_answer = rmc (response.xpath('//a[@id="askATFLink"]/span[@class="a-size-base"]/text()').get())
        mrp             = rmc (response.xpath('//span[@class="priceBlockStrikePriceString a-text-strike"]/text()').get())
        price           = rmc (response.xpath('//span[@id="priceblock_ourprice"]/text()').get() )
        if price == None :
            price = rmc(response.xpath("//span[contains( @class , 'a-color-price'  )]"))
        
        save            = rmc (response.xpath('//td[@class="a-span12 a-color-price a-size-base priceBlockSavingsString"]/text()').get() )
        delivery_date   = rmc (response.xpath('//b/text()').getall() ,arr=2 )
        delivery_type   = rmc (response.xpath('//a[@target="AmazonHelp"]/text()').get() )
        emi             = "EMI" in [ *response.xpath('//div[@id="inemi_feature_div"]/span/b/text()').getall() , *response.xpath('//div[@id="inemi_feature_div"]/span/text()').getall() ]
        order_within    = rmc (response.xpath('//span[@class="ftCountdownClass"]/text()').get() )        
        exchange        = not(response.xpath('//div[@class="a-section a-spacing-none a-padding-none"]/span/span[@class="a-text-bold"]/text()').get() == None)
        link            =  response.xpath('//a[@data-hook="see-all-reviews-link-foot"]/@href').get()        
        about           = ''
        for i in response.xpath('//ul[@class ="a-unordered-list a-vertical a-spacing-mini"]/li/span/text()').getall():
            about += i
        temp1 = response.xpath('//table[@id="productDetails_techSpec_section_1"]/tr/th/text()').getall()
        temp2 = response.xpath('//table[@id="productDetails_techSpec_section_1"]/tr/td/text()').getall()
        more_detail    = ''
        for i,j in zip(temp1,temp2):
            more_detail+=i+'#'+j+'\n'
        about           = rmc (about.replace("\n\n\n",' # ').replace("\n",'#') )
        temp1=None  
        if len(response.xpath('//table[@id="histogramTable"]/tr/td[3]/span/a/text()').getall() ) >4:
            temp1 = response.xpath('//table[@id="histogramTable"]/tr/td[3]/span/a/text()').getall()
        for i in range(0,3):
            if len(response.xpath('//table[@id="histogramTable"]['+str(i)+']/tbody/tr/td[3]/span/a/text()').getall() ) >4 and not (temp1==None) :
                temp1 = response.xpath('//table[@id="histogramTable"]['+str(i)+']/tbody/tr/td[3]/span/a/text()').getall()
                break
        
        if not temp1 == None:
            five_star, four_star , three_star , two_star , one_star = temp1
            five_star       = purify(five_star)
            four_star       = purify(four_star)
            three_star      = purify(three_star)
            two_star        = purify(two_star)
            one_star        = purify (one_star)
        else:
            five_star, four_star , three_star , two_star , one_star = [None,None,None,None,None]

        if not(response.xpath('//tr[@class="a-spacing-small"]/td[2]/span/text()').getall() == [] ) and  len(response.xpath('//tr[@class="a-spacing-small"]/td[2]/span/text()').getall()) >4 :
            Model,Brand,SpecificUses,ScreenSize,OS = response.xpath('//tr[@class="a-spacing-small"]/td[2]/span/text()').getall()[:5]
        else :
            Model,Brand,SpecificUses,ScreenSize,OS = [None,None,None,None,None]
        
        avg_rating      = ''
        reviews         =''
        if not (link == None):
            link = response.urljoin(link + "&sortBy=recent&pageNumber=1") 
        avg_rating = ''
        if  None ==  response.xpath('//i[contains(@class,"a-icon a-icon-star")]/span[@class="a-icon-alt"]/text()').get():
            avg_rating = None
        else:
            avg_rating = response.xpath('//i[contains(@class,"a-icon a-icon-star")]/span[@class="a-icon-alt"]/text()').get().split(' ')[0]

        condition =not(name == None or name == '')
        if  condition :
            yield {
                    "name":name                     , 
                    "mrp":mrp                           , 
                    "save":save                        , 
                    "price":price                       , 
                    "about":about                       , 
                    "no_of_rating":no_of_rating         , 
                    "avg_rating":avg_rating            , 
                    "total_no_answer":total_no_answer   ,  
                    "delivery_type":delivery_type       , 
                    "delivery_date":delivery_date       , 
                    "Model":Model	                   , 
                    "Brand":Brand	                   , 
                    "SpecificUses":SpecificUses         , 
                    "ScreenSize":ScreenSize             , 
                    "OS":OS                             , 
                    "more_detail":more_detail           , 
                    "order_within":order_within         , 
                    "emi":emi                           , 
                    "exchange":exchange                 , 
                    "five_star":five_star               ,
                    "four_star":four_star               , 
                    "three_star":three_star             , 
                    "two_star":two_star                 , 
                    "one_star":one_star                 ,
                    "reviews":reviews
                    }