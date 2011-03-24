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

namespace TaiwanWeather {
    public partial class MainPage : PhoneApplicationPage {
        // Constructor
        public MainPage() {
            InitializeComponent();

            // Set the data context of the listbox control to the sample data
            DataContext = App.ViewModel;
            this.Loaded += new RoutedEventHandler(MainPage_Loaded);
        }

        // Load data for the ViewModel Items
        private void MainPage_Loaded(object sender, RoutedEventArgs e) {
            if (!App.ViewModel.IsDataLoaded) {
                App.ViewModel.LoadData();
            }
        }

        // Call IE to show cwb.gov.tw
        private void CWB_Pressed(object sender, EventArgs e) {
            WebBrowserTask cwbWeb = new WebBrowserTask();
            cwbWeb.URL = "http://www.cwb.gov.tw/";
            cwbWeb.Show();
        }

        private void AboutUs_Pressed(object sender, EventArgs e) {
            NavigationService.Navigate(new Uri("/Views/AboutUs.xaml", UriKind.Relative));
        }

    }
}