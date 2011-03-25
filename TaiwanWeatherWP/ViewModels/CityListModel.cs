using System;
using System.ComponentModel;
using System.Diagnostics;
using System.Net;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Documents;
using System.Windows.Ink;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Animation;
using System.Windows.Shapes;

namespace TaiwanWeatherWP {
    public class City : INotifyPropertyChanged {
        private string name;
        public string cityName {
            get { return name; }
            set {
                if (value != name) {
                    name = value;
                    NotifyPropertyChanged("CityName");
                }
            }
        }

        private string enName;
        public string cityEnName {
            get { return enName; }
            set {
                if (value != enName) {
                    enName = value;
                    NotifyPropertyChanged("CityEnName");
                }
            }
        }

        public event PropertyChangedEventHandler PropertyChanged;

        private void NotifyPropertyChanged(String propertyName) {
            PropertyChangedEventHandler handler = PropertyChanged;
            if (null != handler)
                handler(this, new PropertyChangedEventArgs(propertyName));
        }
    }
}