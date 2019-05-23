import pandas as pd
from math import pi
import matplotlib.pyplot as plt

# radar chart
def radarPlot(variableNamingScore, variableUsageScore, argumentNamingScore, argumentUsageScore,
              activityNamingScore, screenshotScore, wfAnnotationScore, logMessageScore):
    # Set data
    df = pd.DataFrame({
        'group': ['Score', 'tolerance'],
        'Variable Naming': [variableNamingScore, 90],
        'Variable Usage': [variableUsageScore, 100],
        'Argument Naming': [argumentNamingScore, 90],
        'Argument Usage': [argumentUsageScore, 100],
        'Activity Naming': [activityNamingScore, 100],
        'Exception Screenshot': [screenshotScore, 100],
        'Exception Log Message': [logMessageScore, 100],
        'Workflow Annotation': [wfAnnotationScore, 100]
    })

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
    ax.plot(angles, values, linewidth=0, linestyle='solid', label="group A")
    # for i, v in enumerate(values):
    #     ax.text(i, v, "%d" % v, fontsize=12)
    ax.fill(angles, values, 'b', alpha=0.1)

    # Tolerance
    values = df.loc[1].drop('group').values.flatten().tolist()
    values += values[:1]
    ax.plot(angles, values, linewidth=1, linestyle='--', label="group B")

    # finish up
    plt.savefig('static/dist/Score.png')
    plt.close()
# end radar chart