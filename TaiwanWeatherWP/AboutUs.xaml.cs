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

namespace TaiwanWeatherWP {
    public partial class AboutUs : PhoneApplicationPage {
        public AboutUs() {
            InitializeComponent();
            //AnimationContext = LayoutRoot;
        }

        private void LabWebSite_Click(object sender, RoutedEventArgs e) {
            WebBrowserTask labWeb = new WebBrowserTask();
            labWeb.URL = "http://www.ntumobile.org/";
            labWeb.Show();
        }

        // Animation
        protected override void OnBackKeyPress(System.ComponentModel.CancelEventArgs e) {
            e.Cancel = true;
            Storyboard storyboard = Application.Current.Resources["FlipBackwardOut"] as Storyboard;
            Storyboard.SetTarget(storyboard, LayoutRoot);
            EventHandler completedHandler = delegate { };
            completedHandler = delegate {
                storyboard.Stop();
                storyboard.Completed -= completedHandler;

                NavigationService.GoBack();
            };
            storyboard.Completed += completedHandler;
            storyboard.Begin();
        }
    }
}