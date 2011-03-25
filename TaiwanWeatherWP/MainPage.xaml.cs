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
using Clarity.Phone.Controls.Animations;

namespace TaiwanWeatherWP {
    public partial class MainPage : AnimatedBasePage {
        // Note selected index for page transition
        int selectedIndex = 0;
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
            String cityName = (MainListBox.SelectedItem as City).cityName;
            String cityEnName = (MainListBox.SelectedItem as City).cityEnName;
            NavigationService.Navigate(new Uri("/CityDetail.xaml?cityName=" + cityName + "&cityEnName=" + cityEnName, UriKind.Relative));

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

        // Page Animation
        protected override Clarity.Phone.Controls.Animations.AnimatorHelperBase GetAnimation(AnimationType animationType, Uri toOrFrom) {
            if (toOrFrom != null) {
                if (toOrFrom.OriginalString.Contains("CityDetail.xaml")) {
                    if (animationType == AnimationType.NavigateForwardOut)
                        selectedIndex = MainListBox.SelectedIndex;
                    return GetContinuumAnimation(MainListBox.ItemContainerGenerator.ContainerFromIndex(selectedIndex) as FrameworkElement, animationType);
                }
            }
            return base.GetAnimation(animationType, toOrFrom);
        }
    }
}