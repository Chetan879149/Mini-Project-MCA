import kivy
import os
import random  # Import random to simulate changing vitals
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.properties import StringProperty, ColorProperty
from kivy.lang import Builder
from kivy.utils import get_color_from_hex
from kivy.clock import Clock
from kivy.uix.screenmanager import Screen

# --- Import Kivy Garden Graph ---
# Ensure these are installed: pip install kivy-garden && kivy garden install graph
try:
    from kivy_garden.graph import Graph, MeshLinePlot
except ImportError:
    print("Error: kivy_garden.graph not installed.")
    print("Run: pip install kivy-garden && kivy garden install graph")
    exit(1)

kivy.require('2.1.0')

class VitalBox(BoxLayout):
    """
    Custom Widget for the colored vital statistics boxes.
    Properties are set in the KV file.
    """
    title = StringProperty('')
    value = StringProperty('')
    unit = StringProperty('')
    box_color = ColorProperty((0, 0, 0, 1))

from kivy.clock import Clock
class PatientScreen(Screen):
    """
    Root Widget for the Dashboard.
    """
    def on_enter(self):
        # Wait until the screen is actually entered/visible
        self.setup_graph()
        # We delay graph setup slightly to ensure the KV layout is fully loaded
        Clock.schedule_once(self.setup_graph, 0)

    def setup_graph(self, dt):
        """
        Initializes the graph data and adds plots.
        """
        # Access the graph widget defined in KV using its ID
        graph = self.ids.vitals_graph

        # 1. Heart Rate Plot (Red)
        # We store it as 'self.hr_plot' so we can update it later
        self.hr_plot = MeshLinePlot(color=get_color_from_hex("#E74C3C"))
        self.hr_plot.points = [(i, random.randint(70, 85)) for i in range(12)]
        
        # 2. Blood Pressure Plot (Blue)
        # We store it as 'self.bp_plot' so we can update it later
        self.bp_plot = MeshLinePlot(color=get_color_from_hex("#3498DB"))
        self.bp_plot.points = [(i, random.randint(110, 130)) for i in range(12)]

        # Add plots to the graph
        graph.add_plot(self.hr_plot)
        graph.add_plot(self.bp_plot)

        # --- START DYNAMIC UPDATES ---
        # Call self.update_graph every 1.0 second
        Clock.schedule_interval(self.update_graph, 1.0)

    def update_graph(self, dt):
        """
        Called every second by the Clock.
        It shifts data to the left and adds a new random point at the end.
        """
        
        # --- Update Heart Rate ---
        # 1. Extract just the Y values (heart rates) from the current points
        current_hr_y = [point[1] for point in self.hr_plot.points]
        # 2. Remove the first (oldest) value and add a new random value at the end
        new_hr_y = current_hr_y[1:] + [random.randint(70, 90)]
        # 3. Rebuild the list of (x, y) tuples. 'i' is the X axis (0 to 11)
        self.hr_plot.points = [(i, y) for i, y in enumerate(new_hr_y)]

        # --- Update Blood Pressure ---
        # Same logic as above
        current_bp_y = [point[1] for point in self.bp_plot.points]
        new_bp_y = current_bp_y[1:] + [random.randint(115, 135)]
        self.bp_plot.points = [(i, y) for i, y in enumerate(new_bp_y)]

class PatientDashboardApp(App):
    def build(self):
        # Robustly load the KV file relative to this script
        current_dir = os.path.dirname(os.path.abspath(__file__))
        kv_file_path = os.path.join(current_dir, 'kv', 'patient.kv')
        
        try:
            Builder.load_file("kv/patient.kv")
        except FileNotFoundError:
            print(f"\nERROR: Could not find KV file at: {kv_file_path}")
            print("Please create a folder named 'kv' and place 'patient.kv' inside it.\n")
            exit(1)

        return PatientDashboard()

