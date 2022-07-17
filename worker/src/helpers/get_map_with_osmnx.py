from typing import Tuple
import networkx
import osmnx as ox
from matplotlib import figure


def _plot_graph(
        graph: networkx.MultiDiGraph,
        bgcolor: str,
        roadColors: list,
        roadWidths) -> figure:
    """
    Converts a graph into figure using the supplied styles.

    Parameters
    ----------
        graph : networkx.MultiDiGraph
            Ox's MultiDiGraph is used to extract informations about the
            streets.

        bgcolor: string
            This fields expec ts a string containing the background color in
            hexadecimal format. 

        roadColors: strings[]
            List of string representing the colors.
        
        roadWidths"
            List of numbers representing the width of the lines. 

    Returns
    ---------
        Retusn a Matplotlib's figure
    
    """

    fig, ax = ox.plot_graph(
        graph,
        node_size=0,
        bbox = None,
        dpi = 300,
        bgcolor = bgcolor,
        save = False,
        show = False,
        edge_color=roadColors,
        edge_linewidth=roadWidths,
        edge_alpha=1)

    fig.tight_layout(pad=0)
    
    return fig

def _generate_graph(center_point: Tuple[float, float], distance:int):
    """
    This function create a map graph using
    ther coordinates of the cente and the raius.

    Parameters
    -----------

        center_point: Tuple(number, number)
            Is a tuple that represents the pair of coordinates (lat, lon).
        distance: int
            Is a number that represents the radius in meters in
            order to get the information inside that radius.
    
    Returns
    ----------
        Returns a tuple with the graph (networkx.MultiDiGraph) in the first
        position and an array with descriptive information of the ways.

    """
    graph = ox.graph_from_point(center_point, dist=distance, retain_all=True, simplify = True, network_type='all')

    u = []
    v = []
    key = []
    data = []
    for uu, vv, kkey, ddata in graph.edges(keys=True, data=True):
        u.append(uu)
        v.append(vv)
        key.append(kkey)
        data.append(ddata)
    return graph,data

def _get_styles(multigraph: networkx.MultiDiGraph) -> Tuple[list, list]:
    """
    This function creates a pair of lists contaning the styles for
    the streets based on the length and the type of each one.

    Parameters
    ----------
        multigraph : networkx.MultiDiGraph
            Ox's MultiDiGraph is used to extract informations about the
            streets.

    Returns
    ----------

        This functions returns a tuple with two lists: the first one is a
        list of strnig representing the colors; the second one refers to
        the width of the lines. 

    """

    # Lists to store colors and widths 
    roadColors = []
    roadWidths = []

    for item in multigraph:
        if "length" in item.keys():
            if item["length"] <= 100:
                linewidth = 0.10
                color = "#a6a6a6" 
                
            elif item["length"] > 100 and item["length"] <= 200:
                linewidth = 0.15
                color = "#676767"
                
            elif item["length"] > 200 and item["length"] <= 400:
                linewidth = 0.25
                color = "#454545"
                
            elif item["length"] > 400 and item["length"] <= 800:
                color = "#bdbdbd"
                linewidth = 0.35
            else:
                color = "#d5d5d5"
                linewidth = 0.45

            if "primary" in item["highway"]:
                linewidth = 0.5
                color = "#ffff"
        else:
            color = "#a6a6a6"
            linewidth = 0.10
                
        roadColors.append(color)
        roadWidths.append(linewidth)

    return roadColors,roadWidths


def generate_map_snapshot(center_point: Tuple[float, float], file_name: str, bgcolor: str):
    """
    This function generates a map snapshots and save it in a .png file.

    Parameters
    ----------
        center_point: Tuple(number, number)
            Is a tuple that represents the pair of coordinates (lat, lon).

        file_name: string
            Final name of the file.

        bgcolor: string
            This fields expec ts a string containing the background color in
            hexadecimal format. 

    """


    graph, data = _generate_graph(center_point, 2000)    

    roadColors, roadWidths = _get_styles(data)

    fig = _plot_graph(graph, bgcolor, roadColors, roadWidths)

    fig.savefig(
        file_name,
        dpi=300,
        bbox_inches='tight',
        format="png",
        facecolor=fig.get_facecolor(),
        transparent=False)


if __name__ == "__main__":
    center = (40.4168, -3.7038)
    bgcolor = "#061529"
    generate_map_snapshot(center, "madrid.png", bgcolor)