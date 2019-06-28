import pandas as pd
from math import pi
import matplotlib.pyplot as plt
from os import path

# radar chart
def radarPlot(lst_score, lst_tolerance, lst_checkName, main_location):
    # Set data
    dict = {'group': ['Score', 'tolerance']}
    for i in range(len(lst_score)):
        dict[lst_checkName[i]] = [lst_score[i], lst_tolerance[i]]
    df = pd.DataFrame(dict)

    categories = list(df)[1:]
    N = len(categories)
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]
    plt.figure(figsize=(10, 10))
    ax = plt.subplot(111, polar=True)
    plt.xticks(angles[:-1], categories, color='Blue', size=12)
    ax.set_rlabel_position(0)
    plt.yticks([20, 40, 60, 80, 100], ["20", "40", "60", "80", "100"], color="grey", size=10)
    plt.ylim(0, 100)

    # Actual
    values = df.loc[0].drop('group').values.flatten().tolist()
    values += values[:1]
    ax.plot(angles, values, linewidth=1, linestyle='solid', label="group A")
    # for i, v in enumerate(values):
    #     ax.text(i, v, "%d" % v, fontsize=12)
    ax.fill(angles, values, 'b', alpha=0.1)

    # Tolerance
    values = df.loc[1].drop('group').values.flatten().tolist()
    values += values[:1]
    ax.plot(angles, values, linewidth=1, linestyle='--', label="group B")

    # finish up
    radarStore = "/".join(main_location.split("/")[:-3]) + "/static/dist/chart/radar.png"
    count = 1
    picExists = path.isfile(radarStore)
    while picExists:
        radarStore = "/".join(main_location.split("/")[:-3]) + "/static/dist/chart/radar" + str(count) + ".png"
        picExists = path.isfile(radarStore)
        count += 1
    plt.savefig(radarStore)
    plt.close()

    return radarStore
# end radar chart