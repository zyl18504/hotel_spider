# -*- coding: utf-8 -*-
import scrapy


class TanglaSpider(scrapy.Spider):
    name = "tangla"

    hotel_code_dict = {
            'TLBJ':u'北京唐拉雅秀酒店',
            'TLTJ':u'天津中心唐拉雅秀酒店',
            'CCMM':u'长春海航名门酒店',
            'CCZJH':u'长春紫荆花海航大酒店',
            'CBSBG':u'海航长白山宾馆',
            'DZXTD':u'儋州新天地海航大酒店',
            'HZHG':u'杭州花港海航度假酒店',
            'XAHC':u'西安皇城海航商务酒店',
            'SYYT':u'海南三亚亚太国际会议中心',
            #'SYFH',
            'THWX':u'无锡嘉昱珺唐酒店',
    }

    hotel_code_list = [
        'TLBJ',
        'TLTJ',
        'CCMM',
        'CCZJH',
        'CBSBG',
        'DZXTD',
        'HZHG',
        'XAHC',
        'SYYT',
        'THWX',
    ]
        
    def start_requests(self):
        init_url = 'https://www.tanglarewards.com/HotelBook/Room'
        headers = {
            'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4',
            "Content-Type":"application/x-www-form-urlencoded",
            #"Host":"www.tanglarewards.com",
            "Origin":"https://www.tanglarewards.com",
            "Referer":"https://www.tanglarewards.com/HotelBook",
            "Upgrade-Insecure-Requests":1,
            "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36",
        }
        start_date = '2017-02-27'
        end_date = '2017-01-28'
        cookies={
                '__RequestVerificationToken':'ZS8wlTl79HhL5P-B_eKxxDSkolsYXyqxbftp7lRAY30p-1A0fFShSyX2_twk0ykZzFK4-Paqq4JKxKyLTyFEVZlZkuKdjARwyqRtJpSqvJjiFhIU_gdhrv11GT7UVksgWRbsm_6L36izv8rPXzBc_w2',
                'ASP.NET_SessionId':'jdt0qfx0rkqi4hygaujpzzon',
                'Hm_lvt_cd522d7bd80776ff6f438a86d0b303e7':'1485580336',
                'Hm_lpvt_cd522d7bd80776ff6f438a86d0b303e7':'1486559197',
                }
            
        for hotel_code in self.hotel_code_list:
            yield scrapy.FormRequest(init_url,formdata={'HotelCode':hotel_code},headers=headers,cookies=cookies,meta={'dont_redirect':True,'handle_httpstatus_list':[302]},callback=self.parse_room)



    def parse_room(self,response):
        hotel_code = response.request.body.split('=')[-1]
        print 'hotel_code',hotel_code
        hotel_name = self.hotel_code_dict.get(hotel_code,'')
        hotel_room_info = []
        for room_div in response.css('div.hotel_contentview_contentfind'):
            room_name = room_div.css('div.hotel_contentview_contentfindwhichwrite a::text').extract_first().strip()
            room_desc = room_div.css('div.hotel_contentview_contentfindwhichwrite2::text').extract_first().strip()
            min_price = room_div.css('div.hotel_contentview_confincost2::attr(data-minprice)').extract_first().strip()
            #min_price = int(min_price) if min_price.isdigit() else 0
            hotel_room_info.append((room_name,room_desc,min_price))

        with open('./room_result','ab') as f:
            f.write('%s(%s)' % (hotel_name.encode('utf8'),hotel_code))
            f.write('\n')
            if hotel_room_info:
                for room_info in hotel_room_info:
                    f.write('\t')
                    f.write('房型:%s' % room_info[0].encode('utf8'))
                    f.write('\n\t')
                    f.write('房型信息:%s' % room_info[1].encode('utf8'))
                    f.write('\n\t')
                    f.write('起订价:%s' % room_info[-1].encode('utf8'))
                    f.write('\n')
            else:
                f.write('\t未查到预订信息')
            f.write('\n')
