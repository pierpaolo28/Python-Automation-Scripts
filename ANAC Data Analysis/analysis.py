import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import six
import seaborn as sns
import os
import time
from shutil import copyfile
pd.options.mode.chained_assignment = None


# https://stackoverflow.com/questions/26678467/export-a-pandas-dataframe-as-a-table-image
def render_mpl_table(data, col_width=3.0, row_height=0.625, font_size=14,
                     header_color='#40466e', row_colors=['#f1f1f2', 'w'], edge_color='w',
                     bbox=[0, 0, 1, 1], header_columns=0,
                     ax=None, **kwargs):
    if ax is None:
        size = (np.array(data.shape[::-1]) + np.array([0, 1])) * np.array([col_width, row_height])
        fig, ax = plt.subplots(figsize=size)
        ax.axis('off')

    mpl_table = ax.table(cellText=data.values, bbox=bbox, colLabels=data.columns, **kwargs)

    mpl_table.auto_set_font_size(False)
    mpl_table.set_fontsize(font_size)

    for k, cell in six.iteritems(mpl_table._cells):
        cell.set_edgecolor(edge_color)
        if k[0] == 0 or k[1] < header_columns:
            cell.set_text_props(weight='bold', color='w')
            cell.set_facecolor(header_color)
        else:
            cell.set_facecolor(row_colors[k[0] % len(row_colors)])
    return ax


def single_agent_focus(agent_name, df):
    one = df[df['Agent 1'] == agent_name]
    two = df[df['Agent 2'] == agent_name]
    one = one.drop(["Agent 2", "Utility 2","Disc. Util. 2", "Perceived. Util. 2",
                    "User Bother 2", "User Util. 2", "Profile 2"], axis=1)
    two = two.drop(["Agent 1", "Utility 1","Disc. Util. 1", "Perceived. Util. 1",
                    "User Bother 1", "User Util. 1", "Profile 1"], axis=1)
    two = two.rename(columns={"Agent 2" : "Agent 1", "Utility 2": "Utility 1",
                              "Disc. Util. 2": "Disc. Util. 1", "Perceived. Util. 2": "Perceived. Util. 1",
                              "User Bother 2" : "User Bother 1", "User Util. 2": "User Util. 1",
                              "Profile 2": "Profile 1"})
    result = pd.concat([one, two])
    return result


def utility_comp(name):
    df = pd.read_csv('log/results.csv', ';', skiprows=1)
    df = df.drop('Exception', axis=1)
    for i in range(0, df.shape[0]):
        df['Agent 1'][i] = df['Agent 1'][i].split('@', 1)[0]
        df['Agent 2'][i] = df['Agent 2'][i].split('@', 1)[0]

    agents = np.unique(np.append(df['Agent 1'].unique(), df['Agent 2'].unique()))

    data = {'Agents Name': agents, 'Overall Utility': np.zeros(len(agents)),
            'Total Dist to Nash': np.zeros(len(agents))}

    final_df = pd.DataFrame(data=data)

    for i in range(0, df.shape[0]):
        final_df['Overall Utility'][final_df['Agents Name'] == df['Agent 1'][i]] += df['Utility 1'][i]
        final_df['Overall Utility'][final_df['Agents Name'] == df['Agent 2'][i]] += df['Utility 2'][i]
        final_df['Total Dist to Nash'][final_df['Agents Name'] == df['Agent 1'][i]] += df['Dist. to Nash'][i]
        final_df['Total Dist to Nash'][final_df['Agents Name'] == df['Agent 2'][i]] += df['Dist. to Nash'][i]

    final_df['Matches Win'] = np.zeros(len(agents))
    final_df['N Matches'] = np.zeros(len(agents))

    for i in range(0, df.shape[0]):
        if df['Utility 1'][i] > df['Utility 2'][i]:
            final_df['Matches Win'][final_df['Agents Name'] == df['Agent 1'][i]] += 1
        elif df['Utility 1'][i] < df['Utility 2'][i]:
            final_df['Matches Win'][final_df['Agents Name'] == df['Agent 2'][i]] += 1
        else:
            final_df['Matches Win'][final_df['Agents Name'] == df['Agent 1'][i]] += 0
            final_df['Matches Win'][final_df['Agents Name'] == df['Agent 2'][i]] += 0
        final_df['N Matches'][final_df['Agents Name'] == df['Agent 1'][i]] += 1
        final_df['N Matches'][final_df['Agents Name'] == df['Agent 2'][i]] += 1

    folder = str(name) + str(time.strftime("_%Y-%m-%d_%H%M"))
    os.makedirs('log/' + folder)

    copyfile('log/results.csv', 'log/' + folder + '/results.csv')

    result = single_agent_focus(str(name), df)

    # ax = sns.distplot(result['Utility 1'])
    # plt.savefig('log/' + folder + '/seaborn_agent_utility.png')
    # plt.clf()

    # ax = sns.distplot(df['Dist. to Nash'])
    # plt.savefig('log/' + folder + '/seaborn_dist._to_nash.png')
    # plt.clf()

    ax = render_mpl_table(final_df.sort_values(by='Total Dist to Nash', ascending=True), header_columns=0, col_width=4.0)
    plt.savefig('log/' + folder + '/total_dist_to_nash_rank.png')
    plt.clf()

    ax = render_mpl_table(final_df.sort_values(by='Overall Utility', ascending=True), header_columns=0, col_width=4.0)
    plt.savefig('log/' + folder + '/overall_utility_rank.png')
    plt.clf()

    fig, ax = plt.subplots()
    ax.set_xlim([0, 1.41])
    ax.hist(df['Dist. to Nash'])
    textstr = '\n'.join((
        r'$\mu=%.2f$' % (df['Dist. to Nash'].mean(),),
        r'$\sigma=%.2f$' % (df['Dist. to Nash'].std(),),
        r'$\min=%.2f$' % (min(df['Dist. to Nash']),),
        r'$\max=%.2f$' % (max(df['Dist. to Nash']),)))
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    ax.set_title('Agent Distance To Nash Distribution')
    ax.set_ylabel("Number of Negotiations")
    ax.set_xlabel("Distance to Nash")
    ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=14,
        verticalalignment='top', bbox=props)
    plt.savefig('log/' + folder + '/dist._to_Nash.svg', dpi=300)

    fig, ax = plt.subplots()
    ax.set_xlim([0, 1])
    ax.hist(result['Utility 1'].values)
    textstr = '\n'.join((
        r'$\mu=%.2f$' % (result['Utility 1'].values.mean(),),
        r'$\sigma=%.2f$' % (result['Utility 1'].values.std(),),
        r'$\min=%.2f$' % (min(result['Utility 1'].values),),
        r'$\max=%.2f$' % (max(result['Utility 1'].values),)))
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    ax.set_title('Agent Utility Distribution')
    ax.set_ylabel("Number of Negotiations")
    ax.set_xlabel("Utility")
    ax.text(0.73, 0.95, textstr, transform=ax.transAxes, fontsize=14,
        verticalalignment='top', bbox=props)
    plt.savefig('log/' + folder + '/agent_utility.svg', dpi=300)

    figure(num=None, figsize=(6.66, 3.33), dpi=300, facecolor='w', edgecolor='k')
    ax = sns.jointplot(x= result['Utility 1'], y= df['Dist. to Nash'])
    ax.ax_joint.set_xlabel("Utility")
    ax.ax_joint.set_ylabel("Distance To Nash")
    ax.ax_joint.set_xlim([0, 1])
    ax.ax_joint.set_ylim([0, 1.41])
    plt.savefig('log/' + folder + '/distributions.svg', dpi=300)

    # collabel = ("Dist. to Nash", "Value")
    # plt.clf()
    # plt.axis('off')
    # plt.table(cellText=[['Mean', np.mean(df['Dist. to Nash'])], ['Std', np.std(df['Dist. to Nash'])],
    #                      ['Min', min(df['Dist. to Nash'])], ['Max', max(df['Dist. to Nash'])]],
    #           colLabels=collabel, loc='center')
    # plt.savefig('log/' + folder + '/summary1.png')

    # collabel = ("Utility", "Value")
    # plt.clf()
    # plt.axis('off')
    # plt.table(cellText=[['Mean', np.mean(result['Utility 1'])], ['Std', np.std(result['Utility 1'])],
    #                      ['Min', min(result['Utility 1'])], ['Max', max(result['Utility 1'])]],
    #           colLabels=collabel, loc='center')
    # plt.savefig('log/' + folder + '/summary2.png')

    distance = 'Dist. to Nash'
    score = {}
    for i in range(0, df.shape[0]):
        if df['Agent 1'][i] == str(name):
            try:
                score[df['Agent 2'][i]].append(df[distance][i])
            except KeyError:
                score[df['Agent 2'][i]] = []
                score[df['Agent 2'][i]].append(df[distance][i])
        elif df['Agent 2'][i] == str(name):
            try:
                score[df['Agent 1'][i]].append(df[distance][i])
            except KeyError:
                score[df['Agent 1'][i]] = []
                score[df['Agent 1'][i]].append(df[distance][i])

    plot_opp = []
    plot_dist = []
    for i in score.keys():
        plot_opp.append(i)
        plot_dist.append(np.mean(score[i]))

    figure(num=None, figsize=(6.66, 3.33), dpi=300, facecolor='w', edgecolor='k')
    plt.title(
        distance + " for " + str(name) + " (Mean: " + str(np.mean([x for x in plot_dist if str(x) != 'nan'])) + ")",
        fontsize=14)
    plt.ylim(0, 2)
    plt.xticks(fontsize=12, rotation=90)
    plt.yticks(fontsize=12)
    plt.bar(plot_opp, plot_dist)
    plt.ylabel("Average Distance to Nash", fontsize=14)
    plt.xlabel("Opponents",fontsize=14)
    plt.savefig('log/' + folder + '/nash_dist_agent_vs_opponents.svg', dpi=300, bbox_inches='tight')

    distance = 'Utility 1'
    score = {}
    for i in range(0, df.shape[0]):
        if df['Agent 1'][i] == str(name):
            try:
                score[df['Agent 2'][i]].append(df[distance][i])
            except KeyError:
                score[df['Agent 2'][i]] = []
                score[df['Agent 2'][i]].append(df[distance][i])
        elif df['Agent 2'][i] == str(name):
            try:
                score[df['Agent 1'][i]].append(df['Utility 2'][i])
            except KeyError:
                score[df['Agent 1'][i]] = []
                score[df['Agent 1'][i]].append(df['Utility 2'][i])

    plot_opp = []
    plot_dist = []
    for i in score.keys():
        plot_opp.append(i)
        plot_dist.append(np.mean(score[i]))

    figure(num=None, figsize=(6.66, 3.33), dpi=300, facecolor='w', edgecolor='k')
    plt.title(
        "Utility for " + str(name) + " (Mean: " + str(np.mean([x for x in plot_dist if str(x) != 'nan'])) + ")",
        fontsize=14)
    plt.ylim(0, 1.41)
    plt.xticks(fontsize=12, rotation=90)
    plt.yticks(fontsize=12)
    plt.bar(plot_opp, plot_dist)
    plt.ylabel("Average Agent Utility", fontsize=14)
    plt.xlabel("Opponents",fontsize=14)
    plt.savefig('log/' + folder + '/utility_agent_vs_opponents.svg', dpi=300, bbox_inches='tight')

    file = open('log/' + folder + '/report.md', "w")
    file.write("\n\n# Tournament Report \n")
    file.write("\n\n## Key Statistical Results \n")
    file.write("Agreements Reached: \n")
    file.writelines(str(result.Agreement.value_counts()))
    aggr_ratio = (result.Agreement.value_counts()['Yes']/sum(result.Agreement.value_counts().values))*100
    file.writelines("\n\nAgreement rate: " + str(aggr_ratio)+'%')
    file.write("\n\nNumber of matches won by " + str(name) + ': ')
    file.writelines(str(int(final_df['Matches Win'][final_df['Agents Name'] == str(name)].values)))
    win_ratio = (float(final_df['Matches Win'][final_df['Agents Name'] == str(name)].values)/float(final_df['N Matches'][final_df['Agents Name'] == str(name)].values))*100
    file.writelines("\n\nWinning Rate: " + str(win_ratio)+'%')
    min_nash = (1 - df['Dist. to Nash'].mean())
    file.write("\n\nOverall score: " + str((min_nash*result['Utility 1'].values.mean()*aggr_ratio/100)))
    result = result.reset_index(drop=True)
    # perc_error = []
    # for i in range(0, result.shape[0]):
    #     perc_error.append((abs(result['Perceived. Util. 1'][i] - result['Utility 1'][i]))/(result['Utility 1'][i]+1e-9)*100)
    # file.write("\n\nPercentage Error between Perceived Utility and Actual Utility: " + str(round(np.mean(perc_error), 3))+'%')
    percent_error = []
    for i in range(0, result.shape[0]):
        percent_error.append((abs(result['Utility 1'][i] - result['Perceived. Util. 1'][i]))/(result['Perceived. Util. 1'][i] +1e-9)*100)
    file.write("\n\nPercent Error between Perceived Utility and Actual Utility: " + str(round(np.mean(percent_error), 3))+'%')
    file.write("\n\nUsed Domains: " + str(result['Profile 1'].unique()))
    file.write("\n\n## Data Visualization \n")
    file.write("![](dist._to_Nash.svg)\n")
    file.write("![](agent_utility.svg)\n")
    file.write("![](distributions.svg)\n")
    file.write("![](nash_dist_agent_vs_opponents.svg)\n")
    file.write("![](utility_agent_vs_opponents.svg)\n")
    # file.write("![](summary1.png)\n")
    # file.write("![](summary2.png)")
    file.close()
