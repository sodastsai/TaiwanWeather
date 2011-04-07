//
//  RootViewController.h
//  weather
//
//  Created by Archer on 3/24/11.
//  Copyright 2011 __MyCompanyName__. All rights reserved.
//

#import <UIKit/UIKit.h>
#import "DetailViewController.h"
#import "ASIHTTPRequest.h"

@interface RootViewController : UITableViewController <ASIHTTPRequestDelegate> {
	NSArray *names;
}

@end
