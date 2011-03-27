using System;
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
using Clarity.Phone.Controls;
using Clarity.Phone.Controls.Animations;
using System.Windows.Navigation;
using System.IO;
using System.Text;
using System.Runtime.Serialization.Json;
using TaiwanWeatherWP.ViewModels;

namespace TaiwanWeatherWP {
    public partial class CityDetail : AnimatedBasePage {
        CurrentInformation currentData;
        ForecastInformation forecastData;

        public CityDetail() {
            InitializeComponent();
            AnimationContext = LayoutRoot;
        }

        protected override void OnNavigatedTo(NavigationEventArgs e) {
            // Update Page title
            String cityName;
            if (NavigationContext.QueryString.TryGetValue("cityName", out cityName))
                PageTitle.Text = cityName;
            // Get URL
            String cityEnName;
            if (!NavigationContext.QueryString.TryGetValue("cityEnName", out cityEnName))
                // No CityEnName
                return;

            // Prepare to load data
            String forecastURL = App.GAE_BaseURL + "forecast/" + cityEnName + "/";
            String currentURL = App.GAE_BaseURL + "current/" + cityEnName + "/";

            // Load Data
            WebClient currentDataWebClient = new WebClient();
            currentDataWebClient.OpenReadAsync(new Uri(currentURL));
            currentDataWebClient.OpenReadCompleted += new OpenReadCompletedEventHandler(currentDataWebClient_OpenReadCompleted);

            WebClient forecastDataWebClient = new WebClient();
            forecastDataWebClient.OpenReadAsync(new Uri(forecastURL));
            forecastDataWebClient.OpenReadCompleted += new OpenReadCompletedEventHandler(forecastDataWebClient_OpenReadCompleted);
        }

        // Async Get data
        private MemoryStream getMemoryStream(OpenReadCompletedEventArgs e) {
            StreamReader reader = new StreamReader(e.Result);
            String resultString = reader.ReadToEnd();
            return new MemoryStream(Encoding.Unicode.GetBytes(resultString));
        }
        private void currentDataWebClient_OpenReadCompleted(object sender, OpenReadCompletedEventArgs e) {
            DataContractJsonSerializer serializer = new DataContractJsonSerializer(typeof(CurrentInformation));
            currentData = serializer.ReadObject(getMemoryStream(e)) as CurrentInformation;
        }
        private void forecastDataWebClient_OpenReadCompleted(object sender, OpenReadCompletedEventArgs e) {
            DataContractJsonSerializer serialzer = new DataContractJsonSerializer(typeof(ForecastInformation));
            forecastData = serialzer.ReadObject(getMemoryStream(e)) as ForecastInformation;
        }
        
        // Animation
        protected override AnimatorHelperBase GetAnimation(AnimationType animationType, Uri toOrFrom) {
            return GetContinuumAnimation(ApplicationTitle, animationType);
        }
    }
}