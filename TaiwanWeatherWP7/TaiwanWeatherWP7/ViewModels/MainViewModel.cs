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


namespace TaiwanWeatherWP7 {
    // City list object
    public class City {
        public string name { set; get; }
        public string enName { set; get; }
    }

    public class MainViewModel : INotifyPropertyChanged {
        public MainViewModel() {
            this.CityLists = new ObservableCollection<CityListModel>();
        }

        /// <summary>
        /// A collection for ItemViewModel objects.
        /// </summary>
        public ObservableCollection<CityListModel> CityLists { get; private set; }

        public bool IsDataLoaded {
            get;
            private set;
        }

        public void LoadData() {
            // Get a web client to fetch string from Network
            var webClient = new WebClient();
            webClient.OpenReadAsync(new Uri("http://ntu-taiwan-weather.appspot.com/json/city/"));
            webClient.OpenReadCompleted += new OpenReadCompletedEventHandler(webClientCompletedRead); // Completed Method
        }

        private void webClientCompletedRead(object sender, OpenReadCompletedEventArgs e) {
            using (var reader = new StreamReader(e.Result)) {
                // Get string
                string result = reader.ReadToEnd();
                // Convert from JSON to Object
                MemoryStream jsonStream = new MemoryStream(Encoding.Unicode.GetBytes(result));
                DataContractJsonSerializer serializer = new DataContractJsonSerializer(typeof(List<City>));
                List<City> cityLists = (List<City>)serializer.ReadObject(jsonStream);
                // Make it to city list box
                foreach (City c in cityLists)
                    this.CityLists.Add(new CityListModel() { cityName = c.name, cityEnName = c.enName });
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