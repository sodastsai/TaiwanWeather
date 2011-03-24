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

namespace TaiwanWeather.Views {
    public partial class AboutUs : PhoneApplicationPage {
        public AboutUs() {
            InitializeComponent();
        }

        private void PhoneApplicationPage_Loaded(object sender, RoutedEventArgs e) {
        }

        private void LabWebSite_Click(object sender, RoutedEventArgs e) {
            WebBrowserTask labWeb = new WebBrowserTask();
            labWeb.URL = "http://www.ntumobile.org/";
            labWeb.Show();
        }
    }
}