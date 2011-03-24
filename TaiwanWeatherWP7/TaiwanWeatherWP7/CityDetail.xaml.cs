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
using System.IO;
using System.Text;
using System.Runtime.Serialization.Json;

namespace TaiwanWeatherWP7 {
    public partial class CityDetail : PhoneApplicationPage {
        // Weather Data
        ForecastInformation forecastData;
        CurrentInformation currentData;

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
                String currentURL = App.GAEBaseURL + "current/" + cityEnName + "/";
                WebClient currentWebClient = new WebClient();
                currentWebClient.OpenReadAsync(new Uri(currentURL));
                currentWebClient.OpenReadCompleted += new OpenReadCompletedEventHandler(currentCompletedRead);

                String forecastURL = App.GAEBaseURL + "forecast/" + cityEnName + "/";
                WebClient forecastWebClient = new WebClient();
                forecastWebClient.OpenReadAsync(new Uri(forecastURL));
                forecastWebClient.OpenReadCompleted += new OpenReadCompletedEventHandler(forecastCompletedRead);
            }
        }

        private void forecastCompletedRead(object sender, OpenReadCompletedEventArgs e) {
            // Get String
            StreamReader reader = new StreamReader(e.Result);
            String result = reader.ReadToEnd();
            // Get json
            MemoryStream jsonStream = new MemoryStream(Encoding.Unicode.GetBytes(result));
            DataContractJsonSerializer serializer = new DataContractJsonSerializer(typeof(ForecastInformation));
            forecastData = serializer.ReadObject(jsonStream) as ForecastInformation;
        }

        private void currentCompletedRead(object sender, OpenReadCompletedEventArgs e) {
            // Get String
            StreamReader reader = new StreamReader(e.Result);
            String result = reader.ReadToEnd();
            // Get json
            MemoryStream jsonStream = new MemoryStream(Encoding.Unicode.GetBytes(result));
            DataContractJsonSerializer serializer = new DataContractJsonSerializer(typeof(CurrentInformation));
            currentData = serializer.ReadObject(jsonStream) as CurrentInformation;
        }
    }
}