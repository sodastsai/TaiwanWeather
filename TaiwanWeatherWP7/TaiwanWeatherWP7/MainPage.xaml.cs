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
using Microsoft.Phone.Tasks;
using System.Runtime.Serialization.Json;
using System.IO;
using System.Text;

namespace TaiwanWeatherWP7 {
    // City list object
    public class City {
        public string name {set; get;}
        public string enName {set; get;}
    }

    public partial class MainPage : PhoneApplicationPage {
        // Data source
        List<City> cityLists;

        // Constructor
        public MainPage() {
            InitializeComponent();

            // Set the data context of the listbox control to the sample data
            DataContext = App.ViewModel;
            this.Loaded += new RoutedEventHandler(MainPage_Loaded);
        }

        // Handle selection changed on ListBox
        private void CityListBox_SelectionChanged(object sender, SelectionChangedEventArgs e) {
            // If selected index is -1 (no selection) do nothing
            if (CityListBox.SelectedIndex == -1)
                return;

            // Navigate to the new page
            NavigationService.Navigate(new Uri("/DetailsPage.xaml?selectedItem=" + CityListBox.SelectedIndex, UriKind.Relative));

            // Reset selected index to -1 (no selection)
            CityListBox.SelectedIndex = -1;
        }

        // Load data for the ViewModel Items
        private void MainPage_Loaded(object sender, RoutedEventArgs e) {
            if (!App.ViewModel.IsDataLoaded) {
                App.ViewModel.LoadData();

                // Get a web client to fetch string from Network
                var webClient = new WebClient();
                webClient.OpenReadAsync(new Uri("http://ntu-taiwan-weather.appspot.com/json/city/"));
                webClient.OpenReadCompleted += new OpenReadCompletedEventHandler(webClientCompletedRead); // Completed Method
            }
        }

        void webClientCompletedRead(object sender, OpenReadCompletedEventArgs e) {
            using (var reader = new StreamReader(e.Result)) {
                // Get string
                string result = reader.ReadToEnd();
                // Convert from JSON to Object
                MemoryStream jsonStream = new MemoryStream(Encoding.Unicode.GetBytes(result));
                DataContractJsonSerializer serializer = new DataContractJsonSerializer(typeof(List<City>));
                cityLists = (List<City>)serializer.ReadObject(jsonStream);
                // Make it to city list box
                CityListBox.ItemsSource = cityLists;
            }
        }

        // Call IE to show cwb.gov.tw
        private void CWB_Pressed(object sender, EventArgs e) {
            WebBrowserTask cwbWeb = new WebBrowserTask();
            cwbWeb.URL = "http://www.cwb.gov.tw/";
            cwbWeb.Show();
        }

        // Show lab's page
        private void AboutUs_Pressed(object sender, EventArgs e) {
            NavigationService.Navigate(new Uri("AboutUs.xaml", UriKind.Relative));
        }

        private void PhoneApplicationPage_Loaded(object sender, RoutedEventArgs e) {

        }
    }
}