using System;
using System.ComponentModel;
using System.Collections.Generic;
using System.Diagnostics;
using System.Text;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Shapes;
using System.Collections.ObjectModel;
using System.Net;
using System.IO;
using System.Runtime.Serialization.Json;


namespace TaiwanWeatherWP {
    public class BasicCity {
        public String name;
        public String enName;
    }

    public class MainViewModel : INotifyPropertyChanged {
        public MainViewModel() {
            this.cityList = new ObservableCollection<City>();
        }

        // Data Source Itself
        public ObservableCollection<City> cityList { get; private set; }

        private string _sampleProperty = "CityList Sample";
        public string SampleProperty {
            get { return _sampleProperty; }
            set {
                if (value != _sampleProperty) {
                    _sampleProperty = value;
                    NotifyPropertyChanged("SampleProperty");
                }
            }
        }

        public bool IsDataLoaded { get; private set; }

        public void LoadData() {
            // Get a web client to fetch string from Network
            WebClient webClient = new WebClient();
            webClient.OpenReadAsync(new Uri(App.GAE_BaseURL + "city/"));
            webClient.OpenReadCompleted += new OpenReadCompletedEventHandler(webClientCompletedRead); // Completed Method
        }

        // Async Result
        private void webClientCompletedRead(object sender, OpenReadCompletedEventArgs e) {
            using (var reader = new StreamReader(e.Result)) {
                // Get string
                String result = reader.ReadToEnd();
                // Convert from JSON to Object
                MemoryStream jsonStream = new MemoryStream(Encoding.Unicode.GetBytes(result));
                DataContractJsonSerializer serializer = new DataContractJsonSerializer(typeof(List<BasicCity>));
                List<BasicCity> BasicCityList = serializer.ReadObject(jsonStream) as List<BasicCity>;
                // Save the result
                foreach (BasicCity c in BasicCityList)
                    this.cityList.Add(new City() { cityName = c.name, cityEnName = c.enName });
                this.IsDataLoaded = true;
            }
        }

        public event PropertyChangedEventHandler PropertyChanged;
        private void NotifyPropertyChanged(String propertyName) {
            PropertyChangedEventHandler handler = PropertyChanged;
            if (null != handler) {
                handler(this, new PropertyChangedEventArgs(propertyName));
            }
        }
    }
}