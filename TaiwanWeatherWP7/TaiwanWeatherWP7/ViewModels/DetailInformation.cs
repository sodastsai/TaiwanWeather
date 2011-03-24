using System;
using System.Net;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Documents;
using System.Windows.Ink;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Animation;
using System.Windows.Shapes;
using System.Collections.Generic;

namespace TaiwanWeatherWP7 {
    // Basic Information
    public class BasicInformation {
        public String image { get; set; }
        public String description { get; set; }
        public String temperature { get; set; }
    }
    // Current Weather Information
    public class CurrentInformation : BasicInformation {
        public String city { get; set; }
    }
    // Components of Forecast Weather Information
    public class TouristComponent : BasicInformation {
        public String name { get; set; }
        public List<BasicInformation> forecast { get; set; }
    }
    public class RecentComponent : BasicInformation {
        public String feel { get; set; }
        public String rainProbability { get; set; }
    }
    // Forecast Weather Information
    public class ForecastInformation {
        public List<BasicInformation> week { get; set; }
        public List<TouristComponent> tourist { get; set; }
        public List <RecentComponent> recent { get; set; }
    }
}
