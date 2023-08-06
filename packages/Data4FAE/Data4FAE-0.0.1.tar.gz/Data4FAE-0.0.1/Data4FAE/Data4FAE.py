import os
import pandas as pd
import seaborn as sns
from pandas.plotting import table
import matplotlib.pyplot as plt
import folium
from dms2dec.dms_convert import dms2dec

def test_import():
    print ("import working!")

class ProcessData:
    def __init__(self, url_from="https://data.nasa.gov/resource/mc52-syum.json", path_to=""):
        # mc52_df is the dataframe with the data from the url. Access this Dataset via SODA API.
        self.mc52_df = pd.read_json(url_from)
        # defines  for parse data.
        self.points = []
        self.alt = []
        self.date = []
        self.radiated_energy = []
        self.top_15_radiation_index = []
        # parse data and set the path to log
        self.parse_data()  # process the data
        self.path = path_to  # Path for store

    def explore_data(self):
        # Start exploring data
        print("Data fame description:\n\n")
        print("len of pandas DF:", len(self.mc52_df))
        print("len of pandas DF: (row,col) -> ", self.mc52_df.shape)  # get the number of row and col
        print("\nDF head", self.mc52_df.head())
        print(self.mc52_df.info())
        print(self.mc52_df.describe())
        print("\n\nColumns:", self.mc52_df.columns)

    def parse_data(self):
        # converting data from df to python list.
        self.alt = self.mc52_df["altitude_km"].to_list()
        self.date = self.mc52_df["date_time_peak_brightness_ut"].to_list()
        self.radiated_energy = self.mc52_df["total_radiated_energy_j"].to_list()

        # Get the top 15 in radiation
        self.top_15_radiation_index = self.mc52_df["total_radiated_energy_j"].nlargest(n=15).index.to_list()

        # save the points need to convert to dec, according to
        # https://python-visualization.github.io/folium/quickstart.html#Markers
        for index in self.top_15_radiation_index:
            lat = self.mc52_df.iloc[index]["latitude_deg"]
            long = self.mc52_df.iloc[index]["longitude_deg"]
            self.points.append([lat, long])

    def mark_points_in_map(self):
        # Mark in the map
        # I suppose that the coordinate correspond to the observation point.
        # Sincerely i didn't read detailed the data information

        map_obj = folium.Map(location=[20, 0], tiles="OpenStreetMap", zoom_start=2)
        for point in self.points:
            folium.Marker(location=[dms2dec(point[0]), dms2dec(point[1])]).add_to(map_obj)

        title_html = '''
                     <h3 align="center" style="font-size:20px"><b>FAE-technical-interview -
                      Top 15 radiated energy - Map using Folium</b></h3>
                     '''
        map_obj.get_root().html.add_child(folium.Element(title_html))
        map_obj.save(self.path+os.sep+"map.html")

    def plot_3_axis_velocity(self, show=False):
        # Plot the velocity in 3 axis
        vx = []
        vy = []
        vz = []
        for index in range(len(self.mc52_df)):
            vx.append(self.mc52_df.iloc[index]["velocity_components_km_s_vx"])
            vy.append(self.mc52_df.iloc[index]["velocity_components_km_s_vy"])
            vz.append(self.mc52_df.iloc[index]["velocity_components_km_s_vz"])
        # generate each plot
        plt.plot(vx, label='Velocity X', marker='.')
        plt.plot(vy, label='Velocity Y', marker='1')
        plt.plot(vz, label='Velocity Z', marker='*')
        plt.grid(True, which="both", ls="-")
        plt.title("Velocity in each axis")
        plt.xlabel("Obs ID")
        plt.ylabel("Velocity [Km/s]")
        plt.legend()
        plt.savefig(self.path+os.sep+"Velocity_3_axis.png")
        if show:
            plt.show()
        else:
            plt.close()
            plt.clf()

    def histogram_radiation(self):
        # Get radiation Histogram
        total_radiation = self.mc52_df["total_radiated_energy_j"].to_list()
        estimated_impact_energy = self.mc52_df["calculated_total_impact_energy_kt"].to_list()
        num_bins = 50
        plt.hist(estimated_impact_energy, num_bins, density=True, histtype='bar', label="Total impact energy")
        plt.title("Total impact energy distribution")
        plt.xlabel("energy [J]")
        plt.ylabel("Probability")
        plt.legend()
        plt.show()
        plt.savefig(self.path+os.sep+"impact_energy_distribution.png")
        plt.clf()

        plt.hist(total_radiation, num_bins, density=True, histtype='bar', label="Total radiated energy")
        plt.title("Total radiated energy distribution")
        plt.xlabel("energy [J]")
        plt.ylabel("Probability")
        plt.legend()
        plt.show()
        plt.savefig(self.path+os.sep+"total_radiated_energy_distribution.png")
        plt.clf()

    def histogram_altitude(self):
        # Create another histogram for altitude, using seaborn
        # seaborn histogram
        alt = self.mc52_df["altitude_km"].to_list()
        sns.distplot(alt, hist=True, kde=False, bins=int(180/5), color='blue', hist_kws={'edgecolor': 'black'})
        plt.title('Histogram of Altitude')
        plt.xlabel('Altitude [Km]')
        plt.ylabel('Probability')
        plt.savefig(self.path+os.sep+"Altitude_histogram.png")
        plt.clf()

    def create_pdf(self,  len_data=15):
        # make the PDF file from the Pandas df
        ax = plt.subplot(111, frame_on=False)
        ax.xaxis.set_visible(0)
        ax.yaxis.set_visible(0)
        table(ax, self.mc52_df.head(len_data), loc='upper center')
        plt.savefig(self.path+os.sep+'20_first_entries.pdf')
        plt.close()


if __name__ == "__main__":
    data = ProcessData(url_from="https://data.nasa.gov/resource/mc52-syum.json",  path_to=r"C:\out")
    data.plot_3_axis_velocity()
    data.mark_points_in_map()
    data.histogram_radiation()
    data.histogram_altitude()
    data.create_pdf(len_data=16)
    data.explore_data()
