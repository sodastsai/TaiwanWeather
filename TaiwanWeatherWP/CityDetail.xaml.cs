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
using Clarity.Phone.Controls;
using Clarity.Phone.Controls.Animations;
using System.Windows.Navigation;

namespace TaiwanWeatherWP {
    public partial class CityDetail : AnimatedBasePage {
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
            if (NavigationContext.QueryString.TryGetValue("cityEnName", out cityEnName)) {
                System.Diagnostics.Debug.WriteLine(cityEnName);
            } else {
                return;
            }

            String forecastURL = App.GAE_BaseURL + "forecast/" + cityEnName + "/";
            String currentURL = App.GAE_BaseURL + "current/" + cityEnName + "/";
            System.Diagnostics.Debug.WriteLine(forecastURL);
            System.Diagnostics.Debug.WriteLine(currentURL);
        }

        protected override AnimatorHelperBase GetAnimation(AnimationType animationType, Uri toOrFrom) {
            return GetContinuumAnimation(ApplicationTitle, animationType);
            //return base.GetAnimation(animationType, toOrFrom);
        }
    }
}