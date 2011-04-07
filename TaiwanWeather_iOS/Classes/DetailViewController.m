//
//  DetailViewController.m
//  weather
//
//  Created by Archer on 3/24/11.
//  Copyright 2011 __MyCompanyName__. All rights reserved.
//

#import "DetailViewController.h"


@implementation DetailViewController

#pragma mark -
#pragma mark initWithCityName

- (id)initWithCityName:(NSString *)aCityName{
	if (self = [super initWithStyle:UITableViewStyleGrouped] ) {
		cityName=[aCityName retain];
		 
		NSURL *jsonURL = [NSURL URLWithString:[NSString stringWithFormat:@"http://ntu-taiwan-weather.appspot.com/json/current/%@/",cityName]];
		ASIHTTPRequest *request = [ASIHTTPRequest requestWithURL:jsonURL];
		request.delegate = self;
		request.username = @"request";
		[request startAsynchronous];
		
		//json week day
		NSURL *weekURL = [NSURL URLWithString:[NSString stringWithFormat:@"http://ntu-taiwan-weather.appspot.com/json/forecast/%@/",cityName]];
		ASIHTTPRequest *weekRequest = [ASIHTTPRequest requestWithURL:weekURL];
		weekRequest.delegate = self;
		weekRequest.username = @"weekRequest";
		[weekRequest startAsynchronous];
		
//		NSLog(@"ditail's city is>> %@",cityName);
	}
	return self;
}


#pragma mark -
#pragma mark requestFinished

- (void)requestFinished:(ASIHTTPRequest *)request{
	if (request.username==@"request") {
		NSLog(@"%@",request.username);
		NSString *jsonString = [request responseString];
		cityWeather = [[jsonString objectFromJSONString] retain];
		[self.tableView reloadData];
		
	}else if (request.username==@"weekRequest") {
		NSLog(@"%@",request.username);
		NSString *weekJsonString = [request responseString];
		NSDictionary *cityForecast = [[weekJsonString objectFromJSONString] retain];
		weekWeather = [cityForecast objectForKey:@"week"];
		NSLog(@"%@",[[weekWeather objectAtIndex:0] objectForKey:@"temperature"]);
		[self.tableView reloadData];
	}
}

#pragma mark -
#pragma mark View lifecycle

/*
- (void)viewDidLoad {
    [super viewDidLoad];

    // Uncomment the following line to display an Edit button in the navigation bar for this view controller.
    // self.navigationItem.rightBarButtonItem = self.editButtonItem;
}
*/

/*
- (void)viewWillAppear:(BOOL)animated {
    [super viewWillAppear:animated];
}
*/
/*
- (void)viewDidAppear:(BOOL)animated {
    [super viewDidAppear:animated];
}
*/
/*
- (void)viewWillDisappear:(BOOL)animated {
    [super viewWillDisappear:animated];
}
*/
/*
- (void)viewDidDisappear:(BOOL)animated {
    [super viewDidDisappear:animated];
}
*/

// Override to allow orientations other than the default portrait orientation.
//- (BOOL)shouldAutorotateToInterfaceOrientation:(UIInterfaceOrientation)interfaceOrientation {
//    // Return YES for supported orientations.
//    return YES;
//}



#pragma mark -
#pragma mark Table view data source

- (NSInteger)numberOfSectionsInTableView:(UITableView *)tableView {
    // Return the number of sections.
    return 2;
}


- (NSInteger)tableView:(UITableView *)tableView numberOfRowsInSection:(NSInteger)section {
    // Return the number of rows in the section.
	if (section==0) {
		return 1;
	}else if (section==1) {
		return 7;
	}
    return -1;
}

- (CGFloat)tableView:(UITableView *)tableView heightForRowAtIndexPath:(NSIndexPath *)indexPath {
	if (indexPath.section==0) {
		return 132;
	}
	return 44;
}

// Customize the appearance of table view cells.
- (UITableViewCell *)tableView:(UITableView *)tableView cellForRowAtIndexPath:(NSIndexPath *)indexPath {
    
	NSDate *nowDate = [NSDate date];
	NSCalendar *cal = [NSCalendar currentCalendar];
	NSDateComponents *cmp = [cal components:NSWeekdayCalendarUnit
								   fromDate:nowDate];
	
	if (indexPath.section==0) {
		//today cell 會用到view
		UIImageView *todayImgView;
		UILabel *todayLabel_line1;
		UILabel *todayLabel_line2;
		UILabel *todayLabel_line3;
		
		static NSString *CellIdentifier1 = @"todayCell";
		
		
		UITableViewCell *todayCell = [tableView dequeueReusableCellWithIdentifier:CellIdentifier1];
		if (todayCell == nil) {
			todayCell = [[[UITableViewCell alloc] initWithStyle:UITableViewCellStyleDefault reuseIdentifier:CellIdentifier1] autorelease];
			todayCell.selectionStyle = UITableViewCellSelectionStyleNone;
			
			todayImgView = [[UIImageView alloc] initWithFrame:CGRectMake(10, 15, 100, 100)];
			todayImgView.tag = 1;
			//todayImgView.autoresizingMask = UIViewAutoresizingFlexibleLeftMargin | UIViewAutoresizingFlexibleHeight;
			[todayCell.contentView addSubview:todayImgView];
			
			todayLabel_line1 = [[UILabel alloc] initWithFrame:CGRectMake(120, 5, 100, 50)];
			todayLabel_line1.tag = 2;
			todayLabel_line1.font = [UIFont fontWithName:@"Helvetica-Bold" size:20];
			todayLabel_line1.textAlignment = UITextAlignmentLeft;
			todayLabel_line1.textColor = [UIColor blackColor];
			//todayLabel_line1.autoresizingMask = UIViewAutoresizingFlexibleLeftMargin | UIViewAutoresizingFlexibleHeight;
			[todayCell.contentView addSubview:todayLabel_line1];
			
			todayLabel_line2 = [[UILabel alloc] initWithFrame:CGRectMake(120, 47, 150, 40)];
			todayLabel_line2.tag = 3;
			todayLabel_line2.font = [UIFont fontWithName:@"Helvetica-Bold" size:17];
			todayLabel_line2.textAlignment = UITextAlignmentLeft;
			todayLabel_line2.textColor = [UIColor blackColor];
			//todayLabel_line2.autoresizingMask = UIViewAutoresizingFlexibleLeftMargin | UIViewAutoresizingFlexibleHeight;
			[todayCell.contentView addSubview:todayLabel_line2];
			
			todayLabel_line3 = [[UILabel alloc] initWithFrame:CGRectMake(120, 82, 120, 40)];
			todayLabel_line3.tag = 4;
			todayLabel_line3.font = [UIFont fontWithName:@"Helvetica-Bold" size:17];
			todayLabel_line3.textAlignment = UITextAlignmentLeft;
			todayLabel_line3.textColor = [UIColor blackColor];
			//todayLabel_line3.autoresizingMask = UIViewAutoresizingFlexibleLeftMargin | UIViewAutoresizingFlexibleHeight;
			[todayCell.contentView addSubview:todayLabel_line3];
			
		}else {
			todayImgView = (UIImageView *)[todayCell.contentView viewWithTag:1];
			todayLabel_line1 = (UILabel *)[todayCell.contentView viewWithTag:2];
			todayLabel_line2 = (UILabel *)[todayCell.contentView viewWithTag:3];
			todayLabel_line3 = (UILabel *)[todayCell.contentView viewWithTag:4];
		}

		
		
			NSURL *imgURL = [NSURL URLWithString:[cityWeather objectForKey:@"image"]];
			ASIHTTPRequest *img_request = [ASIHTTPRequest requestWithURL:imgURL];
			[img_request startSynchronous];
			UIImage *img = [UIImage imageWithData:[img_request responseData]];
			todayImgView.image=img;
			todayLabel_line1.text = [cityWeather objectForKey:@"city"];
			todayLabel_line2.text = [NSString stringWithFormat:@"天氣概況： %@",[cityWeather objectForKey:@"description"]];
			todayLabel_line3.text = [NSString stringWithFormat:@"溫度： %@ °C",[cityWeather objectForKey:@"temperature"]];
		
		return todayCell;
	}else if (indexPath.section==1) {
			static NSString *CellIdentifier = @"weekDayCell";
			//week cell要用到的view
		
			UILabel *weekDayLabel;
			UIImageView *weekDayImgView;
			UILabel *weekDaydescriptionLabel;
			UILabel *weekDayTemperatureLabel;
		
			UITableViewCell *cell = [tableView dequeueReusableCellWithIdentifier:CellIdentifier];//先看有沒有同種類的cell可以用
		
			if (cell==nil) {//若沒有就開始做一個新的同種類的cell
				cell = [[[UITableViewCell alloc] initWithStyle:UITableViewCellStyleDefault reuseIdentifier:CellIdentifier] autorelease];
				cell.selectionStyle = UITableViewCellSelectionStyleNone;
			 
				weekDayLabel = [[UILabel alloc] initWithFrame:CGRectMake(28, 0, 30, 44)];
				weekDayLabel.tag = 1;
				weekDayLabel.font =[UIFont  fontWithName:@"Helvetica-Bold"  size:17];
				weekDayLabel.textAlignment = UITextAlignmentLeft;
				weekDayLabel.textColor = [UIColor blackColor];
				weekDayLabel.autoresizingMask = UIViewAutoresizingFlexibleLeftMargin | UIViewAutoresizingFlexibleHeight;
				[cell.contentView addSubview:weekDayLabel];
			
				weekDayImgView = [[UIImageView alloc] initWithFrame:CGRectMake(53, 8, 32, 27)];
				weekDayImgView.tag=2;
				weekDayImgView.autoresizingMask = UIViewAutoresizingFlexibleLeftMargin | UIViewAutoresizingFlexibleHeight;
				[cell.contentView addSubview:weekDayImgView];
			
				weekDaydescriptionLabel = [[UILabel alloc] initWithFrame:CGRectMake(95, 0, 130, 44)];
				weekDaydescriptionLabel.tag = 3;
				weekDaydescriptionLabel.font =[UIFont  fontWithName:@"Helvetica-Bold"  size:17];
				weekDaydescriptionLabel.textAlignment = UITextAlignmentLeft;
				weekDaydescriptionLabel.textColor = [UIColor blackColor];
				weekDaydescriptionLabel.autoresizingMask = UIViewAutoresizingFlexibleLeftMargin | UIViewAutoresizingFlexibleHeight;
				[cell.contentView addSubview:weekDaydescriptionLabel];
			
				weekDayTemperatureLabel = [[UILabel alloc] initWithFrame:CGRectMake(215, 0, 95, 44)];
				weekDayTemperatureLabel.tag = 4;
				weekDayTemperatureLabel.font =[UIFont  fontWithName:@"Helvetica-Bold"  size:17];
				weekDayTemperatureLabel.textAlignment = UITextAlignmentRight;
				weekDayTemperatureLabel.textColor = [UIColor blackColor];
				weekDayTemperatureLabel.autoresizingMask = UIViewAutoresizingFlexibleLeftMargin | UIViewAutoresizingFlexibleHeight;
				[cell.contentView addSubview:weekDayTemperatureLabel];
			}else {
				weekDayLabel = (UILabel *)[cell.contentView viewWithTag:1];
				weekDayImgView = (UIImageView *)[cell.contentView viewWithTag:2];
				weekDaydescriptionLabel = (UILabel *)[cell.contentView viewWithTag:3];
				weekDayTemperatureLabel = (UILabel *)[cell.contentView viewWithTag:4];
			}
			NSLog(@"%d",(([cmp weekday]+indexPath.row) % 7));
		
			int weekDayNumber = (([cmp weekday]+indexPath.row) % 7);
			switch (weekDayNumber) {
				case 0:
					weekDay = [NSString stringWithFormat:@"六"];  
					break;
				case 1:
					weekDay = [NSString stringWithFormat:@"日"];
					break;
				case 2:
					weekDay = [NSString stringWithFormat:@"一"];
					break;
				case 3:
					weekDay = [NSString stringWithFormat:@"二"];
					break;
				case 4:
					weekDay = [NSString stringWithFormat:@"三"];
					break;
				case 5:
					weekDay = [NSString stringWithFormat:@"四"];
					break;
				case 6:
					weekDay = [NSString stringWithFormat:@"五"];
					break;
				default:
					break;
			}
			NSURL *weekImgURL = [NSURL URLWithString:[[weekWeather objectAtIndex:indexPath.row] objectForKey:@"image"]];
			ASIHTTPRequest *weekImg_request = [ASIHTTPRequest requestWithURL:weekImgURL];
			[weekImg_request startSynchronous];
			UIImage *weekImg = [UIImage imageWithData:[weekImg_request responseData]];
			weekDayImgView.image=weekImg;
			weekDayLabel.text = [NSString stringWithFormat:@"%@",weekDay];
			weekDaydescriptionLabel.text = [NSString stringWithFormat:@"%@",[[weekWeather objectAtIndex:indexPath.row] objectForKey:@"description"]];
			weekDayTemperatureLabel.text = [NSString stringWithFormat:@"%@ °C",[[weekWeather objectAtIndex:indexPath.row] objectForKey:@"temperature"]];
							
							   		
			return cell;
		}

    // Configure the cell...

	//else if (indexPath.section==1) {
//		
//		NSLog(@"%d",(([cmp weekday]+indexPath.row) % 7));
//		
//		int weekDayNumber = (([cmp weekday]+indexPath.row) % 7);
//		switch (weekDayNumber) {
//			case 0:
//				weekDay = [NSString stringWithFormat:@"六"];  
//				break;
//			case 1:
//				weekDay = [NSString stringWithFormat:@"日"];
//				break;
//			case 2:
//				weekDay = [NSString stringWithFormat:@"一"];
//				break;
//			case 3:
//				weekDay = [NSString stringWithFormat:@"二"];
//				break;
//			case 4:
//				weekDay = [NSString stringWithFormat:@"三"];
//				break;
//			case 5:
//				weekDay = [NSString stringWithFormat:@"四"];
//				break;
//			case 6:
//				weekDay = [NSString stringWithFormat:@"五"];
//				break;
//			default:
//				break;
//		}
//		NSURL *weekImgURL = [NSURL URLWithString:[[weekWeather objectAtIndex:indexPath.row] objectForKey:@"image"]];
//		ASIHTTPRequest *weekImg_request = [ASIHTTPRequest requestWithURL:weekImgURL];
//		[weekImg_request startSynchronous];
//		UIImage *weekImg = [UIImage imageWithData:[weekImg_request responseData]];
//		cell.imageView.image=weekImg;
//		cell.textLabel.text = [NSString stringWithFormat:@"%@ %@ %@ °C"
//							   ,weekDay
//							   ,[[weekWeather objectAtIndex:indexPath.row] objectForKey:@"description"]
//							   ,[[weekWeather objectAtIndex:indexPath.row] objectForKey:@"temperature"]];
//		
//	}
    
    return nil;
}


/*
// Override to support conditional editing of the table view.
- (BOOL)tableView:(UITableView *)tableView canEditRowAtIndexPath:(NSIndexPath *)indexPath {
    // Return NO if you do not want the specified item to be editable.
    return YES;
}
*/


/*
// Override to support editing the table view.
- (void)tableView:(UITableView *)tableView commitEditingStyle:(UITableViewCellEditingStyle)editingStyle forRowAtIndexPath:(NSIndexPath *)indexPath {
    
    if (editingStyle == UITableViewCellEditingStyleDelete) {
        // Delete the row from the data source.
        [tableView deleteRowsAtIndexPaths:[NSArray arrayWithObject:indexPath] withRowAnimation:UITableViewRowAnimationFade];
    }   
    else if (editingStyle == UITableViewCellEditingStyleInsert) {
        // Create a new instance of the appropriate class, insert it into the array, and add a new row to the table view.
    }   
}
*/


/*
// Override to support rearranging the table view.
- (void)tableView:(UITableView *)tableView moveRowAtIndexPath:(NSIndexPath *)fromIndexPath toIndexPath:(NSIndexPath *)toIndexPath {
}
*/


/*
// Override to support conditional rearranging of the table view.
- (BOOL)tableView:(UITableView *)tableView canMoveRowAtIndexPath:(NSIndexPath *)indexPath {
    // Return NO if you do not want the item to be re-orderable.
    return YES;
}
*/

#pragma mark -
#pragma mark titleForHeaderInSection

- (NSString *)tableView:(UITableView *)tableView titleForHeaderInSection:(NSInteger)section{
	if(section==0){
		NSString *str = [NSString stringWithFormat:@"今日天氣"]; 
		return str;
	}
	if(section==1){
		NSString *str = [NSString stringWithFormat:@"未來一周天氣"]; 
		return str;
	}
	return nil;
}

#pragma mark -
#pragma mark Table view delegate

- (void)tableView:(UITableView *)tableView didSelectRowAtIndexPath:(NSIndexPath *)indexPath {
	[self.tableView deselectRowAtIndexPath:indexPath animated:NO];
	
}


#pragma mark -
#pragma mark Memory management

- (void)didReceiveMemoryWarning {
    // Releases the view if it doesn't have a superview.
    [super didReceiveMemoryWarning];
    
    // Relinquish ownership any cached data, images, etc. that aren't in use.
}

- (void)viewDidUnload {
    // Relinquish ownership of anything that can be recreated in viewDidLoad or on demand.
    // For example: self.myOutlet = nil;
}


- (void)dealloc {
	[cityName release];
	[cityWeather release];
    [super dealloc];
}


@end

