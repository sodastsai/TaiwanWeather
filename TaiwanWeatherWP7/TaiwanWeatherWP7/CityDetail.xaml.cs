using System;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Animation;
using System.Windows.Shapes;
using Microsoft.Phone.Controls;
using System.Windows.Navigation;

namespace TaiwanWeatherWP7 {
    public partial class CityDetail : PhoneApplicationPage {
        public CityDetail() {
            InitializeComponent();
        }

        // When page is navigated to set data context to selected item in list
        protected override void OnNavigatedTo(NavigationEventArgs e) {
            string cityName = "";
            if (NavigationContext.QueryString.TryGetValue("cityName", out cityName))
                PageTitle.Text = cityName;

            string cityEnName = "";
            if (NavigationContext.QueryString.TryGetValue("cityEnName", out cityEnName)) {
                String currentURL = "http://ntu-taiwan-weather.appspot.com/json/current/" + cityEnName + "/";
                String forecastURL = "http://ntu-taiwan-weather.appspot.com/json/forecast/" + cityEnName + "/";
                System.Diagnostics.Debug.WriteLine(currentURL);
                System.Diagnostics.Debug.WriteLine(forecastURL);
            }
        }
    }
}