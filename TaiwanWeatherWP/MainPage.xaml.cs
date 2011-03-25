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
using Clarity.Phone.Controls;

namespace TaiwanWeatherWP {
    public partial class MainPage : AnimatedBasePage {
        // Constructor
        public MainPage() {
            InitializeComponent();

            // Set the data context of the listbox control to the sample data
            DataContext = App.ViewModel;
            this.Loaded += new RoutedEventHandler(MainPage_Loaded);

            AnimationContext = LayoutRoot;
        }

        // Handle selection changed on ListBox
        private void MainListBox_SelectionChanged(object sender, SelectionChangedEventArgs e) {
            // If selected index is -1 (no selection) do nothing
            if (MainListBox.SelectedIndex == -1)
                return;

            // Navigate to the new page
            NavigationService.Navigate(new Uri("/DetailsPage.xaml?selectedItem=" + MainListBox.SelectedIndex, UriKind.Relative));

            // Reset selected index to -1 (no selection)
            MainListBox.SelectedIndex = -1;
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

        // Show lab's page
        private void AboutUs_Pressed(object sender, EventArgs e) {
            NavigationService.Navigate(new Uri("/AboutUs.xaml", UriKind.Relative));
        }
    }
}