//
//  DetailViewController.h
//  weather
//
//  Created by Archer on 3/24/11.
//  Copyright 2011 __MyCompanyName__. All rights reserved.
//

#import <UIKit/UIKit.h>
#import "ASIHTTPRequest.h"

@interface DetailViewController : UITableViewController <ASIHTTPRequestDelegate> {
	NSString *cityName;
	NSString *weekDay;
	NSDictionary *cityWeather;//用來顯示城市當日的天氣
	NSArray *weekWeather;//用來顯示城市一周的天氣

}

- (id)initWithCityName:(NSString *)aCityName;

@end
